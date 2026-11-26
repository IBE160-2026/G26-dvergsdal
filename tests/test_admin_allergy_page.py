"""The allergy list, admin page A5, with the seed data (Story 3.4; FR-58, UX-DR48, AD-18, FR-26).

Counts come from expected.toml (with Synne's named offset until Story 7.2) and from Oversikt's own
number; consent is checked against the seed file, never with names written here.
"""

import datetime
import re
import tomllib
from pathlib import Path

import pytest
from django.test import Client

from tests.helpers import (
    HELPER_LINE,
    SYNNE_UNTIL_7_2,
    log_in_as,
    log_in_as_new_couple,
    main_html,
    page_text,
)
from wedding.models import Allergy, Consent, Guest

ROOT = Path(__file__).resolve().parent.parent / "wedding" / "fixtures"
EXPECTED = tomllib.loads((ROOT / "expected.toml").read_text(encoding="utf-8"))
SEED = tomllib.loads((ROOT / "seed.toml").read_text(encoding="utf-8"))
URL = "/admin/allergier/"
LABELS = {
    "gluten": "Gluten",
    "lactose": "Laktose",
    "nuts": "Nøtter",
    "shellfish": "Skalldyr",
    "vegetarian": "Vegetar",
    "vegan": "Vegan",
    "other": "Annet",
}


def seed_guests():
    """Every guest of seed.toml as a dict, by lower-case name."""
    return {
        guest["name"].lower(): guest
        for household in SEED["households"]
        for guest in household["guests"]
    }


def items(html):
    """Each `li` of the list as its text."""
    return [page_text(body) for body in re.findall(r"<li>(.*?)</li>", main_html(html), re.DOTALL)]


@pytest.fixture
def page(seeded_with_answers):
    return log_in_as("testpar").get(URL).content.decode()


def test_the_list_is_as_long_as_the_has_allergies_count(page):
    """FR-58, AD-18: one `li` per guest: expected.toml `has_allergies` plus Synne's offset, and
    the number Oversikt shows for «Har allergier eller matbehov»."""
    expected = EXPECTED["counts"]["allergy_states"]["has_allergies"] + SYNNE_UNTIL_7_2
    oversikt = page_text(log_in_as("testpar").get("/admin/").content.decode())

    assert len(items(page)) == expected
    assert f"{expected} personer" in page_text(main_html(page))
    assert f"Har allergier eller matbehov {expected} personer" in oversikt


def test_eva_and_bestemor_show_categories_and_note(page):
    """FR-58, UX-DR48: name, category labels in form order and the note."""
    rows = items(page)

    assert "Eva : Skalldyr, Annet . Tåler ikke koriander." in rows
    assert "bestemor : Gluten" in rows


def test_nothing_about_a_guest_without_consent_is_on_the_page(page):
    """FR-26, FR-58, AD-18: a guest without consent «Ja» is absent with name, categories and
    note: checked for every guest of the seed that expected.toml says has nothing stored."""
    text = page_text(main_html(page))
    guests = seed_guests()
    silent = [
        key
        for key, state in EXPECTED["guests"].items()
        if state.get("allergy_state") in ("nothing_stored", "no_allergies") and key != "synne"
    ]
    assert silent

    for key in silent:
        assert not re.search(rf"\b{re.escape(guests[key]['name'])}\b", text), key
        for category in guests[key].get("allergy_categories", ()):
            assert LABELS[category] not in text, key
        if note := guests[key].get("allergy_note"):
            assert note not in text, key


def test_a_withdrawn_consent_removes_the_guest_and_the_note(seeded_with_answers):
    """FR-26, FR-30, AD-18: a `Consent` withdrawn event takes Eva off the list, note included."""
    eva = Guest.objects.get(name="Eva")
    Consent.objects.create(
        guest=eva,
        event=Consent.WITHDRAWN,
        at=datetime.datetime(2030, 1, 1, tzinfo=datetime.UTC),
        given_by_name="Eva",
        text_version="test",
    )

    html = log_in_as("testpar").get(URL).content.decode()

    assert "Eva" not in page_text(main_html(html))
    assert "koriander" not in html
    assert len(items(html)) == (
        EXPECTED["counts"]["allergy_states"]["has_allergies"] + SYNNE_UNTIL_7_2 - 1
    )


def test_a_note_with_markup_is_shown_as_text(seeded_with_answers):
    """NFR-4: the note is autoescaped; its line breaks are kept in CSS."""
    Allergy.objects.filter(guest__name="Eva").update(note="<b>x</b>\nlinje to")

    html = log_in_as("testpar").get(URL).content.decode()

    assert "&lt;b&gt;x&lt;/b&gt;\nlinje to" in html
    assert "<b>x</b>" not in html


def test_nobody_with_consent_says_so(seeded_with_answers):
    """UX-DR48: the empty state and «0 personer»."""
    Consent.objects.all().delete()

    html = log_in_as("testpar").get(URL).content.decode()

    assert "Ingen allergier registrert ennå." in html
    assert "0 personer" in page_text(main_html(html))
    assert items(html) == []


def test_it_links_back_and_marks_no_nav_link_as_open(page):
    """UX A5: «Tilbake til Oversikt»; the list is a sub-page, so no nav link is current."""
    assert '<a class="count-back" href="/admin/">Tilbake til Oversikt</a>' in page
    assert "aria-current" not in page


def test_logged_out_goes_to_login_with_next(db):
    response = Client().get(URL)

    assert response.status_code == 302
    assert response["Location"] == f"/admin/logg-inn/?next={URL}"


def test_helper_sees_the_same_list_and_the_read_only_line(seeded_with_answers):
    """UX-DR49: helpers read everything."""
    helper = log_in_as("testhjelper").get(URL).content.decode()
    couple = log_in_as("testpar").get(URL).content.decode()

    assert HELPER_LINE in helper
    assert HELPER_LINE not in couple
    assert items(helper) == items(couple)


def test_only_get_and_head_are_allowed(seeded_with_answers):
    """AD-10: `require_safe`."""
    assert log_in_as("testpar").post(URL).status_code == 405


def test_an_empty_database_has_an_empty_list(db):
    """UX-DR48: no guests at all is the empty state, not an error."""
    html = log_in_as_new_couple().get(URL).content.decode()

    assert "Ingen allergier registrert ennå." in html
