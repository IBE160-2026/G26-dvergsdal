"""Guest pages stay private: headers, link previews and robots.txt (Story 1.4c).

FR-4, NFR-4, AD-15. Every row of the story's I/O matrix except the log rows
(those are in test_log_masking.py): `X-Robots-Tag: noindex` and
`Referrer-Policy: same-origin` on pages, redirects, robots.txt and static
files; one robots meta tag and one fixed set of Open Graph tags that are the
same for every code and name nobody; `/robots.txt` routed above the catch-all;
and `rel="noreferrer"` on every external link in the templates. Since Story
1.5 the seeded links open the front page and the three info pages, which carry
the same headers and, per page, the same title and preview for every guest.
What a real browser and a real chat app show is MT-8 and MT-10 in
docs/manual-test-plan.md.
"""

import re
import tomllib
from html.parser import HTMLParser
from pathlib import Path

import pytest
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import Client
from django.urls import URLResolver, get_resolver

from config.logging_filters import NOT_LINK_CODES

BASE_DIR = Path(__file__).resolve().parent.parent
SEED = tomllib.loads((BASE_DIR / "wedding" / "fixtures" / "seed.toml").read_text(encoding="utf-8"))
TEMPLATE_DIRS = (BASE_DIR / "wedding" / "templates", BASE_DIR / "guests" / "templates")

UNKNOWN_CODE = "AAAAAAAAAAAAAAAAAAAAAA"
# The front page and the info pages under a valid link (Story 1.5), with each
# page's fixed title.
GUEST_PAGES = {
    "": "Invitasjon",
    "program/": "Programmet \N{EN DASH} Invitasjon",
    "praktisk/": "Praktisk informasjon \N{EN DASH} Invitasjon",
    "historie/": "Vår historie \N{EN DASH} Invitasjon",
}
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

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


@pytest.fixture
def seeded_codes(seeded) -> list[str]:
    """The seed loaded; the first guest's code in household 1 and in household 2."""
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


def test_a_csrf_failure_says_noindex_and_same_origin():
    """AD-15: the 403 page for a form without a CSRF token carries the headers too
    (it is made by the CSRF middleware, not by a view)."""
    response = Client(enforce_csrf_checks=True).post("/")
    assert response.status_code == 403
    _assert_private_headers(response)


@pytest.mark.parametrize("page", GUEST_PAGES)
def test_a_seeded_test_link_says_noindex_and_same_origin(client, seeded_codes, page):
    """AD-15: a real guest link's front page and each info page answer 200 with the
    same headers."""
    response = client.get(f"/{seeded_codes[0]}/{page}")
    assert response.status_code == 200
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


def test_referrer_policy_is_written_out_in_settings(settings):
    """AD-15: `same-origin` is Django's default, so the value alone proves little;
    the setting is written in config/settings.py, so the choice is traceable and a
    new Django default cannot change it. Never `no-referrer`, which makes Django's
    CSRF check reject forms."""
    assert settings.SECURE_REFERRER_POLICY == "same-origin"
    source = (BASE_DIR / "config" / "settings.py").read_text(encoding="utf-8")
    assert re.search(r'^SECURE_REFERRER_POLICY = "same-origin"$', source, re.MULTILINE)


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


@pytest.mark.parametrize(
    "bad",
    [
        '<img src="//cdn.example/x.png" alt="">',
        '<img srcset="/static/a.png 1x, //cdn.example/b.png 2x" alt="">',
        '<form action="//example.org/svar/"></form>',
        '<meta property="og:image" content="//example.org/x.jpg">',
        '<video poster="//example.org/x.jpg"></video>',
        "<div style=\"background: url('//example.org/x.png')\"></div>",
        '<a href="https://example.org/">x</a>',
        '<meta property="og:image" content="http://testserver/x.jpg">',  # wrong scheme
    ],
)
def test_own_host_checker_catches_other_sites(assert_loads_only_own_host, bad):
    """The checker in conftest.py is proved on each kind of address it looks for;
    the last sample is our own host, but over HTTP on an HTTPS request."""
    with pytest.raises(AssertionError):
        assert_loads_only_own_host(bad, scheme="https")


def test_preview_image_follows_the_request_scheme(client, assert_loads_only_own_host):
    """FR-4, AD-15: over HTTPS the og:image is `https://` on our own host, so a chat
    app never fetches it over plain HTTP."""
    html = client.get("/", secure=True).content.decode()
    assert _preview(html)["og:image"] == "https://testserver/static/img/forhandsvisning.jpg"
    assert_loads_only_own_host(html, scheme="https")


def test_base_rendered_without_a_request_leaves_og_image_out():
    """FR-4: a page rendered with no request (render_to_string, Django's default
    500 page) has no host to build the og:image from, so it leaves the tag out
    instead of writing «:///static/…»; the other preview tags stay."""
    html = render_to_string("wedding/base.html")
    preview = _preview(html)
    assert "og:image" not in preview
    assert preview == {
        "title": "Invitasjon",
        **{key: value for key, value in PREVIEW.items() if key != "og:image"},
    }
    assert "://" not in html


def test_preview_is_the_same_for_every_code_and_names_nobody(client, seeded_codes):
    """FR-4: two guests in different households and an unknown code get the same
    title and Open Graph tags as `/`, and none of them names a guest, the couple,
    their initials, the year or the place."""
    previews = [
        _preview(client.get(path).content.decode())
        for path in ["/", *(f"/{code}/" for code in seeded_codes), f"/{UNKNOWN_CODE}/"]
    ]
    assert all(preview == previews[0] for preview in previews)
    # The <title> sits in a block that a page may fill, but never per guest.
    assert {preview["title"] for preview in previews} == {"Invitasjon"}
    text = " ".join(previews[0].values())
    names = [guest["name"] for household in SEED["households"] for guest in household["guests"]]
    names += [SEED["settings"]["contact_1_name"], SEED["settings"]["contact_2_name"]]
    for name in names:
        assert not re.search(rf"\b{re.escape(name)}\b", text), name
    for forbidden in ("R & V", "R &amp; V", "2028", "Hardingasete"):
        assert forbidden not in text, forbidden


@pytest.mark.parametrize(("page", "title"), GUEST_PAGES.items())
def test_each_guest_page_has_one_preview_for_every_guest(client, seeded_codes, page, title):
    """FR-4, Story 1.5: the front page and each info page have the same title and
    Open Graph tags for guests of two households: the page's fixed title and the
    shared preview, naming nobody and holding no code."""
    previews = [_preview(client.get(f"/{code}/{page}").content.decode()) for code in seeded_codes]
    assert previews[0] == previews[1] == {"title": title, **PREVIEW}
    text = " ".join(previews[0].values())
    names = [guest["name"] for household in SEED["households"] for guest in household["guests"]]
    names += [SEED["settings"]["contact_1_name"], SEED["settings"]["contact_2_name"]]
    for name in names:
        assert not re.search(rf"\b{re.escape(name)}\b", text), name
    for code in seeded_codes:
        assert code not in text


def test_preview_tags_sit_outside_every_block():
    """FR-4: the robots meta and the preview include are in base.html's head outside
    every `{% block %}`, so no page can change them for one guest."""
    source = (BASE_DIR / "wedding" / "templates" / "wedding" / "base.html").read_text(
        encoding="utf-8"
    )
    head = source[source.index("<head>") : source.index("</head>")]
    # `{% endblock %}` may or may not repeat the block's name.
    outside = re.sub(r"{% block (\w+) %}.*?{% endblock(?: \1)? %}", "", head, flags=re.DOTALL)
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


def _top_level_routes(patterns, prefix: str = "") -> list[str]:
    """Every route as the browser sees it, with includes at `""` opened up."""
    routes = []
    for pattern in patterns:
        route = prefix + str(pattern.pattern)
        if isinstance(pattern, URLResolver) and str(pattern.pattern) == "":
            routes += _top_level_routes(pattern.url_patterns, route)
        else:
            routes.append(route)
    return routes


def test_every_fixed_route_stays_readable_in_the_log():
    """NFR-4, AD-15: every top-level route that is not a link code (everything
    except `""` and the guest pages starting with `<str:code>/`) is in the log
    filter's `NOT_LINK_CODES`, so a new route such as Story 3.1's `admin/` fails
    here until the filter knows it."""
    routes = _top_level_routes(get_resolver().url_patterns)
    assert "<str:code>/" in routes
    assert "<str:code>/program/" in routes
    fixed = [route for route in routes if route != "" and not route.startswith("<str:code>/")]
    assert "robots.txt" in fixed
    for route in fixed:
        assert route.split("/")[0] in NOT_LINK_CODES, route


# External links (AD-15)

# A link to another site: a literal `http(s):` address, or an address that comes
# from a variable (`{{ … }}`), which may be anywhere. `{% url %}` and
# `{% static %}` links are our own and are not matched, and neither are `tel:`
# links (the footer's phone numbers, Story 1.5), which reach no site.
_EXTERNAL_LINK = re.compile(
    r"""<a\b[^>]*\bhref=["']?(?!tel:)(?:https?:|[^"'>]*\{\{)[^>]*>""", re.IGNORECASE
)


def _links_without_noreferrer(html: str) -> list[str]:
    """Every external `<a>` tag whose `rel` does not include `noreferrer`."""
    return [
        tag
        for tag in _EXTERNAL_LINK.findall(html)
        if not re.search(r"""\brel=["'][^"']*\bnoreferrer\b""", tag)
    ]


def test_noreferrer_checker_finds_a_bare_external_link():
    """The checker below is proved on good and bad samples."""
    good = (
        '<a href="https://example.com/" rel="noreferrer">Kart</a>'
        '<a href="{{ map_url }}" rel="external noreferrer">Kart</a>'
        "<a href=\"{% url 'guests:private_invitation' %}\">Hjem</a>"
        "<a href=\"{% static 'img/segl.png' %}\">Segl</a>"
        '<a href="#svar">Svar</a>'
        '<a href="tel:{{ contact.tel }}">{{ contact.name }} {{ contact.phone }}</a>'
    )
    bad = '<a class="lenke" href="https://example.com/">Kart</a><a href="{{ map_url }}">Kart</a>'
    assert _links_without_noreferrer(good) == []
    assert _links_without_noreferrer(bad) == [
        '<a class="lenke" href="https://example.com/">',
        '<a href="{{ map_url }}">',
    ]


@pytest.mark.parametrize(
    "path",
    sorted(path for folder in TEMPLATE_DIRS for path in folder.rglob("*.html")),
    ids=lambda path: path.name,
)
def test_every_external_link_has_noreferrer(path):
    """AD-15: an external link never tells the other site which guest page the
    visitor came from."""
    assert _links_without_noreferrer(path.read_text(encoding="utf-8")) == []
