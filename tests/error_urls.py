"""A test-only URLconf with one route that raises (Story 1.8, FR-5, FR-6, AD-15).

Never part of the site: `config.urls` is the site's URLconf and has no route
that raises. This one adds `/<code>/feil/`, whose view raises `RuntimeError`,
in front of the site's own routes, so the tests (`@pytest.mark.urls`) and the
browser check MT-22 (through tests/error_settings.py) can see the 500 page with
and without a valid code. The error handlers are the site's own, re-exported
from `config.urls`.
"""

from django.http import HttpRequest, HttpResponse
from django.urls import path

from config.urls import handler400, handler404, handler500
from config.urls import urlpatterns as site_urlpatterns

__all__ = ["handler400", "handler404", "handler500", "urlpatterns"]


def raise_error(request: HttpRequest, code: str) -> HttpResponse:
    """AD-15: a view that always fails, to trigger handler500."""
    raise RuntimeError("Story 1.8: a deliberate error for the 500 page")


urlpatterns = [path("<str:code>/feil/", raise_error), *site_urlpatterns]
