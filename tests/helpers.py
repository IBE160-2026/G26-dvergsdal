"""Helpers and constants shared by several test modules (Story 1.5, 1.6, 1.7, 1.8, 2.1).

Fixtures live in conftest.py; plain values and functions that tests import live
here.
"""

import re

from django.contrib.sessions.models import Session

from wedding.models import Guest, Household, Settings, User

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
        for model in (Household, Guest, Settings, User, Session)
    }


def checked_radios(html: str) -> dict[str, str]:
    """Every checked radio or checkbox in `html` as {name: value} (Story 2.1)."""
    found = {}
    for tag in re.findall(r"<input\b[^>]*>", html):
        if re.search(r"\schecked\b", tag):
            attributes = tag_attrs(tag)
            found[attributes["name"]] = attributes["value"]
    return found
