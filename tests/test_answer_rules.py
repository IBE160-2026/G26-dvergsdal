"""The answer rules and the household total (Stories 2.2, 2.3, 2.5).

FR-14, FR-15, FR-16, FR-33, FR-70, FR-73, FR-75, AD-2, AD-12, NFR-2: every
allowed day combination with what it opens up, `present_days`,
`normalise_answer` for days, overnight stays and meals, `household_total`
for each paid option, the seed households against expected.toml, removed
choices and a price of 0, the shared `kroner` display, and the Friday
hike answer kept only for someone present on Friday (FR-17, Story 2.5).
"""

import tomllib
from itertools import combinations
from pathlib import Path

import pytest

from wedding.rules.answer import Answer, normalise_answer, present_days
from wedding.rules.days import (
    DAY_KEYS,
    HIKE_ANSWERS,
    MEAL_KEYS,
    WHOLE_WEEKEND,
    can_stay_overnight,
    day_error,
    joins_hike,
    offered_meals,
)
from wedding.rules.money import CABIN, household_total
from wedding.templatetags.money import kroner

FIXTURES = Path(__file__).resolve().parent.parent / "wedding" / "fixtures"
SEED = tomllib.loads((FIXTURES / "seed.toml").read_text(encoding="utf-8"))
EXPECTED = tomllib.loads((FIXTURES / "expected.toml").read_text(encoding="utf-8"))
PRICES = {
    CABIN: SEED["settings"]["price_cabin_weekend"],
    "friday_dinner": SEED["settings"]["price_friday_dinner"],
    "saturday_breakfast": SEED["settings"]["price_saturday_breakfast"],
    "sunday_breakfast": SEED["settings"]["price_sunday_breakfast"],
}
DINNER, SAT_BREAKFAST, SUN_BREAKFAST = MEAL_KEYS
ALL = ["fri", "sat", "sun"]
ARILD, MARIE, FILIPPA, LEONE = 1, 2, 3, 4

# Every allowed set of days: (can stay overnight, offered meals).
ALLOWED = {
    ("fri",): (False, (DINNER,)),
    ("sat",): (False, ()),
    ("sun",): (False, (SUN_BREAKFAST,)),
    ("fri", "sat"): (True, (DINNER, SAT_BREAKFAST)),
    ("sat", "sun"): (True, (SUN_BREAKFAST,)),
    ("fri", "sat", "sun"): (True, MEAL_KEYS),
}
SUBSETS = [combo for size in range(4) for combo in combinations(DAY_KEYS, size)]


@pytest.mark.parametrize("days", SUBSETS, ids=str)
def test_every_subset_of_the_days(days):
    """FR-14, FR-15, FR-16, FR-70, FR-73: the six allowed sets open exactly their
    stay and meals; the two refused ones (none, Friday + Sunday) are refused."""
    if days in ALLOWED:
        overnight, meals = ALLOWED[days]
        assert day_error(days) is None
        assert can_stay_overnight(days) is overnight
        assert offered_meals(days) == meals
    else:
        assert day_error(days) is not None
        assert can_stay_overnight(days) is False


def test_present_days():
    """FR-70, UX-DR19: non-comers left out; «Ja» or unanswered is the whole weekend;
    after «Nei» an allowed set counts, an unchosen or refused one is the whole weekend."""
    attendance = {ARILD: True, MARIE: True, FILIPPA: True, LEONE: False}
    days = {ARILD: ["sat"], MARIE: ["fri", "sun"]}
    everyone = dict.fromkeys((ARILD, MARIE, FILIPPA), WHOLE_WEEKEND)
    assert present_days(Answer(attendance, True, days)) == everyone
    assert present_days(Answer(attendance, None, days)) == everyone
    assert present_days(Answer(attendance, False, days)) == everyone | {ARILD: frozenset({"sat"})}


# normalise_answer (FR-75)


def test_yes_drops_every_day():
    """FR-75: «Ja» keeps no days."""
    answer = normalise_answer(Answer({ARILD: True, MARIE: True}, True, {ARILD: ["fri"]}))
    assert (answer.whole, answer.days) == (True, {})


def test_unanswered_keeps_no_days():
    """FR-75: while «Ja»/«Nei» is unanswered there are no days."""
    answer = normalise_answer(Answer({ARILD: True}, None, {ARILD: ["fri"]}))
    assert (answer.whole, answer.days) == (None, {})


def test_days_are_ordered_and_unknown_keys_dropped():
    """FR-75: days in `DAY_KEYS` order, unknown keys and duplicates gone, a member
    left with no day left out, and a non-member dropped."""
    days = {ARILD: ["sun", "mon", "fri", "sun"], MARIE: ["x"], 99: ["fri"]}
    answer = normalise_answer(Answer({ARILD: True, MARIE: True}, False, days))
    assert answer.days == {ARILD: ["fri", "sun"]}


def test_nobody_coming_clears_the_answer():
    """FR-75: nobody coming clears «Ja»/«Nei», days, stays and meals."""
    answer = normalise_answer(
        Answer({ARILD: False}, False, {ARILD: ALL}, {ARILD: True}, {ARILD: [DINNER]})
    )
    assert answer == Answer({ARILD: False}, None, {}, {}, {})


def test_a_non_comer_loses_stay_and_meals():
    """FR-75: Filippa «Kommer ikke»: her days, stay and meals are removed."""
    answer = normalise_answer(
        Answer(
            {ARILD: True, FILIPPA: False},
            False,
            {ARILD: ALL, FILIPPA: ["sat", "sun"]},
            {ARILD: True, FILIPPA: True},
            {ARILD: [DINNER], FILIPPA: [SUN_BREAKFAST]},
        )
    )
    assert answer.days == {ARILD: ALL}
    assert answer.night == {ARILD: True}
    assert answer.meals == {ARILD: [DINNER]}


def test_a_removed_day_drops_what_it_allowed():
    """FR-70, FR-75: Filippa down to Saturday: her «Ja» to the cabin is removed (so
    unanswered) and her Sunday breakfast goes; a «Nei» stays."""
    answer = normalise_answer(
        Answer(
            {ARILD: True, FILIPPA: True},
            False,
            {ARILD: ["sat"], FILIPPA: ["sat"]},
            {ARILD: False, FILIPPA: True},
            {FILIPPA: [SUN_BREAKFAST, "lunch"]},
        )
    )
    assert answer.night == {ARILD: False}
    assert answer.meals == {}


@pytest.mark.parametrize("days", [{}, {FILIPPA: ["fri", "sun"]}], ids=["unchosen", "refused"])
def test_an_unchosen_or_refused_set_keeps_the_choices(days):
    """FR-75, UX-DR19: a half-made day choice counts as the whole weekend, so the
    stay and every meal are kept, in `MEAL_KEYS` order."""
    answer = normalise_answer(
        Answer(
            {FILIPPA: True},
            False,
            days,
            {FILIPPA: True},
            {FILIPPA: [SUN_BREAKFAST, SAT_BREAKFAST, DINNER]},
        )
    )
    assert answer.night == {FILIPPA: True}
    assert answer.meals == {FILIPPA: list(MEAL_KEYS)}


# household_total (FR-33, AD-12, NFR-2)


def _one(night=None, meals=()) -> Answer:
    night_map = {} if night is None else {ARILD: night}
    return Answer({ARILD: True}, True, {}, night_map, {ARILD: list(meals)} if meals else {})


@pytest.mark.parametrize(
    ("answer", "total"),
    [
        (_one(), 0),
        (_one(night=False), 0),
        (_one(night=True), 1500),
        (_one(meals=[DINNER]), 340),
        (_one(meals=[SAT_BREAKFAST]), 260),
        (_one(meals=[SUN_BREAKFAST]), 260),
        (_one(night=True, meals=MEAL_KEYS), 2360),
    ],
)
def test_each_paid_option(answer, total):
    """FR-16, FR-32, FR-33: each paid option alone, and all of them."""
    assert household_total(answer, PRICES) == total


def _seeded(household: dict) -> Answer:
    """A seed household's answer, keyed by each guest's position."""
    coming = [(i, guest) for i, guest in enumerate(household["guests"]) if guest["coming"]]
    return Answer(
        {i: guest["coming"] for i, guest in enumerate(household["guests"])},
        False,
        {i: guest["days"] for i, guest in coming},
        {i: guest["overnight"] for i, guest in coming},
        {i: guest["meals"] for i, guest in coming},
    )


ANSWERED = [household for household in SEED["households"] if "answered_by" in household]


@pytest.mark.parametrize("household", ANSWERED, ids=[h["key"] for h in ANSWERED])
def test_the_seed_households_give_expected_toml(household):
    """FR-33, FR-69: each answered seed household's total is expected.toml's
    (Sigmund 4720, Arild 6480, Synne 0, Tor 0, Eva 1840, Jonas/Ida 4200)."""
    total = EXPECTED["households"][household["key"]]["total"]
    assert household_total(_seeded(household), PRICES) == total


def test_filippa_saturday_and_sunday_and_synne_saturday():
    """FR-16, FR-73: Filippa Saturday + Sunday with a cabin and Sunday breakfast is
    1 760; Synne on Saturday alone owes nothing, whatever was chosen."""
    filippa = Answer(
        {FILIPPA: True},
        False,
        {FILIPPA: ["sat", "sun"]},
        {FILIPPA: True},
        {FILIPPA: [SUN_BREAKFAST]},
    )
    assert household_total(filippa, PRICES) == 1760
    synne = Answer({1: True}, False, {1: ["sat"]}, {1: True}, {1: list(MEAL_KEYS)})
    assert household_total(synne, PRICES) == 0


def test_nobody_coming_and_removed_choices_never_count():
    """FR-75: choices of a non-comer count for nothing."""
    answer = Answer({ARILD: False}, True, {}, {ARILD: True}, {ARILD: list(MEAL_KEYS)})
    assert household_total(answer, PRICES) == 0


def test_a_price_of_zero():
    """FR-32 (Rikke 2026-11-21): a free cabin adds nothing."""
    assert household_total(_one(night=True), PRICES | {CABIN: 0}) == 0


@pytest.mark.parametrize(
    ("amount", "shown"),
    [(0, "0 kr"), (340, "340 kr"), (1450, "1 450 kr"), (12345, "12 345 kr")],
)
def test_kroner(amount, shown):
    """FR-32, Story 2.3 (spec-1-7 deferred): whole kroner with no-break spaces."""
    assert kroner(amount) == shown.replace(" ", "\N{NO-BREAK SPACE}")


# Story 2.5: the Friday hike (FR-17, FR-75)


def test_a_hike_answer_is_kept_for_someone_present_on_friday():
    """FR-17: every answer in `HIKE_ANSWERS` is kept for a member present on Friday,
    and the whole weekend counts as present."""
    for choice in HIKE_ANSWERS:
        answer = Answer({ARILD: True, MARIE: True}, True, hike={ARILD: choice, MARIE: "no"})
        assert normalise_answer(answer).hike == {ARILD: choice, MARIE: "no"}


def test_a_hike_answer_is_dropped_without_friday():
    """FR-17, FR-75: a member whose days lose Friday, or who stops coming, loses the
    answer; the others keep theirs."""
    answer = Answer(
        {ARILD: True, MARIE: True, FILIPPA: False},
        False,
        {ARILD: ["fri", "sat"], MARIE: ["sat", "sun"]},
        hike={ARILD: "yes", MARIE: "maybe", FILIPPA: "yes"},
    )
    assert normalise_answer(answer).hike == {ARILD: "yes"}


def test_a_forged_hike_answer_is_dropped():
    """FR-17: a value outside `HIKE_ANSWERS` is never kept."""
    answer = Answer({ARILD: True}, True, hike={ARILD: "perhaps"})
    assert normalise_answer(answer).hike == {}


def test_the_hike_never_counts_in_the_total():
    """FR-33, AD-12: the hike is free; `household_total` ignores it."""
    assert household_total(Answer({ARILD: True}, True, hike={ARILD: "yes"}), PRICES) == 0


def test_joins_hike():
    """FR-17: only days with Friday are asked about the hike."""
    assert joins_hike(["fri"])
    assert joins_hike(ALL)
    assert not joins_hike(["sat", "sun"])
