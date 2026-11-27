"""The conflict notice's text and the opened revision (Story 4.2; FR-38, AD-9, AD-18).

`conflict_notice` is read against the seeded Arild household, whose stored
answer Arild sent; `mine` is the stored answer with the draft's changes.
`opened_at` and `posted_revision` are pure and need no database.
"""

from dataclasses import replace
from zoneinfo import ZoneInfo

import pytest

from wedding.actors import AdminActor, GuestActor
from wedding.models import Guest, HouseholdAnswer, User
from wedding.rsvp.change import opened_at, posted_revision
from wedding.rsvp.conflict import CLOSING, NOT_SENT, SAME, conflict_notice
from wedding.rsvp.draft import Draft
from wedding.rules.allergies import AllergyEntry
from wedding.selectors import household_members, sent_answer

ARILD = "test-arild000000000000"
OSLO = ZoneInfo("Europe/Oslo")

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _arild():
    guest = Guest.objects.get(code=ARILD)
    return GuestActor(guest=guest, household=guest.household), household_members(guest.household)


def _ids() -> dict[str, int]:
    return {guest.name: guest.pk for guest in Guest.objects.filter(household__guests__code=ARILD)}


def test_the_notice_names_who_sent_when_and_what_differs(seeded_with_answers):
    """FR-38, AD-9 (matrix «Differences listed»): sender, weekday, date and time in Oslo time,
    the golden line for Filippa's cabin and the closing sentence about consent."""
    actor, members = _arild()
    filippa = _ids()["Filippa"]
    mine = sent_answer(actor.household)
    mine = replace(mine, night=mine.night | {filippa: False})
    stored = HouseholdAnswer.objects.get(household=actor.household)
    local = stored.sent_at.astimezone(OSLO)
    notice = conflict_notice(actor, mine, members)
    assert notice.variant == "warning"
    assert notice.text.startswith(f"{NOT_SENT}Arild sendte et svar for husstanden ")
    assert notice.text.endswith(f"kl. {local:%H:%M} etter at du begynte.")
    assert notice.items == ["Filippa: du svarte overnatter ikke, Arild sendte hytte hele helgen"]
    assert notice.after == CLOSING
    assert "Samtykke til å lagre allergier må gis på nytt." in notice.after


def test_each_topic_is_worded_as_the_check_page_words_it(seeded_with_answers):
    """FR-38, UX-DR28: «kommer ikke», the day names, meal names, the hike words and the topic
    only for allergies (never the note)."""
    actor, members = _arild()
    ids = _ids()
    mine = sent_answer(actor.household)
    mine = replace(
        mine,
        attendance=mine.attendance | {ids["Filippa"]: False},
        whole=False,
        days={ids["Arild"]: ["fri", "sat", "sun"], ids["Marie"]: ["sat", "sun"]},
        meals=mine.meals | {ids["Arild"]: ["friday_dinner", "sunday_breakfast"]},
        hike=mine.hike | {ids["Arild"]: "maybe"},
        allergies=mine.allergies | {ids["Arild"]: AllergyEntry(("gluten",), False, "hemmelig")},
    )
    items = conflict_notice(actor, mine, members).items
    assert "Marie: du svarte lørdag 27. mai og søndag 28. mai, Arild sendte hele helgen" in items
    assert "Filippa: du svarte kommer ikke, Arild sendte kommer" in items
    assert (
        "Arild: du svarte middag fredag og frokost søndag, "
        "Arild sendte middag fredag, frokost lørdag og frokost søndag"
    ) in items
    assert "Arild: du svarte kanskje, Arild sendte ja" in items
    assert "Arild: du og Arild har ulike opplysninger om allergier og matbehov" in items
    assert "hemmelig" not in " ".join(items)


def test_no_differences_says_so(seeded_with_answers):
    """FR-38 (matrix «Identical content»): the same sentence, no list, and still who sent."""
    actor, members = _arild()
    notice = conflict_notice(actor, sent_answer(actor.household), members)
    assert notice.items == []
    assert notice.text.endswith(f"etter at du begynte. {SAME}")
    assert "Arild sendte et svar for husstanden" in notice.text


def test_an_actor_without_a_guest_household_gets_the_generic_sentence(seeded_with_answers):
    """FR-38 (matrix «Non-guest actor»): no name, no list; the couple's text is Story 4.4."""
    _, members = _arild()
    couple = AdminActor(user=User(username="rikke", role=User.Role.COUPLE))
    notice = conflict_notice(couple, sent_answer(_arild()[0].household), members)
    assert notice.text == NOT_SENT + "svaret for husstanden er endret etter at du begynte."
    assert (notice.items, notice.after) == ([], CLOSING)


def test_no_stored_answer_gives_the_generic_sentence(seeded):
    """FR-38: a household with no stored answer (the seed fixture removed it)."""
    actor, members = _arild()
    notice = conflict_notice(actor, sent_answer(actor.household), members)
    assert notice.text.endswith("svaret for husstanden er endret etter at du begynte.")
    assert notice.items == []


def _draft(**overrides) -> Draft:
    draft = Draft(started="2026-11-27T10:00:00+00:00", rev=5, resp=1, cons={1: True}, conf=[2])
    return replace(draft, **({"cv": "v1"} | overrides))


@pytest.mark.parametrize(
    ("posted", "revision"),
    [
        (2, 2),
        (0, 0),
        (None, 5),
        (5, 5),
        (9, 5),
    ],
)
def test_opened_at_moves_a_seed_only_for_an_older_whole_revision(posted, revision):
    """FR-38, AD-9 (matrix «Forged or missing field»): a posted revision below the current
    one is taken; missing, equal or higher values change nothing."""
    assert opened_at(_draft(), posted, 5).rev == revision


def test_a_taken_revision_clears_consent_confirmations_and_version():
    """AD-18: no «Ja» across a revision change, also on a stale seeded draft."""
    moved = opened_at(_draft(), 2, 5)
    assert (moved.cons, moved.conf, moved.cv) == ({}, [], None)
    assert (opened_at(_draft(), 9, 5).cons, opened_at(_draft(), 9, 5).conf) == ({1: True}, [2])


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("3", 3),
        ("0", 0),
        ("", None),
        ("abc", None),
        ("-1", None),
        ("1.5", None),
        ("٣", None),
        ("1" * 5000, None),
        ("1" * 10, None),
        ("1" * 9, 111111111),
    ],
)
def test_posted_revision_reads_only_whole_numbers(value, expected):
    """FR-38 (matrix «Forged or missing field»): only whole ASCII numbers are taken."""
    assert posted_revision({"revisjon": value}) == expected
    assert posted_revision({}) is None


def test_a_guest_who_is_not_a_member_is_called_en_gjest(seeded_with_answers):
    """FR-38: a difference for a guest id the household no longer lists never starts with «: »."""
    actor, members = _arild()
    mine = sent_answer(actor.household)
    mine = replace(mine, night=mine.night | {_ids()["Filippa"]: False})
    others = [member for member in members if member[1] != "Filippa"]
    notice = conflict_notice(actor, mine, others)
    assert notice.items == ["en gjest: du svarte overnatter ikke, Arild sendte hytte hele helgen"]
