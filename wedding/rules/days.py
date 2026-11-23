"""Which days a guest comes, and what those days open up (Story 2.2).

FR-14, FR-70: a person comes on one or more of the wedding weekend's three
days, and the days must follow each other: Friday and Sunday without Saturday
is refused. The keys are the ones seed.toml uses; the names and dates the form
shows live in the step registry (wedding/rsvp/steps.py, `DAYS`).

FR-16, FR-70: overnight stay needs two or more days in a row, since a cabin is
booked for the nights between them. FR-15, FR-73: the paid meals a person can
be offered follow from their days: Friday dinner on Friday, Saturday breakfast
only after a night from Friday to Saturday, and Sunday breakfast on Sunday.
The meal keys match `programme_prices` (wedding/selectors.py) and seed.toml;
Story 2.3 builds the questions on them, in the order of `MEAL_KEYS`.

FR-17 (Story 2.5): each person present on Friday answers the Friday hike with
one of `HIKE_ANSWERS` («Ja», «Nei», «Kanskje»), the keys seed.toml uses.
"""

from collections.abc import Iterable

DAY_KEYS = ("fri", "sat", "sun")
WHOLE_WEEKEND = frozenset(DAY_KEYS)
# FR-15, FR-73: the paid meals, in the order `offered_meals` returns them.
MEAL_KEYS = ("friday_dinner", "saturday_breakfast", "sunday_breakfast")

# FR-17: the answers to the Friday hike, in the order the form shows them.
HIKE_ANSWERS = ("yes", "no", "maybe")

# FR-14, FR-70: what `day_error` returns for a set that is not allowed.
NO_DAY = "none"
GAP = "gap"


def _day_set(days: Iterable[str]) -> frozenset[str]:
    """FR-14: `days` as a set; a key that is not a day raises ValueError."""
    chosen = frozenset(days)
    unknown = chosen - WHOLE_WEEKEND
    if unknown:
        raise ValueError(f"Unknown day keys: {sorted(unknown)}")
    return chosen


def day_error(days: Iterable[str]) -> str | None:
    """FR-14, FR-70: None for an allowed set of days, else what is wrong with it.

    Allowed are one day, Friday and Saturday, Saturday and Sunday, and all
    three. An empty set gives `"none"`, and Friday and Sunday without Saturday
    `"gap"`. A key that is not in `DAY_KEYS` raises ValueError.
    """
    chosen = _day_set(days)
    if not chosen:
        return NO_DAY
    if {"fri", "sun"} <= chosen and "sat" not in chosen:
        return GAP
    return None


def can_stay_overnight(days: Iterable[str]) -> bool:
    """FR-16, FR-70: True for an allowed set of two or more days in a row."""
    chosen = _day_set(days)
    return day_error(chosen) is None and len(chosen) >= 2


def joins_hike(days: Iterable[str]) -> bool:
    """FR-17: True when the days include Friday, so the person is asked about the hike."""
    return "fri" in _day_set(days)


def offered_meals(days: Iterable[str]) -> tuple[str, ...]:
    """FR-15, FR-73: the paid meals a person with these days can be offered, in order.

    `friday_dinner` when Friday is in the set, `saturday_breakfast` when both
    Friday and Saturday are (the night between them), and `sunday_breakfast`
    when Sunday is. Saturday's lunch and dinner are not asked.
    """
    chosen = _day_set(days)
    meals = []
    if "fri" in chosen:
        meals.append("friday_dinner")
    if {"fri", "sat"} <= chosen:
        meals.append("saturday_breakfast")
    if "sun" in chosen:
        meals.append("sunday_breakfast")
    return tuple(meals)
