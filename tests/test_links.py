"""Personal link codes and the one resolver (FR-1, FR-2, FR-3, AD-6).

FR-3 is tested here at the resolver, because no guest view exists until Story 1.5;
Story 1.5 repeats the test over an HTTP GET. Rows are set up directly in the tests,
so the resolver is tested on its own.
"""

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from wedding.actors import GuestActor
from wedding.links import CODE_LENGTH, is_code_format, new_code, resolve_code
from wedding.models import Guest, Household, Settings, User

VALID_UNKNOWN_CODE = "A" * 21 + "_"


def make_household(*names):
    household = Household.objects.create()
    guests = [Guest.objects.create(household=household, name=n, code=new_code()) for n in names]
    return household, guests


def row_counts():
    return {model.__name__: model.objects.count() for model in (Household, Guest, Settings, User)}


def test_new_code_is_22_url_safe_characters():
    """FR-1, AD-6: `token_urlsafe(16)` gives 22 characters from `[A-Za-z0-9_-]`."""
    for _ in range(200):
        code = new_code()
        assert len(code) == CODE_LENGTH == 22
        assert is_code_format(code)


def test_the_guest_code_field_holds_exactly_one_code():
    """AD-6: the model's column width and the code length agree, and the code is unique."""
    field = Guest._meta.get_field("code")
    assert field.max_length == CODE_LENGTH
    assert field.unique


@pytest.mark.parametrize(
    "code",
    [
        "A" * 21,  # one too short
        "A" * 23,  # one too long
        "",
        "A" * 21 + "+",  # standard base64, not URL-safe
        "A" * 21 + "/",
        "A" * 21 + "=",
        "A" * 21 + "\n",
        "Æ" + "A" * 21,
        None,
    ],
)
@pytest.mark.django_db
def test_a_code_in_the_wrong_format_resolves_to_none_without_a_query(code):
    """AD-6, NFR-4: a malformed code never reaches the database."""
    assert not is_code_format(code)
    with CaptureQueriesContext(connection) as queries:
        assert resolve_code(code) is None
    assert queries.captured_queries == []


@pytest.mark.django_db
def test_a_known_code_resolves_to_the_guest_and_their_household():
    """FR-1, AD-6: a known code gives a guest actor with the guest and the household."""
    household, (sigmund, _bestemor) = make_household("Sigmund", "Bestemor")

    actor = resolve_code(sigmund.code)

    assert actor == GuestActor(guest=sigmund, household=household)
    assert actor.guest.name == "Sigmund"


@pytest.mark.django_db
def test_an_unknown_code_in_the_right_format_resolves_to_none():
    """FR-1, AD-6: a well-formed code that matches no guest gives nothing."""
    make_household("Sigmund")
    assert is_code_format(VALID_UNKNOWN_CODE)
    assert resolve_code(VALID_UNKNOWN_CODE) is None


@pytest.mark.django_db
def test_a_code_that_differs_only_in_letter_case_resolves_to_none():
    """AD-6, NFR-4: codes are matched exactly, so case changes do not open a link."""
    _household, (sigmund,) = make_household("Sigmund")
    sigmund.code = "abcdefghijklmnopqrstuv"
    sigmund.save()

    assert resolve_code("ABCDEFGHIJKLMNOPQRSTUV") is None
    assert resolve_code("abcdefghijklmnopqrstuv").guest == sigmund


@pytest.mark.django_db
def test_the_actor_of_household_1_exposes_no_guest_of_household_2():
    """FR-2: nothing reachable from the actor belongs to another household."""
    first, first_guests = make_household("Sigmund", "Bestemor")
    second, second_guests = make_household("Kari", "Ola")

    actor = resolve_code(first_guests[0].code)

    assert actor.household == first
    assert actor.guest.household_id == first.pk
    assert list(actor.household.guests.all()) == first_guests
    reachable = {guest.pk for guest in actor.household.guests.all()} | {actor.guest.pk}
    assert reachable.isdisjoint({guest.pk for guest in second_guests})
    assert actor.household != second


@pytest.mark.django_db
def test_resolving_a_code_only_reads_and_changes_no_rows():
    """FR-3: resolving a link runs SELECT queries only and creates or changes nothing."""
    _household, (sigmund,) = make_household("Sigmund")
    before = row_counts()
    revision_before = Household.objects.get().revision

    with CaptureQueriesContext(connection) as queries:
        resolve_code(sigmund.code)
        resolve_code(VALID_UNKNOWN_CODE)

    assert len(queries.captured_queries) == 2  # one lookup each, household joined in
    assert all(q["sql"].lstrip().upper().startswith("SELECT") for q in queries.captured_queries)
    assert row_counts() == before
    assert Household.objects.get().revision == revision_before
