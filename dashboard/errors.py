"""The couple's own error pages under `/admin/` (Story 3.1; FR-5 spirit, UX-DR36, AD-15).

`config/error_handlers.py` sends 403, 404, 500 and a failed CSRF check here when
the path is `/admin/…`, and to `guests/views.py` otherwise, so a guest page is
never shown to the couple and the couple's frame is never shown to a guest. Each
page keeps its status, says what happened in a few words and offers a way back:
«Til oversikten» for a logged-in admin, «Til innlogging» otherwise. The nav shows
only for a logged-in admin, and never on a 500. A lookup that fails falls back to
the plain frame, so an error page never fails itself. They never name the
couple's contact details: the couple read these pages themselves.
"""

import logging

from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache

from dashboard.access import is_admin
from dashboard.navigation import frame

logger = logging.getLogger(__name__)

FORBIDDEN = "dashboard/errors/forbidden.html"
NOT_FOUND = "dashboard/errors/not_found.html"
SERVER_ERROR = "dashboard/errors/server_error.html"
CSRF_FAILURE = "dashboard/errors/csrf_failure.html"


def _frame(request: HttpRequest) -> dict[str, object]:
    """UX-DR36: the nav and the right way back for a logged-in admin, else `{}`.

    The helper's read-only line is for the working pages only, so an error page leaves it out.

    Reading the user touches the session, which can fail with a broken database;
    that is logged once (the handlers mask link codes) and the plain frame is used.
    """
    try:
        if is_admin(request.user):
            return {**frame(request), "read_only": False, "logged_in": True}
    except Exception:
        logger.warning("Admin error page lookup failed for %s", request.path_info, exc_info=True)
    return {}


@never_cache
def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """UX-DR36: handler404 under `/admin/`: «Vi finner ikke denne siden»."""
    return render(request, NOT_FOUND, _frame(request), status=404)


@never_cache
def permission_denied(request: HttpRequest, exception: Exception) -> HttpResponse:
    """UX-DR36: handler403 under `/admin/`: «Du har ikke tilgang til denne siden»."""
    return render(request, FORBIDDEN, _frame(request), status=403)


@never_cache
def csrf_failure(request: HttpRequest, reason: str = "") -> HttpResponse:
    """UX-DR36: CSRF_FAILURE_VIEW under `/admin/`: «Skjemaet ble ikke sendt».

    `reason` is Django's technical cause and is never shown.
    """
    return render(request, CSRF_FAILURE, _frame(request), status=403)


@never_cache
def server_error(request: HttpRequest) -> HttpResponse:
    """UX-DR36, AD-15: handler500 under `/admin/`: «Noe gikk galt».

    Rendered without the request, because a 500 can come from a middleware before
    the host is checked, and so never with the nav: the way back is the login.
    """
    return HttpResponseServerError(render_to_string(SERVER_ERROR))
