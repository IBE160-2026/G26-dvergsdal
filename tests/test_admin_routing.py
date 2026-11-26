"""`/admin/` is routed above the guests' catch-all (Story 3.1; FR-5, FR-46, NFR-4, AD-10, AD-13).

`<str:code>/` matches any single path segment, so every reserved first segment
must be routed above it and listed in `NOT_LINK_CODES` of the log filter. Covers
the «No slash» and «Unknown admin path» rows: `/admin/`, `/admin` and
`/admin/program/` never render G1, and the guest pages stay free of the admin
frame, the session and the nav.
"""

import pytest
from django.conf import settings
from django.test import Client
from django.urls import URLPattern, URLResolver

import config.urls
from config.logging_filters import NOT_LINK_CODES
from tests.helpers import page_text, row_counts
from tests.test_log_masking import CODE
from wedding.models import User

G1 = "Dette er en privat invitasjon"
PASSWORD = "bryllup-test-2028"
NAV_WORDS = ("Oversikt", "Gjester", "Betalinger", "Innstillinger", "Logg ut")


def first_segments(patterns, prefix=""):
    """The first path segment of every fixed route in `patterns`, nested includes too."""
    found = set()
    for pattern in patterns:
        route = prefix + str(pattern.pattern)
        if isinstance(pattern, URLResolver):
            found |= first_segments(pattern.url_patterns, route)
        elif isinstance(pattern, URLPattern):
            segment = route.split("/")[0]
            if segment and not segment.startswith("<"):
                found.add(segment)
    return found


def test_every_reserved_first_segment_is_listed_in_not_link_codes():
    """NFR-4, AD-15: a fixed route above the catch-all, and the static files' prefix, must
    stay readable in the log; the test fails when a new one is routed and not listed."""
    reserved = first_segments(config.urls.urlpatterns) | {settings.STATIC_URL.strip("/")}

    assert {"admin", "robots.txt", "static"} <= reserved
    assert reserved - NOT_LINK_CODES == set()


@pytest.mark.parametrize("path", ["/admin/", "/admin/hei/", "/admin/program/", "/robots.txt"])
def test_admin_paths_and_robots_never_render_g1(db, path):
    """FR-5, FR-46: a logged-out visitor is redirected, `/robots.txt` is plain text."""
    response = Client().get(path)

    assert G1 not in page_text(response.content.decode())
    if path == "/robots.txt":
        assert response.status_code == 200
    else:
        assert response.status_code == 302
        assert response["Location"] == f"/admin/logg-inn/?next={path}"


def test_admin_without_a_slash_redirects_to_admin_and_not_to_g1(db):
    """FR-46: `/admin` is a 301 to `/admin/`."""
    response = Client().get("/admin")

    assert (response.status_code, response["Location"]) == (301, "/admin/")


def test_a_logged_in_admin_never_sees_g1_under_admin(db):
    """FR-5, UX-DR36: an unknown admin page is the couple's 404, not G1 or a guest page."""
    User.objects.create_user(username="rikke", password=PASSWORD, role=User.Role.COUPLE)
    admin = Client()
    admin.login(username="rikke", password=PASSWORD)

    for path in ("/admin/", "/admin/program/", "/admin/hei/", f"/admin/{CODE}/"):
        response = admin.get(path)
        assert G1 not in page_text(response.content.decode()), path
    assert admin.get("/admin/").status_code == 200
    assert admin.get("/admin/hei/").status_code == 404


def test_the_frame_is_on_every_admin_page_for_a_logged_in_admin(db):
    """UX-DR34: the nav words, «Logg ut» as a POST button, and `aria-current` on the open
    page; the unbuilt pages are plain text, not links."""
    User.objects.create_user(username="rikke", password=PASSWORD, role=User.Role.COUPLE)
    admin = Client()
    admin.login(username="rikke", password=PASSWORD)

    for path in ("/admin/", "/admin/hei/"):
        html = admin.get(path).content.decode()
        text = page_text(html)
        assert 'aria-label="Administrasjon"' in html
        for word in NAV_WORDS:
            assert word in text, (path, word)
        assert 'action="/admin/logg-ut/"' in html
        assert 'method="post"' in html
        assert 'class="admin-nav__logout">Logg ut</button>' in html
        assert "Svar</a>" not in html
        for word in ("Gjester", "Betalinger", "Innstillinger"):
            assert f">{word}</a>" not in html
    home = admin.get("/admin/").content.decode()
    assert 'href="/admin/" aria-current="page">Oversikt</a>' in " ".join(home.split())
    assert "admin-page" in home
    assert "<script" not in home


def test_guest_pages_render_no_nav_session_or_user(seeded):
    """AD-8, AD-10: a guest link shows no admin frame, sets no cookie and writes no row."""
    before = row_counts()
    client = Client()

    for path in (f"/{CODE}/", f"/{CODE}/program/", f"/{CODE}/hei/", "/"):
        response = client.get(path)
        html = response.content.decode()
        assert 'aria-label="Administrasjon"' not in html, path
        assert "admin-page" not in html, path
        assert "Logg ut" not in html, path
        assert not response.cookies, path

    assert row_counts() == before
