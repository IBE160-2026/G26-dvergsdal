"""The draft cookie that holds an answer between steps (Story 2.1, AD-8).

AD-8, FR-78: until the answer is sent, nothing is stored on the server. The
answers live in one signed, compressed cookie, `rsvp_draft`, scoped to the
mount's cookie path (`/<code>/` for guests), `HttpOnly`, `SameSite=Lax` and
`Secure` in production. Its 90-day lifetime is only a backstop: the server
decides with the deadline rule whether the form is open. The draft is written
first on «Fortsett» or «Velg», never on a GET.

A cookie that cannot be trusted is broken: a bad signature, a signature older
than 90 days (the server checks the age too), a payload that is not zlib or
not JSON, another format version, wrong types, a start time in the future, a
respondent or an attendance key that is not a member of the household, or an
unknown step key.
A broken draft is deleted and the form starts empty, never with a server
error. (Story 2.9 will drop changed members instead of deleting.)
"""

import zlib
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from django.conf import settings
from django.core import signing
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from wedding.rsvp.steps import FormMount
from wedding.rules.form_steps import STEP_KEYS

COOKIE_NAME = "rsvp_draft"
SALT = "wedding.rsvp.draft"
VERSION = 1
MAX_AGE = timedelta(days=90)
# A draft that says it started later than this after now is not ours.
FUTURE_SKEW = timedelta(seconds=60)


@dataclass
class Draft:
    """AD-8: what the guest has entered so far.

    `started` is when the draft was first written (ISO 8601, UTC), `rev` the
    household revision it started from, `resp` the respondent's guest id,
    `att` each member's attendance by guest id, and `done` the completed steps.
    """

    started: str
    rev: int
    resp: int
    att: dict[int, bool] = field(default_factory=dict)
    done: list[str] = field(default_factory=list)

    @classmethod
    def new(cls, *, revision: int, respondent: int, now: datetime) -> Draft:
        """AD-8: an empty draft, started `now` at the household's `revision`."""
        return cls(started=now.astimezone(UTC).isoformat(), rev=revision, resp=respondent)

    def payload(self) -> dict[str, object]:
        """AD-8: the cookie's JSON payload, format version 1."""
        return {
            "v": VERSION,
            "started": self.started,
            "rev": self.rev,
            "resp": self.resp,
            "att": {str(guest_id): coming for guest_id, coming in self.att.items()},
            "done": list(self.done),
        }


PAYLOAD_KEYS = ("v", "started", "rev", "resp", "att", "done")


def _is_int(value: object) -> bool:
    # bool is a subclass of int, but True is not a guest id.
    return type(value) is int


def _is_start_time(value: object) -> bool:
    """AD-8: an aware ISO time that is not in the future (a minute of clock skew allowed)."""
    try:
        started = datetime.fromisoformat(value) if isinstance(value, str) else None
    except ValueError:
        return False
    if started is None or started.tzinfo is None:
        return False
    return started <= timezone.now() + FUTURE_SKEW


def _attendance(att: object, member_ids: set[int]) -> dict[int, bool] | None:
    """AD-8: `att` with guest ids as ints, or None unless every key is a member's id."""
    if not isinstance(att, dict):
        return None
    attendance = {}
    for key, coming in att.items():
        if not (isinstance(key, str) and key.isascii() and key.isdigit()):
            return None
        if int(key) not in member_ids or not isinstance(coming, bool):
            return None
        attendance[int(key)] = coming
    return attendance


def _parse(payload: object, member_ids: set[int]) -> Draft | None:
    """AD-8: the draft in `payload`, or None when anything is off."""
    if not isinstance(payload, dict) or set(payload) != set(PAYLOAD_KEYS):
        return None
    version, started, rev, resp, att, done = (payload[key] for key in PAYLOAD_KEYS)
    attendance = _attendance(att, member_ids)
    if (
        not (_is_int(version) and version == VERSION)
        or not _is_start_time(started)
        or not (_is_int(rev) and rev >= 0)
        or not (_is_int(resp) and resp in member_ids)
        or attendance is None
        or not isinstance(done, list)
        or not all(isinstance(step, str) and step in STEP_KEYS for step in done)
    ):
        return None
    return Draft(
        started=started, rev=rev, resp=resp, att=attendance, done=list(dict.fromkeys(done))
    )


def read_draft(request: HttpRequest, member_ids: set[int]) -> tuple[Draft | None, bool]:
    """AD-8: (the draft, False), (None, False) without a cookie, or (None, True) when broken."""
    value = request.COOKIES.get(COOKIE_NAME)
    if value is None:
        return None, False
    try:
        payload = signing.loads(value, salt=SALT, max_age=MAX_AGE)
    except signing.BadSignature, zlib.error, ValueError, TypeError:
        return None, True
    draft = _parse(payload, member_ids)
    return draft, draft is None


def write_draft(response: HttpResponse, draft: Draft, mount: FormMount) -> None:
    """AD-8: set the draft cookie on `response`, scoped to the mount's cookie path."""
    response.set_cookie(
        COOKIE_NAME,
        signing.dumps(draft.payload(), salt=SALT, compress=True),
        max_age=MAX_AGE,
        path=mount.cookie_path,
        secure=settings.IS_PRODUCTION,
        httponly=True,
        samesite="Lax",
    )


def delete_draft(response: HttpResponse, mount: FormMount) -> None:
    """AD-8: delete the draft cookie, with the same path it was set with."""
    response.delete_cookie(COOKIE_NAME, path=mount.cookie_path, samesite="Lax")
