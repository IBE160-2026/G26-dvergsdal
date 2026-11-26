"""URLs under `/admin/` (Story 3.1, 3.4; FR-46, FR-57, FR-58, AD-10, AD-13, UX-DR34).

`config/urls.py` includes this above the guests' `<str:code>/`, so `/admin/…`
is never read as a link code. The last pattern catches every other admin path
and answers the couple's own 404 for a logged-in admin (and the login redirect
for anyone else), so `/admin/program/` never falls through to a guest page.
"""

from django.urls import path
from django.views.generic import RedirectView

from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("tall/<slug:slug>/", views.count_page, name="count"),
    path("gjester/", views.guests_page, name="guests"),
    path("logg-inn/", views.login_view, name="login"),
    path("logg-ut/", views.logout_view, name="logout"),
    # No slash: the catch-all would otherwise take these before APPEND_SLASH can act.
    path(
        "logg-inn",
        RedirectView.as_view(pattern_name="dashboard:login", query_string=True, permanent=True),
    ),
    path(
        "logg-ut",
        RedirectView.as_view(pattern_name="dashboard:logout", query_string=True, permanent=True),
    ),
    path("<path:rest>", views.unknown, name="unknown"),
]
