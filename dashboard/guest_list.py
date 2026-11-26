"""The view models of the Gjester page and the allergy list (Story 3.4; FR-57, FR-58, AD-18).

FR-57, UX-DR42: `build_guest_list` turns the guests' facts into «N husstander · M gjester» and one
row per household, households that have not answered first. FR-58, UX-DR48, AD-18:
`build_allergy_list` names the guests of `wedding.rules.summary.allergy_list`, the one consent-
checked rule. Nothing is counted or filtered in a template: the headings and every line are
written here.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from dashboard.counts import ALLERGY_NAMES, households, persons
from dashboard.selectors import GuestNames
from wedding.rules.households import household_names
from wedding.rules.summary import GuestFacts, all_households, allergy_list
from wedding.templatetags.money import kroner

NOT_ANSWERED_LINE = "Har ikke svart ennå"
NOT_COMING_LINE = "Kommer ikke"


@dataclass(frozen=True)
class HouseholdListRow:
    """FR-57, UX-DR42: one household on Gjester. `answered` False shows the tag «Ikke svart»."""

    household_id: int
    names: str
    answered: bool
    line: str


@dataclass(frozen=True)
class GuestList:
    """FR-57, UX-DR42: what `guests.html` shows: the count line and the rows, in order."""

    summary: str
    rows: tuple[HouseholdListRow, ...]


@dataclass(frozen=True)
class AllergyRow:
    """FR-58, UX-DR48: one guest on the allergy list: name, category labels and note."""

    name: str
    categories: tuple[str, ...]
    note: str


@dataclass(frozen=True)
class AllergyList:
    """FR-58, UX-DR48: what `allergies.html` shows: the count line and the rows."""

    summary: str
    rows: tuple[AllergyRow, ...]


def _gjester(count: int) -> str:
    return f"{count} gjest" if count == 1 else f"{count} gjester"


def _line(guests: Sequence[GuestFacts], names: GuestNames, total: int) -> str:
    """FR-57: «Kommer: Sigmund og bestemor · Totalt 4 720 kr», «Kommer ikke» or the unanswered
    line. No payment word before Epic 5."""
    if not guests[0].answered:
        return NOT_ANSWERED_LINE
    coming = [names.guests[guest.guest_id] for guest in guests if guest.coming]
    if not coming:
        return NOT_COMING_LINE
    return f"Kommer: {household_names(coming)} · Totalt {kroner(total)}"


def build_guest_list(
    facts: Sequence[GuestFacts], names: GuestNames, totals: Mapping[int, int]
) -> GuestList:
    """FR-57, UX-DR42: the Gjester page. Households that have not answered come first, then the
    rest, each group by household name (`str.casefold`, then id). `totals` is
    `household_totals(facts, form_prices())`."""
    members: dict[int, list[GuestFacts]] = {}
    for guest in facts:
        members.setdefault(guest.household_id, []).append(guest)
    rows = [
        HouseholdListRow(
            household_id,
            names.households[household_id],
            members[household_id][0].answered,
            _line(members[household_id], names, totals[household_id]),
        )
        for household_id in all_households(facts)
    ]
    rows.sort(key=lambda row: (row.answered, row.names.casefold(), row.household_id))
    return GuestList(f"{households(len(rows))} · {_gjester(len(facts))}", tuple(rows))


def build_allergy_list(facts: Sequence[GuestFacts], names: GuestNames) -> AllergyList:
    """FR-58, UX-DR48, AD-18: the allergy list, in guest id order, with the labels of
    `ALLERGY_NAMES`; exactly the entries of the `allergy_list` rule."""
    entries = allergy_list(facts)
    rows = tuple(
        AllergyRow(
            names.guests[entry.guest_id],
            tuple(ALLERGY_NAMES[key][1] for key in entry.categories),
            entry.note,
        )
        for entry in entries
    )
    return AllergyList(persons(len(rows)), rows)
