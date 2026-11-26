"""The couple's summary: every count is the length of an id list (Story 3.2).

FR-54, FR-73, FR-74, AD-2: each rule takes the guests' facts as plain values
(`GuestFacts`) and returns the sorted ids it counts; the dashboard's number is
`len()` of the tuple, and Story 3.3 opens exactly those ids. A guest who has
sent no answer is «not answered», counts for nothing else and is never
dropped. Hike «Nei» is never added to «kommer» or «kanskje». AD-18: allergy
categories and states count only with consent «Ja».
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from wedding.rules.allergies import (
    ALLERGY_KEYS,
    HAS_ALLERGIES,
    AllergyEntry,
    allergy_state,
)
from wedding.rules.days import MEAL_KEYS, WHOLE_WEEKEND
from wedding.rules.households import COMING, household_state, person_state

SATURDAY_LUNCH = "saturday_lunch"
SATURDAY_DINNER = "saturday_dinner"


@dataclass(frozen=True)
class GuestFacts:
    """AD-2: what the summary needs to know about one guest, as plain values.

    `answered` says whether the guest's household has sent an answer, `coming`
    is the guest's «Kommer» (None: no answer from the guest), `days` the day
    keys, `cabin` the overnight stay, `meals` the chosen paid meal keys,
    `hike` the Friday answer (blank: none), `allergy` the stored entry and
    `consent` the latest consent (True only for «Ja» not withdrawn).
    """

    guest_id: int
    household_id: int
    answered: bool
    coming: bool | None
    days: frozenset[str] = frozenset()
    cabin: bool = False
    meals: frozenset[str] = frozenset()
    hike: str = ""
    allergy: AllergyEntry | None = None
    consent: bool | None = None


@dataclass(frozen=True)
class AllergyListEntry:
    """FR-58, AD-18: one line of the allergy list: the guest, their categories in
    `ALLERGY_KEYS` order and their note."""

    guest_id: int
    categories: tuple[str, ...]
    note: str


def _ids(guests: Iterable[GuestFacts]) -> tuple[int, ...]:
    return tuple(sorted(guest.guest_id for guest in guests))


def _coming(facts: Iterable[GuestFacts]) -> list[GuestFacts]:
    return [guest for guest in facts if guest.coming]


def all_households(facts: Iterable[GuestFacts]) -> tuple[int, ...]:
    """FR-54: the sorted ids of every household in `facts`."""
    return tuple(sorted({guest.household_id for guest in facts}))


def answered_households(facts: Iterable[GuestFacts]) -> tuple[int, ...]:
    """FR-54, FR-74: the sorted ids of households that have sent an answer."""
    return tuple(sorted({guest.household_id for guest in facts if guest.answered}))


def households_by_state(facts: Iterable[GuestFacts], state: str) -> tuple[int, ...]:
    """FR-54, FR-74: the sorted ids of households in `state` (coming, not coming, not answered)."""
    members: dict[int, list[GuestFacts]] = {}
    for guest in facts:
        members.setdefault(guest.household_id, []).append(guest)
    return tuple(
        sorted(
            household_id
            for household_id, guests in members.items()
            if household_state(guests[0].answered, [bool(guest.coming) for guest in guests])
            == state
        )
    )


def people_by_state(facts: Iterable[GuestFacts], state: str) -> tuple[int, ...]:
    """FR-54, FR-74: the sorted ids of guests in `state` (no answer: not answered)."""
    return _ids(guest for guest in facts if person_state(guest.coming) == state)


def whole_weekend(facts: Iterable[GuestFacts]) -> tuple[int, ...]:
    """FR-54: the coming guests who are there all three days."""
    return _ids(guest for guest in _coming(facts) if guest.days == WHOLE_WEEKEND)


def not_whole_weekend(facts: Iterable[GuestFacts]) -> tuple[int, ...]:
    """FR-54: the coming guests who are not there all three days."""
    return _ids(guest for guest in _coming(facts) if guest.days != WHOLE_WEEKEND)


def days_only(facts: Iterable[GuestFacts], combo: Iterable[str]) -> tuple[int, ...]:
    """FR-54: the coming guests whose days are exactly `combo` (for example `("sat", "sun")`)."""
    wanted = frozenset(combo)
    return _ids(guest for guest in _coming(facts) if guest.days == wanted)


def other_days(facts: Iterable[GuestFacts], combos: Iterable[Iterable[str]]) -> tuple[int, ...]:
    """FR-54: the coming guests who are not there all three days and whose days are none
    of `combos` (for example Friday and Sunday, or no day at all)."""
    listed = {frozenset(combo) for combo in combos}
    return _ids(
        guest
        for guest in _coming(facts)
        if guest.days != WHOLE_WEEKEND and guest.days not in listed
    )


def not_staying(facts: Iterable[GuestFacts]) -> tuple[int, ...]:
    """FR-54: the coming guests who do not stay overnight."""
    return _ids(guest for guest in _coming(facts) if not guest.cabin)


def beds(facts: Iterable[GuestFacts]) -> tuple[int, ...]:
    """FR-54, FR-16: the coming guests who stay overnight, one bed each."""
    return _ids(guest for guest in _coming(facts) if guest.cabin)


def meal_eaters(facts: Iterable[GuestFacts], meal: str) -> tuple[int, ...]:
    """FR-54, FR-73: the guests who eat `meal`.

    The three paid meals are the guests who chose them. Saturday lunch and
    dinner are paid by the couple and count every coming guest present on
    Saturday.
    """
    if meal in (SATURDAY_LUNCH, SATURDAY_DINNER):
        return _ids(guest for guest in _coming(facts) if "sat" in guest.days)
    if meal not in MEAL_KEYS:
        raise ValueError(f"Unknown meal: {meal}")
    return _ids(guest for guest in _coming(facts) if meal in guest.meals)


def allergy_state_ids(facts: Iterable[GuestFacts], state: str) -> tuple[int, ...]:
    """FR-54, AD-18: the coming guests whose allergy state is `state`; each has exactly one."""
    return _ids(
        guest for guest in _coming(facts) if allergy_state(guest.allergy, guest.consent) == state
    )


def allergy_category_ids(facts: Iterable[GuestFacts], category: str) -> tuple[int, ...]:
    """FR-54, FR-58, AD-18: the coming guests with consent «Ja» who stored `category`."""
    if category not in ALLERGY_KEYS:
        raise ValueError(f"Unknown allergy category: {category}")
    return _ids(
        guest
        for guest in _coming(facts)
        if guest.consent is True and guest.allergy is not None and category in guest.allergy.cats
    )


def allergy_list(facts: Iterable[GuestFacts]) -> tuple[AllergyListEntry, ...]:
    """FR-58, FR-26, AD-18: the allergy list, by guest id: exactly the guests of
    `allergy_state_ids(facts, HAS_ALLERGIES)`, so consent «Ja» (not withdrawn) is checked by the
    same rule as Oversikt and the list is as long as its count. A guest without consent never
    appears, and neither does their note."""
    facts = tuple(facts)
    by_id = {guest.guest_id: guest for guest in facts}
    entries = []
    for guest_id in allergy_state_ids(facts, HAS_ALLERGIES):
        allergy = by_id[guest_id].allergy
        assert allergy is not None  # HAS_ALLERGIES needs a stored entry
        entries.append(
            AllergyListEntry(
                guest_id,
                tuple(key for key in ALLERGY_KEYS if key in allergy.cats),
                allergy.note,
            )
        )
    return tuple(entries)


def hike_ids(facts: Iterable[GuestFacts], answer: str) -> tuple[int, ...]:
    """FR-17, FR-54: the coming guests present on Friday who gave `answer` to the hike.

    Counted per answer; «Nei» is never added to «kommer» or «kanskje».
    """
    return _ids(guest for guest in _coming(facts) if "fri" in guest.days and guest.hike == answer)


def households_by_payment(
    statuses: Mapping[int, str], facts: Iterable[GuestFacts], status: str
) -> tuple[int, ...]:
    """FR-54, FR-60: the sorted ids of coming households whose payment status is `status`.

    `statuses` holds each household's status (`payment_status`); only
    households that are coming are listed.
    """
    coming = set(households_by_state(facts, COMING))
    return tuple(
        sorted(hid for hid, value in statuses.items() if hid in coming and value == status)
    )
