"""Shared pytest setup.

Django's real password hasher is slow on purpose, and the seed command hashes two
passwords per run. Tests use the fast MD5 hasher instead, as Django's testing
docs recommend; it is never used outside the tests.

`production_urls` rebuilds the URLconf as production sees it (Story 1.4a and 1.4b).
"""

import importlib

import pytest
from django.test import override_settings
from django.urls import clear_url_caches

import config.urls
import guests.urls


@pytest.fixture(autouse=True)
def fast_password_hasher(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


def _reload_urlconf():
    importlib.reload(guests.urls)
    importlib.reload(config.urls)
    clear_url_caches()


@pytest.fixture
def production_urls():
    """The URLconf as it is built with `APP_ENV=production` (no `/stil/`), for the
    length of one test. `guests/urls.py` reads `APP_ENV` at import, so it is
    reloaded on the way in and again on the way out."""
    try:
        with override_settings(APP_ENV="production"):
            _reload_urlconf()
            yield guests.urls.urlpatterns
    finally:
        _reload_urlconf()
