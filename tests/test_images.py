"""Rikke's images in static/img/ (Story 1.4b, UX-DR4, NFR-7, NFR-5).

`tools/prepare_images.py` writes the files; these tests check what it wrote
without Pillow (not a project dependency): the format from the first bytes,
the width from the file header, no metadata in the JPEGs, transparency kept in
the cutouts, the size budget, the README listing every file, `alt` on every
`<img>` in every template, and the favicon links in base.html.
"""

import re
import struct
from pathlib import Path

import pytest
from django.template.loader import render_to_string

from tests.helpers import FRONT_PAGE

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "static" / "img"
README = IMG_DIR / "README.md"
TEMPLATE_DIRS = (BASE_DIR / "wedding" / "templates", BASE_DIR / "guests" / "templates")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"
START_OF_FRAME = (0xC0, 0xC1, 0xC2)
PROGRESSIVE = 0xC2
SOS = 0xDA
APP1 = 0xE1

ICONS = [
    "fjelltur",
    "hytte",
    "rebus",
    "middag",
    "stamp",
    "frokost",
    "yoga",
    "bil",
    "ringer",
    "lunsj",
    "fest",
    "avreise",
]

# File name -> planned width in pixels (spec 1.4b, Code Map): twice the display
# width, or the source width when the source is smaller.
TARGETS = {
    "segl.png": 148,
    "favicon-32.png": 32,
    "apple-touch-icon.png": 180,
    "brudeslor.png": 448,
    "lilje-topp.png": 592,
    "lilje-bunn.png": 592,
    "blonde.png": 320,
    "illustrasjon.jpg": 524,
    "oss-strand.jpg": 400,
    "oss-utsikt.jpg": 440,
    "sted-middag.jpg": 440,
    "sted-tunet.jpg": 440,
    "sted-kirka.jpg": 440,
    "sted-omradet.jpg": 440,
    "forhandsvisning.jpg": 1000,  # link preview (Story 1.4c, FR-4), never loaded by a page
} | {f"ikoner/ikon-{number:02d}-{name}.png": 112 for number, name in enumerate(ICONS, start=1)}

FILE_BUDGET = 100 * 1024
FRONT_PAGE_BUDGET = 300 * 1024


def _jpeg_segments(data: bytes) -> list[tuple[int, bytes]]:
    """Every JPEG marker segment up to and including SOS, as (marker, payload).

    Fails with an assertion, not a struct or index error, on a malformed file."""
    segments = []
    index = 2
    while index + 4 <= len(data):
        assert data[index] == 0xFF, f"no JPEG marker at byte {index}"
        marker = data[index + 1]
        length = struct.unpack(">H", data[index + 2 : index + 4])[0]
        assert length >= 2, f"bad segment length at byte {index}"
        assert index + 2 + length <= len(data), f"segment at byte {index} runs past the end"
        segments.append((marker, data[index + 4 : index + 2 + length]))
        if marker == SOS:
            return segments
        index += 2 + length
    raise AssertionError("no start-of-scan marker")


def _jpeg_frame_payload(data: bytes) -> tuple[int, bytes]:
    """The start-of-frame marker (0xC0, 0xC1 or 0xC2) and its payload."""
    for marker, payload in _jpeg_segments(data):
        if marker in START_OF_FRAME:
            assert len(payload) >= 5, "short frame header"
            return marker, payload
    raise AssertionError("no JPEG frame header")


def _jpeg_frame(data: bytes) -> tuple[int, int]:
    """The start-of-frame marker (0xC0, 0xC1 or 0xC2) and the image width."""
    marker, payload = _jpeg_frame_payload(data)
    return marker, struct.unpack(">H", payload[3:5])[0]


def _png_chunks(data: bytes) -> dict[bytes, bytes]:
    """Every PNG chunk by type (the last one wins; only single chunks are read)."""
    chunks = {}
    index = len(PNG_MAGIC)
    while index + 8 <= len(data):
        length = struct.unpack(">I", data[index : index + 4])[0]
        kind = data[index + 4 : index + 8]
        assert index + 12 + length <= len(data), f"chunk {kind!r} runs past the end"
        chunks[kind] = data[index + 8 : index + 8 + length]
        index += 12 + length
    return chunks


@pytest.mark.parametrize(("name", "width"), TARGETS.items())
def test_every_planned_image_exists_with_its_format_and_width(name, width):
    """UX-DR4, NFR-7: PNG for cutouts and icons, progressive JPEG for photos and the
    illustration (no WebP or AVIF, so old iPads show them), at the planned width."""
    data = (IMG_DIR / name).read_bytes()
    if name.endswith(".png"):
        assert data.startswith(PNG_MAGIC)
        assert data[25] == 3, "PNG should be palette-quantised (colour type 3)"
        assert struct.unpack(">I", data[16:20])[0] == width
    else:
        assert data.startswith(JPEG_MAGIC)
        assert _jpeg_frame(data) == (PROGRESSIVE, width)


def test_link_preview_image_is_1000_by_525():
    """FR-4, Story 1.4c: the og:image is 1.91:1 and at least 600 x 315, so Messenger
    shows the large card; `og:image:width` and `og:image:height` say the same."""
    _marker, payload = _jpeg_frame_payload((IMG_DIR / "forhandsvisning.jpg").read_bytes())
    assert struct.unpack(">H", payload[1:3])[0] == 525
    assert struct.unpack(">H", payload[3:5])[0] == 1000


@pytest.mark.parametrize("name", [name for name in TARGETS if name.endswith(".jpg")])
def test_jpegs_carry_no_metadata(name):
    """NFR-3: no APP1 segment (EXIF or XMP) in any JPEG, so photos of the couple and
    the venue carry no camera data, place or time."""
    markers = [marker for marker, _payload in _jpeg_segments((IMG_DIR / name).read_bytes())]
    assert APP1 not in markers


@pytest.mark.parametrize(
    "name", [name for name in TARGETS if name.endswith(".png") and name != "apple-touch-icon.png"]
)
def test_cutouts_keep_their_transparency(name):
    """UX-DR4: quantising kept the alpha channel: the palette PNG has a tRNS chunk."""
    assert b"tRNS" in _png_chunks((IMG_DIR / name).read_bytes())


def test_apple_touch_icon_is_opaque():
    """UX-DR4: iOS paints transparency black, so the touch icon has none."""
    alpha = _png_chunks((IMG_DIR / "apple-touch-icon.png").read_bytes()).get(b"tRNS", b"")
    assert set(alpha) <= {255}


def test_static_img_holds_only_the_planned_files():
    """UX-DR4, spec 1.4b: nothing else in static/img/ (no WebP, no leftovers), and no
    images or Python files anywhere else in static/."""
    files = {path.relative_to(IMG_DIR).as_posix() for path in IMG_DIR.rglob("*") if path.is_file()}
    assert files == {*TARGETS, "README.md"}
    static = BASE_DIR / "static"
    strays = [
        path
        for path in static.rglob("*")
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".py"}
        and IMG_DIR not in path.parents
    ]
    assert strays == []


@pytest.mark.parametrize("name", TARGETS)
def test_every_image_is_within_the_file_budget(name):
    """NFR-7: every image file is at most 100 KB."""
    assert (IMG_DIR / name).stat().st_size <= FILE_BUDGET


def test_front_page_images_are_within_their_budget():
    """NFR-7: the front page's images are at most 300 KB together (the fonts add
    about 280 KB more on 4G)."""
    assert sum((IMG_DIR / name).stat().st_size for name in FRONT_PAGE) <= FRONT_PAGE_BUDGET


def test_readme_lists_every_image_and_the_command():
    """UX-DR4: static/img/README.md names every file and how to make them again."""
    text = README.read_text(encoding="utf-8")
    for name in TARGETS:
        assert f"`{name}`" in text, name
    assert "uvx --with pillow==13.0.0 python -I tools/prepare_images.py" in text


def _templates() -> list[Path]:
    return sorted(path for folder in TEMPLATE_DIRS for path in folder.rglob("*.html"))


@pytest.mark.parametrize("path", _templates(), ids=lambda path: path.name)
def test_every_img_has_alt(path):
    """NFR-5: every `<img>` in every template has an `alt` attribute (empty when
    the picture is decoration)."""
    for tag in re.findall(r"<img\b[^>]*>", path.read_text(encoding="utf-8")):
        assert re.search(r"\salt=\"[^\"]*\"", tag), tag


def test_base_template_links_the_favicons():
    """UX-DR4: the tab icon from the seal, 32px PNG and the 180px apple-touch icon,
    inside `{% block icons %}` so G1 can leave them out."""
    html = render_to_string("wedding/base.html")
    assert re.search(
        r'<link rel="icon"\s+type="image/png"\s+sizes="32x32"\s+'
        r'href="/static/img/favicon-32.png">',
        html,
    )
    assert '<link rel="apple-touch-icon" href="/static/img/apple-touch-icon.png">' in html
    source = (BASE_DIR / "wedding" / "templates" / "wedding" / "base.html").read_text(
        encoding="utf-8"
    )
    block = source[source.index("{% block icons %}") : source.index("{% endblock icons %}")]
    assert "favicon-32.png" in block
    assert "apple-touch-icon.png" in block
