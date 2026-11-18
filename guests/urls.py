"""URLs for the guest side.

The style sample `/stil/` exists only when `APP_ENV` is `local`, so it is never
part of the real site (Story 1.4a). Guest pages under `/<code>/` arrive with
Story 1.4b and 1.5.
"""

from django.conf import settings
from django.urls import URLPattern, path

from guests import views

app_name = "guests"

urlpatterns: list[URLPattern] = []

if settings.APP_ENV == "local":
    urlpatterns.append(path("stil/", views.style_sample, name="style_sample"))
