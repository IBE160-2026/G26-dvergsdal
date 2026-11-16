"""The `update_settings` service (FR-64, AD-3, AD-10, AD-11, AD-12).

The system actor (the seed command) and the couple may change the settings row;
helpers and guests may not. Invalid values are refused with a Norwegian message,
and every refusal leaves the row as it was.
"""

import dataclasses
import datetime

import pytest

from wedding.actors import SYSTEM, AdminActor, GuestActor
from wedding.models import Settings, User
from wedding.services.exceptions import InvalidSettings, NotAllowed
from wedding.services.households import NewGuest, create_household
from wedding.services.settings import SettingsValues, update_settings

VALUES = SettingsValues(
    contact_1_name="Rikke",
    contact_1_phone="+47 000 00 101",
    contact_2_name="Valdemar",
    contact_2_phone="+47 000 00 102",
    price_cabin_weekend=1500,
    price_friday_dinner=340,
    price_saturday_breakfast=260,
    price_sunday_breakfast=260,
    rsvp_deadline=datetime.date(2027, 12, 15),
    vipps_number="00000",
    account_number="1234.56.78900",
)


def stored_values():
    row = Settings.objects.get()
    return SettingsValues(
        **{field.name: getattr(row, field.name) for field in dataclasses.fields(SettingsValues)}
    )


def make_admin(role):
    return AdminActor(User.objects.create_user(username="rikke", role=role))


@pytest.mark.django_db
def test_the_system_actor_replaces_every_value():
    """FR-64, AD-3: the seed command sets all settings in one write."""
    update_settings(SYSTEM, VALUES)

    assert stored_values() == VALUES
    assert Settings.objects.count() == 1


@pytest.mark.django_db
def test_the_couple_can_change_the_settings():
    """FR-64, AD-10: the couple may change prices, deadline, contacts and payment details."""
    changed = dataclasses.replace(VALUES, price_cabin_weekend=1600)

    update_settings(make_admin(User.Role.COUPLE), changed)

    assert stored_values() == changed


@pytest.mark.django_db
def test_texts_are_stored_without_edge_spaces():
    """FR-64: what the couple types is trimmed before it is stored."""
    update_settings(
        SYSTEM, dataclasses.replace(VALUES, contact_1_name="  Rikke ", vipps_number=" 1 ")
    )

    row = Settings.objects.get()
    assert (row.contact_1_name, row.vipps_number) == ("Rikke", "1")


@pytest.mark.django_db
def test_a_helper_cannot_change_the_settings():
    """AD-10, FR-64, Story 1.3 matrix row "Settings, helper": refused, nothing written."""
    before = stored_values()

    with pytest.raises(NotAllowed):
        update_settings(make_admin(User.Role.HELPER), VALUES)

    assert stored_values() == before


@pytest.mark.django_db
def test_a_guest_cannot_change_the_settings():
    """AD-3, AD-10: a guest actor is neither the system nor the couple."""
    household = create_household(SYSTEM, [NewGuest("Sigmund")])
    before = stored_values()

    with pytest.raises(NotAllowed):
        update_settings(GuestActor(guest=household.guests.get(), household=household), VALUES)

    assert stored_values() == before


@pytest.mark.django_db
def test_zero_prices_and_blank_optional_texts_are_allowed():
    """FR-64, AD-12: a free item costs 0, and phones and payment details may be empty."""
    free = dataclasses.replace(
        VALUES,
        price_friday_dinner=0,
        contact_1_phone="",
        contact_2_phone="",
        vipps_number="",
        account_number="",
    )

    update_settings(SYSTEM, free)

    assert stored_values() == free


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"price_cabin_weekend": -1}, "Prisen for hytte kan ikke være negativ."),
        ({"price_sunday_breakfast": -260}, "Prisen for frokost søndag kan ikke være negativ."),
        ({"price_friday_dinner": 340.5}, "Prisen for middag fredag må være et helt antall kroner."),
        ({"price_friday_dinner": "340"}, "Prisen for middag fredag må være et helt antall kroner."),
        (
            {"price_saturday_breakfast": True},
            "Prisen for frokost lørdag må være et helt antall kroner.",
        ),
        ({"contact_1_name": "  "}, "Navnet på kontaktperson 1 kan ikke være tomt."),
        ({"contact_2_name": ""}, "Navnet på kontaktperson 2 kan ikke være tomt."),
        ({"contact_1_name": "x" * 101}, "Navnet på kontaktperson 1 kan ha høyst 100 tegn."),
        (
            {"contact_2_phone": "1" * 31},
            "Telefonnummeret til kontaktperson 2 kan ha høyst 30 tegn.",
        ),
        ({"vipps_number": "1" * 21}, "Vipps-nummeret kan ha høyst 20 tegn."),
        ({"account_number": "1" * 21}, "Kontonummeret kan ha høyst 20 tegn."),
        (
            {"rsvp_deadline": datetime.datetime(2027, 12, 15, 23, 59)},
            "Svarfristen må være en dato.",
        ),
        ({"rsvp_deadline": "2027-12-15"}, "Svarfristen må være en dato."),
    ],
)
def test_an_invalid_value_is_refused_and_nothing_is_written(change, message):
    """FR-64, AD-11, AD-12: prices are whole kroner from 0, texts fit, the deadline is a date."""
    before = stored_values()

    with pytest.raises(InvalidSettings) as refused:
        update_settings(SYSTEM, dataclasses.replace(VALUES, **change))

    assert refused.value.message == message
    assert stored_values() == before


@pytest.mark.django_db
def test_the_longest_allowed_texts_are_stored():
    """FR-64: the length limits are inclusive."""
    longest = dataclasses.replace(
        VALUES, contact_1_name="x" * 100, contact_1_phone="1" * 30, vipps_number="1" * 20
    )

    update_settings(SYSTEM, longest)

    assert stored_values() == longest
