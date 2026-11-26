"""The registry of every count on Oversikt (Story 3.3; FR-54, FR-55, UX-DR41, AD-2).

Each count is named once: its slug (the address `/admin/tall/<slug>/`), its page
title, whether it counts people or households, and the `wedding.rules.summary`
call that returns its id tuple. Oversikt's number and the list on the count page
both read that tuple, so they cannot disagree: a count is `len()` of it, and the
list shows exactly its ids. Adding a count is one entry here.
"""

from collections.abc import Callable, Mapping, Sequence
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

PEOPLE = "people"
HOUSEHOLDS = "households"

# FR-54: the day combinations that «Ikke hele helgen» is broken down by: (slug, days, label).
DAY_COMBOS = (
    ("bare-lordag-sondag", ("sat", "sun"), "Bare lørdag\u2013søndag"),
    ("bare-lordag", ("sat",), "Bare lørdag"),
    ("bare-fredag-lordag", ("fri", "sat"), "Bare fredag\u2013lørdag"),
    ("bare-fredag", ("fri",), "Bare fredag"),
    ("bare-sondag", ("sun",), "Bare søndag"),
)
# FR-54: the meals in the order of the weekend (Saturday lunch and dinner sit between the
# breakfasts): (meal key, slug, label).
MEALS = (
    ("friday_dinner", "maltid-fredag-middag", "Middag fredag"),
    ("saturday_breakfast", "maltid-lordag-frokost", "Frokost lørdag"),
    (SATURDAY_LUNCH, "maltid-lordag-lunsj", "Lunsj lørdag"),
    (SATURDAY_DINNER, "maltid-lordag-middag", "Middag lørdag"),
    ("sunday_breakfast", "maltid-sondag-frokost", "Frokost søndag"),
)
# FR-54: allergy category key -> (slug, label).
ALLERGY_NAMES = {
    "gluten": ("allergi-gluten", "Gluten"),
    "lactose": ("allergi-laktose", "Laktose"),
    "nuts": ("allergi-notter", "Nøtter"),
    "shellfish": ("allergi-skalldyr", "Skalldyr"),
    "vegetarian": ("allergi-vegetar", "Vegetar"),
    "vegan": ("allergi-vegan", "Vegan"),
    "other": ("allergi-annet", "Annet"),
}
HIKE_NAMES = {
    "yes": ("tur-ja", "Fjelltur: vil gå"),
    "maybe": ("tur-kanskje", "Fjelltur: kanskje"),
    "no": ("tur-nei", "Fjelltur: kommer ikke"),
}
# FR-60: payment status -> (slug, label).
PAYMENTS = (
    (NOTHING_TO_PAY, "betaling-ingenting", "Ingenting å betale"),
    (NOT_PAID, "betaling-ikke-betalt", "Ikke betalt"),
    (PART_PAID, "betaling-delbetalt", "Delbetalt"),
    (PAID, "betaling-betalt", "Betalt"),
    (REFUND_OWED, "betaling-tilbake", "Skal ha penger tilbake"),
)

Ids = Callable[[Sequence[GuestFacts], Mapping[int, str]], tuple[int, ...]]


@dataclass(frozen=True)
class Count:
    """One count: its address slug, the page heading, what it counts and its rule call.

    `ids(facts, statuses)` returns the sorted ids (guest ids for `PEOPLE`, household ids for
    `HOUSEHOLDS`); `statuses` is `payment_statuses(...)`, which only the payment counts read.
    """

    slug: str
    title: str
    kind: str
    ids: Ids


def persons(count: int) -> str:
    """«1 person», «9 personer»."""
    return f"{count} person" if count == 1 else f"{count} personer"


def households(count: int) -> str:
    """«1 husstand», «5 husstander»."""
    return f"{count} husstand" if count == 1 else f"{count} husstander"


def count_text(kind: str, count: int) -> str:
    """The count as Oversikt and the count page's heading write it, by what it counts."""
    return persons(count) if kind == PEOPLE else households(count)


def payment_statuses(facts: Sequence[GuestFacts], totals: Mapping[int, int]) -> dict[int, str]:
    """FR-60, AD-12: each household's payment status from its total; received and refunded
    are 0 until Story 5.2. Oversikt and the count pages share this one helper."""
    answered = set(answered_households(facts))
    return {
        household_id: payment_status(household_id in answered, total, 0, 0)
        for household_id, total in totals.items()
    }


def _people(slug: str, title: str, rule: Callable[[Sequence[GuestFacts]], tuple[int, ...]]):
    return Count(slug, title, PEOPLE, lambda facts, statuses: rule(facts))


def _build() -> tuple[Count, ...]:
    counts = []
    for state, slug, title in (
        (COMING, "kommer", "Kommer"),
        (NOT_COMING, "kommer-ikke", "Kommer ikke"),
        (NOT_ANSWERED, "ikke-svart", "Ikke svart ennå"),
    ):
        counts.append(
            _people(
                f"{slug}-personer", title, lambda facts, state=state: people_by_state(facts, state)
            )
        )
        counts.append(
            Count(
                f"{slug}-husstander",
                title,
                HOUSEHOLDS,
                lambda facts, statuses, state=state: households_by_state(facts, state),
            )
        )
    counts.append(_people("hele-helgen", "Hele helgen (fre\u2013søn)", whole_weekend))
    counts.append(_people("ikke-hele-helgen", "Ikke hele helgen", not_whole_weekend))
    for slug, combo, label in DAY_COMBOS:
        counts.append(_people(slug, label, lambda facts, combo=combo: days_only(facts, combo)))
    counts.append(
        _people(
            "andre-kombinasjoner",
            "Andre kombinasjoner",
            lambda facts: other_days(facts, [combo for _, combo, _ in DAY_COMBOS]),
        )
    )
    counts.append(_people("overnatter-ikke", "Overnatter ikke", not_staying))
    counts.append(_people("senger", "Senger totalt", beds))
    for meal, slug, label in MEALS:
        counts.append(_people(slug, label, lambda facts, meal=meal: meal_eaters(facts, meal)))
    counts.append(
        _people(
            "allergi-har",
            "Har allergier eller matbehov",
            lambda facts: allergy_state_ids(facts, HAS_ALLERGIES),
        )
    )
    for key in ALLERGY_KEYS:
        slug, label = ALLERGY_NAMES[key]
        counts.append(
            _people(
                slug, f"Allergi: {label}", lambda facts, key=key: allergy_category_ids(facts, key)
            )
        )
    counts.append(
        _people(
            "allergi-ingen",
            "Ingen allergier eller matbehov",
            lambda facts: allergy_state_ids(facts, NO_ALLERGIES),
        )
    )
    counts.append(
        _people(
            "allergi-ingen-lagret",
            "Ingen allergiopplysninger lagret",
            lambda facts: allergy_state_ids(facts, NOTHING_STORED),
        )
    )
    for answer in HIKE_ANSWERS:
        slug, title = HIKE_NAMES[answer]
        counts.append(_people(slug, title, lambda facts, answer=answer: hike_ids(facts, answer)))
    for status, slug, label in PAYMENTS:
        counts.append(
            Count(
                slug,
                f"Betaling: {label}",
                HOUSEHOLDS,
                lambda facts, statuses, status=status: households_by_payment(
                    statuses, facts, status
                ),
            )
        )
    return tuple(counts)


COUNTS = _build()
_BY_SLUG = {count.slug: count for count in COUNTS}


def count_for(slug: str) -> Count:
    """FR-55: the count with this slug; a `KeyError` when the registry has none."""
    return _BY_SLUG[slug]
