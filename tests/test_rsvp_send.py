"""«Send svaret» and «Svaret er sendt» over HTTP (Story 2.6a).

FR-12, FR-41, FR-74, AD-3, AD-7, AD-8, AD-15, UX-DR15, UX-DR24, UX-DR52. The
view rows of the story's I/O matrix: Sigmund's journey then send (rows, the
draft cookie deleted, 303 to `sendt/`), a switched respondent, the sent page
(its `h1`, the sent line in Oslo time, the link to the invitation, never
cached) and its 302 before any answer, the deadline passing at send, a member
missing from the draft, a POST without `action=send`, an unfinished step, a
CSRF failure on the check page, and the busy-state hooks on the check page.
Story 2.6b (FR-26, FR-28, AD-18): allergies stored only with «Ja», and a
re-send with consent unanswered warned about and keeping the stored data.
Story 2.6c (AD-7, AD-9, AD-18, AD-20, NFR-1, UX-DR52): the hidden
submission id and total, a double send, a late repeat without the draft, a
send from an older revision, a changed price, a failed database write, a
changed consent text, bad hidden fields, an unknown `?sending`, `cv` on step
5 and the hidden fields after a CSRF failure.
The service is tested in test_send_answer.py; the browser runs are MT-39 to
MT-41 and MT-45 to MT-49 in docs/manual-test-plan.md.
"""

import datetime
import logging
import re
import uuid
from zoneinfo import ZoneInfo

import pytest
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core import signing
from django.db import IntegrityError, OperationalError
from django.test import Client

from tests.helpers import page_text, row_counts, tag_attrs
from tests.test_rsvp_hike_check import _arild_to_hike, _ids, _sigmund_to_check, _url
from wedding.actors import SYSTEM
from wedding.models import (
    Allergy,
    Consent,
    Guest,
    HouseholdAnswer,
    PersonAnswer,
    Settings,
    Submission,
)
from wedding.rsvp.draft import COOKIE_NAME, SALT
from wedding.rules.answer import Answer
from wedding.services.answers import send_answer
from wedding.services.consent import CONSENT_TEXT_VERSION
from wedding.services.households import NewGuest, create_household

SIGMUND = "test-sigmund0000000000"
ARILD = "test-arild000000000000"
OSLO = ZoneInfo("Europe/Oslo")

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _hidden(client, code: str = SIGMUND) -> dict[str, str]:
    """Story 2.6c: the check page form's hidden `innsending` and `sum`, as a GET shows them."""
    return _hidden_in(client.get(_url(code, "se-over")).content.decode())


def _hidden_in(html: str) -> dict[str, str]:
    """Story 2.6c: the hidden `innsending` and `sum` of a check page's HTML."""
    fields = {}
    for tag in re.findall(r'<input type="hidden"[^>]*>', html):
        attributes = tag_attrs(tag)
        if attributes["name"] in ("innsending", "sum"):
            fields[attributes["name"]] = attributes["value"]
    return fields


def _send(client, code: str = SIGMUND, data: dict | None = None):
    """«Send svaret» with the hidden fields the check page shows, unless `data` is given."""
    if data is None:
        data = _hidden(client, code) | {"action": "send"}
    return client.post(_url(code, "se-over"), data)


def _draft(response) -> dict:
    return signing.loads(response.cookies[COOKIE_NAME].value, salt=SALT)


def test_sigmund_sends(client, seeded):
    """FR-74, AD-3, AD-8 (matrix «Sigmund sends»): one HouseholdAnswer sent by
    Sigmund, two PersonAnswer rows, revision 1, the draft cookie deleted on
    `/<code>/` and 303 to `sendt/`; no session and no messages."""
    sigmund, bestemor = _sigmund_to_check(client)
    response = _send(client)
    assert response.status_code == 303
    assert response["Location"] == _url(SIGMUND, "sendt")
    cookie = response.cookies[COOKIE_NAME]
    assert cookie.value == ""
    assert cookie["max-age"] == 0
    assert cookie["path"] == f"/{SIGMUND}/"
    sent = HouseholdAnswer.objects.get()
    assert (sent.sent_by_id, sent.sent_by_name) == (sigmund, "Sigmund")
    assert PersonAnswer.objects.filter(guest_id__in=[sigmund, bestemor], coming=True).count() == 2
    assert PersonAnswer.objects.get(guest_id=sigmund).hike == "maybe"
    assert Guest.objects.get(code=SIGMUND).household.revision == 1
    assert "sessionid" not in response.cookies
    assert "messages" not in response.cookies
    assert Session.objects.count() == 0


def test_the_switched_respondent_is_the_sender(client, seeded):
    """FR-12, FR-74 (matrix «Bytt»): Arild's household with Marie as respondent
    records Marie; Leone not coming has every field False."""
    arild, marie, filippa, leone = _arild_to_hike(client)
    client.post(_url(ARILD, "fjelltur"), {"action": "choose", "respondent": marie})
    client.post(_url(ARILD, "fjelltur"), {f"hike_{arild}": "yes", f"hike_{marie}": "no"})
    response = _send(client, ARILD)
    assert response["Location"] == _url(ARILD, "sendt")
    assert HouseholdAnswer.objects.get().sent_by_name == "Marie"
    assert PersonAnswer.objects.get(guest_id=leone).coming is False
    filippa_row = PersonAnswer.objects.get(guest_id=filippa)
    assert (filippa_row.friday, filippa_row.saturday, filippa_row.hike) == (False, True, "")


def test_the_sent_page(client, seeded):
    """FR-74, UX-DR24, AD-15: title, the success notice holding the `h1` and the
    sent line in Oslo time, «Til invitasjonen» to `/<code>/`, no nav bar, the
    footer band, never cached. Story 2.7 adds the rest of the receipt below the
    notice (test_rsvp_receipt.py), so the notice ends before Rikke's message."""
    _sigmund_to_check(client)
    _send(client)
    sent = HouseholdAnswer.objects.get()
    response = client.get(_url(SIGMUND, "sendt"))
    assert response.status_code == 200
    assert "private" in response["Cache-Control"]
    assert "no-store" in response["Cache-Control"]
    html = response.content.decode()
    assert re.search(r"<title>\s*Svaret er sendt \N{EN DASH} Invitasjon\s*</title>", html)
    notice = html[html.index("notice--success") : html.index("receipt-message")]
    assert "<h1>Svaret er sendt</h1>" in notice
    local = sent.sent_at.astimezone(OSLO)
    assert f"kl. {local:%H:%M}." in page_text(notice)
    assert "Sendt av Sigmund " in page_text(notice)
    assert f"{local.day}. " in page_text(notice)
    assert f'href="/{SIGMUND}/">Til invitasjonen</a>' in html
    assert "<nav" not in html
    assert "<footer" in html


def test_the_sent_line_is_in_oslo_time(client, seeded):
    """FR-74, AD-11: a send at 22:30 UTC on 1 June reads «… 2. juni … kl. 00:30»."""
    guest = Guest.objects.get(code=SIGMUND)
    sigmund, bestemor = _ids(SIGMUND)
    send_answer(
        SYSTEM,
        household=guest.household,
        respondent=bestemor,
        answer=Answer({sigmund: True, bestemor: False}, True),
        now=datetime.datetime(2027, 6, 1, 22, 30, tzinfo=datetime.UTC),
        submission=uuid.uuid4(),
        revision=0,
        shown_total=0,
        consent_version=None,
    )
    text = page_text(client.get(_url(SIGMUND, "sendt")).content.decode())
    assert "Sendt av bestemor onsdag 2. juni 2027 kl. 00:30." in text


def test_the_sent_page_without_an_answer(client, seeded):
    """AD-7 (matrix «Sent page, no answer»): 302 to `/svar/`; an unknown code is G1
    with 404; POST is not allowed."""
    response = client.get(_url(SIGMUND, "sendt"))
    assert response.status_code == 302
    assert response["Location"] == _url(SIGMUND)
    assert client.get("/ukjent-kode0000000000/svar/sendt/").status_code == 404
    assert client.post(_url(SIGMUND, "sendt")).status_code == 405


def test_the_deadline_passes_at_send(client, seeded, monkeypatch):
    """FR-41, AD-11 (matrix «After deadline»): when `send_answer` refuses with
    `DeadlinePassed`, the closed page shows the deadline and the phones, and
    nothing is written."""
    _sigmund_to_check(client)
    monkeypatch.setattr("wedding.services.answers.is_past_deadline", lambda *_: True)
    before = row_counts()
    response = _send(client)
    assert response.status_code == 200
    text = page_text(response.content.decode())
    assert "Svarfristen har gått ut" in text
    assert "Fristen gikk ut" in text
    assert "tel:" in response.content.decode()
    assert HouseholdAnswer.objects.count() == 0
    assert row_counts() == before


def test_a_member_missing_from_step_1_goes_to_step_1(client, seeded):
    """FR-13, AD-9 (matrix «Missing member»): nobody coming reaches the check
    page; a guest then moved into the household is not in the draft's
    attendance, so the household changed (Story 2.9, FR-78): no step stays
    done, «Send svaret» goes back to step 1 and nothing is written."""
    sigmund, bestemor = _ids(SIGMUND)
    client.post(_url(SIGMUND), {f"attendance_{sigmund}": "no", f"attendance_{bestemor}": "no"})
    assert client.get(_url(SIGMUND, "se-over")).status_code == 200
    newcomer = create_household(SYSTEM, [NewGuest("Ny gjest")]).guests.get()
    Guest.objects.filter(pk=newcomer.pk).update(household=Guest.objects.get(code=SIGMUND).household)
    response = _send(client)
    assert response.status_code in (302, 303)
    assert response["Location"] == _url(SIGMUND)
    assert HouseholdAnswer.objects.count() == 0
    assert PersonAnswer.objects.count() == 0


def test_a_post_without_send_writes_nothing(client, seeded):
    """AD-7 (matrix «No action»): 303 back to the check page, no row."""
    _sigmund_to_check(client)
    response = _send(client, data={"action": "continue"})
    assert response.status_code == 303
    assert response["Location"] == _url(SIGMUND, "se-over")
    assert HouseholdAnswer.objects.count() == 0


def test_an_unfinished_answer_is_not_sent(client, seeded):
    """AD-7 (matrix «Unfinished»): the gate redirects to the first unfinished step."""
    sigmund, bestemor = _ids(SIGMUND)
    client.post(_url(SIGMUND), {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "yes"})
    response = _send(client)
    assert response.status_code == 302
    assert response["Location"] == _url(SIGMUND, "dager")
    assert HouseholdAnswer.objects.count() == 0


def test_csrf_failure_on_the_check_page(seeded):
    """UX-DR52 (matrix «CSRF on check page»): 403, the check page with the focused
    error notice above «Obs», no cookie set, nothing written."""
    client = Client()
    _sigmund_to_check(client)
    client.handler.enforce_csrf_checks = True
    response = _send(client)
    assert response.status_code == 403
    html = response.content.decode()
    assert "<h1>Se over svaret før du sender</h1>" in html
    error = re.search(r'class="notice notice--error"\s+tabindex="-1" autofocus', html)
    assert error
    assert error.start() < html.index("notice--warning")
    assert "Feil: Skjemaet ble ikke sendt." in page_text(html)
    assert COOKIE_NAME not in response.cookies
    assert HouseholdAnswer.objects.count() == 0


def test_csrf_failure_on_an_unfinished_check_page_is_the_generic_page(seeded):
    """UX-DR52: without a finished draft the generic 403 page is shown."""
    client = Client(enforce_csrf_checks=True)
    response = _send(client)
    assert response.status_code == 403
    assert "Skjemaet ble ikke sendt</h1>" in response.content.decode()


def test_the_check_page_carries_the_busy_state(client, seeded):
    """UX-DR15: the form has `data-send-form` and loads rsvp-send.js with `defer`;
    the script never sets `disabled`."""
    _sigmund_to_check(client)
    html = client.get(_url(SIGMUND, "se-over")).content.decode()
    assert re.search(r"<form[^>]*\bdata-send-form\b", html)
    assert '<script src="/static/js/rsvp-send.js" defer></script>' in html
    script = (settings.BASE_DIR / "static" / "js" / "rsvp-send.js").read_text(encoding="utf-8")
    assert "Sender …" in script
    assert 'setAttribute("aria-disabled", "true")' in script
    assert ".disabled" not in script
    assert "persisted" in script


def _sigmund_with_allergies(client, allergies: dict) -> None:
    """Story 2.6b: Sigmund's household through every step to the check page,
    with `allergies` posted on step 5."""
    sigmund, bestemor = _ids(SIGMUND)
    client.post(_url(SIGMUND), {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "yes"})
    client.post(_url(SIGMUND, "dager"), {"whole": "yes"})
    client.post(
        _url(SIGMUND, "overnatting"),
        {f"overnight_{sigmund}": "yes", f"overnight_{bestemor}": "yes"},
    )
    client.post(_url(SIGMUND, "maltider"), {"action": "continue"})
    response = client.post(_url(SIGMUND, "allergier"), allergies | {"action": "continue"})
    assert response["Location"] == _url(SIGMUND, "fjelltur")
    response = client.post(
        _url(SIGMUND, "fjelltur"), {f"hike_{sigmund}": "maybe", f"hike_{bestemor}": "no"}
    )
    assert response["Location"] == _url(SIGMUND, "se-over")


def test_allergies_are_stored_only_with_consent(client, seeded):
    """FR-26, FR-28, FR-29, AD-18 (Story 2.6b, epics AC): Sigmund gluten «Ja»
    and bestemor nuts «Nei» store only Sigmund's data and two consent events;
    a re-send from a fresh draft that changes Sigmund's data with consent
    unanswered keeps his stored data. Since Story 2.8 the answered household's
    GET of the check page goes to the status block, so the warning is not
    shown there; the POST still sends."""
    sigmund, bestemor = _ids(SIGMUND)
    _sigmund_with_allergies(
        client,
        {
            f"allergies_{sigmund}": "gluten",
            f"consent_{sigmund}": "yes",
            f"allergies_{bestemor}": "nuts",
            f"consent_{bestemor}": "no",
        },
    )
    assert _send(client).status_code == 303
    assert list(Allergy.objects.values_list("guest_id", "gluten", "nuts")) == [
        (sigmund, True, False)
    ]
    events = Consent.objects.order_by("guest_id").values_list("guest_id", "event")
    assert list(events) == [(sigmund, Consent.GIVEN), (bestemor, Consent.REFUSED)]

    _sigmund_with_allergies(client, {f"allergies_{sigmund}": ["gluten", "lactose"]})
    assert client.get(_url(SIGMUND, "se-over"))["Location"] == f"/{SIGMUND}/#status"
    assert _send(client).status_code == 303
    allergy = Allergy.objects.get()
    assert (allergy.guest_id, allergy.gluten, allergy.lactose) == (sigmund, True, False)
    assert Consent.objects.count() == 2


def test_the_check_page_carries_a_submission_id_and_its_total(client, seeded):
    """AD-7, AD-20 (Story 2.6c): `innsending` is a UUID, new on every GET, and
    `sum` is the total the page shows."""
    _sigmund_to_check(client)
    first, second = _hidden(client), _hidden(client)
    assert uuid.UUID(first["innsending"]) != uuid.UUID(second["innsending"])
    html = client.get(_url(SIGMUND, "se-over")).content.decode()
    shown = re.search(r"Totalt for husstanden: <strong>(.*?)</strong>", html).group(1)
    assert first["sum"] == second["sum"] == re.sub(r"\D", "", shown) != "0"


def test_a_double_send_writes_once(client, seeded):
    """AD-20, NFR-1 (Story 2.6c, matrix «Double tap», epics AC): the same form
    posted twice gives one `HouseholdAnswer`, one `Submission`, revision 1,
    and both land on `sendt/`; the same POST again without the draft cookie
    lands there too."""
    _sigmund_to_check(client)
    data = _hidden(client) | {"action": "send"}
    cookie = client.cookies[COOKIE_NAME].value
    first = _send(client, data=data)
    client.cookies[COOKIE_NAME] = cookie
    second = _send(client, data=data)
    for response in (first, second):
        assert response.status_code == 303
        assert response["Location"] == _url(SIGMUND, "sendt")
    assert HouseholdAnswer.objects.count() == 1
    assert Submission.objects.count() == 1
    assert Guest.objects.get(code=SIGMUND).household.revision == 1
    del client.cookies[COOKIE_NAME]
    late = _send(client, data=data)
    assert (late.status_code, late["Location"]) == (303, _url(SIGMUND, "sendt"))
    assert Submission.objects.count() == 1


def test_a_send_from_an_older_revision(client, seeded):
    """AD-9, AD-18 (Story 2.6c, matrix «Two tabs / devices», epics AC): a draft
    at revision 0 after another send is refused: 303 `?sending=endret`, the
    draft moved to revision 1 without consent answers, the notice names
    Sigmund and the time; the next send is a new send. The check page is open
    before the other send (since Story 2.8 a later GET goes to the status
    block), and the next send uses the hidden fields of the refused send's
    check page."""
    sigmund, _ = _ids(SIGMUND)
    _sigmund_with_allergies(
        client,
        {f"allergies_{sigmund}": "gluten", f"consent_{sigmund}": "yes"},
    )
    opened = _hidden(client) | {"action": "send"}
    other = Client()
    _sigmund_to_check(other)
    assert _send(other).status_code == 303
    response = _send(client, data=opened)
    assert response.status_code == 303
    assert response["Location"] == _url(SIGMUND, "se-over") + "?sending=endret"
    draft = _draft(response)
    assert (draft["rev"], draft["cons"], draft["conf"]) == (1, {}, [])
    assert Submission.objects.count() == 1
    html = client.get(response["Location"]).content.decode()
    sent = HouseholdAnswer.objects.get().sent_at.astimezone(OSLO)
    notice = re.search(r'notice--error"\s+tabindex="-1" autofocus>(.*?)</div>', html, re.S)
    text = page_text(notice.group(1))
    assert "Feil: Svaret ble ikke sendt, fordi Sigmund sendte et svar" in text
    assert f"kl. {sent:%H:%M} etter at du begynte." in text
    assert "Samtykke til å lagre allergier må gis på nytt." in text
    assert "Allergiopplysningene om Sigmund blir ikke lagret" in page_text(html)
    again = _send(client, data=_hidden_in(html) | {"action": "send"})
    assert again["Location"] == _url(SIGMUND, "sendt")
    assert Guest.objects.get(code=SIGMUND).household.revision == 2
    assert Allergy.objects.count() == 0


def test_a_price_change_before_sending(client, seeded):
    """AD-7, NFR-2 (Story 2.6c, matrix «Price changed», epics AC): 303
    `?sending=sum`, the draft unchanged, nothing written; the page then
    shows the notice and the new total."""
    _sigmund_to_check(client)
    data = _hidden(client) | {"action": "send"}
    Settings.objects.filter(pk=1).update(price_cabin_weekend=9999)
    response = _send(client, data=data)
    assert response["Location"] == _url(SIGMUND, "se-over") + "?sending=sum"
    assert COOKIE_NAME not in response.cookies
    assert HouseholdAnswer.objects.count() == 0
    assert Submission.objects.count() == 0
    html = client.get(response["Location"]).content.decode()
    assert "Feil: Svaret ble ikke sendt, fordi summen har endret seg." in page_text(html)
    assert _hidden(client)["sum"] != data["sum"]
    assert _send(client)["Location"] == _url(SIGMUND, "sendt")


def test_a_failed_database_write(client, seeded, monkeypatch, caplog):
    """UX-DR52, NFR-1 (Story 2.6c, matrix «Database fails», epics AC): 303
    `?sending=feilet`, the draft neither deleted nor rewritten, the notice
    with «Prøv igjen» and both phones, and a log line without the name."""
    _sigmund_to_check(client)

    def fails(*_, **__):
        raise OperationalError("database is locked")

    monkeypatch.setattr("wedding.rsvp.views.send_answer", fails)
    with caplog.at_level(logging.DEBUG):
        response = _send(client)
    assert response["Location"] == _url(SIGMUND, "se-over") + "?sending=feilet"
    assert COOKIE_NAME not in response.cookies
    household = Guest.objects.get(code=SIGMUND).household_id
    assert f"Sending the answer failed (OperationalError) for household {household}" in caplog.text
    assert "Sigmund" not in caplog.text
    html = client.get(response["Location"]).content.decode()
    text = page_text(html)
    assert "Feil: Svaret ble ikke sendt, fordi noe gikk galt da det skulle lagres." in text
    assert "Prøv igjen" in text
    settings_row = Settings.objects.get()
    assert f"ring {settings_row.contact_1_name} på {settings_row.contact_1_phone}" in text
    assert f"eller {settings_row.contact_2_name} på {settings_row.contact_2_phone}." in text


def test_a_changed_consent_text(client, seeded, monkeypatch):
    """AD-18, FR-29 (Story 2.6c, matrix «Consent text changed»): 303
    `?sending=samtykke`, consent answers cleared, nothing written."""
    sigmund, _ = _ids(SIGMUND)
    _sigmund_with_allergies(client, {f"allergies_{sigmund}": "gluten", f"consent_{sigmund}": "yes"})
    monkeypatch.setattr("wedding.services.answers.CONSENT_TEXT_VERSION", "2027-01-01")
    response = _send(client)
    assert response["Location"] == _url(SIGMUND, "se-over") + "?sending=samtykke"
    draft = _draft(response)
    assert (draft["cons"], draft["conf"], draft["cv"]) == ({}, [], None)
    assert (HouseholdAnswer.objects.count(), Consent.objects.count()) == (0, 0)
    text = page_text(client.get(response["Location"]).content.decode())
    assert "teksten om lagring av allergier er endret" in text


def test_step_5_records_the_consent_text_version(client, seeded):
    """AD-18 (Story 2.6c): «Fortsett» on step 5 writes `cv`."""
    _sigmund_with_allergies(client, {})
    payload = signing.loads(client.cookies[COOKIE_NAME].value, salt=SALT)
    assert payload["cv"] == CONSENT_TEXT_VERSION


@pytest.mark.parametrize(
    "data",
    [{"innsending": "x", "sum": "0"}, {"innsending": str(uuid.uuid4())}, {"sum": "0"}],
    ids=["not a uuid", "no sum", "no id"],
)
def test_bad_hidden_fields_write_nothing(client, seeded, data):
    """AD-20 (Story 2.6c, matrix «Bad hidden fields»): 303 to the check page."""
    _sigmund_to_check(client)
    response = _send(client, data=data | {"action": "send"})
    assert response["Location"] == _url(SIGMUND, "se-over")
    assert (HouseholdAnswer.objects.count(), Submission.objects.count()) == (0, 0)


def test_an_unknown_sending_reason_shows_no_notice(client, seeded):
    """UX-DR52 (Story 2.6c): `?sending=x` is ignored; only the hidden client notice exists."""
    _sigmund_to_check(client)
    html = client.get(_url(SIGMUND, "se-over") + "?sending=x").content.decode()
    assert "autofocus" not in html
    assert re.search(r"<div data-send-failed hidden tabindex=\"-1\">", html)
    assert "fordi forbindelsen ble brutt" in page_text(html)


def test_the_csrf_failure_page_carries_the_hidden_fields(seeded):
    """AD-20, UX-DR52 (Story 2.6c): the 403 check page has `innsending` and `sum`."""
    client = Client()
    _sigmund_to_check(client)
    client.handler.enforce_csrf_checks = True
    html = _send(client, data={"action": "send"}).content.decode()
    assert re.search(r'name="innsending" value="[0-9a-f-]{36}"', html)
    assert re.search(r'name="sum" value="\d+"', html)


def test_a_same_id_race_lands_on_the_sent_page(client, seeded, monkeypatch):
    """AD-20, NFR-1 (Story 2.6c): the loser of a same-id race gets an
    `IntegrityError` after the winner wrote the id; it lands on `sendt/` and
    the draft is deleted."""
    _sigmund_to_check(client)
    real = send_answer

    def races(actor, **kwargs):
        real(actor, **kwargs)
        raise IntegrityError("UNIQUE constraint failed")

    monkeypatch.setattr("wedding.rsvp.views.send_answer", races)
    response = _send(client)
    assert response["Location"] == _url(SIGMUND, "sendt")
    assert response.cookies[COOKIE_NAME]["max-age"] == 0
    assert Submission.objects.count() == 1


def test_another_households_id_goes_back_to_the_check_page(client, seeded):
    """AD-3, AD-20 (Story 2.6c): an `innsending` written for Arild's household
    is refused with 303 to the check page, nothing written, no server error."""
    arild, marie, filippa, leone = _ids(ARILD)
    key = uuid.uuid4()
    send_answer(
        SYSTEM,
        household=Guest.objects.get(code=ARILD).household,
        respondent=arild,
        answer=Answer({arild: False, marie: False, filippa: False, leone: False}, True),
        now=datetime.datetime(2027, 1, 1, tzinfo=datetime.UTC),
        submission=key,
        revision=0,
        shown_total=0,
        consent_version=None,
    )
    _sigmund_to_check(client)
    data = _hidden(client) | {"action": "send", "innsending": str(key)}
    response = _send(client, data=data)
    assert response["Location"] == _url(SIGMUND, "se-over")
    assert HouseholdAnswer.objects.count() == 1
    assert Submission.objects.count() == 1
