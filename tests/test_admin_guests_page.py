"""Gjester, the admin page A4, with the seed data (Story 3.4; FR-48, FR-57, UX-DR42, UX-DR49).

Counts and totals are read from expected.toml, never written here. The view model's order and
lines are tested on small facts in test_guest_list.py.
"""

import re

import pytest
from django.test import Client

from tests.helpers import (
    HELPER_LINE,
    load_expected,
    log_in_as,
    log_in_as_new_couple,
    main_html,
    page_text,
)
from wedding.models import Guest, Household
from wedding.rules.households import household_names

EXPECTED = load_expected()
URL = "/admin/gjester/"


def rows_of(html):
    """Every `li` of the household list: (its id, its text)."""
    main = main_html(html)
    return [
        (attributes, page_text(body))
        for attributes, body in re.findall(r'<li id="([^"]*)">(.*?)</li>', main, re.DOTALL)
    ]


@pytest.fixture
def page(seeded_with_answers):
    return log_in_as("testpar").get(URL).content.decode()


def test_the_counts_and_one_row_per_household_come_from_expected_toml(page):
    """FR-57, UX-DR42: «7 husstander · 14 gjester» and one `li` per household."""
    households = EXPECTED["counts"]["households"]["total"]
    people = sum(EXPECTED["counts"]["people"].values())
    text = page_text(main_html(page))

    assert '<h1 class="admin-title">Gjester</h1>' in page
    assert f"{households} husstander · {people} gjester" in text
    assert len(rows_of(page)) == households == Household.objects.count()


def test_the_household_not_answered_is_first_with_the_tag(page):
    """FR-57, UX-DR17: «Ikke svart» as tag (icon and word) on mona's household only, which is
    first, with the unanswered line."""
    rows = rows_of(page)
    tagged = [row for row in rows if "Ikke svart" in row[1]]

    assert tagged == rows[:1]
    assert rows[0][1].startswith(household_names(["Mona", "Geir"]))
    assert "Har ikke svart ennå" in rows[0][1]
    assert page.count('class="status-tag"') == EXPECTED["counts"]["households"]["not_answered"]
    assert re.search(r'class="status-tag">\s*<svg[^>]*aria-hidden="true"', page)


def test_each_household_shows_its_total_from_expected_toml(page):
    """FR-33, FR-57: «Totalt N kr» for the households that come, «Kommer ikke» for tor's."""
    for key, expected in EXPECTED["households"].items():
        guest = Guest.objects.get(name__iexact=key)
        text = next(text for id_, text in rows_of(page) if id_ == f"husstand-{guest.household_id}")
        if EXPECTED["guests"][key]["status"] == "coming":
            amount = f"{expected['total']:,}".replace(",", " ")
            assert f"Totalt {amount} kr" in text.replace("\N{NO-BREAK SPACE}", " "), key
        elif EXPECTED["guests"][key]["status"] == "not_coming":
            assert "Kommer ikke" in text, key
            assert "Ikke svart" not in text, key
            assert "Totalt" not in text, key


def test_every_row_has_an_anchor_with_the_household_id(page):
    """FR-55, FR-57: `husstand-<id>` for the links of the count pages."""
    assert {id_ for id_, _ in rows_of(page)} == {
        f"husstand-{id_}" for id_ in Household.objects.values_list("id", flat=True)
    }


def test_no_allergy_text_and_a_link_to_the_allergy_list(page):
    """FR-58, NFR-3: allergy details live only on the allergy list."""
    text = page_text(main_html(page)).lower()

    for word in ("gluten", "skalldyr", "nøtter", "laktose", "vegetar", "samtykke"):
        assert word not in text
    assert re.search(r'<a class="count-back" href="/admin/allergier/">Allergilisten</a>', page)


def test_no_households_say_so(db):
    """UX-DR42: the empty state, with a zero count line."""
    html = log_in_as_new_couple().get(URL).content.decode()

    assert "0 husstander · 0 gjester" in page_text(html)
    assert "Ingen husstander ennå." in html
    assert rows_of(html) == []


def test_logged_out_goes_to_login_with_next(db):
    """FR-46: 302 to the login page, keeping the page as `next`."""
    response = Client().get(URL)

    assert response.status_code == 302
    assert response["Location"] == f"/admin/logg-inn/?next={URL}"


def test_helper_sees_the_same_page_and_the_read_only_line(seeded_with_answers):
    """UX-DR49: helpers read everything; the couple see no such line."""
    helper = log_in_as("testhjelper").get(URL).content.decode()
    couple = log_in_as("testpar").get(URL).content.decode()

    assert HELPER_LINE in helper
    assert HELPER_LINE not in couple
    assert rows_of(helper) == rows_of(couple)


def test_the_nav_marks_gjester_as_the_open_page(page):
    """UX-DR34: Gjester is a link with `aria-current`, Oversikt is not marked."""
    nav = " ".join(page.split())

    assert 'href="/admin/gjester/" aria-current="page">Gjester</a>' in nav
    assert 'aria-current="page">Oversikt' not in nav


def test_only_get_and_head_are_allowed(seeded_with_answers):
    """AD-10: `require_safe`."""
    assert log_in_as("testpar").post(URL).status_code == 405
