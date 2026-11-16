"""Households and guests: the size rule and the `create_household` service.

Covers FR-1 (fresh unguessable codes), FR-49 and AD-8 (1 to 8 people), AD-3 (one
transaction with an explicit actor), AD-6 (fixed codes for the seed command only),
AD-9 (revision starts at 0) and AD-10 (helpers cannot write).
"""

import pytest
from django.db import IntegrityError

from wedding.actors import SYSTEM, AdminActor, GuestActor
from wedding.links import is_code_format
from wedding.models import Guest, Household, User
from wedding.rules.households import MAX_HOUSEHOLD_SIZE, household_size_problem
from wedding.services.exceptions import InvalidHousehold, NotAllowed, ServiceError
from wedding.services.households import NewGuest, create_household
from wedding.services.permissions import require_couple

FIXED_CODE = "Fixed_code-for-seed-01"


def make_admin(role, username="rikke"):
    return AdminActor(User.objects.create_user(username=username, role=role))


def names(count):
    return [NewGuest(name=f"Gjest {n}") for n in range(1, count + 1)]


def assert_nothing_written():
    assert Household.objects.count() == 0
    assert Guest.objects.count() == 0


# The rule


def test_the_cap_is_8():
    """AD-8: Rikke confirmed 8 as the largest household; the 4 KB draft test relies on it."""
    assert MAX_HOUSEHOLD_SIZE == 8


@pytest.mark.parametrize("count", [1, 8])
def test_1_to_8_people_is_a_valid_household(count):
    """FR-49, AD-8: both bounds are allowed."""
    assert household_size_problem(count) is None


@pytest.mark.parametrize(
    ("count", "message"),
    [
        (0, "En husstand må ha minst én person."),
        (9, "En husstand kan ha høyst 8 personer."),
    ],
)
def test_0_or_9_people_is_refused_with_a_norwegian_message(count, message):
    """FR-49, AD-8: just outside the bounds gives a message the couple can read."""
    assert household_size_problem(count) == message


# Who may create a household


@pytest.mark.django_db
@pytest.mark.parametrize("count", [1, 8])
def test_the_couple_creates_a_household_at_revision_0_with_fresh_codes(count):
    """FR-1, FR-49, AD-6, AD-9: 1 to 8 guests, each with its own new code."""
    household = create_household(make_admin(User.Role.COUPLE), names(count))

    assert household.revision == 0
    guests = list(household.guests.all())
    assert [guest.name for guest in guests] == [f"Gjest {n}" for n in range(1, count + 1)]
    codes = [guest.code for guest in guests]
    assert all(is_code_format(code) for code in codes)
    assert len(set(codes)) == count


@pytest.mark.django_db
def test_the_system_actor_creates_a_household():
    """AD-3, AD-16: the seed command creates households with the system actor."""
    household = create_household(SYSTEM, [NewGuest("Sigmund"), NewGuest("Bestemor")])
    assert household.guests.count() == 2


@pytest.mark.django_db
def test_phone_and_email_are_stored_and_names_trimmed():
    """FR-49: name, optional phone and optional email are stored without edge spaces."""
    create_household(
        SYSTEM,
        [
            NewGuest("  Sigmund ", phone=" 00000000 ", email=" sigmund@example.com "),
            NewGuest("Kari"),
        ],
    )

    sigmund, kari = Guest.objects.all()
    assert (sigmund.name, sigmund.phone, sigmund.email) == (
        "Sigmund",
        "00000000",
        "sigmund@example.com",
    )
    assert (kari.phone, kari.email) == ("", "")


@pytest.mark.django_db
def test_codes_are_distinct_across_50_guests():
    """FR-1, AD-6: every guest gets a different code."""
    actor = make_admin(User.Role.COUPLE)
    for _ in range(10):
        create_household(actor, names(5))

    codes = list(Guest.objects.values_list("code", flat=True))
    assert len(codes) == 50
    assert len(set(codes)) == 50


@pytest.mark.django_db
def test_a_helper_cannot_create_a_household():
    """AD-10, FR-46: a helper's write is refused in the service and writes nothing."""
    with pytest.raises(NotAllowed) as refused:
        create_household(make_admin(User.Role.HELPER), names(2))

    assert refused.value.message == "Du har ikke lov til å gjøre denne endringen."
    assert_nothing_written()


@pytest.mark.django_db
def test_a_guest_cannot_create_a_household():
    """AD-3, AD-10: a guest actor is neither the system nor the couple."""
    household = create_household(SYSTEM, [NewGuest("Sigmund")])
    guest = household.guests.get()

    with pytest.raises(NotAllowed):
        create_household(GuestActor(guest=guest, household=household), names(1))
    assert Household.objects.count() == 1


@pytest.mark.parametrize("actor", [None, SYSTEM, "couple"])
def test_require_couple_refuses_anything_but_a_couple_account(actor):
    """AD-10: only an `AdminActor` with the couple role passes the check."""
    with pytest.raises(NotAllowed):
        require_couple(actor)


@pytest.mark.django_db
def test_require_couple_lets_the_couple_through():
    """AD-10: the couple passes the one role check."""
    require_couple(make_admin(User.Role.COUPLE))


# Invalid households


@pytest.mark.django_db
@pytest.mark.parametrize("use_system", [True, False])
@pytest.mark.parametrize(
    ("guests", "message"),
    [
        ([], "En husstand må ha minst én person."),
        (names(9), "En husstand kan ha høyst 8 personer."),
        ([NewGuest("Sigmund"), NewGuest("")], "Hver person må ha et navn."),
        ([NewGuest("   ")], "Hver person må ha et navn."),
        ([NewGuest("x" * 101)], "Et navn kan ha høyst 100 tegn."),
    ],
)
def test_an_invalid_household_is_refused_and_nothing_is_written(guests, message, use_system):
    """FR-49, AD-8: 0 or 9 guests, a blank name or a too-long name writes nothing."""
    actor = SYSTEM if use_system else make_admin(User.Role.COUPLE)

    with pytest.raises(InvalidHousehold) as refused:
        create_household(actor, guests)

    assert refused.value.message == message
    assert isinstance(refused.value, ServiceError)
    assert_nothing_written()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("guest", "message"),
    [
        (NewGuest("Sigmund", phone="1" * 31), "Et telefonnummer kan ha høyst 30 tegn."),
        (
            NewGuest("Sigmund", email=" sigmund.example.com "),
            "«sigmund.example.com» er ikke en gyldig e-postadresse.",
        ),
    ],
)
def test_a_too_long_phone_or_a_malformed_email_is_refused(guest, message):
    """FR-49: the service checks what `objects.create` and SQLite would store silently."""
    with pytest.raises(InvalidHousehold) as refused:
        create_household(SYSTEM, [guest])

    assert refused.value.message == message
    assert_nothing_written()


@pytest.mark.django_db
def test_a_30_character_phone_and_a_valid_email_are_allowed():
    """FR-49: the phone limit is inclusive, and a well-formed email passes."""
    create_household(SYSTEM, [NewGuest("Sigmund", phone="1" * 30, email="s@example.com")])

    guest = Guest.objects.get()
    assert (guest.phone, guest.email) == ("1" * 30, "s@example.com")


@pytest.mark.django_db
def test_a_100_character_name_is_allowed():
    """FR-49: the name limit is inclusive."""
    create_household(SYSTEM, [NewGuest("x" * 100)])
    assert Guest.objects.get().name == "x" * 100


# Fixed codes (seed command only)


@pytest.mark.django_db
def test_the_system_actor_can_set_a_fixed_code():
    """AD-6, AD-16: the seed command may give a guest a fixed code in the same format."""
    create_household(SYSTEM, [NewGuest("Sigmund", code=FIXED_CODE), NewGuest("Bestemor")])

    sigmund, bestemor = Guest.objects.all()
    assert sigmund.code == FIXED_CODE
    assert is_code_format(bestemor.code)
    assert bestemor.code != FIXED_CODE


@pytest.mark.django_db
def test_the_couple_cannot_set_a_fixed_code():
    """AD-6: only the seed command may choose a code."""
    with pytest.raises(InvalidHousehold) as refused:
        create_household(make_admin(User.Role.COUPLE), [NewGuest("Sigmund", code=FIXED_CODE)])

    assert refused.value.message == "Bare testdata kan ha faste lenkekoder."
    assert_nothing_written()


@pytest.mark.django_db
@pytest.mark.parametrize("code", ["", "too-short", FIXED_CODE + "x", FIXED_CODE[:-1] + "+"])
def test_a_badly_formed_fixed_code_is_refused(code):
    """AD-6: a fixed code must have the same 22-character format as a fresh one."""
    with pytest.raises(InvalidHousehold) as refused:
        create_household(SYSTEM, [NewGuest("Sigmund"), NewGuest("Bestemor", code=code)])

    assert refused.value.message == "En fast lenkekode må ha 22 tegn: bokstaver, tall, - eller _."
    assert_nothing_written()


@pytest.mark.django_db
def test_a_fixed_code_already_in_use_is_refused():
    """AD-6: a code opens exactly one guest, so a repeated fixed code writes nothing."""
    create_household(SYSTEM, [NewGuest("Sigmund", code=FIXED_CODE)])

    with pytest.raises(InvalidHousehold) as refused:
        create_household(SYSTEM, [NewGuest("Kari", code=FIXED_CODE)])

    assert refused.value.message == "Lenkekoden er allerede i bruk."
    assert Household.objects.count() == 1
    assert Guest.objects.count() == 1


@pytest.mark.django_db
def test_the_same_fixed_code_twice_in_one_household_is_refused():
    """AD-6: two guests in one call cannot share a fixed code."""
    with pytest.raises(InvalidHousehold) as refused:
        create_household(
            SYSTEM, [NewGuest("Sigmund", code=FIXED_CODE), NewGuest("Bestemor", code=FIXED_CODE)]
        )

    assert refused.value.message == "To personer kan ikke ha samme lenkekode."
    assert_nothing_written()


# One transaction


@pytest.mark.django_db
def test_a_failure_halfway_leaves_no_household_behind(monkeypatch):
    """AD-3: the service is one transaction, so a failing second guest undoes the first."""
    create_household(SYSTEM, [NewGuest("Sigmund", code=FIXED_CODE)])
    fresh_codes = iter(["Brand_new-code-for-k01", FIXED_CODE])  # the second one collides
    monkeypatch.setattr("wedding.services.households.new_code", lambda: next(fresh_codes))

    with pytest.raises(IntegrityError):
        create_household(SYSTEM, [NewGuest("Kari"), NewGuest("Ola")])

    assert Household.objects.count() == 1
    assert list(Guest.objects.values_list("name", flat=True)) == ["Sigmund"]
