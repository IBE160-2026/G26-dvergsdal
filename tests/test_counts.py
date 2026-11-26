"""The count registry (Story 3.3; FR-54, FR-55, AD-2).

Every count is named once in `dashboard.counts`. These tests check the registry
against the rules it wraps, on the seed data, never against a number written here.
"""

import re

import pytest

from dashboard.counts import (
    COUNTS,
    HOUSEHOLDS,
    PEOPLE,
    count_for,
    count_text,
    payment_statuses,
)
from dashboard.selectors import guest_facts, household_totals
from wedding.rules.summary import people_by_state, whole_weekend
from wedding.selectors import form_prices


@pytest.fixture
def facts(seeded_with_answers):
    return guest_facts()


def test_slugs_are_unique_and_url_safe():
    """FR-55: a slug is the address of its count, so it is ASCII, lower case and unique."""
    slugs = [count.slug for count in COUNTS]

    assert len(slugs) == len(set(slugs))
    assert all(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug) for slug in slugs)


def test_every_count_counts_people_or_households():
    assert {count.kind for count in COUNTS} <= {PEOPLE, HOUSEHOLDS}
    assert all(count.title for count in COUNTS)


def test_ids_return_the_tuple_of_the_rule_they_wrap(facts):
    """AD-2: the registry adds nothing; its tuple is the rule's, sorted."""
    assert count_for("hele-helgen").ids(facts, {}) == whole_weekend(facts)
    assert count_for("kommer-personer").ids(facts, {}) == people_by_state(facts, "coming")
    for count in COUNTS:
        statuses = payment_statuses(facts, household_totals(facts, form_prices()))
        ids = count.ids(facts, statuses)
        assert ids == tuple(sorted(ids)), count.slug


def test_the_payment_counts_cover_the_coming_households(facts):
    """FR-60: each coming household is in exactly one payment count."""
    statuses = payment_statuses(facts, household_totals(facts, form_prices()))
    paid = [
        id_
        for count in COUNTS
        if count.slug.startswith("betaling-")
        for id_ in count.ids(facts, statuses)
    ]

    assert sorted(paid) == list(count_for("kommer-husstander").ids(facts, statuses))


def test_count_text_uses_the_right_plural():
    assert count_text(PEOPLE, 1) == "1 person"
    assert count_text(PEOPLE, 9) == "9 personer"
    assert count_text(HOUSEHOLDS, 1) == "1 husstand"
    assert count_text(HOUSEHOLDS, 0) == "0 husstander"


def test_an_unknown_slug_fails():
    with pytest.raises(KeyError):
        count_for("finnes-ikke")
