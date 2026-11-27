"""Read queries for views and commands (Structural Seed).

Selectors load facts from the models and never filter on answer content; counts
and totals come from `wedding.rules` (AD-2). None of them writes, so a guest
view built on them never writes either (FR-3).
"""

from collections.abc import Iterable
from uuid import UUID

from django.db.models import Exists, OuterRef

from wedding.models import (
    Allergy,
    Consent,
    Guest,
    Household,
    HouseholdAnswer,
    PersonAnswer,
    Settings,
    Submission,
    User,
)
from wedding.rules.allergies import ALLERGY_KEYS, AllergyEntry
from wedding.rules.answer import Answer
from wedding.rules.contacts import tel_number
from wedding.rules.days import DAY_KEYS, MEAL_KEYS, WHOLE_WEEKEND
from wedding.rules.money import CABIN


def seed_conflicts(codes: Iterable[str], usernames: Iterable[str]) -> list[str]:
    """FR-72, AD-16: the seed codes and usernames already used by rows that are not test data.

    The seed command stops before writing anything when this is not empty, so it
    never replaces a real guest's link or a real account. Each item names the
    code or username in Norwegian; codes come first, in the order given.
    """
    codes = list(codes)
    usernames = list(usernames)
    taken_codes = set(
        Guest.objects.filter(code__in=codes, household__is_test_data=False).values_list(
            "code", flat=True
        )
    )
    taken_usernames = set(
        User.objects.filter(username__in=usernames, is_test_data=False).values_list(
            "username", flat=True
        )
    )
    return [f"lenkekoden «{code}»" for code in codes if code in taken_codes] + [
        f"brukernavnet «{username}»" for username in usernames if username in taken_usernames
    ]


def site_settings() -> Settings:
    """FR-3, FR-6, FR-41: the one settings row, read with `.get()` and never created.

    A data migration makes the row, so a missing row is a broken database and
    raises instead of being repaired by a guest's GET.
    """
    return Settings.objects.get()


def footer_contacts(settings: Settings | None = None) -> list[dict[str, str]]:
    """FR-6: the couple's contacts for the footer band on every valid-link page.

    Contact 1 first; each with the name, the phone as typed and the `tel:` number
    from `wedding.rules.contacts.tel_number`. A contact whose phone has no digit
    is left out, so an empty list means no footer
    (wedding/components/footer-band.html). Reads the settings row unless the
    caller already has it.
    """
    if settings is None:
        settings = site_settings()
    contacts = [
        (settings.contact_1_name, settings.contact_1_phone),
        (settings.contact_2_name, settings.contact_2_phone),
    ]
    return [
        {"name": name, "phone": phone, "tel": tel}
        for name, phone in contacts
        if (tel := tel_number(phone))
    ]


def programme_prices(settings: Settings | None = None) -> dict[str, int]:
    """FR-9, FR-32, AD-12: the three meal prices the programme's «Godt å vite» shows.

    Friday's dinner and the Saturday and Sunday breakfasts, in whole kroner, from
    the one settings row, the same source the RSVP form totals from
    (`form_prices`), so the programme and the form cannot show different
    prices. The template writes them with the `kroner` filter; no price is ever
    template text. Reads the settings row unless the caller already has it.
    """
    if settings is None:
        settings = site_settings()
    return {
        "friday_dinner": settings.price_friday_dinner,
        "saturday_breakfast": settings.price_saturday_breakfast,
        "sunday_breakfast": settings.price_sunday_breakfast,
    }


def form_prices(settings: Settings | None = None) -> dict[str, int]:
    """FR-16, FR-32, FR-33, AD-12 (Story 2.3): every price the RSVP form shows and totals.

    The programme's three meal prices plus the cabin for the whole weekend
    under `CABIN`, in whole kroner, for `household_total`. Reads the settings
    row unless the caller already has it.
    """
    if settings is None:
        settings = site_settings()
    return programme_prices(settings) | {CABIN: settings.price_cabin_weekend}


def household_guest_names(household: Household) -> list[str]:
    """FR-2, FR-7: the names of `household`'s guests, in the order they were added (by id).

    One SELECT of the names only; nothing from another household.
    """
    return list(
        Guest.objects.filter(household=household).order_by("id").values_list("name", flat=True)
    )


def household_members(household: Household) -> list[tuple[int, str]]:
    """FR-12, FR-13, AD-7: `household`'s guests as (id, name), in the order they were added.

    One SELECT; the RSVP form asks one question per member in this order, and
    only these ids are accepted from a draft or a posted form.
    """
    return list(Guest.objects.filter(household=household).order_by("id").values_list("id", "name"))


def household_answer(household: Household) -> HouseholdAnswer | None:
    """FR-74, AD-4 (Story 2.6a): `household`'s sent answer, or None before it has sent one.

    One SELECT; nothing from another household.
    """
    return HouseholdAnswer.objects.filter(household=household).first()


# The `PersonAnswer` field for each day key, as `send_answer` writes them.
_DAY_FIELDS = {"fri": "friday", "sat": "saturday", "sun": "sunday"}


def sent_answer(household: Household) -> Answer:
    """FR-23, FR-33, AD-4, AD-12 (Story 2.7): `household`'s stored answer as an `Answer`.

    The receipt shows what was sent, never a draft. Three SELECTs: the
    `PersonAnswer` rows, the `Allergy` rows and the `Consent` events of the
    household's guests. `whole` is True when every coming guest has all three
    days, else False with `days` per coming guest (None when nobody comes).
    `night` holds each coming guest's cabin, `meals` the chosen paid meals,
    `allergies` an `AllergyEntry` from the stored booleans, `consent` the
    latest event (given True, refused False, withdrawn or none: no entry) and
    `hike` the stored answer (blank: no entry). `confirmed` is empty: it is
    not stored. Guests with no `PersonAnswer` are left out.
    """
    rows = list(PersonAnswer.objects.filter(guest__household=household).order_by("guest_id"))
    attendance = {row.guest_id: row.coming for row in rows}
    coming = [row for row in rows if row.coming]
    days = {
        row.guest_id: [key for key in DAY_KEYS if getattr(row, _DAY_FIELDS[key])] for row in coming
    }
    whole = None
    if coming:
        whole = all(frozenset(chosen) == WHOLE_WEEKEND for chosen in days.values())
    allergies = {
        allergy.guest_id: AllergyEntry(
            cats=tuple(key for key in ALLERGY_KEYS if getattr(allergy, key)),
            none=allergy.none,
            note=allergy.note,
        )
        for allergy in Allergy.objects.filter(guest__household=household)
    }
    consent: dict[int, bool] = {}
    for event in Consent.objects.filter(guest__household=household).order_by("at", "pk"):
        if event.event == Consent.WITHDRAWN:
            consent.pop(event.guest_id, None)
        else:
            consent[event.guest_id] = event.event == Consent.GIVEN
    return Answer(
        attendance=attendance,
        whole=whole,
        days=days if whole is False else {},
        night={row.guest_id: row.cabin for row in coming},
        meals={row.guest_id: [meal for meal in MEAL_KEYS if getattr(row, meal)] for row in coming},
        allergies=allergies,
        consent=consent,
        confirmed=frozenset(),
        hike={row.guest_id: row.hike for row in coming if row.hike},
    )


def consent_versions(household: Household) -> dict[int, str]:
    """FR-37, AD-18 (Story 4.1): the text version of each guest's latest consent event.

    One SELECT over the household's guests' `Consent` events, in the order
    `sent_answer` reads them, so the version belongs to the event whose answer
    `sent_answer` reports. A guest with no event is left out.
    """
    events = Consent.objects.filter(guest__household=household).order_by("at", "pk")
    return {event.guest_id: event.text_version for event in events}


def submitted(household: Household, key: UUID) -> bool:
    """AD-20, NFR-1 (Story 2.6c): whether `key` was written as `household`'s answer.

    One SELECT; a key written for another household is False.
    """
    answers = HouseholdAnswer.objects.filter(pk=OuterRef("object_id"), household=household)
    return (
        Submission.objects.filter(key=key, kind=Submission.ANSWER).filter(Exists(answers)).exists()
    )
