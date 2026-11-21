---
title: 'Story 1.8: Error pages that still show how to reach the couple'
type: 'feature'
created: '2026-11-21'
status: 'done'
baseline_revision: '49f6b4b28e7f631e0a0eb5e7a10b84b017342cc7'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
warnings:
  - oversized
deferred:
  - summary: >-
      Story 2.x (the RSVP form): handler400 treats every 400 as an untrusted host, so a form POST under a valid link that trips RequestDataTooBig, TooManyFieldsSent or a bad multipart body gets the impersonal 400 page with no back button and no phones.
    evidence: |-
      guests.views.bad_request never looks up the code. Unreachable today because no guest view reads a request body; the RSVP form is the first that does. Decide there whether a non-DisallowedHost 400 should use _reachable.
    location: >-
      guests/views.py bad_request
    severity: medium
  - summary: >-
      Story 3.1 (the couple's dashboard): there is no handler403, so a PermissionDenied (the admin raises it for staff without a permission) still gets Django's own bare 403 page.
    evidence: |-
      config/urls.py sets handler400, handler404 and handler500 only; no guest code raises PermissionDenied, so only the admin can reach it. Decide the couple's own 403 together with their 404/500/CSRF pages.
    location: >-
      config/urls.py
    severity: low
  - summary: >-
      MaskLinkCodes only masks a path that starts with `/`, so a link code inside a slash-less path in a log record (for example Django's Resolver404 text `{'path': '<code>/finnes-ikke/'}` in a chained traceback) is logged unmasked.
    evidence: |-
      Found by the implementer during the 1.8 patch: the new `_reachable` warning on a 404 chained the Resolver404 and leaked the code; fixed there with `__suppress_context__`. No other path in the code is known to log a slash-less path, but the filter's `_PATH` regex in config/logging_filters.py cannot catch one. Widen the pattern (or mask Resolver404's `path`) before go-live.
    location: >-
      config/logging_filters.py _PATH
    severity: low
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
- [x] `guests/templates/guests/error_page.html` -- frame per Boundaries; comment naming FR-5, FR-6 and AD-15, and saying which views use it and why 400/500 render without a request.
- [x] `guests/templates/guests/private_invitation.html` -- extend the frame, keep its comment, same rendered HTML.
- [x] `guests/templates/guests/errors/{not_found,server_error,csrf_failure,bad_request}.html` -- text per Boundaries.
- [x] `guests/views.py` -- `_reachable`, `page_not_found`, `server_error`, `bad_request`, `csrf_failure`; update the module docstring.
- [x] `config/urls.py`, `config/settings.py` -- handlers, `CSRF_FAILURE_VIEW`, docstring and comment (AD-15).
- [x] `static/css/site.css` -- grouped selector, G1 section comment mentions the error pages.
- [x] `tests/error_urls.py` -- test-only URLconf: `<str:code>/feil/` → a view raising `RuntimeError`, then `config.urls.urlpatterns`; re-export `handler400/404/500` from `config.urls`. `tests/error_settings.py` -- `from config.settings import *` (noqa F403) with `ROOT_URLCONF = "tests.error_urls"`, used only for MT-22. Both docstrings say they are never part of the site.
- [x] `tests/test_error_pages.py` -- every matrix row, plus:
  - each response: status, `_assert_private_headers`, one `<meta name="robots" content="noindex">`, `<title>`, assets only from our own host;
  - impersonal pages contain none of `FORBIDDEN` or any seed name; no «Traceback», «Exception» or «RuntimeError»;
  - error pages with a valid code show the footer `tel:` rows like the front page and no `<nav`;
  - 404/CSRF previews equal `/`'s, and 400/500 previews equal it minus `og:image`;
  - the three handlers and `CSRF_FAILURE_VIEW` resolve to the views (`config.urls.handler404` …);
  - no error page writes (row counts unchanged).
- [x] `docs/manual-test-plan.md` -- MT-1 (1.8) and MT-22 (Norwegian, «Kjøres av Claude med Playwright mot Edge», date and result cells empty). Server: `uv run manage.py seed_testdata`, `uv run manage.py collectstatic --noinput`, then in PowerShell `$env:DEBUG='false'; $env:ALLOWED_HOSTS='localhost'; uv run manage.py runserver --settings=tests.error_settings`.
  - MT-1 (1.8): README's new «Feilsider» steps (normal settings, `DEBUG=false`). `http://localhost:8000/hei/x/` shows G1, and `/test-sigmund0000000000/finnes-ikke/` shows «Vi finner ikke denne siden» with the phones.
  - MT-22: pages A `http://localhost:8000/hei/x/` (404, G1), B `…/test-sigmund0000000000/finnes-ikke/` (404), C `…/test-sigmund0000000000/feil/` (500), D `…/AAAAAAAAAAAAAAAAAAAAAA/feil/` (500), E `http://127.0.0.1:8000/test-sigmund0000000000/` (400, host not allowed), F = B's code with POST to `…/test-sigmund0000000000/` via `page.route(url, r => r.continue({ method: 'POST' }))` (403).
  - At 360 × 640 and 180 × 320, after `document.fonts.ready`: `response.status()` as listed and `X-Robots-Tag` `noindex`; `document.documentElement.scrollWidth` ≤ `innerWidth`; `h1` text as in Boundaries; `a[href^="tel:"]` count 2 on B, C and F and 0 on A, D and E, each ≥ 44px tall; the back link on B, C and F only; `body.innerText` has none of «Traceback», «Django», «DEBUG», «Exception», «RuntimeError», «settings».
  - On B, `Tab` from the top focuses «Tilbake til invitasjonen» and then the `tel:` links, each with `outline-style` `solid`.
- [x] `README.md` -- status sentence (1.8). The `:64` paragraph: other wrong addresses also show G1 or an error page with the phones. New short section «Feilsider»: they show only with `DEBUG=false`, which needs `collectstatic` first; exact commands; the two example URLs; 500, 400 and CSRF are covered by `tests/test_error_pages.py`. Add a tree line for `guests/` («feilsidene»).
- [x] `DESIGN.md:585`, `EXPERIENCE.md:240` -- dated notes (2026-11-21, Story 1.8): error pages reuse G1's sheet, with the wording above, the outlined back button on green and the footer band only under a valid link. Add an «Error page» row to the states table.
- [x] `ARCHITECTURE-SPINE.md:208` -- dated note: the handlers live in `guests/views.py`. 400 is always impersonal, and 400/500 render without a request (no `get_host`). Any lookup failure falls back. `/admin/` paths get the impersonal pages until Story 3.1.
- [x] `.docs/implementation-artifacts/deferred-work.md` -- add an entry for Story 3.1: the site-wide handlers give `/admin/` the impersonal guest error pages («ta kontakt med brudeparet»), so decide the couple's own 404/500/CSRF pages there. Add `admin` to `NOT_LINK_CODES`, as already planned.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass, with no assertion in `tests/test_private_invitation.py` or `tests/test_guest_privacy.py` changed.
- Given `DEBUG=False`, when any listed error happens, then no Django default or technical page is ever served (FR-5, FR-6).
- Given the 400 for a bad `Host`, when it renders, then it raises nothing again and shows the impersonal page (deferred 1.4c).
- Given `docs/manual-test-plan.md`, when read, then MT-1 (1.8) and MT-22 hold the steps above with empty result cells.

## Spec Change Log

## Review Triage Log

### 2026-11-21 — Review pass
- verdicts: 27 findings — high 0, medium 2, low 18, false 7, maybe-false 0
- findings:
  - `[low]` `[reject]` A 500 with the phones under a valid code is only shown on a test-only route (`tests/error_urls.py`), never on a real site route (intent) — no real guest view can be made to raise without changing production code; the handler is the same one, and MT-22 C showed it in Edge with 2 `tel:` links.
  - `[low]` `[reject]` The CSRF failure is tested with a POST to the front page, which has no form, not with a real form flow (intent) — no guest form exists until Epic 2; the POST exercises `CSRF_FAILURE_VIEW` exactly as an expired form would, and Epic 2's form tests will meet it again.
  - `[low]` `[reject]` The database failure is simulated (patched `resolve_code` raising `DatabaseError`, deleted Settings row), never a real broken connection (intent) — a lost connection raises the same `DatabaseError` subclasses that `_reachable` catches; a real fault would add setup but not a new code path.
  - `[low]` `[patch]` The header/preview/no-writes test has no row for a 404 at `/<UNKNOWN>/svar/` or a CSRF failure at `/<UNKNOWN>/` (intent) — both rows added to the `ERRORS` table in `tests/test_error_pages.py`.
  - `[false]` `[reject]` The 400 and 500 pages leave out `og:image`, a subset of the 1.4c preview (intent) — deliberate: the 1.4c deferred entry asks for exactly this so `request.get_host` is never called again; the tests pin it.
  - `[low]` `[reject]` Code masking in the 500's log line is claimed but not tested in this diff (intent) — `MaskLinkCodes` sits on every LOGGING handler (Story 1.4c, with its own tests), and the 500 is logged through `django.request` like the 404 those tests cover.
  - `[false]` `[reject]` The diff goes beyond `/<code>/`, also covering 400, every other address and `/admin/` (intent) — the 1.4b, 1.4c and 1.5 deferred entries assign these to 1.8; `/admin/` is recorded for Story 3.1 in deferred-work.
  - `[false]` `[reject]` A valid-code error page shows no contact details when both phones are blank (intent) — the footer band has hidden blank phones since Story 1.5 (`footer_contacts`); there is nothing to show, and the page then says «ta kontakt med brudeparet direkte».
  - `[false]` `[reject]` MT-1 (1.8) and MT-22 have no results (intent) — run by Claude with Playwright in Edge 157: all OK, recorded in the test plan.
  - `[false]` `[reject]` MT-22 runs on the test URLconf, not the real settings (intent) — only the raising `/<code>/feil/` route differs; MT-1 (1.8) ran A and B on the real settings with the same results.
  - `[false]` `[reject]` The spec file is not in the reviewed diff (intent) — the spec is committed separately at the baseline and finalized by the orchestrator.
  - `[low]` `[patch]` The DESIGN.md and EXPERIENCE.md notes for the error pages name no approver, unlike G1's «approved (Rikke, 2026-11-15)» (intent) — the notes now say the wording is Claude's proposal awaiting Rikke's approval; the PR and issues.md ask her.
  - `[low]` `[patch]` The CSRF page's line A/B choice under a valid link with blank phones is never tested (verification-gap) — `test_valid_link_without_phones_keeps_the_back_button` also POSTs without a token and asserts the CSRF heading, the back link, no footer and line B.
  - `[low]` `[patch]` The docstring of `test_a_csrf_failure_says_noindex_and_same_origin` says the 403 is made by the middleware, not a view (verification-gap) — docstring corrected to `guests.views.csrf_failure`; no assertion changed.
  - `[low]` `[defer]` No `handler403`, so a `PermissionDenied` still gets Django's page despite «no visitor ever sees one of Django's own pages» (blind) — no guest code raises `PermissionDenied`; the admin (Story 3.1) is the first place it can, so the 3.1 deferred entry now names 403; the docstrings are narrowed to 400, 404, 500 and CSRF.
  - `[medium]` `[patch]` `_reachable` catches every exception and logs nothing, so on a 404 or CSRF 403 a broken database or a bug in `footer_contacts` is silently dropped (blind) — it now logs a warning with `exc_info` through the masked handlers before falling back; the fallback test asserts the record.
  - `[medium]` `[defer]` `handler400` treats every 400 as a bad host, so a future RSVP POST that trips `RequestDataTooBig` or `TooManyFieldsSent` under a valid link gets no back button and no phones (blind) — unreachable today (no guest view reads a request body); before 1.8 such a request got Django's bare 400. Deferred to Epic 2's RSVP form, which adds the first body.
  - `[low]` `[reject]` The `{# djlint:off #}` block leaves the frame unlinted and awkwardly formatted (blind) — the spec requires G1's rendered HTML to stay byte-identical, which djLint's formatting breaks; `paper-filters.html` uses the same exclusion, and the template comment explains it.
  - `[low]` `[patch]` The forbidden-word list now exists twice (`tests/helpers.IMPERSONAL_FORBIDDEN` and `FORBIDDEN` in `test_private_invitation.py`) and can drift (blind) — `test_private_invitation.py` now uses the helpers list; same values, no assertion changed.
  - `[low]` `[reject]` The new tests import private helpers from `test_guest_privacy.py` and Django's private `_get_failure_view` (blind) — both work and are exercised; moving the helpers would rewrite a module the spec keeps stable, and `_get_failure_view` checks Django's real resolution of the setting.
  - `[low]` `[patch]` Nothing proves the 500 path never calls `request.get_host` (blind) — a test calls `server_error` with a request whose `get_host` raises `DisallowedHost` and gets the 500 page.
  - `[low]` `[patch]` MT-1 (1.8) and MT-22 are not run, MT-22's «B sin kode» is unclear, and its forbidden list has «settings» but `TECHNICAL` does not (blind) — both rows run and recorded; MT-22 F reworded to the URL; «settings» added to `TECHNICAL`.
  - `[false]` `[reject]` Sprint status, spec status and the session log are not updated (blind) — the finalize and log steps do that.
  - `[low]` `[patch]` The CSRF page with blank phones is not tested (blind) — same as the verification-gap row above.
  - `[low]` `[patch]` README «Feilsider» tells PowerShell users to close the window, and only shows the two 404s by hand (blind) — the reset command `Remove-Item Env:DEBUG, Env:ALLOWED_HOSTS` is given; the 500/400/CSRF recipe stays in MT-22, which the section already links.
  - `[low]` `[defer]` No `handler403` (edge-case) — same as the blind row above; deferred to Story 3.1.
  - `[low]` `[reject]` If the 500 came from a shared include (`footer-band.html`), `server_error` raises again rendering it (edge-case) — the impersonal page extends the same `base.html`, so the guard would only help for a broken footer include, which every guest-page test renders; the extra try adds a branch for a state no test or story produces.

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

## Auto Run Result

Status: done

**Summary:** Every 404, 500, 400 and failed CSRF check now shows a calm G1-style sheet instead of Django's own page. Each view in `guests/views.py` looks up the first path segment through the one resolver. Under a valid code the page adds «Tilbake til invitasjonen» and the footer band with the couple's phones (`footer_contacts`). Without one, it shows nothing personal, and an unmatched 404 is G1 byte for byte. If the lookup fails, it falls back to the impersonal page and logs one masked warning. The 400 page is always impersonal. The 400 and 500 pages render without the request, so nothing calls `request.get_host` again. G1's markup moved into the shared frame `error_page.html`, and G1 renders byte-identical. This closes the three deferred items from 1.4b, 1.4c and 1.5. The Norwegian wording is Claude's proposal and is waiting for Rikke's approval.

**Files changed:**
- `guests/views.py`, `config/urls.py`, `config/settings.py`: `_reachable` and the four error views, plus `handler400/404/500` and `CSRF_FAILURE_VIEW`.
- `guests/templates/guests/error_page.html` (new), `guests/templates/guests/private_invitation.html`, `guests/templates/guests/errors/*.html` (new): the shared frame and the four pages.
- `static/css/site.css`: `.error-page__back` is grouped with `.info-page__bottom`.
- `tests/test_error_pages.py`, `tests/error_urls.py`, `tests/error_settings.py` (new), `tests/helpers.py`, `tests/test_private_invitation.py`, `tests/test_guest_privacy.py`: the test matrix, a test-only route that raises a 500, and the shared forbidden-word list.
- `README.md` (new «Feilsider» section), `docs/manual-test-plan.md` (MT-1 (1.8), MT-22), DESIGN.md, EXPERIENCE.md, ARCHITECTURE-SPINE AD-15 (dated notes), `deferred-work.md`.

**Review:** 27 findings: high 0, medium 2, low 18, false 7.
- 10 patched. The two that mattered: the lookup fallback now logs a warning instead of dropping the error silently, and the no-phones CSRF case and the `get_host`-free 500 are now tested.
- 3 deferred: a 400 from a form body (Epic 2), handler403 (Story 3.1), and slash-less paths in the log mask, which the implementer found while patching.
- 14 rejected, with reasons in the triage log.

**Follow-up review recommendation:** false. No high was patched. The medium fix (a logged fallback) is pinned by a `caplog` test, which also asserts that the code is not in the log. The browser checks were run again after patching with the same results.

**Verification:** `uv run pytest` gives 666 passed, and ruff, ruff format and djlint are clean. Claude ran MT-1 (1.8) and MT-22 with Playwright in Edge 157, with `DEBUG=false`, before and after the patches:
- the six pages at 360 and 180 px return the right status and `noindex`;
- no page scrolls sideways;
- the `tel:` links are 44 or 56 px tall, and only under a valid code;
- there is no technical text;
- keyboard focus moves back link → phones, with a solid outline.

**Residual risks:**
- The Norwegian wording awaits Rikke's approval.
- `/admin/` gets the guest error pages until Story 3.1.
- A non-host 400 under a valid link shows no phones (Epic 2).
- MT-22 needs the test-only settings to trigger a 500.
