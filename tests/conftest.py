"""Shared pytest setup.

Django's real password hasher is slow on purpose, and the seed command hashes two
passwords per run. Tests use the fast MD5 hasher instead, as Django's testing
docs recommend; it is never used outside the tests.

`production_urls` rebuilds the URLconf as production sees it (Story 1.4a and 1.4b).
`assert_loads_only_own_host` checks that a page names no other site (Story 1.4c).
"""

import importlib
import re
from collections.abc import Callable

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


OWN_HOST = "http://testserver/"


def _loads_only_own_host(html: str) -> None:
    """AD-15, NFR-4: every `://` in `html` starts the test client's own address
    (the og:image is absolute, from the request host), and no `src` or `href` is
    protocol-relative (`//other.site/`), which would load from another site."""
    addresses = re.findall(r"""[\w+.-]*://[^/\s"'<>]*/?""", html)
    assert [address for address in addresses if address != OWN_HOST] == []
    assert not re.search(r"""\b(?:src|href)=["']?//""", html)


@pytest.fixture
def assert_loads_only_own_host() -> Callable[[str], None]:
    """The checker above, for any test that renders a page."""
    return _loads_only_own_host
