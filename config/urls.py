"""Root URL configuration.

Guest pages live under `/<code>/` (AD-6) and the couple's pages under `/admin/`
(AD-10). `guests.urls` holds `/`, the local style sample `/stil/` (Stories 1.4a
and 1.4b), the front page `/<code>/` and the info pages `/<code>/program/`,
`/<code>/praktisk/` and `/<code>/historie/` (Story 1.5), and the RSVP form
`/<code>/svar/` with its steps `/<code>/svar/<slug>/` (Story 2.1). Its
`<str:code>/` matches any single path segment, so every reserved route goes
above the guest include, or it would be read as a link code. `/robots.txt`
is there (Story 1.4c, NFR-4, AD-15): it blocks nothing, because a crawler
must fetch a page to read its `noindex`, and it stops `/robots.txt` from
showing G1. The `admin/` include (the couple's dashboard, Story 3.1) goes
there too.

The error handlers are guests/views.py's (Story 1.8, FR-5, FR-6, AD-15), so a
400, 404, 500 or failed CSRF check never shows one of Django's own pages (there
is no handler403; Story 3.1 decides it): a 404 without a valid code is G1,
and a 404 or 500 under a valid link shows the couple's phones. A 400 is always
impersonal. The CSRF failure page is set in config/settings.py.
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

# FR-5, FR-6, AD-15: site-wide error pages (Story 1.8).
handler400 = "guests.views.bad_request"
handler404 = "guests.views.page_not_found"
handler500 = "guests.views.server_error"
