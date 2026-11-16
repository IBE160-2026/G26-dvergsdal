"""Creating households and their guests (FR-1, FR-49, AD-3, AD-6).

The couple will create households from the admin pages (Story 6.4) and the seed
command with the system actor (Story 1.3). Only the seed command may give a guest
a fixed link code; everyone else gets a fresh one from `wedding.links.new_code()`.
"""

from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction

from wedding.actors import SystemActor
from wedding.links import is_code_format, new_code
from wedding.models import PHONE_MAX_LENGTH, Guest, Household
from wedding.rules.households import household_size_problem
from wedding.services.exceptions import InvalidHousehold
from wedding.services.permissions import require_couple

NAME_MAX_LENGTH = Guest._meta.get_field("name").max_length


@dataclass(frozen=True)
class NewGuest:
    """One person to add to a new household; `code` is for the seed command only."""

    name: str
    phone: str = ""
    email: str = ""
    code: str | None = None


def create_household(actor: object, guests: list[NewGuest]) -> Household:
    """FR-1, FR-49, AD-3, AD-6, AD-8, AD-9: create a household with 1 to 8 guests.

    Only the system actor or a couple account may create one (AD-10). Each guest
    gets a fresh, unique link code, except that the system actor may set a fixed
    code in the same 22-character format. The household starts at revision 0.
    Everything is written in one transaction, and a refusal raises `NotAllowed` or
    `InvalidHousehold` with nothing written.
    """
    with transaction.atomic():
        is_system = isinstance(actor, SystemActor)
        if not is_system:
            require_couple(actor)
        _validate_guests(guests, fixed_codes_allowed=is_system)
        fixed_codes = [guest.code for guest in guests if guest.code is not None]
        if Guest.objects.filter(code__in=fixed_codes).exists():
            raise InvalidHousehold("Lenkekoden er allerede i bruk.")
        household = Household.objects.create()
        for guest in guests:
            Guest.objects.create(
                household=household,
                name=guest.name.strip(),
                phone=guest.phone.strip(),
                email=guest.email.strip(),
                code=guest.code if guest.code is not None else new_code(),
            )
    return household


def _validate_guests(guests: list[NewGuest], *, fixed_codes_allowed: bool) -> None:
    """FR-49, AD-6, AD-8: raise `InvalidHousehold` for the first problem found.

    `objects.create` runs no validators and SQLite ignores `max_length`, so names,
    phones and emails are checked here.
    """
    problem = household_size_problem(len(guests))
    if problem:
        raise InvalidHousehold(problem)
    for guest in guests:
        name = guest.name.strip()
        if not name:
            raise InvalidHousehold("Hver person må ha et navn.")
        if len(name) > NAME_MAX_LENGTH:
            raise InvalidHousehold(f"Et navn kan ha høyst {NAME_MAX_LENGTH} tegn.")
        if len(guest.phone.strip()) > PHONE_MAX_LENGTH:
            raise InvalidHousehold(f"Et telefonnummer kan ha høyst {PHONE_MAX_LENGTH} tegn.")
        email = guest.email.strip()
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise InvalidHousehold(f"«{email}» er ikke en gyldig e-postadresse.") from None
    fixed_codes = [guest.code for guest in guests if guest.code is not None]
    if fixed_codes and not fixed_codes_allowed:
        raise InvalidHousehold("Bare testdata kan ha faste lenkekoder.")
    if not all(is_code_format(code) for code in fixed_codes):
        raise InvalidHousehold("En fast lenkekode må ha 22 tegn: bokstaver, tall, - eller _.")
    if len(set(fixed_codes)) != len(fixed_codes):
        raise InvalidHousehold("To personer kan ikke ha samme lenkekode.")
