"""Oversikt's view model: the Svar panel and the six summary panels (Story 3.2, 3.3).

FR-54, FR-55, FR-73, FR-74, UX-DR39, UX-DR40, UX-DR41, AD-2: `build_overview` turns
the registry of `dashboard.counts` into Norwegian labels and cells. A cell carries
the count's text, its slug and its number, and the number is `len()` of the id tuple
the registry's rule call returned; nothing here filters or adds, and the template
shows a count above 0 as a link to its page and a 0 as plain text. «Stemmer ikke»
is an attention item (FR-61), not a count here.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from dashboard.counts import (
    ALLERGY_NAMES,
    DAY_COMBOS,
    HIKE_NAMES,
    MEALS,
    PAYMENTS,
    count_for,
    count_text,
    payment_statuses,
)
from wedding.rules.allergies import ALLERGY_KEYS
from wedding.rules.summary import GuestFacts, all_households, answered_households


@dataclass(frozen=True)
class Cell:
    """One number in a row: its text, the slug of its count page and the number itself."""

    text: str
    slug: str
    count: int


@dataclass(frozen=True)
class Row:
    """One label with its cells, as a `dl` pair. Two cells are joined by `separator`."""

    label: str
    cells: tuple[Cell, ...]
    indent: bool = False
    separator: str = " · "

    @property
    def text(self) -> str:
        """The row's numbers as a reader sees them, for example «9 personer · 5 husstander»."""
        return self.separator.join(cell.text for cell in self.cells)


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


class _Counter:
    """FR-55, AD-2: reads each count from the registry, once, against one set of facts."""

    def __init__(self, facts: Sequence[GuestFacts], statuses: Mapping[int, str]):
        self._facts = facts
        self._statuses = statuses

    def number(self, slug: str) -> int:
        return len(count_for(slug).ids(self._facts, self._statuses))

    def cell(self, slug: str, text: str | None = None) -> Cell:
        """The cell of `slug`; `text` is how it is written, by default «9 personer»."""
        count = self.number(slug)
        return Cell(text or count_text(count_for(slug).kind, count), slug, count)

    def row(self, label: str, *slugs: str, indent: bool = False) -> Row:
        return Row(label, tuple(self.cell(slug) for slug in slugs), indent)


def _progress(facts: Sequence[GuestFacts], counter: _Counter) -> Progress:
    """FR-54, FR-74, UX-DR39: «Svart: X av Y husstander», the bar and the three state rows."""
    answered = len(answered_households(facts))
    total = len(all_households(facts))
    return Progress(
        line=f"Svart: {answered} av {total} husstander",
        percent=max(1, round(100 * answered / total)) if answered else 0,
        rows=(
            counter.row("Kommer", "kommer-personer", "kommer-husstander"),
            counter.row("Kommer ikke", "kommer-ikke-personer", "kommer-ikke-husstander"),
            counter.row("Ikke svart ennå", "ikke-svart-personer", "ikke-svart-husstander"),
        ),
    )


def _when(counter: _Counter) -> Panel:
    rows = [
        counter.row("Hele helgen (fre\u2013søn)", "hele-helgen"),
        counter.row("Ikke hele helgen", "ikke-hele-helgen"),
    ]
    rows += [
        counter.row(label, slug, indent=True)
        for slug, label in (
            *((slug, label) for slug, _, label in DAY_COMBOS),
            ("andre-kombinasjoner", "Andre kombinasjoner"),
        )
        if counter.number(slug)
    ]
    return Panel("Når kommer de?", tuple(rows))


def _overnight(counter: _Counter) -> Panel:
    senger = counter.number("senger")
    return Panel(
        "Overnatting",
        (
            counter.row("Overnatter ikke", "overnatter-ikke"),
            Row("Senger totalt", (Cell(str(senger), "senger", senger),)),
        ),
    )


def _meals(counter: _Counter) -> Panel:
    return Panel("Mat", tuple(counter.row(label, slug) for _, slug, label in MEALS))


def _allergies(counter: _Counter) -> Panel:
    rows = [counter.row("Har allergier eller matbehov", "allergi-har")]
    rows += [
        counter.row(ALLERGY_NAMES[key][1], ALLERGY_NAMES[key][0], indent=True)
        for key in ALLERGY_KEYS
    ]
    rows += [
        counter.row("Ingen allergier eller matbehov", "allergi-ingen"),
        counter.row("Ingen allergiopplysninger lagret", "allergi-ingen-lagret"),
    ]
    return Panel("Allergier (med samtykke)", tuple(rows), note="Én person kan ha flere allergier.")


def _hike(counter: _Counter) -> Panel:
    """FR-17: «ja» and «kanskje» are two counts in one row, never added."""
    yes, maybe = (HIKE_NAMES[answer][0] for answer in ("yes", "maybe"))
    yes_count, maybe_count = counter.number(yes), counter.number(maybe)
    return Panel(
        "Fjelltur fredag",
        (
            Row(
                "Vil gå turen",
                (
                    Cell(f"{yes_count} ja", yes, yes_count),
                    Cell(f"{maybe_count} kanskje", maybe, maybe_count),
                ),
                separator=", ",
            ),
            counter.row("Kommer ikke", HIKE_NAMES["no"][0]),
        ),
    )


def _payment(counter: _Counter) -> Panel:
    """FR-60, AD-12: status per household from its total; received and refunded are 0 until 5.2."""
    return Panel(
        "Betaling (husstander som kommer)",
        tuple(counter.row(label, slug) for _, slug, label in PAYMENTS),
    )


def build_overview(facts: Sequence[GuestFacts], totals: Mapping[int, int]) -> Overview:
    """FR-54, FR-55, UX-DR39, UX-DR40: the Svar panel and the six summary panels, in order.

    `facts` is `guest_facts()`, `totals` is `household_totals(facts, form_prices())`.
    """
    counter = _Counter(facts, payment_statuses(facts, totals))
    return Overview(
        progress=_progress(facts, counter),
        panels=(
            _when(counter),
            _overnight(counter),
            _meals(counter),
            _allergies(counter),
            _hike(counter),
            _payment(counter),
        ),
    )
