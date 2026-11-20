"""The `seed_testdata` command, the reset service and the conflict check (Story 1.3).

Covers every row of the Story 1.3 I/O matrix: first run, second run, a taken code,
a taken username and a wrong `APP_ENV` (FR-68, FR-72, AD-14, AD-16). The
"Settings, helper" row is in `test_settings_service.py`. Only the loading is
tested here; the expected results are asserted by the stories that compute them.
"""

import datetime
import tomllib
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from wedding import selectors
from wedding.actors import SYSTEM, AdminActor
from wedding.models import Guest, Household, Settings, User
from wedding.services.exceptions import NotAllowed
from wedding.services.households import NewGuest, create_household
from wedding.services.testdata import reset_test_data

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
SEED_GUESTS = [guest for household in SEED["households"] for guest in household["guests"]]
SIGMUNDS_CODE = SEED_GUESTS[0]["code"]


def seed():
    """Run the command and return what it printed."""
    out = StringIO()
    call_command("seed_testdata", stdout=out)
    return out.getvalue()


def make_couple(username="rikke"):
    return AdminActor(User.objects.create_user(username=username, role=User.Role.COUPLE))


def snapshot():
    """Everything the command could write, to show that a refusal wrote nothing."""
    return (
        list(Household.objects.values_list("id", "is_test_data")),
        list(Guest.objects.values_list("id", "name", "code")),
        list(User.objects.values_list("id", "username", "is_test_data")),
        list(Settings.objects.values()),
    )


# The examiner's machine: no APP_ENV set (NFR-8); `local_env` is in conftest.py.
pytestmark = pytest.mark.usefixtures("local_env")


# First run


@pytest.mark.django_db
def test_first_run_creates_the_seed_households_and_guests_as_test_data():
    """FR-68, AD-16: 7 households and 14 guests with the names, contacts and codes in seed.toml."""
    seed()

    assert Household.objects.count() == len(SEED["households"]) == 7
    assert not Household.objects.filter(is_test_data=False).exists()
    stored = [
        [(g.name, g.phone, g.email, g.code) for g in household.guests.all()]
        for household in Household.objects.prefetch_related("guests")
    ]
    planned = [
        [
            (g["name"], g.get("phone", ""), g.get("email", ""), g["code"])
            for g in household["guests"]
        ]
        for household in SEED["households"]
    ]
    assert stored == planned
    assert Guest.objects.count() == 14


@pytest.mark.django_db
def test_first_run_sets_the_settings_with_the_deadline_30_days_from_today():
    """FR-68, AD-16: fictional prices and contacts, and a deadline that keeps the form open."""
    seed()

    row = Settings.objects.get()
    planned = SEED["settings"]
    for name in [
        "contact_1_name",
        "contact_1_phone",
        "contact_2_name",
        "contact_2_phone",
        "price_cabin_weekend",
        "price_friday_dinner",
        "price_saturday_breakfast",
        "price_sunday_breakfast",
        "vipps_number",
        "account_number",
    ]:
        assert getattr(row, name) == planned[name], name
    assert row.rsvp_deadline == timezone.localdate() + datetime.timedelta(days=30)


@pytest.mark.django_db
def test_first_run_creates_a_test_couple_and_a_test_helper():
    """FR-47, FR-68: `testpar` and `testhjelper`, with the password from seed.toml."""
    seed()

    users = {user.username: user for user in User.objects.all()}
    assert set(users) == {"testpar", "testhjelper"}
    assert users["testpar"].role == User.Role.COUPLE
    assert users["testhjelper"].role == User.Role.HELPER
    for user in users.values():
        assert user.is_test_data
        assert user.check_password("bryllup-test-2028")


@pytest.mark.django_db
def test_first_run_prints_a_test_link_per_guest_and_both_logins():
    """FR-68: the examiner can copy each guest's link and the logins from the output."""
    printed = seed()

    for guest in SEED_GUESTS:
        line = next(line for line in printed.splitlines() if f"/{guest['code']}/" in line)
        assert guest["name"] in line
        assert f"http://127.0.0.1:8000/{guest['code']}/" in line
    assert "testpar / bryllup-test-2028" in printed
    assert "testhjelper / bryllup-test-2028" in printed


# Second run


@pytest.mark.django_db
def test_a_second_run_gives_the_same_result_and_leaves_the_couples_household_alone():
    """FR-72, AD-16: the old test data is replaced; data the seed did not make is kept."""
    first = seed()
    couple = make_couple()
    kept = create_household(couple, [NewGuest("Kari"), NewGuest("Ola")])
    kept_guests = list(kept.guests.values_list("id", "name", "code"))

    second = seed()

    assert second == first
    assert Household.objects.filter(is_test_data=True).count() == 7
    assert Guest.objects.filter(household__is_test_data=True).count() == 14
    assert list(Household.objects.filter(is_test_data=False)) == [kept]
    assert list(kept.guests.values_list("id", "name", "code")) == kept_guests
    assert set(User.objects.values_list("username", flat=True)) == {
        "rikke",
        "testpar",
        "testhjelper",
    }
    assert User.objects.get(username="rikke").is_test_data is False


# Conflicts with data the seed did not make


@pytest.mark.django_db
def test_a_seed_code_held_by_a_real_guest_stops_the_command_and_writes_nothing():
    """FR-72, AD-16: matrix row "Code taken": a CommandError names the code."""
    household = create_household(make_couple(), [NewGuest("Kari")])
    household.guests.update(code=SIGMUNDS_CODE)  # as if a real guest had this code
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    assert SIGMUNDS_CODE in str(refused.value)
    assert "Ingenting ble endret." in str(refused.value)
    assert snapshot() == before


@pytest.mark.django_db
def test_a_seed_username_held_by_a_real_user_stops_the_command_and_writes_nothing():
    """FR-72, AD-16: matrix row "Username taken": a CommandError names the user."""
    User.objects.create_user(username="testpar", role=User.Role.COUPLE)
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    assert "«testpar»" in str(refused.value)
    assert "testhjelper" not in str(refused.value)
    assert snapshot() == before


@pytest.mark.django_db
def test_a_conflict_after_an_earlier_run_keeps_the_earlier_test_data():
    """FR-72: a refusal on a later run does not reset either, since nothing is written."""
    seed()
    Household.objects.filter(is_test_data=True).update(is_test_data=False)  # now "real" data
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    assert SIGMUNDS_CODE in str(refused.value)
    assert snapshot() == before


@pytest.mark.django_db
def test_a_value_a_service_refuses_undoes_the_reset_too(monkeypatch, tmp_path):
    """FR-72, AD-3: a refusal after the reset has run rolls everything back, reset included."""
    seed()
    before = snapshot()
    broken = tmp_path / "seed.toml"
    broken.write_text(
        SEED_FILE.read_text(encoding="utf-8").replace(
            "price_cabin_weekend = 1500", "price_cabin_weekend = -1"
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("wedding.management.commands.seed_testdata.SEED_PATH", broken)

    with pytest.raises(CommandError) as refused:
        seed()

    assert "Prisen for hytte kan ikke være negativ." in str(refused.value)
    assert "Ingenting ble endret." in str(refused.value)
    assert snapshot() == before


# APP_ENV


@pytest.mark.django_db
@pytest.mark.parametrize("app_env", ["production", "prod", "Local", "local "])
def test_any_app_env_but_local_is_refused_and_nothing_is_written(monkeypatch, app_env):
    """FR-72, AD-14: matrix row "Wrong env": an allow list, so a misspelling never passes."""
    monkeypatch.setenv("APP_ENV", app_env)
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    message = str(refused.value)
    assert f"APP_ENV er «{app_env}»" in message
    assert "«local»" in message
    assert snapshot() == before


@pytest.mark.django_db
@pytest.mark.parametrize("app_env", ["local", ""])
def test_app_env_local_or_empty_is_allowed(monkeypatch, app_env):
    """AD-14, NFR-8: `local`, and empty as unset, are the examiner's machine."""
    monkeypatch.setenv("APP_ENV", app_env)

    seed()

    assert Household.objects.count() == 7


@pytest.mark.django_db
def test_production_settings_are_refused_even_without_app_env_in_the_environment(settings):
    """AD-14: the command also checks the loaded settings, not only the variable."""
    settings.APP_ENV = "production"

    with pytest.raises(CommandError) as refused:
        seed()

    assert "APP_ENV er «production»" in str(refused.value)
    assert Household.objects.count() == 0


# The reset service


@pytest.mark.django_db
def test_reset_removes_only_test_households_guests_and_users():
    """FR-72, AD-4, AD-16: rows the couple made are never touched."""
    create_household(SYSTEM, [NewGuest("Sigmund"), NewGuest("bestemor")])
    couple = make_couple()
    kept = create_household(couple, [NewGuest("Kari")])
    User.objects.create_user(username="testpar", is_test_data=True)

    reset_test_data(SYSTEM)

    assert list(Household.objects.all()) == [kept]
    assert list(Guest.objects.values_list("name", flat=True)) == ["Kari"]
    assert list(User.objects.all()) == [couple.user]


@pytest.mark.django_db
@pytest.mark.parametrize("role", [User.Role.COUPLE, User.Role.HELPER])
def test_only_the_system_actor_may_reset(role):
    """AD-3, AD-16: admins cannot remove test data; only the seed command does."""
    create_household(SYSTEM, [NewGuest("Sigmund")])
    actor = AdminActor(User.objects.create_user(username="rikke", role=role))

    with pytest.raises(NotAllowed):
        reset_test_data(actor)

    assert Household.objects.count() == 1


# The conflict check


@pytest.mark.django_db
def test_conflicts_name_only_codes_and_usernames_used_by_real_data():
    """FR-72, AD-16: test rows are not conflicts, since the reset replaces them."""
    create_household(SYSTEM, [NewGuest("Sigmund", code="test-sigmund0000000000")])
    real = create_household(make_couple(), [NewGuest("Kari")])
    real.guests.update(code="test-bestemor000000000")
    User.objects.create_user(username="testhjelper", is_test_data=True)

    conflicts = selectors.seed_conflicts(
        ["test-sigmund0000000000", "test-bestemor000000000", "test-eva00000000000000"],
        ["testpar", "testhjelper", "rikke"],
    )

    assert conflicts == ["lenkekoden «test-bestemor000000000»", "brukernavnet «rikke»"]
