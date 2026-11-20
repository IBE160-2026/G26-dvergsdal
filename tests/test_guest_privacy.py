"""Guest pages stay private: headers, link previews and robots.txt (Story 1.4c).

FR-4, NFR-4, AD-15. Every row of the story's I/O matrix except the log rows
(those are in test_log_masking.py): `X-Robots-Tag: noindex` and
`Referrer-Policy: same-origin` on pages, redirects, robots.txt and static
files; one robots meta tag and one fixed set of Open Graph tags that are the
same for every code and name nobody; `/robots.txt` routed above the catch-all;
and `rel="noreferrer"` on every external link in the templates. What a real
browser and a real chat app show is MT-8 and MT-10 in docs/manual-test-plan.md.
"""

import re
import tomllib
from html.parser import HTMLParser
from io import StringIO
from pathlib import Path

import pytest
from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.test import Client

BASE_DIR = Path(__file__).resolve().parent.parent
SEED = tomllib.loads((BASE_DIR / "wedding" / "fixtures" / "seed.toml").read_text(encoding="utf-8"))
TEMPLATE_DIRS = (BASE_DIR / "wedding" / "templates", BASE_DIR / "guests" / "templates")

UNKNOWN_CODE = "AAAAAAAAAAAAAAAAAAAAAA"
PREVIEW = {
    "og:type": "website",
    "og:locale": "nb_NO",
    "og:title": "Invitasjon",
    "og:description": "En personlig invitasjon. Åpne lenken for å se den.",
    "og:image": "http://testserver/static/img/forhandsvisning.jpg",
    "og:image:width": "1000",
    "og:image:height": "525",
    "og:image:alt": (
        "Akvarell av et gammelt tun med et lite klokketårn, et våningshus og furutrær."
    ),
}
ROBOTS_TXT = (
    "# Every page says noindex in a meta tag and an X-Robots-Tag header (AD-15).\n"
    "# Search engines must be allowed to fetch a page to read that, so nothing is blocked.\n"
    "User-agent: *\n"
    "Disallow:\n"
)

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def local_env(monkeypatch):
    """The examiner's machine: no APP_ENV set (NFR-8), so the seed command runs."""
    monkeypatch.delenv("APP_ENV", raising=False)


@pytest.fixture
def seeded_codes() -> list[str]:
    """The seed loaded; the first guest's code in household 1 and in household 2."""
    call_command("seed_testdata", stdout=StringIO())
    return [household["guests"][0]["code"] for household in SEED["households"][:2]]


class _HeadTags(HTMLParser):
    """The `<title>` text and every `<meta>` tag's attributes in a page."""

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.metas: list[dict[str, str]] = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.metas.append({name: value or "" for name, value in attrs})

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def _head_tags(html: str) -> _HeadTags:
    parser = _HeadTags()
    parser.feed(html)
    return parser


def _preview(html: str) -> dict[str, str]:
    """The page title and every Open Graph tag, as the link previewer reads them."""
    tags = _head_tags(html)
    preview = {"title": tags.title}
    for meta in tags.metas:
        if meta.get("property", "").startswith("og:"):
            assert meta["property"] not in preview, f"{meta['property']} twice"
            preview[meta["property"]] = meta["content"]
    return preview


def _assert_private_headers(response) -> None:
    assert response["X-Robots-Tag"] == "noindex"
    assert response["Referrer-Policy"] == "same-origin"


# Headers (AD-15)


@pytest.mark.parametrize(
    ("path", "status"),
    [
        ("/", 200),
        (f"/{UNKNOWN_CODE}/", 404),
        ("/stil/", 200),
        ("/hei", 301),
        ("/robots.txt", 200),
    ],
)
def test_every_response_says_noindex_and_same_origin(client, path, status):
    """AD-15, NFR-4: pages, the APPEND_SLASH redirect and robots.txt all carry
    `X-Robots-Tag: noindex` and `Referrer-Policy: same-origin`."""
    response = client.get(path)
    assert response.status_code == status
    _assert_private_headers(response)


def test_a_seeded_test_link_says_noindex_and_same_origin(client, seeded_codes):
    """AD-15: a real guest link carries the same headers."""
    response = client.get(f"/{seeded_codes[0]}/")
    assert response.status_code == 404  # G1 until Story 1.5
    _assert_private_headers(response)


def test_static_files_say_noindex(settings):
    """AD-15: the noindex middleware runs before WhiteNoise, so an image fetched on
    its own (the og:image) carries the header too, and it answers 200 image/jpeg."""
    settings.WHITENOISE_USE_FINDERS = True
    settings.WHITENOISE_AUTOREFRESH = True
    response = Client().get("/static/img/forhandsvisning.jpg")
    assert response.status_code == 200
    assert response["Content-Type"] == "image/jpeg"
    _assert_private_headers(response)


def test_noindex_middleware_comes_before_whitenoise(settings):
    """AD-15: directly after SecurityMiddleware and before WhiteNoise, which answers
    static files without calling the middleware after it."""
    middleware = settings.MIDDLEWARE
    noindex = middleware.index("config.middleware.noindex_middleware")
    assert middleware[noindex - 1] == "django.middleware.security.SecurityMiddleware"
    assert noindex < middleware.index("whitenoise.middleware.WhiteNoiseMiddleware")


def test_referrer_policy_is_set_explicitly_to_same_origin(settings):
    """AD-15: never `no-referrer`, which makes Django's CSRF check reject forms."""
    assert settings.SECURE_REFERRER_POLICY == "same-origin"


# The page head: noindex and the link preview (FR-4)


def test_bare_address_has_one_robots_meta_and_the_fixed_preview(client, assert_loads_only_own_host):
    """FR-4, AD-15: `/` on an empty database has exactly one robots meta tag, the
    fixed Open Graph tags and the title «Invitasjon», and names no other site."""
    response = client.get("/")
    html = response.content.decode()
    robots = [meta for meta in _head_tags(html).metas if meta.get("name") == "robots"]
    assert robots == [{"name": "robots", "content": "noindex"}]
    assert _preview(html) == {"title": "Invitasjon", **PREVIEW}
    assert html.count("<title>") == 1
    assert_loads_only_own_host(html)
    for absent in ("og:url", 'rel="canonical"', "og:site_name", "twitter:"):
        assert absent not in html, absent


def test_preview_is_the_same_for_every_code_and_names_nobody(client, seeded_codes):
    """FR-4: two guests in different households and an unknown code get the same
    title and Open Graph tags as `/`, and none of them names a guest, the couple,
    their initials, the year or the place."""
    previews = [
        _preview(client.get(path).content.decode())
        for path in ["/", *(f"/{code}/" for code in seeded_codes), f"/{UNKNOWN_CODE}/"]
    ]
    assert all(preview == previews[0] for preview in previews)
    text = " ".join(previews[0].values())
    names = [guest["name"] for household in SEED["households"] for guest in household["guests"]]
    names += [SEED["settings"]["contact_1_name"], SEED["settings"]["contact_2_name"]]
    for name in names:
        assert not re.search(rf"\b{re.escape(name)}\b", text), name
    for forbidden in ("R & V", "R &amp; V", "2028", "Hardingasete"):
        assert forbidden not in text, forbidden


def test_preview_tags_sit_outside_every_block():
    """FR-4: the robots meta and the preview include are in base.html's head outside
    every `{% block %}`, so no page can change them for one guest."""
    source = (BASE_DIR / "wedding" / "templates" / "wedding" / "base.html").read_text(
        encoding="utf-8"
    )
    head = source[source.index("<head>") : source.index("</head>")]
    outside = re.sub(r"{% block (\w+) %}.*?{% endblock \1 %}", "", head, flags=re.DOTALL)
    assert '<meta name="robots" content="noindex">' in outside
    assert '{% include "wedding/components/link-preview.html" %}' in outside


def test_preview_image_is_a_static_file():
    """FR-4: the og:image path is a file the static finders know, so it is served
    from our own host."""
    path = PREVIEW["og:image"].removeprefix("http://testserver/static/")
    assert finders.find(path) is not None


# robots.txt (NFR-4, deferred work from 1.4b)


def test_robots_txt_allows_crawling_and_is_not_g1(client, django_assert_num_queries):
    """NFR-4, AD-15: `/robots.txt` is routed above `<str:code>/`: plain text with
    the exact body, not the G1 page, and it reads nothing from the database. It
    blocks nothing, so crawlers can read every page's `noindex`."""
    with django_assert_num_queries(0):
        response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response["Content-Type"] == "text/plain; charset=utf-8"
    assert response.content.decode() == ROBOTS_TXT
    assert [template.name for template in response.templates] == ["wedding/robots.txt"]
    assert "Disallow: /" not in response.content.decode()


# External links (AD-15)

_EXTERNAL_LINK = re.compile(r"""<a\b[^>]*\bhref=["']?https?:[^>]*>""", re.IGNORECASE)


def _links_without_noreferrer(html: str) -> list[str]:
    """Every `<a href="http…">` tag whose `rel` does not include `noreferrer`."""
    return [
        tag
        for tag in _EXTERNAL_LINK.findall(html)
        if not re.search(r"""\brel=["'][^"']*\bnoreferrer\b""", tag)
    ]


def test_noreferrer_checker_finds_a_bare_external_link():
    """The checker below is proved on one good and one bad sample."""
    good = '<a href="https://example.com/" rel="noreferrer">Kart</a>'
    bad = '<a class="lenke" href="https://example.com/">Kart</a>'
    assert _links_without_noreferrer(good) == []
    assert _links_without_noreferrer(bad) == ['<a class="lenke" href="https://example.com/">']


@pytest.mark.parametrize(
    "path",
    sorted(path for folder in TEMPLATE_DIRS for path in folder.rglob("*.html")),
    ids=lambda path: path.name,
)
def test_every_external_link_has_noreferrer(path):
    """AD-15: an external link never tells the other site which guest page the
    visitor came from."""
    assert _links_without_noreferrer(path.read_text(encoding="utf-8")) == []
