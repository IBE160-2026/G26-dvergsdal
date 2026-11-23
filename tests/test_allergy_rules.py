"""The allergy and consent rules (Story 2.4).

FR-25, FR-26, FR-27, FR-28, FR-75, AD-2, AD-18: `has_allergy_info`, each
problem code of `allergy_problems` for the respondent and for someone else,
`not_saved` with consent unanswered, «Nei» and «Ja», `clean_note`, and
`normalise_answer` dropping allergy data for someone who stops coming. The
form over HTTP is in test_rsvp_allergies.py; that `wedding/rules/` imports
no Django is test_rules_purity.py, which scans every module there.
"""

import pytest

from tests.test_rules_purity import BASE_DIR, forbidden_imports
from wedding.rules.allergies import (
    ALLERGY_KEYS,
    CONFIRM,
    CONFLICT,
    EMPTY,
    NOTE_MAX,
    AllergyEntry,
    allergy_problems,
    clean_note,
    has_allergy_info,
    not_saved,
)
from wedding.rules.answer import Answer, normalise_answer
from wedding.rules.money import CABIN, household_total

SIGMUND, BESTEMOR = 1, 2
LACTOSE = AllergyEntry(cats=("lactose",))
NONE = AllergyEntry(none=True)


def test_the_categories_and_the_note_limit():
    """FR-25: seven fixed categories, in form order, and a 200-character note."""
    assert ALLERGY_KEYS == (
        "gluten",
        "lactose",
        "nuts",
        "shellfish",
        "vegetarian",
        "vegan",
        "other",
    )
    assert NOTE_MAX == 200


@pytest.mark.parametrize(
    ("entry", "expected"),
    [
        (EMPTY, False),
        (NONE, True),
        (LACTOSE, True),
        (AllergyEntry(note="ikke koriander"), True),
        (AllergyEntry(note=""), False),
    ],
)
def test_has_allergy_info(entry, expected):
    """FR-26: «Ingen …», any category or a note is allergy information."""
    assert has_allergy_info(entry) is expected


@pytest.mark.parametrize(
    ("entry", "consent", "confirmed", "is_respondent", "expected"),
    [
        # Skip all: nothing entered, nothing answered.
        (EMPTY, None, False, False, ()),
        # Sigmund's journey: his own «Ingen» and «Ja»; bestemor's Laktose, «Ja», confirmed.
        (NONE, True, False, True, ()),
        (LACTOSE, True, True, False, ()),
        # Conflict, by a category or by a note.
        (AllergyEntry(cats=("lactose",), none=True), None, False, False, (CONFLICT,)),
        (AllergyEntry(none=True, note="ikke koriander"), None, False, True, (CONFLICT,)),
        # Missing confirmation (the epics AC).
        (LACTOSE, True, False, False, (CONFIRM,)),
        (NONE, True, False, False, (CONFIRM,)),
        # Both at once.
        (AllergyEntry(cats=("nuts",), none=True), True, False, False, (CONFLICT, CONFIRM)),
        # Confirmation not needed: the respondent's own «Ja», «Ja» with no info, «Nei»,
        # unanswered.
        (LACTOSE, True, False, True, ()),
        (EMPTY, True, False, False, ()),
        (LACTOSE, False, False, False, ()),
        (LACTOSE, None, False, False, ()),
    ],
)
def test_allergy_problems(entry, consent, confirmed, is_respondent, expected):
    """FR-25, FR-27, FR-28, UX-DR21: the problem codes, for the respondent and
    for someone else; missing consent is never one."""
    assert allergy_problems(entry, consent, confirmed, is_respondent) == expected


def test_not_saved_names_whoever_has_info_without_a_ja():
    """FR-28, AD-18: unanswered and «Nei» are not saved, «Ja» is; no info, no
    warning; the order is the household's."""
    allergies = {SIGMUND: NONE, BESTEMOR: LACTOSE, 3: EMPTY}
    assert not_saved([SIGMUND, BESTEMOR, 3], allergies, {}) == (SIGMUND, BESTEMOR)
    assert not_saved([BESTEMOR, SIGMUND], allergies, {}) == (BESTEMOR, SIGMUND)
    assert not_saved([SIGMUND, BESTEMOR], allergies, {BESTEMOR: False}) == (SIGMUND, BESTEMOR)
    assert not_saved([SIGMUND, BESTEMOR], allergies, {SIGMUND: True}) == (BESTEMOR,)
    assert not_saved([SIGMUND, BESTEMOR], allergies, {SIGMUND: True, BESTEMOR: True}) == ()
    assert not_saved([3], allergies, {}) == ()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("   ", ""),
        ("  ikke koriander \r\n", "ikke koriander"),
        ("linje 1\r\nlinje 2", "linje 1\nlinje 2"),
        ("æøå" * 3, "æøå" * 3),
    ],
)
def test_clean_note(text, expected):
    """FR-25: a whitespace note is empty, and line ends count as one character."""
    assert clean_note(text) == expected


def _answer(attendance, **parts) -> Answer:
    return Answer(attendance, True, **parts)


def test_normalise_drops_allergy_data_for_someone_who_stops_coming():
    """FR-75: bestemor «Kommer ikke» loses her entry, consent and confirmation;
    Sigmund keeps his."""
    answer = _answer(
        {SIGMUND: True, BESTEMOR: False},
        allergies={SIGMUND: NONE, BESTEMOR: LACTOSE},
        consent={SIGMUND: True, BESTEMOR: True},
        confirmed=frozenset({SIGMUND, BESTEMOR}),
    )
    normal = normalise_answer(answer)
    assert normal.allergies == {SIGMUND: NONE}
    assert normal.consent == {SIGMUND: True}
    assert normal.confirmed == frozenset({SIGMUND})


def test_normalise_keeps_consent_and_drops_an_empty_entry():
    """FR-26, AD-8: «Nei» keeps the typed allergies (nothing is withdrawn before
    send); an entry with no information is left out."""
    answer = _answer(
        {SIGMUND: True, BESTEMOR: True},
        allergies={SIGMUND: EMPTY, BESTEMOR: LACTOSE},
        consent={BESTEMOR: False},
    )
    normal = normalise_answer(answer)
    assert normal.allergies == {BESTEMOR: LACTOSE}
    assert normal.consent == {BESTEMOR: False}


def test_the_total_ignores_allergies():
    """FR-33: allergies and consent never change the household total."""
    prices = {CABIN: 1500, "friday_dinner": 340, "saturday_breakfast": 260, "sunday_breakfast": 260}
    plain = _answer({SIGMUND: True}, night={SIGMUND: True})
    with_allergies = _answer(
        {SIGMUND: True},
        night={SIGMUND: True},
        allergies={SIGMUND: LACTOSE},
        consent={SIGMUND: True},
    )
    assert household_total(with_allergies, prices) == household_total(plain, prices) == 1500


def test_the_allergy_rules_are_pure():
    """AD-2: the new module imports no Django or project code outside the rules."""
    assert forbidden_imports(BASE_DIR / "wedding" / "rules", BASE_DIR) == []
