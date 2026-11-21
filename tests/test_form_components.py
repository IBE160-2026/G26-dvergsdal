"""The RSVP form's components in the stylesheet, and em breakpoints (Story 2.1).

FR-14, FR-22, UX-DR16, UX-DR18, UX-DR19, UX-DR30, NFR-5; DESIGN.md > Choice
control, Error summary, Form step. Its own file, as the Epic 1 retrospective
asked when Epic 2 adds form components; the shared stylesheet readers come
from test_design_system.py. The choice control (26px native radio in
green-dark, row at least 44px), the borderless group, the 22px field error
icon, the summary links at least 44px, and the actions (column, 12px apart,
24px below). Besides: every width in a `@media` or `@container` query is in em
(DESIGN.md > Narrow widths, rule of 2026-11-21), except three px breakpoints
from Epic 1 that are routed to deferred-work.md. How the form looks in a
browser at 360, 320 and 180 CSS px and with 20px text is MT-25.
"""

import re

from tests.test_design_system import DESIGN, ROOT, _bodies, _css

# Epic 1's px breakpoints, to be converted to em (deferred-work.md, Story 2.1).
PX_ALLOWED = {"339.98px", "299.98px", "259.98px"}


def _value(declarations: str, prop: str) -> str:
    values = re.findall(rf"(?<![-\w]){re.escape(prop)}\s*:\s*([^;]+);", declarations)
    assert values, prop
    return values[-1].strip()


def _resolved(value: str) -> str:
    """A `var(--token)` resolved from `:root`, anything else as it is."""
    match = re.fullmatch(r"var\(--([a-z0-9-]+)\)", value)
    return ROOT[match.group(1)] if match else value


def test_choice_control_is_a_26px_native_radio_in_green_dark():
    """UX-DR16, DESIGN.md components.choice-control: 26px box, the selected mark in
    green-dark through accent-color, which survives forced colours."""
    radio = _bodies(_css(), ".choice input")
    assert DESIGN["components"]["choice-control"]["box"] == "26px"
    assert _value(radio, "width") == "26px"
    assert _value(radio, "height") == "26px"
    assert _value(radio, "accent-color") == "var(--color-green-dark)"
    assert _value(radio, "flex") == "none"


def test_whole_choice_row_is_a_44px_target():
    """UX-DR16, NFR-5: the label is the row, at least 44px tall."""
    row = _bodies(_css(), ".choice")
    assert _value(row, "display") == "flex"
    assert _resolved(_value(row, "min-height")) == "44px"


def test_group_has_no_border_and_a_label_legend():
    """DESIGN.md > Choice control: no border on the group; the legend in `label`
    (20px, 600). `min-width: 0` stops a fieldset from overflowing at 180 CSS px."""
    css = _css()
    group = _bodies(css, ".form-group")
    assert _value(group, "border") == "none"
    assert _value(group, "min-width") == "0"
    legend = _bodies(css, ".form-group > legend")
    assert _value(legend, "font-size") == "var(--font-size-label)"
    assert _value(legend, "font-weight") == "var(--font-weight-label)"


def test_field_error_is_a_22px_icon_and_text_in_the_error_colour():
    """UX-DR16, DESIGN.md > Choice control: the error line under the legend."""
    css = _css()
    line = _bodies(css, ".form-sheet .field-error")
    assert _value(line, "color") == "var(--color-error)"
    icon = _bodies(css, ".field-error__icon")
    assert _value(icon, "width") == "22px"
    assert _value(icon, "height") == "22px"


def test_error_summary_links_are_44px_targets():
    """FR-22, UX-DR16, NFR-5: each summary link at least 44px tall."""
    link = _bodies(_css(), ".error-summary__list a")
    assert _resolved(_value(link, "min-height")) == "44px"


def test_bytt_is_a_44px_underlined_summary():
    """UX-DR18, DESIGN.md > Respondent line: «Bytt» looks like an underlined link
    and is at least 44 x 44px."""
    summary = _bodies(_css(), ".respondent__switch > summary")
    assert _resolved(_value(summary, "min-height")) == "44px"
    assert _resolved(_value(summary, "min-width")) == "44px"
    assert _value(summary, "text-decoration-line") == "underline"


def test_actions_are_a_column_12px_apart_24px_below():
    """DESIGN.md > Form step: «Fortsett» above «Tilbake», both full width, 12px
    apart, 24px below the content."""
    actions = _bodies(_css(), ".form-actions")
    assert _value(actions, "flex-direction") == "column"
    assert _resolved(_value(actions, "gap")) == "12px"
    assert _resolved(_value(actions, "margin-top")) == "24px"


def test_every_breakpoint_width_is_in_em():
    """UX-DR30, NFR-5 (DESIGN.md > Narrow widths, 2026-11-21): every width in a
    `@media` or `@container` query is in em, so it follows a larger default text
    size; only Epic 1's three px breakpoints remain, routed to deferred-work.md."""
    css = _css()
    queries = re.findall(r"@(?:media|container)\s*([^{]+)\{", css)
    assert queries
    widths = [
        value
        for query in queries
        for value in re.findall(r"(?:min-|max-)?width\s*:\s*([^)]+)\)", query)
    ]
    assert widths
    px = {value.strip() for value in widths if not value.strip().endswith("em")}
    assert px == PX_ALLOWED
