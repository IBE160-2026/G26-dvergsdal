"""The summary's loader and view model against expected.toml (Story 3.2).

FR-54, FR-69, FR-73, FR-74, NFR-2, AD-2, AD-12, AD-16, AD-18: the seed data is
loaded through `seeded_with_answers`, and every number of the Svar panel and the
six summary panels is compared with the hand-worked list, never a number written
here. Hike, meals and totals need no `now`; no rule here takes one.
"""

import datetime

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from dashboard.counts import count_for, payment_statuses
from dashboard.overview import build_overview
from dashboard.selectors import (
    guest_facts,
    guest_names,
    household_totals,
    households_behind,
    people_behind,
)
from tests.helpers import load_expected
from wedding.models import Consent, Guest, Household, HouseholdAnswer, PersonAnswer
from wedding.rules.allergies import HAS_ALLERGIES, NOTHING_STORED, allergy_state
from wedding.rules.households import COMING, NOT_ANSWERED, household_names
from wedding.rules.money import household_total
from wedding.rules.summary import (
    GuestFacts,
    people_by_state,
)
from wedding.selectors import form_prices, sent_answer

EXPECTED = load_expected()


@pytest.fixture
def facts(seeded_with_answers):
    return guest_facts()


def rows_of(panel):
    return {row.label: row.text for row in panel.rows}


def guest_id(key):
    """The id of the seed guest `key` (the name, lower case in expected.toml)."""
    return next(g.id for g in Guest.objects.all() if g.name.lower() == key)


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
    assert hike["Vil gå turen"] == (
        f"{expected['hike']['yes']} ja, {expected['hike']['maybe']} kanskje"
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


@pytest.mark.parametrize(
    ("events", "state"),
    [
        ((Consent.GIVEN, Consent.WITHDRAWN), NOTHING_STORED),
        ((Consent.WITHDRAWN, Consent.GIVEN), HAS_ALLERGIES),
        ((Consent.GIVEN, Consent.REFUSED), NOTHING_STORED),
    ],
)
def test_the_latest_consent_event_decides_the_allergy_state(seeded_with_answers, events, state):
    """AD-18, FR-26: the loader reads the latest event by `at`; withdrawn removes consent,
    refused is not «Ja», and a later «Ja» after a withdrawal counts again."""
    target = guest_id("bestemor")
    Consent.objects.filter(guest_id=target).delete()
    start = datetime.datetime(2028, 1, 1, tzinfo=datetime.UTC)
    for number, event in enumerate(events):
        Consent.objects.create(
            guest_id=target,
            event=event,
            at=start + datetime.timedelta(days=number),
            given_by_name="Test",
            text_version="test",
        )
    fact = next(guest for guest in guest_facts() if guest.guest_id == target)

    assert fact.allergy is not None
    assert allergy_state(fact.allergy, fact.consent) == state


def test_household_totals_equal_the_total_of_the_sent_answer(seeded_with_answers):
    """FR-33, AD-12, NFR-2: the dashboard's total (whole=False facts) equals `household_total`
    of the stored answer that the receipt uses (`sent_answer`), for every seeded household."""
    prices = form_prices()
    totals = household_totals(guest_facts(), prices)

    for household in Household.objects.all():
        if HouseholdAnswer.objects.filter(household=household).exists():
            assert totals[household.id] == household_total(sent_answer(household), prices)
        else:
            assert totals[household.id] == 0


def facts_for(*days_by_guest):
    """Coming guests in one answered household, each with the given day keys."""
    return [
        GuestFacts(number, 1, True, True, frozenset(days))
        for number, days in enumerate(days_by_guest, start=1)
    ]


def test_day_rows_show_only_above_zero_and_sum_to_not_whole_weekend():
    """FR-54: zero combinations are hidden, and combinations outside the list (Friday and
    Sunday, or no day) show as «Andre kombinasjoner», so the rows add up."""
    facts = facts_for(("fri", "sat", "sun"), ("sat",), ("sat",), ("fri", "sun"), (), ("fri", "sat"))
    when = build_overview(facts, {}).panels[0]
    rows = {row.label: row.text for row in when.rows}
    sub_rows = [row for row in when.rows if row.indent]

    assert rows["Ikke hele helgen"] == "5 personer"
    assert "Bare fredag" not in rows
    assert "Bare søndag" not in rows
    assert rows["Andre kombinasjoner"] == "2 personer"
    assert sum(int(row.text.split()[0]) for row in sub_rows) == 5


def test_no_other_combinations_row_when_all_fit():
    """FR-54: «Andre kombinasjoner» is left out when nothing is left over."""
    when = build_overview(facts_for(("sat",)), {}).panels[0]

    assert "Andre kombinasjoner" not in {row.label for row in when.rows}


@pytest.mark.parametrize(("answered", "percent"), [(0, 0), (1, 1), (100, 50), (200, 100)])
def test_the_bar_is_at_least_one_percent_when_anyone_has_answered(answered, percent):
    """UX-DR39: 1 of 200 answered is not shown as an empty bar; none answered is 0."""
    facts = [
        GuestFacts(number, number, number <= answered, True if number <= answered else None)
        for number in range(1, 201)
    ]

    assert build_overview(facts, {}).progress.percent == percent


def test_people_behind_follow_the_ids_and_name_the_household(seeded_with_answers):
    """FR-55: one entry per id, in the order of the ids, the guest's name and the household
    as the invitation names it; nothing about allergies."""
    ids = tuple(reversed(sorted(guest.id for guest in Guest.objects.all())[:4]))
    people = people_behind(ids)

    assert [person.name for person in people] == [Guest.objects.get(id=i).name for i in ids]
    for person, id_ in zip(people, ids, strict=True):
        household = Guest.objects.get(id=id_).household
        assert person.household == household_names([g.name for g in household.guests.all()])
        assert person.household_id == household.id
        assert set(vars(person)) == {"name", "household", "household_id"}


def test_households_behind_name_every_guest_of_the_household(seeded_with_answers):
    ids = tuple(Household.objects.order_by("-id").values_list("id", flat=True)[:3])
    rows = households_behind(ids)

    assert [row.names for row in rows] == [
        household_names([g.name for g in Household.objects.get(id=i).guests.all()]) for i in ids
    ]
    assert [row.household_id for row in rows] == list(ids)


def test_guest_names_name_every_guest_and_household_in_one_query(
    seeded_with_answers, django_assert_num_queries
):
    """FR-57, FR-58, NFR-2: every guest and household, one query, households as the invitation
    names them."""
    with django_assert_num_queries(1):
        names = guest_names()

    assert names.guests == dict(Guest.objects.order_by("id").values_list("id", "name"))
    for household in Household.objects.all():
        assert names.households[household.id] == household_names(
            [g.name for g in household.guests.order_by("id")]
        )


def test_the_names_load_in_a_fixed_number_of_queries(
    seeded_with_answers, django_assert_num_queries
):
    """NFR-2: two queries for people and one for households, however many ids."""
    guest_ids = tuple(Guest.objects.values_list("id", flat=True))
    household_ids = tuple(Household.objects.values_list("id", flat=True))

    with django_assert_num_queries(2):
        people_behind(guest_ids)
    with django_assert_num_queries(1):
        households_behind(household_ids)


def test_no_ids_give_nothing_and_no_queries(db, django_assert_num_queries):
    with django_assert_num_queries(0):
        assert people_behind(()) == ()
        assert households_behind(()) == ()


def test_every_cell_opens_a_registry_count_of_the_same_size(facts):
    """FR-54, FR-55, AD-2: each cell's slug is a registry entry whose tuple length is the
    cell's number, and the number is written in the cell's text (Senger totalt: bare tallet)."""
    totals = household_totals(facts, form_prices())
    statuses = payment_statuses(facts, totals)
    overview = build_overview(facts, totals)
    rows = [*overview.progress.rows, *(row for panel in overview.panels for row in panel.rows)]
    cells = [cell for row in rows for cell in row.cells]

    assert cells
    for cell in cells:
        assert len(count_for(cell.slug).ids(facts, statuses)) == cell.count, cell.slug
        assert cell.text.split()[0] == str(cell.count), cell.slug
    assert len({cell.slug for cell in cells}) == len(cells)


def test_the_hike_row_keeps_ja_and_kanskje_as_two_counts(facts):
    """FR-17: «3 ja, 2 kanskje» is two cells with their own slugs, never one added number."""
    hike = EXPECTED["counts"]["hike"]
    row = next(
        row
        for panel in build_overview(facts, household_totals(facts, form_prices())).panels
        for row in panel.rows
        if row.label == "Vil gå turen"
    )

    assert [(cell.slug, cell.count) for cell in row.cells] == [
        ("tur-ja", hike["yes"]),
        ("tur-kanskje", hike["maybe"]),
    ]
