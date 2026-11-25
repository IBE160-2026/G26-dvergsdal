"""What is owed and the payment message (Story 2.7; FR-34, FR-36, FR-71, AD-2, AD-4, AD-12).

The «Rules» row of the story's I/O matrix: `guest_balance` is the total less
the reported amount, never below 0; `payment_message` is «Bryllup » and the
household's names.
"""

import pytest

from wedding.rules.households import payment_message
from wedding.rules.money import guest_balance


@pytest.mark.parametrize(
    ("total", "report", "owed"),
    [(4720, None, 4720), (4720, 1000, 3720), (4720, 5000, 0), (0, None, 0)],
)
def test_guest_balance(total, report, owed):
    """FR-34, FR-36, AD-12: nothing reported owes the total; overpaying owes 0."""
    assert guest_balance(total, report) == owed


@pytest.mark.parametrize(
    ("names", "message"),
    [
        (["Synne"], "Bryllup Synne"),
        (["Sigmund", "bestemor"], "Bryllup Sigmund og bestemor"),
        (["Arild", "Marie", "Filippa", "Leone"], "Bryllup Arild, Marie, Filippa og Leone"),
    ],
)
def test_payment_message(names, message):
    """FR-71, AD-4: derived from the names in order, as the hero names the household."""
    assert payment_message(names) == message
