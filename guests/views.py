"""Guest views.

The private-invitation page G1 for the bare address and for every link code
(Story 1.4b, FR-5), and the local style sample (Story 1.4a). The invitation's
front page under `/<code>/` arrives with Story 1.5.
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
    """UX-DR1, UX-DR2, UX-DR3, UX-DR15, UX-DR17, UX-DR53, UX-DR54: the design sample.

    A local-only page (Rikke's decision, 2026-11-18) where the couple and the
    examiner can see the design system and run the forced-colours, reduced-motion
    and font checks in docs/manual-test-plan.md (MT-2 to MT-4). It holds no
    personal data and reads nothing from the database. `guests/urls.py` only
    adds its URL when `APP_ENV` is `local`.
    """
    return render(request, "guests/style_sample.html", {"colour_tokens": COLOUR_TOKENS})


PRIVATE_INVITATION = "guests/private_invitation.html"


def private_invitation(request: HttpRequest) -> HttpResponse:
    """FR-5, UX-DR5: the bare address `/` shows only the private-invitation page G1.

    No names, phone numbers, date, place, seal, nav bar or footer. It reads
    nothing from the database, so it renders on an empty, migrated one.
    """
    return render(request, PRIVATE_INVITATION)


def front_page(request: HttpRequest, code: str) -> HttpResponse:
    """FR-5: every `/<code>/` shows G1 with status 404 until Story 1.5.

    The visitor sees the same page as on `/`; the 404 tells crawlers and link
    scanners that the code is not a page. It is a normal response, so `DEBUG`
    never shows Django's technical 404 with the URL list. Story 1.5 puts the
    resolver (`wedding.links.resolve_code`) and the invitation's front page
    here, and keeps G1 for a code that resolves to nobody. Until then the code
    is not looked up, so the view reads nothing from the database.
    """
    return render(request, PRIVATE_INVITATION, status=404)
