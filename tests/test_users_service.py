"""The `create_admin_user` and `create_admin_account` services (FR-47, FR-72, AD-3, AD-10, AD-16).

The system actor (the seed command) creates test accounts; the operator actor (the
`create_admin` command, Story 3.1) creates real ones. Every refusal writes nothing.
"""

import pytest
from django.db import IntegrityError

from tests.helpers import make_admin
from wedding.actors import OPERATOR, SYSTEM, AdminActor, GuestActor
from wedding.models import User
from wedding.services.exceptions import InvalidUser, NotAllowed
from wedding.services.households import NewGuest, create_household
from wedding.services.permissions import require_couple
from wedding.services.users import create_admin_account, create_admin_user

PASSWORD = "bryllup-test-2028"


@pytest.mark.django_db
@pytest.mark.parametrize("role", [User.Role.COUPLE, User.Role.HELPER])
def test_the_system_actor_creates_a_test_account_with_a_hashed_password(role):
    """FR-47, FR-72, AD-16: the account has its role, is test data and can log in."""
    user = create_admin_user(SYSTEM, "testpar", PASSWORD, role)

    user.refresh_from_db()
    assert (user.username, user.role, user.is_test_data) == ("testpar", role, True)
    assert user.password != PASSWORD
    assert user.check_password(PASSWORD)


@pytest.mark.django_db
@pytest.mark.parametrize("role", [User.Role.COUPLE, User.Role.HELPER])
def test_an_admin_cannot_create_an_account_yet(role):
    """FR-47, AD-10: accounts come from a command, never from the admin pages."""
    actor = AdminActor(User.objects.create_user(username="rikke", role=role))

    with pytest.raises(NotAllowed):
        create_admin_user(actor, "testhjelper", PASSWORD, User.Role.HELPER)
    assert list(User.objects.values_list("username", flat=True)) == ["rikke"]


@pytest.mark.django_db
def test_a_guest_cannot_create_an_account():
    """AD-3, AD-10: a guest actor is neither the system nor an admin."""
    household = create_household(SYSTEM, [NewGuest("Sigmund")])
    actor = GuestActor(guest=household.guests.get(), household=household)

    with pytest.raises(NotAllowed):
        create_admin_user(actor, "testpar", PASSWORD, User.Role.COUPLE)
    assert User.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("username", "password", "role", "message"),
    [
        ("", PASSWORD, "couple", "Brukernavnet kan ikke være tomt."),
        ("x" * 151, PASSWORD, "couple", "Et brukernavn kan ha høyst 150 tegn."),
        (
            "test par",
            PASSWORD,
            "couple",
            "«test par» kan bare ha bokstaver, tall og tegnene @ . + - _.",
        ),
        ("testpar", PASSWORD, "admin", "«admin» er ikke en rolle. Bruk «couple» eller «helper»."),
        ("testpar", "", "couple", "Passordet kan ikke være tomt."),
    ],
)
def test_an_invalid_account_is_refused_and_nothing_is_written(username, password, role, message):
    """FR-47, AD-10: a blank, too long or malformed username, an unknown role or no password."""
    with pytest.raises(InvalidUser) as refused:
        create_admin_user(SYSTEM, username, password, role)

    assert refused.value.message == message
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_a_taken_username_is_refused():
    """FR-47: two accounts cannot share a username, and the existing one is untouched."""
    User.objects.create_user(username="testpar", role=User.Role.HELPER)

    with pytest.raises(InvalidUser) as refused:
        create_admin_user(SYSTEM, "testpar", PASSWORD, User.Role.COUPLE)

    assert refused.value.message == "Brukernavnet «testpar» er allerede i bruk."
    user = User.objects.get()
    assert (user.role, user.is_test_data) == (User.Role.HELPER, False)


# Story 3.1: the real accounts the `create_admin` command makes (FR-47, AD-3, AD-10, AD-16)


@pytest.mark.django_db
@pytest.mark.parametrize("role", [User.Role.COUPLE, User.Role.HELPER])
def test_the_operator_creates_a_real_account_with_a_hashed_password(role):
    """FR-47, AD-16: not test data, the role set deliberately, the password hashed."""
    user = create_admin_account(OPERATOR, "rikke", PASSWORD, role)

    user.refresh_from_db()
    assert (user.username, user.role, user.is_test_data) == ("rikke", role, False)
    assert user.password != PASSWORD
    assert user.check_password(PASSWORD)


@pytest.mark.django_db
def test_only_the_operator_creates_a_real_account():
    """AD-3, AD-10: the system, an admin and a guest actor are refused, nothing written."""
    household = create_household(SYSTEM, [NewGuest("Sigmund")])
    guest = GuestActor(guest=household.guests.get(), household=household)
    for actor in (SYSTEM, make_admin(User.Role.COUPLE, "par"), guest):
        with pytest.raises(NotAllowed):
            create_admin_account(actor, "rikke", PASSWORD, User.Role.COUPLE)
    assert list(User.objects.values_list("username", flat=True)) == ["par"]


@pytest.mark.django_db
def test_the_operator_cannot_create_a_test_account():
    """AD-16: `create_admin_user` stays the seed's, so a real caller cannot make test data."""
    with pytest.raises(NotAllowed):
        create_admin_user(OPERATOR, "testpar", PASSWORD, User.Role.COUPLE)
    assert User.objects.count() == 0


def test_the_operator_cannot_write_through_the_admin_services():
    """AD-10: `require_couple` refuses the operator, so it cannot change settings or households."""
    with pytest.raises(NotAllowed):
        require_couple(OPERATOR)


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["", "admin", "Couple"])
def test_a_real_account_with_an_invalid_role_is_refused(role):
    """FR-47, AD-10: only `couple` and `helper`; nothing is written."""
    with pytest.raises(InvalidUser):
        create_admin_account(OPERATOR, "rikke", PASSWORD, role)
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_a_real_account_with_a_taken_username_is_refused():
    """FR-47: the existing account is untouched."""
    User.objects.create_user(username="rikke", role=User.Role.HELPER)

    with pytest.raises(InvalidUser) as refused:
        create_admin_account(OPERATOR, "rikke", PASSWORD, User.Role.COUPLE)

    assert refused.value.message == "Brukernavnet «rikke» er allerede i bruk."
    assert User.objects.get().role == User.Role.HELPER


@pytest.mark.django_db(transaction=True)
def test_the_database_refuses_a_blank_or_unknown_role():
    """AD-10 (Story 3.1): the check constraint stops a row written outside the services."""
    for role in ("", "admin"):
        with pytest.raises(IntegrityError):
            User.objects.create_user(username="rikke", role=role)
    assert User.objects.count() == 0
