"""The invitation's colours, type, buttons and notices (Story 1.4a), and the paper
sheet, page texture and column (Story 1.4b).

The stylesheet is read as text and compared with the DESIGN.md frontmatter, so
a token changed in one place and not the other fails here (UX-DR1). The
templates are rendered for every row of the story's I/O matrix: the notice
include (UX-DR17) and the local style sample `/stil/`. What only a browser can
show (forced colours, reduced motion, the fonts themselves) is MT-2 to MT-4 in
docs/manual-test-plan.md.
"""

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest
from django.template.loader import render_to_string

from guests.views import COLOUR_TOKENS

BASE_DIR = Path(__file__).resolve().parent.parent
DESIGN_MD = (
    BASE_DIR
    / ".docs"
    / "planning-artifacts"
    / "ux-designs"
    / "ux-aill-handle-it-2026-11-10"
    / "DESIGN.md"
)
STATIC_DIR = BASE_DIR / "static"
SITE_CSS = STATIC_DIR / "css" / "site.css"
CSS_FILES = sorted((STATIC_DIR / "css").glob("*.css"))
FONT_FILES = ("imperial-script-400.woff2", "eb-garamond-roman.woff2", "eb-garamond-italic.woff2")
PAPER_FILTERS = BASE_DIR / "wedding" / "templates" / "wedding" / "components" / "paper-filters.html"
REDUCED_MOTION_QUERY = "@media (prefers-reduced-motion: no-preference)"
FORCED_COLORS_QUERY = "@media (forced-colors: active)"
SMALL_PHONE_QUERY = "@media (max-width: 339.98px)"
NARROW_QUERY = "@media (max-width: 259.98px)"
DATA_URI = r'url\("(data:[^"]*)"\)'
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
TEXTURES = ("grain-sheet", "fibre-sheet", "grain-green")

# A path that only the icon of that variant has (DESIGN.md, Notice: check,
# circle with «!», triangle with «!», «i»).
ICON_MARKS = {
    "success": "M7 12.4l3.3 3.3L17.2 8.8",
    "warning": "M12 6.4v7.2",
    "error": "M12 2.6L22.4 20.8H1.6z",
    "info": "M12 10.6v7",
}
PREFIXES = {"error": "Feil:", "warning": "Obs:"}


# Helpers: DESIGN.md frontmatter and the stylesheet as text


def _design_frontmatter() -> dict[str, dict]:
    """Parse the parts of the DESIGN.md frontmatter the stylesheet must mirror.

    The frontmatter is plain two-level YAML (`section:` / `  key: value` /
    `    key: value`), so a line reader is enough and no YAML library is needed.
    """
    text = DESIGN_MD.read_text(encoding="utf-8")
    front = text.split("\n---\n", 1)[0].removeprefix("---\n")
    sections: dict[str, dict] = {}
    section: dict = {}
    group: dict = {}
    for line in front.splitlines():
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, _, value = line.strip().partition(":")
        key = key.strip("'\"")
        value = value.strip().strip("'\"")
        if indent == 0:
            section = sections.setdefault(key, {})
        elif indent == 2 and value:
            section[key] = value
        elif indent == 2:
            group = section.setdefault(key, {})
        else:
            group[key] = value
    return sections


DESIGN = _design_frontmatter()


def _css(path: Path = SITE_CSS) -> str:
    """The stylesheet without comments, so comments can mention what rules forbid."""
    return re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


def _block(css: str, opening: str) -> str:
    """The text inside the braces that follow `opening` (for example a media query)."""
    start = css.index(opening)
    depth = 0
    for index in range(css.index("{", start), len(css)):
        if css[index] == "{":
            depth += 1
        elif css[index] == "}":
            depth -= 1
            if depth == 0:
                return css[css.index("{", start) + 1 : index]
    raise AssertionError(f"unbalanced braces after {opening}")


def _without_block(css: str, opening: str) -> str:
    """The stylesheet with the block after `opening` cut out."""
    inner = _block(css, opening)
    return css.replace(inner, "")


def _custom_properties(css: str) -> dict[str, str]:
    """Every custom property declared in `:root`, name without the leading `--`."""
    root = _block(css, ":root {")
    return {
        name: value.strip() for name, value in re.findall(r"--([a-z0-9-]+)\s*:\s*([^;]+);", root)
    }


def _rules(css: str) -> list[tuple[str, str]]:
    """Every innermost rule as (selector, declarations); media queries are flattened."""
    return [
        (selector.strip(), body)
        for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)
        if not selector.strip().startswith("@")
    ]


def _declarations(css: str, selector: str) -> str:
    """All declarations of the rules whose selector is exactly `selector`."""
    return "\n".join(body for rule, body in _rules(css) if rule == selector)


def _selector_parts(selector: str) -> list[str]:
    """The comma-separated parts of a selector, ignoring commas inside `:where(...)`,
    each with its whitespace collapsed."""
    parts, depth, current = [], 0, ""
    for char in selector:
        depth += {"(": 1, ")": -1}.get(char, 0)
        if char == "," and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return [" ".join(part.split()) for part in parts]


def _bodies(css: str, part: str) -> str:
    """All declarations of the rules that have `part` as one of their selector parts."""
    return "\n".join(body for rule, body in _rules(css) if part in _selector_parts(rule))


ROOT = _custom_properties(_css())


# Tokens (UX-DR1)


@pytest.mark.parametrize("name", sorted(DESIGN["colors"]))
def test_every_colour_token_has_the_design_value(name):
    """UX-DR1: `--color-<name>` exists with exactly the DESIGN.md value."""
    assert ROOT.get(f"color-{name}") == DESIGN["colors"][name]


@pytest.mark.parametrize("name", sorted(DESIGN["spacing"]))
def test_every_spacing_token_has_the_design_value(name):
    """UX-DR1: `--space-<name>` exists with exactly the DESIGN.md value."""
    assert ROOT.get(f"space-{name}") == DESIGN["spacing"][name]


@pytest.mark.parametrize("name", sorted(DESIGN["rounded"]))
def test_every_radius_token_has_the_design_value(name):
    """UX-DR1: `--radius-<name>` exists with exactly the DESIGN.md value."""
    assert ROOT.get(f"radius-{name}") == DESIGN["rounded"][name]


def test_frontmatter_parser_found_every_token():
    """UX-DR1: a sanity check on the line reader, so the token tests cannot shrink
    silently if it drops keys (counts as in DESIGN.md on 2026-11-18)."""
    assert len(DESIGN["colors"]) == 17
    assert len(DESIGN["spacing"]) == 24
    assert len(DESIGN["rounded"]) == 4
    assert len(DESIGN["typography"]) == 21


@pytest.mark.parametrize(
    ("prefix", "section"), [("color-", "colors"), ("space-", "spacing"), ("radius-", "rounded")]
)
def test_every_css_token_comes_from_design(prefix, section):
    """UX-DR1: no colour, spacing or radius token in the stylesheet that DESIGN.md lacks."""
    names = [name.removeprefix(prefix) for name in ROOT if name.startswith(prefix)]
    assert names
    assert [name for name in names if name not in DESIGN[section]] == []


@pytest.mark.parametrize("role", sorted(DESIGN["typography"]))
def test_every_type_role_is_in_rem_with_the_design_values(role):
    """UX-DR2, NFR-5: DESIGN.md's px sizes become rem (px / 16), with the same
    line height, letter spacing and any weight other than 400."""
    token = DESIGN["typography"][role]
    pixels = int(token["fontSize"].removesuffix("px"))
    assert ROOT.get(f"font-size-{role}") == f"{pixels / 16:g}rem"
    assert ROOT.get(f"line-height-{role}") == token["lineHeight"]
    assert ROOT.get(f"letter-spacing-{role}") == token.get("letterSpacing")
    weight = token["fontWeight"]
    assert ROOT.get(f"font-weight-{role}") == (None if weight == "400" else weight)


def test_font_families_match_design():
    """UX-DR2: every type role uses one of the two self-hosted families."""
    families = {token["fontFamily"] for token in DESIGN["typography"].values()}
    assert families == {"Imperial Script", "EB Garamond"}
    assert ROOT["font-script"].startswith('"Imperial Script"')
    assert ROOT["font-serif"].startswith('"EB Garamond"')


def test_light_only_and_body_text():
    """UX-DR1, UX-DR2: light only; guest body text 20px (1.25rem) with lining figures."""
    css = _css()
    assert "color-scheme: light only;" in _block(css, ":root {")
    body = _declarations(css, "body")
    assert "font-size: var(--font-size-body);" in body
    assert ROOT["font-size-body"] == "1.25rem"
    assert "font-variant-numeric: lining-nums;" in body


# Rules that hold for every stylesheet


@pytest.mark.parametrize("path", CSS_FILES, ids=lambda path: path.name)
def test_every_font_size_is_in_rem(path):
    """NFR-5, UX-DR2: no px font sizes, so the phone's text-size setting scales all text."""
    css = _css(path)
    sizes = re.findall(r"(?<![-\w])font-size\s*:\s*([^;]+);", css)
    if path == SITE_CSS:
        assert sizes
    for size in sizes:
        variable = re.fullmatch(r"var\(--(font-size-[a-z-]+)\)", size.strip())
        value = ROOT.get(variable.group(1), "") if variable else size.strip()
        assert re.fullmatch(r"\d+(\.\d+)?rem", value), size
    shorthands = re.findall(r"(?<![-\w])font\s*:\s*([^;]+);", css)
    assert all(value.strip() == "inherit" for value in shorthands)


@pytest.mark.parametrize("path", CSS_FILES, ids=lambda path: path.name)
def test_outline_is_never_removed(path):
    """UX-DR15, NFR-5: no `outline: none` or a zero-width outline (`0`, `0px`, `0rem` ...)."""
    css = _css(path)
    zero = r"(none|0(\.0+)?[a-z%]*)(?=[\s;!}]|$)"
    assert not re.search(rf"outline(-style)?\s*:\s*{zero}", css)
    assert not re.search(rf"outline-width\s*:\s*{zero}", css)


@pytest.mark.parametrize("path", CSS_FILES, ids=lambda path: path.name)
def test_nothing_moves_by_itself(path):
    """UX-DR54: no keyframes, animations or transitions."""
    css = _css(path)
    assert "@keyframes" not in css
    assert not re.search(r"(?<![-\w])(animation|transition)[\w-]*\s*:", css)


@pytest.mark.parametrize("path", CSS_FILES, ids=lambda path: path.name)
def test_every_url_points_to_a_local_file(path):
    """AD-15, UX-DR2, UX-DR3: nothing is loaded from another site. Every `url()`
    file exists, and every `url(#id)` names a filter in the paper-filters include.
    A whole data-URI is skipped (the texture SVGs hold their own `url(%23t)`),
    after checking that its only `://` is the SVG namespace."""
    css = _css(path)
    assert "@import" not in css
    for data_uri in re.findall(DATA_URI, css):
        assert "://" not in data_uri.replace(SVG_NAMESPACE, ""), data_uri
    filters = PAPER_FILTERS.read_text(encoding="utf-8")
    for url in re.findall(r"url\(\s*[\"']?([^\"')]+)[\"']?\s*\)", re.sub(DATA_URI, "", css)):
        assert "://" not in url
        assert not url.startswith("//")
        if url.startswith("#"):
            assert f'id="{url[1:]}"' in filters, url
            continue
        assert (path.parent / url).resolve().is_file(), url


def test_smooth_scroll_only_without_reduced_motion():
    """UX-DR54: smooth scrolling is set only under `prefers-reduced-motion: no-preference`."""
    css = _css()
    assert "scroll-behavior: smooth;" in _block(css, REDUCED_MOTION_QUERY)
    assert "scroll-behavior" not in _without_block(css, REDUCED_MOTION_QUERY)


# Fonts (UX-DR2)


@pytest.mark.parametrize("name", FONT_FILES)
def test_font_files_exist_and_are_woff2(name):
    """UX-DR2: self-hosted WOFF2 files (the signature `wOF2`)."""
    font = STATIC_DIR / "fonts" / name
    assert font.read_bytes()[:4] == b"wOF2"
    assert f'url("../fonts/{name}") format("woff2")' in _css()


def test_font_licences_are_committed_beside_the_fonts():
    """UX-DR2: both families are SIL OFL, and the licence travels with the files."""
    for licence in ("imperial-script-OFL.txt", "eb-garamond-OFL.txt"):
        text = (STATIC_DIR / "fonts" / licence).read_text(encoding="utf-8")
        assert "SIL Open Font License, Version 1.1" in text


# Focus ring, buttons and forced colours (UX-DR15, UX-DR53)


def test_focus_ring_on_focus_and_press_in_the_surface_colour():
    """UX-DR15: 3px at 3px offset on `:focus-visible` and `:active`, coloured by surface."""
    rules = _rules(_css())
    focus_rules = [
        (_selector_parts(selector), body)
        for selector, body in rules
        if ":focus-visible" in _selector_parts(selector)
    ]
    assert [parts for parts, _body in focus_rules] == [
        [":focus-visible", ":where(a, button, input, select, textarea, summary):active"]
    ]
    focus = [body for _parts, body in focus_rules]
    assert "outline: var(--space-focus-width) solid var(--focus-color);" in focus[0]
    assert "outline-offset: var(--space-focus-offset);" in focus[0]
    assert ROOT["focus-color"] == "var(--color-focus-on-green)"
    surface = _bodies(_css(), ".surface-cream")
    assert "--focus-color: var(--color-focus-on-panel);" in surface


def test_press_never_rings_the_whole_page():
    """UX-DR15: browsers mark every ancestor of a pressed element `:active`, so the
    press ring is limited to interactive elements; no bare `:active` selector."""
    allowed = re.compile(
        r"(\.button(--[a-z-]+)?|a|:where\(a, button, input, select, textarea, summary\)):active"
    )
    actives = [
        part
        for selector, _body in _rules(_css())
        for part in _selector_parts(selector)
        if ":active" in part
    ]
    assert actives
    assert [part for part in actives if not allowed.fullmatch(part)] == []


def test_primary_button():
    """UX-DR15, DESIGN.md button-primary: cream on dark green, transparent border, 52px."""
    css = _css()
    body = _bodies(css, ".button")
    assert "background-color: var(--color-green-dark);" in body
    assert "color: var(--color-cream-on-green);" in body
    assert "border: var(--button-border-width) solid transparent;" in body
    assert "min-height: var(--space-button-height);" in body
    assert "background-color: var(--color-green-dark-hover);" in _bodies(css, ".button:hover")


@pytest.mark.parametrize(
    ("variant", "colour"), [("secondary", "green-dark"), ("destructive", "error")]
)
def test_outlined_buttons_on_cream(variant, colour):
    """UX-DR15, DESIGN.md button-secondary / button-destructive: outline in the
    text colour on cream, 44px, and a 3px outline on hover and press."""
    css = _css()
    body = _bodies(css, f".button--{variant}")
    assert f"color: var(--color-{colour});" in body
    assert "border-color: currentColor;" in body
    assert "background-color: var(--color-panel-cream);" in body
    assert "min-height: var(--space-target-min);" in body
    for state in ("hover", "active"):
        assert "--button-border-width: 3px;" in _bodies(css, f".button--{variant}:{state}")


def test_outlined_button_on_green():
    """UX-DR15, DESIGN.md button-on-green: transparent with cream text, 44px, 3px on press."""
    css = _css()
    body = _bodies(css, ".button--on-green")
    assert "background-color: transparent;" in body
    assert "color: var(--color-cream-on-green);" in body
    assert "border-color: currentColor;" in body
    assert "min-height: var(--space-target-min);" in body
    for state in ("hover", "active"):
        assert "--button-border-width: 3px;" in _bodies(css, f".button--on-green:{state}")


@pytest.mark.parametrize("surface", [".surface-cream", ".paper-sheet"])
def test_outlined_button_on_cream_is_drawn_in_ink(surface):
    """DESIGN.md, Outlined button on green: on a cream sheet the same shape is ink."""
    assert "color: var(--color-ink);" in _bodies(_css(), f"{surface} .button--on-green")


def _rules_with_parts(css: str, parts: set[str]) -> list[str]:
    """The declarations of every rule whose selector list holds all of `parts`."""
    return [body for rule, body in _rules(css) if parts <= set(_selector_parts(rule))]


@pytest.mark.parametrize(
    ("declaration", "selector"),
    [
        ("color: var(--color-ink);", ".surface-cream"),
        ("--focus-color: var(--color-focus-on-panel);", ".surface-cream"),
        ("color: var(--color-ink);", ".surface-cream .button--on-green"),
    ],
)
def test_paper_sheet_shares_the_cream_surface_rules(declaration, selector):
    """UX-DR3, spec 1.4b: the sheet joins `.surface-cream`'s selector lists for ink
    text, the dark green focus ring and the ink outlined button, so the two
    surfaces cannot drift apart; nothing is copied into a rule of its own."""
    css = _css()
    sheet = selector.replace(".surface-cream", ".paper-sheet")
    assert any(declaration in body for body in _rules_with_parts(css, {selector, sheet}))
    assert declaration not in _declarations(css, sheet)


def test_paper_sheet_draws_everything_on_a_layer_behind_the_content():
    """UX-DR3, DESIGN.md components.paper-sheet: cream, 5px corners, the sheet
    texture and the edge-b3 filter sit on `::before` behind the content; the
    sheet itself is never filtered, so text and focus rings stay sharp."""
    css = _css()
    sheet = _declarations(css, ".paper-sheet")
    assert "position: relative;" in sheet
    assert "isolation: isolate;" in sheet
    layer = _declarations(css, ".paper-sheet::before")
    for declaration in (
        'content: "";',
        "inset: 0;",
        "z-index: -1;",
        "background-color: var(--color-panel-cream);",
        "border-radius: var(--radius-sheet);",
        "background-image: var(--grain-sheet), var(--fibre-sheet);",
        "background-blend-mode: overlay, overlay;",
        "filter: url(#edge-b3);",
    ):
        assert declaration in layer, declaration
    unfiltered = [
        rule
        for rule, body in _rules(_without_block(css, FORCED_COLORS_QUERY))
        if "filter:" in body and rule != ".paper-sheet::before"
    ]
    assert unfiltered == []


def test_page_has_the_calm_green_texture():
    """UX-DR3, DESIGN.md components.page: page-green with grain-green, overlay."""
    body = _declarations(_css(), "body")
    assert "background-color: var(--color-page-green);" in body
    assert "background-image: var(--grain-green);" in body
    assert "background-blend-mode: overlay;" in body


@pytest.mark.parametrize("name", TEXTURES)
def test_texture_keeps_the_average_colour(name):
    """UX-DR3, DESIGN.md > Paper texture: each texture is an inline SVG data-URI
    without `;utf8` (the parser splits on `;`) whose colour matrix maps the noise
    around mid-grey (offset + slope / 2 = 0.5 per channel), so `overlay` leaves
    the average colour and the measured contrast unchanged."""
    value = ROOT[name]
    assert value.startswith('url("data:image/svg+xml,<svg ')
    assert ";" not in value
    matrix = [float(number) for number in re.search(r"values='([^']+)'", value).group(1).split()]
    for row in range(3):
        coefficients = matrix[row * 5 : row * 5 + 5]
        assert sum(coefficients[:4]) / 2 + coefficients[4] == pytest.approx(0.5), (name, row)


def test_forced_colours_keep_outlines_rules_and_focus():
    """UX-DR53: under forced colours the buttons keep an outline, cream surfaces an
    edge and the focus ring a system colour; the notice rule is `currentColor`."""
    css = _css()
    forced = _block(css, FORCED_COLORS_QUERY)
    assert "border-color: ButtonText;" in forced
    assert "--focus-color: CanvasText;" in forced
    assert "border: 1px solid CanvasText;" in forced
    assert "border-left: 4px solid currentColor;" in _declarations(css, ".notice")


def test_forced_colours_give_the_sheet_a_border_and_drop_the_texture():
    """UX-DR53, DESIGN.md > Elevation & Depth: the sheet becomes a flat panel with a
    1px CanvasText border and its focus ring a system colour; the page and the
    sheet layer lose texture and filter."""
    forced = _block(_css(), FORCED_COLORS_QUERY)
    assert "border: 1px solid CanvasText;" in _bodies(forced, ".paper-sheet")
    assert "--focus-color: CanvasText;" in _bodies(forced, ".paper-sheet")
    for selector in ("body", ".paper-sheet::before"):
        assert "background-image: none;" in _bodies(forced, selector), selector
    assert "filter: none;" in _bodies(forced, ".paper-sheet::before")


def test_column_gutters_narrow_with_the_tokens():
    """UX-DR30, NFR-5, DESIGN.md > Grid and gutters: one centred column of at most
    content-max with the gutter; 260 to 339.98px uses the small-phone gutter, and
    below 260px the narrow gutter, for the column and the G1 sheet's padding."""
    css = _css()
    column = _declarations(css, ".column")
    assert "max-width: var(--space-content-max);" in column
    assert "margin-inline: auto;" in column
    assert "padding-inline: var(--space-gutter);" in column
    small = _block(css, SMALL_PHONE_QUERY)
    assert "padding-inline: var(--space-gutter-small-phone);" in _bodies(small, ".column")
    narrow = _block(css, NARROW_QUERY)
    assert "padding-inline: var(--space-gutter-narrow);" in _bodies(narrow, ".column")
    sheet = _bodies(narrow, ".private-invitation__sheet")
    assert "padding-inline: var(--space-gutter-narrow);" in sheet


# Base template


def test_base_template_declares_language_colour_scheme_and_local_css():
    """UX-DR1, NFR-5: `lang="nb"`, light only, and the stylesheet from our own server."""
    html = render_to_string("wedding/base.html")
    assert '<html lang="nb">' in html
    assert '<meta name="color-scheme" content="light only">' in html
    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in html
    assert '<link rel="stylesheet" href="/static/css/site.css">' in html
    assert "://" not in html


def test_base_template_holds_the_edge_filter_once_and_hidden():
    """UX-DR3: the edge-b3 filter is an inline SVG at the start of `<body>`, hidden
    from screen readers and zero-size by class, without xmlns (no `://` above)."""
    html = render_to_string("wedding/base.html")
    body = html[html.index("<body>") :]
    assert body.count('<filter id="edge-b3"') == 1
    svg = re.search(r"<svg[^>]*>", body).group(0)
    assert 'class="paper-filters"' in svg
    assert 'aria-hidden="true"' in svg
    assert 'focusable="false"' in svg
    assert "xmlns" not in svg
    assert "display: none" not in _declarations(_css(), ".paper-filters")


# The notice include (UX-DR17): every row of the I/O matrix


class _NoticeParser(HTMLParser):
    """Collects the notice's root attributes, its icon's attributes and its text."""

    def __init__(self):
        super().__init__()
        self.root: dict[str, str | None] | None = None
        self.icon: dict[str, str | None] | None = None
        self.paths: list[str] = []
        self.text_parts: list[str] = []
        self._in_text = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "div" and self.root is None:
            self.root = attributes
        elif tag == "svg":
            self.icon = attributes
        elif tag == "path":
            self.paths.append(attributes.get("d") or "")
        elif tag == "p":
            self._in_text = True

    def handle_endtag(self, tag):
        if tag == "p":
            self._in_text = False

    def handle_data(self, data):
        if self._in_text:
            self.text_parts.append(data)

    @property
    def text(self) -> str:
        return " ".join("".join(self.text_parts).split())


def _notice(variant: str, text: str = "Prøv igjen.", **context) -> _NoticeParser:
    html = render_to_string(
        "wedding/components/notice.html", {"variant": variant, "text": text, **context}
    )
    parser = _NoticeParser()
    parser.feed(html)
    return parser


@pytest.mark.parametrize("variant", ["success", "warning", "error", "info"])
def test_notice_at_load_is_not_a_live_region(variant):
    """UX-DR17: a notice present at page load has no `role` and no `aria-live`."""
    notice = _notice(variant)
    assert notice.root is not None
    assert "role" not in notice.root
    assert "aria-live" not in notice.root
    assert notice.root["class"] == f"notice notice--{variant}"


def test_error_notice_has_triangle_icon_and_prefix():
    """UX-DR17: error = triangle «!» icon, 4px rule (class) and «Feil:» first."""
    notice = _notice("error", "Velg «Kommer» eller «Kommer ikke» for bestemor.")
    assert ICON_MARKS["error"] in notice.paths
    assert notice.text == "Feil: Velg «Kommer» eller «Kommer ikke» for bestemor."


@pytest.mark.parametrize("variant", ["success", "warning", "error", "info"])
def test_each_variant_has_its_own_hidden_icon(variant):
    """UX-DR17: a 22px SVG icon per variant, hidden from screen readers; its shape is
    the variant's own, so state never depends on colour (WCAG 1.4.1)."""
    notice = _notice(variant)
    assert notice.icon is not None
    assert notice.icon["aria-hidden"] == "true"
    assert notice.icon["focusable"] == "false"
    marks = {name for name, mark in ICON_MARKS.items() if mark in notice.paths}
    assert marks == {variant}


@pytest.mark.parametrize(
    ("variant", "expected"),
    [
        ("error", "Feil: Prøv igjen."),
        ("warning", "Obs: Prøv igjen."),
        ("success", "Prøv igjen."),
        ("info", "Prøv igjen."),
    ],
)
def test_only_error_and_warning_get_a_prefix(variant, expected):
    """UX-DR17: «Feil:» and «Obs:» only; info and success have no prefix."""
    assert _notice(variant).text == expected


@pytest.mark.parametrize(
    ("variant", "role"),
    [("error", "alert"), ("warning", "status"), ("success", "status"), ("info", "status")],
)
def test_notice_added_later_is_a_live_region(variant, role):
    """UX-DR17: `live=True` makes a live region: errors assertive, the others polite."""
    assert _notice(variant, live=True).root["role"] == role


def test_unknown_variant_renders_as_info():
    """UX-DR17: an unknown variant falls back to info, with no prefix."""
    notice = _notice("oops")
    assert notice.root["class"] == "notice notice--info"
    assert ICON_MARKS["info"] in notice.paths
    assert notice.text == "Prøv igjen."
    assert "role" not in notice.root


def test_notice_text_is_escaped():
    """NFR-4: text passed to the notice is escaped, never rendered as HTML."""
    html = render_to_string(
        "wedding/components/notice.html", {"variant": "info", "text": "<b>Hei</b>"}
    )
    assert "&lt;b&gt;Hei&lt;/b&gt;" in html


# The style sample /stil/ (Rikke's decision, 2026-11-18)


def test_style_sample_shows_every_button_and_notice_locally(client):
    """UX-DR1, UX-DR15, UX-DR17, UX-DR54: `/stil/` renders on the base template with
    the four buttons, the four notices and a jump link for the motion check (MT-3)."""
    response = client.get("/stil/")
    assert response.status_code == 200
    page = response.content.decode()
    link = '<link rel="stylesheet" href="/static/css/style-sample.css">'
    assert link in page
    assert page.index(link) < page.index("</head>")
    assert "wedding/base.html" in [template.name for template in response.templates]
    html = response.content.decode()
    for button in (
        'class="button"',
        "button--secondary",
        "button--destructive",
        "button--on-green",
    ):
        assert button in html
    for variant in ("success", "warning", "error", "info"):
        assert f"notice notice--{variant}" in html
    assert "Obs: Svaret er ikke sendt ennå." in " ".join(html.split())
    assert 'href="#varsler"' in html
    assert 'id="varsler"' in html
    assert "://" not in html


def test_style_sample_swatches_follow_design():
    """UX-DR1: the swatch list is DESIGN.md's colour keys in frontmatter order, and
    every swatch has a chip rule painted with its own token."""
    assert list(COLOUR_TOKENS) == list(DESIGN["colors"])
    sample_css = _css(STATIC_DIR / "css" / "style-sample.css")
    for token in COLOUR_TOKENS:
        body = _bodies(sample_css, f".sample__chip--{token}")
        assert f"background-color: var(--color-{token});" in body, token


def test_style_sample_shows_a_paper_sheet(client):
    """UX-DR3, spec 1.4b: `/stil/` has a `.paper-sheet` sample with a link and the
    outlined button, so ink text and the focus ring can be compared with
    `.surface-cream` in a browser (CSS rules: the sharing test above)."""
    html = client.get("/stil/").content.decode()
    sample = html[html.index('class="paper-sheet') :]
    sample = sample[: sample.index("</section>")]
    assert "<a href=" in sample
    assert "button--on-green" in sample


def test_style_sample_does_not_exist_in_production(client, production_urls):
    """Rikke's decision, 2026-11-18: with `APP_ENV=production` the URLconf has no
    `/stil/`; the path is then read as a link code and shows G1 with 404 (FR-5)."""
    response = client.get("/stil/")
    assert "style_sample" not in [pattern.name for pattern in production_urls]
    assert response.status_code == 404
    page = response.content.decode()
    assert "Dette er en privat invitasjon" in page
    assert "Stilprøve" not in page
    assert "guests/private_invitation.html" in [template.name for template in response.templates]
