"""The RSVP form's step registry, days and addresses (Stories 2.1, 2.2; AD-7, UX-DR19).

Each step key from `wedding.rules.form_steps.STEP_KEYS` has its address slug,
its Norwegian name for the progress line «Steg n av m: <name>» and its
question, the step's `h1`. Steps 3 to 6 are frames until Stories 2.3 to 2.5,
so their question is still their name. Step 1
lives at the form's base address, the others at `<base>/<slug>/`, and the
check page at `<base>/se-over/`. A `FormMount` says where the one form is
mounted: for guests at `/<code>/svar/` (built in guests/views.py); the couple's
override mount comes in Story 4.4.

FR-14, FR-70, AD-17 (Story 2.2): `DAYS` names each day key from
`wedding.rules.days.DAY_KEYS` with its weekday, its date and what happens that
day. It is the only place the form holds the dates; a test ties them to the
programme page (guests/templates/guests/programme.html).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    """One step: its key, its address slug, its name in the progress line and its question."""

    key: str
    slug: str
    name: str
    question: str


STEPS = {
    step.key: step
    for step in (
        Step("who", "", "Hvem kommer", "Hvem kommer?"),
        # The days question is a proposal (EXPERIENCE.md, Microcopy).
        Step("days", "dager", "Dager", "Er alle som kommer, med hele helgen?"),
        Step("overnight", "overnatting", "Overnatting", "Overnatting"),
        Step("meals", "maltider", "Måltider", "Måltider"),
        Step("allergies", "allergier", "Allergier og matbehov", "Allergier og matbehov"),
        Step("hike", "fjelltur", "Fjelltur fredag", "Fjelltur fredag"),
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

# AD-7: the check page's slug and its key in the views; it is not a step.
CHECK = "check"
CHECK_SLUG = "se-over"

# Every slug under the base address, to the step key (or CHECK) it opens.
KEY_BY_SLUG = {step.slug: step.key for step in STEPS.values() if step.slug} | {CHECK_SLUG: CHECK}


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
