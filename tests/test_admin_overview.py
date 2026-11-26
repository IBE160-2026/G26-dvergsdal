"""Oversikt with the seed data (Story 3.2; FR-46, FR-48, FR-54, UX-DR39, UX-DR40, UX-DR49).

The Svar panel and the six summary panels as HTML, the helper's read-only line, and
that the login page, the error pages and the couple's own view show no such line.
Numbers are read from expected.toml; their values are asserted in test_overview.py.
"""

import re
import tomllib
from pathlib import Path

import pytest
from django.test import Client

from tests.helpers import main_html, page_text, sections_of
from wedding.models import User

EXPECTED = tomllib.loads(
    (Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "expected.toml").read_text(
        encoding="utf-8"
    )
)
PASSWORD = "bryllup-test-2028"
HELPER_LINE = "Du kan se alt, men ikke endre noe."
PANELS = [
    "Svar",
    "Når kommer de?",
    "Overnatting",
    "Mat",
    "Allergier (med samtykke)",
    "Fjelltur fredag",
    "Betaling (husstander som kommer)",
]


def log_in_as(username):
    client = Client()
    assert client.post("/admin/logg-inn/", {"username": username, "password": PASSWORD}).status_code
    return client


@pytest.fixture
def couple_page(seeded_with_answers):
    """The couple's Oversikt, from the seeded users `testpar` and `testhjelper`."""
    return log_in_as("testpar").get("/admin/").content.decode()


def test_the_svar_panel_and_the_six_panels_come_in_order(couple_page):
    """FR-54, UX-DR39, UX-DR40: one `h2` per panel, in the order of the epics."""
    main = main_html(couple_page)

    assert re.findall(r"<h2[^>]*>(.*?)</h2>", main) == PANELS
    assert len(sections_of(main)) == len(PANELS)


def test_the_svar_panel_has_the_line_a_decorative_bar_and_the_rows(couple_page):
    """FR-48, UX-DR39: «Svart: X av Y husstander» from expected.toml, `aria-hidden` bar,
    the three rows and «Se hva alle har svart» as plain text."""
    households = EXPECTED["counts"]["households"]
    people = EXPECTED["counts"]["people"]
    svar = sections_of(main_html(couple_page))[0][1]
    text = page_text(svar)

    assert f"Svart: {households['answered']} av {households['total']} husstander" in text
    assert re.search(r'class="answer-bar"[^>]*aria-hidden="true"', svar)
    assert f"Kommer {people['coming']} personer · {households['coming']} husstander" in text
    assert (
        f"Kommer ikke {people['not_coming']} personer · {households['not_coming']} husstand" in text
    )
    assert f"Ikke svart ennå {people['not_answered']} personer" in text
    assert "Se hva alle har svart" in text
    assert "<a" not in svar


def test_the_panels_show_numbers_as_plain_text_without_links(couple_page):
    """UX-DR40: every count is plain text until Story 3.3; a 0 is never a link."""
    main = main_html(couple_page)
    text = page_text(main)

    assert "<a" not in main
    assert "Senger totalt" in text
    assert "Lunsj lørdag" in text
    hike = EXPECTED["counts"]["hike"]
    assert f"{hike['yes']} ja, {hike['maybe']} kanskje" in text
    assert "Stemmer ikke" not in text


def test_the_couple_sees_no_read_only_line(couple_page):
    """UX-DR49: the line is for helpers only."""
    assert HELPER_LINE not in couple_page


def test_a_helper_sees_the_same_numbers_and_the_line_under_the_nav(seeded_with_answers):
    """FR-46, UX-DR49: the line stands after the `nav` and before the `main`."""
    html = log_in_as("testhjelper").get("/admin/").content.decode()
    couple = log_in_as("testpar").get("/admin/").content.decode()

    assert html.index("</nav>") < html.index(HELPER_LINE) < html.index("<main")
    assert page_text(main_html(html)) == page_text(main_html(couple))


def test_the_helper_line_is_not_on_the_login_page_or_error_pages(db):
    """UX-DR49: no line on the login page, nor on an error page, not even for a helper."""
    User.objects.create_user(username="hjelper", password=PASSWORD, role=User.Role.HELPER)
    client = Client()
    client.post("/admin/logg-inn/", {"username": "hjelper", "password": PASSWORD})
    error = client.get("/admin/finnes-ikke/")

    assert error.status_code == 404
    assert "Til oversikten" in error.content.decode()
    assert HELPER_LINE not in error.content.decode()
    assert HELPER_LINE not in Client().get("/admin/logg-inn/").content.decode()


def test_logged_out_oversikt_redirects_to_the_login(db):
    """FR-46: unchanged by this story."""
    response = Client().get("/admin/")

    assert response.status_code == 302
    assert response["Location"] == "/admin/logg-inn/?next=/admin/"


def test_no_data_shows_zero_without_error(db):
    """FR-54: an empty database renders «Svart: 0 av 0 husstander» and a 0 % bar."""
    User.objects.create_user(username="rikke", password=PASSWORD, role=User.Role.COUPLE)
    client = Client()
    client.post("/admin/logg-inn/", {"username": "rikke", "password": PASSWORD})
    page = client.get("/admin/").content.decode()

    assert "Svart: 0 av 0 husstander" in page_text(page)
    assert 'style="width: 0%"' in page
