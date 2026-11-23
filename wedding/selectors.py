"""Read queries for views and commands (Structural Seed).

Selectors load facts from the models and never filter on answer content; counts
and totals come from `wedding.rules` (AD-2). None of them writes, so a guest
view built on them never writes either (FR-3).
"""

from collections.abc import Iterable

from wedding.models import Guest, Household, Settings, User
from wedding.rules.contacts import tel_number
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
