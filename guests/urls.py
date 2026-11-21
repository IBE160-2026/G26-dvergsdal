"""URLs for the guest side.

The style sample `/stil/` exists only when `APP_ENV` is `local`, so it is never
part of the real site (Story 1.4a). It comes first, because `<str:code>/`
matches any single path segment. The bare address shows the private-invitation
page G1 (Story 1.4b, FR-5). Under `/<code>/` are the invitation's front page
and its three info pages (Story 1.5, AD-6, FR-8, FR-11), with the Norwegian
paths from the architecture memlog; each view resolves the code and shows G1
with 404 for a code that resolves to nobody. The RSVP form (Story 2.1, AD-7)
has step 1 at `/<code>/svar/` and its later steps and check page at
`/<code>/svar/<slug>/` (`dager`, `overnatting`, `maltider`, `allergier`,
`fjelltur`, `se-over`; wedding/rsvp/steps.py); an unknown slug gives «Vi finner
ikke denne siden». `/<code>/personvern/` (Story 7.1) follows.
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
    path("<str:code>/program/", views.info_page, {"page": "programme"}, name="programme"),
    path("<str:code>/praktisk/", views.info_page, {"page": "practical"}, name="practical"),
    path("<str:code>/historie/", views.info_page, {"page": "our_story"}, name="our_story"),
    path("<str:code>/svar/", views.rsvp, name="rsvp"),
    path("<str:code>/svar/<str:slug>/", views.rsvp_step, name="rsvp_step"),
]
