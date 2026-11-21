"""Settings for the browser check MT-22 only (Story 1.8, FR-5, FR-6, AD-15).

Never part of the site: the site's settings, with the test-only URLconf
tests/error_urls.py, which adds `/<code>/feil/` so a browser can see the 500
page. Used as `uv run manage.py runserver --settings=tests.error_settings`
(docs/manual-test-plan.md, MT-22).
"""

from config.settings import *  # noqa: F403

ROOT_URLCONF = "tests.error_urls"
