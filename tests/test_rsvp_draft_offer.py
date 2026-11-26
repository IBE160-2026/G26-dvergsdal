"""An interrupted answer is kept on the phone (Story 2.9; FR-78, AD-8, AD-11, UX-DR26).

The front page's draft notice, the Draft offer that comes first on any form
address in a new browser visit (no `rsvp_visit` cookie), «Ja, fortsett» and
«Nei, begynn på nytt», a household that changed since the draft started, the
deadline deleting the draft (AD-11), an answered household's draft left alone,
and that no session row is ever created (AD-8). The draft cookie's own format
is in test_rsvp_draft.py.
"""

import datetime

import pytest
from django.contrib.sessions.models import Session
from django.core import signing
from django.utils import timezone

from tests.helpers import checked_radios, page_text
from wedding.models import Guest, Settings
from wedding.rsvp.draft import COOKIE_NAME, SALT, VISIT_COOKIE

MONA = "test-mona0000000000000"
GEIR = "test-geir0000000000000"
MARIE = "test-marie000000000000"
FRONT = f"/{MONA}/"
STEP_1 = f"/{MONA}/svar/"
NOTICE = "Du har et svar som ikke er sendt ennå."
OFFER = "Vil du fortsette der du slapp?"
ALL_STEPS = ["who", "days", "overnight", "meals", "allergies", "hike"]

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _ids(code: str) -> list[int]:
    household = Guest.objects.get(code=code).household
    return list(household.guests.order_by("id").values_list("id", flat=True))


def _payload(code: str = MONA, **changes) -> dict:
    ids = _ids(code)
    payload = {
        "v": 6,
        "started": "2026-11-21T10:00:00+00:00",
        "rev": Guest.objects.get(code=code).household.revision,
        "resp": ids[0],
        "att": {str(guest_id): True for guest_id in ids},
        "done": ["who"],
        "whole": None,
        "days": {},
        "night": {},
        "meals": {},
        "alg": {},
        "cons": {},
        "conf": [],
        "long": [],
        "hike": {},
        "cv": None,
    }
    return payload | changes


def _with_draft(client, payload: dict | None = None) -> None:
    """A draft cookie at `/<code>/`, as the browser keeps it after closing (no visit)."""
    client.cookies[COOKIE_NAME] = signing.dumps(payload or _payload(), salt=SALT, compress=True)
    client.cookies[COOKIE_NAME]["path"] = FRONT


def _written(response) -> dict:
    return signing.loads(response.cookies[COOKIE_NAME].value, salt=SALT)


def _past_deadline() -> None:
    Settings.objects.update(rsvp_deadline=timezone.localdate() - datetime.timedelta(days=2))


# The notice on the front page


def test_the_front_page_shows_the_notice_above_the_button(client, seeded):
    """FR-78, UX-DR26, AD-8: a usable draft at path `/<code>/` gives the warning
    notice «Obs: Du har et svar som ikke er sendt ennå.» above «Svar på
    invitasjonen»; the GET writes no cookie."""
    _with_draft(client)
    response = client.get(FRONT)
    assert response.status_code == 200
    html = response.content.decode()
    text = page_text(html)
    assert f"Obs: {NOTICE}" in text
    assert html.index("notice--warning") < html.index(f'href="{STEP_1}"')
    assert not response.cookies


def test_the_notice_survives_a_removed_member(client, seeded):
    """FR-78, AD-8 (Story 2.9): a draft naming Geir, then Geir deleted: the
    draft is cleaned, not broken, so the front page shows the notice and does
    not delete `rsvp_draft`."""
    geir = _ids(MONA)[1]
    _with_draft(client, _payload(resp=geir, cons={str(geir): True}, conf=[geir]))
    Guest.objects.filter(code=GEIR).delete()
    response = client.get(FRONT)
    assert NOTICE in response.content.decode()
    assert COOKIE_NAME not in response.cookies


def test_no_draft_no_notice(client, seeded):
    """FR-78: without the cookie, no notice, and step 1 is shown as before."""
    assert NOTICE not in client.get(FRONT).content.decode()
    response = client.get(STEP_1)
    assert OFFER not in response.content.decode()
    assert "Hvem kommer?" in response.content.decode()


def test_a_broken_draft_gives_no_notice_and_is_deleted(client, seeded):
    """AD-8: a broken cookie gives no notice; the front page deletes it."""
    client.cookies[COOKIE_NAME] = "broken"
    response = client.get(FRONT)
    assert NOTICE not in response.content.decode()
    assert response.cookies[COOKIE_NAME]["max-age"] == 0
    assert response.cookies[COOKIE_NAME]["path"] == FRONT


def test_a_broken_draft_gives_no_offer(client, seeded):
    """AD-8: a broken cookie on the form gives step 1, not the offer, and is deleted."""
    client.cookies[COOKIE_NAME] = "broken"
    response = client.get(STEP_1)
    assert OFFER not in response.content.decode()
    assert response.cookies[COOKIE_NAME]["max-age"] == 0


# The offer


@pytest.mark.parametrize("slug", ["", "dager/", "overnatting/", "se-over/"])
def test_the_offer_comes_first_on_any_form_address(client, seeded, slug):
    """FR-78, UX-DR26: in a new visit, any step or the check page shows the
    Draft offer instead (200, same URL), with the start line and both buttons
    and no step fields; it writes no cookie (AD-8)."""
    _with_draft(client)
    response = client.get(STEP_1 + slug)
    assert response.status_code == 200
    html = response.content.decode()
    text = page_text(html)
    assert f"<h1>{OFFER}</h1>" in html
    assert f"<title>{OFFER} \N{EN DASH} Invitasjon</title>" in html
    assert "Du begynte på svaret lørdag 21. november kl. 11:00." in text
    assert "Det du har fylt ut, er tatt vare på på denne telefonen." in text
    assert 'name="action" value="resume">Ja, fortsett</button>' in html
    assert "Nei, begynn på nytt" in html
    assert html.index("Ja, fortsett") < html.index("Nei, begynn på nytt")
    assert "csrfmiddlewaretoken" in html
    assert html.count("<input") == 1
    assert COOKIE_NAME not in response.cookies
    assert VISIT_COOKIE not in response.cookies


def test_within_a_visit_the_step_is_shown(client, seeded):
    """FR-78: with `rsvp_visit`, the step itself, with the draft's answers."""
    _with_draft(client)
    client.cookies[VISIT_COOKIE] = "1"
    response = client.get(STEP_1)
    html = response.content.decode()
    assert OFFER not in html
    mona = _ids(MONA)[0]
    assert checked_radios(html)[f"attendance_{mona}"] == "yes"


def test_yes_goes_to_the_first_unfinished_step(client, seeded):
    """FR-78, AD-8: «Ja, fortsett» writes the draft, sets `rsvp_visit` and goes
    (303) to the first unfinished step, whose answers are kept."""
    _with_draft(client, _payload(whole=True, done=["who", "days"]))
    response = client.post(STEP_1, {"action": "resume"})
    assert response.status_code == 303
    assert response["Location"] == f"/{MONA}/svar/overnatting/"
    assert _written(response)["done"] == ["who", "days"]
    visit = response.cookies[VISIT_COOKIE]
    assert visit.value == "1"
    assert visit["max-age"] == ""
    assert visit["expires"] == ""
    assert visit["httponly"] is True
    assert visit["samesite"] == "Lax"
    assert visit["path"] == FRONT
    step_2 = client.get(f"/{MONA}/svar/dager/").content.decode()
    assert OFFER not in step_2
    assert checked_radios(step_2)["whole"] == "yes"


def test_yes_goes_to_the_check_page_when_all_is_done(client, seeded):
    """FR-78, UX-DR23: with every applicable step done, «Ja» goes to `se-over/`."""
    mona, geir = _ids(MONA)
    _with_draft(client, _payload(att={str(mona): False, str(geir): False}))
    response = client.post(f"/{MONA}/svar/se-over/", {"action": "resume"})
    assert response.status_code == 303
    assert response["Location"] == f"/{MONA}/svar/se-over/"
    assert client.get(response["Location"]).status_code == 200


def test_no_deletes_the_draft_and_step_1_starts_empty(client, seeded):
    """FR-78, AD-8: «Nei, begynn på nytt» deletes `rsvp_draft`, sets `rsvp_visit`
    and goes (303) to step 1, where nothing is checked; the front page then has
    no notice."""
    _with_draft(client)
    response = client.post(f"/{MONA}/svar/dager/", {"action": "restart"})
    assert response.status_code == 303
    assert response["Location"] == STEP_1
    assert response.cookies[COOKIE_NAME]["max-age"] == 0
    assert response.cookies[COOKIE_NAME]["path"] == FRONT
    assert response.cookies[VISIT_COOKIE].value == "1"
    html = client.get(STEP_1).content.decode()
    assert OFFER not in html
    assert checked_radios(html) == {"respondent": str(_ids(MONA)[0])}
    assert NOTICE not in client.get(FRONT).content.decode()


@pytest.mark.parametrize("action", ["resume", "restart"])
def test_an_answer_without_a_draft_goes_to_step_1(client, seeded, action):
    """FR-78: «Ja» or «Nei» with no draft goes to step 1 and sets `rsvp_visit`."""
    response = client.post(f"/{MONA}/svar/se-over/", {"action": action})
    assert response.status_code == 303
    assert response["Location"] == STEP_1
    assert response.cookies[VISIT_COOKIE].value == "1"
    assert COOKIE_NAME not in response.cookies or response.cookies[COOKIE_NAME]["max-age"] == 0


def test_an_answer_with_a_broken_draft_deletes_it(client, seeded):
    """AD-8: «Ja» over a broken cookie goes to step 1 and deletes it."""
    client.cookies[COOKIE_NAME] = "broken"
    response = client.post(STEP_1, {"action": "resume"})
    assert response["Location"] == STEP_1
    assert response.cookies[COOKIE_NAME]["max-age"] == 0
    assert response.cookies[VISIT_COOKIE].value == "1"


def test_every_step_post_marks_the_visit(client, seeded):
    """FR-78: a «Fortsett» writes the draft and `rsvp_visit`, so the next step
    is shown, not the offer."""
    mona, geir = _ids(MONA)
    response = client.post(STEP_1, {f"attendance_{mona}": "yes", f"attendance_{geir}": "yes"})
    assert response.cookies[VISIT_COOKIE].value == "1"
    assert OFFER not in client.get(response["Location"]).content.decode()


# A household that changed


def test_a_removed_member_is_dropped_and_yes_goes_to_step_1(client, seeded):
    """FR-78, AD-8, AD-18: Geir deleted after the draft named him: the offer is
    shown, «Ja» goes to step 1, which lists only Mona, and the written draft
    holds no id of Geir and no consent answers."""
    mona, geir = _ids(MONA)
    _with_draft(
        client,
        _payload(
            resp=geir,
            done=ALL_STEPS,
            whole=True,
            night={str(mona): True, str(geir): False},
            alg={str(geir): {"c": ["nuts"], "n": False, "t": ""}},
            cons={str(mona): True, str(geir): True},
            conf=[geir],
            hike={str(geir): "yes"},
            cv="2026-11-23",
        ),
    )
    Guest.objects.filter(code=GEIR).delete()
    assert OFFER in client.get(f"/{MONA}/svar/se-over/").content.decode()
    response = client.post(f"/{MONA}/svar/se-over/", {"action": "resume"})
    assert response.status_code == 303
    assert response["Location"] == STEP_1
    written = _written(response)
    assert str(geir) not in signing.dumps(written)
    assert written["resp"] == mona
    assert written["cons"] == {}
    assert written["conf"] == []
    assert written["cv"] is None
    assert written["done"] == []
    assert written["att"] == {str(mona): True}
    html = client.get(STEP_1).content.decode()
    assert "Mona" in html
    assert "Geir" not in page_text(html[html.index("<main") :])


def test_a_member_added_after_step_1_goes_to_step_1(client, seeded):
    """FR-78, AD-8: a member added after step 1 is missing from the attendance,
    so «Ja» goes to step 1."""
    mona = _ids(MONA)[0]
    _with_draft(client, _payload(att={str(mona): True}, whole=True, done=["who", "days"]))
    response = client.post(STEP_1, {"action": "resume"})
    assert response["Location"] == STEP_1
    assert _written(response)["done"] == []


# The deadline (AD-11)


def test_after_the_deadline_the_front_page_deletes_the_draft(client, seeded):
    """AD-11, FR-78: no notice, and the front page deletes `rsvp_draft`."""
    _past_deadline()
    _with_draft(client)
    response = client.get(FRONT)
    assert NOTICE not in response.content.decode()
    assert response.cookies[COOKIE_NAME]["max-age"] == 0
    assert response.cookies[COOKIE_NAME]["path"] == FRONT


@pytest.mark.parametrize("slug", ["", "dager/", "se-over/"])
def test_after_the_deadline_the_form_is_closed_and_deletes_the_draft(client, seeded, slug):
    """AD-11, FR-41: the closed page, no offer, and `rsvp_draft` deleted."""
    _past_deadline()
    _with_draft(client)
    response = client.get(STEP_1 + slug)
    assert OFFER not in response.content.decode()
    assert "Svarfristen har gått ut" in page_text(response.content.decode())
    assert response.cookies[COOKIE_NAME]["max-age"] == 0


# An answered household


def test_an_answered_household_gets_no_notice_and_keeps_the_cookie(client, seeded_with_answers):
    """FR-24, Story 4.1: Marie's household has answered: the status block, no
    notice, the cookie untouched, and a form GET still goes to `#status`."""
    _with_draft(client, _payload(MARIE))
    client.cookies[COOKIE_NAME]["path"] = f"/{MARIE}/"
    response = client.get(f"/{MARIE}/")
    assert NOTICE not in response.content.decode()
    assert COOKIE_NAME not in response.cookies
    response = client.get(f"/{MARIE}/svar/")
    assert response.status_code == 302
    assert response["Location"] == f"/{MARIE}/#status"


# AD-8: no session


def test_the_whole_flow_creates_no_session(client, seeded):
    """AD-8: notice, offer, «Ja» and the step after it create no session row."""
    _with_draft(client)
    client.get(FRONT)
    client.get(STEP_1)
    response = client.post(STEP_1, {"action": "resume"})
    client.get(response["Location"])
    assert Session.objects.count() == 0
    assert "sessionid" not in client.cookies
