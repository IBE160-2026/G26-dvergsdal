"""The content of Programmet (Story 1.7, G3).

FR-9, FR-11, FR-32, AD-12, AD-17, UX-DR13. Every row of the story's I/O
matrix for `/program/`: two SELECTs; the «Hopp til» jump links in one list
with hidden dots, the voluntary line, then three day sheets, each a focusable
jump target labelled by its `h2`, with its date line, the timeline (Rikke's
decorative icons, `<time>` and the short name) and «Godt å vite». The text is
compared with the approved mockup, so a page that drifts from Rikke's approved
text fails here without the text being retyped in the test; the mockup's
«[x]» price placeholders are the meal prices from the settings row, never
template text. The frame (one `h1`, «Program» current, both ways back, no
script, own host only) and the unknown-code 404 on every info page are
test_info_pages.py; what only a browser can show (where a jump lands, the
alternating and one-sided timeline, forced colours, screen-reader names) is
MT-19 to MT-21 in docs/manual-test-plan.md.
"""

import dataclasses
import re
from pathlib import Path

import pytest

from tests.helpers import main_html, page_text, sections_of, tag_attrs
from wedding.actors import SYSTEM
from wedding.models import Settings
from wedding.selectors import programme_prices, site_settings
from wedding.services.settings import SettingsValues, update_settings

CODE = "test-sigmund0000000000"  # several invited, «dere»
SYNNE = "test-synne000000000000"  # one invited, «deg»
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = BASE_DIR / "guests" / "templates" / "guests" / "programme.html"
MOCKUP = (
    BASE_DIR
    / ".docs"
    / "planning-artifacts"
    / "ux-designs"
    / "ux-aill-handle-it-2026-11-10"
    / "mockups"
    / "info-program.html"
).read_text(encoding="utf-8")

# The three days in order: (id, heading, date line as read).
DAYS = [
    ("fredag", "Fredag", "26. mai"),
    ("lordag", "Lørdag", "27. mai · bryllupsdagen"),
    ("sondag", "Søndag", "28. mai"),
]
# Each day's events as (placeholder time, name, icon), info-program.html:145,154,163.
EVENTS = {
    "fredag": [
        ("10:00", "Fjelltur", "ikon-01-fjelltur.png"),
        ("15:00", "Hyttene er klare", "ikon-02-hytte.png"),
        ("17:00", "Middag", "ikon-04-middag.png"),
        ("19:00", "Rebus", "ikon-03-rebus.png"),
        ("21:00", "Badstue, stamp og mingling", "ikon-05-stamp.png"),
    ],
    "lordag": [
        ("08:00", "Yoga", "ikon-07-yoga.png"),
        ("09:00", "Frokost", "ikon-06-frokost.png"),
        ("13:30", "Vi drar til kirka", "ikon-08-bil.png"),
        ("14:00", "Vielsen", "ikon-09-ringer.png"),
        ("16:00", "Lunsj utenfor kirka", "ikon-10-lunsj.png"),
        ("19:00", "Middag og fest", "ikon-11-fest.png"),
    ],
    "sondag": [
        ("09:00", "Frokost", "ikon-06-frokost.png"),
        ("12:00", "Hyttene skal være tomme", "ikon-12-avreise.png"),
    ],
}
# The seed's meal prices (wedding/fixtures/seed.toml), one «[x]» per day.
SEED_PRICES = {"fredag": 340, "lordag": 260, "sondag": 260}
JUMP_DOT = '<span class="jump-links__dot" aria-hidden="true">·</span>'
VOLUNTARY = "Alt i programmet er frivillig. Bli med på det dere har lyst til."

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _get(client, django_assert_num_queries, code: str = CODE) -> str:
    with django_assert_num_queries(2):
        response = client.get(f"/{code}/program/")
    assert response.status_code == 200
    return response.content.decode()


def _days(html: str) -> dict[str, str]:
    """The day sheets' inner HTML by id."""
    return {attrs["id"]: body for attrs, body in sections_of(main_html(html))}


def _mockup_days() -> dict[str, str]:
    """The approved day parts by id, as in the mockup."""
    return dict(
        re.findall(r'<section class="PART" id="([^"]+)">(.*?)</section>', MOCKUP, re.DOTALL)
    )


def _events(body: str) -> list[tuple[dict[str, str], dict[str, str], str, str]]:
    """Each timeline item of a day as (img attributes, time attributes, time, name)."""
    timeline = re.search(r'<ol class="programme-timeline">(.*?)</ol>', body, re.DOTALL).group(1)
    return [
        (
            tag_attrs(re.search(r"<img\b[^>]*>", item).group(0)),
            tag_attrs(re.search(r"<time\b[^>]*>", item).group(0)),
            page_text(re.search(r"<time\b[^>]*>(.*?)</time>", item, re.DOTALL).group(1)),
            page_text(
                re.search(
                    r'<span class="programme-timeline__name">(.*?)</span>', item, re.DOTALL
                ).group(1)
            ),
        )
        for item in re.findall(r"<li>(.*?)</li>", timeline, re.DOTALL)
    ]


def _set_prices(dinner: int, saturday: int, sunday: int) -> None:
    """Change the three meal prices through the settings service, as the couple would."""
    row = Settings.objects.get()
    values = SettingsValues(
        **{field.name: getattr(row, field.name) for field in dataclasses.fields(SettingsValues)}
    )
    update_settings(
        SYSTEM,
        dataclasses.replace(
            values,
            price_friday_dinner=dinner,
            price_saturday_breakfast=saturday,
            price_sunday_breakfast=sunday,
        ),
    )


@pytest.fixture
def programme(client, seeded, django_assert_num_queries) -> str:
    return _get(client, django_assert_num_queries)


def test_jump_links_are_one_list_between_the_title_and_the_first_sheet(programme):
    """UX-DR13, DESIGN.md > Info pages: one «Hopp til» nav after the `h1` and
    before the first sheet, with one list Fredag · Lørdag · Søndag; every item
    but the first starts with an aria-hidden dot, and no dot stands in the nav
    outside such a span (the same markup as Praktisk informasjon)."""
    main = main_html(programme)
    assert main.count('aria-label="Hopp til"') == 1
    nav_start = main.index('<nav class="jump-links" aria-label="Hopp til">')
    assert main.index("</h1>") < nav_start < main.index("<section")
    nav = main[nav_start : main.index("</nav>", nav_start)]
    lists = re.findall(r"<ul>(.*?)</ul>", nav, re.DOTALL)
    assert len(lists) == 1
    items = re.findall(r"<li>(.*?)</li>", lists[0], re.DOTALL)
    links = []
    for index, item in enumerate(items):
        assert item.strip().startswith(JUMP_DOT) == (index > 0), item
        links.append(re.search(r'<a href="#([^"]+)">([^<]+)</a>', item).groups())
    assert links == [("fredag", "Fredag"), ("lordag", "Lørdag"), ("sondag", "Søndag")]
    assert "·" not in nav.replace(JUMP_DOT, "")
    mockup_nav = re.search(r'<nav class="toc1" aria-label="Hopp til">(.*?)</nav>', MOCKUP)
    assert re.findall(r'<a href="#([^"]+)">([^<]+)</a>', mockup_nav.group(1)) == links


def test_voluntary_line_sits_between_the_jump_links_and_the_first_sheet(programme):
    """UX-DR13, DESIGN.md voluntary-line, EXPERIENCE.md:115: the decided line,
    word for word as in the mockup, after the jump links and before Fredag."""
    main = main_html(programme)
    line = f'<p class="voluntary-line">{VOLUNTARY}</p>'
    assert main.count(line) == 1
    assert main.index("</nav>") < main.index(line) < main.index("<section")
    assert f'<p class="voluntary">{VOLUNTARY}</p>' in MOCKUP


def test_three_day_sheets_in_order_each_a_focusable_jump_target(programme):
    """FR-9, UX-DR13, EXPERIENCE.md > Info sheet: three info sheets in the
    approved order with the mockup's ids; each takes focus from its link
    (tabindex -1), is labelled by its own `h2` and opens with the italic date
    line, whose dot on Saturday is aria-hidden."""
    sections = sections_of(main_html(programme))
    assert [attrs["id"] for attrs, _ in sections] == [day_id for day_id, _, _ in DAYS]
    assert [attrs["id"] for attrs, _ in sections] == list(_mockup_days())
    for (attrs, body), (day_id, heading, date) in zip(sections, DAYS, strict=True):
        assert attrs["class"] == "paper-sheet info-sheet programme-day"
        assert attrs["tabindex"] == "-1"
        assert attrs["aria-labelledby"] == f"{day_id}-overskrift"
        assert re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.DOTALL) == [
            (f"{day_id}-overskrift", heading)
        ]
        dates = re.findall(r'<p class="programme-day__date">(.*?)</p>', body, re.DOTALL)
        assert [page_text(text) for text in dates] == [date]
        assert body.index("</h2>") < body.index("programme-day__date")
    saturday = re.search(
        r'<p class="programme-day__date">(.*?)</p>', _days(programme)["lordag"], re.DOTALL
    )
    assert " ".join(saturday.group(1).split()) == (
        '27. mai <span aria-hidden="true">·</span> bryllupsdagen'
    )


@pytest.mark.parametrize("day_id", EVENTS)
def test_each_day_lists_its_events_with_icon_time_and_name(programme, day_id):
    """FR-9, UX-DR13, DESIGN.md programme-timeline, programme-icon: the day's
    events in the approved order, each with its icon (decorative, alt="",
    56 by 56), a `<time>` whose datetime is the time shown, and the short
    name; the times rise through the day."""
    events = _events(_days(programme)[day_id])
    assert [(time, name) for _, _, time, name in events] == [
        (time, name) for time, name, _ in EVENTS[day_id]
    ]
    for (image, time_attrs, time, _), (_, _, icon) in zip(events, EVENTS[day_id], strict=True):
        assert image["class"] == "programme-timeline__icon"
        assert image["src"] == f"/static/img/ikoner/{icon}"
        assert image["alt"] == ""
        assert (image["width"], image["height"]) == ("56", "56")
        assert time_attrs == {"class": "programme-timeline__time", "datetime": time}
    times = [time for _, _, time, _ in events]
    assert times == sorted(times)


def test_icons_are_the_twelve_used_in_the_mockup_friday_eager_the_rest_lazy(programme):
    """NFR-7, UX-DR4, UX-DR13: the page shows exactly the twelve icons (breakfast
    twice), the mockup's for each event; Friday's load at once, so the first
    screen has them, and Saturday's and Sunday's lazily."""
    main = main_html(programme)
    sources = re.findall(r'<img\b[^>]*src="/static/img/([^"]+)"', main)
    assert len(sources) == 13
    assert set(sources) == {f"ikoner/{icon}" for day in EVENTS.values() for _, _, icon in day}
    assert len(set(sources)) == 12
    mockup_icons = re.findall(r'<img class="icon" src="ikoner/([^"]+)"', MOCKUP)
    assert [source.removeprefix("ikoner/") for source in sources] == mockup_icons
    for day_id, body in _days(programme).items():
        for image, _, _, _ in _events(body):
            expected = None if day_id == "fredag" else "lazy"
            assert image.get("loading") == expected, (day_id, image["src"])


@pytest.mark.parametrize("day_id", EVENTS)
def test_good_to_know_closes_each_day_after_the_timeline(programme, day_id):
    """UX-DR13, DESIGN.md good-to-know: the italic «Godt å vite» heading is an
    `h3` after the timeline, the last thing on the sheet; what costs money is
    a `strong` label, never `b`."""
    body = _days(programme)[day_id]
    assert body.count("<h3>Godt å vite</h3>") == 1
    assert body.index("</ol>") < body.index('<div class="good-to-know">') < body.index("<h3>")
    assert body.rstrip().endswith("</div>")
    assert "<b>" not in body
    assert re.search(r"<strong>(Middagen|Frokosten) betales selv:</strong>", body)


@pytest.mark.parametrize("day_id", EVENTS)
def test_each_day_holds_the_approved_text_with_the_seed_price(programme, day_id):
    """FR-9, AD-17: each day's text is the approved mockup's word for word, its
    «[x]» price placeholder replaced by the seed's price for that meal."""
    expected = _mockup_days()[day_id].replace("[x]", str(SEED_PRICES[day_id]))
    assert page_text(_days(programme)[day_id]) == page_text(expected)


def test_prices_follow_the_settings(client, programme, django_assert_num_queries):
    """FR-9, FR-32, AD-12: the couple changes the meal prices in the settings
    and «Godt å vite» shows the new ones, each on its own day."""
    _set_prices(dinner=415, saturday=255, sunday=265)
    days = _days(_get(client, django_assert_num_queries))
    assert "Middagen betales selv: 415 kr." in page_text(days["fredag"])
    assert "Frokosten betales selv: 255 kr." in page_text(days["lordag"])
    assert "Frokosten betales selv: 265 kr." in page_text(days["sondag"])


def test_one_invited_reads_the_same_programme(client, programme, django_assert_num_queries):
    """Story 1.7 boundaries: no du/dere logic yet (the decided voluntary line
    says «dere»), so a one-person household reads the same page text."""
    one = _get(client, django_assert_num_queries, code=SYNNE)
    assert page_text(main_html(one)) == page_text(main_html(programme))


def test_unknown_code_on_the_programme_shows_g1_with_404(client, db):
    """FR-5: an unknown or malformed code under `/program/` shows G1 with 404,
    the same body as `/` (test_info_pages.py covers the query counts)."""
    bare = client.get("/").content.decode()
    for code in ("AAAAAAAAAAAAAAAAAAAAAA", "hei"):
        response = client.get(f"/{code}/program/")
        assert response.status_code == 404
        assert response.content.decode() == bare


def test_template_holds_no_price_and_no_sign_up():
    """FR-9, FR-32, AD-12: every «kr» in the template follows a price from the
    settings (`}}`), no «[x]» placeholder and no form are left, so the
    programme is information only and cannot show a price of its own. Besides
    the placeholder times, the three dates, the icons' 56px size, the sheets'
    tabindex and the `h2`/`h3` tag names, no digit stands in the template, so
    a price written as «340 kroner» or «340,-» fails too."""
    source = TEMPLATE.read_text(encoding="utf-8")
    assert source.count(" kr.") == 3
    assert re.findall(r"(\S+) kr\b", source) == ["}}", "}}", "}}"]
    for price in ("prices.friday_dinner", "prices.saturday_breakfast", "prices.sunday_breakfast"):
        assert source.count(f"{{{{ {price} }}}} kr.") == 1, price
    text = re.sub(r"{% comment %}.*?{% endcomment %}", "", source, flags=re.DOTALL)
    text = re.sub(r"{%.*?%}|{{.*?}}", "", text, flags=re.DOTALL)
    text = re.sub(r'datetime="\d\d:\d\d"|>\d\d:\d\d</time>', "", text)
    text = re.sub(r"</?h[23]\b", "", text)
    for allowed in ("26. mai", "27. mai", "28. mai", 'width="56"', 'height="56"', 'tabindex="-1"'):
        text = text.replace(allowed, "")
    assert re.findall(r"\d", text) == []
    assert "[x]" not in source
    assert "<form" not in source
    assert "<script" not in source


def test_programme_prices_read_the_row_without_a_query_when_given_it(
    seeded, django_assert_num_queries
):
    """FR-9, FR-32, AD-12: `programme_prices` returns the row's three meal
    prices as ints; given the row it reads nothing more, and without it it
    reads the row once."""
    row = site_settings()
    with django_assert_num_queries(0):
        prices = programme_prices(row)
    assert prices == {"friday_dinner": 340, "saturday_breakfast": 260, "sunday_breakfast": 260}
    assert all(type(price) is int for price in prices.values())
    with django_assert_num_queries(1):
        assert programme_prices() == prices
