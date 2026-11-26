"""URLs under `/admin/` (Story 3.1; FR-46, AD-10, AD-13, UX-DR34).

`config/urls.py` includes this above the guests' `<str:code>/`, so `/admin/…`
is never read as a link code. The last pattern catches every other admin path
and answers the couple's own 404 for a logged-in admin (and the login redirect
for anyone else), so `/admin/program/` never falls through to a guest page.
"""

from django.urls import path

from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("logg-inn/", views.login_view, name="login"),
    path("logg-ut/", views.logout_view, name="logout"),
    path("<path:rest>", views.unknown, name="unknown"),
]
