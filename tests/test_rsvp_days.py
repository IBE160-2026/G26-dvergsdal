"""Which days each person comes: step 2 of the RSVP form (Story 2.2).

FR-14, FR-17, FR-22, FR-70, FR-75, AD-1, AD-7, AD-8, UX-DR16, UX-DR19,
UX-DR52. Every row of the story's I/O matrix over HTTP: opening step 2, «Ja»,
the reveal after «Nei», a gap, no day, no «Ja»/«Nei», valid days, the step
count following the days, a person who stops coming or starts coming, nobody
coming, the gate on later steps, a broken draft and a CSRF failure. Also
«Velg» on step 2, Enter as «Fortsett», and a flow that writes no row, uses no
session and is never cached. The rules are in test_days_rules.py and
test_form_steps.py; the browser runs are MT-27 to MT-29 in
docs/manual-test-plan.md.
"""

import re

import pytest
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core import signing
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext

from tests.helpers import checked_radios, page_text, row_counts, ticked_boxes
from wedding.links import new_code
from wedding.models import Guest
from wedding.rsvp.draft import COOKIE_NAME, SALT

ARILD = "test-arild000000000000"
SYNNE = "test-synne000000000000"
SIGMUND = "test-sigmund0000000000"
ALL = ["fri", "sat", "sun"]
GAP_TEXT = (
    "Feil: Filippa kan ikke komme fredag og søndag uten lørdag, fordi dagene må komme "
    "etter hverandre. Velg lørdag også, eller bare én av dagene."
)

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _ids(code: str) -> list[int]:
    household = Guest.objects.get(code=code).household
    return list(household.guests.order_by("id").values_list("id", flat=True))


def _url(code: str, slug: str = "") -> str:
    return f"/{code}/svar/{slug}/" if slug else f"/{code}/svar/"


def _answers(code: str, *coming: bool) -> dict[str, str]:
    return {
        f"attendance_{guest_id}": "yes" if answer else "no"
        for guest_id, answer in zip(_ids(code), coming, strict=True)
    }


def _draft(response) -> dict:
    return signing.loads(response.cookies[COOKIE_NAME].value, salt=SALT)


def _title(html: str) -> str:
    return " ".join(re.search(r"<title>(.*?)</title>", html, re.DOTALL).group(1).split())


def _progress(html: str) -> str:
    return re.search(r'<p class="form-progress">(.*?)</p>', html).group(1)


def _day_groups(html: str) -> list[str]:
    groups = re.findall(r"<fieldset\b[^>]*>.*?</fieldset>", html, re.DOTALL)
    return [group for group in groups if 'name="days_' in group]


def _legend(group: str) -> str:
    return re.search(r"<legend>(.*?)</legend>", group).group(1)


def _arild_to_step_2(client) -> None:
    """Arild, Marie and Filippa «Kommer», Leone «Kommer ikke»."""
    response = client.post(_url(ARILD), _answers(ARILD, True, True, True, False))
    assert response["Location"] == _url(ARILD, "dager")


def _days(code: str, **chosen: list[str]) -> dict[str, list[str]]:
    """POST data for «Nei» with days, by position name a/b/c/d in the household."""
    ids = _ids(code)
    data = {"whole": "no"}
    for position, days in chosen.items():
        data[f"days_{ids['abcd'.index(position)]}"] = days
    return data


def _arild_revealed(client) -> None:
    _arild_to_step_2(client)
    response = client.post(_url(ARILD, "dager"), {"whole": "no"})
    assert response["Location"] == f"{_url(ARILD, 'dager')}#velg-dager"


# The I/O matrix


def test_open(client, seeded, django_assert_num_queries):
    """FR-14, FR-70, UX-DR19: «Steg 2 av 6: Dager», the question as `h1`, the three
    days with dates and what happens, «Ja»/«Nei» with nothing chosen, no day
    checkbox yet, in four SELECTs (Story 2.8 adds the answer check)."""
    _arild_to_step_2(client)
    with django_assert_num_queries(4):
        response = client.get(_url(ARILD, "dager"))
    assert response.status_code == 200
    html = response.content.decode()
    assert _title(html) == "Steg 2 av 6: Dager \N{EN DASH} Invitasjon"
    assert '<h1 id="sporsmal">Er alle som kommer, med hele helgen?</h1>' in html
    assert _progress(html) == "Steg 2 av 6: Dager"
    text = page_text(html)
    for line in (
        "Fredag 26. mai : Fjelltur, middag og rebus",
        "Lørdag 27. mai : Bryllupsdagen: vielse, lunsj og fest",
        "Søndag 28. mai : Frokost og hjemreise",
    ):
        assert line in text
    assert "<strong>Fredag 26. mai</strong>" in html
    assert re.search(r'<fieldset class="form-group"\s+aria-labelledby="sporsmal"', html)
    assert "Ja, alle er med fra fredag til søndag" in text
    assert "Nei, jeg velger dager for hver person" in text
    assert 'id="whole_yes"' in html
    assert checked_radios(html) == {"respondent": str(_ids(ARILD)[0])}
    assert 'type="checkbox"' not in html
    assert "velg-dager" not in html


def test_the_page_follows_the_order(client, seeded):
    """UX-DR19, DESIGN.md, Form step: question, progress, respondent, days,
    «Ja»/«Nei», «Fortsett» above «Tilbake» to step 1."""
    _arild_to_step_2(client)
    html = client.get(_url(ARILD, "dager")).content.decode()
    marks = [
        "<h1",
        'class="form-progress"',
        'class="respondent"',
        'class="day-list"',
        'id="whole_yes"',
        'id="whole_no"',
        'value="continue">Fortsett</button>',
        f'href="{_url(ARILD)}">Tilbake</a>',
    ]
    positions = [html.index(mark) for mark in marks]
    assert positions == sorted(positions)


def test_ja(client, seeded):
    """FR-14: «Ja» completes the step and goes to the overnight step."""
    _arild_to_step_2(client)
    response = client.post(_url(ARILD, "dager"), {"whole": "yes"})
    assert response.status_code == 302
    assert response["Location"] == _url(ARILD, "overnatting")
    draft = _draft(response)
    assert draft["whole"] is True
    assert draft["days"] == {}
    assert draft["done"] == ["who", "days"]


def test_reveal(client, seeded):
    """FR-14, AD-7: «Nei» the first time saves «Nei» and shows the day groups at
    the same address: one per coming person (not Leone), nothing ticked, still
    «Steg 2 av 6»; not an error."""
    _arild_to_step_2(client)
    response = client.post(_url(ARILD, "dager"), {"whole": "no"})
    assert response.status_code == 302
    assert response["Location"] == f"{_url(ARILD, 'dager')}#velg-dager"
    draft = _draft(response)
    assert draft["whole"] is False
    assert draft["done"] == ["who"]
    html = client.get(_url(ARILD, "dager")).content.decode()
    assert checked_radios(html)["whole"] == "no"
    assert (
        '<h2 class="day-groups__heading" id="velg-dager">Velg dagene for hver person</h2>' in html
    )
    groups = _day_groups(html)
    assert [_legend(group) for group in groups] == ["Arild", "Marie", "Filippa"]
    assert sum(group.count('type="checkbox"') for group in groups) == 9
    assert ticked_boxes(html) == []
    assert _progress(html) == "Steg 2 av 6: Dager"
    assert "error-summary" not in html
    arild = _ids(ARILD)[0]
    assert re.search(
        rf'<input type="checkbox"\s+name="days_{arild}"\s+id="days_{arild}_fri"\s+value="fri"\s*>'
        r"\s*Fredag 26. mai\s*</label>",
        html,
    )


def test_gap(client, seeded):
    """FR-14, FR-22, FR-70: Friday + Sunday for Filippa is refused with one summary
    link, the explanation under her legend, and her boxes still ticked."""
    _arild_revealed(client)
    filippa = _ids(ARILD)[2]
    response = client.post(_url(ARILD, "dager"), _days(ARILD, a=ALL, b=ALL, c=["fri", "sun"]))
    assert response.status_code == 303
    assert response["Location"] == f"{_url(ARILD, 'dager')}?feil=1"
    assert "days" not in _draft(response)["done"]
    html = client.get(response["Location"]).content.decode()
    assert _title(html).startswith("Feil: Steg 2 av 6: Dager")
    summary = re.search(r'<div class="notice notice--error error-summary"[^>]*>', html).group(0)
    assert 'tabindex="-1"' in summary
    assert "autofocus" in summary
    links = re.findall(r'<li>\s*<a href="(#[^"]+)">([^<]+)</a>\s*</li>', html)
    assert links == [(f"#days_{filippa}_fri", "Velg dager for Filippa")]
    group = _day_groups(html)[2]
    assert f'aria-describedby="days_{filippa}_error"' in group
    error = re.search(r'<p class="field-error" id="([^"]+)">(.*?)</p>', group, re.DOTALL)
    assert error.group(1) == f"days_{filippa}_error"
    assert page_text(error.group(2)) == GAP_TEXT
    assert group.index("</legend>") < group.index("field-error")
    assert group.count('aria-invalid="true"') == 3
    assert "aria-invalid" not in _day_groups(html)[0]
    assert [box for box in ticked_boxes(html) if box.startswith(f"days_{filippa}_")] == [
        f"days_{filippa}_fri",
        f"days_{filippa}_sun",
    ]


def test_no_day(client, seeded):
    """FR-14, FR-22: no day for Marie is «Velg minst én dag for Marie.»."""
    _arild_revealed(client)
    response = client.post(_url(ARILD, "dager"), _days(ARILD, a=ALL, c=ALL))
    assert response.status_code == 303
    html = client.get(response["Location"]).content.decode()
    assert "Feil: Velg minst én dag for Marie." in page_text(html)
    links = re.findall(r'<li>\s*<a href="(#[^"]+)">([^<]+)</a>\s*</li>', html)
    assert links == [(f"#days_{_ids(ARILD)[1]}_fri", "Velg dager for Marie")]


@pytest.mark.parametrize("data", [{}, {"whole": "maybe"}, {"whole": ""}])
def test_no_whole(client, seeded, data):
    """FR-22: no or a forged «Ja»/«Nei» gives «Velg «Ja» eller «Nei».», linked to «Ja»."""
    _arild_to_step_2(client)
    response = client.post(_url(ARILD, "dager"), data)
    assert response.status_code == 303
    assert response["Location"] == f"{_url(ARILD, 'dager')}?feil=1"
    html = client.get(response["Location"]).content.decode()
    links = re.findall(r'<li>\s*<a href="(#[^"]+)">([^<]+)</a>\s*</li>', html)
    assert links == [("#whole_yes", "Svar på om alle er med hele helgen")]
    assert "Feil: Velg «Ja» eller «Nei»." in page_text(html)
    assert 'aria-describedby="whole_error"' in html
    assert html.count('aria-invalid="true"') == 2


def test_valid_days(client, seeded):
    """FR-14, FR-70: Filippa Saturday + Sunday, the others all: on to step 3 of 6."""
    _arild_revealed(client)
    ids = _ids(ARILD)
    response = client.post(_url(ARILD, "dager"), _days(ARILD, a=ALL, b=ALL, c=["sun", "sat"]))
    assert response.status_code == 302
    assert response["Location"] == _url(ARILD, "overnatting")
    draft = _draft(response)
    assert draft["done"] == ["who", "days"]
    assert draft["days"] == {str(ids[0]): ALL, str(ids[1]): ALL, str(ids[2]): ["sat", "sun"]}
    html = client.get(response["Location"]).content.decode()
    assert _progress(html) == "Steg 3 av 6: Overnatting"


def test_m_follows_the_days(client, seeded):
    """FR-17, UX-DR19: Synne on Saturday only has no overnight, meals or hike: step
    3 of 3 is allergies, and back on step 2 it says «Steg 2 av 3»."""
    synne = _ids(SYNNE)[0]
    client.post(_url(SYNNE), _answers(SYNNE, True))
    client.post(_url(SYNNE, "dager"), {"whole": "no"})
    response = client.post(_url(SYNNE, "dager"), {"whole": "no", f"days_{synne}": "sat"})
    assert response["Location"] == _url(SYNNE, "allergier")
    assert _progress(client.get(response["Location"]).content.decode()) == (
        "Steg 3 av 3: Allergier og matbehov"
    )
    html = client.get(_url(SYNNE, "dager")).content.decode()
    assert _progress(html) == "Steg 2 av 3: Dager"
    assert ticked_boxes(html) == [f"days_{synne}_sat"]
    assert client.get(_url(SYNNE, "overnatting"))["Location"] == _url(SYNNE, "allergier")


def test_someone_who_stops_coming_loses_their_days(client, seeded):
    """FR-75: Filippa «Kommer ikke» after her days are chosen: her days are gone and
    step 2 stays done."""
    _arild_revealed(client)
    client.post(_url(ARILD, "dager"), _days(ARILD, a=ALL, b=ALL, c=["sat", "sun"]))
    response = client.post(_url(ARILD), _answers(ARILD, True, True, False, False))
    draft = _draft(response)
    assert str(_ids(ARILD)[2]) not in draft["days"]
    assert draft["done"] == ["who", "days"]
    assert response["Location"] == _url(ARILD, "dager")


def test_a_new_comer_reopens_step_2(client, seeded):
    """FR-75, AD-7: Leone starts coming after «Nei» with days: step 2 is not done,
    and the check page sends the guest back to it."""
    _arild_revealed(client)
    client.post(_url(ARILD, "dager"), _days(ARILD, a=ALL, b=ALL, c=["sat", "sun"]))
    response = client.post(_url(ARILD), _answers(ARILD, True, True, True, True))
    assert response["Location"] == _url(ARILD, "dager")
    assert "days" not in _draft(response)["done"]
    assert client.get(_url(ARILD, "se-over"))["Location"] == _url(ARILD, "dager")
    html = client.get(_url(ARILD, "dager")).content.decode()
    assert [_legend(group) for group in _day_groups(html)] == [
        "Arild",
        "Marie",
        "Filippa",
        "Leone",
    ]


def test_nobody_coming_after_days(client, seeded):
    """FR-75: everyone «Kommer ikke» after step 2: no «Ja»/«Nei», no days, check page."""
    _arild_revealed(client)
    client.post(_url(ARILD, "dager"), _days(ARILD, a=ALL, b=ALL, c=ALL))
    response = client.post(_url(ARILD), _answers(ARILD, False, False, False, False))
    assert response["Location"] == _url(ARILD, "se-over")
    draft = _draft(response)
    assert draft["whole"] is None
    assert draft["days"] == {}
    assert draft["done"] == ["who"]
    assert client.get(_url(ARILD, "se-over")).status_code == 200


@pytest.mark.parametrize("slug", ["overnatting", "fjelltur", "se-over"])
def test_gate(client, seeded, slug):
    """AD-7: with step 1 done and step 2 not, a later step goes to step 2."""
    _arild_to_step_2(client)
    response = client.get(_url(ARILD, slug))
    assert response.status_code == 302
    assert response["Location"] == _url(ARILD, "dager")


def test_step_2_before_step_1_goes_to_step_1(client, seeded):
    """AD-7: step 2 needs step 1 done."""
    assert client.get(_url(ARILD, "dager"))["Location"] == _url(ARILD)
    assert client.post(_url(ARILD, "dager"), {"whole": "yes"})["Location"] == _url(ARILD)


def test_broken_days_start_empty(client, seeded):
    """AD-8: a draft with `whole` "no" is broken: deleted, step 1 empty, no 500."""
    ids = _ids(ARILD)
    payload = {
        "v": 3,
        "started": "2026-11-21T10:00:00+00:00",
        "rev": 0,
        "resp": ids[0],
        "att": {str(guest_id): True for guest_id in ids},
        "done": ["who"],
        "whole": "no",
        "days": {},
        "night": {},
        "meals": {},
    }
    client.cookies[COOKIE_NAME] = signing.dumps(payload, salt=SALT, compress=True)
    response = client.get(_url(ARILD))
    assert response.status_code == 200
    assert response.cookies[COOKIE_NAME]["max-age"] == 0
    assert checked_radios(response.content.decode()) == {"respondent": str(ids[0])}


def test_csrf(seeded):
    """UX-DR52: «Nei» and Filippa's Saturday posted without a token: 403, «Nei»
    checked, the groups shown with Saturday ticked, no draft written."""
    client = Client()
    _arild_to_step_2(client)
    filippa = _ids(ARILD)[2]
    client.handler.enforce_csrf_checks = True
    response = client.post(_url(ARILD, "dager"), {"whole": "no", f"days_{filippa}": "sat"})
    assert response.status_code == 403
    html = response.content.decode()
    assert "Prøv igjen." in page_text(html)
    assert checked_radios(html)["whole"] == "no"
    assert len(_day_groups(html)) == 3
    assert ticked_boxes(html) == [f"days_{filippa}_sat"]
    assert COOKIE_NAME not in response.cookies
    assert "error-summary" not in html


def test_csrf_keeps_the_saved_groups(seeded):
    """UX-DR52: with «Nei» saved, the groups show even when nothing is posted."""
    client = Client()
    _arild_revealed(client)
    client.handler.enforce_csrf_checks = True
    response = client.post(_url(ARILD, "dager"))
    assert response.status_code == 403
    html = response.content.decode()
    assert checked_radios(html)["whole"] == "no"
    assert len(_day_groups(html)) == 3


# «Velg», Enter and the flow


def test_velg_on_step_2_keeps_the_choices(client, seeded):
    """FR-12, UX-DR18: «Velg» keeps the respondent, «Nei» and the ticked days
    without validating them, and stays on step 2."""
    _arild_revealed(client)
    ids = _ids(ARILD)
    data = _days(ARILD, c=["fri", "sun"]) | {"action": "switch", "respondent": str(ids[1])}
    response = client.post(_url(ARILD, "dager"), data)
    assert response.status_code == 302
    assert response["Location"] == _url(ARILD, "dager")
    draft = _draft(response)
    assert draft["resp"] == ids[1]
    assert draft["whole"] is False
    assert draft["days"] == {str(ids[2]): ["fri", "sun"]}
    assert draft["done"] == ["who"]
    html = client.get(_url(ARILD, "dager")).content.decode()
    assert "Jeg er Marie" in page_text(html)
    assert ticked_boxes(html) == [f"days_{ids[2]}_fri", f"days_{ids[2]}_sun"]
    assert "error-summary" not in html


def test_velg_before_the_reveal_keeps_ja_or_nei(client, seeded):
    """FR-12: «Velg» with «Nei» chosen but no groups saves «Nei»."""
    _arild_to_step_2(client)
    response = client.post(_url(ARILD, "dager"), {"action": "switch", "whole": "no"})
    assert _draft(response)["whole"] is False


def test_enter_submits_as_fortsett(client, seeded):
    """UX-DR18: the first button in the form is the hidden «Fortsett», before «Velg»."""
    _arild_revealed(client)
    html = client.get(_url(ARILD, "dager")).content.decode()
    form = html[html.index("<form") :]
    first = re.search(r"<button[^>]*>[^<]*</button>", form).group(0)
    assert first == '<button type="submit" hidden>Fortsett</button>'
    assert form.index(first) < form.index('value="switch"')


def test_the_flow_writes_nothing_and_is_never_cached(client, seeded, monkeypatch):
    """AD-1, AD-8, FR-3: steps 1 to 2 with an error, the reveal and «Velg»: no row,
    no session, no messages, no script, four SELECTs per request (Story 2.8 adds the answer
    check), and every
    response private and never stored."""

    def no_messages(*args, **kwargs):
        raise AssertionError("the messages framework must not be used")

    monkeypatch.setattr(messages, "add_message", no_messages)
    ids = _ids(ARILD)
    days = _url(ARILD, "dager")
    before = row_counts()
    requests = [
        ("post", _url(ARILD), _answers(ARILD, True, True, True, False), 302),
        ("get", days, {}, 200),
        ("post", days, {}, 303),
        ("get", f"{days}?feil=1", {}, 200),
        ("post", days, {"whole": "no"}, 302),
        ("get", days, {}, 200),
        ("post", days, {"action": "switch", "respondent": str(ids[1])}, 302),
        ("post", days, _days(ARILD, a=ALL, b=["fri"], c=["fri", "sun"]), 303),
        ("get", f"{days}?feil=1", {}, 200),
        ("post", days, _days(ARILD, a=ALL, b=["fri"], c=["sat"]), 302),
        ("get", _url(ARILD, "overnatting"), {}, 200),
    ]
    for method, path, data, status in requests:
        with CaptureQueriesContext(connection) as captured:
            response = getattr(client, method)(path, data)
        assert response.status_code == status, (method, path)
        sql = [query["sql"] for query in captured.captured_queries]
        assert len(sql) == 4, (method, path, sql)
        assert all(statement.lstrip().upper().startswith("SELECT") for statement in sql)
        assert "private" in response["Cache-Control"]
        assert "no-store" in response["Cache-Control"]
        # Story 2.3: only the paid steps load the running total's script.
        scripts = 1 if path.endswith("/overnatting/") else 0
        assert response.content.decode().count("<script") == scripts
        assert "sessionid" not in response.cookies
        assert "messages" not in response.cookies
    assert row_counts() == before
    assert Session.objects.count() == 0


def test_one_person_has_one_group(client, seeded):
    """FR-14: Sigmund's household of two, bestemor not coming: one group after «Nei»."""
    client.post(_url(SIGMUND), _answers(SIGMUND, True, False))
    client.post(_url(SIGMUND, "dager"), {"whole": "no"})
    html = client.get(_url(SIGMUND, "dager")).content.decode()
    assert [_legend(group) for group in _day_groups(html)] == ["Sigmund"]


def test_no_day_for_anyone_after_the_reveal(client, seeded):
    """FR-14, FR-22: «Nei» again with no box ticked is an error for every coming
    person, and step 2 stays not done."""
    _arild_revealed(client)
    response = client.post(_url(ARILD, "dager"), {"whole": "no"})
    assert response.status_code == 303
    assert response["Location"] == f"{_url(ARILD, 'dager')}?feil=1"
    assert "days" not in _draft(response)["done"]
    html = client.get(response["Location"]).content.decode()
    text = page_text(html)
    links = re.findall(r'<li>\s*<a href="(#[^"]+)">([^<]+)</a>\s*</li>', html)
    ids = _ids(ARILD)
    assert links == [
        (f"#days_{guest_id}_fri", f"Velg dager for {name}")
        for guest_id, name in zip(ids, ["Arild", "Marie", "Filippa"], strict=False)
    ]
    for name in ("Arild", "Marie", "Filippa"):
        assert f"Feil: Velg minst én dag for {name}." in text


def test_changing_ja_to_nei_reopens_the_day_groups(client, seeded):
    """FR-14, FR-75: «Nei» after «Ja» was done reveals the groups and step 2 is
    no longer done."""
    _arild_to_step_2(client)
    client.post(_url(ARILD, "dager"), {"whole": "yes"})
    response = client.post(_url(ARILD, "dager"), {"whole": "no"})
    assert response["Location"] == f"{_url(ARILD, 'dager')}#velg-dager"
    draft = _draft(response)
    assert draft["whole"] is False
    assert "days" not in draft["done"]
    assert len(_day_groups(client.get(_url(ARILD, "dager")).content.decode())) == 3


def test_changing_nei_to_ja_drops_the_days(client, seeded):
    """FR-75, UX-DR19: «Ja» after «Nei» with days empties the days, and the steps
    are the whole weekend's again."""
    synne = _ids(SYNNE)[0]
    client.post(_url(SYNNE), _answers(SYNNE, True))
    client.post(_url(SYNNE, "dager"), {"whole": "no"})
    client.post(_url(SYNNE, "dager"), {"whole": "no", f"days_{synne}": "sat"})
    response = client.post(_url(SYNNE, "dager"), {"whole": "yes"})
    assert response["Location"] == _url(SYNNE, "overnatting")
    draft = _draft(response)
    assert draft["whole"] is True
    assert draft["days"] == {}
    assert draft["done"] == ["who", "days"]
    html = client.get(response["Location"]).content.decode()
    assert _progress(html) == "Steg 3 av 6: Overnatting"


@pytest.mark.parametrize("slug", ["overnatting", "se-over"])
def test_a_member_added_after_step_2_reopens_it(client, seeded, slug):
    """FR-75, AD-7, FR-78 (Story 2.9): a guest added to the household after
    step 1 is not in the draft's attendance, so the household changed: no step
    stays done and the gate sends a later step back to step 1."""
    _arild_revealed(client)
    client.post(_url(ARILD, "dager"), _days(ARILD, a=ALL, b=ALL, c=["sat", "sun"]))
    household = Guest.objects.get(code=ARILD).household
    Guest.objects.create(household=household, name="Ny", code=new_code())
    response = client.get(_url(ARILD, slug))
    assert response.status_code == 302
    assert response["Location"] == _url(ARILD)
