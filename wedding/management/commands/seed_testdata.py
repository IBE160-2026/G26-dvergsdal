"""`uv run manage.py seed_testdata`: fill the database with fictional test data (FR-68).

Reads `wedding/fixtures/seed.toml` and builds the settings, the households with
their guests and the two test admin accounts through services with the system
actor (AD-3, AD-16). It runs only with `APP_ENV` unset or `local` (FR-72, AD-14),
stops without writing if a seed code or username belongs to data it did not make,
and replaces its own earlier test data, so every run gives the same result.

Story 1.3 loads only settings, users, households and the guests' name, phone,
email and code. The planned answers, allergies, consents and payments in the
file are loaded by Stories 2.6d, 5.2 and 7.2.
"""

import datetime
import os
import tomllib
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from config.env import validate_app_env
from wedding.actors import SYSTEM
from wedding.selectors import test_data_conflicts
from wedding.services.exceptions import ServiceError
from wedding.services.households import NewGuest, create_household
from wedding.services.settings import SettingsValues, update_settings
from wedding.services.testdata import reset_test_data
from wedding.services.users import create_admin_user

SEED_PATH = Path(__file__).resolve().parents[2] / "fixtures" / "seed.toml"
LOCAL_URL = "http://127.0.0.1:8000"
ROLE_NAMES = {"couple": "brudeparet", "helper": "hjelper"}
NOTHING_CHANGED = "Ingenting ble endret."


class Command(BaseCommand):
    help = (
        "Fyller databasen med fiktive testdata fra wedding/fixtures/seed.toml og skriver ut "
        "en testlenke per gjest. Erstatter testdata fra forrige kjøring. Kjører bare med "
        "APP_ENV=local (eller uten APP_ENV)."
    )

    def handle(self, *args, **options):
        """FR-68, FR-72, AD-14, AD-16: guard, load, check, then write everything at once."""
        require_local_env(os.environ.get("APP_ENV"), settings.APP_ENV)
        seed = load_seed(SEED_PATH)
        households = [
            [
                NewGuest(
                    name=guest["name"],
                    phone=guest.get("phone", ""),
                    email=guest.get("email", ""),
                    code=guest["code"],
                )
                for guest in household["guests"]
            ]
            for household in seed["households"]
        ]
        deadline = timezone.localdate() + datetime.timedelta(
            days=seed["settings"]["deadline_days_from_today"]
        )
        values = settings_values(seed["settings"], deadline)

        with transaction.atomic():
            conflicts = test_data_conflicts(
                [guest.code for guests in households for guest in guests],
                [user["username"] for user in seed["users"]],
            )
            if conflicts:
                raise CommandError(
                    "Testdata ble ikke lagt inn fordi dette allerede brukes av data som ikke er "
                    f"testdata: {', '.join(conflicts)}. {NOTHING_CHANGED}"
                )
            try:
                reset_test_data(SYSTEM)
                update_settings(SYSTEM, values)
                for guests in households:
                    create_household(SYSTEM, guests)
                for user in seed["users"]:
                    create_admin_user(SYSTEM, user["username"], user["password"], user["role"])
            except ServiceError as error:
                raise CommandError(
                    f"Testdata ble ikke lagt inn: {error.message} {NOTHING_CHANGED}"
                ) from error

        self.print_summary(households, seed["users"], deadline)

    def print_summary(self, households, users, deadline):
        """FR-68: a test link per guest and the test logins, ready to copy."""
        out = self.stdout
        out.write(self.style.SUCCESS("Testdata er lagt inn."))
        out.write(f"Svarfrist: {deadline.isoformat()}")
        out.write("")
        out.write("Testlenker (start appen med `uv run manage.py runserver` først):")
        width = max(len(guest.name) for guests in households for guest in guests)
        for guests in households:
            for guest in guests:
                out.write(f"  {guest.name.ljust(width)}  {LOCAL_URL}/{guest.code}/")
            out.write("")
        out.write("Testbrukere (innlogging under /admin/):")
        for user in users:
            out.write(f"  {user['username']} / {user['password']} ({ROLE_NAMES[user['role']]})")


def require_local_env(environ_value: str | None, settings_value: str) -> None:
    """FR-72, AD-14: raise `CommandError` unless `APP_ENV` is unset (or empty) or `local`.

    Settings already refuse to start with a misspelled value, so the environment
    is read again here as well: an allow list, so `prod` or `Local` never passes.
    """
    try:
        app_env = validate_app_env(environ_value)
    except ImproperlyConfigured:
        app_env = None
    if app_env != "local" or settings_value != "local":
        shown = environ_value if environ_value is not None else settings_value
        raise CommandError(
            f"seed_testdata kjører bare når APP_ENV ikke er satt eller er «local», men "
            f"APP_ENV er «{shown}». Testdata skal aldri inn på den ekte nettsiden. "
            f"{NOTHING_CHANGED}"
        )


def load_seed(path: Path) -> dict:
    """AD-16: read the seed data with `tomllib`, or raise `CommandError`."""
    try:
        with path.open("rb") as file:
            return tomllib.load(file)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise CommandError(f"Fant ikke eller kunne ikke lese {path}: {error}") from error


def settings_values(seed_settings: dict, deadline: datetime.date) -> SettingsValues:
    """FR-68, AD-16: the settings from `seed.toml`, with the deadline already worked out."""
    return SettingsValues(
        contact_1_name=seed_settings["contact_1_name"],
        contact_1_phone=seed_settings["contact_1_phone"],
        contact_2_name=seed_settings["contact_2_name"],
        contact_2_phone=seed_settings["contact_2_phone"],
        price_cabin_weekend=seed_settings["price_cabin_weekend"],
        price_friday_dinner=seed_settings["price_friday_dinner"],
        price_saturday_breakfast=seed_settings["price_saturday_breakfast"],
        price_sunday_breakfast=seed_settings["price_sunday_breakfast"],
        rsvp_deadline=deadline,
        vipps_number=seed_settings["vipps_number"],
        account_number=seed_settings["account_number"],
    )
