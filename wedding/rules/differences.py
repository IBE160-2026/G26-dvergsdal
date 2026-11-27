"""What differs between a draft and the stored answer (Story 4.2; FR-38, AD-9, AD-2).

`answer_differences` is the rule behind the conflict notice: after a send was
refused because the household's answer changed, the guest sees which choices
of the draft differ from the stored answer. Pure: two `Answer`s in, a list of
`Difference` out. Confirmations and consent never count: a stale draft has no
consent «Ja» by design (AD-18), and the notice says so.
"""

from dataclasses import dataclass

from wedding.rules.allergies import EMPTY
from wedding.rules.answer import Answer, normalise_answer, present_days
from wedding.rules.changes import allergy_key

ATTENDANCE = "attendance"
DAYS = "days"
CABIN = "cabin"
MEALS = "meals"
HIKE = "hike"
ALLERGIES = "allergies"


@dataclass(frozen=True)
class Difference:
    """FR-38: one topic where the draft (`mine`) and the stored answer (`sent`) differ for a guest.

    `attendance`: True, False or None (no answer for that guest on that side);
    `days` and `meals`: a frozenset of keys; `cabin`: a bool; `hike`: the
    answer, "" for none; `allergies`: a comparable key that the text never
    shows (the note is private).
    """

    guest_id: int
    topic: str
    mine: object
    sent: object


def answer_differences(mine: Answer, sent: Answer) -> list[Difference]:
    """FR-38, AD-9, AD-2: where `mine` differs from `sent`, per guest id and topic.

    Both are normalised first. Guests are taken in ascending id order (the
    order household members are added). Attendance is compared for every
    guest on either side; days, cabin, meals, hike and allergies only for a
    guest who is coming on both sides. Identical answers give an empty list.
    """
    mine, sent = normalise_answer(mine), normalise_answer(sent)
    mine_days, sent_days = present_days(mine), present_days(sent)
    found = []
    for guest_id in sorted(set(mine.attendance) | set(sent.attendance)):
        coming = (mine.attendance.get(guest_id), sent.attendance.get(guest_id))
        if coming[0] != coming[1]:
            found.append(Difference(guest_id, ATTENDANCE, *coming))
            continue
        if guest_id not in mine_days:
            continue
        pairs = (
            (DAYS, mine_days[guest_id], sent_days[guest_id]),
            (CABIN, mine.night.get(guest_id) is True, sent.night.get(guest_id) is True),
            (
                MEALS,
                frozenset(mine.meals.get(guest_id, ())),
                frozenset(sent.meals.get(guest_id, ())),
            ),
            (HIKE, mine.hike.get(guest_id, ""), sent.hike.get(guest_id, "")),
            (
                ALLERGIES,
                allergy_key(mine.allergies.get(guest_id, EMPTY)),
                allergy_key(sent.allergies.get(guest_id, EMPTY)),
            ),
        )
        found += [Difference(guest_id, topic, a, b) for topic, a, b in pairs if a != b]
    return found
