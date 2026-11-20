"""Root URL configuration.

Guest pages live under `/<code>/` (AD-6) and the couple's pages under `/admin/`
(AD-10). `guests.urls` holds `/`, the local style sample `/stil/` (Stories 1.4a
and 1.4b), the front page `/<code>/` and the info pages `/<code>/program/`,
`/<code>/praktisk/` and `/<code>/historie/` (Story 1.5). Its `<str:code>/`
matches any single path segment, so
every reserved route goes above the guest include, or it would be read as a
link code. `/robots.txt` is there (Story 1.4c, NFR-4, AD-15): it blocks nothing,
because a crawler must fetch a page to read its `noindex`, and it stops
`/robots.txt` from showing G1. The `admin/` include (the couple's dashboard,
Story 3.1) goes there too.
"""

from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="wedding/robots.txt", content_type="text/plain; charset=utf-8"
        ),
    ),
    path("", include("guests.urls")),
]
