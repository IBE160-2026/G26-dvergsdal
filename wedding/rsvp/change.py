"""Opening a sent answer to change it (Story 4.1; FR-37, FR-38, AD-8, AD-18).

`seeded_draft` builds, in memory and per request, the draft an answered
household's form opens with, from the stored answer; it is never written to
the cookie by a GET (AD-8), only by «Fortsett» or «Velg» as any draft is.
`last_changed_text` is the form's top notice: who sent the answer last.
Story 4.2 (FR-38, AD-9): a seeded form carries the revision it was opened at
in a hidden `revisjon`; `opened_at` starts a cookie-less first POST at it.
"""

from collections.abc import Mapping
from dataclasses import replace
from datetime import datetime

from django.utils import dateformat, timezone

from wedding.models import Household, HouseholdAnswer
from wedding.rsvp.draft import Draft
from wedding.rules.form_steps import STEP_KEYS
from wedding.selectors import consent_versions, sent_answer
from wedding.services.consent import CONSENT_TEXT_VERSION

Members = list[tuple[int, str]]
# FR-38, AD-9 (Story 4.2): the hidden field that carries the revision a form was opened at.
REVISION_FIELD = "revisjon"


def seeded_draft(household: Household, members: Members, respondent: int, now: datetime) -> Draft:
    """FR-37, AD-8, AD-18: the draft of `household`'s stored answer, started `now` at its revision.

    `respondent` is the opener. Attendance, days, cabin, meals, allergies and
    hike come from the stored answer, and every step is done (the caller runs
    `_settled`), unless a member has no stored answer yet (added after it):
    then no step is done and the form opens at step 1 with the others
    filled in. A stored consent «Ja» or «Nei» is kept only for the current
    consent text (`CONSENT_TEXT_VERSION`); confirmations are never stored, so
    nobody carries one over and a respondent who is not the person confirms
    again on step 5.
    """
    stored = sent_answer(household)
    versions = consent_versions(household)
    consent = {
        guest_id: given
        for guest_id, given in stored.consent.items()
        if versions.get(guest_id) == CONSENT_TEXT_VERSION
    }
    complete = all(guest_id in stored.attendance for guest_id, _ in members)
    draft = Draft.new(revision=household.revision, respondent=respondent, now=now)
    draft.att = dict(stored.attendance)
    draft.done = list(STEP_KEYS) if complete else []
    draft.whole = stored.whole
    draft.days = {guest_id: list(days) for guest_id, days in stored.days.items()}
    draft.night = dict(stored.night)
    draft.meals = {guest_id: list(meals) for guest_id, meals in stored.meals.items()}
    draft.alg = dict(stored.allergies)
    draft.cons = consent
    draft.hike = dict(stored.hike)
    draft.cv = CONSENT_TEXT_VERSION if consent else None
    return draft


def posted_revision(post: Mapping[str, str]) -> int | None:
    """FR-38, AD-9: the revision a form was opened at (hidden `revisjon`), or None unless whole."""
    value = post.get(REVISION_FIELD, "")
    return int(value) if value.isascii() and value.isdigit() else None


def opened_at(draft: Draft, posted: int | None, current: int) -> Draft:
    """FR-38, AD-9, AD-18 (Story 4.2): a seeded `draft` moved back to its form's revision.

    `posted` is the form's `revisjon`. When it is a whole number below the
    household's `current` revision, the household's answer changed after the
    form was opened: the draft starts at `posted`, so the send is refused
    (Story 2.6c), and its consent answers and text version are cleared (no
    «Ja» across a revision change). A missing, forged or higher value
    changes nothing.
    """
    if posted is None or not 0 <= posted < current:
        return draft
    return replace(draft, rev=posted, cons={}, conf=[], cv=None)


def last_changed_text(answer: HouseholdAnswer) -> str:
    """FR-38, UX-DR28: «Sist endret av <name>, <j. F> kl. <H:i>», Oslo time, no year.

    It names the last send (`sent_by_name`, `sent_at`), the one who answered
    last; `Household.changed_at` is only the couple's marker.
    """
    local = timezone.localtime(answer.sent_at)
    return (
        f"Sist endret av {answer.sent_by_name}, {dateformat.format(local, 'j. F')} "
        f"kl. {dateformat.format(local, 'H:i')}"
    )
