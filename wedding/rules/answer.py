"""An answer made consistent with itself before it is kept (Stories 2.2, 2.3).

FR-75: when a person stops coming, or a day is removed, the choices that
depended on it are removed and never count. `normalise_answer` runs on every
draft write (AD-8), so the draft never holds days, an overnight stay or a meal
for someone who is not coming, nor a stay or a meal their days do not allow
(FR-16, FR-70, FR-73). `Answer` holds the parts of an answer as plain values
(AD-2), and `present_days` says which days each coming person counts with,
the same way `form_steps` does, so a half-made day choice never drops a later
choice.

Story 2.4: the answer also holds each person's allergy entry, consent and
the respondent's confirmation; `normalise_answer` drops them for anyone who
is not coming (FR-75), and drops an entry with no information in it.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from wedding.rules.allergies import AllergyEntry, has_allergy_info
from wedding.rules.days import (
    DAY_KEYS,
    WHOLE_WEEKEND,
    can_stay_overnight,
    day_error,
    offered_meals,
)


@dataclass(frozen=True)
class Answer:
    """AD-2, FR-13 to FR-16, FR-73: a household's answer as plain values, by guest id.

    `attendance` is each member's «Kommer», `whole` the answer to «Er alle som
    kommer, med hele helgen?» (None while unanswered), `days` each member's
    chosen day keys after «Nei», `night` each member's «Ja»/«Nei» to the cabin
    (a member with no entry has not answered) and `meals` each member's chosen
    meal keys. Story 2.4 (FR-25 to FR-27): `allergies` is each member's
    `AllergyEntry`, `consent` each member's «Ja» (True) or «Nei» (False) to
    storing it (no entry: unanswered), and `confirmed` the members the
    respondent has confirmed know and agree.
    """

    attendance: Mapping[int, bool]
    whole: bool | None
    days: Mapping[int, Iterable[str]] = field(default_factory=dict)
    night: Mapping[int, bool] = field(default_factory=dict)
    meals: Mapping[int, Iterable[str]] = field(default_factory=dict)
    allergies: Mapping[int, AllergyEntry] = field(default_factory=dict)
    consent: Mapping[int, bool] = field(default_factory=dict)
    confirmed: frozenset[int] = frozenset()


def present_days(answer: Answer) -> dict[int, frozenset[str]]:
    """FR-14, FR-70, UX-DR19: the days each coming member counts with, by guest id.

    Members who are not coming are left out. Unless `whole` is False, everyone
    coming counts with the whole weekend; after «Nei», each counts with their
    chosen set when `day_error` allows it, and with the whole weekend while it
    is not chosen or not allowed, as in `form_steps`. The day keys must be
    `DAY_KEYS` (an unknown key raises ValueError, as `day_error` does).
    """
    present = {}
    for guest_id, coming in answer.attendance.items():
        if not coming:
            continue
        chosen = answer.days.get(guest_id) if answer.whole is False else None
        if chosen is not None and day_error(chosen) is None:
            present[guest_id] = frozenset(chosen)
        else:
            present[guest_id] = WHOLE_WEEKEND
    return present


def _kept_days(answer: Answer) -> tuple[bool | None, dict[int, list[str]]]:
    """FR-75 (Story 2.2): `whole` and the days that still apply.

    Nobody coming gives `whole` None. Days are kept only when `whole` is
    False, only for members who are coming, in `DAY_KEYS` order, with unknown
    keys dropped; a member left with no day is left out (the form shows that
    as «no day chosen»). Otherwise there are no days.
    """
    if not any(answer.attendance.values()):
        return None, {}
    if answer.whole is not False:
        return answer.whole, {}
    kept = {}
    for guest_id, chosen in answer.days.items():
        if answer.attendance.get(guest_id):
            chosen_set = set(chosen)
            if ordered := [day for day in DAY_KEYS if day in chosen_set]:
                kept[guest_id] = ordered
    return False, kept


def normalise_answer(answer: Answer) -> Answer:
    """FR-75, FR-16, FR-70, FR-73: `answer` with everything that no longer applies removed.

    First `whole` and the days, as in Story 2.2 (see `_kept_days`). Then, with
    `present_days` of that: `night` keeps only coming members, and a «Ja»
    only when `can_stay_overnight` allows their days; otherwise the entry is
    removed, so the question is unanswered again. `meals` keeps only coming
    members and only the keys `offered_meals` offers for their days, in that
    order; a member left with no meal is left out. Allergy entries, consent
    and confirmations are kept only for coming members (FR-75, Story 2.4), and
    an entry with no information is left out.
    """
    whole, days = _kept_days(answer)
    present = present_days(Answer(answer.attendance, whole, days))
    night = {
        guest_id: stays
        for guest_id, stays in answer.night.items()
        if guest_id in present and (not stays or can_stay_overnight(present[guest_id]))
    }
    meals = {}
    for guest_id, chosen in answer.meals.items():
        if guest_id in present:
            chosen_set = set(chosen)
            if kept := [meal for meal in offered_meals(present[guest_id]) if meal in chosen_set]:
                meals[guest_id] = kept
    allergies = {
        guest_id: entry
        for guest_id, entry in answer.allergies.items()
        if guest_id in present and has_allergy_info(entry)
    }
    consent = {guest_id: given for guest_id, given in answer.consent.items() if guest_id in present}
    confirmed = frozenset(guest_id for guest_id in answer.confirmed if guest_id in present)
    return Answer(dict(answer.attendance), whole, days, night, meals, allergies, consent, confirmed)
