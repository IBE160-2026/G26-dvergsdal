"""The draft cookie that holds an answer between steps (Stories 2.1, 2.2; AD-8).

AD-8, FR-78: until the answer is sent, nothing is stored on the server. The
answers live in one signed, compressed cookie, `rsvp_draft`, scoped to the
mount's cookie path (`/<code>/` for guests), `HttpOnly`, `SameSite=Lax` and
`Secure` in production. Its 90-day lifetime is only a backstop: the server
decides with the deadline rule whether the form is open. The draft is written
first on «Fortsett» or «Velg», never on a GET.

A cookie that cannot be trusted is broken: a bad signature, a signature older
than 90 days (the server checks the age too), a payload that is not zlib or
not JSON, another format version, wrong types, a start time in the future, a
respondent or an attendance key that is not a member of the household, an
unknown step key, or (format 2, Story 2.2) a `whole` that is not true, false
or null, or `days` with a key that is not a member, an empty list, a key that
is not a day, or the same day twice. A format 1 cookie is broken too; nothing
was live then.
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
from wedding.rules.days import DAY_KEYS
from wedding.rules.form_steps import STEP_KEYS

COOKIE_NAME = "rsvp_draft"
SALT = "wedding.rsvp.draft"
VERSION = 2
MAX_AGE = timedelta(days=90)
# A draft that says it started later than this after now is not ours.
FUTURE_SKEW = timedelta(seconds=60)


@dataclass
class Draft:
    """AD-8: what the guest has entered so far.

    `started` is when the draft was first written (ISO 8601, UTC), `rev` the
    household revision it started from, `resp` the respondent's guest id,
    `att` each member's attendance by guest id, `done` the completed steps,
    `whole` the answer to «Er alle som kommer, med hele helgen?» (None while
    unanswered) and `days` each member's chosen day keys by guest id, kept only
    after «Nei» (Story 2.2, FR-14, FR-75).
    """

    started: str
    rev: int
    resp: int
    att: dict[int, bool] = field(default_factory=dict)
    done: list[str] = field(default_factory=list)
    whole: bool | None = None
    days: dict[int, list[str]] = field(default_factory=dict)

    @classmethod
    def new(cls, *, revision: int, respondent: int, now: datetime) -> Draft:
        """AD-8: an empty draft, started `now` at the household's `revision`."""
        return cls(started=now.astimezone(UTC).isoformat(), rev=revision, resp=respondent)

    def payload(self) -> dict[str, object]:
        """AD-8: the cookie's JSON payload, format version 2."""
        return {
            "v": VERSION,
            "started": self.started,
            "rev": self.rev,
            "resp": self.resp,
            "att": {str(guest_id): coming for guest_id, coming in self.att.items()},
            "done": list(self.done),
            "whole": self.whole,
            "days": {str(guest_id): list(days) for guest_id, days in self.days.items()},
        }


PAYLOAD_KEYS = ("v", "started", "rev", "resp", "att", "done", "whole", "days")


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


def _member_key(key: object, member_ids: set[int]) -> int | None:
    """AD-8: a payload key as a member's guest id, or None when it is not one."""
    if isinstance(key, str) and key.isascii() and key.isdigit() and int(key) in member_ids:
        return int(key)
    return None


def _attendance(att: object, member_ids: set[int]) -> dict[int, bool] | None:
    """AD-8: `att` with guest ids as ints, or None unless every key is a member's id."""
    if not isinstance(att, dict):
        return None
    attendance = {}
    for key, coming in att.items():
        guest_id = _member_key(key, member_ids)
        if guest_id is None or not isinstance(coming, bool):
            return None
        attendance[guest_id] = coming
    return attendance


def _is_day_list(value: object) -> bool:
    """AD-8, FR-14: a non-empty list of distinct day keys."""
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(day, str) and day in DAY_KEYS for day in value)
        and len(set(value)) == len(value)
    )


def _days(days: object, member_ids: set[int]) -> dict[int, list[str]] | None:
    """AD-8, FR-14: `days` with guest ids as ints, or None when any entry is off."""
    if not isinstance(days, dict):
        return None
    chosen = {}
    for key, value in days.items():
        guest_id = _member_key(key, member_ids)
        if guest_id is None or not _is_day_list(value):
            return None
        chosen[guest_id] = list(value)
    return chosen


def _parse(payload: object, member_ids: set[int]) -> Draft | None:
    """AD-8: the draft in `payload`, or None when anything is off."""
    if not isinstance(payload, dict) or set(payload) != set(PAYLOAD_KEYS):
        return None
    version, started, rev, resp, att, done, whole, days = (payload[key] for key in PAYLOAD_KEYS)
    attendance = _attendance(att, member_ids)
    chosen_days = _days(days, member_ids)
    if (
        not (_is_int(version) and version == VERSION)
        or not _is_start_time(started)
        or not (_is_int(rev) and rev >= 0)
        or not (_is_int(resp) and resp in member_ids)
        or attendance is None
        or not isinstance(done, list)
        or not all(isinstance(step, str) and step in STEP_KEYS for step in done)
        or not (whole is None or isinstance(whole, bool))
        or chosen_days is None
    ):
        return None
    return Draft(
        started=started,
        rev=rev,
        resp=resp,
        att=attendance,
        done=list(dict.fromkeys(done)),
        whole=whole,
        days=chosen_days,
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
