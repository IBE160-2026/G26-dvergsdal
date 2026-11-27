"""What differs between a draft and the stored answer (Story 4.2; FR-38, AD-9, AD-2).

`answer_differences` is pure, so these tests build `Answer`s by hand: one test
per topic, a guest on one side only, identical answers and normalisation first.
"""

from wedding.rules.allergies import AllergyEntry
from wedding.rules.answer import Answer
from wedding.rules.differences import Difference, answer_differences

ALL = frozenset({"fri", "sat", "sun"})


def _base(**overrides) -> Answer:
    """Guests 1 and 2 coming the whole weekend, 2 with a cabin, a meal and a hike answer."""
    parts = {
        "attendance": {1: True, 2: True},
        "whole": True,
        "night": {1: False, 2: True},
        "meals": {1: ["friday_dinner"], 2: ["friday_dinner", "saturday_breakfast"]},
        "hike": {1: "yes", 2: "no"},
    }
    return Answer(**(parts | overrides))


def test_identical_answers_differ_in_nothing():
    """FR-38 (matrix «Identical content»): an empty list."""
    assert answer_differences(_base(), _base()) == []


def test_attendance_is_compared_for_every_guest():
    """FR-38: coming or not, and nothing else for a guest who is not coming on both sides."""
    mine = _base(attendance={1: True, 2: False})
    assert answer_differences(mine, _base()) == [Difference(2, "attendance", False, True)]


def test_a_guest_on_one_side_only_differs_in_attendance_only():
    """FR-38: a member the stored answer has no row for (added after it was sent)."""
    mine = _base(attendance={1: True, 2: True, 3: True})
    assert answer_differences(mine, _base()) == [Difference(3, "attendance", True, None)]


def test_days_are_compared_only_when_both_come():
    """FR-14, FR-38: Saturday and Sunday on one side, the whole weekend on the other."""
    mine = _base(whole=False, days={1: ["fri", "sat", "sun"], 2: ["sat", "sun"]})
    found = answer_differences(mine, _base())
    assert [d for d in found if d.topic == "days"] == [
        Difference(2, "days", frozenset({"sat", "sun"}), ALL)
    ]


def test_the_cabin_differs():
    """FR-16, FR-38 (matrix «Differences listed»): «Ja» against «Nei»."""
    mine = _base(night={1: False, 2: False})
    assert answer_differences(mine, _base()) == [Difference(2, "cabin", False, True)]


def test_meals_are_compared_as_sets():
    """FR-15, FR-38: the order never counts, a missing meal does."""
    same = _base(meals={1: ["friday_dinner"], 2: ["saturday_breakfast", "friday_dinner"]})
    assert answer_differences(same, _base()) == []
    fewer = _base(meals={1: ["friday_dinner"], 2: ["friday_dinner"]})
    assert answer_differences(fewer, _base()) == [
        Difference(
            2,
            "meals",
            frozenset({"friday_dinner"}),
            frozenset({"friday_dinner", "saturday_breakfast"}),
        )
    ]


def test_the_hike_differs_and_no_answer_is_empty():
    """FR-17, FR-38: «yes» against «maybe», and an answer against none."""
    mine = _base(hike={1: "maybe"})
    assert answer_differences(mine, _base()) == [
        Difference(1, "hike", "maybe", "yes"),
        Difference(2, "hike", "", "no"),
    ]


def test_allergies_differ_without_the_note_leaving_the_key():
    """FR-25, FR-38: a different entry is a difference; the same entry with the categories
    in another order is not."""
    stored = _base(allergies={1: AllergyEntry(("gluten", "nuts"), False, "")})
    reordered = _base(allergies={1: AllergyEntry(("nuts", "gluten"), False, "")})
    assert answer_differences(reordered, stored) == []
    other = _base(allergies={1: AllergyEntry(("gluten",), False, "")})
    assert [d.topic for d in answer_differences(other, stored)] == ["allergies"]


def test_confirmations_and_consent_never_count():
    """FR-38, AD-18: a draft's cleared consent and a confirmation are not differences."""
    mine = _base(consent={1: True}, confirmed=frozenset({2}))
    assert answer_differences(mine, _base(consent={})) == []


def test_normalisation_comes_first():
    """FR-75, FR-38: days, a cabin and a meal kept for a guest who is not coming do not count."""
    mine = _base(
        attendance={1: True, 2: False},
        whole=False,
        days={1: ["fri", "sat", "sun"], 2: ["sat"]},
        night={1: False, 2: True},
        meals={1: ["friday_dinner"], 2: ["friday_dinner"]},
        hike={1: "yes", 2: "yes"},
    )
    stored = _base(attendance={1: True, 2: False}, night={1: False}, meals={1: ["friday_dinner"]})
    assert answer_differences(mine, stored) == []


def test_differences_are_in_guest_order_then_topic_order():
    """FR-38: per guest id, each guest's topics together."""
    mine = _base(night={1: True, 2: False}, hike={1: "no", 2: "no"})
    assert [(d.guest_id, d.topic) for d in answer_differences(mine, _base())] == [
        (1, "cabin"),
        (1, "hike"),
        (2, "cabin"),
    ]
