"""Tests prove the numbers match the expected-results list (Story 3.5; FR-69, SM-2).

FR-54, FR-73, FR-74, NFR-2, AD-16, AD-18, FR-26, FR-30: this module is the one place that
compares the app with `wedding/fixtures/expected.toml`, the list counted by hand. It checks every
FR-54 count (the Betaling panel excluded, it waits for Stories 5.3 and 4.3), each household's
total and each guest's status and allergy state, on three levels: the rules, the count registry
and the rendered admin pages. No number is written here: they come from `EXPECTED`, from the
registry in `dashboard/counts.py` and from the keys of seed.toml.

`now`: no rule behind the counts takes a clock, so no test here passes one (a test fails the day
one does, see `test_no_rule_behind_the_counts_takes_now`).

Synne's withdrawal is applied by the fixture `seeded_with_synne_withdrawal`, so the whole list
holds with no offset. The seed alone differs by exactly her nut allergy until Story 7.2.
"""

import inspect
import tomllib

import pytest

from dashboard import counts
from dashboard.counts import ALLERGY_NAMES, COUNTS, HIKE_NAMES, MEALS, PAYMENTS, count_for
from dashboard.selectors import guest_facts, household_totals
from tests.helpers import (
    FIXTURES,
    SYNNE_UNTIL_7_2,
    load_expected,
)
from wedding.models import Guest
from wedding.rules import allergies, households, summary
from wedding.rules.allergies import HAS_ALLERGIES, NO_ALLERGIES, NOTHING_STORED
from wedding.rules.households import COMING, NOT_ANSWERED, NOT_COMING
from wedding.rules.summary import (
    all_households,
    allergy_state_ids,
    answered_households,
    households_by_state,
    people_by_state,
)
from wedding.selectors import form_prices

EXPECTED = load_expected()
SEED = tomllib.loads((FIXTURES / "seed.toml").read_text(encoding="utf-8"))
ALLERGY_STATES = (HAS_ALLERGIES, NO_ALLERGIES, NOTHING_STORED)

# Where each registry slug sits in expected.toml: (section, key). Written here, not in app code,
# so a new registry count without an expected value fails by its slug.
PLACES = {
    "kommer-personer": ("people", COMING),
    "kommer-ikke-personer": ("people", NOT_COMING),
    "ikke-svart-personer": ("people", NOT_ANSWERED),
    "kommer-husstander": ("households", COMING),
    "kommer-ikke-husstander": ("households", NOT_COMING),
    "ikke-svart-husstander": ("households", NOT_ANSWERED),
    "hele-helgen": ("days", "whole_weekend"),
    "ikke-hele-helgen": ("days", "not_whole_weekend"),
    "bare-lordag-sondag": ("days", "sat_sun"),
    "bare-lordag": ("days", "sat"),
    "bare-fredag-lordag": ("days", "fri_sat"),
    "overnatter-ikke": ("overnight", "not_staying"),
    "senger": ("overnight", "beds"),
    "allergi-har": ("allergy_states", HAS_ALLERGIES),
    "allergi-ingen": ("allergy_states", NO_ALLERGIES),
    "allergi-ingen-lagret": ("allergy_states", NOTHING_STORED),
    **{slug: ("meals", meal) for meal, slug, _ in MEALS},
    **{slug: ("allergy_categories", key) for key, (slug, _) in ALLERGY_NAMES.items()},
    **{slug: ("hike", answer) for answer, (slug, _) in HIKE_NAMES.items()},
}
# The day combinations the list does not name: expected.toml says «not whole weekend» is exactly
# the three it names, so these three together are what is left over (a guard test keeps it so).
UNLISTED_DAYS = ("bare-fredag", "bare-sondag", "andre-kombinasjoner")
# `counts.households` keys with no registry slug: they have their own rule functions.
HOUSEHOLD_RULES = {"total": all_households, "answered": answered_households}
PAYMENT_SLUGS = {slug for _, slug, _ in PAYMENTS}
# What this module leaves out for Stories 5.3 and 4.3 (FR-60, FR-61, FR-41).
LEFT_OUT_COUNTS = {"payment_status_coming"}
LEFT_OUT_HOUSEHOLD_KEYS = {"received", "payment_status", "report_matches", "missing", "refund"}
LEFT_OUT_TOP = {"lock"}


@pytest.fixture
def facts(seeded_with_synne_withdrawal):
    return guest_facts()


def expected_for(slug):
    """The expected number of a registry slug, or a failure that names the slug."""
    assert slug in PLACES, f"{slug}: no place in expected.toml"
    section, key = PLACES[slug]
    assert key in EXPECTED["counts"][section], f"{slug}: {section}.{key} missing in expected.toml"
    return EXPECTED["counts"][section][key]


def listed_slugs():
    """Every registry slug this module checks: all but the payment counts."""
    return [count.slug for count in COUNTS if count.slug not in PAYMENT_SLUGS]


def actual_numbers(facts):
    """Every checked registry count as slug -> len() of its id tuple (payment counts left out)."""
    return {slug: len(count_for(slug).ids(facts, {})) for slug in listed_slugs()}


def unlisted_expected():
    """What expected.toml leaves for the unnamed day combinations: not whole weekend minus the
    three it names."""
    days = EXPECTED["counts"]["days"]
    return days["not_whole_weekend"] - days["sat_sun"] - days["sat"] - days["fri_sat"]


def guest_id(key):
    """The id of the seed guest `key` (the name, lower case in expected.toml)."""
    return next(g.id for g in Guest.objects.all() if g.name.lower() == key)


def household_id(key):
    """The id of seed household `key`, found through its first guest."""
    first = next(h for h in SEED["households"] if h["key"] == key)["guests"][0]["key"]
    return Guest.objects.get(id=guest_id(first)).household_id


def test_every_registry_count_equals_expected_toml(facts):
    """FR-54, FR-73, FR-74, AD-2, AD-18: each count is `len()` of its id tuple and equals the
    list, Synne's withdrawal applied, no offset. The failing assert names the slug."""
    actual = actual_numbers(facts)
    for slug, number in actual.items():
        if slug not in UNLISTED_DAYS:
            assert number == expected_for(slug), slug
    assert sum(actual[slug] for slug in UNLISTED_DAYS) == unlisted_expected()


def test_household_counts_without_a_slug_equal_expected_toml(facts):
    """FR-54, FR-74: all households and the answered ones, from their own rule functions."""
    for key, rule in HOUSEHOLD_RULES.items():
        assert len(rule(facts)) == EXPECTED["counts"]["households"][key], key


def test_every_expected_count_is_read_by_a_test(facts):
    """FR-69, SM-2: a count added to expected.toml without a registry slug or a rule here fails."""
    read = {tuple(place) for place in PLACES.values()}
    read |= {("households", key) for key in HOUSEHOLD_RULES}
    stored = {
        (section, key)
        for section, values in EXPECTED["counts"].items()
        if section not in LEFT_OUT_COUNTS
        for key in values
    }
    assert stored == read


def test_every_registry_count_has_an_expected_value():
    """FR-54, AD-2: a registry slug that is neither payment nor placed above fails by its slug."""
    missing = [slug for slug in listed_slugs() if slug not in PLACES and slug not in UNLISTED_DAYS]
    assert missing == []


def test_every_guest_has_the_status_and_allergy_state_of_expected_toml(facts):
    """FR-74, AD-18: status per guest; a coming guest is in exactly one allergy list, the
    expected one; guests not coming or not answered are in none."""
    for key, expected in EXPECTED["guests"].items():
        target = guest_id(key)
        status = next(
            state
            for state in (COMING, NOT_COMING, NOT_ANSWERED)
            if target in people_by_state(facts, state)
        )
        found = [state for state in ALLERGY_STATES if target in allergy_state_ids(facts, state)]
        assert status == expected["status"], key
        assert found == ([expected["allergy_state"]] if status == COMING else []), key


def household_state_of(key):
    """The state of household `key` from the list's `[guests]`: not answered if any guest has not
    answered, coming if any comes, otherwise not coming."""
    statuses = {
        EXPECTED["guests"][guest["key"]]["status"]
        for household in SEED["households"]
        if household["key"] == key
        for guest in household["guests"]
    }
    if NOT_ANSWERED in statuses:
        return NOT_ANSWERED
    return COMING if COMING in statuses else NOT_COMING


def test_every_household_has_the_total_and_state_of_expected_toml(facts):
    """FR-33, FR-74, AD-12: each household's total, and its state, which sums to the counts."""
    totals = household_totals(facts, form_prices())
    for key, expected in EXPECTED["households"].items():
        assert totals[household_id(key)] == expected["total"], key
    for state in (COMING, NOT_COMING, NOT_ANSWERED):
        keys = {key for key in EXPECTED["households"] if household_state_of(key) == state}
        assert len(keys) == EXPECTED["counts"]["households"][state], state
        assert set(households_by_state(facts, state)) == {household_id(key) for key in keys}, state


def test_no_rule_behind_the_counts_takes_now():
    """FR-69, epic context: the counts depend on facts only, so no test passes a clock. The day a
    rule behind a count takes `now`, this fails and the tests must pass an explicit one."""
    for module in (summary, allergies, households):
        for name, function in inspect.getmembers(module, inspect.isfunction):
            if function.__module__ == module.__name__:
                assert "now" not in inspect.signature(function).parameters, (
                    f"{module.__name__}.{name}"
                )
    for name, function in inspect.getmembers(counts, inspect.isfunction):
        assert "now" not in inspect.signature(function).parameters, f"counts.{name}"


def test_the_seed_alone_differs_from_expected_only_by_synne_until_7_2(seeded_with_answers):
    """FR-26, FR-30, AD-18: without the withdrawal the app shows Synne's nut allergy: one nut
    category and one `has_allergies` more, one `nothing_stored` fewer, every other number equal.
    Story 7.2 loads the withdrawal in the seed: delete this test, the fixture
    `seeded_with_synne_withdrawal` and `SYNNE_UNTIL_7_2` then."""
    facts = guest_facts()
    actual = actual_numbers(facts)
    differences = {
        slug: number - expected_for(slug)
        for slug, number in actual.items()
        if slug not in UNLISTED_DAYS and number != expected_for(slug)
    }

    assert differences == {
        ALLERGY_NAMES["nuts"][0]: SYNNE_UNTIL_7_2,
        "allergi-har": SYNNE_UNTIL_7_2,
        "allergi-ingen-lagret": -SYNNE_UNTIL_7_2,
    }
    assert sum(actual[slug] for slug in UNLISTED_DAYS) == unlisted_expected()
    assert guest_id("synne") in allergy_state_ids(facts, HAS_ALLERGIES)
