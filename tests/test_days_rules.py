"""The day rules (Story 2.2).

FR-14, FR-15, FR-16, FR-70, FR-73, FR-75, AD-2: one table over all eight
subsets of the weekend's days for `day_error`, `can_stay_overnight` and
`offered_meals` (Friday + Sunday without Saturday is refused, no day is
«none») and an unknown key. `normalise_answer` is in test_answer_rules.py.
"""

import pytest

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
