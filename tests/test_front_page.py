"""The invitation's front page under `/<code>/` (Story 1.5, G2).

FR-2, FR-3, FR-6, FR-7, FR-8, FR-41, UX-DR6 to UX-DR9, UX-DR51. Every row of
the story's I/O matrix for `/<code>/`: two, one and four invited, an unsafe
name, the deadline, the phones, and no writes over HTTP (FR-3, also for the
three info pages). Besides: the order of the sections and of the hero, one
`h1`, the «Les mer» links and their accessible names, each seeded household
seeing only its own names, exactly the planned images and no script. Unknown
codes are in test_private_invitation.py and test_info_pages.py, the headers
and link previews in test_guest_privacy.py. How the page looks and behaves in
a browser is MT-11 to MT-14 in docs/manual-test-plan.md.
"""

import datetime
import re
import tomllib
from pathlib import Path

import pytest
from django.contrib.sessions.models import Session
from django.db import connection
from django.test.utils import CaptureQueriesContext

from tests.helpers import FRONT_PAGE, page_text, row_counts
from wedding.links import new_code
from wedding.models import Guest, Household, Settings
from wedding.rules.households import household_names

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
SEED_NAMES = [guest["name"] for household in SEED["households"] for guest in household["guests"]]

SIGMUND = "test-sigmund0000000000"
SYNNE = "test-synne000000000000"
ARILD = "test-arild000000000000"
NAMES_H1 = (
    '<h1 class="display-names hero__names">'
    "<span>Rikke</span> <span>&amp;</span> <span>Valdemar</span></h1>"
)
INFO_PATHS = ("program/", "praktisk/", "historie/")

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _page(client, code: str, path: str = "") -> str:
    response = client.get(f"/{code}/{path}")
    assert response.status_code == 200
    return response.content.decode()


# The I/O matrix


@pytest.mark.parametrize(
    ("code", "household", "word"),
    [
        (SIGMUND, "Sigmund og bestemor", "dere"),
        (SYNNE, "Synne", "deg"),
        (ARILD, "Arild, Marie, Filippa og Leone", "dere"),
    ],
)
def test_household_line_and_du_or_dere(client, seeded, code, household, word):
    """FR-7, UX-DR51: the hero names the household; «deg» to one invited person,
    «dere» to two or more, in the invites line and the lead-in."""
    text = page_text(_page(client, code))
    assert f"for {household}" in text
    assert f"inviterer {word} til sitt bryllup" in text
    assert f"Vi gleder oss til å feire med {word}" in text
    other = "deg" if word == "dere" else "dere"
    assert f"inviterer {other}" not in text
    assert f"feire med {other}" not in text


def test_an_unsafe_name_is_escaped(client):
    """NFR-4: a guest name is text, never HTML."""
    household = Household.objects.create()
    guest = Guest.objects.create(household=household, name="<b>Ola</b>", code=new_code())
    html = _page(client, guest.code)
    assert "&lt;b&gt;Ola&lt;/b&gt;" in html
    assert "<b>Ola</b>" not in html


@pytest.mark.parametrize(
    ("deadline", "short", "full"),
    [
        (
            datetime.date(2028, 1, 4),
            "Svar innen 4. januar 2028",
            "Svar innen tirsdag 4. januar 2028 kl. 23:59",
        ),
        (
            datetime.date(2027, 12, 31),
            "Svar innen 31. desember 2027",
            "Svar innen fredag 31. desember 2027 kl. 23:59",
        ),
    ],
)
def test_deadline_short_in_the_hero_and_full_in_the_rsvp_sheet(
    client, seeded, deadline, short, full
):
    """FR-41: the hero's deadline line has no weekday or time; the RSVP sheet has
    both. Plain spaces only, so the date can wrap at 180 CSS px."""
    Settings.objects.filter(pk=1).update(rsvp_deadline=deadline)
    html = _page(client, SIGMUND)
    hero = html[html.index('class="paper-sheet hero"') : html.index('class="lead-in"')]
    rsvp = html[html.index('id="svar"') :]
    assert short in page_text(hero)
    assert full not in page_text(hero)
    assert full in page_text(rsvp)
    assert "&nbsp;" not in html
    assert "\xa0" not in html


def test_footer_shows_both_phones_as_tel_links(client, seeded):
    """FR-6: «Spørsmål? Send oss en melding:» and one `tel:` row per contact,
    contact 1 first, with the number as typed and the link with digits only."""
    html = _page(client, SIGMUND)
    footer = html[html.index("<footer") : html.index("</footer>")]
    assert "Spørsmål? Send oss en melding:" in footer
    rows = re.findall(r'<a href="(tel:[^"]*)">([^<]*)</a>', footer)
    assert rows == [
        ("tel:+4700000101", "Rikke +47 000 00 101"),
        ("tel:+4700000102", "Valdemar +47 000 00 102"),
    ]


@pytest.mark.parametrize("phone", ["", "ukjent"])
def test_footer_leaves_out_a_contact_without_a_phone(client, seeded, phone):
    """FR-6: a phone with no digit, blank or not, gives no row for that contact."""
    Settings.objects.filter(pk=1).update(contact_2_phone=phone)
    html = _page(client, SIGMUND)
    assert re.findall(r'href="tel:[^"]*"', html) == ['href="tel:+4700000101"']
    assert "Valdemar" not in html[html.index("<footer") :]


def test_without_any_phone_there_is_no_footer(client):
    """FR-6: the migration's settings have blank phones, so there is nothing to
    call, and the whole footer is left out."""
    household = Household.objects.create()
    guest = Guest.objects.create(household=household, name="Ola", code=new_code())
    html = _page(client, guest.code)
    assert "<footer" not in html
    assert "tel:" not in html


def test_without_a_digit_in_either_phone_there_is_no_footer(client, seeded):
    """FR-6: phones that hold no digit (here «ukjent») give nothing to call, so
    the whole footer is left out, as with blank phones."""
    Settings.objects.filter(pk=1).update(contact_1_phone="ukjent", contact_2_phone="ukjent")
    html = _page(client, SIGMUND)
    assert "<footer" not in html
    assert "tel:" not in html


@pytest.mark.parametrize(("path", "queries"), [("", 4), *((path, 3) for path in INFO_PATHS)])
def test_opening_a_guest_page_never_writes(client, seeded, path, queries):
    """FR-2, FR-3 over HTTP: a GET of the front page runs four SELECTs (the
    resolver, the household's guest names, the settings row, the answer check of
    Story 2.8) and of an info page three (the resolver, the settings row, the
    answer check), and nothing else: it creates and changes no row (household revisions
    included), sets no cookie and makes no session."""
    before = row_counts()
    revisions = list(Household.objects.values_list("id", "revision"))
    with CaptureQueriesContext(connection) as captured:
        response = client.get(f"/{SIGMUND}/{path}")
    assert response.status_code == 200
    sql = [query["sql"] for query in captured.captured_queries]
    assert len(sql) == queries
    assert all(statement.lstrip().upper().startswith("SELECT") for statement in sql)
    assert row_counts() == before
    assert list(Household.objects.values_list("id", "revision")) == revisions
    assert not response.cookies
    assert "Set-Cookie" not in response
    assert Session.objects.count() == 0


# Structure


def test_sections_come_in_the_approved_order(client, seeded):
    """FR-8, UX-DR6 to UX-DR9, DESIGN.md > Front page: nav bar, hero sheet, lead-in,
    «Alt om helgen», RSVP sheet, footer band."""
    html = _page(client, SIGMUND)
    marks = [
        '<nav class="nav-bar" aria-label="Invitasjonen">',
        'class="paper-sheet hero"',
        'class="lead-in"',
        "Alt om helgen",
        'id="svar"',
        "<footer",
    ]
    positions = [html.index(mark) for mark in marks]
    assert positions == sorted(positions)
    main = html[html.index("<main") : html.index("</main>")]
    for mark in marks[1:5]:
        assert mark in main, mark


def test_hero_holds_the_invitation_in_order(client, seeded):
    """FR-7, UX-DR7: seal, illustration, names, invites line, gypsophila, date,
    place, household line, deadline line, as approved."""
    html = _page(client, SIGMUND)
    hero = html[html.index('class="paper-sheet hero"') : html.index('class="lead-in"')]
    marks = [
        "segl.png",
        "illustrasjon.jpg",
        "<h1",
        "inviterer",
        "brudeslor.png",
        "Lørdag 27. mai 2028",
        "Hardingasete <span",
        "for <span",
        "innen",
    ]
    positions = [hero.index(mark) for mark in marks]
    assert positions == sorted(positions)
    assert NAMES_H1 in hero
    assert re.search(r"<img[^>]*segl\.png[^>]*>", hero).group(0).count('alt=""') == 1
    assert 'alt="Akvarell av tunet på Hardingasete."' in hero
    assert 'Hardingasete <span aria-hidden="true">·</span> Hardanger' in hero
    assert '<a href="#svar">Svar</a> innen' in hero
    assert "small-caps hero__date" in hero
    assert "small-caps hero__place" in hero


def test_one_h1_with_the_names(client, seeded):
    """NFR-5, EXPERIENCE.md > Accessibility Floor: one `h1` per page, the names."""
    html = _page(client, SIGMUND)
    assert html.count("<h1") == 1
    assert NAMES_H1 in html


def test_nav_bar_words_and_svar(client, seeded):
    """FR-8, UX-DR6: the three nav words go to the info pages, with no separator
    characters and no current word on the front page; «Svar» jumps to #svar."""
    html = _page(client, SIGMUND)
    nav = html[html.index("<nav") : html.index("</nav>")]
    words = re.findall(r'<a href="([^"]+)"\s*>([^<]+)</a>', nav)
    assert words == [
        (f"/{SIGMUND}/program/", "Program"),
        (f"/{SIGMUND}/praktisk/", "Praktisk"),
        (f"/{SIGMUND}/historie/", "Vår historie"),
    ]
    assert re.search(r'<a class="nav-bar__svar"\s+href="#svar">Svar</a>', nav)
    assert "aria-current" not in nav
    assert "·" not in nav
    assert "|" not in nav


def test_les_mer_links_have_their_pages_and_accessible_names(client, seeded):
    """FR-8, UX-DR8: each topic's «Les mer» is an outlined button on green to its
    page, and screen readers hear which topic it is for."""
    html = _page(client, SIGMUND)
    links = re.findall(
        r'<a class="button button--on-green"\s+href="([^"]+)">'
        r'Les mer<span class="visually-hidden">([^<]+)</span></a>',
        html,
    )
    assert links == [
        (f"/{SIGMUND}/program/", " om programmet"),
        (f"/{SIGMUND}/praktisk/", " om praktisk informasjon"),
        (f"/{SIGMUND}/historie/", " om vår historie"),
    ]
    text = page_text(html)
    for title, line in (
        ("Programmet", "Hele helgen, dag for dag."),
        ("Praktisk informasjon", "Reise, hyttene, tunet og området rundt."),
        ("Vår historie", "Fra vi møttes til i dag."),
    ):
        assert f"<h3>{title}</h3>" in html
        assert line in text


def test_rsvp_sheet_is_the_jump_target(client, seeded):
    """FR-41, UX-DR7: the RSVP sheet is `#svar`, focusable by a link only and
    labelled by its heading."""
    html = _page(client, SIGMUND)
    rsvp = html[html.index('<section class="paper-sheet rsvp"') : html.index("</main>")]
    assert re.search(
        r'<section class="paper-sheet rsvp"\s+id="svar"\s+tabindex="-1"\s+'
        r'aria-labelledby="svar-heading">',
        rsvp,
    )
    assert '<h2 id="svar-heading">Svar på invitasjonen</h2>' in rsvp
    assert "Barnefritt bryllup" in rsvp
    assert re.search(r'<img[^>]*brudeslor\.png[^>]*width="180"', rsvp)


@pytest.mark.parametrize("code", [SIGMUND, SYNNE, ARILD])
def test_rsvp_sheet_links_to_the_form(client, seeded, code):
    """FR-12, FR-14, UX-DR7 (Story 2.1): every household's RSVP sheet ends with the
    primary link «Svar på invitasjonen» to its own `/<code>/svar/`, after the
    deadline line. It is a link, not a button: opening the form posts nothing."""
    html = _page(client, code)
    rsvp = html[html.index('<section class="paper-sheet rsvp"') : html.index("</main>")]
    link = f'<a class="button" href="/{code}/svar/">Svar på invitasjonen</a>'
    assert link in rsvp
    assert rsvp.index('class="rsvp__deadline"') < rsvp.index(link)
    assert html.count("/svar/") == 1
    assert "<button" not in html


def test_images_are_exactly_the_front_page_set(client, seeded):
    """NFR-7, UX-DR4: the page shows exactly the nine planned front-page images
    (their budget is in test_images.py), each with a size; everything below the
    hero loads lazily."""
    html = _page(client, SIGMUND)
    tags = re.findall(r"<img\b[^>]*>", html)
    sources = {re.search(r'src="/static/img/([^"]+)"', tag).group(1) for tag in tags}
    assert sources == set(FRONT_PAGE)
    for tag in tags:
        assert re.search(r'\swidth="\d+"', tag), tag
        assert re.search(r'\sheight="\d+"', tag), tag
    below_hero = html.index('class="lead-in"')
    for match in re.finditer(r"<img\b[^>]*>", html):
        lazy = 'loading="lazy"' in match.group(0)
        assert lazy == (match.start() > below_hero), match.group(0)


def test_no_script_no_form_and_only_our_own_host(client, seeded, assert_loads_only_own_host):
    """AD-15, Story 1.5: no JavaScript, no CSRF token (so no cookie), and every
    absolute address is our own host (`tel:` links reach no site)."""
    html = _page(client, SIGMUND)
    assert "<script" not in html
    assert "csrfmiddlewaretoken" not in html
    assert_loads_only_own_host(html)


@pytest.mark.parametrize("index", range(len(SEED["households"])))
def test_each_household_sees_only_its_own_names(client, seeded, index):
    """FR-2: a seeded household's link shows its own names in the hero and no
    other seeded guest's name anywhere on the page."""
    household = SEED["households"][index]
    own = [guest["name"] for guest in household["guests"]]
    html = _page(client, household["guests"][0]["code"])
    assert f"for {household_names(own)}" in page_text(html)
    for name in SEED_NAMES:
        if name not in own:
            assert not re.search(rf"\b{re.escape(name)}\b", html), name
