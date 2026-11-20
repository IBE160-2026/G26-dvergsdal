"""Shared pytest setup.

Django's real password hasher is slow on purpose, and the seed command hashes two
passwords per run. Tests use the fast MD5 hasher instead, as Django's testing
docs recommend; it is never used outside the tests.

`production_urls` rebuilds the URLconf as production sees it (Story 1.4a and 1.4b).
`assert_loads_only_own_host` checks that a page names no other site (Story 1.4c).
`local_env` and `seeded` give the examiner's machine and the seeded test data
(Story 1.5); plain helpers that tests import are in tests/helpers.py.
"""

import importlib
import re
from collections.abc import Callable
from io import StringIO

import pytest
from django.core.management import call_command
from django.test import override_settings
from django.urls import clear_url_caches

import config.urls
import guests.urls


@pytest.fixture(autouse=True)
def fast_password_hasher(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture
def local_env(monkeypatch):
    """The examiner's machine: no APP_ENV set (NFR-8), so the seed command runs."""
    monkeypatch.delenv("APP_ENV", raising=False)


@pytest.fixture
def seeded(local_env, db):
    """The fictional test data from seed.toml, loaded through the seed command."""
    call_command("seed_testdata", stdout=StringIO())


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


OWN_HOST = "testserver"

# Attributes whose value is a URL the browser fetches or the previewer reads.
# `srcset` is a list, so any of its entries may start with `//`.
_PROTOCOL_RELATIVE = re.compile(
    r"""\b(?:src|href|action|content|poster)=["']?//"""
    r"""|\bsrcset=["']?(?:[^"'>]*,\s*)?//"""
    r"""|url\(\s*["']?//"""
)


def _loads_only_own_host(html: str, scheme: str = "http") -> None:
    """AD-15, NFR-4: every `://` in `html` starts the test client's own address with
    the request's own scheme (the og:image is absolute, from the request host),
    and no URL attribute or CSS `url()` is protocol-relative (`//other.site/`),
    which would load from another site."""
    own = f"{scheme}://{OWN_HOST}/"
    addresses = re.findall(r"""[\w+.-]*://[^/\s"'<>]*/?""", html)
    assert [address for address in addresses if address != own] == []
    assert not _PROTOCOL_RELATIVE.search(html)


@pytest.fixture
def assert_loads_only_own_host() -> Callable[..., None]:
    """The checker above, for any test that renders a page; pass `scheme="https"`
    for a request made with `secure=True`."""
    return _loads_only_own_host
