"""Changing the one row of settings: contacts, prices, deadline and payment details.

FR-64: the couple changes them (the admin page comes in Story 4.5), and the seed
command sets the fictional ones with the system actor (Story 1.3). Helpers cannot
(AD-10). Prices are whole kroner (AD-12) and the deadline is a date (AD-11).
"""

import datetime
from dataclasses import asdict, dataclass

from django.db import transaction

from wedding.actors import Actor, SystemActor
from wedding.models import Settings
from wedding.services.exceptions import InvalidSettings
from wedding.services.permissions import require_couple

TEXT_FIELDS = {
    "contact_1_name": "Navnet på kontaktperson 1",
    "contact_1_phone": "Telefonnummeret til kontaktperson 1",
    "contact_2_name": "Navnet på kontaktperson 2",
    "contact_2_phone": "Telefonnummeret til kontaktperson 2",
    "vipps_number": "Vipps-nummeret",
    "account_number": "Kontonummeret",
}
REQUIRED_TEXT_FIELDS = ("contact_1_name", "contact_2_name")
PRICE_FIELDS = {
    "price_cabin_weekend": "Prisen for hytte",
    "price_friday_dinner": "Prisen for middag fredag",
    "price_saturday_breakfast": "Prisen for frokost lørdag",
    "price_sunday_breakfast": "Prisen for frokost søndag",
}


@dataclass(frozen=True)
class SettingsValues:
    """Every value of the settings row, all replaced together (FR-64)."""

    contact_1_name: str
    contact_1_phone: str
    contact_2_name: str
    contact_2_phone: str
    price_cabin_weekend: int
    price_friday_dinner: int
    price_saturday_breakfast: int
    price_sunday_breakfast: int
    rsvp_deadline: datetime.date
    vipps_number: str
    account_number: str


def update_settings(actor: Actor, values: SettingsValues) -> Settings:
    """FR-64, AD-3, AD-10, AD-11, AD-12: replace every value of the settings row.

    Only the system actor or a couple account may change settings. Texts are
    stored without edge spaces. A refusal raises `NotAllowed` or `InvalidSettings`
    with nothing written.
    """
    with transaction.atomic():
        if not isinstance(actor, SystemActor):
            require_couple(actor)
        cleaned = _validated(values)
        settings_row = Settings.objects.get()
        for name, value in cleaned.items():
            setattr(settings_row, name, value)
        settings_row.save(update_fields=list(cleaned))
    return settings_row


def _validated(values: SettingsValues) -> dict:
    """FR-64, AD-11, AD-12: the values with texts trimmed, or `InvalidSettings`.

    `save()` runs no validators and SQLite ignores `max_length`, so lengths and
    prices are checked here.
    """
    cleaned = asdict(values)
    for name, label in TEXT_FIELDS.items():
        text = cleaned[name].strip()
        max_length = Settings._meta.get_field(name).max_length
        if name in REQUIRED_TEXT_FIELDS and not text:
            raise InvalidSettings(f"{label} kan ikke være tomt.")
        if len(text) > max_length:
            raise InvalidSettings(f"{label} kan ha høyst {max_length} tegn.")
        cleaned[name] = text
    for name, label in PRICE_FIELDS.items():
        price = cleaned[name]
        # bool is a subclass of int, but True is not a price.
        if type(price) is not int:
            raise InvalidSettings(f"{label} må være et helt antall kroner.")
        if price < 0:
            raise InvalidSettings(f"{label} kan ikke være negativ.")
    deadline = cleaned["rsvp_deadline"]
    # datetime is a subclass of date, but the deadline is a date only (AD-11).
    if type(deadline) is not datetime.date:
        raise InvalidSettings("Svarfristen må være en dato.")
    return cleaned
