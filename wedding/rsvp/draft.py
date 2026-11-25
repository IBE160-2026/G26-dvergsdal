"""The draft cookie that holds an answer between steps (Stories 2.1 to 2.6c; AD-8).

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
unknown step key, a `whole` that is not true, false or null (Story 2.2),
`days` with a key that is not a member, an empty list, a key that is not a
day, or the same day twice, `night` (Story 2.3) with a key that is not a
member or a value that is not true or false, or `meals` with a key that is
not a member, an empty list, a key that is not a meal, or the same meal
twice. Story 2.4 adds `alg` (a key that is not a member, an entry without
exactly `c`, `n` and `t`, a category that is not one of `ALLERGY_KEYS` or
repeated, `n` not true or false, `t` not text or longer than `NOTE_MAX`),
`cons` (a key that is not a member, a value not true or false) and `conf`
and `long` (not a list, an id that is not a member, or the same id twice).
Story 2.5 adds `hike` (a key that is not a member, or a value that is not
one of `HIKE_ANSWERS`). Story 2.6c (format 6, AD-18) adds `cv` (not null
and not a string of at most 20 characters). A cookie of format 1 to 5 is
broken too; nothing was live then. The check page's one-time submission id
and the total it showed are hidden fields of its form, not draft fields: they
belong to the rendered page, and neither is an answer.
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
from wedding.rules.allergies import ALLERGY_KEYS, NOTE_MAX, AllergyEntry
from wedding.rules.days import DAY_KEYS, HIKE_ANSWERS, MEAL_KEYS
from wedding.rules.form_steps import STEP_KEYS

COOKIE_NAME = "rsvp_draft"
SALT = "wedding.rsvp.draft"
VERSION = 6
# AD-18: the longest consent-text version a draft may name.
CONSENT_VERSION_MAX = 20
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
    unanswered), `days` each member's chosen day keys by guest id, kept only
    after «Nei» (Story 2.2, FR-14, FR-75), `night` each member's «Ja»/«Nei» to
    the cabin and `meals` each member's chosen meal keys (Story 2.3, FR-15,
    FR-16). Story 2.4 (FR-25 to FR-27): `alg` each member's allergy entry,
    `cons` each member's «Ja»/«Nei» to consent (none: unanswered), `conf` the
    members the respondent confirmed know and agree, and `long` the members
    whose last posted note was too long and was not kept. Story 2.5 (FR-17):
    `hike` each member's answer to the Friday hike, one of `HIKE_ANSWERS`.
    Story 2.6c (AD-18): `cv` the consent-text version step 5 showed when the
    guest last posted it (None before that, or after the text changed).
    """

    started: str
    rev: int
    resp: int
    att: dict[int, bool] = field(default_factory=dict)
    done: list[str] = field(default_factory=list)
    whole: bool | None = None
    days: dict[int, list[str]] = field(default_factory=dict)
    night: dict[int, bool] = field(default_factory=dict)
    meals: dict[int, list[str]] = field(default_factory=dict)
    alg: dict[int, AllergyEntry] = field(default_factory=dict)
    cons: dict[int, bool] = field(default_factory=dict)
    conf: list[int] = field(default_factory=list)
    long: list[int] = field(default_factory=list)
    hike: dict[int, str] = field(default_factory=dict)
    cv: str | None = None

    @classmethod
    def new(cls, *, revision: int, respondent: int, now: datetime) -> Draft:
        """AD-8: an empty draft, started `now` at the household's `revision`."""
        return cls(started=now.astimezone(UTC).isoformat(), rev=revision, resp=respondent)

    def payload(self) -> dict[str, object]:
        """AD-8: the cookie's JSON payload, format version 6."""
        return {
            "v": VERSION,
            "started": self.started,
            "rev": self.rev,
            "resp": self.resp,
            "att": {str(guest_id): coming for guest_id, coming in self.att.items()},
            "done": list(self.done),
            "whole": self.whole,
            "days": {str(guest_id): list(days) for guest_id, days in self.days.items()},
            "night": {str(guest_id): stays for guest_id, stays in self.night.items()},
            "meals": {str(guest_id): list(meals) for guest_id, meals in self.meals.items()},
            "alg": {
                str(guest_id): {"c": list(entry.cats), "n": entry.none, "t": entry.note}
                for guest_id, entry in self.alg.items()
            },
            "cons": {str(guest_id): given for guest_id, given in self.cons.items()},
            "conf": list(self.conf),
            "long": list(self.long),
            "hike": {str(guest_id): choice for guest_id, choice in self.hike.items()},
            "cv": self.cv,
        }


PAYLOAD_KEYS = (
    "v",
    "started",
    "rev",
    "resp",
    "att",
    "done",
    "whole",
    "days",
    "night",
    "meals",
    "alg",
    "cons",
    "conf",
    "long",
    "hike",
    "cv",
)


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


def _is_key_list(value: object, keys: tuple[str, ...], *, allow_empty: bool = False) -> bool:
    """AD-8: a list of distinct keys from `keys`, non-empty unless `allow_empty`."""
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(isinstance(key, str) and key in keys for key in value)
        and len(set(value)) == len(value)
    )


def _key_lists(
    value: object, member_ids: set[int], keys: tuple[str, ...]
) -> dict[int, list[str]] | None:
    """AD-8, FR-14, FR-15: `days` or `meals` with guest ids as ints, or None if any is off."""
    if not isinstance(value, dict):
        return None
    chosen = {}
    for key, entry in value.items():
        guest_id = _member_key(key, member_ids)
        if guest_id is None or not _is_key_list(entry, keys):
            return None
        chosen[guest_id] = list(entry)
    return chosen


def _bools(night: object, member_ids: set[int]) -> dict[int, bool] | None:
    """AD-8, FR-16, FR-26: `night` or `cons` with guest ids as ints, or None when any is off."""
    if not isinstance(night, dict):
        return None
    stays = {}
    for key, value in night.items():
        guest_id = _member_key(key, member_ids)
        if guest_id is None or not isinstance(value, bool):
            return None
        stays[guest_id] = value
    return stays


def _hike(value: object, member_ids: set[int]) -> dict[int, str] | None:
    """AD-8, FR-17: `hike` with guest ids as ints, or None when any is off."""
    if not isinstance(value, dict):
        return None
    answers = {}
    for key, choice in value.items():
        guest_id = _member_key(key, member_ids)
        if guest_id is None or not (isinstance(choice, str) and choice in HIKE_ANSWERS):
            return None
        answers[guest_id] = choice
    return answers


def _allergy_entries(value: object, member_ids: set[int]) -> dict[int, AllergyEntry] | None:
    """AD-8, FR-25: `alg` with guest ids as ints, or None when any entry is off."""
    if not isinstance(value, dict):
        return None
    entries = {}
    for key, entry in value.items():
        guest_id = _member_key(key, member_ids)
        if (
            guest_id is None
            or not isinstance(entry, dict)
            or set(entry) != {"c", "n", "t"}
            or not _is_key_list(entry["c"], ALLERGY_KEYS, allow_empty=True)
            or not isinstance(entry["n"], bool)
            or not isinstance(entry["t"], str)
            or len(entry["t"]) > NOTE_MAX
        ):
            return None
        entries[guest_id] = AllergyEntry(tuple(entry["c"]), entry["n"], entry["t"])
    return entries


def _id_list(value: object, member_ids: set[int]) -> list[int] | None:
    """AD-8, FR-27: `conf` or `long`, distinct member ids, or None when off."""
    if (
        not isinstance(value, list)
        or not all(_is_int(guest_id) and guest_id in member_ids for guest_id in value)
        or len(set(value)) != len(value)
    ):
        return None
    return list(value)


def _parse(payload: object, member_ids: set[int]) -> Draft | None:
    """AD-8: the draft in `payload`, or None when anything is off."""
    if not isinstance(payload, dict) or set(payload) != set(PAYLOAD_KEYS):
        return None
    (
        version,
        started,
        rev,
        resp,
        att,
        done,
        whole,
        days,
        night,
        meals,
        alg,
        cons,
        conf,
        long,
        hike,
        consent_version,
    ) = (payload[key] for key in PAYLOAD_KEYS)
    attendance = _attendance(att, member_ids)
    chosen_days = _key_lists(days, member_ids, DAY_KEYS)
    stays = _bools(night, member_ids)
    chosen_meals = _key_lists(meals, member_ids, MEAL_KEYS)
    entries = _allergy_entries(alg, member_ids)
    consent = _bools(cons, member_ids)
    confirmed = _id_list(conf, member_ids)
    too_long = _id_list(long, member_ids)
    hike_answers = _hike(hike, member_ids)
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
        or stays is None
        or chosen_meals is None
        or entries is None
        or consent is None
        or confirmed is None
        or too_long is None
        or hike_answers is None
        or not (
            consent_version is None
            or (isinstance(consent_version, str) and len(consent_version) <= CONSENT_VERSION_MAX)
        )
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
        night=stays,
        meals=chosen_meals,
        alg=entries,
        cons=consent,
        conf=confirmed,
        long=too_long,
        hike=hike_answers,
        cv=consent_version,
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
