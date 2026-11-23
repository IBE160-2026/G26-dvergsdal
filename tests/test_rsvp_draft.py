"""The RSVP draft cookie (Stories 2.1 to 2.3; AD-8).

FR-78, AD-8: a round trip through `rsvp_draft`, its attributes (path `/<code>/`,
HttpOnly, SameSite=Lax, Secure only in production, the 90-day backstop), and
every kind of broken draft: each is deleted with the same path and the form
starts empty, never with a server error. Format 2 (Story 2.2) added `whole`
and `days`, format 3 (Story 2.3) `night` and `meals`; a format 1 or 2 cookie
is broken. The step flow itself is in
test_rsvp_who_is_coming.py.
"""

import base64
import time
import zlib
from datetime import UTC, datetime, timedelta

import pytest
from django.core import signing

from tests.helpers import checked_radios, ticked_boxes
from wedding.models import Guest
from wedding.rsvp.draft import COOKIE_NAME, SALT

SIGMUND = "test-sigmund0000000000"
ARILD = "test-arild000000000000"
STEP_1 = f"/{SIGMUND}/svar/"
NINETY_DAYS = 90 * 24 * 60 * 60

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _ids(code: str) -> list[int]:
    household = Guest.objects.get(code=code).household
    return list(household.guests.order_by("id").values_list("id", flat=True))


def _payload(**changes) -> dict:
    sigmund, bestemor = _ids(SIGMUND)
    payload = {
        "v": 3,
        "started": "2026-11-21T10:00:00+00:00",
        "rev": 0,
        "resp": sigmund,
        "att": {str(sigmund): True, str(bestemor): False},
        "done": ["who"],
        "whole": None,
        "days": {},
        "night": {},
        "meals": {},
    }
    return payload | changes


def _signed(payload: object) -> str:
    return signing.dumps(payload, salt=SALT, compress=True)


def _raw(data: bytes, *, compressed: bool) -> str:
    """A correctly signed value whose content is `data`, as `signing.dumps` frames it."""
    encoded = base64.urlsafe_b64encode(data).strip(b"=").decode()
    return signing.TimestampSigner(salt=SALT).sign(("." if compressed else "") + encoded)


def _post_valid(client):
    sigmund, bestemor = _ids(SIGMUND)
    return client.post(STEP_1, {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "no"})


def test_a_valid_post_writes_the_draft_with_its_attributes(client, seeded):
    """AD-8: path `/<code>/`, HttpOnly, SameSite=Lax, not Secure locally, 90 days;
    the payload has format 3, the household revision, the respondent, everyone's
    attendance and step 1 done."""
    sigmund, bestemor = _ids(SIGMUND)
    response = _post_valid(client)
    assert response.status_code == 302
    cookie = response.cookies[COOKIE_NAME]
    assert cookie["path"] == f"/{SIGMUND}/"
    assert cookie["httponly"] is True
    assert cookie["samesite"] == "Lax"
    assert not cookie["secure"]
    assert cookie["max-age"] == NINETY_DAYS
    payload = signing.loads(cookie.value, salt=SALT)
    assert payload["v"] == 3
    assert payload["rev"] == 0
    assert payload["resp"] == sigmund
    assert payload["att"] == {str(sigmund): True, str(bestemor): False}
    assert payload["done"] == ["who"]
    assert payload["whole"] is None
    assert payload["days"] == {}
    assert payload["night"] == {}
    assert payload["meals"] == {}
    assert payload["started"].endswith("+00:00")


def test_the_draft_is_secure_in_production(client, seeded, settings):
    """AD-8: `Secure` only when `IS_PRODUCTION`."""
    settings.IS_PRODUCTION = True
    assert _post_valid(client).cookies[COOKIE_NAME]["secure"] is True


def test_round_trip_keeps_started_and_revision(client, seeded):
    """AD-8: a second «Fortsett» keeps when the draft started and its revision."""
    client.cookies[COOKIE_NAME] = _signed(_payload(rev=7, done=[]))
    response = _post_valid(client)
    payload = signing.loads(response.cookies[COOKIE_NAME].value, salt=SALT)
    assert payload["started"] == "2026-11-21T10:00:00+00:00"
    assert payload["rev"] == 7
    assert payload["done"] == ["who"]


def test_a_full_draft_for_eight_fits_in_a_cookie():
    """AD-8: a household is at most 8, and its draft, with every day, a stay and
    every meal for everyone, stays below 4 KB."""
    ids = range(10_000_000, 10_000_008)
    payload = {
        "v": 3,
        "started": "2026-11-21T10:00:00.123456+00:00",
        "rev": 123,
        "resp": ids[0],
        "att": {str(guest_id): True for guest_id in ids},
        "done": ["who", "days", "overnight", "meals", "allergies", "hike"],
        "whole": False,
        "days": {str(guest_id): ["fri", "sat", "sun"] for guest_id in ids},
        "night": {str(guest_id): True for guest_id in ids},
        "meals": {
            str(guest_id): ["friday_dinner", "saturday_breakfast", "sunday_breakfast"]
            for guest_id in ids
        },
    }
    assert len(_signed(payload)) < 4096


def test_days_round_trip(client, seeded):
    """AD-8, FR-14: a format 2 draft with «Nei» and days is read back: step 2 shows
    the day groups with the saved days ticked, and a GET does not rewrite it."""
    sigmund, bestemor = _ids(SIGMUND)
    client.cookies[COOKIE_NAME] = _signed(
        _payload(
            att={str(sigmund): True, str(bestemor): True},
            whole=False,
            days={str(sigmund): ["fri", "sat"], str(bestemor): ["sun"]},
        )
    )
    response = client.get(f"/{SIGMUND}/svar/dager/")
    assert response.status_code == 200
    assert COOKIE_NAME not in response.cookies
    html = response.content.decode()
    ticked = ticked_boxes(html)
    assert ticked == [f"days_{sigmund}_fri", f"days_{sigmund}_sat", f"days_{bestemor}_sun"]


BROKEN = {
    "bad signature": lambda: _signed(_payload())[:-2] + "xx",
    "other salt": lambda: signing.dumps(_payload(), salt="other", compress=True),
    "signed non-zlib": lambda: _raw(b"not zlib at all", compressed=True),
    "signed non-JSON": lambda: _raw(zlib.compress(b"{not json"), compressed=True),
    "plain non-JSON": lambda: _raw(b"\xff\xfe", compressed=False),
    "not a dict": lambda: _signed([1, 2, 3]),
    "v 0": lambda: _signed(_payload(v=0)),
    "v 1 (Story 2.1)": lambda: _signed(_payload(v=1)),
    "v 2 (Story 2.2)": lambda: _signed(
        {k: v for k, v in _payload(v=2).items() if k not in ("night", "meals")}
    ),
    "v true": lambda: _signed(_payload(v=True)),
    "missing key": lambda: _signed({k: v for k, v in _payload().items() if k != "rev"}),
    "naive started": lambda: _signed(_payload(started="2026-11-21T10:00:00")),
    "started in the future": lambda: _signed(
        _payload(started=(datetime.now(UTC) + timedelta(minutes=2)).isoformat())
    ),
    "started not a time": lambda: _signed(_payload(started="i går")),
    "rev a string": lambda: _signed(_payload(rev="0")),
    "negative rev": lambda: _signed(_payload(rev=-1)),
    "resp a string": lambda: _signed(_payload(resp=str(_ids(SIGMUND)[0]))),
    "foreign resp": lambda: _signed(_payload(resp=_ids(ARILD)[0])),
    "att a list": lambda: _signed(_payload(att=[True])),
    "att value a string": lambda: _signed(_payload(att={str(_ids(SIGMUND)[0]): "yes"})),
    "foreign att key": lambda: _signed(_payload(att={str(_ids(ARILD)[0]): True})),
    "att key not a number": lambda: _signed(_payload(att={"²": True})),
    "unknown done key": lambda: _signed(_payload(done=["who", "send"])),
    "done a string": lambda: _signed(_payload(done="who")),
    "whole a string": lambda: _signed(_payload(whole="no")),
    "whole a number": lambda: _signed(_payload(whole=0)),
    "days a list": lambda: _signed(_payload(whole=False, days=[["fri"]])),
    "days for a non-member": lambda: _signed(
        _payload(whole=False, days={str(_ids(ARILD)[0]): ["fri"]})
    ),
    "days key not a number": lambda: _signed(_payload(whole=False, days={"x": ["fri"]})),
    "a bad day key": lambda: _signed(
        _payload(whole=False, days={str(_ids(SIGMUND)[0]): ["fri", "mon"]})
    ),
    "an empty day list": lambda: _signed(_payload(whole=False, days={str(_ids(SIGMUND)[0]): []})),
    "a day twice": lambda: _signed(
        _payload(whole=False, days={str(_ids(SIGMUND)[0]): ["sat", "sat"]})
    ),
    "days not a list": lambda: _signed(_payload(whole=False, days={str(_ids(SIGMUND)[0]): "fri"})),
    "missing whole": lambda: _signed({k: v for k, v in _payload().items() if k != "whole"}),
    "missing night": lambda: _signed({k: v for k, v in _payload().items() if k != "night"}),
    "night a list": lambda: _signed(_payload(night=[True])),
    "night not a bool": lambda: _signed(_payload(night={str(_ids(SIGMUND)[0]): "yes"})),
    "night for a non-member": lambda: _signed(_payload(night={str(_ids(ARILD)[0]): True})),
    "meals an unknown key": lambda: _signed(_payload(meals={str(_ids(SIGMUND)[0]): ["lunch"]})),
    "meals an empty list": lambda: _signed(_payload(meals={str(_ids(SIGMUND)[0]): []})),
    "a meal twice": lambda: _signed(
        _payload(meals={str(_ids(SIGMUND)[0]): ["friday_dinner", "friday_dinner"]})
    ),
    "meals for a non-member": lambda: _signed(
        _payload(meals={str(_ids(ARILD)[0]): ["friday_dinner"]})
    ),
}


@pytest.mark.parametrize("make", BROKEN.values(), ids=BROKEN.keys())
def test_a_broken_draft_is_deleted_and_the_form_starts_empty(client, seeded, make):
    """AD-8: step 1 answers 200 with nothing checked and «Jeg er Sigmund», and the
    cookie is deleted with `max-age=0` on the same path; no server error."""
    client.cookies[COOKIE_NAME] = make()
    response = client.get(STEP_1)
    assert response.status_code == 200
    html = response.content.decode()
    assert checked_radios(html) == {"respondent": str(_ids(SIGMUND)[0])}
    assert "<strong>Sigmund</strong>" in html
    cookie = response.cookies[COOKIE_NAME]
    assert cookie.value == ""
    assert cookie["max-age"] == 0
    assert cookie["path"] == f"/{SIGMUND}/"


@pytest.mark.parametrize("make", BROKEN.values(), ids=BROKEN.keys())
def test_a_broken_draft_on_a_frame_goes_to_step_1_and_is_deleted(client, seeded, make):
    """AD-8: a frame with a broken draft redirects to step 1 and deletes it."""
    client.cookies[COOKIE_NAME] = make()
    response = client.get(f"/{SIGMUND}/svar/dager/")
    assert response.status_code == 302
    assert response["Location"] == STEP_1
    assert response.cookies[COOKIE_NAME]["max-age"] == 0


def test_a_valid_post_over_a_broken_draft_writes_a_new_one(client, seeded):
    """AD-8: a broken draft never blocks «Fortsett»: the new draft replaces it."""
    client.cookies[COOKIE_NAME] = BROKEN["bad signature"]()
    response = _post_valid(client)
    assert response.status_code == 302
    payload = signing.loads(response.cookies[COOKIE_NAME].value, salt=SALT)
    assert payload["done"] == ["who"]


def test_a_valid_draft_is_read_back(client, seeded):
    """AD-8: a draft with a valid signature checks what it holds and is not rewritten
    on a GET."""
    client.cookies[COOKIE_NAME] = _signed(_payload())
    response = client.get(STEP_1)
    sigmund, bestemor = _ids(SIGMUND)
    assert COOKIE_NAME not in response.cookies
    assert checked_radios(response.content.decode()) == {
        f"attendance_{sigmund}": "yes",
        f"attendance_{bestemor}": "no",
        "respondent": str(sigmund),
    }


def test_a_draft_older_than_90_days_is_broken(client, seeded, monkeypatch):
    """AD-8: the server checks the signature's age too, not only the browser's
    `max_age`: a draft signed 91 days ago is deleted and the form starts empty."""
    signed_at = time.time() - 91 * 24 * 60 * 60
    payload = _payload()
    with monkeypatch.context() as patch:
        patch.setattr(signing.time, "time", lambda: signed_at)
        client.cookies[COOKIE_NAME] = _signed(payload)
    response = client.get(STEP_1)
    assert response.status_code == 200
    assert response.cookies[COOKIE_NAME]["max-age"] == 0
    assert checked_radios(response.content.decode()) == {"respondent": str(_ids(SIGMUND)[0])}


def test_a_start_time_within_a_minute_ahead_is_accepted(client, seeded):
    """AD-8: a minute of clock skew is allowed for `started`."""
    started = (datetime.now(UTC) + timedelta(seconds=30)).isoformat()
    client.cookies[COOKIE_NAME] = _signed(_payload(started=started))
    response = client.get(STEP_1)
    assert COOKIE_NAME not in response.cookies
