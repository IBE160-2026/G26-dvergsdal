"""The couple's own error pages under `/admin/` (Story 3.1; FR-5 spirit, UX-DR36, AD-15).

Covers the «Error pages» and «Same errors on guest paths» rows: 403, 404, 500 and
a failed CSRF check under `/admin/` give the couple's page in the admin frame with
a way back and the status kept; the same errors on a guest path or `/` keep the
guest pages, and a `PermissionDenied` there gives a new impersonal 403. The
test-only URLconf tests/error_urls.py adds the routes that raise.
"""

import pytest
from django.test import Client

from tests.helpers import IMPERSONAL_FORBIDDEN, page_text
from wedding.models import User

PASSWORD = "bryllup-test-2028"
SIGMUND = "test-sigmund0000000000"
CONTACT_LINE = "ta kontakt med brudeparet direkte"

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("local_env"),
    pytest.mark.urls("tests.error_urls"),
]


def client(*, csrf=False) -> Client:
    return Client(enforce_csrf_checks=csrf, raise_request_exception=False)


def logged_in(*, csrf=False) -> Client:
    User.objects.create_user(username="rikke", password=PASSWORD, role=User.Role.COUPLE)
    admin = client(csrf=csrf)
    assert admin.login(username="rikke", password=PASSWORD)
    return admin


PAGES = [
    ("/admin/hei/", 404, "Vi finner ikke denne siden"),
    ("/admin/forbudt/", 403, "Du har ikke tilgang til denne siden"),
    ("/admin/feil/", 500, "Noe gikk galt"),
]


@pytest.mark.parametrize(("path", "status", "heading"), PAGES)
def test_a_logged_in_admin_gets_the_couples_page_with_nav_and_a_way_back(path, status, heading):
    """UX-DR36: status kept, heading, the admin frame with nav, «Til oversikten», and
    never the guest wording."""
    response = logged_in().get(path)

    html = response.content.decode()
    text = page_text(html)
    assert response.status_code == status
    assert f'<h1 class="admin-title">\n        {heading}' in html or heading in text
    assert "admin-page" in html
    assert CONTACT_LINE not in text
    assert "Dette er en privat invitasjon" not in text
    if status == 500:  # rendered without the request: never the nav
        assert "<nav" not in html
        assert "Til innlogging" in text
    else:
        assert "Til oversikten" in text
        assert 'aria-label="Administrasjon"' in html
        assert "Logg ut" in text


def test_the_404_for_a_logged_in_admin_is_the_couples_not_g1():
    """UX-DR36: `/admin/hei/` and `/admin/program/` are never G1 or a guest page."""
    admin = logged_in()

    for path in ("/admin/hei/", "/admin/program/"):
        response = admin.get(path)
        assert response.status_code == 404
        assert "Vi finner ikke denne siden" in page_text(response.content.decode())
        assert "Dette er en privat invitasjon" not in response.content.decode()


@pytest.mark.parametrize(("path", "status", "heading"), PAGES[1:])
def test_a_visitor_who_is_not_logged_in_gets_the_plain_frame(path, status, heading):
    """UX-DR36: no nav, and the way back is the login page. (A 404 under `/admin/` for
    such a visitor never happens: the page redirects to the login first.)"""
    response = client().get(path)

    html = response.content.decode()
    text = page_text(html)
    assert response.status_code == status
    assert heading in text
    assert "<nav" not in html
    assert "Til innlogging" in text
    assert "Til oversikten" not in text
    assert 'href="/admin/logg-inn/"' in html


def test_a_failed_csrf_check_under_admin_gives_the_couples_page():
    """UX-DR36: «Skjemaet ble ikke sendt» in the admin frame, 403, with a way back."""
    response = client(csrf=True).post("/admin/logg-inn/", {"username": "x", "password": "y"})

    html = response.content.decode()
    text = page_text(html)
    assert response.status_code == 403
    assert "Skjemaet ble ikke sendt" in text
    assert "admin-page" in html
    assert "Til innlogging" in text
    assert CONTACT_LINE not in text


def test_a_failed_csrf_check_for_a_logged_in_admin_has_the_nav():
    """UX-DR36: «Logg ut» posts too, so a stale logout form gets the page with the nav."""
    response = logged_in(csrf=True).post("/admin/logg-ut/")

    text = page_text(response.content.decode())
    assert response.status_code == 403
    assert "Skjemaet ble ikke sendt" in text
    assert "Til oversikten" in text


def test_the_error_pages_are_not_cached_and_keep_the_noindex_header():
    """AD-15: the couple's error pages say no-store and carry X-Robots-Tag."""
    for path in ("/admin/forbudt/", "/admin/feil/"):
        response = client().get(path)
        assert "no-store" in response["Cache-Control"]
        assert "noindex" in response["X-Robots-Tag"]


def test_a_failing_lookup_falls_back_to_the_plain_frame(monkeypatch):
    """UX-DR36: an error page never fails itself; a broken user lookup gives the plain
    frame with the way back to the login."""

    def broken(user):
        raise RuntimeError("the database is gone")

    monkeypatch.setattr("dashboard.errors.is_admin", broken)

    response = logged_in().get("/admin/forbudt/")

    html = response.content.decode()
    assert response.status_code == 403
    assert "<nav" not in html
    assert "Til innlogging" in page_text(html)


# The same errors on guest paths keep the guest pages


def test_a_permission_denied_on_a_guest_path_gives_the_impersonal_403(seeded):
    """UX-DR36, FR-5: a new 403 page that names nobody and has no nav, footer or phones."""
    response = client().get(f"/{SIGMUND}/forbudt/")

    html = response.content.decode()
    text = page_text(html)
    assert response.status_code == 403
    assert "Du har ikke tilgang til denne siden" in text
    assert "admin-page" not in html
    assert SIGMUND not in html
    for forbidden in IMPERSONAL_FORBIDDEN:
        assert forbidden not in html, forbidden
    assert "no-store" in response["Cache-Control"]


def test_the_guest_pages_are_unchanged_by_the_admin_pages(seeded):
    """FR-5, FR-6: a 404 under a valid link, a 500 under one and G1 keep their pages."""
    not_found = client().get(f"/{SIGMUND}/hei/")
    server_error = client().get(f"/{SIGMUND}/feil/")
    nothing = client().get("/")

    assert not_found.status_code == 404
    assert "Vi finner ikke denne siden" in page_text(not_found.content.decode())
    assert "Tilbake til invitasjonen" in page_text(not_found.content.decode())
    assert server_error.status_code == 500
    assert "Noe gikk galt hos oss" in page_text(server_error.content.decode())
    assert "Dette er en privat invitasjon" in page_text(nothing.content.decode())
    for response in (not_found, server_error, nothing):
        assert "admin-page" not in response.content.decode()


def test_a_failed_csrf_check_on_a_guest_path_keeps_the_guest_page(seeded):
    """FR-5, UX-DR52: the guest CSRF page is unchanged outside `/admin/`."""
    response = client(csrf=True).post(f"/{SIGMUND}/")

    text = page_text(response.content.decode())
    assert response.status_code == 403
    assert "Skjemaet ble ikke sendt" in text
    assert "admin-page" not in response.content.decode()
