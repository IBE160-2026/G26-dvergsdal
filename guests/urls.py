"""URLs for the guest side.

The style sample `/stil/` exists only when `APP_ENV` is `local`, so it is never
part of the real site (Story 1.4a). It comes first, because `<str:code>/`
matches any single path segment. The bare address and every code show the
private-invitation page G1 (Story 1.4b, FR-5); Story 1.5 turns `<str:code>/`
into the invitation's front page for a valid code.
"""

from django.conf import settings
from django.urls import URLPattern, path

from guests import views

app_name = "guests"

urlpatterns: list[URLPattern] = []

if settings.APP_ENV == "local":
    urlpatterns.append(path("stil/", views.style_sample, name="style_sample"))

urlpatterns += [
    path("", views.private_invitation, name="private_invitation"),
    path("<str:code>/", views.front_page, name="front_page"),
]
