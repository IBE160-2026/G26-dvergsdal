"""Two members of one household sending in sequence (Story 4.2; FR-38, AD-9, AD-18, AD-20).

Marie and Arild are one household with two links, two browsers (two test
clients). Arild's seeded answer gives Filippa a cabin «Ja» (6 480 kr);
changing it to «Nei» (4 980 kr) is the change that makes the other member's
send stale. The service refusal is tested in test_answers_service.py and the
2.6c refusal in test_rsvp_send_views.py; the browser runs are MT-97 to MT-102
in docs/manual-test-plan.md.
"""

import re
from html import unescape
from zoneinfo import ZoneInfo

import pytest
from django.core import signing
from django.template.loader import render_to_string
from django.test import Client

from tests.helpers import page_text, row_counts
from tests.test_rsvp_hike_check import _ids, _url
from tests.test_rsvp_send_views import (
    ARILD,
    MARIE,
    _hidden_in,
    _household,
    _prefilled,
    _walk_to_check,
)
from wedding.models import HouseholdAnswer, Submission
from wedding.rsvp.draft import COOKIE_NAME, SALT

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]

OSLO = ZoneInfo("Europe/Oslo")
GOLDEN = "Filippa: du svarte hytte hele helgen, Arild sendte overnatter ikke"


def _confirmations() -> dict[str, dict]:
    """Marie answers for Arild and Filippa, so step 5 asks her to confirm them."""
    arild, _, filippa, _ = _ids(ARILD)
    return {"allergier": {f"confirm_{arild}": ["yes"], f"confirm_{filippa}": ["yes"]}}


def _arild_sends_no_cabin_for_filippa() -> None:
    """Arild's own browser: Filippa's cabin «Nei», then «Send svaret» (4 980 kr)."""
    other, filippa = Client(), _ids(ARILD)[2]
    html = _walk_to_check(other, ARILD, {"overnatting": {f"overnight_{filippa}": ["no"]}})
    response = other.post(_url(ARILD, "se-over"), _hidden_in(html) | {"action": "send"})
    assert response["Location"] == _url(ARILD, "sendt")


def _cookie(response) -> dict:
    return signing.loads(response.cookies[COOKIE_NAME].value, salt=SALT)


def _warning(html: str) -> str:
    """The text of the focused warning notice and its list, as the guest reads it."""
    notice = re.search(r'<div class="notice notice--warning"\s+tabindex="-1" autofocus>', html)
    assert notice, "no focused warning notice"
    return page_text(html[notice.end() : html.index("</ul>", notice.end())])


def test_marie_is_refused_after_arild_sends_and_sends_again(client, seeded_with_answers):
    """FR-38, AD-9, AD-18, AD-20 (matrix «Two members in sequence», «Review and send again»):
    Marie's draft starts at revision n, Arild sends (n+1), Marie's send is refused with a
    warning that names Arild, the time and the cabin line, writes nothing, and her draft
    moves to n+1 without consent; her next send is saved at n+2 as Marie."""
    n = _household(ARILD).revision
    html = _walk_to_check(client, MARIE, _confirmations())
    data = _hidden_in(html) | {"action": "send"}
    _arild_sends_no_cabin_for_filippa()
    before = row_counts() | {"revision": _household(ARILD).revision}
    assert before["revision"] == n + 1
    response = client.post(_url(MARIE, "se-over"), data)
    assert (response.status_code, response["Location"]) == (
        303,
        _url(MARIE, "se-over") + "?sending=endret",
    )
    assert row_counts() | {"revision": _household(ARILD).revision} == before
    assert _cookie(response)["rev"] == n + 1
    assert _cookie(response)["cons"] == {}
    page = client.get(response["Location"]).content.decode()
    sent = HouseholdAnswer.objects.get(household=_household(ARILD)).sent_at
    text = _warning(page)
    assert text.startswith("Obs: Svaret ble ikke sendt, fordi Arild sendte et svar for husstanden")
    assert f"kl. {sent.astimezone(OSLO):%H:%M}" in text
    assert GOLDEN in text
    assert "Samtykke til å lagre allergier må gis på nytt." in page_text(page)
    assert "notice--error" not in page.split("data-send-failed")[0]
    assert 'role="alert"' not in page.split("data-send-notice")[1].split("</div>")[0]
    again = client.post(_url(MARIE, "se-over"), _hidden_in(page) | {"action": "send"})
    assert again["Location"] == _url(MARIE, "sendt")
    assert _household(ARILD).revision == n + 2
    assert HouseholdAnswer.objects.get(household=_household(ARILD)).sent_by_name == "Marie"
    assert Submission.objects.count() == before["Submission"] + 1


def test_a_form_opened_before_the_send_is_refused_at_the_send(client, seeded_with_answers):
    """FR-38, AD-9 (matrix «Form opened before the send»): step 1 carries `revisjon`; Arild sends;
    Marie posts it with no cookie draft, so her draft starts at the old revision and her send
    is refused."""
    n = _household(ARILD).revision
    opened = client.get(_url(MARIE)).content.decode()
    assert re.search(rf'<input type="hidden" name="revisjon" value="{n}">', opened)
    _arild_sends_no_cabin_for_filippa()
    posted = _prefilled(opened) | {"revisjon": str(n), "action": "continue"}
    first = client.post(_url(MARIE), posted)
    assert _cookie(first)["rev"] == n
    assert _cookie(first)["cons"] == {}
    html = _walk_to_check(client, MARIE, _confirmations())
    before = row_counts()
    response = client.post(_url(MARIE, "se-over"), _hidden_in(html) | {"action": "send"})
    assert response["Location"] == _url(MARIE, "se-over") + "?sending=endret"
    assert row_counts() == before
    assert _household(ARILD).revision == n + 1


def test_a_stale_seeded_step_never_carries_a_consent_yes(client, seeded_with_answers):
    """AD-18 (matrix «Consent»): Arild's stored «Ja» is in a fresh seed, but a first POST from a
    form opened at an older revision starts a draft with no consent «Ja» and no version."""
    n = _household(ARILD).revision
    opened = client.get(_url(ARILD)).content.decode()
    _arild_sends_no_cabin_for_filippa()
    response = client.post(
        _url(ARILD), _prefilled(opened) | {"revisjon": str(n), "action": "continue"}
    )
    draft = _cookie(response)
    assert (draft["rev"], draft["cons"], draft["conf"], draft["cv"]) == (n, {}, [], None)


def test_a_forged_revision_is_ignored(client, seeded_with_answers):
    """FR-38 (matrix «Forged or missing field»): absent, text, negative or higher than the
    household's revision: the draft starts at the current revision with the stored consent."""
    n = _household(ARILD).revision
    opened = client.get(_url(ARILD)).content.decode()
    for value in (None, "abc", "-1", str(n + 5)):
        extra = {} if value is None else {"revisjon": value}
        response = Client().post(_url(ARILD), _prefilled(opened) | extra | {"action": "continue"})
        draft = _cookie(response)
        assert draft["rev"] == n
        assert draft["cons"]


def test_the_cookie_draft_wins_over_the_posted_revision(client, seeded_with_answers):
    """FR-38 (matrix «Cookie draft present»): a cookie draft at n and a post with `revisjon=n+1`
    keep the draft's own revision; the field is ignored."""
    n = _household(ARILD).revision
    opened = client.get(_url(ARILD)).content.decode()
    first = client.post(_url(ARILD), _prefilled(opened) | {"action": "continue"})
    assert _cookie(first)["rev"] == n
    page = client.get(first["Location"]).content.decode()
    second = client.post(
        first["Location"], _prefilled(page) | {"revisjon": str(n + 1), "action": "continue"}
    )
    assert _cookie(second)["rev"] == n


def test_only_a_seeded_form_carries_the_field(client, seeded):
    """FR-38, AD-8: a household with no answer has no seed and no hidden `revisjon`, and a
    cookie draft's own revision is never in the form."""
    assert "revisjon" not in client.get(_url(ARILD)).content.decode()


def test_the_field_survives_a_csrf_failure(seeded_with_answers):
    """FR-38, UX-DR52: step 1 shown again after a failed CSRF check keeps the revision."""
    strict = Client(enforce_csrf_checks=True)
    n = _household(ARILD).revision
    response = strict.post(_url(ARILD), {"revisjon": str(n), "action": "continue"})
    assert response.status_code == 403
    assert f'name="revisjon" value="{n}"' in unescape(response.content.decode())


def test_the_notice_component_lists_items_and_stays_silent(client):
    """UX-DR17, NFR-5 (Story 4.2): `items` render as `notice__list` and `after` as a paragraph;
    the notice is focused on load and never a live region."""
    html = render_to_string(
        "wedding/components/notice.html",
        {
            "variant": "warning",
            "text": "Tekst",
            "items": ["A", "B"],
            "after": "Slutt",
            "focus": True,
        },
    )
    assert re.search(r'<ul class="notice__list">\s*<li>A</li>\s*<li>B</li>\s*</ul>', html)
    assert "autofocus" in html
    assert "role=" not in html
    assert "Slutt" in html
    plain = render_to_string("wedding/components/notice.html", {"variant": "info", "text": "x"})
    assert "notice__list" not in plain


def test_an_invalid_first_step_keeps_the_opened_revision(client, seeded_with_answers):
    """FR-38, AD-8, AD-9: a stale cookie-less form posted with no «Kommer» choice is written
    (as any «Fortsett») at the opened revision and goes to `?feil=1`, whose page reads that
    cookie draft; the corrected post still ends in the conflict refusal at send."""
    n = _household(ARILD).revision
    opened = client.get(_url(MARIE)).content.decode()
    _arild_sends_no_cabin_for_filippa()
    invalid = client.post(_url(MARIE), {"revisjon": str(n), "action": "continue"})
    assert (invalid.status_code, invalid["Location"]) == (303, _url(MARIE) + "?feil=1")
    assert (_cookie(invalid)["rev"], _cookie(invalid)["cons"]) == (n, {})
    assert client.get(invalid["Location"]).status_code == 200
    client.post(_url(MARIE), _prefilled(opened) | {"action": "continue"})
    html = _walk_to_check(client, MARIE, _confirmations())
    response = client.post(_url(MARIE, "se-over"), _hidden_in(html) | {"action": "send"})
    assert response["Location"] == _url(MARIE, "se-over") + "?sending=endret"
