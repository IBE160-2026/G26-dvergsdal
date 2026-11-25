"""The household's status on the invitation over HTTP (Story 2.8).

FR-3, FR-24, FR-34, AD-4, AD-12, UX-DR10. The story's I/O matrix: the front
page before an answer (Mona) and after one, owing (Marie, sent by Arild) and
owing nothing (Synne); the nav «Svar» on an info page; an answered household
opening the form, before and after the deadline; the closed page for an
unanswered household after the deadline; a POST left to Story 2.6c; an
unknown code. The browser runs are MT-55 to MT-58 in docs/manual-test-plan.md.
"""

import datetime
import re

import pytest
from django.contrib.sessions.models import Session
from django.db import connection
from django.template.defaultfilters import date
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from tests.helpers import page_text, row_counts
from wedding.models import Guest, Settings
from wedding.selectors import household_answer

MARIE = "test-marie000000000000"
SYNNE = "test-synne000000000000"
MONA = "test-mona0000000000000"

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _front(client, code: str) -> str:
    response = client.get(f"/{code}/")
    assert response.status_code == 200
    return response.content.decode()


def _hero_line(html: str) -> str:
    return re.search(r'<p class="hero__deadline">(.*?)</p>', html, re.S).group(1)


def _nav_svar(html: str) -> str:
    return re.search(r'class="nav-bar__svar"\s+href="([^"]*)"', html)[1]


def _status_block(html: str) -> str:
    return re.search(r'<section class="paper-sheet rsvp status-block".*?</section>', html, re.S)[0]


def _past_deadline() -> None:
    Settings.objects.filter(pk=1).update(
        rsvp_deadline=timezone.localdate() - datetime.timedelta(days=1)
    )


def test_the_front_page_before_an_answer_is_unchanged(client, seeded_with_answers):
    """FR-24, UX-DR10 (matrix «Not answered»): Mona's household has not answered,
    so the hero says «Svar innen …», the RSVP sheet `#svar` holds «Svar på
    invitasjonen», the nav «Svar» goes to `#svar` and there is no `#status`."""
    html = _front(client, MONA)
    assert "innen" in page_text(_hero_line(html))
    assert 'id="svar"' in html
    assert "Svar på invitasjonen" in html
    assert _nav_svar(html) == "#svar"
    assert "#status" not in html
    assert 'id="status"' not in html


def test_the_front_page_after_an_answer_that_owes(client, seeded_with_answers):
    """FR-24, FR-34, AD-12, UX-DR10 (matrix «Answered, owes»): Marie sees that
    Arild has answered: the hero line «Svar sendt <j. F> · Se svaret», and in
    the RSVP sheet's place the status block, in order: heading, gypsophila,
    «Barnefritt bryllup», the sent line, the total and «Slik betaler du» to the
    payment page. The nav «Svar» goes to `#status`; no «Svar på invitasjonen»."""
    answer = household_answer(Guest.objects.get(code=MARIE).household)
    sent_at = timezone.localtime(answer.sent_at)
    html = _front(client, MARIE)
    hero = _hero_line(html)
    assert page_text(hero) == f"Svar sendt {date(sent_at, 'j. F')} · Se svaret"
    assert '<span aria-hidden="true">·</span>' in hero
    assert '<a href="#status">Se svaret</a>' in hero
    assert "&nbsp;" not in hero
    assert "\xa0" not in hero
    block = _status_block(html)
    assert 'aria-labelledby="status"' in block
    order = [
        block.index('<h2 id="status" tabindex="-1">Svaret er sendt</h2>'),
        block.index('class="rsvp__flowers"'),
        block.index("Barnefritt bryllup"),
        block.index("Sendt av Arild"),
        block.index("Totalt for husstanden"),
        block.index("Slik betaler du"),
    ]
    assert order == sorted(order)
    assert 'alt=""' in block
    assert 'loading="lazy"' in block
    text = page_text(block)
    assert f"kl. {sent_at:%H:%M}." in text
    assert "Totalt for husstanden: 6 480 kr" in text
    assert re.search(
        rf'class="button button--secondary"\s+href="/{MARIE}/svar/betal/">Slik betaler du<', block
    )
    assert _nav_svar(html) == "#status"
    assert html.count("#status") == 2
    assert html.count('id="status"') == 1
    assert "Svar på invitasjonen" not in html
    assert 'id="svar"' not in html


def test_the_sent_line_is_the_receipts(client, seeded_with_answers):
    """FR-24, FR-74: the status block's sent line is the receipt's, word for word
    (the shared include rsvp/includes/sent-line.html)."""
    block = page_text(_status_block(_front(client, MARIE)))
    receipt = page_text(client.get(f"/{MARIE}/svar/sendt/").content.decode())
    line = re.search(r"Sendt av .*? kl\. \d\d:\d\d\.", receipt)[0]
    assert line in block


def test_the_status_block_when_nothing_is_owed(client, seeded_with_answers):
    """FR-34 (matrix «Answered, nothing owed»): Synne's total is 0 kr, so the
    status block has no «Slik betaler du»."""
    block = _status_block(_front(client, SYNNE))
    assert "Totalt for husstanden: 0 kr" in page_text(block)
    assert "Slik betaler du" not in block
    assert "/svar/betal/" not in block


@pytest.mark.parametrize("path", ["program/", "praktisk/", "historie/"])
def test_the_nav_on_an_info_page_follows_the_answer(client, seeded_with_answers, path):
    """FR-8, FR-24, UX-DR10 (matrix «Info page nav»): the nav «Svar» goes to the
    front page's `#status` for an answered household, `#svar` otherwise."""
    marie = client.get(f"/{MARIE}/{path}").content.decode()
    mona = client.get(f"/{MONA}/{path}").content.decode()
    assert _nav_svar(marie) == f"/{MARIE}/#status"
    assert _nav_svar(mona) == f"/{MONA}/#svar"


@pytest.mark.parametrize(
    ("method", "path"), [("get", "svar/"), ("get", "svar/se-over/"), ("head", "svar/")]
)
def test_an_answered_household_opening_the_form_goes_to_the_status(
    client, seeded_with_answers, method, path
):
    """FR-24, UX-DR10 (matrix «Answered opens form»): every form address, GET
    or HEAD, sends an answered household (302) to the status block."""
    response = getattr(client, method)(f"/{MARIE}/{path}")
    assert response.status_code == 302
    assert response["Location"] == f"/{MARIE}/#status"


def test_after_the_deadline_an_answered_household_keeps_its_status(client, seeded_with_answers):
    """FR-24, FR-41 (matrix «Answered after deadline»): the same hero line and
    status block, and `/svar/` still goes to `#status`, not the closed page."""
    _past_deadline()
    html = _front(client, MARIE)
    assert page_text(_hero_line(html)).startswith("Svar sendt")
    assert "Svaret er sendt" in _status_block(html)
    response = client.get(f"/{MARIE}/svar/")
    assert response.status_code == 302
    assert response["Location"] == f"/{MARIE}/#status"


def test_after_the_deadline_an_unanswered_household_gets_the_closed_page(
    client, seeded_with_answers
):
    """FR-41 (matrix «Unanswered after deadline»): Mona's `/svar/` shows the
    closed page of Story 2.1 as before."""
    _past_deadline()
    response = client.get(f"/{MONA}/svar/")
    assert response.status_code == 200
    assert "Svarfristen har gått ut" in response.content.decode()


def test_a_post_by_an_answered_household_is_not_redirected(client, seeded_with_answers):
    """FR-38 (matrix «POST by answered household»): a POST keeps the handling of
    Story 2.6c, so it is never sent to `#status`: with no draft the check page
    sends it (302) to step 1, as before Story 2.8."""
    response = client.post(f"/{MARIE}/svar/se-over/", {})
    assert (response.status_code, response["Location"]) == (302, f"/{MARIE}/svar/")


def test_the_check_page_after_a_refused_send_is_shown(client, seeded_with_answers):
    """AD-9, UX-DR52 (Story 2.6c): the check page a refused send comes back to,
    `se-over/?sending=endret`, is shown to an answered household before the
    deadline, so the conflict notice is not lost. Step 1 is posted with nobody
    coming, so the draft goes straight to the check page."""
    household = Guest.objects.get(code=MARIE).household
    step_1 = {f"attendance_{guest.id}": "no" for guest in household.guests.all()}
    assert client.post(f"/{MARIE}/svar/", step_1)["Location"] == f"/{MARIE}/svar/se-over/"
    assert client.get(f"/{MARIE}/svar/se-over/?sending=endret").status_code == 200


def test_another_step_with_sending_goes_to_the_status(client, seeded_with_answers):
    """FR-24, UX-DR10: `?sending=` opens only the check page; any other step
    still goes to `#status`."""
    response = client.get(f"/{MARIE}/svar/dager/?sending=endret")
    assert (response.status_code, response["Location"]) == (302, f"/{MARIE}/#status")


def test_the_check_page_with_sending_after_the_deadline_goes_to_the_status(
    client, seeded_with_answers
):
    """FR-24, FR-41: after the deadline an answered household always gets its
    status, also on `se-over/?sending=…`."""
    _past_deadline()
    response = client.get(f"/{MARIE}/svar/se-over/?sending=endret")
    assert (response.status_code, response["Location"]) == (302, f"/{MARIE}/#status")


def test_an_unknown_code_still_gets_g1(client, seeded_with_answers):
    """FR-5 (matrix «Unknown code»): G1 with 404, as before."""
    assert client.get("/x/").status_code == 404


def test_the_answered_front_page_only_reads(client, seeded_with_answers):
    """FR-3, AD-12: the answered front page runs only SELECTs (seven: the
    resolver, the guest names, the settings row, the answer check and the
    stored answer's three tables for the total), writes nothing and sets no
    cookie or session."""
    before = row_counts()
    with CaptureQueriesContext(connection) as captured:
        response = client.get(f"/{MARIE}/")
    assert response.status_code == 200
    sql = [query["sql"] for query in captured.captured_queries]
    assert all(statement.lstrip().upper().startswith("SELECT") for statement in sql)
    assert len(sql) == 7
    assert row_counts() == before
    assert not response.cookies
    assert Session.objects.count() == 0
