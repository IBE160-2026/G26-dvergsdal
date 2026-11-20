"""The pure rules behind the front page (Story 1.5, FR-6, FR-7, AD-4, UX-DR51).

`household_names` writes the hero's «for …» line from the guests' names (no
household name is stored), `speaks_to_one` picks «deg» or «dere», and
`tel_number` turns a phone number as the couple typed it into a `tel:` link.
They run on plain values, so these tests need no database.
"""

import pytest

from wedding.rules.contacts import tel_number
from wedding.rules.households import household_names, speaks_to_one


@pytest.mark.parametrize(
    ("names", "expected"),
    [
        ([], ""),
        (["Synne"], "Synne"),
        (["Sigmund", "bestemor"], "Sigmund og bestemor"),
        (["Tor", "Hilde", "Eva"], "Tor, Hilde og Eva"),
        (["Arild", "Marie", "Filippa", "Leone"], "Arild, Marie, Filippa og Leone"),
    ],
)
def test_household_names_join_with_commas_and_og(names, expected):
    """FR-7, AD-4: none, one, two, three and four names, as the hero writes them."""
    assert household_names(names) == expected


def test_household_names_keep_the_order_given():
    """FR-7: the order is the caller's (the guests' order by id), never sorted."""
    assert household_names(("bestemor", "Sigmund")) == "bestemor og Sigmund"
    assert household_names(["Leone", "Arild", "Marie"]) == "Leone, Arild og Marie"


@pytest.mark.parametrize(("size", "expected"), [(1, True), (2, False), (8, False)])
def test_speaks_to_one_only_for_a_household_of_one(size, expected):
    """UX-DR51: «deg» for one invited person, «dere» for two or more (up to 8)."""
    assert speaks_to_one(size) is expected


@pytest.mark.parametrize(
    ("phone", "expected"),
    [
        ("+47 000 00 101", "+4700000101"),
        ("900 00 000", "90000000"),
        ("(+47) 900-00-000", "+4790000000"),
        ("+47 (0) 900 00 000", "+4790000000"),
        ("", ""),
        ("ukjent", ""),
    ],
)
def test_tel_number_keeps_a_leading_plus_and_the_digits(phone, expected):
    """FR-6: a `tel:` link takes a leading `+` and digits only, never the «(0)»
    trunk prefix; without a digit there is nothing to call, and the footer leaves
    the contact out."""
    assert tel_number(phone) == expected


def test_tel_number_ignores_a_plus_after_the_first_digit():
    """FR-6: only a `+` before the first digit is a country-code prefix."""
    assert tel_number("900+00 000") == "90000000"
