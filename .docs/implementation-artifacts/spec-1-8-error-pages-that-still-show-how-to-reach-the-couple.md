---
title: 'Story 1.8: Error pages that still show how to reach the couple'
type: 'feature'
created: '2026-11-21'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
warnings:
  - oversized
deferred: []
---

<intent-contract>

## Intent

**Problem:** Only an unknown code on a single path segment shows G1. Every other 404 (`/hei/x/`, `/<code>/svar/` until Story 2.1), every 500, the 400 for a bad `Host` header and the CSRF 403 show Django's own pages, which name no way to reach Rikke and Valdemar. A 400 that extends `base.html` would also fail again while rendering, because the link preview calls `request.get_host` (FR-5, FR-6, AD-15; deferred from 1.4b, 1.4c and 1.5).

**Approach:** Add site-wide `handler404`, `handler500`, `handler400` and `CSRF_FAILURE_VIEW` in `guests/views.py`. Each one looks up the first path segment through the one resolver and shows a calm G1-style sheet explaining what happened. When the code resolves, the page adds a back button and the footer band with the couple's phones (`footer_contacts`). Otherwise it shows nothing personal, and an unmatched path with no valid code gets plain G1. Any lookup failure falls back to the impersonal page. G1's markup moves into a shared frame, so no sheet markup is duplicated.

## Boundaries & Constraints

**Always:**
- **Frame:** new `guests/templates/guests/error_page.html` extends `wedding/base.html` and takes over G1's exact markup from `private_invitation.html:14-28`: the icons block `data:,`, `main.column.private-invitation`, the sheet, `h1.private-invitation__heading`, and the gypsophila (`alt=""`, 180×40). It adds blocks `heading` and `message`. After the sheet, still inside `main`, it shows `<p class="error-page__back"><a class="button button--on-green" href="{% url 'guests:front_page' code %}">Tilbake til invitasjonen</a></p>` only `{% if code %}`. After `main` it has `{% include "wedding/components/footer-band.html" %}` (renders nothing without `contacts`). There is no nav bar. `private_invitation.html` becomes a child of the frame, and its rendered HTML must stay byte-identical (`tests/test_private_invitation.py` unchanged and green).
- **Children** in `guests/templates/guests/errors/`, all extending the frame. Text is in the templates (AD-17). Each `<title>` is «<h1> – Invitasjon» (en dash, like the info pages). «Ring/meld» line A = «Går det fortsatt ikke, send oss en melding.» when `contacts`, else B = «Går det fortsatt ikke, ta kontakt med brudeparet direkte.»
  - `not_found.html`: h1 «Vi finner ikke denne siden». p «Lenken kan ha en skrivefeil. Invitasjonen ligger der den var.»
  - `server_error.html`: h1 «Noe gikk galt hos oss». p «Prøv igjen om litt.» + A/B.
  - `csrf_failure.html`: h1 «Skjemaet ble ikke sendt». p «Det skjer når siden har stått åpen lenge, eller når nettleseren ikke tar imot informasjonskapsler. Gå tilbake og prøv igjen.» + A/B.
  - `bad_request.html`: h1 «Siden kunne ikke vises». p «Prøv å åpne lenken på nytt.» + B (never contacts).
- **Views** (`guests/views.py`, new section «Error pages»). A helper `_reachable(request)` takes the first segment of `request.path_info` and calls `resolve_code`, then `footer_contacts(site_settings())`. It returns `{"code": …, "contacts": […]}`, or `{}` when the code is unknown or **any** exception is raised (comment: the error page must never fail, FR-5).
  - `page_not_found(request, exception)`: `{}` → `_not_found(request)` (G1, 404), else `not_found.html` with 404.
  - `csrf_failure(request, reason="")`: `csrf_failure.html` with 403.
  - Both render with `render(request, …)`, since the host is already validated by then.
  - `server_error(request)`: `server_error.html` with 500. `bad_request(request, exception)`: `bad_request.html` with 400 and never looks up the code.
  - Both build the response from `render_to_string(template, context)` **without** `request`, so the preview leaves out `og:image` and nothing calls `request.get_host` (deferred 1.4c).
- `config/urls.py` sets `handler400`, `handler404` and `handler500` as dotted strings. `config/settings.py` sets `CSRF_FAILURE_VIEW = "guests.views.csrf_failure"`. Every docstring and comment names FR-5, FR-6 and AD-15.
- **CSS:** add `.error-page__back` to the existing `.info-page__bottom` rule (`site.css:931`) as a grouped selector. No other new CSS.
- Every error response carries `X-Robots-Tag: noindex` and `Referrer-Policy: same-origin` (existing middleware).

**Never:** no production route that raises, and no `DEBUG`-only branch; no names, date, place or seal on any error page; no nav bar; no du/dere wording; no change to `link-preview.html`, `_not_found`, `front_page` or `info_page`; no handler403 (no guest view raises `PermissionDenied`); no running a browser (the orchestrator runs the MT rows).

## I/O & Edge-Case Matrix

Seeded unless noted; S = `test-sigmund0000000000`, U = `AAAAAAAAAAAAAAAAAAAAAA`. `/<x>/feil/` exists only in the test URLconf.

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| 404, no code | GET `/hei/x/` (0 queries), `/U/svar/` (1 query), also on an empty, migrated DB | 404, G1 byte-identical to `/` | N/A |
| 404, valid code | GET `/S/finnes-ikke/`, `/S/program/x/` (not `svar/`: Story 2.1 routes it) | 404, «Vi finner ikke denne siden», back link `/S/`, footer with both `tel:` rows; 2 queries | N/A |
| Valid code, no phones | both phones blanked; GET `/S/feil/`, `/S/finnes-ikke/` | back link stays; no `<footer`, no `tel:`; the 500 shows line B | N/A |
| 500, valid code | GET `/S/feil/` (view raises `RuntimeError`) | 500, «Noe gikk galt hos oss», back link, footer, line A, no `og:image`, no traceback | N/A |
| 500, unknown code | GET `/U/feil/`, also on an empty DB | 500, same heading, line B, no `<footer`/`tel:`/back link | N/A |
| 500, broken DB | valid S, `Settings` row deleted, GET `/S/` | 500, impersonal 500 page | lookup raises → `{}` |
| 500, lookup raises | `resolve_code` patched to raise `DatabaseError`, GET `/S/feil/` | 500, impersonal 500 page | same |
| CSRF | `Client(enforce_csrf_checks=True)` POST `/S/` / POST `/U/` and `/` | 403, «Skjemaet ble ikke sendt»; with S: back link + footer + A; else B, nothing personal | N/A |
| 400, bad host | GET `/S/` with `HTTP_HOST="evil.example"` | 400, «Siden kunne ikke vises», line B, no footer, no `og:image`, «evil.example» nowhere in the body | never resolves |

</intent-contract>

## Code Map

- `guests/views.py:62-81` -- `PRIVATE_INVITATION`, `private_invitation`, `_not_found` (reuse for the no-code 404). `:84-96` `_guest_context` (pattern, not reused: error pages need no deadline or `current`). `:1-12` module docstring to extend (the error pages also only read).
- `wedding/links.py:34-46` -- `resolve_code` (0 queries when the format is wrong). `wedding/selectors.py:38-66` -- `site_settings`, `footer_contacts` (empty list → no footer).
- `guests/templates/guests/private_invitation.html:1-29` -- G1 markup and comment to move into the frame. `wedding/templates/wedding/base.html:11,14-21` -- title block, preview include, icons block. `wedding/templates/wedding/components/link-preview.html:17-20` -- `og:image` only `{% if request %}`. `wedding/templates/wedding/components/footer-band.html:1-63` -- comment already says 1.8 uses it.
- `guests/templates/guests/info_page.html:36-39` -- back-button markup to mirror. `static/css/site.css:476-505` G1 rules, `:881-903` footer band, `:931-935` `.info-page__bottom`, `:1248-1252` narrow padding (already covers the sheet).
- `config/urls.py:1-26` -- docstring + handlers. `config/settings.py:60-77` -- middleware order (noindex and Security wrap every error response); add `CSRF_FAILURE_VIEW` near `SECURE_REFERRER_POLICY`.
- `tests/test_private_invitation.py:34-75` -- `FORBIDDEN` list and `assert_is_g1` fixture (copy the forbidden list into `tests/helpers.py` if shared). `tests/test_guest_privacy.py:110-141` -- `_assert_private_headers`, existing CSRF test (stays green). `:99-107` `_preview`. `:228-239` render-without-request test. `tests/test_front_page.py:120-150` -- footer row regex and blank-phone pattern. `tests/conftest.py` -- `seeded`, `local_env`, `assert_loads_only_own_host`.
- pytest-django runs with `DEBUG=False`, so the handlers are live. 500 tests need `Client(raise_request_exception=False)` and `@pytest.mark.urls("tests.error_urls")`.
- `docs/manual-test-plan.md:36` -- last row MT-21. `README.md:9` status, `:64` paragraph on links, `:150` `guests/` tree line.
- `DESIGN.md:583-585` (No valid link), `EXPERIENCE.md:240` (states table, «No valid link» row), `ARCHITECTURE-SPINE.md:208` (AD-15 error pages), `.docs/implementation-artifacts/deferred-work.md`.

## Tasks & Acceptance

**Execution:**
- [ ] `guests/templates/guests/error_page.html` -- frame per Boundaries; comment naming FR-5, FR-6 and AD-15, and saying which views use it and why 400/500 render without a request.
- [ ] `guests/templates/guests/private_invitation.html` -- extend the frame, keep its comment, same rendered HTML.
- [ ] `guests/templates/guests/errors/{not_found,server_error,csrf_failure,bad_request}.html` -- text per Boundaries.
- [ ] `guests/views.py` -- `_reachable`, `page_not_found`, `server_error`, `bad_request`, `csrf_failure`; update the module docstring.
- [ ] `config/urls.py`, `config/settings.py` -- handlers, `CSRF_FAILURE_VIEW`, docstring and comment (AD-15).
- [ ] `static/css/site.css` -- grouped selector, G1 section comment mentions the error pages.
- [ ] `tests/error_urls.py` -- test-only URLconf: `<str:code>/feil/` → a view raising `RuntimeError`, then `config.urls.urlpatterns`; re-export `handler400/404/500` from `config.urls`. `tests/error_settings.py` -- `from config.settings import *` (noqa F403) with `ROOT_URLCONF = "tests.error_urls"`, used only for MT-22. Both docstrings say they are never part of the site.
- [ ] `tests/test_error_pages.py` -- every matrix row, plus:
  - each response: status, `_assert_private_headers`, one `<meta name="robots" content="noindex">`, `<title>`, assets only from our own host;
  - impersonal pages contain none of `FORBIDDEN` or any seed name; no «Traceback», «Exception» or «RuntimeError»;
  - error pages with a valid code show the footer `tel:` rows like the front page and no `<nav`;
  - 404/CSRF previews equal `/`'s, and 400/500 previews equal it minus `og:image`;
  - the three handlers and `CSRF_FAILURE_VIEW` resolve to the views (`config.urls.handler404` …);
  - no error page writes (row counts unchanged).
- [ ] `docs/manual-test-plan.md` -- MT-1 (1.8) and MT-22 (Norwegian, «Kjøres av Claude med Playwright mot Edge», date and result cells empty). Server: `uv run manage.py seed_testdata`, `uv run manage.py collectstatic --noinput`, then in PowerShell `$env:DEBUG='false'; $env:ALLOWED_HOSTS='localhost'; uv run manage.py runserver --settings=tests.error_settings`.
  - MT-1 (1.8): README's new «Feilsider» steps (normal settings, `DEBUG=false`). `http://localhost:8000/hei/x/` shows G1, and `/test-sigmund0000000000/finnes-ikke/` shows «Vi finner ikke denne siden» with the phones.
  - MT-22: pages A `http://localhost:8000/hei/x/` (404, G1), B `…/test-sigmund0000000000/finnes-ikke/` (404), C `…/test-sigmund0000000000/feil/` (500), D `…/AAAAAAAAAAAAAAAAAAAAAA/feil/` (500), E `http://127.0.0.1:8000/test-sigmund0000000000/` (400, host not allowed), F = B's code with POST to `…/test-sigmund0000000000/` via `page.route(url, r => r.continue({ method: 'POST' }))` (403).
  - At 360 × 640 and 180 × 320, after `document.fonts.ready`: `response.status()` as listed and `X-Robots-Tag` `noindex`; `document.documentElement.scrollWidth` ≤ `innerWidth`; `h1` text as in Boundaries; `a[href^="tel:"]` count 2 on B, C and F and 0 on A, D and E, each ≥ 44px tall; the back link on B, C and F only; `body.innerText` has none of «Traceback», «Django», «DEBUG», «Exception», «RuntimeError», «settings».
  - On B, `Tab` from the top focuses «Tilbake til invitasjonen» and then the `tel:` links, each with `outline-style` `solid`.
- [ ] `README.md` -- status sentence (1.8). The `:64` paragraph: other wrong addresses also show G1 or an error page with the phones. New short section «Feilsider»: they show only with `DEBUG=false`, which needs `collectstatic` first; exact commands; the two example URLs; 500, 400 and CSRF are covered by `tests/test_error_pages.py`. Add a tree line for `guests/` («feilsidene»).
- [ ] `DESIGN.md:585`, `EXPERIENCE.md:240` -- dated notes (2026-11-21, Story 1.8): error pages reuse G1's sheet, with the wording above, the outlined back button on green and the footer band only under a valid link. Add an «Error page» row to the states table.
- [ ] `ARCHITECTURE-SPINE.md:208` -- dated note: the handlers live in `guests/views.py`. 400 is always impersonal, and 400/500 render without a request (no `get_host`). Any lookup failure falls back. `/admin/` paths get the impersonal pages until Story 3.1.
- [ ] `.docs/implementation-artifacts/deferred-work.md` -- add an entry for Story 3.1: the site-wide handlers give `/admin/` the impersonal guest error pages («ta kontakt med brudeparet»), so decide the couple's own 404/500/CSRF pages there. Add `admin` to `NOT_LINK_CODES`, as already planned.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass, with no assertion in `tests/test_private_invitation.py` or `tests/test_guest_privacy.py` changed.
- Given `DEBUG=False`, when any listed error happens, then no Django default or technical page is ever served (FR-5, FR-6).
- Given the 400 for a bad `Host`, when it renders, then it raises nothing again and shows the impersonal page (deferred 1.4c).
- Given `docs/manual-test-plan.md`, when read, then MT-1 (1.8) and MT-22 hold the steps above with empty result cells.

## Spec Change Log

## Review Triage Log

## Design Notes

- **Why 400 never resolves:** a 400 means the request itself is untrusted (bad host, malformed data), and AD-15 lists only 404, 500 and CSRF for contacts. Rendering without `request` is the simplest way to guarantee no second `DisallowedHost`.
- **Why 500 renders without `request`:** a 500 can come from middleware before host validation. The preview's `og:image` is worthless on an error page anyway.
- **Broad `except Exception` in `_reachable`:** the only goal is that the error page itself never fails. The original error is already logged (masked) by `django.request`.
- **Browser 500 trigger:** `tests/error_settings.py` swaps in a test URLconf with one raising route. The site's own URLconf never gets one. The broken-database fallback is covered by automated tests only, since deleting the settings row would damage the local database.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0
- `git status --short staticfiles` -- expected: no output (ignored)

**Manual checks:**
- MT-1 (1.8) and MT-22 are run afterwards by the orchestrator with Playwright in Edge.
