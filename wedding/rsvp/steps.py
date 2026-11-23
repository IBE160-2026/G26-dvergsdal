"""The RSVP form's step registry, days, meals, allergies, hike and addresses (Stories 2.1 to 2.5).

AD-7, UX-DR19.

Each step key from `wedding.rules.form_steps.STEP_KEYS` has its address slug,
its Norwegian name for the progress line «Steg n av m: <name>», its
question, the step's `h1`, and the template with its fields, which step.html
includes. Step 1 lives at the form's base address, the others at `<base>/<slug>/`, and the
check page at `<base>/se-over/`. A `FormMount` says where the one form is
mounted: for guests at `/<code>/svar/` (built in guests/views.py); the couple's
override mount comes in Story 4.4. The running total on the paid steps is
posted to `<base>/sum/?steg=<slug>` (AD-7, Story 2.3).

FR-14, FR-70, AD-17 (Story 2.2): `DAYS` names each day key from
`wedding.rules.days.DAY_KEYS` with its weekday, its date and what happens that
day. It is the only place the form holds the dates; a test ties them to the
programme page (guests/templates/guests/programme.html).

FR-15, FR-73 (Story 2.3): `MEALS` names each paid meal key from
`wedding.rules.days.MEAL_KEYS`, as the meal checkboxes on step 4 show it.

FR-25 (Story 2.4): `ALLERGIES` names each category key from
`wedding.rules.allergies.ALLERGY_KEYS`, as the checkboxes on step 5 show it.

FR-17 (Story 2.5): `HIKE` names each answer key from
`wedding.rules.days.HIKE_ANSWERS`, as the radios on step 6 show it.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    """One step: its key, address slug, name in the progress line, question and fields.

    `fields_template` is the include with the step's fields.
    """

    key: str
    slug: str
    name: str
    question: str
    fields_template: str


STEPS = {
    step.key: step
    for step in (
        Step("who", "", "Hvem kommer", "Hvem kommer?", "rsvp/includes/who_fields.html"),
        # The questions of steps 2 to 4 are avgjort av Claude 2026-11-23
        # (EXPERIENCE.md, Microcopy); «Hvem …?» and «Hvilke …?» need no du/dere.
        Step(
            "days",
            "dager",
            "Dager",
            "Er alle som kommer, med hele helgen?",
            "rsvp/includes/days_fields.html",
        ),
        Step(
            "overnight",
            "overnatting",
            "Overnatting",
            "Hvem skal overnatte på Hardingasete?",
            "rsvp/includes/overnight_fields.html",
        ),
        Step(
            "meals",
            "maltider",
            "Måltider",
            "Hvilke måltider skal vi bestille?",
            "rsvp/includes/meals_fields.html",
        ),
        Step(
            "allergies",
            "allergier",
            "Allergier og matbehov",
            "Allergier og matbehov",
            "rsvp/includes/allergy_fields.html",
        ),
        Step(
            "hike",
            "fjelltur",
            "Fjelltur fredag",
            "Hvem blir med på fjellturen fredag?",
            "rsvp/includes/hike_fields.html",
        ),
    )
}


@dataclass(frozen=True)
class Day:
    """FR-14, FR-70: one day of the weekend: its key, weekday, date and what happens."""

    key: str
    name: str
    date: str
    summary: str

    @property
    def label(self) -> str:
        """FR-14: «Fredag 26. mai», the day's checkbox label and its line in the list."""
        return f"{self.name} {self.date}"


# The summaries are proposals (EXPERIENCE.md, Microcopy).
DAYS = {
    day.key: day
    for day in (
        Day("fri", "Fredag", "26. mai", "Fjelltur, middag og rebus"),
        Day("sat", "Lørdag", "27. mai", "Bryllupsdagen: vielse, lunsj og fest"),
        Day("sun", "Søndag", "28. mai", "Frokost og hjemreise"),
    )
}


@dataclass(frozen=True)
class Meal:
    """FR-15, FR-73: one paid meal: its key and its name on step 4."""

    key: str
    name: str


MEALS = {
    meal.key: meal
    for meal in (
        Meal("friday_dinner", "Middag fredag"),
        Meal("saturday_breakfast", "Frokost lørdag"),
        Meal("sunday_breakfast", "Frokost søndag"),
    )
}

# FR-25: the allergy categories' labels on step 5, in `ALLERGY_KEYS` order.
ALLERGIES = {
    "gluten": "Gluten",
    "lactose": "Laktose",
    "nuts": "Nøtter",
    "shellfish": "Skalldyr",
    "vegetarian": "Vegetar",
    "vegan": "Veganer",
    "other": "Annet",
}

# FR-17: the hike answers' labels on step 6, in `HIKE_ANSWERS` order.
HIKE = {"yes": "Ja", "no": "Nei", "maybe": "Kanskje"}

# AD-7: the check page's slug and its key in the views; it is not a step.
CHECK = "check"
CHECK_SLUG = "se-over"

# Every slug under the base address, to the step key (or CHECK) it opens.
KEY_BY_SLUG = {step.slug: step.key for step in STEPS.values() if step.slug} | {CHECK_SLUG: CHECK}

# AD-7, Story 2.3: the running total's address under the base address.
TOTAL_SLUG = "sum"


@dataclass(frozen=True)
class FormMount:
    """AD-7, AD-8: where the form is mounted.

    `base_path` is step 1's address, `cookie_path` the path the draft cookie is
    scoped to, and `exit_url` where «Tilbake» on step 1 goes.
    """

    base_path: str
    cookie_path: str
    exit_url: str

    def url(self, key: str | None) -> str:
        """AD-7: the address of step `key`; None or CHECK give the check page."""
        if key is None or key == CHECK:
            return f"{self.base_path}{CHECK_SLUG}/"
        slug = STEPS[key].slug
        return f"{self.base_path}{slug}/" if slug else self.base_path

    def sent_url(self) -> str:
        """AD-7, FR-74 (Story 2.6a): where the guest lands after «Send svaret»."""
        return f"{self.base_path}sendt/"

    def total_url(self, key: str) -> str:
        """AD-7, FR-33: where step `key` posts its choices for the running total."""
        return f"{self.base_path}{TOTAL_SLUG}/?steg={STEPS[key].slug}"
