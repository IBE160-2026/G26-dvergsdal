"""The content of Praktisk informasjon and Vår historie (Story 1.6, G3).

FR-10, FR-11, AD-17, UX-DR12, UX-DR14. Every row of the story's I/O matrix
for `/praktisk/` and `/historie/`: three SELECTs; on Praktisk the «Hopp til»
jump links in three lists with hidden dots, then seven info sheets, each a
focusable jump target labelled by its `h2`; on Vår historie one story sheet
labelled by the page title, nine chapter `h2`s with one hidden dot each and the
signature last. The text is compared with the approved mockups, so a page that
drifts from Rikke's approved text fails here without the text being retyped in
the test. The unknown-code row and the frame (one `h1`, both ways back, the
hidden arrow, no script) are test_info_pages.py; what only a browser can
show (where a jump lands, narrow widths, screen-reader names) is MT-16 to
MT-18 in docs/manual-test-plan.md.
"""

import html as html_module
import re
from pathlib import Path

import pytest

from tests.helpers import main_html, page_text, sections_of, tag_attrs

CODE = "test-sigmund0000000000"  # several invited, «dere»
SYNNE = "test-synne000000000000"  # one invited, «deg»
MOCKUPS = (
    Path(__file__).resolve().parent.parent
    / ".docs"
    / "planning-artifacts"
    / "ux-designs"
    / "ux-aill-handle-it-2026-11-10"
    / "mockups"
)
PRACTICAL_MOCKUP = (MOCKUPS / "info-praktisk.html").read_text(encoding="utf-8")
STORY_MOCKUP = (MOCKUPS / "info-om-oss.html").read_text(encoding="utf-8")

# EXPERIENCE.md > Copy: the jump links in three balanced lines (id, word).
JUMP_LINES = [
    [("vielsen", "Vielsen"), ("stedet", "Hardingasete")],
    [("komme-dit", "Komme dit"), ("husregler", "Husregler"), ("antrekk", "Antrekk")],
    [("ta-med", "Ta med"), ("omradet", "Området")],
]
# The seven parts in order (id, heading).
SECTIONS = [
    ("vielsen", "Vielsen"),
    ("stedet", "Hardingasete og hyttene"),
    ("komme-dit", "Hvordan komme seg dit"),
    ("husregler", "Husregler"),
    ("antrekk", "Antrekk"),
    ("ta-med", "Ta med"),
    ("omradet", "Området rundt"),
]
# The parts with a photo: (photo, alt, extra class on the photo).
PHOTOS = {
    "vielsen": (
        "sted-kirka.jpg",
        "Strandebarm kirke, en hvit trekirke med fjell bak.",
        "lace-frame__photo--kirka",
    ),
    "stedet": (
        "sted-tunet.jpg",
        "Tunet på Hardingasete med de gamle husene.",
        "lace-frame__photo--tunet",
    ),
    "omradet": ("sted-omradet.jpg", "Fjorden og fjellene i Hardanger.", None),
}
CHAPTERS = [
    "Sensommeren 2021 · Trondheim",
    "2022 · Trondheim",
    "2023 · Trondheim",
    "Høsten 2024 · Firenze",
    "Starten av 2025 · Annecy",
    "Våren 2025 · Italia",
    "Høsten 2025 · Trondheim",
    "Sommeren 2026 · Asia",
    "Våren 2027 · Oslo",
]
HIDDEN_DOT = '<span aria-hidden="true">·</span>'
JUMP_DOT = '<span class="jump-links__dot" aria-hidden="true">·</span>'

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _mockup_parts() -> dict[str, str]:
    """The approved Praktisk parts by id, without the map button (Story 7.4)."""
    parts = re.findall(
        r'<section class="PART" id="([^"]+)">(.*?)</section>', PRACTICAL_MOCKUP, re.DOTALL
    )
    return {
        part_id: re.sub(r'<a class="small-btn"[^>]*>.*?</a>', "", body, flags=re.DOTALL)
        for part_id, body in parts
    }


def _get(client, django_assert_num_queries, path: str) -> str:
    with django_assert_num_queries(3):
        response = client.get(f"/{CODE}/{path}")
    assert response.status_code == 200
    return response.content.decode()


@pytest.fixture
def practical(client, seeded, django_assert_num_queries) -> str:
    return _get(client, django_assert_num_queries, "praktisk/")


@pytest.fixture
def story(client, seeded, django_assert_num_queries) -> str:
    return _get(client, django_assert_num_queries, "historie/")


# Praktisk informasjon (FR-10, UX-DR12)


def test_jump_links_sit_between_the_title_and_the_first_sheet(practical):
    """UX-DR12, DESIGN.md > Info pages: the «Hopp til» nav comes after the `h1`
    and before the first sheet, and there is exactly one."""
    main = main_html(practical)
    assert main.count('aria-label="Hopp til"') == 1
    nav = main.index('<nav class="jump-links" aria-label="Hopp til">')
    assert main.index("</h1>") < nav < main.index("<section")


def test_jump_links_are_three_lists_with_hidden_dots(practical):
    """UX-DR12, EXPERIENCE.md > Jump links: three lists in the approved lines;
    every item but each list's first starts with an aria-hidden dot, and no dot
    stands in the nav outside such a span."""
    nav = re.search(r'<nav class="jump-links" aria-label="Hopp til">(.*?)</nav>', practical, re.S)
    lists = re.findall(r"<ul>(.*?)</ul>", nav.group(1), re.DOTALL)
    found = []
    for items in lists:
        line = []
        for index, item in enumerate(re.findall(r"<li>(.*?)</li>", items, re.DOTALL)):
            assert item.strip().startswith(JUMP_DOT) == (index > 0), item
            link = re.search(r'<a href="#([^"]+)">([^<]+)</a>', item)
            line.append((link.group(1), link.group(2)))
        found.append(line)
    assert found == JUMP_LINES
    assert "·" not in nav.group(1).replace(JUMP_DOT, "")


def test_jump_links_match_the_approved_mockup(practical):
    """UX-DR12: the hrefs and words are the mockup's, line for line."""
    mockup = re.search(r'<nav class="toc1" aria-label="Hopp til">(.*?)</nav>', PRACTICAL_MOCKUP)
    lines = [
        re.findall(r'<a href="#([^"]+)">([^<]+)</a>', items)
        for items in re.findall(r"<ul>(.*?)</ul>", mockup.group(1))
    ]
    assert lines == JUMP_LINES


def test_seven_sheets_in_order_each_a_focusable_jump_target(practical):
    """FR-10, UX-DR12, EXPERIENCE.md > Info sheet: seven info sheets in the
    approved order with the mockup's ids; each takes focus from its link
    (tabindex -1) and is labelled by its own `h2`."""
    sections = sections_of(main_html(practical))
    assert [attrs["id"] for attrs, _ in sections] == [part_id for part_id, _ in SECTIONS]
    assert [attrs["id"] for attrs, _ in sections] == list(_mockup_parts())
    for (attrs, body), (part_id, heading) in zip(sections, SECTIONS, strict=True):
        assert attrs["class"] == "paper-sheet info-sheet"
        assert attrs["tabindex"] == "-1"
        assert attrs["aria-labelledby"] == f"{part_id}-overskrift"
        h2 = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.DOTALL)
        assert h2 == [(f"{part_id}-overskrift", heading)]


@pytest.mark.parametrize(("part_id", "heading"), SECTIONS)
def test_each_sheet_holds_the_approved_text(practical, part_id, heading):
    """FR-10, AD-17: each sheet's text is the approved mockup's word for word,
    placeholders in square brackets included; the map button is left out
    until Story 7.4."""
    sections = {attrs["id"]: body for attrs, body in sections_of(main_html(practical))}
    assert page_text(sections[part_id]) == page_text(_mockup_parts()[part_id])
    assert page_text(sections[part_id]).startswith(heading)


def test_facts_use_strong_not_b(practical):
    """FR-10, DESIGN.md > Info sheet: the facts' labels are `strong`."""
    main = main_html(practical)
    assert "<b>" not in main
    for label in ("Lørdag 27. mai kl. [14:00]", "Adresse:", "Lørdag:", "Fredag og søndag:"):
        assert f"<strong>{label}</strong>" in main, label


def test_vielsen_links_to_the_programme(practical):
    """FR-8, FR-10: «programmet» in Vielsen opens the programme page."""
    sections = {attrs["id"]: body for attrs, body in sections_of(main_html(practical))}
    assert f'<a href="/{CODE}/program/">programmet</a>' in sections["vielsen"]


def test_practical_images_are_framed_with_alt_size_and_loading(practical):
    """NFR-5, NFR-7, UX-DR4: the photos and the lace in the 220px frame, each with
    alt, width and height; the Vielsen images load at once and every later
    image lazily; the page shows exactly these four files."""
    main = main_html(practical)
    sources = set(re.findall(r'<img\b[^>]*src="/static/img/([^"]+)"', main))
    assert sources == {"sted-kirka.jpg", "sted-tunet.jpg", "sted-omradet.jpg", "blonde.png"}
    sections = {attrs["id"]: body for attrs, body in sections_of(main)}
    for part_id, body in sections.items():
        images = [tag_attrs(tag) for tag in re.findall(r"<img\b[^>]*>", body)]
        if part_id not in PHOTOS:
            assert images == [], part_id
            continue
        photo_file, alt, modifier = PHOTOS[part_id]
        assert '<div class="lace-frame lace-frame--info">' in body
        photo, lace = images
        assert photo["src"] == f"/static/img/{photo_file}"
        assert photo["alt"] == alt
        assert (photo["width"], photo["height"]) == ("197", "190")
        assert photo["class"].split() == ["lace-frame__photo"] + ([modifier] if modifier else [])
        assert lace["src"] == "/static/img/blonde.png"
        assert lace["alt"] == ""
        assert (lace["width"], lace["height"]) == ("220", "213")
        for image in (photo, lace):
            expected = None if part_id == "vielsen" else "lazy"
            assert image.get("loading") == expected, (part_id, image["src"])


def test_practical_leaves_out_what_later_stories_bring(
    client, practical, django_assert_num_queries
):
    """Story 1.6 boundaries: no map button (7.4), no «Godt å vite» (1.7) and no
    du/dere logic: a one-person household gets the same text as a household of
    several (the placeholder text stays as written until 7.4)."""
    main = main_html(practical)
    assert "veibeskrivelse" not in main
    assert "Godt å vite" not in main
    with django_assert_num_queries(3):
        one = client.get(f"/{SYNNE}/praktisk/").content.decode()
    assert page_text(main_html(one)) == page_text(main)


# Vår historie (UX-DR14)


def test_story_has_one_sheet_labelled_by_the_title_and_no_jump_links(story):
    """UX-DR14, EXPERIENCE.md > Story sheet: no «Hopp til»; one story sheet,
    labelled by the page's `h1`, whose id is `sidetittel`."""
    assert story.count("<h1") == 1
    assert '<h1 class="info-page__title" id="sidetittel">' in story
    main = main_html(story)
    assert "Hopp til" not in main
    sections = sections_of(main)
    assert [attrs for attrs, _ in sections] == [
        {"class": "paper-sheet story-sheet", "aria-labelledby": "sidetittel"}
    ]


def test_story_chapters_are_h2_with_one_hidden_dot_each(story):
    """UX-DR14: nine chapter `h2`s in the approved order, each a time · place
    line whose dot is one aria-hidden span; they match the mockup's chapters."""
    (_, body) = sections_of(main_html(story))[0]
    headings = re.findall(r"<h2>(.*?)</h2>", body, re.DOTALL)
    assert [page_text(heading) for heading in headings] == CHAPTERS
    for heading in headings:
        assert heading.count(HIDDEN_DOT) == 1, heading
        assert heading.count("·") == 1, heading
    mockup = re.findall(r'<h2 class="ch">(.*?)</h2>', STORY_MOCKUP)
    assert mockup == CHAPTERS


def test_story_text_is_the_approved_text_with_the_signature_last(story):
    """UX-DR14, AD-17: the sheet's text is the approved mockup's word for word,
    the closing line before the signature, and the signature the last thing
    on the sheet."""
    (_, body) = sections_of(main_html(story))[0]
    mockup = re.search(r'<section class="sheet story">(.*?)</section>', STORY_MOCKUP, re.S)
    assert page_text(body) == page_text(mockup.group(1))
    assert html_module.unescape(page_text(body)).endswith("sammen med dere! Rikke & Valdemar")
    closing = body.index('<p class="story-sheet__closing">')
    signature = body.index('<p class="story-sheet__signature">Rikke &amp; Valdemar</p>')
    assert closing < signature
    assert body[signature:].rstrip().endswith("</p>")
    assert body.count("<p") == len(CHAPTERS) + 2


def test_story_image_is_the_view_photo_in_the_frame_loaded_at_once(story):
    """NFR-5, UX-DR4, UX-DR14: the view photo and the lace in the 220px frame,
    with alt, width and height, loaded at once; exactly these two files."""
    main = main_html(story)
    images = [tag_attrs(tag) for tag in re.findall(r"<img\b[^>]*>", main)]
    assert {image["src"] for image in images} == {
        "/static/img/oss-utsikt.jpg",
        "/static/img/blonde.png",
    }
    photo, lace = images
    assert photo["alt"] == "Rikke og Valdemar med utsikt."
    assert (photo["width"], photo["height"]) == ("197", "190")
    assert lace["alt"] == ""
    assert (lace["width"], lace["height"]) == ("220", "213")
    assert all("loading" not in image for image in images)
    assert '<div class="lace-frame lace-frame--info">' in main
