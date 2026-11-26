"""The Gjester page and the allergy list as view models (Story 3.4; FR-57, FR-58, UX-DR42, UX-DR48).

Hand-made facts show the order and every line; the seed data is checked against expected.toml in
test_admin_guests_page.py and test_admin_allergy_page.py.
"""

from dashboard.guest_list import (
    NOT_ANSWERED_LINE,
    NOT_COMING_LINE,
    AllergyRow,
    build_allergy_list,
    build_guest_list,
)
from dashboard.selectors import GuestNames
from wedding.rules.allergies import AllergyEntry
from wedding.rules.summary import GuestFacts

NBSP = "\N{NO-BREAK SPACE}"


def guest(guest_id, household, answered=True, coming=True, **more):
    return GuestFacts(guest_id, household, answered, coming, **more)


NAMES = GuestNames(
    guests={1: "Sigmund", 2: "bestemor", 3: "Tor", 4: "Hilde", 5: "Mona", 6: "Åse", 7: "adam"},
    households={
        1: "Sigmund og bestemor",
        2: "Tor og Hilde",
        3: "Mona",
        4: "Åse",
        5: "adam",
    },
)
FACTS = [
    guest(1, 1),
    guest(2, 1, coming=False),
    guest(3, 2, coming=False),
    guest(4, 2, coming=False),
    guest(5, 3, answered=False, coming=None),
    guest(6, 4),
    guest(7, 5),
]
TOTALS = {1: 4720, 2: 0, 3: 0, 4: 1840, 5: 300}


def test_counts_are_the_households_and_guests_of_the_facts():
    """FR-57, UX-DR42: «N husstander · M gjester» from the facts, not from the rows' text."""
    assert build_guest_list(FACTS, NAMES, TOTALS).summary == "5 husstander · 7 gjester"
    assert build_guest_list(FACTS[:1], NAMES, TOTALS).summary == "1 husstand · 1 gjest"


def test_households_not_answered_come_first_then_by_name_ignoring_case():
    """FR-57: unanswered first; the rest by `str.casefold`, so «adam» sits before «Åse» and
    «Sigmund», and an equal name is broken by id."""
    rows = build_guest_list(FACTS, NAMES, TOTALS).rows

    assert [row.names for row in rows] == [
        "Mona",
        "adam",
        "Sigmund og bestemor",
        "Tor og Hilde",
        "Åse",
    ]
    assert [row.answered for row in rows] == [False, True, True, True, True]


def test_equal_names_are_ordered_by_household_id():
    names = GuestNames({1: "Eva", 2: "Eva"}, {7: "Eva", 3: "Eva"})
    facts = [guest(1, 7), guest(2, 3)]

    rows = build_guest_list(facts, names, {7: 0, 3: 0}).rows

    assert [row.household_id for row in rows] == [3, 7]


def test_each_line_variant():
    """FR-57: coming names with the total, «Kommer ikke», «Har ikke svart ennå»; no payment word."""
    rows = {row.household_id: row for row in build_guest_list(FACTS, NAMES, TOTALS).rows}

    assert rows[1].line == f"Kommer: Sigmund · Totalt 4{NBSP}720{NBSP}kr"
    assert rows[2].line == NOT_COMING_LINE == "Kommer ikke"
    assert rows[3].line == NOT_ANSWERED_LINE == "Har ikke svart ennå"
    assert rows[4].line == f"Kommer: Åse · Totalt 1{NBSP}840{NBSP}kr"
    assert not any("betalt" in row.line.lower() for row in rows.values())


def test_a_household_names_everyone_who_comes():
    names = GuestNames({1: "Arild", 2: "Marie", 3: "Leone"}, {1: "Arild, Marie og Leone"})
    facts = [guest(1, 1), guest(2, 1), guest(3, 1, coming=False)]

    row = build_guest_list(facts, names, {1: 6480}).rows[0]

    assert row.line == f"Kommer: Arild og Marie · Totalt 6{NBSP}480{NBSP}kr"
    assert row.names == "Arild, Marie og Leone"


def test_no_households_give_no_rows():
    """UX-DR42: nothing to list."""
    result = build_guest_list([], GuestNames({}, {}), {})

    assert result.rows == ()
    assert result.summary == "0 husstander · 0 gjester"


def test_the_allergy_list_names_categories_by_label_and_keeps_the_note():
    """FR-58, UX-DR48, AD-18: labels of `ALLERGY_NAMES`, in rule order; consent decides."""
    facts = [
        guest(
            1, 1, allergy=AllergyEntry(cats=("other", "shellfish"), note="Mandler"), consent=True
        ),
        guest(2, 1, allergy=AllergyEntry(cats=("nuts",), note="Hemmelig"), consent=False),
        guest(3, 2, allergy=AllergyEntry(cats=("gluten",)), consent=None),
        guest(4, 2, allergy=AllergyEntry(cats=("gluten",)), consent=True),
    ]

    result = build_allergy_list(facts, NAMES)

    assert result.rows == (
        AllergyRow("Sigmund", ("Skalldyr", "Annet"), "Mandler"),
        AllergyRow("Hilde", ("Gluten",), ""),
    )
    assert result.summary == "2 personer"


def test_an_empty_allergy_list():
    """UX-DR48: no consented allergy data: no rows and «0 personer»."""
    result = build_allergy_list([guest(1, 1)], NAMES)

    assert result.rows == ()
    assert result.summary == "0 personer"
