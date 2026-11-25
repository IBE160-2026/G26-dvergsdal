"""Sending a household's answer (Stories 2.6a, 2.6b, 2.6c; FR-26, FR-29, FR-41, FR-74,
FR-75, AD-3, AD-4, AD-7, AD-9, AD-18, AD-20, NFR-1, NFR-2, NFR-3).

`send_answer` is the RSVP form's one write: the normalised answer as one
`PersonAnswer` per guest and the household's `HouseholdAnswer`, in one
transaction, and `Household.revision` raised. Story 2.6b: in the same
transaction each guest's `Allergy` is stored, deleted or kept by
`consent_outcomes`, and one `Consent` event is recorded per coming guest who
answered «Ja» or «Nei». Story 2.6c makes a send that repeats or comes too
late safe: a submission id already written returns the earlier answer, and a
draft from an older revision, a consent answer to an older consent text or a
total that differs from the one the check page showed is refused, writing
nothing and recording no `Submission`.
"""

from datetime import datetime
from uuid import UUID

from django.db import transaction
from django.db.models import F

from wedding.actors import Actor, AdminActor, GuestActor
from wedding.models import (
    Allergy,
    Consent,
    Guest,
    Household,
    HouseholdAnswer,
    PersonAnswer,
    Settings,
    Submission,
)
from wedding.rules.allergies import (
    ALLERGY_KEYS,
    DELETE,
    EMPTY,
    STORE,
    allergy_problems,
    consent_outcomes,
    has_allergy_info,
)
from wedding.rules.answer import Answer, normalise_answer, present_days
from wedding.rules.days import MEAL_KEYS
from wedding.rules.deadline import is_past_deadline
from wedding.rules.money import household_total
from wedding.selectors import form_prices
from wedding.services.consent import CONSENT_TEXT_VERSION
from wedding.services.exceptions import (
    ConsentTextChanged,
    DeadlinePassed,
    InvalidAnswer,
    NotAllowed,
    RevisionConflict,
    TotalChanged,
)

# The `PersonAnswer` field for each day key in `wedding.rules.days`; the meal
# keys (`MEAL_KEYS`) are the field names themselves.
DAY_FIELDS = {"fri": "friday", "sat": "saturday", "sun": "sunday"}


def _answer_ids(answer: Answer) -> set[int]:
    """AD-3: every guest id the answer names, in any of its mappings."""
    ids = set(answer.attendance) | set(answer.confirmed)
    for mapping in (
        answer.days,
        answer.night,
        answer.meals,
        answer.allergies,
        answer.consent,
        answer.hike,
    ):
        ids |= set(mapping)
    return ids


def _apply_consent(
    guests: dict[int, Guest], present, answer: Answer, sender: Guest, now: datetime
) -> None:
    """FR-26, FR-29, AD-18 (Story 2.6b): store, delete or keep each guest's
    `Allergy`, and record one `Consent` per coming guest who answered."""
    outcomes = consent_outcomes(guests, present, answer.allergies, answer.consent)
    for guest_id, outcome in outcomes.items():
        guest = guests[guest_id]
        entry = answer.allergies.get(guest_id, EMPTY)
        if outcome == STORE and has_allergy_info(entry):
            Allergy.objects.update_or_create(
                guest=guest,
                defaults={
                    **{key: key in entry.cats for key in ALLERGY_KEYS},
                    "none": entry.none,
                    "note": entry.note,
                },
            )
        elif outcome in (STORE, DELETE):
            Allergy.objects.filter(guest=guest).delete()
        if guest_id in present and guest_id in answer.consent:
            Consent.objects.create(
                guest=guest,
                event=Consent.GIVEN if answer.consent[guest_id] else Consent.REFUSED,
                at=now,
                given_by=sender,
                given_by_name=sender.name,
                text_version=CONSENT_TEXT_VERSION,
            )


def send_answer(
    actor: Actor,
    *,
    household: Household,
    respondent: int,
    answer: Answer,
    now: datetime,
    submission: UUID,
    revision: int,
    shown_total: int,
    consent_version: str | None,
) -> HouseholdAnswer:
    """FR-41, FR-74, FR-75, AD-3, AD-4, AD-9, NFR-2: write `household`'s answer.

    Refusals, in order, write nothing: an admin actor (`NotAllowed`; the
    couple's override is Story 4.4); a guest actor from another household, or
    a respondent or answer id that is not a guest of `household`
    (`NotAllowed`); a guest of the household without an attendance entry
    (`InvalidAnswer`); a guest actor after the deadline (`DeadlinePassed`; the
    system actor is not bound by it). Then the answer is normalised, one
    `PersonAnswer` per guest and the `HouseholdAnswer` (sent by `respondent`,
    at `now`) are created or updated, and the revision rises by one.

    Story 2.6b (FR-26, FR-27, FR-29, AD-18): a coming guest whose allergy
    entry has a problem (`allergy_problems`: «Ingen …» with other data, or
    «Ja» for someone else without the confirmation) is refused with
    `InvalidAnswer` before any write. Each guest's `Allergy` then follows
    `consent_outcomes`: stored on «Ja» (deleted when the entry is empty),
    deleted on «Nei» or when not coming, unchanged when unanswered. Every
    coming guest who answered gets one `Consent` event (given or refused) by
    the respondent, at `now`, with `CONSENT_TEXT_VERSION`.

    Story 2.6c (AD-7, AD-9, AD-18, AD-20, NFR-1), in this order after the
    actor and household checks: a `submission` id already recorded is a
    repeat and returns the earlier `HouseholdAnswer` without writing (an id
    recorded for another household is `NotAllowed`); a `revision` other than
    the household's current one is `RevisionConflict`, checked before the
    deadline; after normalising, a coming guest with a consent answer given to
    a `consent_version` other than `CONSENT_TEXT_VERSION` is
    `ConsentTextChanged`; a `shown_total` other than `household_total` at
    today's prices is `TotalChanged`. A send that writes records `submission`
    as a `Submission` in the same transaction, so a same-id race fails on
    the unique key instead of writing twice.
    """
    with transaction.atomic():
        if isinstance(actor, AdminActor):
            raise NotAllowed()
        if isinstance(actor, GuestActor) and actor.household.pk != household.pk:
            raise NotAllowed()
        repeat = Submission.objects.filter(key=submission).first()
        if repeat is not None:
            earlier = HouseholdAnswer.objects.filter(
                pk=repeat.object_id, household=household
            ).first()
            if repeat.kind != Submission.ANSWER or earlier is None:
                raise NotAllowed()
            return earlier
        guests = {guest.pk: guest for guest in Guest.objects.filter(household=household)}
        if respondent not in guests or not _answer_ids(answer) <= set(guests):
            raise NotAllowed()
        if set(guests) - set(answer.attendance):
            raise InvalidAnswer()
        current = Household.objects.values_list("revision", flat=True).get(pk=household.pk)
        if current != revision:
            raise RevisionConflict(revision=current)
        settings = Settings.objects.get()
        if isinstance(actor, GuestActor) and is_past_deadline(settings.rsvp_deadline, now):
            raise DeadlinePassed()
        answer = normalise_answer(answer)
        present = present_days(answer)
        for guest_id in present:
            if allergy_problems(
                answer.allergies.get(guest_id, EMPTY),
                answer.consent.get(guest_id),
                guest_id in answer.confirmed,
                guest_id == respondent,
            ):
                raise InvalidAnswer()
        if consent_version != CONSENT_TEXT_VERSION and any(
            guest_id in answer.consent for guest_id in present
        ):
            raise ConsentTextChanged()
        if household_total(answer, form_prices(settings)) != shown_total:
            raise TotalChanged()
        for guest_id, guest in guests.items():
            days = present.get(guest_id, frozenset())
            meals = set(answer.meals.get(guest_id, ())) if guest_id in present else set()
            PersonAnswer.objects.update_or_create(
                guest=guest,
                defaults={
                    "coming": guest_id in present,
                    **{field: key in days for key, field in DAY_FIELDS.items()},
                    "cabin": guest_id in present and answer.night.get(guest_id) is True,
                    **{field: field in meals for field in MEAL_KEYS},
                    "hike": answer.hike.get(guest_id, "") if guest_id in present else "",
                },
            )
        sender = guests[respondent]
        _apply_consent(guests, present, answer, sender, now)
        sent, _ = HouseholdAnswer.objects.update_or_create(
            household=household,
            defaults={"sent_by": sender, "sent_by_name": sender.name, "sent_at": now},
        )
        Household.objects.filter(pk=household.pk).update(revision=F("revision") + 1)
        Submission.objects.create(
            key=submission, kind=Submission.ANSWER, object_id=sent.pk, created_at=now
        )
    return sent
