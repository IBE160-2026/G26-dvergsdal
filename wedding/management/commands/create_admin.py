"""`uv run manage.py create_admin <username> --role couple|helper`: make a real account (FR-47).

The only way to make an account for the couple or a helper: there is no
self-registration, no Django admin site and no `createsuperuser` (AD-10). The
password is asked for twice with `getpass`, never taken as an argument or from
the environment, and checked with Django's password validators. The account is
made through `create_admin_account` with the operator actor (AD-3), is not test
data (AD-16) and so survives `seed_testdata`. Story 3.1.
"""

from getpass import getpass

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from wedding.actors import OPERATOR
from wedding.models import User
from wedding.services.exceptions import ServiceError
from wedding.services.users import check_new_admin, create_admin_account

ROLE_NAMES = {"couple": "brudeparet", "helper": "hjelper"}


class Command(BaseCommand):
    help = (
        "Lager en ekte konto for brudeparet eller en hjelper. Spør om passordet to ganger. "
        "Kontoen er ikke testdata og blir stående når seed_testdata kjøres."
    )

    def add_arguments(self, parser):
        parser.add_argument("username", help="brukernavnet, for eksempel rikke")
        parser.add_argument(
            "--role",
            required=True,
            choices=list(User.Role.values),
            help="couple (brudeparet, kan endre) eller helper (hjelper, kan bare se)",
        )

    def handle(self, *args, **options):
        """FR-47, AD-3, AD-10: check the username and role, ask for the password twice,
        validate it, then create the account. A refusal writes nothing."""
        username = options["username"]
        role = options["role"]
        try:
            check_new_admin(username, role)
        except ServiceError as error:
            raise CommandError(error.message) from error
        password = self.ask_for_password(username)
        try:
            create_admin_account(OPERATOR, username, password, role)
        except ServiceError as error:
            raise CommandError(error.message) from error
        self.stdout.write(self.style.SUCCESS(f"Opprettet {username} ({ROLE_NAMES[role]})."))

    def ask_for_password(self, username: str) -> str:
        """FR-47: the password typed twice and accepted by `validate_password`."""
        password = getpass("Passord: ")
        if getpass("Passord (en gang til): ") != password:
            raise CommandError("Passordene er ikke like. Ingenting ble lagret.")
        try:
            validate_password(password, User(username=username))
        except ValidationError as error:
            raise CommandError(
                f"Passordet er ikke godt nok: {' '.join(error.messages)} Ingenting ble lagret."
            ) from error
        return password
