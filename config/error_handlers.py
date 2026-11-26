"""The site-wide error handlers, one per status, choosing the couple's or the guests' page.

Django allows one handler per status for the whole site. `guests` and
`dashboard` never import each other (tests/test_architecture_imports.py), so
neither can own the branching; this module imports both. A path that is `/admin`
or starts with `/admin/` gets the couple's own page from `dashboard/errors.py`;
every other path keeps the guest pages from `guests/views.py` (Story 1.8, FR-5,
FR-6, AD-15). A 400 is always the impersonal page, since the request itself is
untrusted. A `PermissionDenied` outside `/admin/` gets an impersonal 403 page
(Story 3.1, UX-DR36). The CSRF failure view is set in `config/settings.py`.
"""

from django.http import HttpRequest, HttpResponse

from dashboard import errors as admin_errors
from guests import views as guest_views

bad_request = guest_views.bad_request


def _under_admin(request: HttpRequest) -> bool:
    """UX-DR36: whether the request is for `/admin` or a page under it."""
    path = getattr(request, "path_info", "")
    return path == "/admin" or path.startswith("/admin/")


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """FR-5, UX-DR36: handler404."""
    handler = admin_errors if _under_admin(request) else guest_views
    return handler.page_not_found(request, exception)


def permission_denied(request: HttpRequest, exception: Exception) -> HttpResponse:
    """UX-DR36: handler403; the guests' page is the impersonal `forbidden`."""
    if _under_admin(request):
        return admin_errors.permission_denied(request, exception)
    return guest_views.forbidden(request, exception)


def server_error(request: HttpRequest) -> HttpResponse:
    """FR-5, UX-DR36, AD-15: handler500."""
    handler = admin_errors if _under_admin(request) else guest_views
    return handler.server_error(request)


def csrf_failure(request: HttpRequest, reason: str = "") -> HttpResponse:
    """FR-5, UX-DR36, UX-DR52: CSRF_FAILURE_VIEW."""
    handler = admin_errors if _under_admin(request) else guest_views
    return handler.csrf_failure(request, reason)
