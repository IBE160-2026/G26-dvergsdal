"""«Send svaret» and «Svaret er sendt» over HTTP (Story 2.6a).

FR-12, FR-41, FR-74, AD-3, AD-7, AD-8, AD-15, UX-DR15, UX-DR24, UX-DR52. The
view rows of the story's I/O matrix: Sigmund's journey then send (rows, the
draft cookie deleted, 303 to `sendt/`), a switched respondent, the sent page
(its `h1`, the sent line in Oslo time, the link to the invitation, never
cached) and its 302 before any answer, the deadline passing at send, a member
missing from the draft, a POST without `action=send`, an unfinished step, a
CSRF failure on the check page, and the busy-state hooks on the check page.
The service is tested in test_send_answer.py; the browser runs are MT-39 to
MT-41 in docs/manual-test-plan.md.
"""

import datetime
import re
from zoneinfo import ZoneInfo

import pytest
from django.conf import settings
from django.contrib.sessions.models import Session
from django.test import Client

from tests.helpers import page_text, row_counts
from tests.test_rsvp_hike_check import _arild_to_hike, _ids, _sigmund_to_check, _url
from wedding.actors import SYSTEM
from wedding.models import Guest, HouseholdAnswer, PersonAnswer
from wedding.rsvp.draft import COOKIE_NAME
from wedding.rules.answer import Answer
from wedding.services.answers import send_answer
from wedding.services.households import NewGuest, create_household

SIGMUND = "test-sigmund0000000000"
ARILD = "test-arild000000000000"
OSLO = ZoneInfo("Europe/Oslo")

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _send(client, code: str = SIGMUND, data: dict | None = None):
    return client.post(_url(code, "se-over"), {"action": "send"} if data is None else data)


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
    footer band, never cached."""
    _sigmund_to_check(client)
    _send(client)
    sent = HouseholdAnswer.objects.get()
    response = client.get(_url(SIGMUND, "sendt"))
    assert response.status_code == 200
    assert "private" in response["Cache-Control"]
    assert "no-store" in response["Cache-Control"]
    html = response.content.decode()
    assert re.search(r"<title>\s*Svaret er sendt \N{EN DASH} Invitasjon\s*</title>", html)
    notice = html[html.index("notice--success") : html.index("form-actions")]
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


def test_a_missing_member_goes_to_step_1(client, seeded):
    """FR-13, AD-9 (matrix «Missing member»): a member added after step 1 is
    never sent for. The gate already sends the guest back to the first step
    that now lacks an answer (here the cabin), before the send branch's own
    check for a member missing from step 1; nothing is written."""
    _sigmund_to_check(client)
    household = Guest.objects.get(code=SIGMUND).household
    # The service for adding a member comes in Epic 6; the test moves a guest in.
    newcomer = create_household(SYSTEM, [NewGuest("Ny gjest")]).guests.get()
    Guest.objects.filter(pk=newcomer.pk).update(household=household)
    response = _send(client)
    assert response.status_code == 302
    assert response["Location"] == _url(SIGMUND, "overnatting")
    assert HouseholdAnswer.objects.count() == 0


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
