"""The seeded draft and the «Sist endret av …» text (Story 4.1; FR-37, FR-38, AD-8, AD-18).

`seeded_draft` is built in memory from the stored answer; these tests read it
through the same `_answer` the form's rules use, so the seed and the stored
answer are compared as the form sees them.
"""

import datetime

import pytest
from django.utils import timezone

from wedding.models import Consent, Guest, PersonAnswer
from wedding.rsvp.change import last_changed_text, seeded_draft
from wedding.rsvp.views import _answer, _settled
from wedding.selectors import household_answer, household_members, sent_answer
from wedding.services.consent import CONSENT_TEXT_VERSION

ARILD = "test-arild000000000000"

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _seed(code: str = ARILD):
    household = Guest.objects.get(code=code).household
    members = household_members(household)
    owner = Guest.objects.get(code=code).pk
    draft = seeded_draft(household, members, owner, timezone.now())
    return household, members, draft


def test_arilds_seed_equals_the_stored_answer(seeded_with_answers):
    """FR-37, AD-8: the seed holds the stored answer, every step done, the
    household's revision and the opener as respondent."""
    household, members, draft = _seed()
    stored = sent_answer(household)
    seeded = _answer(_settled(draft, members), members)
    assert seeded.attendance == stored.attendance
    assert (seeded.whole, dict(seeded.days)) == (stored.whole, dict(stored.days))
    assert seeded.night == stored.night
    assert seeded.meals == stored.meals
    assert seeded.allergies == stored.allergies
    assert seeded.hike == stored.hike
    assert (draft.rev, draft.resp) == (household.revision, Guest.objects.get(code=ARILD).pk)


def test_the_seed_carries_consent_but_never_a_confirmation(seeded_with_answers):
    """FR-37, AD-18: Arild's stored «Ja» and Filippa's «Nei» are kept with the
    current text version; nothing is confirmed, so step 5 asks again for
    another respondent."""
    _, _, draft = _seed()
    arild = Guest.objects.get(code=ARILD).pk
    filippa = Guest.objects.get(name="Filippa").pk
    assert draft.cons == {arild: True, filippa: False}
    assert draft.cv == CONSENT_TEXT_VERSION
    assert draft.conf == []


def test_a_consent_of_another_text_version_is_not_seeded(seeded_with_answers):
    """FR-37, AD-18 (matrix «Consent text changed»): that guest's consent is
    left out and `cv` is empty."""
    Consent.objects.update(text_version="gammel")
    _, _, draft = _seed()
    assert draft.cons == {}
    assert draft.cv is None


def test_a_member_without_a_stored_answer_opens_at_step_1(seeded_with_answers):
    """FR-37, FR-13: a member added after the answer has no `PersonAnswer`; no
    step is done, the others are filled in."""
    household, _, _ = _seed()
    leone = Guest.objects.get(name="Leone", household=household)
    PersonAnswer.objects.filter(guest=leone).delete()
    _, _, draft = _seed()
    assert draft.done == []
    assert leone.pk not in draft.att
    assert draft.att[Guest.objects.get(code=ARILD).pk] is True


def test_the_notice_names_the_last_sender_in_oslo_time(seeded_with_answers):
    """FR-38, UX-DR28: «Sist endret av <name>, <j. F> kl. <H:i>», no year."""
    sent = household_answer(Guest.objects.get(code=ARILD).household)
    sent.sent_at = datetime.datetime(2026, 11, 3, 17, 40, tzinfo=datetime.UTC)
    sent.sent_by_name = "Arild"
    assert last_changed_text(sent) == "Sist endret av Arild, 3. november kl. 18:40"
