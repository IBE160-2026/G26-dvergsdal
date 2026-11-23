"""The RSVP form's step registry and addresses (Story 2.1, AD-7, UX-DR19).

Each step key from `wedding.rules.form_steps.STEP_KEYS` has its address slug
and its Norwegian name for the progress line «Steg n av m: <name>». Step 1
lives at the form's base address, the others at `<base>/<slug>/`, and the
check page at `<base>/se-over/`. A `FormMount` says where the one form is
mounted: for guests at `/<code>/svar/` (built in guests/views.py); the couple's
override mount comes in Story 4.4.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    """One step: its key, its address slug and its name in the progress line."""

    key: str
    slug: str
    name: str


STEPS = {
    step.key: step
    for step in (
        Step("who", "", "Hvem kommer"),
        Step("days", "dager", "Dager"),
        Step("overnight", "overnatting", "Overnatting"),
        Step("meals", "maltider", "Måltider"),
        Step("allergies", "allergier", "Allergier og matbehov"),
        Step("hike", "fjelltur", "Fjelltur fredag"),
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
