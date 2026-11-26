"""The count pages A3 (Story 3.3; FR-46, FR-55, UX-DR41, AD-2).

Every slug in the registry is opened on the seed data: the rows equal the number on
Oversikt and the length of the rule's tuple, and the numbers expected.toml lists are
read from it (with Story 3.2's named offset for the allergy counts).
"""

import re
import tomllib
from pathlib import Path

import pytest
from django.test import Client

from dashboard.counts import COUNTS, DAY_COMBOS, HOUSEHOLDS, count_for, count_text, payment_statuses
from dashboard.overview import build_overview
from dashboard.selectors import guest_facts, household_totals
from tests.helpers import HELPER_LINE, SYNNE_UNTIL_7_2, log_in_as, main_html, page_text
from wedding.selectors import form_prices

EXPECTED = tomllib.loads(
    (Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "expected.toml").read_text(
        encoding="utf-8"
    )
)["counts"]
# slug -> the value expected.toml lists for it (Synne's offset until Story 7.2 loads her
# withdrawal).
KNOWN = {
    "kommer-personer": EXPECTED["people"]["coming"],
    "kommer-husstander": EXPECTED["households"]["coming"],
    "kommer-ikke-personer": EXPECTED["people"]["not_coming"],
    "ikke-svart-personer": EXPECTED["people"]["not_answered"],
    "hele-helgen": EXPECTED["days"]["whole_weekend"],
    "ikke-hele-helgen": EXPECTED["days"]["not_whole_weekend"],
    "senger": EXPECTED["overnight"]["beds"],
    "maltid-fredag-middag": EXPECTED["meals"]["friday_dinner"],
    "maltid-lordag-lunsj": EXPECTED["meals"]["saturday_lunch"],
    "tur-ja": EXPECTED["hike"]["yes"],
    "tur-kanskje": EXPECTED["hike"]["maybe"],
    "tur-nei": EXPECTED["hike"]["no"],
    "allergi-notter": EXPECTED["allergy_categories"]["nuts"] + SYNNE_UNTIL_7_2,
    "allergi-skalldyr": EXPECTED["allergy_categories"]["shellfish"],
    "allergi-har": EXPECTED["allergy_states"]["has_allergies"] + SYNNE_UNTIL_7_2,
    "allergi-ingen-lagret": EXPECTED["allergy_states"]["nothing_stored"] - SYNNE_UNTIL_7_2,
}


# The day sub-rows are left out on Oversikt at 0; every other count has its row there.
SUB_ROWS = {*(slug for slug, _, _ in DAY_COMBOS), "andre-kombinasjoner"}


@pytest.fixture
def couple(seeded_with_answers):
    return log_in_as("testpar")


def page(client, slug):
    return client.get(f"/admin/tall/{slug}/")


def items(html):
    return re.findall(r"<li>(.*?)</li>", main_html(html), re.DOTALL)


def heading(html):
    return page_text(re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL).group(1))


@pytest.mark.parametrize("count", COUNTS, ids=lambda count: count.slug)
def test_the_rows_equal_the_number_on_oversikt_and_the_rule_tuple(couple, count):
    """FR-55, AD-2: status 200; the `h1` count, the `li` items, the Oversikt number and the
    tuple's length are one number; the value expected.toml lists is that number."""
    facts = guest_facts()
    totals = household_totals(facts, form_prices())
    ids = count.ids(facts, payment_statuses(facts, totals))
    overview = build_overview(facts, totals)
    on_oversikt = [
        cell.count
        for row in (*overview.progress.rows, *(r for p in overview.panels for r in p.rows))
        for cell in row.cells
        if cell.slug == count.slug
    ]
    response = page(couple, count.slug)
    html = response.content.decode()

    assert response.status_code == 200
    assert heading(html) == f"{count.title}: {count_text(count.kind, len(ids))}"
    assert len(items(html)) == len(ids)
    if not ids:
        assert "Ingen husstander." in html or "Ingen personer." in html
    # The day sub-rows are left out on Oversikt at 0; every other count has its row there.
    if count.slug in SUB_ROWS and not ids:
        assert on_oversikt == []
    else:
        assert on_oversikt == [len(ids)]
    if count.slug in KNOWN:
        assert len(ids) == KNOWN[count.slug]


def test_the_people_page_lists_each_guest_with_the_household(couple):
    """FR-55: «Kommer: 9 personer», nine items in id order, name and household."""
    ids = count_for("kommer-personer").ids(guest_facts(), {})
    html = page(couple, "kommer-personer").content.decode()

    assert heading(html) == f"Kommer: {len(ids)} personer"
    assert len(items(html)) == len(ids)
    assert all("count-list__name" in i and "count-list__household" in i for i in items(html))


def test_the_households_page_names_each_household(couple):
    """FR-55: «Kommer: 5 husstander», five items."""
    html = page(couple, "kommer-husstander").content.decode()

    assert count_for("kommer-husstander").kind == HOUSEHOLDS
    assert heading(html) == f"Kommer: {EXPECTED['households']['coming']} husstander"
    assert len(items(html)) == EXPECTED["households"]["coming"]
    assert "count-list__name" not in html


def test_a_zero_count_shows_the_empty_text(couple):
    """UX-DR41: «Delbetalt» is 0 before payments exist; the address still answers."""
    html = page(couple, "betaling-delbetalt").content.decode()

    assert heading(html) == "Betaling: Delbetalt: 0 husstander"
    assert "Ingen husstander." in page_text(main_html(html))
    assert items(html) == []


def test_the_nuts_page_shows_names_only_no_allergy_text(couple):
    """FR-58, AD-18: no category, note or consent wording on a count page."""
    text = page_text(main_html(page(couple, "allergi-notter").content.decode())).lower()

    for word in ("gluten", "laktose", "skalldyr", "samtykke", "merknad"):
        assert word not in text
    assert "allergi: nøtter" in text


def test_an_unknown_slug_is_the_couples_own_404(couple):
    response = page(couple, "finnes-ikke")

    assert response.status_code == 404
    assert "Til oversikten" in response.content.decode()


def test_logged_out_goes_to_the_login_with_next(seeded_with_answers):
    response = Client().get("/admin/tall/kommer-personer/")

    assert response.status_code == 302
    assert response["Location"] == "/admin/logg-inn/?next=/admin/tall/kommer-personer/"


def test_a_helper_sees_the_same_list_and_the_line(seeded_with_answers):
    """FR-46, UX-DR49: both roles open the page; the helper also gets the read-only line."""
    helper = page(log_in_as("testhjelper"), "kommer-personer").content.decode()
    couple = page(log_in_as("testpar"), "kommer-personer").content.decode()

    assert HELPER_LINE in helper
    assert HELPER_LINE not in couple
    assert items(helper) == items(couple)


def test_oversikt_is_the_open_page_in_the_nav(couple):
    html = page(couple, "kommer-personer").content.decode()

    assert re.search(r'<a href="/admin/"\s+aria-current="page">Oversikt</a>', html)
    assert 'href="/admin/"' in main_html(html)


def test_the_page_answers_only_get(couple):
    assert couple.post("/admin/tall/kommer-personer/").status_code == 405


def household_links(html):
    """Every link to a row on Gjester in the page's list: (href, link text)."""
    return re.findall(
        r'<a [^>]*href="(/admin/gjester/#husstand-\d+)"[^>]*>(.*?)</a>', main_html(html), re.DOTALL
    )


def test_each_household_link_lands_on_its_row_on_gjester(couple):
    """FR-55, FR-57, UX-DR41 (Story 3.4): the names of every household on A3 link to the Gjester
    row with that household's id and names."""
    html = page(couple, "kommer-husstander").content.decode()
    links = household_links(html)

    assert len(links) == EXPECTED["households"]["coming"]
    for href, text in links:
        path, anchor = href.split("#")
        gjester = couple.get(path).content.decode()
        row = re.search(rf'<li id="{anchor}">(.*?)</li>', gjester, re.DOTALL)
        assert row, href
        assert page_text(text) in page_text(row.group(1))


def test_a_person_keeps_their_name_as_text_and_the_household_is_the_link(couple):
    """FR-55, UX-DR41: on a people page the name is text and the household names are the link."""
    html = page(couple, "kommer-personer").content.decode()
    links = household_links(html)

    assert len(links) == len(items(html))
    for item in items(html):
        name = re.search(r'<span class="count-list__name">(.*?)</span>', item).group(1)
        assert "<a" not in name
        assert 'class="count-list__household"' in item


def test_a_zero_count_has_no_household_link(couple):
    """UX-DR41: an empty list has no link to a household."""
    html = page(couple, "betaling-delbetalt").content.decode()

    assert household_links(html) == []
