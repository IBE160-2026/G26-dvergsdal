"""Project middleware (Story 1.4c).

`noindex_middleware` keeps every page out of search engines (FR-4, NFR-4,
AD-15). It sits directly after `SecurityMiddleware` and before WhiteNoise, so
static files, redirects and `/robots.txt` carry the header too. Under
`runserver`, `whitenoise.runserver_nostatic` in INSTALLED_APPS stops Django's
own static handler, which would answer before any middleware runs.
"""

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse


def noindex_middleware(
    get_response: Callable[[HttpRequest], HttpResponse],
) -> Callable[[HttpRequest], HttpResponse]:
    """AD-15: `X-Robots-Tag: noindex` on every response.

    The header repeats the robots meta tag in `wedding/base.html` for responses
    that are not HTML (images, redirects, robots.txt). Only `noindex`: crawlers
    may still fetch the pages, since a crawler that may not fetch a page never
    reads its `noindex`.
    """

    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)
        response["X-Robots-Tag"] = "noindex"
        return response

    return middleware
