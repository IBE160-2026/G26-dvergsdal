"""`uv run manage.py seed_testdata`: fill the database with fictional test data (FR-68).

Reads `wedding/fixtures/seed.toml` and builds the settings, the households with
their guests and the two test admin accounts through services with the system
actor (AD-3, AD-16). It runs only with `APP_ENV` unset or `local` (FR-72, AD-14),
stops without writing if a seed code or username belongs to data it did not make,
and replaces its own earlier test data, so every run gives the same result.
The one `Settings` row is replaced every run as well, on purpose: the deadline
must be 30 days from today so the form is open (epics 1.3). The help text and
the printout say so.

Story 1.3 loads settings, users, households and the guests' name, phone, email
and code. Story 2.6d sends each answered household's answer, allergies and
consents through `send_answer` with the system actor (FR-68, AD-3, AD-16); the
withdrawn consent and the payments are loaded by Stories 7.2 and 5.2.
"""

import datetime
import os
import tomllib
import uuid
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from config.env import validate_app_env
from wedding.actors import SYSTEM
from wedding.models import Household
from wedding.rules.allergies import AllergyEntry
from wedding.rules.answer import Answer
from wedding.rules.days import WHOLE_WEEKEND
from wedding.rules.money import household_total
from wedding.selectors import form_prices, seed_conflicts, site_settings
from wedding.services.answers import send_answer
from wedding.services.consent import CONSENT_TEXT_VERSION
from wedding.services.exceptions import ServiceError
from wedding.services.households import NewGuest, create_household
from wedding.services.settings import SettingsValues, update_settings
from wedding.services.testdata import reset_test_data
from wedding.services.users import create_admin_user

SEED_PATH = Path(__file__).resolve().parents[2] / "fixtures" / "seed.toml"
LOCAL_URL = "http://127.0.0.1:8000"
ROLE_NAMES = {"couple": "brudeparet", "helper": "hjelper"}
NOTHING_CHANGED = "Ingenting ble endret."
SETTINGS_REPLACED = "Innstillingene er erstattet med testverdiene fra seed.toml."


class Command(BaseCommand):
    help = (
        "Fyller databasen med fiktive testdata fra wedding/fixtures/seed.toml og skriver ut "
        "en testlenke per gjest. Erstatter testdata fra forrige kjøring, og erstatter alltid "
        "innstillingene med testverdiene (svarfrist 30 dager fra i dag). Kjører bare med "
        "APP_ENV=local (eller uten APP_ENV)."
    )

    def handle(self, *args, **options):
        """FR-68, FR-72, AD-3, AD-14, AD-16: guard, load, check, then write everything at once.

        Story 2.6d: after the households and users, each answered household's
        answer is sent through `send_answer` with the system actor.
        """
        require_local_env(os.environ.get("APP_ENV"), settings.APP_ENV)
        seed = load_seed(SEED_PATH)
        check_consent_by(seed["households"])
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
            conflicts = seed_conflicts(
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
                created = [create_household(SYSTEM, guests) for guests in households]
                for user in seed["users"]:
                    create_admin_user(SYSTEM, user["username"], user["password"], user["role"])
                for household_seed, household in zip(seed["households"], created, strict=True):
                    send_seed_answer(household_seed, household)
            except ServiceError as error:
                raise CommandError(
                    f"Testdata ble ikke lagt inn: {error.message} {NOTHING_CHANGED}"
                ) from error

        self.print_summary(households, seed["users"], deadline)

    def print_summary(self, households, users, deadline):
        """FR-68: a test link per guest and the test logins, ready to copy."""
        out = self.stdout
        out.write(self.style.SUCCESS("Testdata er lagt inn."))
        out.write(SETTINGS_REPLACED)
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
        shown = environ_value if app_env != "local" else settings_value
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


def check_consent_by(households: list[dict]) -> None:
    """FR-29, AD-16: raise `CommandError` unless every `consent_by` is the household's
    `answered_by`, since the respondent records every consent. Runs before any write."""
    for household in households:
        for guest in household["guests"]:
            given_by = guest.get("consent_by")
            if given_by is not None and given_by != household.get("answered_by"):
                raise CommandError(
                    f"Testdata ble ikke lagt inn: samtykket for «{guest['key']}» er gitt av "
                    f"«{given_by}», men husstanden er besvart av "
                    f"«{household.get('answered_by')}». {NOTHING_CHANGED}"
                )


def seed_answer(household_seed: dict, ids: dict[str, int]) -> tuple[int, Answer]:
    """FR-13 to FR-17, FR-25 to FR-29, FR-68, AD-2: the respondent's guest id and the
    `Answer` a seed household describes, with `ids` mapping guest keys to guest ids.

    `whole` is True when every coming guest comes all three days; otherwise every
    coming guest's days are set. A consent recorded by someone other than the guest
    puts the guest in `confirmed` (FR-27). `consent_withdrawn` is left to Story 7.2.
    """
    guests = household_seed["guests"]
    coming = [guest for guest in guests if guest["coming"]]
    whole = all(frozenset(guest["days"]) == WHOLE_WEEKEND for guest in coming)
    answer = Answer(
        attendance={ids[g["key"]]: g["coming"] for g in guests},
        whole=whole,
        days={} if whole else {ids[g["key"]]: tuple(g["days"]) for g in coming},
        night={ids[g["key"]]: g["overnight"] for g in coming},
        meals={ids[g["key"]]: tuple(g["meals"]) for g in coming},
        hike={ids[g["key"]]: g["hike"] for g in coming if "hike" in g},
        allergies={
            ids[g["key"]]: AllergyEntry(
                cats=tuple(g.get("allergy_categories", ())),
                none=g.get("no_allergies", False),
                note=g.get("allergy_note", ""),
            )
            for g in coming
        },
        consent={ids[g["key"]]: g["consent"] == "yes" for g in coming if "consent" in g},
        confirmed=frozenset(
            ids[g["key"]] for g in coming if g.get("consent_by", g["key"]) != g["key"]
        ),
    )
    return ids[household_seed["answered_by"]], answer


def send_seed_answer(household_seed: dict, household: Household) -> None:
    """FR-68, AD-3, AD-16: send a seed household's answer as the system actor, if it has one."""
    if "answered_by" not in household_seed:
        return
    codes = {guest.code: guest.pk for guest in household.guests.all()}
    ids = {guest["key"]: codes[guest["code"]] for guest in household_seed["guests"]}
    respondent, answer = seed_answer(household_seed, ids)
    send_answer(
        SYSTEM,
        household=household,
        respondent=respondent,
        answer=answer,
        now=timezone.now(),
        submission=uuid.uuid4(),
        revision=household.revision,
        shown_total=household_total(answer, form_prices(site_settings())),
        consent_version=CONSENT_TEXT_VERSION,
    )


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
