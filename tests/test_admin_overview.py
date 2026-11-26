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

from tests.helpers import HELPER_LINE, PASSWORD, log_in_as, main_html, page_text, sections_of
from wedding.models import User

EXPECTED = tomllib.loads(
    (Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "expected.toml").read_text(
        encoding="utf-8"
    )
)
PANELS = [
    "Svar",
    "Når kommer de?",
    "Overnatting",
    "Mat",
    "Allergier (med samtykke)",
    "Fjelltur fredag",
    "Betaling (husstander som kommer)",
]


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
    assert "Se hva alle har svart" not in " ".join(re.findall(r"<a\b[^>]*>(.*?)</a>", svar))


def count_cells(main):
    """Every `dd` of Oversikt's rows: (the `dd` HTML, its row label)."""
    return [
        (dd, " ".join(re.sub(r"<[^>]+>", " ", dt).split()))
        for dt, dd in re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", main, re.DOTALL)
    ]


def test_counts_above_zero_are_links_and_zero_is_plain_text(couple_page):
    """UX-DR41, FR-55: a number above 0 is one link to its page with an `aria-label` that
    starts with the row label; a 0 has no `a`; no other link is new in `main`."""
    main = main_html(couple_page)
    links = re.findall(r"<a\b([^>]*)>(.*?)</a>", main, re.DOTALL)

    assert links
    row_labels = {label for _, label in count_cells(main)}
    for attrs, text in links:
        label = re.search(r'aria-label="([^"]*)"', attrs).group(1)
        assert re.search(r'href="/admin/tall/[a-z0-9-]+/"', attrs)
        assert label.endswith(f": {page_text(text)}")
        assert label.split(": ")[0] in row_labels
        assert not page_text(text).startswith("0")
    for dd, label in count_cells(main):
        numbers = re.sub(r"<a\b.*?</a>", "", dd, flags=re.DOTALL)
        assert not re.search(r"\b[1-9]\d* (person|husstand|ja|kanskje)", page_text(numbers)), label
        assert not re.search(r"<a\b[^>]*>\s*0", dd), label
    assert "Kommer: 9 personer" in main


def test_a_zero_count_is_plain_text_on_oversikt(couple_page):
    """UX-DR41: «Delbetalt» is 0 before payments exist; its number is text, not a link."""
    dd = next(dd for dd, label in count_cells(main_html(couple_page)) if label == "Delbetalt")

    assert page_text(dd) == "0 husstander"
    assert "<a" not in dd


def test_the_hike_row_has_one_link_per_number(couple_page):
    """FR-17, FR-55: «3 ja, 2 kanskje» is two links with their own addresses."""
    hike = EXPECTED["counts"]["hike"]
    dd = next(dd for dd, label in count_cells(main_html(couple_page)) if label == "Vil gå turen")

    assert re.findall(r'href="([^"]*)"', dd) == ["/admin/tall/tur-ja/", "/admin/tall/tur-kanskje/"]
    assert (
        " ".join(re.sub(r"<[^>]+>", "", dd).split()) == f"{hike['yes']} ja, {hike['maybe']} kanskje"
    )


def test_the_panels_show_the_rows_and_no_attention_item(couple_page):
    main = main_html(couple_page)
    text = page_text(main)

    assert "Senger totalt" in text
    assert "Lunsj lørdag" in text
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


def test_every_rendered_link_opens_a_page_with_the_same_number(seeded_with_answers):
    """FR-55, AD-2: follow each link on Oversikt; the `h1` number and the `li` count equal the
    number in the link text."""
    client = log_in_as("testpar")
    main = main_html(client.get("/admin/").content.decode())
    links = re.findall(r'<a\s[^>]*href="(/admin/tall/[^"]+)"[^>]*>(.*?)</a>', main, re.DOTALL)

    assert links
    for href, text in links:
        response = client.get(href)
        html = response.content.decode()
        number = re.match(r"\d+", page_text(text)).group()
        h1 = page_text(re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL).group(1))

        assert response.status_code == 200, href
        assert re.search(rf": {number}\b", h1), href
        assert len(re.findall(r"<li>", main_html(html))) == int(number), href
