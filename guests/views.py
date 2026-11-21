"""Guest views.

The invitation's front page under `/<code>/` and its three info pages (Story
1.5, FR-2, FR-7, FR-8, FR-11; their content in Story 1.6 and, for Programmet
with the meal prices from the settings, Story 1.7, FR-9), the
private-invitation page G1 for the bare address and for every code that
resolves to nobody (Story 1.4b, FR-5), the local style sample (Story 1.4a),
and the site-wide error pages for 404, 500, 400 and a failed CSRF check
(Story 1.8, FR-5, FR-6, AD-15).

Every guest view only reads (FR-3): one resolver lookup, then selectors. None
of them touches the session, the messages framework, `request.user` or a CSRF
token, so opening a link sets no cookie and writes no row. The error pages
only read too.
"""

import logging

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.template.loader import render_to_string

from wedding.actors import GuestActor
from wedding.links import resolve_code
from wedding.models import Settings
from wedding.rules.households import household_names, speaks_to_one
from wedding.selectors import (
    footer_contacts,
    household_guest_names,
    programme_prices,
    site_settings,
)

logger = logging.getLogger(__name__)

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


def _not_found(request: HttpRequest) -> HttpResponse:
    """FR-5: G1 with status 404 for a code that resolves to nobody.

    The visitor sees the same page as on `/`; the 404 tells crawlers and link
    scanners that the code is not a page. It is a normal response, so `DEBUG`
    never shows Django's technical 404 with the URL list.
    """
    return render(request, PRIVATE_INVITATION, status=404)


def _guest_context(actor: GuestActor, settings: Settings, current: str = "") -> dict[str, object]:
    """FR-6, FR-8, FR-41: what every guest page under a valid link needs.

    The code for the nav links, the open info page (`current`, empty on the
    front page) and, from the settings row the view has read once, the footer
    contacts and the deadline.
    """
    return {
        "code": actor.guest.code,
        "current": current,
        "contacts": footer_contacts(settings),
        "deadline": settings.rsvp_deadline,
    }


def front_page(request: HttpRequest, code: str) -> HttpResponse:
    """FR-2, FR-3, FR-5, FR-6, FR-7, FR-8, FR-41, UX-DR51: the invitation's front page (G2).

    The code goes through the one resolver (AD-6); nobody gets G1 with 404.
    Three SELECTs in all: the resolver, the household's guest names and the
    settings row. The household line and «deg»/«dere» come from the rules; the
    wedding's date and place are template text (AD-17).
    """
    actor = resolve_code(code)
    if actor is None:
        return _not_found(request)
    names = household_guest_names(actor.household)
    context = _guest_context(actor, site_settings()) | {
        "household_names": household_names(names),
        "speaks_to_one": speaks_to_one(len(names)),
    }
    return render(request, "guests/front_page.html", context)


# FR-8, FR-11: each info page's key (its URL name and current nav word) and
# template. The text lives in the templates (AD-17): Praktisk informasjon
# (FR-10) and Vår historie (UX-DR14) are filled in Story 1.6, Programmet
# (FR-9, UX-DR13) in Story 1.7.
INFO_PAGES = {
    "programme": "guests/programme.html",
    "practical": "guests/practical.html",
    "our_story": "guests/our_story.html",
}


def info_page(request: HttpRequest, code: str, page: str) -> HttpResponse:
    """FR-3, FR-5, FR-6, FR-8, FR-9, FR-11: one of the three info pages (G3) under `/<code>/`.

    `page` is a key of `INFO_PAGES`, set by the route. Two SELECTs: the
    resolver and the settings row; nobody gets G1 with 404. The page's content
    is template text (AD-17): Praktisk informasjon (FR-10) and Vår historie
    (UX-DR14) since Story 1.6, Programmet (UX-DR13) since Story 1.7. The
    programme also gets the three meal prices from the same settings row
    (FR-32, AD-12), so «Godt å vite» never holds a price of its own.
    """
    actor = resolve_code(code)
    if actor is None:
        return _not_found(request)
    settings = site_settings()
    context = _guest_context(actor, settings, current=page)
    if page == "programme":
        context["prices"] = programme_prices(settings)
    return render(request, INFO_PAGES[page], context)


# Error pages (Story 1.8, FR-5, FR-6, AD-15)
#
# config/urls.py sets handler404, handler500 and handler400 to these views, and
# CSRF_FAILURE_VIEW in config/settings.py points to csrf_failure, so a 400,
# 404, 500 or failed CSRF check never shows one of Django's own pages. There is
# no handler403: no guest view raises PermissionDenied. Under a valid link (the first path
# segment resolves) an error page shows the back button to the invitation and
# the footer band with the couple's phones; otherwise it shows nothing personal.

NOT_FOUND = "guests/errors/not_found.html"
SERVER_ERROR = "guests/errors/server_error.html"
BAD_REQUEST = "guests/errors/bad_request.html"
CSRF_FAILURE = "guests/errors/csrf_failure.html"


def _reachable(request: HttpRequest) -> dict[str, object]:
    """FR-5, FR-6, AD-15: the code and the couple's contacts when the path starts with a valid link.

    The first segment of the path goes through the one resolver (AD-6): no query
    when it is not in the code format, one when it is, and one more for the
    settings row when it resolves. `{}` when it resolves to nobody.
    """
    segment = request.path_info.lstrip("/").split("/", 1)[0]
    # The error page must never fail itself (FR-5): any error in the lookup, such
    # as a broken database, gives the impersonal page. It is logged once here,
    # since on a 404 or a CSRF failure nothing else would log it; the LOGGING
    # handlers mask the link code (AD-15).
    try:
        actor = resolve_code(segment)
        if actor is None:
            return {}
        return {"code": actor.guest.code, "contacts": footer_contacts(site_settings())}
    except Exception as error:
        # On a 404 the error is raised while Django handles its Resolver404, whose
        # text holds the path without a leading slash, which the mask cannot
        # find; it says nothing about the lookup, so it is left out of the log.
        error.__suppress_context__ = True
        logger.warning("Error page lookup failed for %s", request.path_info, exc_info=True)
        return {}


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """FR-5, FR-6, AD-15: handler404, for every address that is not a page.

    Without a valid code it is G1 with 404, the same page as `/`, so an unknown
    address tells nothing. Under a valid link it is «Vi finner ikke denne siden»
    with the back button and the phones. The host is already checked by then, so
    it renders with the request.
    """
    context = _reachable(request)
    if not context:
        return _not_found(request)
    return render(request, NOT_FOUND, context, status=404)


def csrf_failure(request: HttpRequest, reason: str = "") -> HttpResponse:
    """FR-5, FR-6, AD-15: CSRF_FAILURE_VIEW, a form sent without a valid CSRF token.

    «Skjemaet ble ikke sendt» with status 403; under a valid link with the back
    button and the phones. The host is already checked, so it renders with the
    request. `reason` is Django's technical cause and is never shown.
    """
    return render(request, CSRF_FAILURE, _reachable(request), status=403)


def server_error(request: HttpRequest) -> HttpResponse:
    """FR-5, FR-6, AD-15: handler500, «Noe gikk galt hos oss».

    Rendered without the request, because a 500 can come from a middleware before
    the host is checked: the link preview then leaves out og:image and nothing
    calls `request.get_host`. Under a valid link it has the back button and the
    phones; if the lookup fails as well, the impersonal page.
    """
    return HttpResponseServerError(render_to_string(SERVER_ERROR, _reachable(request)))


def bad_request(request: HttpRequest, exception: Exception) -> HttpResponse:
    """FR-5, AD-15: handler400, for a request Django cannot trust, such as a bad `Host`.

    Always impersonal: the request itself is untrusted, so the code is never
    looked up, and the page is rendered without the request, because
    `request.get_host` would raise the same `DisallowedHost` again.
    """
    return HttpResponseBadRequest(render_to_string(BAD_REQUEST))
