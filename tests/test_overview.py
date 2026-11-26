"""The summary's loader and view model against expected.toml (Story 3.2).

FR-54, FR-69, FR-73, FR-74, NFR-2, AD-2, AD-12, AD-16, AD-18: the seed data is
loaded through `seeded_with_answers`, and every number of the Svar panel and the
six summary panels is compared with the hand-worked list, never a number written
here. Hike, meals and totals need no `now`; no rule here takes one.
"""

import tomllib
from pathlib import Path

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from dashboard.overview import build_overview
from dashboard.selectors import guest_facts, household_totals
from wedding.models import Guest, PersonAnswer
from wedding.rules.allergies import HAS_ALLERGIES, NO_ALLERGIES, NOTHING_STORED
from wedding.rules.households import COMING, NOT_ANSWERED, NOT_COMING
from wedding.rules.summary import (
    allergy_category_ids,
    allergy_state_ids,
    beds,
    days_only,
    hike_ids,
    households_by_state,
    meal_eaters,
    not_staying,
    not_whole_weekend,
    people_by_state,
    whole_weekend,
)
from wedding.selectors import form_prices

EXPECTED = tomllib.loads(
    (Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "expected.toml").read_text(
        encoding="utf-8"
    )
)
# Story 7.2 loads Synne's withdrawn consent. Until then the seed stores her nut allergy, so the
# app shows one nut allergy, one more `has_allergies` and one fewer `nothing_stored` than
# expected.toml. Story 7.2 removes this constant and the three additions below.
SYNNE_UNTIL_7_2 = 1


@pytest.fixture
def facts(seeded_with_answers):
    return guest_facts()


def rows_of(panel):
    return {row.label: row.text for row in panel.rows}


def guest_id(key):
    """The id of the seed guest `key` (the name, lower case in expected.toml)."""
    return next(g.id for g in Guest.objects.all() if g.name.lower() == key)


def test_counts_equal_expected_toml(facts):
    """FR-54, FR-74, AD-2: people and households per state are the lengths of the rule tuples."""
    expected = EXPECTED["counts"]
    for state in (COMING, NOT_COMING, NOT_ANSWERED):
        assert len(people_by_state(facts, state)) == expected["people"][state]
        assert len(households_by_state(facts, state)) == expected["households"][state]
    days = expected["days"]
    assert len(whole_weekend(facts)) == days["whole_weekend"]
    assert len(not_whole_weekend(facts)) == days["not_whole_weekend"]
    assert len(days_only(facts, ("sat", "sun"))) == days["sat_sun"]
    assert len(days_only(facts, ("sat",))) == days["sat"]
    assert len(days_only(facts, ("fri", "sat"))) == days["fri_sat"]
    assert len(not_staying(facts)) == expected["overnight"]["not_staying"]
    assert len(beds(facts)) == expected["overnight"]["beds"]
    for meal, count in expected["meals"].items():
        assert len(meal_eaters(facts, meal)) == count, meal
    for answer, count in expected["hike"].items():
        assert len(hike_ids(facts, answer)) == count, answer


def test_allergies_equal_expected_toml_except_synne_until_7_2(facts):
    """FR-54, AD-18: categories and states equal the list, with Synne's offset named."""
    categories = EXPECTED["counts"]["allergy_categories"]
    for category, count in categories.items():
        offset = SYNNE_UNTIL_7_2 if category == "nuts" else 0
        assert len(allergy_category_ids(facts, category)) == count + offset, category
    states = EXPECTED["counts"]["allergy_states"]
    assert len(allergy_state_ids(facts, HAS_ALLERGIES)) == states["has_allergies"] + SYNNE_UNTIL_7_2
    assert len(allergy_state_ids(facts, NO_ALLERGIES)) == states["no_allergies"]
    assert (
        len(allergy_state_ids(facts, NOTHING_STORED)) == states["nothing_stored"] - SYNNE_UNTIL_7_2
    )


def test_every_coming_guest_has_exactly_one_allergy_state_as_expected(facts):
    """AD-18: each coming guest is in one state list, the one expected.toml names (Synne aside)."""
    for key, expected in EXPECTED["guests"].items():
        if expected["status"] != "coming" or key == "synne":
            continue
        found = [
            state
            for state in (HAS_ALLERGIES, NO_ALLERGIES, NOTHING_STORED)
            if guest_id(key) in allergy_state_ids(facts, state)
        ]
        assert found == [expected["allergy_state"]], key
    synne = [
        state
        for state in (HAS_ALLERGIES, NO_ALLERGIES, NOTHING_STORED)
        if guest_id("synne") in allergy_state_ids(facts, state)
    ]
    assert len(synne) == 1


def test_household_totals_equal_expected_toml(facts):
    """FR-33, AD-12: each household's total is `household_total` of its sent answer."""
    totals = household_totals(facts, form_prices())
    for key, expected in EXPECTED["households"].items():
        household = Guest.objects.get(id=guest_id(key)).household_id
        assert totals[household] == expected["total"], key


def test_overview_panels_equal_expected_toml(facts):
    """FR-54, UX-DR39, UX-DR40: the Svar line, the panel order and each panel's numbers."""
    overview = build_overview(facts, household_totals(facts, form_prices()))
    expected = EXPECTED["counts"]
    households = expected["households"]

    assert (
        overview.progress.line
        == f"Svart: {households['answered']} av {households['total']} husstander"
    )
    assert overview.progress.percent == round(100 * households["answered"] / households["total"])
    people = expected["people"]
    assert rows_of(overview.progress)["Kommer"] == (
        f"{people['coming']} personer · {households['coming']} husstander"
    )
    assert [panel.title for panel in overview.panels] == [
        "Når kommer de?",
        "Overnatting",
        "Mat",
        "Allergier (med samtykke)",
        "Fjelltur fredag",
        "Betaling (husstander som kommer)",
    ]
    when, overnight, meals, allergies, hike, payment = (rows_of(p) for p in overview.panels)
    assert when["Hele helgen (fre\u2013søn)"] == f"{expected['days']['whole_weekend']} personer"
    assert overnight["Senger totalt"] == str(expected["overnight"]["beds"])
    assert meals["Lunsj lørdag"] == f"{expected['meals']['saturday_lunch']} personer"
    assert allergies["Skalldyr"] == f"{expected['allergy_categories']['shellfish']} person"
    assert hike["Kommer"] == (
        f"{expected['hike']['yes']} kommer, {expected['hike']['maybe']} kanskje"
    )
    assert hike["Kommer ikke"] == f"{expected['hike']['no']} personer"
    assert list(payment) == [
        "Ingenting å betale",
        "Ikke betalt",
        "Delbetalt",
        "Betalt",
        "Skal ha penger tilbake",
    ]


def test_payment_panel_before_payments(facts):
    """FR-60, AD-12: with received 0, a coming household with total 0 owes nothing and the
    others are not paid; each household's total comes from expected.toml."""
    overview = build_overview(facts, household_totals(facts, form_prices()))
    payment = rows_of(overview.panels[5])
    coming = [
        key
        for key, guest in EXPECTED["guests"].items()
        if guest["status"] == "coming" and key in EXPECTED["households"]
    ]
    nothing = sum(1 for key in coming if EXPECTED["households"][key]["total"] == 0)
    owing = len(coming) - nothing
    assert payment["Ingenting å betale"] == f"{nothing} husstand"
    assert payment["Ikke betalt"] == f"{owing} husstander"
    assert payment["Delbetalt"] == "0 husstander"
    assert payment["Betalt"] == "0 husstander"
    assert payment["Skal ha penger tilbake"] == "0 husstander"


def test_no_data_gives_zeros_without_dividing_by_zero(db):
    """FR-54: no households gives «Svart: 0 av 0 husstander», 0 % and zero rows."""
    facts = guest_facts()
    overview = build_overview(facts, household_totals(facts, {}))
    assert overview.progress.line == "Svart: 0 av 0 husstander"
    assert overview.progress.percent == 0
    assert all(row.text.startswith("0") for row in overview.progress.rows)


def test_a_guest_without_a_sent_answer_is_not_answered(seeded_with_answers):
    """FR-74: a guest in an answered household with no `PersonAnswer` is «Ikke svart ennå»."""
    target = guest_id("bestemor")
    PersonAnswer.objects.filter(guest_id=target).delete()
    facts = guest_facts()
    assert target in people_by_state(facts, NOT_ANSWERED)
    assert target not in people_by_state(facts, COMING)


def test_the_loader_uses_a_fixed_number_of_queries(seeded_with_answers):
    """NFR-2: guests, answers, allergies, consents and household answers: five queries."""
    with CaptureQueriesContext(connection) as queries:
        guest_facts()
    assert len(queries) <= 5
