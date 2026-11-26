"""Creating admin accounts for the couple and the helpers (FR-47, AD-10).

There is no self-registration: accounts are made by a command. The seed command
makes test accounts with the system actor (`create_admin_user`, FR-72, AD-16); the
`create_admin` command makes real ones with the operator actor
(`create_admin_account`, Story 3.1). Both share one validator.
"""

from django.core.exceptions import ValidationError
from django.db import transaction

from wedding.actors import Actor, OperatorActor, SystemActor
from wedding.models import User
from wedding.services.exceptions import InvalidUser, NotAllowed

USERNAME_MAX_LENGTH = User._meta.get_field("username").max_length


def create_admin_user(actor: Actor, username: str, password: str, role: str) -> User:
    """FR-47, FR-72, AD-3, AD-10, AD-16: create a couple or helper account.

    Only the system actor may create one, and an account it creates is test data;
    the seed command is its only caller. Real accounts go through
    `create_admin_account`. The password is stored hashed. A refusal
    raises `NotAllowed` or `InvalidUser` with nothing written.
    """
    with transaction.atomic():
        if not isinstance(actor, SystemActor):
            raise NotAllowed()
        _validate_user(username, password, role)
        return User.objects.create_user(
            username=username,
            password=password,
            role=role,
            is_test_data=True,  # only the system actor gets this far
        )


def create_admin_account(actor: Actor, username: str, password: str, role: str) -> User:
    """FR-47, AD-3, AD-10, AD-16: create a real couple or helper account (Story 3.1).

    Only the operator actor, the person running `create_admin`, may create one,
    and the account is not test data, so the seed never removes it. The password
    is stored hashed. A refusal raises `NotAllowed` or `InvalidUser` with nothing
    written.
    """
    with transaction.atomic():
        if not isinstance(actor, OperatorActor):
            raise NotAllowed()
        _validate_user(username, password, role)
        return User.objects.create_user(
            username=username,
            password=password,
            role=role,
            is_test_data=False,  # a real account the seed must leave alone
        )


def check_new_admin(username: str, role: str) -> None:
    """FR-47, AD-10: raise `InvalidUser` unless `username` and `role` can make an account.

    The command asks this before it prompts for a password, so a taken username or
    a wrong role is refused first.
    """
    if not username:
        raise InvalidUser("Brukernavnet kan ikke være tomt.")
    if len(username) > USERNAME_MAX_LENGTH:
        raise InvalidUser(f"Et brukernavn kan ha høyst {USERNAME_MAX_LENGTH} tegn.")
    try:
        User.username_validator(username)
    except ValidationError:
        raise InvalidUser(
            f"«{username}» kan bare ha bokstaver, tall og tegnene @ . + - _."
        ) from None
    if role not in User.Role.values:
        raise InvalidUser(f"«{role}» er ikke en rolle. Bruk «couple» eller «helper».")
    if User.objects.filter(username=username).exists():
        raise InvalidUser(f"Brukernavnet «{username}» er allerede i bruk.")


def _validate_user(username: str, password: str, role: str) -> None:
    """FR-47, AD-10: raise `InvalidUser` for the first problem found."""
    check_new_admin(username, role)
    if not password:
        raise InvalidUser("Passordet kan ikke være tomt.")
