"""An answer made consistent with itself before it is kept (Story 2.2).

FR-75: when a person stops coming, or a day is removed, the choices that
depended on it are removed and never count. `normalise_answer` runs on every
draft write (AD-8), so the draft never holds days for someone who is not
coming. Story 2.3 extends it with overnight stay and meals, which then depend
on the days kept here.
"""

from collections.abc import Iterable, Mapping

from wedding.rules.days import DAY_KEYS


def normalise_answer(
    attendance: Mapping[int, bool],
    whole: bool | None,
    days: Mapping[int, Iterable[str]],
) -> tuple[bool | None, dict[int, list[str]]]:
    """FR-75: (whole, days) with everything that no longer applies removed.

    `attendance` is each member's «Kommer» by guest id, `whole` the answer to
    «Er alle som kommer, med hele helgen?» (None while unanswered) and `days`
    each member's chosen day keys. Nobody coming gives `whole` None. Days are
    kept only when `whole` is False, only for members who are coming, in
    `DAY_KEYS` order, with unknown keys dropped; a member left with no day is
    left out (the form shows that as «no day chosen»). Otherwise `days` is `{}`.
    """
    if not any(attendance.values()):
        return None, {}
    if whole is not False:
        return whole, {}
    kept = {}
    for guest_id, chosen in days.items():
        if attendance.get(guest_id):
            chosen_set = set(chosen)
            if ordered := [day for day in DAY_KEYS if day in chosen_set]:
                kept[guest_id] = ordered
    return False, kept
