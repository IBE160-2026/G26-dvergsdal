"""The summary rules on small hand-made facts (Story 3.2; FR-54, FR-73, FR-74, AD-2).

Every rule returns sorted ids, and a count is their length. The numbers of the
seed data are asserted in test_overview.py.
"""

from wedding.rules.allergies import HAS_ALLERGIES, NO_ALLERGIES, NOTHING_STORED, AllergyEntry
from wedding.rules.days import DAY_KEYS
from wedding.rules.households import COMING, NOT_ANSWERED, NOT_COMING
from wedding.rules.summary import (
    GuestFacts,
    all_households,
    allergy_category_ids,
    allergy_state_ids,
    answered_households,
    beds,
    days_only,
    hike_ids,
    households_by_payment,
    households_by_state,
    meal_eaters,
    not_staying,
    not_whole_weekend,
    people_by_state,
    whole_weekend,
)

WEEKEND = frozenset(DAY_KEYS)


def guest(guest_id, household=1, answered=True, coming=True, days=WEEKEND, **more):
    return GuestFacts(
        guest_id, household, answered, coming, days if coming else frozenset(), **more
    )


def test_empty_input_gives_empty_tuples():
    """AD-2: no guests means no ids anywhere, and no error."""
    assert people_by_state([], COMING) == ()
    assert households_by_state([], COMING) == ()
    assert whole_weekend([]) == ()
    assert beds([]) == ()
    assert meal_eaters([], "saturday_lunch") == ()
    assert allergy_state_ids([], NOTHING_STORED) == ()
    assert hike_ids([], "yes") == ()


def test_states_of_people_and_households():
    """FR-74: a guest with no answer is not answered; a household is coming when anyone is."""
    facts = [
        guest(1, household=1),
        guest(2, household=1, coming=False),
        guest(3, household=2, coming=False),
        guest(4, household=3, answered=False, coming=None),
        guest(5, household=2, answered=True, coming=None),
    ]
    assert people_by_state(facts, COMING) == (1,)
    assert people_by_state(facts, NOT_COMING) == (2, 3)
    assert people_by_state(facts, NOT_ANSWERED) == (4, 5)
    assert households_by_state(facts, COMING) == (1,)
    assert households_by_state(facts, NOT_COMING) == (2,)
    assert households_by_state(facts, NOT_ANSWERED) == (3,)


def test_whole_weekend_and_partial_days():
    """FR-54: whole weekend, not whole weekend and an exact combination; not coming is left out."""
    facts = [
        guest(1),
        guest(2, days=frozenset({"sat", "sun"})),
        guest(3, days=frozenset({"sat"})),
        guest(4, coming=False),
    ]
    assert whole_weekend(facts) == (1,)
    assert not_whole_weekend(facts) == (2, 3)
    assert days_only(facts, ("sat", "sun")) == (2,)
    assert days_only(facts, ["sat"]) == (3,)


def test_beds_and_not_staying():
    """FR-54, FR-16: one bed per coming guest who stays; the rest do not stay."""
    facts = [guest(1, cabin=True), guest(2), guest(3, coming=False, cabin=True)]
    assert beds(facts) == (1,)
    assert not_staying(facts) == (2,)


def test_saturday_lunch_and_dinner_count_everyone_present_on_saturday():
    """FR-73: lunch and dinner on Saturday are not chosen; Friday-only guests are not there."""
    facts = [
        guest(1, meals=frozenset({"friday_dinner"})),
        guest(2, days=frozenset({"fri"})),
        guest(3, days=frozenset({"sat"})),
        guest(4, coming=False),
    ]
    assert meal_eaters(facts, "saturday_lunch") == (1, 3)
    assert meal_eaters(facts, "saturday_dinner") == (1, 3)
    assert meal_eaters(facts, "friday_dinner") == (1,)


def test_allergy_states_and_categories_need_consent():
    """FR-54, AD-18: each coming guest has one state; categories count only with «Ja»."""
    facts = [
        guest(1, allergy=AllergyEntry(cats=("gluten", "other")), consent=True),
        guest(2, allergy=AllergyEntry(none=True), consent=True),
        guest(3, allergy=AllergyEntry(cats=("nuts",)), consent=None),
        guest(4),
        guest(5, coming=False, allergy=AllergyEntry(cats=("gluten",)), consent=True),
    ]
    assert allergy_state_ids(facts, HAS_ALLERGIES) == (1,)
    assert allergy_state_ids(facts, NO_ALLERGIES) == (2,)
    assert allergy_state_ids(facts, NOTHING_STORED) == (3, 4)
    assert allergy_category_ids(facts, "gluten") == (1,)
    assert allergy_category_ids(facts, "nuts") == ()


def test_hike_counts_each_answer_and_nei_is_not_coming():
    """FR-17, FR-54: only coming guests present on Friday; the three answers stay apart."""
    facts = [
        guest(1, hike="yes"),
        guest(2, hike="maybe"),
        guest(3, hike="no"),
        guest(4, days=frozenset({"sat"})),
        guest(5, coming=False, hike="yes"),
    ]
    assert hike_ids(facts, "yes") == (1,)
    assert hike_ids(facts, "maybe") == (2,)
    assert hike_ids(facts, "no") == (3,)


def test_payment_households_are_only_those_that_come():
    """FR-54, FR-60: a household that does not come is not in the payment panel."""
    facts = [guest(1, household=1), guest(2, household=2, coming=False)]
    statuses = {1: "not_paid", 2: "nothing_to_pay"}
    assert households_by_payment(statuses, facts, "not_paid") == (1,)
    assert households_by_payment(statuses, facts, "nothing_to_pay") == ()


def test_all_and_answered_households():
    """FR-54: «Svart: X av Y» is the answered over all households; none gives none."""
    facts = [
        guest(1, household=1),
        guest(2, household=1),
        guest(3, household=2, answered=False, coming=None),
    ]
    assert all_households(facts) == (1, 2)
    assert answered_households(facts) == (1,)
    assert all_households([]) == ()
    assert answered_households([]) == ()
