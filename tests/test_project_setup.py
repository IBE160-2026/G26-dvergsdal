"""The project follows the Structural Seed and the settings decisions (Story 1.1).

Covers the custom user model from the first migration (AD-10), time zone and
language (AD-11, NFR-6) and the SQLite options (AD-5).
"""

import importlib
from pathlib import Path

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import migrations

from wedding.models import User

BASE_DIR = Path(__file__).resolve().parent.parent


def test_custom_user_is_the_auth_user_model():
    """AD-10: `wedding.User` is AUTH_USER_MODEL."""
    assert settings.AUTH_USER_MODEL == "wedding.User"
    assert get_user_model() is User


def test_role_is_couple_or_helper_and_defaults_to_helper():
    """AD-10, FR-46: two roles, and a new account gets the least privilege."""
    assert [value for value, _label in User.Role.choices] == ["couple", "helper"]
    assert User().role == User.Role.HELPER


def test_role_is_in_the_first_migration():
    """AD-10: the role field exists from the very first migration, never added later."""
    initial = importlib.import_module("wedding.migrations.0001_initial").Migration
    assert initial.initial is True
    create_user = next(
        op
        for op in initial.operations
        if isinstance(op, migrations.CreateModel) and op.name == "User"
    )
    assert "role" in dict(create_user.fields)


@pytest.mark.django_db
def test_models_and_migrations_agree():
    """AD-10: no model change is left without its migration."""
    call_command("makemigrations", "--check", "--dry-run", verbosity=0)


def test_django_admin_is_not_installed():
    """AD-10: `/admin/` belongs to the dashboard app, not Django's admin."""
    assert "django.contrib.admin" not in settings.INSTALLED_APPS


def test_time_zone_and_language():
    """AD-11, NFR-6: stored in UTC, shown in Oslo time, in Norwegian bokmål."""
    assert settings.USE_TZ is True
    assert settings.TIME_ZONE == "Europe/Oslo"
    assert settings.LANGUAGE_CODE == "nb"


def test_sqlite_options_and_no_atomic_requests():
    """AD-5: busy timeout, WAL, IMMEDIATE transactions, and no request-wide transactions."""
    database = settings.DATABASES["default"]
    assert database["ENGINE"] == "django.db.backends.sqlite3"
    options = database["OPTIONS"]
    assert options["timeout"] > 0
    assert "journal_mode=WAL" in options["init_command"]
    assert options["transaction_mode"] == "IMMEDIATE"
    assert database["ATOMIC_REQUESTS"] is False


def test_static_files_are_self_hosted_through_whitenoise():
    """AD-15: static files come from the site itself, served by WhiteNoise."""
    middleware = settings.MIDDLEWARE
    security = middleware.index("django.middleware.security.SecurityMiddleware")
    assert middleware[security + 1] == "whitenoise.middleware.WhiteNoiseMiddleware"
    assert settings.STATIC_ROOT == BASE_DIR / "staticfiles"
    assert settings.STATICFILES_DIRS == [BASE_DIR / "static"]


def test_structural_seed_folders_exist():
    """Structural Seed: the layout every later story builds on."""
    expected = [
        "config",
        "wedding/rules",
        "wedding/services",
        "wedding/rsvp",
        "wedding/management/commands",
        "wedding/fixtures",
        "guests",
        "dashboard",
        "static/css",
        "static/js",
        "static/fonts",
        "static/img",
        "tests",
    ]
    missing = [path for path in expected if not (BASE_DIR / path).is_dir()]
    assert missing == []
    assert (BASE_DIR / "wedding" / "selectors.py").is_file()
    assert (BASE_DIR / "wedding" / "links.py").is_file()
