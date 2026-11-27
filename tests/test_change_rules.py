"""`answer_changed`: when a re-sent answer really differs (Story 4.1; FR-39, AD-19, AD-2).

Pure rule, no database. Guest 1 and 2 are the household; every case starts
from the same stored answer and changes one thing.
"""

from dataclasses import replace

import pytest

from wedding.rules.allergies import AllergyEntry
from wedding.rules.answer import Answer
from wedding.rules.changes import answer_changed

GLUTEN = AllergyEntry(cats=("gluten",))
STORED = Answer(
    attendance={1: True, 2: True},
    whole=False,
    days={1: ["fri", "sat", "sun"], 2: ["sat", "sun"]},
    night={1: True, 2: True},
    meals={1: ["friday_dinner"], 2: ["saturday_breakfast", "sunday_breakfast"]},
    allergies={1: GLUTEN},
    consent={1: True, 2: False},
    hike={1: "yes"},
)


def test_an_identical_answer_is_not_a_change():
    """FR-39: the same content, even with other list order, never counts."""
    same = replace(
        STORED,
        days={1: ["sun", "sat", "fri"], 2: ["sun", "sat"]},
        meals={1: ["friday_dinner"], 2: ["sunday_breakfast", "saturday_breakfast"]},
        allergies={1: AllergyEntry(cats=("gluten",))},
    )
    assert not answer_changed(STORED, same)


@pytest.mark.parametrize(
    ("what", "new"),
    [
        ("attendance", replace(STORED, attendance={1: True, 2: False})),
        ("days", replace(STORED, days={1: ["fri", "sat", "sun"], 2: ["sun"]})),
        ("whole", replace(STORED, whole=True, days={})),
        ("cabin", replace(STORED, night={1: True, 2: False})),
        ("meal", replace(STORED, meals={1: [], 2: ["saturday_breakfast", "sunday_breakfast"]})),
        ("hike", replace(STORED, hike={1: "no"})),
        ("allergy entry", replace(STORED, allergies={1: AllergyEntry(cats=("gluten", "nuts"))})),
        ("allergy note", replace(STORED, allergies={1: AllergyEntry(cats=("gluten",), note="x")})),
        ("consent flip to no", replace(STORED, consent={1: False, 2: False}, allergies={})),
        ("consent flip to yes", replace(STORED, consent={1: True, 2: True})),
    ],
)
def test_every_kind_of_difference_is_a_change(what, new):
    """FR-39, AD-19: who comes, days, cabin, meals, hike, allergy entry and consent."""
    assert answer_changed(STORED, new), what


def test_a_consent_left_unanswered_never_counts():
    """FR-39, AD-18: the stored data is kept when the new consent is unanswered."""
    kept = replace(STORED, consent={2: False}, allergies={})
    assert not answer_changed(STORED, kept)


def test_a_no_with_the_allergy_still_stored_is_a_change():
    """FR-39, AD-18: «Nei» on a stored «Ja» deletes the entry, so it is a change."""
    assert answer_changed(STORED, replace(STORED, consent={1: False, 2: False}))


def test_a_confirmation_alone_is_not_a_change():
    """FR-39: confirmations are never stored, so they never count."""
    assert not answer_changed(STORED, replace(STORED, confirmed=frozenset({1})))


def test_things_that_no_longer_apply_do_not_count():
    """FR-75, FR-39: a meal or cabin of someone who stops coming is dropped by
    normalising, so only «who comes» differs."""
    stopped = replace(STORED, attendance={1: True, 2: False})
    assert answer_changed(STORED, stopped)
    assert not answer_changed(
        stopped, replace(stopped, night={1: True}, meals={1: ["friday_dinner"]})
    )


def test_a_member_without_a_stored_answer_who_comes_is_a_change():
    """FR-39: a member added after the answer and now coming changes it."""
    stored = Answer(attendance={1: True}, whole=True, night={1: False})
    assert answer_changed(stored, Answer(attendance={1: True, 2: True}, whole=True))
    assert not answer_changed(stored, Answer(attendance={1: True, 2: False}, whole=True))
