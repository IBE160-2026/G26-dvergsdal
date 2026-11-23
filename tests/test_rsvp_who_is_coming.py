"""Start the answer: who is coming (Story 2.1).

FR-12, FR-13, FR-14, FR-22, FR-41, AD-1, AD-7, AD-8, AD-11, UX-DR16, UX-DR18,
UX-DR19, UX-DR52. Every row of the story's I/O matrix over HTTP: step 1 for
two, one and four people, an unknown code, a missing or forged answer, a valid
«Fortsett» with someone or nobody coming, going back, «Bytt», a frame opened
too early, the deadline, a CSRF failure; and a full flow without JavaScript
that writes no row, makes no session and never uses messages. The draft
cookie's own cases are in test_rsvp_draft.py, the rules in test_deadline.py and
test_form_steps.py, the headers of the read views in test_guest_privacy.py.
How the form behaves in a real browser is MT-23 to MT-26 in
docs/manual-test-plan.md.
"""

import datetime
import re
import tomllib
from dataclasses import fields
from pathlib import Path

import pytest
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core import signing
from django.db import connection
from django.test import Client, RequestFactory
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from guests import views
from tests.helpers import checked_radios, page_text, row_counts
from wedding.actors import SYSTEM
from wedding.models import Guest, Household, Settings
from wedding.rsvp.draft import COOKIE_NAME, SALT
from wedding.rsvp.steps import DAYS as DAYS_REGISTRY
from wedding.services.settings import SettingsValues, update_settings

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
NAMES = {
    household["key"]: [guest["name"] for guest in household["guests"]]
    for household in SEED["households"]
}

SIGMUND = "test-sigmund0000000000"
ARILD = "test-arild000000000000"
SYNNE = "test-synne000000000000"
UNKNOWN = "AAAAAAAAAAAAAAAAAAAAAA"
STEP_1 = f"/{SIGMUND}/svar/"
DAYS = f"/{SIGMUND}/svar/dager/"
OVERNIGHT = f"/{SIGMUND}/svar/overnatting/"
MEALS = f"/{SIGMUND}/svar/maltider/"
ALLERGIES = f"/{SIGMUND}/svar/allergier/"
MONTHS = (
    "januar",
    "februar",
    "mars",
    "april",
    "mai",
    "juni",
    "juli",
    "august",
    "september",
    "oktober",
    "november",
    "desember",
)
SUMMARY_HEADING = "For å gå videre må du rette opp følgende feil."
CSRF_NOTICE = (
    "Feil: Skjemaet ble ikke sendt. Det skjer når siden har stått åpen lenge, eller når "
    "nettleseren ikke tar imot informasjonskapsler. Det du fylte ut, står her fortsatt. "
    "Prøv igjen."
)

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _ids(code: str) -> list[int]:
    household = Guest.objects.get(code=code).household
    return list(household.guests.order_by("id").values_list("id", flat=True))


def _answers(code: str, *coming: bool) -> dict[str, str]:
    return {
        f"attendance_{guest_id}": "yes" if answer else "no"
        for guest_id, answer in zip(_ids(code), coming, strict=True)
    }


def _title(html: str) -> str:
    return " ".join(re.search(r"<title>(.*?)</title>", html, re.DOTALL).group(1).split())


def _draft(response) -> dict:
    return signing.loads(response.cookies[COOKIE_NAME].value, salt=SALT)


def _fieldsets(html: str) -> list[str]:
    """The attendance groups (not the «Hvem svarer?» group inside «Bytt»)."""
    groups = re.findall(r"<fieldset\b[^>]*>.*?</fieldset>", html, re.DOTALL)
    return [group for group in groups if 'name="attendance_' in group]


def _set_deadline(deadline: datetime.date) -> None:
    row = Settings.objects.get()
    values = {field.name: getattr(row, field.name) for field in fields(SettingsValues)}
    update_settings(SYSTEM, SettingsValues(**(values | {"rsvp_deadline": deadline})))


# The I/O matrix


def test_open_step_1(client, seeded, django_assert_num_queries):
    """FR-12, FR-14, UX-DR18, UX-DR19: «Hvem kommer?», «Steg 1 av 6», «Jeg er
    Sigmund» with «Bytt», one group per member with nothing chosen, in three
    SELECTs, and no draft before «Fortsett»."""
    with django_assert_num_queries(3):
        response = client.get(STEP_1)
    assert response.status_code == 200
    html = response.content.decode()
    text = page_text(html)
    assert _title(html) == "Steg 1 av 6: Hvem kommer \N{EN DASH} Invitasjon"
    assert '<h1 id="sporsmal">Hvem kommer?</h1>' in html
    assert '<p class="form-progress">Steg 1 av 6: Hvem kommer</p>' in html
    assert "Jeg er Sigmund · Bytt hvem som svarer" in text
    assert [re.search(r"<legend>(.*?)</legend>", group).group(1) for group in _fieldsets(html)] == [
        "Sigmund",
        "bestemor",
    ]
    assert {name for name in checked_radios(html) if name.startswith("attendance_")} == set()
    assert COOKIE_NAME not in response.cookies
    assert re.search(r'method="post"\s+novalidate', html)
    assert "csrfmiddlewaretoken" in html


def test_the_page_follows_the_approved_order(client, seeded):
    """UX-DR18, DESIGN.md > Form step: question, progress line, respondent line,
    the groups, «Fortsett» above «Tilbake»; no nav bar, the footer band kept."""
    html = client.get(STEP_1).content.decode()
    marks = [
        "<h1 ",
        'class="form-progress"',
        'class="respondent"',
        "<legend>Sigmund</legend>",
        "<legend>bestemor</legend>",
        'value="continue">Fortsett</button>',
        'class="button button--secondary" href="/test-sigmund0000000000/#svar">Tilbake</a>',
        "<footer",
    ]
    positions = [html.index(mark) for mark in marks]
    assert positions == sorted(positions)
    assert "<nav" not in html
    assert "tel:" in html


def test_each_member_has_kommer_and_kommer_ikke(client, seeded):
    """FR-13: a radio «Kommer» and «Kommer ikke» per member, each in its label."""
    html = client.get(STEP_1).content.decode()
    for guest_id in _ids(SIGMUND):
        for value, word in (("yes", "Kommer"), ("no", "Kommer ikke")):
            assert re.search(
                rf'<label class="choice">\s*<input type="radio"\s+name="attendance_{guest_id}"\s+'
                rf'id="attendance_{guest_id}_{value}"\s+value="{value}"\s*>\s*{word}\s*</label>',
                html,
            )


def test_one_person_has_no_bytt(client, seeded):
    """FR-12: Synne answers alone, so there is nothing to switch."""
    html = client.get(f"/{SYNNE}/svar/").content.decode()
    assert "<details" not in html
    assert "Bytt" not in html
    assert "Jeg er Synne" in page_text(html)
    assert len(_fieldsets(html)) == 1


@pytest.mark.parametrize("path", [f"/{UNKNOWN}/svar/", f"/{UNKNOWN}/svar/dager/"])
@pytest.mark.parametrize("method", ["get", "post"])
def test_unknown_code_is_g1(client, seeded, django_assert_num_queries, path, method):
    """FR-5: an unknown code gives G1 with 404 after exactly one query."""
    with django_assert_num_queries(1):
        response = getattr(client, method)(path)
    assert response.status_code == 404
    assert response.content == client.get("/").content


def test_unknown_step_slug_is_not_found(client, seeded):
    """AD-7: an address under `/svar/` that is no step gives «Vi finner ikke denne siden»."""
    response = client.get(f"/{SIGMUND}/svar/finnes-ikke/")
    assert response.status_code == 404
    assert "Vi finner ikke denne siden" in response.content.decode()


def _assert_bestemor_missing(client, response) -> None:
    """FR-22, AD-7: the invalid POST keeps Sigmund's answer in the draft (step 1
    not done) and redirects 303 to `?feil=1`, whose GET shows bestemor's error."""
    sigmund, bestemor = _ids(SIGMUND)
    assert response.status_code == 303
    assert response["Location"] == f"{STEP_1}?feil=1"
    draft = _draft(response)
    assert draft["att"] == {str(sigmund): True}
    assert draft["done"] == []
    response = client.get(response["Location"])
    assert response.status_code == 200
    html = response.content.decode()
    assert _title(html) == "Feil: Steg 1 av 6: Hvem kommer \N{EN DASH} Invitasjon"
    summary = re.search(r'<div class="notice notice--error error-summary"[^>]*>', html).group(0)
    assert 'tabindex="-1"' in summary
    assert "autofocus" in summary
    assert html.index("error-summary") < html.index("<h1 ")
    assert SUMMARY_HEADING in html
    links = re.findall(r'<li>\s*<a href="(#[^"]+)">([^<]+)</a>\s*</li>', html)
    assert links == [(f"#attendance_{bestemor}_yes", "Velg om bestemor kommer")]
    groups = _fieldsets(html)
    assert f'aria-describedby="attendance_{bestemor}_error"' in groups[1]
    error_line = re.search(r'<p class="field-error" id="([^"]+)">(.*?)</p>', groups[1], re.DOTALL)
    assert error_line.group(1) == f"attendance_{bestemor}_error"
    assert page_text(error_line.group(2)) == (
        "Feil: Velg «Kommer» eller «Kommer ikke» for bestemor."
    )
    assert groups[1].index("</legend>") < groups[1].index("field-error")
    assert groups[1].count('aria-invalid="true"') == 2
    assert "aria-describedby" not in groups[0]
    assert "aria-invalid" not in groups[0]
    assert checked_radios(html) == {f"attendance_{sigmund}": "yes", "respondent": str(sigmund)}


def test_missing_answer_shows_the_errors(client, seeded):
    """FR-22, UX-DR16, AD-7: only Sigmund answered, so the step redirects to
    `?feil=1` (PRG), which shows «Feil: » in the title, a focused summary linking
    to bestemor's first radio, the error under her legend and Sigmund still chosen."""
    sigmund, _ = _ids(SIGMUND)
    _assert_bestemor_missing(client, client.post(STEP_1, {f"attendance_{sigmund}": "yes"}))


@pytest.mark.parametrize("forged", ["maybe", "", "YES", "1"])
def test_a_forged_value_is_an_error(client, seeded, forged):
    """FR-22: a value other than «yes» or «no» is treated as no answer."""
    sigmund, bestemor = _ids(SIGMUND)
    response = client.post(
        STEP_1, {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": forged}
    )
    _assert_bestemor_missing(client, response)


def test_a_foreign_member_id_is_ignored(client, seeded):
    """FR-12, AD-8: an answer for someone in another household is ignored, and the
    missing answer is still an error."""
    sigmund, _ = _ids(SIGMUND)
    arild = _ids(ARILD)[0]
    data = {f"attendance_{sigmund}": "yes", f"attendance_{arild}": "yes"}
    response = client.post(STEP_1, data)
    _assert_bestemor_missing(client, response)
    assert str(arild) not in str(_draft(response)["att"])


def test_valid_with_someone_coming_goes_to_the_days(client, seeded):
    """FR-13, AD-7, AD-8: 302 to `dager/`, the draft cookie on `/<code>/` with step 1
    done and everyone's answer."""
    sigmund, bestemor = _ids(SIGMUND)
    response = client.post(STEP_1, _answers(SIGMUND, True, False))
    assert response.status_code == 302
    assert response["Location"] == DAYS
    cookie = response.cookies[COOKIE_NAME]
    assert cookie["path"] == f"/{SIGMUND}/"
    assert cookie["httponly"] is True
    assert cookie["samesite"] == "Lax"
    assert not cookie["secure"]
    draft = _draft(response)
    assert draft["done"] == ["who"]
    assert draft["att"] == {str(sigmund): True, str(bestemor): False}
    assert draft["resp"] == sigmund


def test_errors_show_only_for_missing_answers(client, seeded):
    """FR-22: `?feil=1` with every answer saved shows the step without errors."""
    client.post(STEP_1, _answers(SIGMUND, True, False))
    html = client.get(f"{STEP_1}?feil=1").content.decode()
    assert not _title(html).startswith("Feil:")
    assert "error-summary" not in html
    assert "aria-invalid" not in html


def test_an_invalid_fortsett_keeps_the_chosen_respondent(client, seeded):
    """FR-12: a valid respondent posted with an invalid «Fortsett» is kept."""
    _, bestemor = _ids(SIGMUND)
    response = client.post(STEP_1, {"respondent": str(bestemor)})
    assert response.status_code == 303
    assert _draft(response)["resp"] == bestemor
    assert "Jeg er bestemor" in page_text(client.get(response["Location"]).content.decode())


def test_a_new_draft_starts_at_the_household_revision(client, seeded):
    """AD-8, AD-9: a new draft records the household's current revision."""
    Household.objects.filter(guests__code=SIGMUND).update(revision=3)
    assert _draft(client.post(STEP_1, _answers(SIGMUND, True, True)))["rev"] == 3


def test_valid_with_nobody_coming_goes_to_the_check_page(client, seeded):
    """FR-14, UX-DR19: when nobody comes there is no later step: 302 to `se-over/`,
    and step 1 then counts «Steg 1 av 1»."""
    response = client.post(f"/{ARILD}/svar/", _answers(ARILD, False, False, False, False))
    assert response.status_code == 302
    assert response["Location"] == f"/{ARILD}/svar/se-over/"
    html = client.get(f"/{ARILD}/svar/").content.decode()
    assert '<p class="form-progress">Steg 1 av 1: Hvem kommer</p>' in html
    check = client.get(f"/{ARILD}/svar/se-over/")
    assert check.status_code == 200
    check_html = check.content.decode()
    assert "<h1>Se over svaret før du sender</h1>" in check_html
    assert _title(check_html) == "Se over svaret før du sender \N{EN DASH} Invitasjon"
    assert f'href="/{ARILD}/svar/">Tilbake</a>' in check_html
    assert "<details" not in check_html


def test_going_back_shows_what_was_saved(client, seeded):
    """FR-78, AD-8: step 1 again after «Fortsett» shows the saved answers checked."""
    sigmund, bestemor = _ids(SIGMUND)
    client.post(STEP_1, _answers(SIGMUND, True, True))
    html = client.get(STEP_1).content.decode()
    assert '<p class="form-progress">Steg 1 av 6: Hvem kommer</p>' in html
    assert checked_radios(html) == {
        f"attendance_{sigmund}": "yes",
        f"attendance_{bestemor}": "yes",
        "respondent": str(sigmund),
    }


def test_changing_the_answer_replaces_it(client, seeded):
    """FR-13: a second «Fortsett» replaces every member's answer."""
    _, bestemor = _ids(SIGMUND)
    client.post(STEP_1, _answers(SIGMUND, True, True))
    response = client.post(STEP_1, _answers(SIGMUND, False, False))
    assert response["Location"] == f"/{SIGMUND}/svar/se-over/"
    assert _draft(response)["att"][str(bestemor)] is False
    assert _draft(response)["done"] == ["who"]


def test_bytt_switches_the_respondent_and_keeps_the_answers(client, seeded):
    """FR-12, UX-DR18: «Velg» sets the respondent, keeps Sigmund's chosen answer
    without validating the rest, and leaves step 1 not done."""
    sigmund, bestemor = _ids(SIGMUND)
    response = client.post(
        STEP_1,
        {"action": "switch", "respondent": str(bestemor), f"attendance_{sigmund}": "yes"},
    )
    assert response.status_code == 302
    assert response["Location"] == STEP_1
    draft = _draft(response)
    assert draft["resp"] == bestemor
    assert draft["done"] == []
    html = client.get(STEP_1).content.decode()
    assert "Jeg er bestemor" in page_text(html)
    assert checked_radios(html) == {f"attendance_{sigmund}": "yes", "respondent": str(bestemor)}
    assert client.get(DAYS)["Location"] == STEP_1


@pytest.mark.parametrize("respondent", ["foreign", "abc", "", "²"])
def test_bytt_with_a_foreign_respondent_changes_nothing(client, seeded, respondent):
    """FR-12: a respondent outside the household leaves the respondent unchanged."""
    sigmund, _ = _ids(SIGMUND)
    value = str(_ids(ARILD)[0]) if respondent == "foreign" else respondent
    response = client.post(STEP_1, {"action": "switch", "respondent": value})
    assert response.status_code == 302
    assert _draft(response)["resp"] == sigmund


def test_fortsett_applies_a_chosen_respondent(client, seeded):
    """FR-12: the respondent picked in «Bytt» counts on «Fortsett» too."""
    _, bestemor = _ids(SIGMUND)
    data = _answers(SIGMUND, True, True) | {"respondent": str(bestemor)}
    assert _draft(client.post(STEP_1, data))["resp"] == bestemor


def test_bytt_markup_works_without_javascript(client, seeded):
    """UX-DR18, AD-1: «Bytt» is a summary with the accessible name «Bytt hvem som
    svarer»; inside, «Hvem svarer?» with one radio per member, the respondent
    checked, and «Velg» as a secondary submit button."""
    sigmund, bestemor = _ids(SIGMUND)
    html = client.get(STEP_1).content.decode()
    details = html[html.index("<details") : html.index("</details>")]
    assert re.search(
        r"<summary>\s*Bytt<span class=\"visually-hidden\"> hvem som svarer</span>\s*</summary>",
        details,
    )
    assert "<legend>Hvem svarer?</legend>" in details
    assert re.findall(r'name="respondent"\s+value="(\d+)"', details) == [
        str(sigmund),
        str(bestemor),
    ]
    assert re.search(
        r'<button class="button button--secondary respondent__choose"\s+type="submit"\s+'
        r'name="action"\s+value="switch">Velg</button>',
        details,
    )


def test_enter_in_a_radio_submits_as_fortsett(client, seeded):
    """UX-DR18: the form's first submit button, which Enter in a radio uses, is a
    hidden «Fortsett» with no name, before «Velg»; it is never focusable."""
    html = client.get(STEP_1).content.decode()
    form = html[html.index("<form") :]
    first = re.search(r"<button[^>]*>[^<]*</button>", form).group(0)
    assert first == '<button type="submit" hidden>Fortsett</button>'
    assert form.index(first) < form.index('value="switch"')


def test_a_frame_before_step_1_goes_to_step_1(client, seeded):
    """AD-7: a later step without step 1 done redirects to step 1."""
    for path in (DAYS, f"/{SIGMUND}/svar/fjelltur/", f"/{SIGMUND}/svar/se-over/"):
        response = client.get(path)
        assert response.status_code == 302
        assert response["Location"] == STEP_1


def _through_step_2(client) -> None:
    """Story 2.2: both coming, the whole weekend."""
    client.post(STEP_1, _answers(SIGMUND, True, True))
    client.post(DAYS, {"whole": "yes"})


def _through_step_4(client) -> None:
    """Stories 2.2, 2.3: both coming the whole weekend, neither staying, no meal, so
    the frames after step 4 open."""
    sigmund, bestemor = _ids(SIGMUND)
    _through_step_2(client)
    client.post(OVERNIGHT, {f"overnight_{sigmund}": "no", f"overnight_{bestemor}": "no"})
    client.post(MEALS, {"action": "continue"})


def test_a_frame_shows_where_the_guest_is(client, seeded):
    """AD-7, UX-DR19: the allergies frame has the step's name as `h1`, «Steg 5 av 6:
    Allergier og matbehov», the respondent line with «Bytt» and «Tilbake» to
    step 4; no groups, no «Fortsett» and no script."""
    _through_step_4(client)
    html = client.get(ALLERGIES).content.decode()
    assert '<h1 id="sporsmal">Allergier og matbehov</h1>' in html
    assert '<p class="form-progress">Steg 5 av 6: Allergier og matbehov</p>' in html
    assert _title(html) == "Steg 5 av 6: Allergier og matbehov \N{EN DASH} Invitasjon"
    assert "Jeg er Sigmund · Bytt hvem som svarer" in page_text(html)
    assert f'href="{MEALS}">Tilbake</a>' in html
    assert _fieldsets(html) == []
    assert "Fortsett" not in html
    assert "<script" not in html
    # Story 2.2: a later frame opens only when every step before it is done.
    assert client.get(f"/{SIGMUND}/svar/fjelltur/")["Location"] == ALLERGIES


def test_a_frame_that_does_not_apply_goes_on(client, seeded):
    """AD-7: with nobody coming, a later step's address goes to the check page."""
    client.post(STEP_1, _answers(SIGMUND, False, False))
    response = client.get(DAYS)
    assert response.status_code == 302
    assert response["Location"] == f"/{SIGMUND}/svar/se-over/"


def test_a_post_to_a_frame_only_handles_bytt(client, seeded):
    """AD-7: a POST to a frame without `switch` goes back to the frame and changes
    nothing; with `switch` it sets the respondent."""
    _, bestemor = _ids(SIGMUND)
    _through_step_4(client)
    response = client.post(ALLERGIES, {"action": "continue"})
    assert response.status_code == 302
    assert response["Location"] == ALLERGIES
    assert COOKIE_NAME not in response.cookies
    response = client.post(ALLERGIES, {"action": "switch", "respondent": str(bestemor)})
    assert response["Location"] == ALLERGIES
    assert _draft(response)["resp"] == bestemor
    assert _draft(response)["done"] == ["who", "days", "overnight", "meals"]


def _closed(response) -> None:
    assert response.status_code == 200
    html = response.content.decode()
    assert "Svarfristen har gått ut" in html
    text = page_text(html)
    assert "Fristen gikk ut fredag 20. november 2026 kl. 23:59." in text
    assert "Send oss en melding, så finner vi ut av det." in text
    assert f'<a class="button button--on-green" href="/{SIGMUND}/">Tilbake' in html
    assert len(re.findall(r'href="tel:', html)) == 2
    assert COOKIE_NAME not in response.cookies


@pytest.mark.parametrize("path", [STEP_1, DAYS, f"/{SIGMUND}/svar/se-over/"])
def test_after_the_deadline_the_form_is_closed(client, seeded, monkeypatch, path):
    """FR-41, AD-11: after the deadline every RSVP address, GET and POST, shows
    «Svarfristen har gått ut» with the deadline as a weekday date, the back
    button and the phones, with status 200 and no draft."""
    monkeypatch.setattr(
        timezone, "now", lambda: datetime.datetime(2026, 11, 21, 12, tzinfo=datetime.UTC)
    )
    _set_deadline(datetime.date(2026, 11, 20))
    before = row_counts()
    _closed(client.get(path))
    _closed(client.post(path, _answers(SIGMUND, True, True)))
    assert row_counts() == before


def test_on_the_deadline_day_the_form_is_open(client, seeded):
    """FR-41: the deadline day itself is still open."""
    _set_deadline(timezone.localdate())
    assert client.post(STEP_1, _answers(SIGMUND, True, True)).status_code == 302
    _set_deadline(timezone.localdate() - datetime.timedelta(days=1))
    assert "Svarfristen har gått ut" in client.get(STEP_1).content.decode()


# CSRF on a step (UX-DR52)


def test_csrf_failure_on_step_1_keeps_the_choices(seeded):
    """UX-DR52: posted without a token, step 1 comes back with 403, the choice kept,
    a focused notice to try again, no draft and a fresh token; posting again with
    the page's token goes on."""
    sigmund, bestemor = _ids(SIGMUND)
    client = Client(enforce_csrf_checks=True)
    response = client.post(STEP_1, {f"attendance_{sigmund}": "yes"})
    assert response.status_code == 403
    html = response.content.decode()
    assert '<h1 id="sporsmal">Hvem kommer?</h1>' in html
    assert checked_radios(html) == {f"attendance_{sigmund}": "yes", "respondent": str(sigmund)}
    notice = re.search(r'<div class="notice notice--error"[^>]*>(.*?)</div>', html, re.DOTALL)
    assert 'tabindex="-1" autofocus' in notice.group(0)
    assert page_text(notice.group(1)) == CSRF_NOTICE
    assert "error-summary" not in html
    assert "aria-invalid" not in html
    assert COOKIE_NAME not in response.cookies
    token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html).group(1)
    data = {"csrfmiddlewaretoken": token, f"attendance_{bestemor}": "yes"}
    response = client.post(STEP_1, data | {f"attendance_{sigmund}": "yes"})
    assert response.status_code == 302
    assert response["Location"] == DAYS


def test_csrf_failure_keeps_the_saved_draft_under_the_posted_choices(seeded):
    """UX-DR52, AD-8: saved answers stay checked, and a posted choice wins."""
    sigmund, bestemor = _ids(SIGMUND)
    client = Client()
    client.post(STEP_1, _answers(SIGMUND, True, True))
    client.handler.enforce_csrf_checks = True
    response = client.post(STEP_1, {f"attendance_{bestemor}": "no"})
    assert response.status_code == 403
    assert checked_radios(response.content.decode()) == {
        f"attendance_{sigmund}": "yes",
        f"attendance_{bestemor}": "no",
        "respondent": str(sigmund),
    }


def test_csrf_failure_on_a_frame_shows_the_frame(seeded):
    """UX-DR52: a frame posted without a token comes back with its notice."""
    client = Client()
    _through_step_4(client)
    client.handler.enforce_csrf_checks = True
    response = client.post(ALLERGIES, {"action": "switch"})
    assert response.status_code == 403
    html = response.content.decode()
    assert '<h1 id="sporsmal">Allergier og matbehov</h1>' in html
    assert CSRF_NOTICE in page_text(html)


def test_csrf_failure_on_a_frame_before_step_2_is_the_generic_page(seeded):
    """UX-DR52, AD-7: with step 2 not done, the overnight frame cannot have been
    posted from, so a CSRF failure there gets the generic page, not the frame."""
    client = Client()
    client.post(STEP_1, _answers(SIGMUND, True, True))
    client.handler.enforce_csrf_checks = True
    response = client.post(OVERNIGHT, {"action": "switch"})
    assert response.status_code == 403
    html = response.content.decode()
    assert '<h1 class="private-invitation__heading">Skjemaet ble ikke sendt</h1>' in html
    assert "Hvem skal overnatte" not in html


@pytest.mark.parametrize(
    "path",
    [
        f"/{SIGMUND}/svar/se-over/",
        f"/{SIGMUND}/svar/dager/",
        f"/{SIGMUND}/svar/finnes-ikke/",
        f"/{UNKNOWN}/svar/",
    ],
)
def test_csrf_failure_elsewhere_under_svar_is_the_generic_page(seeded, path):
    """UX-DR52, FR-5: the check page has no form, a frame needs step 1 done, an
    unknown slug or code is no step: each gets the generic CSRF page."""
    response = Client(enforce_csrf_checks=True).post(path)
    assert response.status_code == 403
    assert '<h1 class="private-invitation__heading">Skjemaet ble ikke sendt</h1>' in (
        response.content.decode()
    )


@pytest.mark.parametrize("path", [STEP_1, DAYS])
def test_csrf_failure_after_the_deadline_is_the_closed_page(seeded, path):
    """FR-41, AD-11: after the deadline every step address shows the closed page,
    also for a POST with a stale token."""
    _set_deadline(timezone.localdate() - datetime.timedelta(days=1))
    response = Client(enforce_csrf_checks=True).post(path)
    assert response.status_code == 200
    html = response.content.decode()
    assert '<h1 class="private-invitation__heading">Svarfristen har gått ut</h1>' in html
    assert "Skjemaet ble ikke sendt" not in html
    assert COOKIE_NAME not in response.cookies


def test_csrf_failure_on_velg_shows_the_posted_respondent(seeded):
    """UX-DR52, FR-12: «Velg» posted without a token comes back with the chosen
    respondent in the line, private and never stored, and writes no draft."""
    _, bestemor = _ids(SIGMUND)
    response = Client(enforce_csrf_checks=True).post(
        STEP_1, {"action": "switch", "respondent": str(bestemor)}
    )
    assert response.status_code == 403
    assert "Jeg er bestemor" in page_text(response.content.decode())
    assert "private" in response["Cache-Control"]
    assert "no-store" in response["Cache-Control"]
    assert COOKIE_NAME not in response.cookies


def test_csrf_failure_deletes_a_broken_draft(seeded):
    """AD-8, UX-DR52: a broken draft is deleted on the 403 re-render too."""
    client = Client(enforce_csrf_checks=True)
    client.cookies[COOKIE_NAME] = "broken"
    response = client.post(STEP_1)
    assert response.status_code == 403
    assert response.cookies[COOKIE_NAME]["max-age"] == 0
    assert response.cookies[COOKIE_NAME]["path"] == f"/{SIGMUND}/"


def test_csrf_failure_falls_back_to_the_generic_page_on_any_error(seeded, monkeypatch):
    """FR-5: if the step cannot be shown again, the generic page is shown."""

    def broken(*args, **kwargs):
        raise RuntimeError("broken")

    monkeypatch.setattr(views, "render_after_csrf_failure", broken)
    response = Client(enforce_csrf_checks=True).post(STEP_1)
    assert response.status_code == 403
    assert '<h1 class="private-invitation__heading">Skjemaet ble ikke sendt</h1>' in (
        response.content.decode()
    )
    assert "tel:" in response.content.decode()


# The whole flow without JavaScript (AD-1, AD-8)


def test_the_whole_flow_writes_nothing_and_uses_no_session(client, seeded, monkeypatch):
    """AD-1, AD-8, FR-3: GET, an invalid POST, a valid POST, the next frame and a
    switch: no row created or changed, no session, no session or messages cookie,
    messages never called, no script, three SELECTs per request, and every
    response is private and never stored."""

    def no_messages(*args, **kwargs):
        raise AssertionError("the messages framework must not be used")

    monkeypatch.setattr(messages, "add_message", no_messages)
    sigmund, bestemor = _ids(SIGMUND)
    before = row_counts()
    revisions = list(Household.objects.values_list("id", "revision"))
    requests = [
        ("get", STEP_1, {}, 200),
        ("post", STEP_1, {f"attendance_{sigmund}": "yes"}, 303),
        ("get", f"{STEP_1}?feil=1", {}, 200),
        ("post", STEP_1, _answers(SIGMUND, True, False), 302),
        ("get", DAYS, {}, 200),
        ("post", DAYS, {"action": "switch", "respondent": str(bestemor)}, 302),
        ("get", DAYS, {}, 200),
        ("post", STEP_1, {"action": "switch", "respondent": str(sigmund)}, 302),
        ("get", STEP_1, {}, 200),
    ]
    for method, path, data, status in requests:
        with CaptureQueriesContext(connection) as captured:
            response = getattr(client, method)(path, data)
        assert response.status_code == status, (method, path)
        sql = [query["sql"] for query in captured.captured_queries]
        assert len(sql) == 3, (method, path, sql)
        assert all(statement.lstrip().upper().startswith("SELECT") for statement in sql)
        assert "private" in response["Cache-Control"]
        assert "no-store" in response["Cache-Control"]
        assert "<script" not in response.content.decode()
        assert "sessionid" not in response.cookies
        assert "messages" not in response.cookies
    assert "Jeg er Sigmund" in page_text(response.content.decode())
    assert row_counts() == before
    assert list(Household.objects.values_list("id", "revision")) == revisions
    assert Session.objects.count() == 0


def test_head_works_and_other_methods_are_refused(client, seeded):
    """AD-7: the RSVP addresses answer GET, HEAD and POST only."""
    assert client.head(STEP_1).status_code == 200
    assert client.put(STEP_1).status_code == 405
    assert client.delete(DAYS).status_code == 405


@pytest.mark.parametrize(("view", "kwargs"), [("rsvp", {}), ("rsvp_step", {"slug": "dager"})])
def test_rsvp_views_hide_posted_values_from_error_reports(seeded, view, kwargs):
    """AD-15: the RSVP views use `sensitive_post_parameters`, so an error report
    never shows what a guest posted."""
    request = RequestFactory().post(f"/{SIGMUND}/svar/", {"attendance_1": "yes"})
    request._dont_enforce_csrf_checks = True
    getattr(views, view)(request, code=SIGMUND, **kwargs)
    assert request.sensitive_post_parameters == "__ALL__"


def test_no_name_or_date_is_written_in_the_templates():
    """AD-17, Stories 2.1, 2.2: names come from the household, the deadline from the
    settings and the days' dates from the step registry; no guest name, price,
    year or day-and-month date is template text in the form."""
    folder = Path(__file__).resolve().parent.parent / "wedding" / "rsvp" / "templates"
    sources = " ".join(path.read_text(encoding="utf-8") for path in folder.rglob("*.html"))
    sources += (
        Path(__file__).resolve().parent.parent
        / "guests"
        / "templates"
        / "guests"
        / "rsvp_closed.html"
    ).read_text(encoding="utf-8")
    for name in (name for names in NAMES.values() for name in names):
        assert not re.search(rf"\b{re.escape(name)}\b", sources), name
    assert not re.search(r"\b20\d\d\b", sources)
    assert not re.search(rf"\d{{1,2}}\. ({'|'.join(MONTHS)})\b", sources)
    assert " kr" not in sources


def test_every_day_name_and_date_is_the_programme_s():
    """FR-14, FR-70, AD-17: the dates live once in the form's `DAYS`; each day's name
    and date are also the programme page's, so the two cannot drift apart."""
    programme = (
        Path(__file__).resolve().parent.parent
        / "guests"
        / "templates"
        / "guests"
        / "programme.html"
    ).read_text(encoding="utf-8")
    for day in DAYS_REGISTRY.values():
        assert re.search(
            rf'<h2 id="[a-z]+-overskrift">{day.name}</h2>\s*'
            rf'<p class="programme-day__date">\s*{re.escape(day.date)}',
            programme,
        ), day.label
