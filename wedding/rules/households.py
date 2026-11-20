"""Households: how many people one may have, and how the invitation names it.

FR-49, AD-8: a household has at least one person and at most 8. The upper limit
keeps a full RSVP draft inside the 4 KB cookie (AD-8); Rikke confirmed that no
household on the guest list is larger.

FR-7, AD-4, UX-DR51 (Story 1.5): no household name is stored. «for Sigmund og
bestemor» is derived from the guests' names, and the invitation says «deg» to
one invited person and «dere» to more; the words themselves live in the
templates.
"""

from collections.abc import Sequence

MIN_HOUSEHOLD_SIZE = 1
MAX_HOUSEHOLD_SIZE = 8


def household_size_problem(count: int) -> str | None:
    """FR-49, AD-8: a Norwegian message when `count` people is not a valid household, else None."""
    if count < MIN_HOUSEHOLD_SIZE:
        return "En husstand må ha minst én person."
    if count > MAX_HOUSEHOLD_SIZE:
        return f"En husstand kan ha høyst {MAX_HOUSEHOLD_SIZE} personer."
    return None


def household_names(names: Sequence[str]) -> str:
    """FR-7, AD-4: the household as the hero's «for …» line names it, in the order given.

    «Synne», «Sigmund og bestemor», «Arild, Marie, Filippa og Leone»; `""` for
    no names.
    """
    if len(names) < 2:
        return "".join(names)
    return f"{', '.join(names[:-1])} og {names[-1]}"


def speaks_to_one(household_size: int) -> bool:
    """UX-DR51: True when the invitation says «deg» (one invited person), False for «dere»."""
    return household_size == 1
