"""The private-invitation page G1 (Story 1.4b, FR-5, UX-DR5, UX-DR30).

Every row of the story's I/O matrix: the bare address, unknown codes, a seeded
test link before Story 1.5, the seeded data that must not leak, and `/stil/`
with `APP_ENV` local and production. Each GET runs with
`django_assert_num_queries(0)`: G1 reads nothing, so it renders on an empty,
migrated database. How the page looks at 360, 320 and 180 CSS px and under
forced colours is MT-5 and MT-6 in docs/manual-test-plan.md.
"""

import re
import tomllib
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command

from wedding.models import Guest, Household

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
SEED_GUESTS = [guest for household in SEED["households"] for guest in household["guests"]]

HEADING = "Dette er en privat invitasjon"
HELP_LINE = "Virker ikke lenken din? Ta kontakt med brudeparet direkte."
UNKNOWN_CODES = ["AAAAAAAAAAAAAAAAAAAAAA", "hei"]
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

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def local_env(monkeypatch):
    """The examiner's machine: no APP_ENV set (NFR-8), so the seed command runs."""
    monkeypatch.delenv("APP_ENV", raising=False)


def _text(html: str) -> str:
    return " ".join(html.split())


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
        assert HELP_LINE in _text(html)
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


@pytest.mark.parametrize("code", UNKNOWN_CODES)
def test_unknown_code_shows_the_same_g1_with_404(
    client, assert_is_g1, django_assert_num_queries, code
):
    """FR-5: an unknown code gives 404 with the same G1 body as `/`, and no query;
    never Django's technical 404 page with the URL list."""
    with django_assert_num_queries(0):
        bare = client.get("/")
        response = client.get(f"/{code}/")
    assert response.status_code == 404
    html = assert_is_g1(response)
    assert html == bare.content.decode()
    assert "Page not found" not in html


def test_a_seeded_test_link_shows_g1_until_story_1_5(
    client, assert_is_g1, django_assert_num_queries
):
    """FR-5, Design Notes: before Story 1.5 there is no guest page, so a real test
    link also shows G1 with 404, and its code is not looked up."""
    call_command("seed_testdata", stdout=StringIO())
    code = SEED_GUESTS[0]["code"]
    assert Guest.objects.filter(code=code).exists()
    with django_assert_num_queries(0):
        response = client.get(f"/{code}/")
    assert response.status_code == 404
    assert_is_g1(response)


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
