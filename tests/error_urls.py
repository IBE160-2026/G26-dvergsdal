"""A test-only URLconf with one route that raises (Story 1.8, FR-5, FR-6, AD-15).

Never part of the site: `config.urls` is the site's URLconf and has no route
that raises. This one adds `/<code>/feil/`, whose view raises `RuntimeError`,
in front of the site's own routes, so the tests (`@pytest.mark.urls`) and the
browser check MT-22 (through tests/error_settings.py) can see the 500 page with
and without a valid code. Story 3.1 adds `/admin/feil/` (a `RuntimeError`),
`/admin/forbudt/` and `/<code>/forbudt/` (a `PermissionDenied`), for the
couple's 500 and 403 and the guests' 403. The error handlers are the site's own,
re-exported from `config.urls`.
"""

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.urls import path

from config.urls import handler400, handler403, handler404, handler500
from config.urls import urlpatterns as site_urlpatterns

__all__ = ["handler400", "handler403", "handler404", "handler500", "urlpatterns"]


def raise_error(request: HttpRequest, code: str) -> HttpResponse:
    """AD-15: a view that always fails, to trigger handler500."""
    raise RuntimeError("Story 1.8: a deliberate error for the 500 page")


def raise_error_without_code(request: HttpRequest) -> HttpResponse:
    """UX-DR36: the same failure under `/admin/`, where there is no code."""
    raise RuntimeError("Story 3.1: a deliberate error for the couple's 500 page")


def raise_forbidden(request: HttpRequest, code: str = "") -> HttpResponse:
    """UX-DR36: a view that always raises `PermissionDenied`, to trigger handler403."""
    raise PermissionDenied


urlpatterns = [
    path("admin/feil/", raise_error_without_code),
    path("admin/forbudt/", raise_forbidden),
    path("<str:code>/forbudt/", raise_forbidden),
    path("<str:code>/feil/", raise_error),
    *site_urlpatterns,
]
