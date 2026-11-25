"""The receipt and «Slik betaler du» over HTTP (Story 2.7).

FR-23, FR-34, FR-64, FR-71, AD-4, AD-12, AD-15, UX-DR24, UX-DR25, UX-DR51. The
story's I/O matrix: the receipt for a household that owes (Sigmund), owes
nothing (Synne) and where nobody comes (Tor); «Betal senere»; the payment
page, its redirect when nothing is owed and a blank setting; no answer; an
unknown code. Also `sent_answer` read back after `send_answer`, so the
receipt's total equals the check page's. The browser runs are MT-51 to MT-54
in docs/manual-test-plan.md.
"""

import re
import uuid
from pathlib import Path

import pytest
from django.utils import timezone

from tests.helpers import page_text
from wedding.actors import SYSTEM
from wedding.models import Guest, Settings
from wedding.rules.allergies import AllergyEntry
from wedding.rules.answer import Answer
from wedding.rules.money import household_total
from wedding.selectors import form_prices, sent_answer
from wedding.services.answers import send_answer
from wedding.services.consent import CONSENT_TEXT_VERSION

SIGMUND = "test-sigmund0000000000"
SYNNE = "test-synne000000000000"
TOR = "test-tor00000000000000"
MONA = "test-mona0000000000000"
TEMPLATES = Path(__file__).resolve().parent.parent / "wedding" / "rsvp" / "templates" / "rsvp"

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _sent(client, code: str, query: str = "") -> str:
    response = client.get(f"/{code}/svar/sendt/{query}")
    assert response.status_code == 200
    return response.content.decode()


def _pay(client, code: str):
    return client.get(f"/{code}/svar/betal/")


def _ids(code: str) -> list[int]:
    household = Guest.objects.get(code=code).household
    return list(household.guests.order_by("id").values_list("id", flat=True))


def test_the_receipt_when_something_is_owed(client, seeded_with_answers):
    """FR-23, FR-34, UX-DR24, UX-DR51 (matrix «Owes, two people»): «… med dere!»,
    «Dette har dere svart», the total, «Betal nå» before «Betal senere» before
    the closing line, «Til invitasjonen», no autofocus; never cached."""
    response = client.get(f"/{SIGMUND}/svar/sendt/")
    assert "no-store" in response["Cache-Control"]
    html = response.content.decode()
    text = page_text(html)
    assert "vi gleder oss til å feire den store dagen med dere!" in text
    assert '<h2 class="receipt-heading">Dette har dere svart</h2>' in html
    assert "Totalt for husstanden: 4 720 kr" in text
    assert "Sigmund: kommer" in text
    assert "Endre" not in text
    pay_now = html.index(f'href="/{SIGMUND}/svar/betal/">Betal nå</a>')
    pay_later = html.index(f'href="/{SIGMUND}/svar/sendt/?betal=senere">Betal senere</a>')
    closing = html.index("Du kan nå trygt lukke invitasjonen.")
    assert html.index("Svaret er sendt</h1>") < html.index("Tusen takk") < pay_now
    assert pay_now < pay_later < closing
    assert f'href="/{SIGMUND}/">Til invitasjonen</a>' in html
    assert "autofocus" not in html


def test_the_receipt_when_nothing_is_owed(client, seeded_with_answers):
    """FR-23, UX-DR51 (matrix «Nothing owed, one person»): «… med deg!»,
    «Dette har du svart», 0 kr and no payment buttons."""
    html = _sent(client, SYNNE)
    text = page_text(html)
    assert "den store dagen med deg!" in text
    assert "Dette har du svart" in text
    assert "Totalt for husstanden: 0 kr" in text
    assert "/svar/betal/" not in html
    assert "Betal senere" not in html
    assert html.index("Totalt for husstanden") < html.index("Du kan nå trygt lukke")


def test_the_receipt_when_nobody_comes(client, seeded_with_answers):
    """FR-23, UX-DR51 (matrix «Nobody coming»): Rikke's «Så leit at dere …», total 0."""
    text = page_text(_sent(client, TOR))
    assert (
        "Så leit at dere ikke har mulighet til å delta, men dette har vi full forståelse for."
        in text
    )
    assert "Tusen takk" not in text
    assert "Betal nå" not in text


def test_pay_later(client, seeded_with_answers):
    """FR-34, UX-DR24 (matrix «Pay later»): the focused info notice below the buttons
    and above the closing line; another value of `betal` shows nothing."""
    html = _sent(client, SIGMUND, "?betal=senere")
    notice = "Den samme lenken viser alltid hva dere har igjen å betale, og hvordan dere betaler."
    assert notice in html
    assert re.search(r'class="notice notice--info"[^>]*tabindex="-1" autofocus', html)
    assert html.index("Betal senere") < html.index(notice) < html.index("Du kan nå trygt")
    assert "Den samme lenken" not in _sent(client, SIGMUND, "?betal=x")


def test_pay_later_when_nothing_is_owed(client, seeded_with_answers):
    """FR-34 (matrix «Pay later, nothing owed»): no notice."""
    assert "Den samme lenken" not in _sent(client, SYNNE, "?betal=senere")


def test_the_payment_page(client, seeded_with_answers):
    """FR-34, FR-64, FR-71, UX-DR25 (matrix «Payment page»): the four values as text,
    four hidden «Kopier» buttons with their names and `data-copy`, four empty
    status spans, the script deferred; never cached, no nav bar."""
    response = _pay(client, SIGMUND)
    assert response.status_code == 200
    assert "no-store" in response["Cache-Control"]
    html = response.content.decode()
    text = page_text(html)
    assert "<h1>Slik betaler du</h1>" in html
    for value in ("4 720 kr", "00000", "1234.56.78900", "Bryllup Sigmund og bestemor"):
        assert value in text
    buttons = re.findall(r"<button[^>]*>Kopier</button>", html)
    assert len(buttons) == 4
    assert all(re.search(r"\shidden\s", button) for button in buttons)
    for name, copy in (
        ("Kopier beløpet", "4720"),
        ("Kopier Vipps-nummeret", "00000"),
        ("Kopier kontonummeret", "12345678900"),
        ("Kopier betalingsmeldingen", "Bryllup Sigmund og bestemor"),
    ):
        assert re.search(rf'aria-label="{name}"\s+data-copy="{copy}"', html), name
    assert html.count('<span class="copy-status" role="status"></span>') == 4
    assert re.search(r'<script src="[^"]*rsvp-copy\.js" defer>', html)
    assert "<nav" not in html


def test_the_payment_page_when_nothing_is_owed(client, seeded_with_answers):
    """FR-34 (matrix «Payment page, nothing owed»): 302 to the receipt."""
    response = _pay(client, SYNNE)
    assert response.status_code == 302
    assert response["Location"] == f"/{SYNNE}/svar/sendt/"


def test_a_blank_setting_is_left_out(client, seeded_with_answers):
    """FR-64 (matrix «Blank setting»): no Vipps row when the number is blank."""
    Settings.objects.update(vipps_number="")
    html = _pay(client, SIGMUND).content.decode()
    assert "Vipps-nummer" not in html
    assert html.count('role="status"') == 3


def test_not_answered_and_unknown(client, seeded_with_answers):
    """AD-7, FR-5 (matrix «Not answered», «Unknown code»): 302 to `/svar/`; G1 with
    404; only GET and HEAD."""
    for page in ("sendt", "betal"):
        response = client.get(f"/{MONA}/svar/{page}/")
        assert response.status_code == 302
        assert response["Location"] == f"/{MONA}/svar/"
        assert client.get(f"/ukjent-kode0000000000/svar/{page}/").status_code == 404
        assert client.post(f"/{SIGMUND}/svar/{page}/").status_code == 405


def test_sent_answer_round_trip(client, seeded):
    """AD-4, AD-12, FR-33: what `send_answer` stores reads back as the same answer,
    so the receipt's total equals the check page's for the draft; Mona's
    receipt then shows 3 000 kr and «Bryllup Mona og Geir»."""
    mona, geir = _ids(MONA)
    draft = Answer(
        {mona: True, geir: True},
        True,
        night={mona: True, geir: True},
        allergies={mona: AllergyEntry(cats=("nuts",), note="Litt")},
        consent={mona: True, geir: False},
        hike={mona: "yes"},
    )
    household = Guest.objects.get(code=MONA).household
    prices = form_prices()
    total = household_total(draft, prices)
    send_answer(
        SYSTEM,
        household=household,
        respondent=mona,
        answer=draft,
        now=timezone.now(),
        submission=uuid.uuid4(),
        revision=household.revision,
        shown_total=total,
        consent_version=CONSENT_TEXT_VERSION,
    )
    stored = sent_answer(household)
    assert household_total(stored, prices) == total == 3000
    assert stored.attendance == {mona: True, geir: True}
    assert stored.whole is True
    assert stored.allergies == {mona: AllergyEntry(cats=("nuts",), note="Litt")}
    assert stored.consent == {mona: True, geir: False}
    assert stored.hike == {mona: "yes"}
    text = page_text(_sent(client, MONA))
    assert "Totalt for husstanden: 3 000 kr" in text
    assert "Mona: nøtter" in text
    assert "Bryllup Mona og Geir" in page_text(_pay(client, MONA).content.decode())


def test_the_guest_pages_never_name_payment_rows():
    """AD-12, FR-34: the receipt and payment templates read no payment rows."""
    for name in ("sent.html", "pay.html", "includes/pay-row.html"):
        source = (TEMPLATES / name).read_text(encoding="utf-8").lower()
        assert "payment_report" not in source
        assert "paymentreport" not in source
