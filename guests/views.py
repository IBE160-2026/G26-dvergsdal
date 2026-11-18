"""Guest views.

For now only the local style sample (Story 1.4a); the guest pages under
`/<code>/` arrive with Story 1.4b and 1.5.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# DESIGN.md colour tokens, in the frontmatter's order, for the swatches.
COLOUR_TOKENS = (
    "page-green",
    "green-dark",
    "green-dark-hover",
    "seal",
    "panel-cream",
    "ink",
    "ink-muted",
    "cream-on-green",
    "field-surface",
    "field-border",
    "divider",
    "focus-on-panel",
    "focus-on-green",
    "error",
    "success",
    "warning",
    "scrim",
)


def style_sample(request: HttpRequest) -> HttpResponse:
    """UX-DR1, UX-DR2, UX-DR15, UX-DR17, UX-DR53, UX-DR54: colours, type, buttons and notices.

    A local-only page (Rikke's decision, 2026-11-18) where the couple and the
    examiner can see the design system and run the forced-colours, reduced-motion
    and font checks in docs/manual-test-plan.md (MT-2 to MT-4). It holds no
    personal data and reads nothing from the database. `guests/urls.py` only
    adds its URL when `APP_ENV` is `local`.
    """
    return render(request, "guests/style_sample.html", {"colour_tokens": COLOUR_TOKENS})
