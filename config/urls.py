"""Root URL configuration.

Guest pages live under `/<code>/` (AD-6) and the couple's pages under `/admin/`
(AD-10); both arrive from Story 1.4b and 1.5. For now `guests.urls` holds only
the local style sample `/stil/` (Story 1.4a).
"""

from django.urls import include, path

urlpatterns = [
    path("", include("guests.urls")),
]
