"""Households: how many people one may have, and how the invitation names it.

FR-49, AD-8: a household has at least one person and at most 8. The upper limit
keeps a full RSVP draft inside the 4 KB cookie (AD-8); Rikke confirmed that no
household on the guest list is larger.

FR-7, AD-4, UX-DR51 (Story 1.5): no household name is stored. «for Sigmund og
bestemor» is derived from the guests' names, and the invitation says «deg» to
one invited person and «dere» to more; the words themselves live in the
templates.

FR-71, AD-4 (Story 2.7): the payment message «Bryllup Sigmund og bestemor» is
derived from the same names and never stored.

FR-74 (Story 2.6a): a person's and a household's answer state, from the
stored facts. The states are derived, never stored (AD-4).
"""

from collections.abc import Iterable, Sequence

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


def payment_message(names: Sequence[str]) -> str:
    """FR-71, AD-2, AD-4: the message the household writes with its payment.

    «Bryllup » and the household as `household_names` names it, for example
    «Bryllup Sigmund og bestemor». Derived each time, never stored.
    """
    return f"Bryllup {household_names(names)}"


def speaks_to_one(household_size: int) -> bool:
    """UX-DR51: True when the invitation says «deg» (one invited person), False for «dere»."""
    return household_size == 1


# FR-74: the three answer states of a person or a household.
COMING = "coming"
NOT_COMING = "not_coming"
NOT_ANSWERED = "not_answered"


def person_state(coming: bool | None) -> str:
    """FR-74, AD-2: a person's state from their «Kommer» (None: no answer sent)."""
    if coming is None:
        return NOT_ANSWERED
    return COMING if coming else NOT_COMING


def household_state(answered: bool, coming: Iterable[bool]) -> str:
    """FR-74, AD-2: a household's state: not answered until it has sent an answer,
    then coming when anyone in it is coming, else not coming."""
    if not answered:
        return NOT_ANSWERED
    return COMING if any(coming) else NOT_COMING
