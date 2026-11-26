"""Error pages that still show how to reach the couple (Story 1.8).

FR-5, FR-6, AD-15. Every row of the story's I/O matrix: a 404 without a valid
code is G1, a 404, 500 or CSRF failure under a valid link shows the back button
and the couple's phones, an unknown code or a failed lookup gives the
impersonal page, and a 400 for a bad `Host` is always impersonal and never
calls `request.get_host` again. Besides: the headers, the robots meta tag, the
title and the link preview of every error page, the handlers in config/urls.py
and `CSRF_FAILURE_VIEW`, and no writes. pytest-django runs with `DEBUG=False`,
so the handlers are live; `/<code>/feil/` exists only in the test URLconf
tests/error_urls.py. How the pages look in a browser is MT-22 in
docs/manual-test-plan.md.
"""

import re
import tomllib
from pathlib import Path

import pytest
from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.db import DatabaseError
from django.middleware.csrf import _get_failure_view
from django.test import Client, RequestFactory
from django.urls import get_resolver

import config.urls
from config import error_handlers
from guests import views
from tests.helpers import IMPERSONAL_FORBIDDEN, page_text, row_counts, tel_rows
from tests.test_guest_privacy import _assert_private_headers, _head_tags, _preview
from wedding.models import Household, Settings

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
GUEST_NAMES = [guest["name"] for household in SEED["households"] for guest in household["guests"]]
CONTACT_NAMES = [SEED["settings"]["contact_1_name"], SEED["settings"]["contact_2_name"]]

SIGMUND = "test-sigmund0000000000"
UNKNOWN = "AAAAAAAAAAAAAAAAAAAAAA"

NOT_FOUND = "Vi finner ikke denne siden"
SERVER_ERROR = "Noe gikk galt hos oss"
CSRF_FAILURE = "Skjemaet ble ikke sendt"
BAD_REQUEST = "Siden kunne ikke vises"
LINE_A = "Går det fortsatt ikke, send oss en melding."
LINE_B = "Går det fortsatt ikke, ta kontakt med brudeparet direkte."
BACK_LINK = re.compile(
    r'<p class="error-page__back">\s*<a class="button button--on-green" '
    rf'href="/{SIGMUND}/">Tilbake til invitasjonen</a>\s*</p>'
)
# Each error page's `<title>`: its heading, an en dash and «Invitasjon», like the info pages.


def _title(heading: str) -> str:
    return f"{heading} \N{EN DASH} Invitasjon"


# The same words MT-22 forbids in the page text.
TECHNICAL = ("Traceback", "Exception", "RuntimeError", "Django", "DEBUG", "settings")

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("local_env"),
    pytest.mark.urls("tests.error_urls"),
]


def _client(*, csrf: bool = False) -> Client:
    """A test client that returns the 500 page instead of raising the view's error."""
    return Client(enforce_csrf_checks=csrf, raise_request_exception=False)


def _get(path: str, **extra):
    return _client().get(path, **extra)


def _post(path: str):
    return _client(csrf=True).post(path)


def _front_page_rows() -> list[tuple[str, str]]:
    rows = tel_rows(_get(f"/{SIGMUND}/").content.decode())
    assert len(rows) == 2
    return rows


def _heading(html: str) -> str:
    return re.search(r'<h1 class="private-invitation__heading">([^<]*)</h1>', html).group(1)


def _assert_impersonal(html: str) -> None:
    """FR-5: nothing personal and nothing technical, and no back button."""
    for forbidden in IMPERSONAL_FORBIDDEN:
        assert forbidden not in html, forbidden
    for name in GUEST_NAMES + CONTACT_NAMES:
        assert not re.search(rf"\b{re.escape(name)}\b", html), name
    assert "error-page__back" not in html
    assert SIGMUND not in html
    _assert_not_technical(html)


def _assert_not_technical(html: str) -> None:
    text = page_text(html)
    for word in TECHNICAL:
        assert word not in text, word


def _assert_reachable(html: str) -> None:
    """FR-6: the back button to the invitation and the same `tel:` rows as the front
    page, no nav bar and no guest's name."""
    assert BACK_LINK.search(html)
    assert tel_rows(html) == _front_page_rows()
    assert "<nav" not in html
    for name in GUEST_NAMES:
        assert not re.search(rf"\b{re.escape(name)}\b", html), name
    _assert_not_technical(html)


# 404 (FR-5, FR-6)


@pytest.mark.parametrize(("path", "queries"), [("/hei/x/", 0), (f"/{UNKNOWN}/svar/", 1)])
@pytest.mark.parametrize("seed", [True, False], ids=["seeded", "empty"])
def test_404_without_a_valid_code_is_g1(request, django_assert_num_queries, path, queries, seed):
    """FR-5: an address that is not a page and does not start with a valid code
    gives 404 and G1, byte for byte the page on `/`, after one lookup for a
    well-formed code and none otherwise, also on an empty, migrated database."""
    if seed:
        request.getfixturevalue("seeded")
    bare = _get("/").content.decode()
    with django_assert_num_queries(queries):
        response = _get(path)
    assert response.status_code == 404
    assert "guests/private_invitation.html" in [t.name for t in response.templates]
    assert response.content.decode() == bare


@pytest.mark.parametrize("path", [f"/{SIGMUND}/finnes-ikke/", f"/{SIGMUND}/program/x/"])
def test_404_under_a_valid_link_shows_the_phones(seeded, django_assert_num_queries, path):
    """FR-5, FR-6: under a valid link the 404 says «Vi finner ikke denne siden»,
    has the back button to the invitation and the footer band with both phones,
    after two queries (the resolver and the settings row)."""
    with django_assert_num_queries(2):
        response = _get(path)
    assert response.status_code == 404
    html = response.content.decode()
    assert _heading(html) == NOT_FOUND
    assert "Lenken kan ha en skrivefeil. Invitasjonen ligger der den var." in page_text(html)
    _assert_reachable(html)


# 500 (FR-5, FR-6, AD-15)


def test_500_under_a_valid_link_shows_the_phones(seeded):
    """FR-6, AD-15: a view that raises under a valid link gives «Noe gikk galt hos
    oss», the back button, the phones and line A, and no traceback; rendered
    without a request, so no og:image."""
    response = _get(f"/{SIGMUND}/feil/")
    assert response.status_code == 500
    html = response.content.decode()
    assert _heading(html) == SERVER_ERROR
    text = page_text(html)
    assert "Prøv igjen om litt." in text
    assert LINE_A in text
    assert LINE_B not in text
    assert "og:image" not in _preview(html)
    _assert_reachable(html)


@pytest.mark.parametrize("seed", [True, False], ids=["seeded", "empty"])
def test_500_under_an_unknown_code_is_impersonal(request, seed):
    """FR-5: under an unknown code, also on an empty database, the 500 page has
    line B and no footer, phone or back button."""
    if seed:
        request.getfixturevalue("seeded")
    response = _get(f"/{UNKNOWN}/feil/")
    assert response.status_code == 500
    html = response.content.decode()
    assert _heading(html) == SERVER_ERROR
    assert LINE_B in page_text(html)
    assert LINE_A not in page_text(html)
    _assert_impersonal(html)


def test_500_on_a_broken_database_is_impersonal(seeded):
    """FR-5: with the settings row gone the front page fails, and so does the
    error page's own lookup; it falls back to the impersonal 500 page."""
    Settings.objects.all().delete()
    response = _get(f"/{SIGMUND}/")
    assert response.status_code == 500
    html = response.content.decode()
    assert _heading(html) == SERVER_ERROR
    assert LINE_B in page_text(html)
    _assert_impersonal(html)


@pytest.mark.parametrize(
    ("path", "status", "heading"),
    [(f"/{SIGMUND}/feil/", 500, SERVER_ERROR), (f"/{SIGMUND}/finnes-ikke/", 404, None)],
    ids=["500", "404"],
)
def test_a_lookup_that_raises_falls_back(seeded, monkeypatch, caplog, path, status, heading):
    """FR-5: when the resolver itself raises, the error page never fails: the 500
    is impersonal and the 404 is G1. The failed lookup is logged once as a
    warning with its traceback, since on a 404 nothing else would log it."""

    def broken(code):
        raise DatabaseError("database is locked")

    monkeypatch.setattr(views, "resolve_code", broken)
    with caplog.at_level("WARNING", logger="guests.views"):
        response = _get(path)
    records = [record for record in caplog.records if record.name == "guests.views"]
    assert len(records) == 1
    assert records[0].levelname == "WARNING"
    # The LOGGING filter formats the traceback into `exc_text` and masks the code.
    assert "DatabaseError: database is locked" in records[0].exc_text
    assert SIGMUND not in records[0].getMessage() + records[0].exc_text
    assert response.status_code == status
    html = response.content.decode()
    if heading:
        assert _heading(html) == heading
    else:
        assert html == _get("/").content.decode()
    _assert_impersonal(html)


def test_valid_link_without_phones_keeps_the_back_button(seeded):
    """FR-6: with no phone to call there is no footer, but the back button stays,
    and the 500 and CSRF pages say line B, since there is nothing below to
    message."""
    Settings.objects.filter(pk=1).update(contact_1_phone="", contact_2_phone="")
    for path, heading in (
        (f"/{SIGMUND}/feil/", SERVER_ERROR),
        (f"/{SIGMUND}/finnes-ikke/", NOT_FOUND),
    ):
        html = _get(path).content.decode()
        assert _heading(html) == heading
        assert BACK_LINK.search(html)
        assert "<footer" not in html
        assert "tel:" not in html
    assert LINE_B in page_text(_get(f"/{SIGMUND}/feil/").content.decode())
    response = _post(f"/{SIGMUND}/")
    assert response.status_code == 403
    html = response.content.decode()
    assert _heading(html) == CSRF_FAILURE
    assert BACK_LINK.search(html)
    assert "<footer" not in html
    assert "tel:" not in html
    assert LINE_B in page_text(html)
    assert LINE_A not in page_text(html)


# CSRF failure (FR-5, FR-6, AD-15)


def test_csrf_failure_under_a_valid_link_shows_the_phones(seeded):
    """FR-6: a form posted to a valid link without a CSRF token gives 403 with
    «Skjemaet ble ikke sendt», the back button, the phones and line A."""
    response = _post(f"/{SIGMUND}/")
    assert response.status_code == 403
    html = response.content.decode()
    assert _heading(html) == CSRF_FAILURE
    text = page_text(html)
    assert "Gå tilbake og prøv igjen." in text
    assert LINE_A in text
    _assert_reachable(html)


@pytest.mark.parametrize("path", [f"/{UNKNOWN}/", "/"])
def test_csrf_failure_without_a_valid_link_is_impersonal(seeded, path):
    """FR-5: posted to an unknown code or to `/`, the 403 has line B and nothing
    personal."""
    response = _post(path)
    assert response.status_code == 403
    html = response.content.decode()
    assert _heading(html) == CSRF_FAILURE
    assert LINE_B in page_text(html)
    _assert_impersonal(html)


def test_500_never_calls_get_host(seeded, monkeypatch):
    """AD-15: the 500 page renders without the request, so even under a valid
    link, where it reads the code and the phones, `request.get_host` is never
    called; a 500 can come before the host is checked."""
    request = RequestFactory().get(f"/{SIGMUND}/")

    def disallowed():
        raise DisallowedHost("evil.example")

    monkeypatch.setattr(request, "get_host", disallowed)
    response = views.server_error(request)
    assert response.status_code == 500
    html = response.content.decode()
    assert _heading(html) == SERVER_ERROR
    assert BACK_LINK.search(html)


# 400 (FR-5, AD-15, deferred from 1.4c)


def test_bad_host_gives_the_impersonal_400(seeded):
    """FR-5, AD-15: a `Host` that is not allowed gives 400 with «Siden kunne ikke
    vises» and line B; the page never looks up the code, never names the bad host
    and has no og:image, so `request.get_host` is not called again."""
    response = _get(f"/{SIGMUND}/", HTTP_HOST="evil.example")
    assert response.status_code == 400
    html = response.content.decode()
    assert _heading(html) == BAD_REQUEST
    assert "Prøv å åpne lenken på nytt." in page_text(html)
    assert LINE_B in page_text(html)
    assert "evil.example" not in html
    assert "og:image" not in _preview(html)
    _assert_impersonal(html)


# Every error response (AD-15)

# Each error, its status and its page title; seeded.
ERRORS = {
    "404-g1": (lambda: _get("/hei/x/"), 404, "Invitasjon"),
    "404-unknown": (lambda: _get(f"/{UNKNOWN}/svar/"), 404, "Invitasjon"),
    "404-link": (lambda: _get(f"/{SIGMUND}/finnes-ikke/"), 404, _title(NOT_FOUND)),
    "500-link": (lambda: _get(f"/{SIGMUND}/feil/"), 500, _title(SERVER_ERROR)),
    "500-unknown": (lambda: _get(f"/{UNKNOWN}/feil/"), 500, _title(SERVER_ERROR)),
    "403-link": (lambda: _post(f"/{SIGMUND}/"), 403, _title(CSRF_FAILURE)),
    "403-unknown": (lambda: _post(f"/{UNKNOWN}/"), 403, _title(CSRF_FAILURE)),
    "403-bare": (lambda: _post("/"), 403, _title(CSRF_FAILURE)),
    "400": (
        lambda: _get(f"/{SIGMUND}/", HTTP_HOST="evil.example"),
        400,
        _title(BAD_REQUEST),
    ),
}
# Rendered without a request, so the link preview has no og:image.
WITHOUT_REQUEST = {"500-link", "500-unknown", "400"}


@pytest.mark.parametrize("error", ERRORS)
def test_every_error_page_is_private_and_never_writes(seeded, assert_loads_only_own_host, error):
    """AD-15, FR-3, FR-4: every error page carries `X-Robots-Tag: noindex` and
    `Referrer-Policy: same-origin`, one robots meta tag, its fixed title, the
    same link preview as `/` (without og:image when rendered without a
    request), only our own host, and it creates or changes no row."""
    make, status, title = ERRORS[error]
    bare = _preview(_get("/").content.decode())
    before = row_counts()
    revisions = list(Household.objects.values_list("id", "revision"))
    response = make()
    assert response.status_code == status
    _assert_private_headers(response, never_stored=True)
    html = response.content.decode()
    robots = [meta for meta in _head_tags(html).metas if meta.get("name") == "robots"]
    assert robots == [{"name": "robots", "content": "noindex"}]
    preview = _preview(html)
    expected = {**bare, "title": title}
    if error in WITHOUT_REQUEST:
        del expected["og:image"]
    assert preview == expected
    assert_loads_only_own_host(html)
    assert row_counts() == before
    assert list(Household.objects.values_list("id", "revision")) == revisions


# Wiring (FR-5, FR-6, AD-15)


def test_handlers_and_csrf_failure_view_are_the_dispatchers():
    """FR-5, AD-15, UX-DR36: config/urls.py names the four handlers and the settings
    name the CSRF failure view, all in config/error_handlers.py (Story 3.1), so Django
    never shows its own pages. The 400 is the guests' own, always impersonal."""
    assert config.urls.handler400 == "config.error_handlers.bad_request"
    assert config.urls.handler403 == "config.error_handlers.permission_denied"
    assert config.urls.handler404 == "config.error_handlers.page_not_found"
    assert config.urls.handler500 == "config.error_handlers.server_error"
    resolver = get_resolver("config.urls")
    assert resolver.resolve_error_handler(400) is views.bad_request
    assert resolver.resolve_error_handler(403) is error_handlers.permission_denied
    assert resolver.resolve_error_handler(404) is error_handlers.page_not_found
    assert resolver.resolve_error_handler(500) is error_handlers.server_error
    assert settings.CSRF_FAILURE_VIEW == "config.error_handlers.csrf_failure"
    assert _get_failure_view() is error_handlers.csrf_failure
