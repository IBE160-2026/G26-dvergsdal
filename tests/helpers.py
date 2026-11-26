"""Helpers and constants shared by several test modules (Story 1.5, 1.6, 1.7, 1.8, 2.1, 2.2, 3.1).

Fixtures live in conftest.py; plain values and functions that tests import live
here.
"""

import re
import tomllib
from pathlib import Path

from django.contrib.sessions.models import Session
from django.test import Client

from wedding.actors import AdminActor
from wedding.models import Guest, Household, Settings, Submission, User

# NFR-7, UX-DR4: the nine images the front page shows (Story 1.4b plans them,
# test_images.py keeps them within their budget, test_front_page.py checks that
# the rendered page shows exactly these).
FRONT_PAGE = (
    "segl.png",
    "illustrasjon.jpg",
    "brudeslor.png",
    "lilje-topp.png",
    "lilje-bunn.png",
    "blonde.png",
    "sted-middag.jpg",
    "sted-tunet.jpg",
    "oss-strand.jpg",
)

# FR-5, Story 1.8: what an impersonal page (G1 and the error pages without a
# valid link) may never hold: the year, the place, the seal, the couple's
# initials, a nav bar, the footer band or a phone link. Used by
# test_private_invitation.py and test_error_pages.py.
IMPERSONAL_FORBIDDEN = (
    "2028",
    "Hardingasete",
    "Strandebarm",
    "segl",
    "R &amp; V",
    "R & V",
    "<nav",
    "<footer",
    "tel:",
)


FIXTURES = Path(__file__).resolve().parent.parent / "wedding" / "fixtures"

PASSWORD = "bryllup-test-2028"
# UX-DR49: the line a helper sees under the admin nav.
HELPER_LINE = "Du kan se alt, men ikke endre noe."
# Story 7.2 loads Synne's withdrawn consent. Until then the seed stores her nut allergy, so the
# app shows one nut allergy, one more `has_allergies` and one fewer `nothing_stored` than
# expected.toml. Story 7.2 removes this constant and every addition of it in the tests.
SYNNE_UNTIL_7_2 = 1


def load_expected() -> dict:
    """FR-69, AD-16: the hand-worked expected-results list, `wedding/fixtures/expected.toml`,
    read in one place for every test that compares the app with it."""
    return tomllib.loads((FIXTURES / "expected.toml").read_text(encoding="utf-8"))


def tel_rows(html: str) -> list[tuple[str, str]]:
    """FR-6: the footer band's `tel:` rows of a page as (link, text)."""
    footer = html[html.index("<footer") : html.index("</footer>")]
    return re.findall(r'<a href="(tel:[^"]*)">([^<]*)</a>', footer)


def log_in_as(username):
    """FR-46: a client logged in as the seeded account `username` (`testpar`, `testhjelper`)."""
    client = Client()
    assert client.post("/admin/logg-inn/", {"username": username, "password": PASSWORD}).status_code
    return client


def log_in_as_new_couple():
    """FR-46: a client logged in as a new couple account, for tests with an empty database."""
    User.objects.create_user(username="rikke", password=PASSWORD, role=User.Role.COUPLE)
    client = Client()
    client.login(username="rikke", password=PASSWORD)
    return client


def make_admin(role, username="rikke"):
    """AD-10 (Story 3.1): an `AdminActor` for a new account with `role`, for service tests."""
    return AdminActor(User.objects.create_user(username=username, role=role))


def page_text(html: str) -> str:
    """A page's text as a reader sees it: tags removed, whitespace collapsed."""
    return " ".join(re.sub(r"<[^>]+>", " ", html).split())


def tag_attrs(tag: str) -> dict[str, str]:
    """The attributes of one opening tag, as written."""
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))


def main_html(html: str) -> str:
    """The page's `main` element, from its opening tag to before `</main>`."""
    return html[html.index("<main") : html.index("</main>")]


def sections_of(html: str) -> list[tuple[dict[str, str], str]]:
    """Every `section` in `html` as (attributes, inner HTML)."""
    return [
        (tag_attrs(tag), body)
        for tag, body in re.findall(r"(<section\b[^>]*>)(.*?)</section>", html, re.DOTALL)
    ]


def row_counts() -> dict[str, int]:
    """FR-3, AD-8: the number of rows in every table a guest request could write,
    sessions included, so a test can check that a request wrote nothing."""
    return {
        model.__name__: model.objects.count()
        for model in (Household, Guest, Settings, User, Session, Submission)
    }


def checked_radios(html: str) -> dict[str, str]:
    """Every checked radio or checkbox in `html` as {name: value} (Story 2.1)."""
    found = {}
    for tag in re.findall(r"<input\b[^>]*>", html):
        if re.search(r"\schecked\b", tag):
            attributes = tag_attrs(tag)
            found[attributes["name"]] = attributes["value"]
    return found


def ticked_boxes(html: str) -> list[str]:
    """The ids of every checked checkbox in `html`, in page order (Story 2.2)."""
    return [
        tag_attrs(tag)["id"]
        for tag in re.findall(r"<input\b[^>]*>", html)
        if 'type="checkbox"' in tag and re.search(r"\schecked\b", tag)
    ]
