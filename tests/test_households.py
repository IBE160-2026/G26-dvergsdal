"""The household size rule: at least 1 and at most 8 people (FR-49, AD-8)."""

import pytest

from wedding.rules.households import MAX_HOUSEHOLD_SIZE, household_size_problem


def test_the_cap_is_8():
    """AD-8: Rikke confirmed 8 as the largest household; the 4 KB draft test relies on it."""
    assert MAX_HOUSEHOLD_SIZE == 8


@pytest.mark.parametrize("count", [1, 8])
def test_1_to_8_people_is_a_valid_household(count):
    """FR-49, AD-8: both bounds are allowed."""
    assert household_size_problem(count) is None


@pytest.mark.parametrize(
    ("count", "message"),
    [
        (0, "En husstand må ha minst én person."),
        (9, "En husstand kan ha høyst 8 personer."),
    ],
)
def test_0_or_9_people_is_refused_with_a_norwegian_message(count, message):
    """FR-49, AD-8: just outside the bounds gives a message the couple can read."""
    assert household_size_problem(count) == message
