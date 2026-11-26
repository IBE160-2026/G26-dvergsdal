"""The `create_admin` command (Story 3.1, FR-47, AD-3, AD-10, AD-16).

Covers the story's «Create account», «Refused» and «Seed afterwards» rows. The
password prompt (`getpass`) is replaced by a queue of answers, so a test never
waits on a terminal.
"""

from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from wedding.models import User

PASSWORD = "et-langt-og-unikt-passord-2028"


def run(monkeypatch, *args, answers=(PASSWORD, PASSWORD)):
    """Run `create_admin` with `answers` typed at the prompts; return what it printed."""
    typed = iter(answers)
    monkeypatch.setattr(
        "wedding.management.commands.create_admin.getpass", lambda prompt="": next(typed)
    )
    out = StringIO()
    call_command("create_admin", *args, stdout=out)
    return out.getvalue()


@pytest.mark.django_db
@pytest.mark.parametrize(("role", "label"), [("couple", "brudeparet"), ("helper", "hjelper")])
def test_creates_a_real_hashed_account(monkeypatch, role, label):
    """FR-47, AD-16: the account has its role, is not test data and has a hashed password."""
    output = run(monkeypatch, "rikke", "--role", role)

    user = User.objects.get(username="rikke")
    assert (user.role, user.is_test_data) == (role, False)
    assert user.password != PASSWORD
    assert user.check_password(PASSWORD)
    assert f"Opprettet rikke ({label})." in output


@pytest.mark.django_db
def test_a_taken_username_is_refused_before_the_password_is_asked(monkeypatch):
    """FR-47: the existing account stays as it was; an empty queue would raise on a prompt."""
    User.objects.create_user(username="rikke", role=User.Role.HELPER)

    with pytest.raises(CommandError, match=r"Brukernavnet «rikke» er allerede i bruk."):
        run(monkeypatch, "rikke", "--role", "couple", answers=())

    assert User.objects.get().role == User.Role.HELPER


@pytest.mark.django_db
@pytest.mark.parametrize("args", [("rikke",), ("rikke", "--role", "admin")])
def test_a_missing_or_unknown_role_is_refused(monkeypatch, args):
    """FR-47, AD-10: the role has no default and only couple or helper is accepted."""
    with pytest.raises(CommandError):
        run(monkeypatch, *args, answers=())

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_passwords_that_differ_write_nothing(monkeypatch):
    """FR-47: typed twice, so a slip in one is caught."""
    with pytest.raises(CommandError, match="Passordene er ikke like"):
        run(monkeypatch, "rikke", "--role", "couple", answers=(PASSWORD, PASSWORD + "x"))

    assert User.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize("weak", ["kort", "12345678901234", "password1234"])
def test_a_weak_password_is_refused(monkeypatch, weak):
    """FR-47, NFR-4: Django's validators (length, numeric only, common) apply."""
    with pytest.raises(CommandError, match="Passordet er ikke godt nok"):
        run(monkeypatch, "rikke", "--role", "couple", answers=(weak, weak))

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_the_password_is_never_an_argument(monkeypatch):
    """FR-47: there is no password option, so it cannot end up in a shell history."""
    with pytest.raises(CommandError):
        run(monkeypatch, "rikke", "--role", "couple", "--password", PASSWORD)


def test_a_real_account_survives_the_seed(local_env, db, monkeypatch):
    """FR-47, FR-68, FR-72, AD-16: `seed_testdata` replaces its own test accounts and
    leaves a real one."""
    run(monkeypatch, "rikke", "--role", "couple")

    call_command("seed_testdata", stdout=StringIO())
    call_command("seed_testdata", stdout=StringIO())

    real = User.objects.get(username="rikke")
    assert real.is_test_data is False
    assert real.check_password(PASSWORD)
    assert User.objects.filter(is_test_data=True).count() == 2


def test_a_seed_username_equal_to_a_real_one_stops_the_seed(local_env, db, monkeypatch):
    """FR-72, AD-16: the seed never replaces a real account, and writes nothing."""
    run(monkeypatch, "testpar", "--role", "couple")

    with pytest.raises(CommandError, match="brukernavnet «testpar»"):
        call_command("seed_testdata", stdout=StringIO())

    assert User.objects.get().is_test_data is False
