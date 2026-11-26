"""Oversikt's view model: the Svar panel and the six summary panels (Story 3.2).

FR-54, FR-73, FR-74, UX-DR39, UX-DR40, AD-2: `build_overview` turns the rules of
`wedding.rules.summary` into Norwegian labels and count texts. A count is only
ever `len()` of an id tuple a rule returned; nothing here filters or adds, and
the template shows the result as it is. Until Story 3.3 every count is plain
text, not a link. «Stemmer ikke» is an attention item (FR-61), not a count here.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from wedding.rules.allergies import ALLERGY_KEYS, HAS_ALLERGIES, NO_ALLERGIES, NOTHING_STORED
from wedding.rules.days import HIKE_ANSWERS
from wedding.rules.households import COMING, NOT_ANSWERED, NOT_COMING
from wedding.rules.money import (
    NOT_PAID,
    NOTHING_TO_PAY,
    PAID,
    PART_PAID,
    REFUND_OWED,
    payment_status,
)
from wedding.rules.summary import (
    SATURDAY_DINNER,
    SATURDAY_LUNCH,
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
    other_days,
    people_by_state,
    whole_weekend,
)

# FR-54: the day combinations that «Ikke hele helgen» is broken down by.
DAY_COMBOS = (
    (("sat", "sun"), "Bare lørdag\u2013søndag"),
    (("sat",), "Bare lørdag"),
    (("fri", "sat"), "Bare fredag\u2013lørdag"),
    (("fri",), "Bare fredag"),
    (("sun",), "Bare søndag"),
)
MEAL_LABELS = {
    "friday_dinner": "Middag fredag",
    "saturday_breakfast": "Frokost lørdag",
    SATURDAY_LUNCH: "Lunsj lørdag",
    SATURDAY_DINNER: "Middag lørdag",
    "sunday_breakfast": "Frokost søndag",
}
# FR-54: Saturday lunch and dinner sit between the breakfasts, in the order of the weekend.
MEAL_ORDER = (
    "friday_dinner",
    "saturday_breakfast",
    SATURDAY_LUNCH,
    SATURDAY_DINNER,
    "sunday_breakfast",
)
ALLERGY_LABELS = {
    "gluten": "Gluten",
    "lactose": "Laktose",
    "nuts": "Nøtter",
    "shellfish": "Skalldyr",
    "vegetarian": "Vegetar",
    "vegan": "Vegan",
    "other": "Annet",
}
PAYMENT_LABELS = (
    (NOTHING_TO_PAY, "Ingenting å betale"),
    (NOT_PAID, "Ikke betalt"),
    (PART_PAID, "Delbetalt"),
    (PAID, "Betalt"),
    (REFUND_OWED, "Skal ha penger tilbake"),
)


@dataclass(frozen=True)
class Row:
    """One label with its count text, as a `dl` pair."""

    label: str
    text: str
    indent: bool = False


@dataclass(frozen=True)
class Panel:
    """A summary panel: its `h2` and its rows, and an optional note under them."""

    title: str
    rows: tuple[Row, ...]
    note: str = ""


@dataclass(frozen=True)
class Progress:
    """UX-DR39: the Svar panel. `percent` is 0 to 100: 0 when none has answered, else at least 1."""

    line: str
    percent: int
    rows: tuple[Row, ...]


@dataclass(frozen=True)
class Overview:
    """What `home.html` shows: the Svar panel and the six summary panels, in order."""

    progress: Progress
    panels: tuple[Panel, ...]


def persons(count: int) -> str:
    """«1 person», «9 personer»."""
    return f"{count} person" if count == 1 else f"{count} personer"


def households(count: int) -> str:
    """«1 husstand», «5 husstander»."""
    return f"{count} husstand" if count == 1 else f"{count} husstander"


def _progress(facts: Sequence[GuestFacts]) -> Progress:
    """FR-54, FR-74, UX-DR39: «Svart: X av Y husstander», the bar and the three state rows."""
    answered = len(answered_households(facts))
    total = len(all_households(facts))
    rows = []
    for state, label in (
        (COMING, "Kommer"),
        (NOT_COMING, "Kommer ikke"),
        (NOT_ANSWERED, "Ikke svart ennå"),
    ):
        rows.append(
            Row(
                label,
                f"{persons(len(people_by_state(facts, state)))}"
                f" · {households(len(households_by_state(facts, state)))}",
            )
        )
    return Progress(
        line=f"Svart: {answered} av {total} husstander",
        percent=max(1, round(100 * answered / total)) if answered else 0,
        rows=tuple(rows),
    )


def _when(facts: Sequence[GuestFacts]) -> Panel:
    rows = [
        Row("Hele helgen (fre\u2013søn)", persons(len(whole_weekend(facts)))),
        Row("Ikke hele helgen", persons(len(not_whole_weekend(facts)))),
    ]
    rows += [
        Row(label, persons(len(ids)), indent=True)
        for label, ids in (
            *((label, days_only(facts, combo)) for combo, label in DAY_COMBOS),
            ("Andre kombinasjoner", other_days(facts, [combo for combo, _ in DAY_COMBOS])),
        )
        if ids
    ]
    return Panel("Når kommer de?", tuple(rows))


def _overnight(facts: Sequence[GuestFacts]) -> Panel:
    return Panel(
        "Overnatting",
        (
            Row("Overnatter ikke", persons(len(not_staying(facts)))),
            Row("Senger totalt", str(len(beds(facts)))),
        ),
    )


def _meals(facts: Sequence[GuestFacts]) -> Panel:
    return Panel(
        "Mat",
        tuple(
            Row(MEAL_LABELS[meal], persons(len(meal_eaters(facts, meal)))) for meal in MEAL_ORDER
        ),
    )


def _allergies(facts: Sequence[GuestFacts]) -> Panel:
    rows = [
        Row("Har allergier eller matbehov", persons(len(allergy_state_ids(facts, HAS_ALLERGIES))))
    ]
    rows += [
        Row(ALLERGY_LABELS[key], persons(len(allergy_category_ids(facts, key))), indent=True)
        for key in ALLERGY_KEYS
    ]
    rows += [
        Row("Ingen allergier eller matbehov", persons(len(allergy_state_ids(facts, NO_ALLERGIES)))),
        Row(
            "Ingen allergiopplysninger lagret",
            persons(len(allergy_state_ids(facts, NOTHING_STORED))),
        ),
    ]
    return Panel("Allergier (med samtykke)", tuple(rows), note="Én person kan ha flere allergier.")


def _hike(facts: Sequence[GuestFacts]) -> Panel:
    yes, no, maybe = (len(hike_ids(facts, answer)) for answer in HIKE_ANSWERS)
    return Panel(
        "Fjelltur fredag",
        (
            Row("Vil gå turen", f"{yes} ja, {maybe} kanskje"),
            Row("Kommer ikke", persons(no)),
        ),
    )


def _payment(facts: Sequence[GuestFacts], totals: Mapping[int, int]) -> Panel:
    """FR-60, AD-12: status per household from its total; received and refunded are 0 until 5.2."""
    answered = set(answered_households(facts))
    statuses = {
        household_id: payment_status(household_id in answered, total, 0, 0)
        for household_id, total in totals.items()
    }
    return Panel(
        "Betaling (husstander som kommer)",
        tuple(
            Row(label, households(len(households_by_payment(statuses, facts, status))))
            for status, label in PAYMENT_LABELS
        ),
    )


def build_overview(facts: Sequence[GuestFacts], totals: Mapping[int, int]) -> Overview:
    """FR-54, UX-DR39, UX-DR40: the Svar panel and the six summary panels, in the epics order.

    `facts` is `guest_facts()`, `totals` is `household_totals(facts, form_prices())`.
    """
    return Overview(
        progress=_progress(facts),
        panels=(
            _when(facts),
            _overnight(facts),
            _meals(facts),
            _allergies(facts),
            _hike(facts),
            _payment(facts, totals),
        ),
    )
