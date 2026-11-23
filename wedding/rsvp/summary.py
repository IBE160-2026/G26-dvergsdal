"""The check page's summary of an answer (Story 2.5; FR-21, FR-28, UX-DR23).

FR-21: before sending, the guest sees one block per step that applies to the
answer, in step order, each with the step's name, an «Endre» link back to that
step and one line per person. The lines are avgjort av Claude 2026-11-23 from
the mockup (key-check-page.html; EXPERIENCE.md, Microcopy): a skipped
optional answer reads «Ikke oppgitt» (shown muted), and the allergy block
carries the FR-28 warning when someone's allergy information will not be
saved (`not_saved`, wedding/rules/allergies.py). There are no prices per line:
only `household_total` adds prices (AD-12, wedding/rules/money.py).

UX-DR23, AD-7: each «Endre» link carries `?fra=se-over`, so «Fortsett» on that
step returns to the check page (wedding/rsvp/views.py, `_continue_url`).

Names and days are joined «a, b og c» by `join_words` (wedding/rsvp/text.py).
"""

from collections.abc import Sequence

from wedding.rsvp import forms
from wedding.rsvp.steps import ALLERGIES, CHECK_SLUG, DAYS, HIKE, MEALS, STEPS, FormMount
from wedding.rsvp.text import join_words
from wedding.rules.allergies import EMPTY, has_allergy_info, not_saved
from wedding.rules.answer import Answer, normalise_answer, present_days
from wedding.rules.days import (
    DAY_KEYS,
    WHOLE_WEEKEND,
    can_stay_overnight,
    joins_hike,
    offered_meals,
)

# UX-DR23: the query an «Endre» link adds, and its only value that counts.
FROM_QUERY = "fra"
MISSING = "Ikke oppgitt"
# UX-DR23: the hidden context after «Endre» where the step's name alone reads
# oddly («Endre hvem som kommer»); otherwise the name, lowercased.
_HIDDEN = {"who": "hvem som kommer"}


def _line(text: str, *, missing: bool = False) -> dict[str, object]:
    return {"text": text, "missing": missing}


def _who_lines(answer: Answer, members, _present, _respondent) -> list[dict]:
    """FR-13, FR-21: every member, «kommer» or «kommer ikke»."""
    return [
        _line(f"{name}: {'kommer' if answer.attendance.get(guest_id) else 'kommer ikke'}")
        for guest_id, name in members
    ]


def _day_names(days: frozenset[str]) -> str:
    """FR-14: «lørdag 27. mai og søndag 28. mai», in `DAY_KEYS` order."""
    return join_words(
        [f"{DAYS[day].name.lower()} {DAYS[day].date}" for day in DAY_KEYS if day in days]
    )


def _days_lines(answer: Answer, members, present, _respondent) -> list[dict]:
    """FR-14, FR-21: each coming member's days, «hele helgen» for all three."""
    return [
        _line(
            f"{name}: hele helgen"
            if present[guest_id] == WHOLE_WEEKEND
            else f"{name}: {_day_names(present[guest_id])}"
        )
        for guest_id, name in members
        if guest_id in present
    ]


def _overnight_lines(answer: Answer, members, present, _respondent) -> list[dict]:
    """FR-16, FR-21: each member who could stay, «hytte hele helgen» or «overnatter ikke»."""
    return [
        _line(f"{name}: {'hytte hele helgen' if answer.night.get(guest_id) else 'overnatter ikke'}")
        for guest_id, name in members
        if guest_id in present and can_stay_overnight(present[guest_id])
    ]


def _meals_lines(answer: Answer, members, present, _respondent) -> list[dict]:
    """FR-15, FR-21: each member offered a meal: their meals in order, or «ingen måltider»."""
    lines = []
    for guest_id, name in members:
        offered = offered_meals(present[guest_id]) if guest_id in present else ()
        if not offered:
            continue
        chosen = set(answer.meals.get(guest_id, ()))
        names = [MEALS[meal].name.lower() for meal in offered if meal in chosen]
        lines.append(_line(f"{name}: {join_words(names) if names else 'ingen måltider'}"))
    return lines


def _allergy_lines(answer: Answer, members, present, respondent) -> list[dict]:
    """FR-21, FR-25 to FR-27: each coming member's allergies, note and consent."""
    lines = []
    for guest_id, name in members:
        if guest_id not in present:
            continue
        entry = answer.allergies.get(guest_id, EMPTY)
        if not has_allergy_info(entry):
            lines.append(_line(f"{name}: {MISSING}", missing=True))
            continue
        if entry.cats:
            cats = join_words([ALLERGIES[key].lower() for key in entry.cats])
            lines.append(_line(f"{name}: {cats}"))
            if entry.note:
                lines.append(_line(f"Merknad om {name}: {entry.note}"))
        elif entry.none:
            lines.append(_line(f"{name}: ingen allergier eller matbehov"))
        else:
            lines.append(_line(f"Merknad om {name}: {entry.note}"))
        consent = answer.consent.get(guest_id)
        if consent is None:
            lines.append(_line(f"Samtykke for {name}: {MISSING}", missing=True))
        else:
            lines.append(_line(f"Samtykke for {name}: {'ja' if consent else 'nei'}"))
        if guest_id != respondent and guest_id in answer.confirmed:
            lines.append(_line(f"Du har bekreftet at {name} vet om det og er enig."))
    return lines


def _hike_lines(answer: Answer, members, present, _respondent) -> list[dict]:
    """FR-17, FR-21: each member present on Friday, «ja», «nei» or «kanskje»."""
    lines = []
    for guest_id, name in members:
        if guest_id in present and joins_hike(present[guest_id]):
            choice = answer.hike.get(guest_id)
            if choice is None:
                lines.append(_line(f"{name}: {MISSING}", missing=True))
            else:
                lines.append(_line(f"{name}: {HIKE[choice].lower()}"))
    return lines


_LINES = {
    "who": _who_lines,
    "days": _days_lines,
    "overnight": _overnight_lines,
    "meals": _meals_lines,
    "allergies": _allergy_lines,
    "hike": _hike_lines,
}


def check_parts(
    answer: Answer,
    *,
    members: Sequence[tuple[int, str]],
    respondent: int,
    steps: Sequence[str],
    mount: FormMount,
) -> list[dict[str, object]]:
    """FR-21, FR-28, UX-DR23: one block per applicable step in `steps`, in order.

    Each block is `{key, name, url, hidden, lines, warning}`: the step's name
    from the registry, its address with `?fra=se-over`, the hidden context of
    its «Endre» link, its lines (`{text, missing}`) and, on the allergy block,
    the FR-28 warning text when `not_saved` names anyone (else "").
    `answer` is normalised first (FR-75).
    """
    answer = normalise_answer(answer)
    present = present_days(answer)
    parts = []
    for key in steps:
        step = STEPS[key]
        warning = ""
        if key == "allergies":
            coming = [guest_id for guest_id, _ in members if guest_id in present]
            unsaved = set(not_saved(coming, answer.allergies, answer.consent))
            names = [name for guest_id, name in members if guest_id in unsaved]
            warning = forms.AllergiesForm.warning_text(names) if names else ""
        parts.append(
            {
                "key": key,
                "name": step.name,
                "url": f"{mount.url(key)}?{FROM_QUERY}={CHECK_SLUG}",
                "hidden": _HIDDEN.get(key, step.name.lower()),
                "lines": _LINES[key](answer, members, present, respondent),
                "warning": warning,
            }
        )
    return parts
