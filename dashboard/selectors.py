"""What the couple's summary loads (Story 3.2; FR-54, NFR-2, AD-2, AD-12, AD-18).

`guest_facts` reads every guest with their sent answer, allergy and latest
consent into plain `GuestFacts` for `wedding.rules.summary`, and never filters on
answer content, so a guest who has not answered still counts as «ikke svart».
`household_totals` gives each household's total from `household_total` and the
current prices; nothing is added up here or stored. `people_behind` and
`households_behind` (Story 3.3; FR-55) name the people of a count, names only.
"""

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

from wedding.models import Allergy, Consent, Guest, HouseholdAnswer, PersonAnswer
from wedding.rules.allergies import ALLERGY_KEYS, AllergyEntry
from wedding.rules.answer import Answer
from wedding.rules.days import DAY_KEYS, MEAL_KEYS
from wedding.rules.households import household_names
from wedding.rules.money import household_total
from wedding.rules.summary import GuestFacts

# The `PersonAnswer` field for each day key, as `send_answer` writes them.
_DAY_FIELDS = {"fri": "friday", "sat": "saturday", "sun": "sunday"}


def _latest_consent() -> dict[int, bool]:
    """AD-18: each guest's latest consent: given True, refused False, withdrawn or none: absent."""
    consent: dict[int, bool] = {}
    for guest_id, event in Consent.objects.order_by("at", "pk").values_list("guest_id", "event"):
        if event == Consent.WITHDRAWN:
            consent.pop(guest_id, None)
        else:
            consent[guest_id] = event == Consent.GIVEN
    return consent


def guest_facts() -> tuple[GuestFacts, ...]:
    """FR-54, FR-74, NFR-2: every guest's facts, by guest id, in five queries.

    One SELECT each for the guests, the sent `PersonAnswer` rows, the
    `Allergy` rows, the `Consent` events and the households that have sent an
    answer. A guest with no `PersonAnswer` has `coming` None.
    """
    answered = set(HouseholdAnswer.objects.values_list("household_id", flat=True))
    answers = {row.guest_id: row for row in PersonAnswer.objects.all()}
    allergies = {
        allergy.guest_id: AllergyEntry(
            cats=tuple(key for key in ALLERGY_KEYS if getattr(allergy, key)),
            none=allergy.none,
            note=allergy.note,
        )
        for allergy in Allergy.objects.all()
    }
    consent = _latest_consent()
    facts = []
    for guest_id, household_id in Guest.objects.order_by("id").values_list("id", "household_id"):
        row = answers.get(guest_id)
        facts.append(
            GuestFacts(
                guest_id=guest_id,
                household_id=household_id,
                answered=household_id in answered,
                coming=row.coming if row else None,
                days=(
                    frozenset(key for key in DAY_KEYS if getattr(row, _DAY_FIELDS[key]))
                    if row
                    else frozenset()
                ),
                cabin=bool(row and row.cabin),
                meals=frozenset(meal for meal in MEAL_KEYS if row and getattr(row, meal)),
                hike=row.hike if row else "",
                allergy=allergies.get(guest_id),
                consent=consent.get(guest_id),
            )
        )
    return tuple(facts)


def household_totals(facts: Sequence[GuestFacts], prices: Mapping[str, int]) -> dict[int, int]:
    """FR-33, AD-12, NFR-2: each household's total in whole kroner from `household_total`.

    A household that has not answered owes 0. `prices` is `form_prices()`.
    """
    members: dict[int, list[GuestFacts]] = {}
    for guest in facts:
        members.setdefault(guest.household_id, []).append(guest)
    totals = {}
    for household_id, guests in members.items():
        if not guests[0].answered:
            totals[household_id] = 0
            continue
        coming = [guest for guest in guests if guest.coming]
        answer = Answer(
            attendance={
                guest.guest_id: guest.coming for guest in guests if guest.coming is not None
            },
            whole=False,
            days={guest.guest_id: sorted(guest.days) for guest in coming},
            night={guest.guest_id: guest.cabin for guest in coming},
            meals={guest.guest_id: sorted(guest.meals) for guest in coming},
        )
        totals[household_id] = household_total(answer, prices)
    return totals


@dataclass(frozen=True)
class Person:
    """FR-55: one guest on a count page: their name and the household as the invitation names it."""

    name: str
    household: str


@dataclass(frozen=True)
class HouseholdRow:
    """FR-55: one household on a count page, named by its guests."""

    names: str


def _household_names(household_ids: Iterable[int]) -> dict[int, str]:
    """AD-4: each household's guests' names, as `household_names` writes them, in one query."""
    members: dict[int, list[str]] = {}
    for household_id, name in Guest.objects.filter(household_id__in=household_ids).values_list(
        "household_id", "name"
    ):
        members.setdefault(household_id, []).append(name)
    return {household_id: household_names(names) for household_id, names in members.items()}


def people_behind(ids: Sequence[int]) -> tuple[Person, ...]:
    """FR-55, NFR-2: the guests of a count, in the order of `ids`, names only (never allergies,
    which wait for Story 3.4); two queries however many guests."""
    if not ids:
        return ()
    guests = {
        guest_id: (name, household_id)
        for guest_id, name, household_id in Guest.objects.filter(id__in=ids).values_list(
            "id", "name", "household_id"
        )
    }
    households = _household_names({household_id for _, household_id in guests.values()})
    return tuple(Person(guests[id_][0], households[guests[id_][1]]) for id_ in ids)


def households_behind(ids: Sequence[int]) -> tuple[HouseholdRow, ...]:
    """FR-55, NFR-2: the households of a count, in the order of `ids`, each named by its guests
    (names only); one query."""
    if not ids:
        return ()
    names = _household_names(ids)
    return tuple(HouseholdRow(names[id_]) for id_ in ids)
