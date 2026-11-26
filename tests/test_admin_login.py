"""The couple's login, logout and session (Story 3.1; FR-46, NFR-4, AD-10, AD-13).

Covers the story's I/O rows «Login ok», «Login wrong», «Logged out», «Expired»
and «Logout», the safety of `next`, the hashed password, the session cookie and
its 20-hour life, and that admin responses are not cached. The real hasher is
used for one test only; the others use the fast hasher from conftest.py.
"""

import datetime
import re
from urllib.parse import quote

import pytest
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.test import Client
from django.utils import timezone

from dashboard.forms import LOGIN_FAILED, AdminLoginForm
from tests.helpers import page_text, row_counts
from tests.test_log_masking import CODE
from wedding.models import User

LOGIN = "/admin/logg-inn/"
PASSWORD = "bryllup-test-2028"
EXPIRED = "Du ble logget ut fordi du var borte en stund."


@pytest.fixture
def couple(db):
    """A real couple account that can log in."""
    return User.objects.create_user(username="rikke", password=PASSWORD, role=User.Role.COUPLE)


def log_in(client, username="rikke", password=PASSWORD, **extra):
    return client.post(LOGIN, {"username": username, "password": password, **extra})


def test_the_login_page_has_labelled_fields_and_no_nav(db):
    """FR-46, UX A1, WCAG 3.3.8: `h1`, labels tied to fields, autofill attributes, a
    password field, a «Logg inn» button, no nav, no «glemt passord»."""
    response = Client().get(LOGIN)

    html = response.content.decode()
    assert response.status_code == 200
    assert "<h1" in html
    assert "Logg inn</h1>" in html
    assert 'for="id_username">Brukernavn</label>' in html
    assert 'for="id_password">Passord</label>' in html
    assert 'autocomplete="username"' in html
    assert 'autocomplete="current-password"' in html
    assert 'type="password"' in html
    assert "onpaste" not in html
    assert "<nav" not in html
    assert "glemt" not in html.lower()
    assert "<script" not in html


@pytest.mark.parametrize("role", [User.Role.COUPLE, User.Role.HELPER])
def test_the_right_details_lead_to_oversikt_with_the_nav(db, role):
    """FR-46: 302 to `/admin/`, then the nav words, «Logg ut» and the Svar panel (Story 3.2)."""
    User.objects.create_user(username="rikke", password=PASSWORD, role=role)
    client = Client()

    response = log_in(client)

    assert (response.status_code, response["Location"]) == (302, "/admin/")
    page = client.get("/admin/")
    text = page_text(page.content.decode())
    assert page.status_code == 200
    for word in ("Oversikt", "Gjester", "Betalinger", "Innstillinger", "Logg ut"):
        assert word in text
    assert "Svart: 0 av 0 husstander" in text


def test_next_under_admin_is_followed(couple):
    """FR-46: a login from a redirect returns to the page asked for."""
    response = log_in(Client(), next="/admin/hei/")

    assert response["Location"] == "/admin/hei/"


@pytest.mark.parametrize(
    "target",
    [
        "https://evil.example/",
        "//evil.example/admin/",
        "/",
        "/svar/",
        "/Abcdefghijklmnopqrstuv/",
        "/admin/../Abcdefghijklmnopqrstuv/",
        "/admin/%2e%2e/Abcdefghijklmnopqrstuv/",
        "/admin/%2E/",
        "/admin/logg-inn/",
        "/admin/logg-inn",
        "/admin/logg-ut/",
        "javascript:alert(1)",
        "admin/",
    ],
)
def test_next_outside_admin_is_ignored(couple, target):
    """NFR-4: another site or a guest page (a link code) is never where a login leads."""
    response = log_in(Client(), next=target)

    assert response["Location"] == "/admin/"
    page = Client().get(f"{LOGIN}?next={quote(target, safe='')}")
    assert f'name="next" value="{target}"' not in page.content.decode()


@pytest.mark.parametrize(
    ("username", "password"),
    [("rikke", "feil-passord"), ("ukjent", PASSWORD), ("", ""), ("rikke", "")],
)
def test_a_failed_login_shows_one_notice_and_keeps_the_username(couple, username, password):
    """FR-46, NFR-4: 200, the notice with focus, the username kept, the password empty,
    no session."""
    client = Client()

    response = log_in(client, username, password)

    html = response.content.decode()
    assert response.status_code == 200
    assert 'class="notice notice--error"' in html
    assert "autofocus" in html
    assert 'tabindex="-1"' in html
    assert f'value="{username}"' in html
    assert 'name="password"' in html
    assert password == "" or password not in html
    assert Session.objects.count() == 0
    assert client.get("/admin/")["Location"].startswith(LOGIN)


@pytest.mark.parametrize("username", ["rikke", "ukjent"])
def test_every_wrong_login_says_the_same_thing(couple, username):
    """NFR-4: the page never says which usernames exist."""
    html = log_in(Client(), username, "feil-passord").content.decode()

    assert LOGIN_FAILED in page_text(html)


def test_an_inactive_account_gets_the_same_notice(couple):
    """FR-46, AD-10: a disabled account cannot log in and is not told so."""
    User.objects.filter(pk=couple.pk).update(is_active=False)

    response = log_in(Client())

    assert response.status_code == 200
    assert LOGIN_FAILED in page_text(response.content.decode())


def test_an_invalid_role_is_refused_by_the_form():
    """AD-10: an account whose role is neither couple nor helper is refused with the
    same text. The database constraint stops such a row, so the form is called directly."""
    form = AdminLoginForm(data={"username": "x", "password": "y"})
    with pytest.raises(ValidationError, match=LOGIN_FAILED):
        form.confirm_login_allowed(User(username="x", role="admin"))


def test_a_blank_field_is_named_in_the_notice(couple):
    """FR-46: an empty username gives its own short message, as a notice."""
    html = log_in(Client(), "", PASSWORD).content.decode()

    assert "Skriv inn brukernavnet." in page_text(html)


def test_logged_out_pages_redirect_to_the_login_with_next(db):
    """FR-46, AD-10: `/admin/` and any page under it, known or not, go to the login."""
    client = Client()

    for path in ("/admin/", "/admin/hei/", "/admin/program/"):
        response = client.get(path)
        assert response.status_code == 302
        assert response["Location"] == f"{LOGIN}?next={path}"


def test_a_logged_in_visitor_on_the_login_page_goes_to_oversikt(couple):
    """FR-46: nothing to log in to twice."""
    client = Client()
    log_in(client)

    assert client.get(LOGIN)["Location"] == "/admin/"


def test_the_session_cookie_is_scoped_to_admin_and_http_only(couple, settings):
    """NFR-4, AD-13: path `/admin/`, HttpOnly; the marker cookie sits there too."""
    response = log_in(Client())

    session = response.cookies[settings.SESSION_COOKIE_NAME]
    assert session["path"] == "/admin/"
    assert session["httponly"]
    seen = response.cookies["admin_seen"]
    assert (seen["path"], seen.value) == ("/admin/", "1")
    assert seen["httponly"]
    assert settings.SESSION_COOKIE_AGE == 20 * 60 * 60
    assert settings.SESSION_SAVE_EVERY_REQUEST is True
    assert settings.SESSION_COOKIE_PATH == "/admin/"


def test_a_request_renews_the_session(couple):
    """AD-13: every request moves the expiry 20 hours ahead."""
    client = Client()
    log_in(client)
    session = Session.objects.get()
    Session.objects.filter(pk=session.pk).update(
        expire_date=timezone.now() + datetime.timedelta(hours=1)
    )

    client.get("/admin/")

    renewed = Session.objects.get().expire_date
    assert renewed > timezone.now() + datetime.timedelta(hours=19)


def test_an_expired_session_redirects_and_says_so_once(couple):
    """FR-46, AD-13: after 20 hours without use the next request goes to the login page,
    which says why once; the marker cookie is then deleted."""
    client = Client()
    log_in(client)
    Session.objects.update(expire_date=timezone.now() - datetime.timedelta(seconds=1))

    response = client.get("/admin/")
    assert response["Location"] == f"{LOGIN}?next=/admin/"

    first = client.get(response["Location"])
    assert EXPIRED in page_text(first.content.decode())
    assert first.cookies["admin_seen"]["max-age"] == 0
    client.cookies.pop("admin_seen", None)  # the browser drops a deleted cookie
    again = client.get(LOGIN)
    assert EXPIRED not in page_text(again.content.decode())


def test_the_expired_notice_is_not_shown_after_a_wrong_login(couple):
    """FR-46: only the first visit to the login page says it, never a failed attempt."""
    client = Client()
    client.cookies["admin_seen"] = "1"

    html = log_in(client, password="feil-passord").content.decode()

    assert EXPIRED not in page_text(html)
    assert LOGIN_FAILED in page_text(html)


def test_a_visitor_who_never_logged_in_sees_no_expired_notice(db):
    """AD-13: without the marker cookie the login page is just the login page."""
    assert EXPIRED not in page_text(Client().get(LOGIN).content.decode())


def test_logout_needs_post_and_ends_the_session_without_the_expired_notice(couple):
    """FR-46, AD-13: GET is refused; POST flushes the session, deletes the marker and
    goes to the login page, which shows no expired notice."""
    client = Client()
    log_in(client)
    assert client.get("/admin/logg-ut/").status_code == 405

    response = client.post("/admin/logg-ut/")

    assert (response.status_code, response["Location"]) == (302, LOGIN)
    assert response.cookies["admin_seen"]["max-age"] == 0
    assert Session.objects.count() == 0
    client.cookies.pop("admin_seen", None)
    assert client.get("/admin/")["Location"].startswith(LOGIN)
    assert EXPIRED not in page_text(client.get(LOGIN).content.decode())


def test_logout_without_a_session_just_goes_to_the_login(db):
    """FR-46: a logout posted after the session ended is harmless."""
    response = Client().post("/admin/logg-ut/")

    assert (response.status_code, response["Location"]) == (302, LOGIN)


def test_the_password_is_stored_hashed_with_the_real_hasher(db, settings):
    """NFR-4, AD-10: Django's default hasher, never the password itself."""
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    ]
    user = User.objects.create_user(username="rikke", password=PASSWORD, role=User.Role.COUPLE)

    assert user.password.startswith("pbkdf2_sha256$")
    assert PASSWORD not in user.password


def test_admin_responses_are_not_cached(couple):
    """AD-15, AD-13: login, Oversikt, a redirect and the couple's 404 all say no-store."""
    client = Client()
    for response in (client.get(LOGIN), client.get("/admin/"), log_in(client)):
        assert "no-store" in response["Cache-Control"]
    for path in ("/admin/", "/admin/hei/"):
        assert "no-store" in client.get(path)["Cache-Control"]


def test_guest_requests_still_create_no_session(seeded):
    """AD-8, AD-10: opening a guest link or `/` writes no row and sets no cookie."""
    before = row_counts()
    client = Client()

    for path in (f"/{CODE}/", f"/{CODE}/program/", "/", "/robots.txt"):
        response = client.get(path)
        assert not response.cookies, path

    assert row_counts() == before


def test_a_logged_in_visitor_sent_to_the_login_itself_goes_to_oversikt(couple):
    """NFR-4: `next` pointing at the login page is dropped, so no ValueError (500)."""
    client = Client()
    log_in(client)

    response = client.get(f"{LOGIN}?next=/admin/logg-inn/")

    assert (response.status_code, response["Location"]) == (302, "/admin/")


def test_the_hidden_next_field_carries_the_page_through_the_login(couple):
    """FR-46: the login page holds `next`, and posting its own fields leads there."""
    client = Client()
    html = client.get(f"{LOGIN}?next=/admin/hei/").content.decode()

    assert '<input type="hidden" name="next" value="/admin/hei/">' in html
    fields = dict(re.findall(r'<input type="hidden" name="(\w+)" value="([^"]*)">', html))
    response = client.post(LOGIN, {**fields, "username": "rikke", "password": PASSWORD})

    assert response["Location"] == "/admin/hei/"


@pytest.mark.parametrize("page", ["logg-inn", "logg-ut"])
def test_login_and_logout_without_a_slash_redirect_with_the_query(db, page):
    """FR-46: `/admin/logg-inn` is not swallowed by the catch-all."""
    response = Client().get(f"/admin/{page}?next=/admin/hei/")

    assert response.status_code == 301
    assert response["Location"] == f"/admin/{page}/?next=/admin/hei/"


def test_the_marker_survives_a_logged_in_visit_and_a_head_request(couple):
    """AD-13: only a GET by a visitor who is not logged in reads and clears `admin_seen`."""
    client = Client()
    log_in(client)
    assert "admin_seen" not in client.get(LOGIN).cookies

    other = Client()
    other.cookies["admin_seen"] = "1"
    assert "admin_seen" not in other.head(LOGIN).cookies
    assert EXPIRED in page_text(other.get(LOGIN).content.decode())
