"""When a re-sent answer really differs from the stored one (Story 4.1; FR-39, AD-19, AD-2).

`answer_changed` is the rule behind the couple's «Changed» marker
(`Household.changed_at`): a first answer, an identical re-send and the seed
never count, only a different answer does. Pure: plain values in, a bool out.
"""

from wedding.rules.allergies import EMPTY, AllergyEntry
from wedding.rules.answer import Answer, normalise_answer, present_days


def allergy_key(entry: AllergyEntry) -> tuple[frozenset[str], bool, str]:
    """FR-39: an allergy entry as comparable values (the category order never counts)."""
    return frozenset(entry.cats), entry.none, entry.note


def _consent_differs(stored: Answer, new: Answer, guest_id: int) -> bool:
    """FR-39, AD-18: whether a present guest's consent answer or stored allergy entry changes.

    A new «Ja» changes when the stored consent was not «Ja» or the entry
    differs; a new «Nei» when the stored consent was not «Nei» or an
    allergy entry would still be stored. A new consent left unanswered keeps
    what is stored, so it never counts.
    """
    given = new.consent.get(guest_id)
    if given is None:
        return False
    if given:
        return stored.consent.get(guest_id) is not True or allergy_key(
            stored.allergies.get(guest_id, EMPTY)
        ) != allergy_key(new.allergies.get(guest_id, EMPTY))
    return stored.consent.get(guest_id) is not False or guest_id in stored.allergies


def answer_changed(stored: Answer, new: Answer) -> bool:
    """FR-39, AD-19: whether `new` differs in content from `stored`, after normalising both.

    Compared per household member: who is coming, the days each is present,
    the cabin, the chosen meals as sets, the Friday hike and, for each
    present guest, the consent and allergy entry (`_consent_differs`).
    Confirmations are not stored and never count.
    """
    stored, new = normalise_answer(stored), normalise_answer(new)
    stored_days, new_days = present_days(stored), present_days(new)
    for guest_id in set(stored.attendance) | set(new.attendance):
        if stored_days.get(guest_id) != new_days.get(guest_id):
            return True
        if guest_id not in new_days:
            continue
        if (
            (stored.night.get(guest_id) is True) != (new.night.get(guest_id) is True)
            or set(stored.meals.get(guest_id, ())) != set(new.meals.get(guest_id, ()))
            or stored.hike.get(guest_id, "") != new.hike.get(guest_id, "")
            or _consent_differs(stored, new, guest_id)
        ):
            return True
    return False
