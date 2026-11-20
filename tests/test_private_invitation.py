"""The private-invitation page G1 (Story 1.4b, FR-5, UX-DR5, UX-DR30).

Every row of the story's I/O matrix: the bare address, unknown codes, the
seeded data that must not leak, and `/stil/` with `APP_ENV` local and
production. Each GET counts its queries: G1 itself reads nothing, so it renders
on an empty, migrated database; since Story 1.5 a well-formed unknown code
costs the resolver's one lookup and a malformed one none, and a seeded test link
opens the invitation instead (test_front_page.py, test_info_pages.py). How the
page looks at 360, 320 and 180 CSS px and under forced colours is MT-5 and
MT-6 in docs/manual-test-plan.md.
"""

import re
import tomllib
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command

from tests.helpers import page_text
from wedding.models import Guest, Household

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
SEED_GUESTS = [guest for household in SEED["households"] for guest in household["guests"]]

HEADING = "Dette er en privat invitasjon"
HELP_LINE = "Virker ikke lenken din? Ta kontakt med brudeparet direkte."
# An unknown code in the right format costs the resolver's one lookup; a malformed
# one never reaches the database (AD-6).
UNKNOWN_CODES = [("AAAAAAAAAAAAAAAAAAAAAA", 1), ("hei", 0)]
# Nothing on G1 may name or place the wedding (FR-5, EXPERIENCE.md G1).
FORBIDDEN = [
    "2028",
    "Hardingasete",
    "Strandebarm",
    "segl",
    "R &amp; V",
    "R & V",
    "<nav",
    "<footer",
    "tel:",
]

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


@pytest.fixture
def assert_is_g1(assert_loads_only_own_host):
    """A checker that the response is the G1 page and nothing more; it returns
    the HTML. Every absolute address is our own host (AD-15, Story 1.4c)."""

    def check(response) -> str:
        html = response.content.decode()
        templates = [template.name for template in response.templates]
        assert "guests/private_invitation.html" in templates
        assert "wedding/base.html" in templates
        assert '<main class="column private-invitation">' in html
        assert '<div class="paper-sheet private-invitation__sheet">' in html
        assert f'<h1 class="private-invitation__heading">{HEADING}</h1>' in html
        assert HELP_LINE in page_text(html)
        flowers = re.search(r"<img[^>]*brudeslor\.png[^>]*>", html).group(0)
        assert 'alt=""' in flowers
        assert 'width="180"' in flowers
        for forbidden in FORBIDDEN:
            assert forbidden not in html, forbidden
        assert "favicon" not in html
        assert "apple-touch-icon" not in html
        icons = re.findall(r"<link[^>]*\bicon\b[^>]*>", html)
        assert icons == ['<link rel="icon" href="data:,">']
        assert_loads_only_own_host(html)
        return html

    return check


def test_bare_address_shows_g1_on_an_empty_database(
    client, assert_is_g1, django_assert_num_queries
):
    """FR-5: `/` on an empty, migrated database gives 200 and G1, with no query."""
    assert Household.objects.count() == 0
    with django_assert_num_queries(0):
        response = client.get("/")
    assert response.status_code == 200
    assert_is_g1(response)


@pytest.mark.parametrize(("code", "queries"), UNKNOWN_CODES)
def test_unknown_code_shows_the_same_g1_with_404(
    client, assert_is_g1, django_assert_num_queries, code, queries
):
    """FR-5, AD-6: an unknown code gives 404 with the same G1 body as `/`, after one
    lookup for a well-formed code and none for a malformed one; never Django's
    technical 404 page with the URL list."""
    with django_assert_num_queries(0):
        bare = client.get("/")
    with django_assert_num_queries(queries):
        response = client.get(f"/{code}/")
    assert response.status_code == 404
    html = assert_is_g1(response)
    assert html == bare.content.decode()
    assert "Page not found" not in html


def test_a_seeded_test_link_opens_the_invitation_not_g1(client):
    """FR-2, FR-5, Story 1.5: a real test link answers 200 with the front page, and
    nothing of G1."""
    call_command("seed_testdata", stdout=StringIO())
    code = SEED_GUESTS[0]["code"]
    assert Guest.objects.filter(code=code).exists()
    response = client.get(f"/{code}/")
    assert response.status_code == 200
    templates = [template.name for template in response.templates]
    assert "guests/front_page.html" in templates
    assert "guests/private_invitation.html" not in templates
    assert HEADING not in response.content.decode()


def test_seeded_data_never_reaches_g1(client, assert_is_g1):
    """FR-5, NFR-3: with the seed loaded, G1 holds no guest name, no couple name and
    no phone number, besides the year, the place, the seal, nav, footer or `tel:`."""
    call_command("seed_testdata", stdout=StringIO())
    html = assert_is_g1(client.get("/"))
    settings = SEED["settings"]
    names = [guest["name"] for guest in SEED_GUESTS]
    names += [settings["contact_1_name"], settings["contact_2_name"]]
    for name in names:
        assert not re.search(rf"\b{re.escape(name)}\b", html), name
    for phone in (settings["contact_1_phone"], settings["contact_2_phone"]):
        assert phone not in html
        assert phone.replace(" ", "")[-6:] not in html.replace(" ", "")


def test_style_sample_locally_is_the_sample(client):
    """Spec 1.4b matrix: with `APP_ENV` local `/stil/` is the style sample, because
    its pattern comes before `<str:code>/`."""
    response = client.get("/stil/")
    assert response.status_code == 200
    assert "guests/style_sample.html" in [template.name for template in response.templates]


def test_style_sample_in_production_is_g1(
    client, assert_is_g1, django_assert_num_queries, production_urls
):
    """Spec 1.4b matrix: with `APP_ENV=production` `/stil/` is read as a code and
    gives the G1 page with 404."""
    with django_assert_num_queries(0):
        response = client.get("/stil/")
    assert response.status_code == 404
    assert_is_g1(response)
