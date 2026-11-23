"""Which steps the RSVP form has, and where a step sits among them (Story 2.1).

FR-14, UX-DR19, AD-7: the form asks one thing per step, in a fixed order: who
is coming, days, overnight stay, meals, allergies and the Friday hike, then the
check page. The progress line «Steg n av m» counts the steps that apply.
Before step 1 is answered, everyone is assumed to come all weekend, so all six
count; once nobody is coming, only step 1 is left before the check page. Days
are unknown until Story 2.2, which extends `form_steps` with them (the hike
only for people present on Friday). The check page is not a step: `next_step`
returns None for it.
"""

from collections.abc import Sequence

STEP_KEYS = ("who", "days", "overnight", "meals", "allergies", "hike")


def form_steps(attendance: Sequence[bool] | None) -> tuple[str, ...]:
    """FR-14, UX-DR19: the keys of the steps that apply, in order.

    `attendance` is one bool per household member, or None while step 1 is not
    completed. None, or anyone coming, gives all six (the whole weekend is
    assumed until Story 2.2 asks for days); nobody coming gives only `("who",)`.
    """
    if attendance is None or any(attendance):
        return STEP_KEYS
    return ("who",)


def step_position(steps: Sequence[str], key: str) -> tuple[int, int]:
    """UX-DR19: (n, m) for «Steg n av m»; `key` must be one of `steps`."""
    return steps.index(key) + 1, len(steps)


def next_step(steps: Sequence[str], key: str) -> str | None:
    """AD-7: the first applicable step after `key`, or None for the check page.

    `key` may be a step that does not apply (a frame opened by its address);
    the answer is then the next applicable one after it in `STEP_KEYS` order.
    """
    position = STEP_KEYS.index(key)
    return next((step for step in steps if STEP_KEYS.index(step) > position), None)


def previous_step(steps: Sequence[str], key: str) -> str | None:
    """AD-7, UX-DR18: the last applicable step before `key`, or None before step 1."""
    position = STEP_KEYS.index(key)
    earlier = [step for step in steps if STEP_KEYS.index(step) < position]
    return earlier[-1] if earlier else None
