"""Allergies, dietary needs and consent on the RSVP form (Story 2.4).

FR-25: each coming person may give fixed categories and a short note, or
«Ingen allergier eller matbehov», which is exclusive. FR-26, AD-18: the
allergy information is stored only with that person's own «Ja» to consent,
and «Ingen …» counts as allergy information too. FR-27: answering «Ja» for
someone else needs «Jeg bekrefter at <name> vet om dette og er enig». FR-28:
sending never requires consent; without it the form says plainly that the
information will not be saved (`not_saved`). AD-2: plain values only.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

# FR-25: the fixed categories, in the order the form shows them.
ALLERGY_KEYS = ("gluten", "lactose", "nuts", "shellfish", "vegetarian", "vegan", "other")
# FR-25: the longest note, counted in characters.
NOTE_MAX = 200

# FR-25, UX-DR21: «Ingen …» together with a category or a note.
CONFLICT = "conflict"
# FR-27: «Ja» for someone else with information entered, not confirmed.
CONFIRM = "confirm"


@dataclass(frozen=True)
class AllergyEntry:
    """FR-25: one person's allergy answer: categories, «Ingen …» and the note."""

    cats: tuple[str, ...] = ()
    none: bool = False
    note: str = ""


EMPTY = AllergyEntry()


def clean_note(text: str) -> str:
    """FR-25: a note with Windows line ends made `\\n` and the outer spaces removed."""
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def has_allergy_info(entry: AllergyEntry) -> bool:
    """FR-25, FR-26, AD-18: whether the person has given any allergy information.

    «Ingen allergier eller matbehov» counts, as does any category or a
    non-empty note.
    """
    return entry.none or bool(entry.cats) or bool(entry.note)


def allergy_problems(
    entry: AllergyEntry, consent: bool | None, confirmed: bool, is_respondent: bool
) -> tuple[str, ...]:
    """FR-25, FR-27, UX-DR21: what stops the step from being done for one person.

    `CONFLICT` when «Ingen …» is ticked together with a category or a note.
    `CONFIRM` when consent is «Ja», the person is not the respondent, they
    have allergy information and the respondent has not confirmed that they
    know and agree. Missing consent is never a problem (FR-28).
    """
    problems = []
    if entry.none and (entry.cats or entry.note):
        problems.append(CONFLICT)
    if consent is True and not is_respondent and has_allergy_info(entry) and not confirmed:
        problems.append(CONFIRM)
    return tuple(problems)


def not_saved(
    coming: Iterable[int],
    allergies: Mapping[int, AllergyEntry],
    consent: Mapping[int, bool],
) -> tuple[int, ...]:
    """FR-28, AD-18: the coming people, in `coming` order, whose allergy information
    will not be saved: information entered, but consent not «Ja»."""
    return tuple(
        guest_id
        for guest_id in coming
        if has_allergy_info(allergies.get(guest_id, EMPTY)) and consent.get(guest_id) is not True
    )
