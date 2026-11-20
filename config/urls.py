"""Root URL configuration.

Guest pages live under `/<code>/` (AD-6) and the couple's pages under `/admin/`
(AD-10). `guests.urls` holds `/`, `/<code>/` and the local style sample `/stil/`
(Stories 1.4a and 1.4b). Its `<str:code>/` matches any single path segment, so
the `admin/` include (the couple's dashboard, Story 3.1) must be added above the
guest include, or `/admin/` would be read as a link code.
"""

from django.urls import include, path

urlpatterns = [
    path("", include("guests.urls")),
]
