"""The notice after a refused send, with what differs (Story 4.2; FR-38, AD-9, AD-18, UX-DR28).

Story 2.6c refused the send (AD-9) and said only who sent and when. Now the
notice also lists what differs between the guest's draft and the stored answer
(`answer_differences`), one line per difference, in the words the check page
uses. The list compares with the current stored answer only: there is no
history of earlier revisions (AD-4). Consent «Ja» is never carried across a
revision (AD-18), so the closing sentence says it must be given again.
"""

from collections.abc import Sequence
from dataclasses import dataclass, field

from django.utils import dateformat, timezone

from wedding.actors import Actor, GuestActor
from wedding.rsvp.steps import HIKE, MEALS
from wedding.rsvp.summary import day_names
from wedding.rsvp.text import join_words
from wedding.rules import differences as diff
from wedding.rules.answer import Answer
from wedding.rules.days import MEAL_KEYS, WHOLE_WEEKEND
from wedding.selectors import household_answer, sent_answer

NOT_SENT = "Svaret ble ikke sendt, fordi "
SAME = "Det du har fylt ut, er likt det som er sendt."
CLOSING = "Se over svaret og send det på nytt. Samtykke til å lagre allergier må gis på nytt."


@dataclass(frozen=True)
class Notice:
    """UX-DR52, FR-38: a notice: `text`, the `items` listed under it, an `after` paragraph.

    A refused send is an error; a conflict is a warning (the answer is not lost).
    """

    text: str
    items: Sequence[str] = field(default_factory=list)
    after: str = ""
    variant: str = "error"


def _attendance(coming: bool | None) -> str:
    if coming is None:
        return "ikke svart"
    return "kommer" if coming else "kommer ikke"


def _days(days: frozenset[str]) -> str:
    return "hele helgen" if days == WHOLE_WEEKEND else day_names(days)


def _meals(chosen: frozenset[str]) -> str:
    names = [MEALS[meal].name.lower() for meal in MEAL_KEYS if meal in chosen]
    return join_words(names) if names else "ingen måltider"


def _hike(choice: str) -> str:
    return HIKE[choice].lower() if choice else "ikke oppgitt"


def _cabin(stays: bool) -> str:
    return "hytte hele helgen" if stays else "overnatter ikke"


_WORDS = {
    diff.ATTENDANCE: _attendance,
    diff.DAYS: _days,
    diff.CABIN: _cabin,
    diff.MEALS: _meals,
    diff.HIKE: _hike,
}


def _line(difference: diff.Difference, name: str, sender: str) -> str:
    """FR-38: «<name>: du svarte <mine>, <sender> sendte <sent>»; allergies name the topic only."""
    if difference.topic == diff.ALLERGIES:
        return f"{name}: du og {sender} har ulike opplysninger om allergier og matbehov"
    words = _WORDS[difference.topic]
    return f"{name}: du svarte {words(difference.mine)}, {sender} sendte {words(difference.sent)}"


def conflict_notice(actor: Actor, mine: Answer, members: Sequence[tuple[int, str]]) -> Notice:
    """FR-38, AD-9, AD-18: why the send was refused, who sent when, and what differs.

    `mine` is the guest's draft as an `Answer`. A guest actor with a stored
    answer gets «<name> sendte et svar for husstanden <dag dato> kl. <tid>
    etter at du begynte» (Oslo time) and one line per difference, or `SAME`
    when there is none. Any other actor, or no stored answer, gets the
    generic sentence and no list (the couple's mount is Story 4.4).
    """
    stored = household_answer(actor.household) if isinstance(actor, GuestActor) else None
    if stored is None:
        generic = NOT_SENT + "svaret for husstanden er endret etter at du begynte."
        return Notice(generic, after=CLOSING, variant="warning")
    local = timezone.localtime(stored.sent_at)
    text = (
        f"{NOT_SENT}{stored.sent_by_name} sendte et svar for husstanden "
        f"{dateformat.format(local, 'l j. F Y')} kl. {dateformat.format(local, 'H:i')} "
        "etter at du begynte."
    )
    found = diff.answer_differences(mine, sent_answer(actor.household))
    if not found:
        return Notice(f"{text} {SAME}", after=CLOSING, variant="warning")
    names = dict(members)
    items = [_line(d, names.get(d.guest_id, "en gjest"), stored.sent_by_name) for d in found]
    return Notice(text, items, CLOSING, "warning")
