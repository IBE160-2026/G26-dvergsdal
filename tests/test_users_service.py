"""The `create_admin_user` service (FR-47, FR-72, AD-3, AD-10, AD-16).

For now only the system actor (the seed command) creates admin accounts, and the
accounts it creates are test data. Every refusal writes nothing.
"""

import pytest

from wedding.actors import SYSTEM, AdminActor, GuestActor
from wedding.models import User
from wedding.services.exceptions import InvalidUser, NotAllowed
from wedding.services.households import NewGuest, create_household
from wedding.services.users import create_admin_user

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
