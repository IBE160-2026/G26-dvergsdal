"""Shared pytest setup.

Django's real password hasher is slow on purpose, and the seed command hashes two
passwords per run. Tests use the fast MD5 hasher instead, as Django's testing
docs recommend; it is never used outside the tests.
"""

import pytest


@pytest.fixture(autouse=True)
def fast_password_hasher(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
