"""The day rules and `normalise_answer` (Story 2.2).

FR-14, FR-15, FR-16, FR-70, FR-73, FR-75, AD-2: one table over all eight
subsets of the weekend's days for `day_error`, `can_stay_overnight` and
`offered_meals` (Friday + Sunday without Saturday is refused, no day is
«none»), an unknown key, and `normalise_answer` for the cases in the story's
I/O matrix.
"""

import pytest

from wedding.rules.answer import normalise_answer
from wedding.rules.days import (
    DAY_KEYS,
    WHOLE_WEEKEND,
    can_stay_overnight,
    day_error,
    offered_meals,
)

FRI, SAT, SUN = "friday_dinner", "saturday_breakfast", "sunday_breakfast"

# (days, day_error, can_stay_overnight, offered_meals)
SUBSETS = [
    ((), "none", False, ()),
    (("fri",), None, False, (FRI,)),
    (("sat",), None, False, ()),
    (("sun",), None, False, (SUN,)),
    (("fri", "sat"), None, True, (FRI, SAT)),
    (("sat", "sun"), None, True, (SUN,)),
    (("fri", "sun"), "gap", False, (FRI, SUN)),
    (("fri", "sat", "sun"), None, True, (FRI, SAT, SUN)),
]


def test_the_keys_are_the_seed_keys():
    """FR-14: the day keys seed.toml uses, and the whole weekend is all three."""
    assert DAY_KEYS == ("fri", "sat", "sun")
    assert frozenset(DAY_KEYS) == WHOLE_WEEKEND


@pytest.mark.parametrize(("days", "error", "overnight", "meals"), SUBSETS, ids=str)
def test_every_subset_of_the_weekend(days, error, overnight, meals):
    """FR-14, FR-15, FR-16, FR-70, FR-73: all eight subsets, in any order."""
    assert day_error(days) == error
    assert day_error(reversed(days)) == error
    assert can_stay_overnight(days) is overnight
    assert offered_meals(days) == meals
    assert offered_meals(list(reversed(days))) == meals


@pytest.mark.parametrize("rule", [day_error, can_stay_overnight, offered_meals])
def test_an_unknown_day_key_raises(rule):
    """FR-14: a key that is not a day is a programming error, not a choice."""
    with pytest.raises(ValueError, match="mon"):
        rule(["fri", "mon"])


# normalise_answer (FR-75)

ARILD, MARIE, FILIPPA, LEONE = 1, 2, 3, 4
ALL = ["fri", "sat", "sun"]


def test_yes_drops_every_day():
    """FR-75: «Ja» keeps no days."""
    attendance = {ARILD: True, MARIE: True}
    assert normalise_answer(attendance, True, {ARILD: ["fri"]}) == (True, {})


def test_unanswered_keeps_no_days():
    """FR-75: while «Ja»/«Nei» is unanswered there are no days."""
    assert normalise_answer({ARILD: True}, None, {ARILD: ["fri"]}) == (None, {})


def test_someone_who_stops_coming_loses_their_days():
    """FR-75: Filippa says «Kommer ikke» after choosing days: hers are removed."""
    attendance = {ARILD: True, MARIE: True, FILIPPA: False, LEONE: False}
    days = {ARILD: ALL, MARIE: ALL, FILIPPA: ["sat", "sun"]}
    assert normalise_answer(attendance, False, days) == (False, {ARILD: ALL, MARIE: ALL})


def test_days_are_ordered_and_unknown_keys_dropped():
    """FR-75: days in `DAY_KEYS` order, unknown keys and duplicates gone, a member
    left with no day left out, and a non-member dropped."""
    attendance = {ARILD: True, MARIE: True}
    days = {ARILD: ["sun", "mon", "fri", "sun"], MARIE: ["x"], 99: ["fri"]}
    assert normalise_answer(attendance, False, days) == (False, {ARILD: ["fri", "sun"]})


def test_nobody_coming_clears_the_answer():
    """FR-75: nobody coming makes «Ja»/«Nei» unanswered and drops every day."""
    attendance = {ARILD: False, MARIE: False}
    assert normalise_answer(attendance, False, {ARILD: ALL}) == (None, {})
    assert normalise_answer(attendance, True, {}) == (None, {})
