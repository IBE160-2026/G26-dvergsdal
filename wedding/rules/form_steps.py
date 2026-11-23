"""Which steps the RSVP form has, and where a step sits among them (Stories 2.1, 2.2).

FR-14, UX-DR19, AD-7: the form asks one thing per step, in a fixed order: who
is coming, days, overnight stay, meals, allergies and the Friday hike, then the
check page. The progress line «Steg n av m» counts the steps that apply.
Before step 1 is answered, everyone is assumed to come all weekend, so all six
count; once nobody is coming, only step 1 is left before the check page.

FR-15, FR-16, FR-17, FR-70 (Story 2.2): once days are chosen, overnight stay
counts only if someone can stay overnight, meals only if someone is offered a
paid meal, and the hike only if someone comes on Friday. A day choice that is
not made yet, or not allowed, counts as the whole weekend, so m never shrinks
on a half-made choice. The check page is not a step: `next_step` and
`first_unfinished` return None for it.
"""

from collections.abc import Collection, Sequence

from wedding.rules.days import WHOLE_WEEKEND, can_stay_overnight, day_error, offered_meals

STEP_KEYS = ("who", "days", "overnight", "meals", "allergies", "hike")


def form_steps(
    attendance: Sequence[bool] | None,
    days: Sequence[Collection[str] | None] | None = None,
) -> tuple[str, ...]:
    """FR-14, FR-17, FR-70, UX-DR19: the keys of the steps that apply, in order.

    `attendance` is one bool per household member, or None while step 1 is not
    completed. `days` is aligned with it: one chosen set of day keys or None
    per member, or None while no days are chosen. A coming member counts with
    their set when `day_error` allows it, and as the whole weekend otherwise.
    None, or nobody coming, gives what Story 2.1 gave: all six, or only
    `("who",)` when nobody comes.
    """
    if attendance is not None and not any(attendance):
        return ("who",)
    if attendance is None or days is None:
        return STEP_KEYS
    present = [
        frozenset(chosen) if chosen is not None and day_error(chosen) is None else WHOLE_WEEKEND
        for coming, chosen in zip(attendance, days, strict=True)
        if coming
    ]
    applies = {
        "who": True,
        "days": True,
        "overnight": any(can_stay_overnight(chosen) for chosen in present),
        "meals": any(offered_meals(chosen) for chosen in present),
        "allergies": True,
        "hike": any("fri" in chosen for chosen in present),
    }
    return tuple(key for key in STEP_KEYS if applies[key])


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


def first_unfinished(steps: Sequence[str], done: Collection[str], before: str | None) -> str | None:
    """AD-7, UX-DR19: the first applicable step before `before` that is not done.

    `before` is a step key, or None for the check page. None means every
    applicable step before it is done, so the guest may open it.
    """
    limit = len(STEP_KEYS) if before is None else STEP_KEYS.index(before)
    return next(
        (step for step in steps if STEP_KEYS.index(step) < limit and step not in done), None
    )
