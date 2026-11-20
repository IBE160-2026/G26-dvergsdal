---
title: 'Story 1.4c: Guest pages stay private: headers, link previews and logs'
type: 'feature'
created: '2026-11-20'
status: 'done'
baseline_revision: 'ec1b8bb03ec0881b777e444a79a53dc8238770a0'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
warnings:
  - multiple-goals
  - oversized
deferred:
  - summary: >-
      MT-10, a real Messenger/SMS link preview, needs the site on a public address.
    evidence: |-
      Previews are built by the apps' servers, which cannot reach 127.0.0.1. Recorded in deferred-work.md for the hosting work (no story yet).
    location: >-
      docs/manual-test-plan.md
    severity: low
  - summary: >-
      If SECURE_SSL_REDIRECT is turned on, SecurityMiddleware answers the redirect before noindex_middleware runs, so that redirect has no X-Robots-Tag.
    evidence: |-
      SECURE_SSL_REDIRECT is off today; recorded in deferred-work.md for the hosting work together with SECURE_PROXY_SSL_HEADER and production access logs.
    location: >-
      config/settings.py
    severity: low
  - summary: >-
      A DisallowedHost 400 page that extends base.html would call request.get_host in the link preview and fail again.
    evidence: |-
      No custom 400 page exists yet; Story 1.8 adds the error pages. Recorded in deferred-work.md.
    location: >-
      wedding/templates/wedding/components/link-preview.html
    severity: low
---

<intent-contract>

## Intent

**Problem:** Guest responses send no `noindex`, the link preview is whatever an app guesses, `/robots.txt` falls through to the catch-all `<str:code>/` and renders G1, and every G1 404 writes the link code to the log («Not Found: /<code>/») (FR-4, NFR-4, AD-15).

**Approach:** One middleware adds `X-Robots-Tag: noindex` to every response, `Referrer-Policy: same-origin` is set explicitly, the base template gets the robots meta tag and one fixed set of Open Graph tags with a preview image made from Rikke's watercolour, `/robots.txt` is routed above the catch-all, and a logging filter on every handler masks the first path segment of request paths.

## Boundaries & Constraints

**Always:**
- `X-Robots-Tag: noindex` on **every** response (guest pages, redirects, robots.txt, static files): middleware placed directly after `SecurityMiddleware`, before WhiteNoise. `SECURE_REFERRER_POLICY = "same-origin"` set explicitly with an AD-15 comment (never `no-referrer`: it breaks CSRF).
- `<meta name="robots" content="noindex">` and the preview tags live in `wedding/base.html` `<head>` outside any block, so every page (G1, later the front page, info pages, admin) has identical tags. No `og:url`, no `<link rel="canonical">`, no `og:site_name`, no twitter tags: nothing that varies by code or names the couple.
- Preview values (fixed): `og:type` `website`, `og:locale` `nb_NO`, `og:title` `Invitasjon`, `og:description` `En personlig invitasjon. Åpne lenken for å se den.`, `og:image` = `{{ request.scheme }}://{{ request.get_host }}{% static 'img/forhandsvisning.jpg' %}` (own host, so nothing comes from another site; `request.scheme` honours `SECURE_PROXY_SSL_HEADER` later), `og:image:width` `1000`, `og:image:height` `525`, `og:image:alt` `Akvarell av et gammelt tun med et lite klokketårn, et våningshus og furutrær.`
- Preview image `static/img/forhandsvisning.jpg`: `ImageOps.fit` centre crop of `.docs/planning-artifacts/ux/egne-bilder/04-Illustration.jpg` (1695×928, checked: no text or signature) to 1000×525 (1.91:1, ≥ 600×315 so Messenger shows the large card), progressive JPEG at the script's `JPEG_QUALITY`, no metadata. Planner trial: ≈ 77 KB (within the 100 KB file budget; 1200×630 was 105 KB). Not part of the front-page budget: the page never loads it.
- `/robots.txt`: `path("robots.txt", TemplateView.as_view(template_name="wedding/robots.txt", content_type="text/plain; charset=utf-8"))` **above** the guest include in `config/urls.py`. Body exactly:
  ```
  # Every page says noindex in a meta tag and an X-Robots-Tag header (AD-15).
  # Search engines must be allowed to fetch a page to read that, so nothing is blocked.
  User-agent: *
  Disallow:
  ```
- Logging: `config/logging_filters.py` holds a pure `mask_link_codes(message: str) -> str` and `MaskLinkCodes(logging.Filter)`, which formats the record (`record.getMessage()`), masks it, sets `record.msg` to the result and `record.args = ()`, and returns `True`. A request path is a `/` at the start of the message or after whitespace, `"`, `'` or `(`; its first segment (`[^/\s?#"']+`) becomes `[code]` unless it is in `NOT_LINK_CODES = frozenset({"static", "stil", "robots.txt"})` (docstring: Story 3.1 adds `admin`; over-masking is safe, under-masking is not). Masks any first segment, not only 22-character ones: a mistyped code is nearly a real one.
- `LOGGING` in `config/settings.py` (explicit, no `mail_admins`, since no mail is ever sent and its body would carry the request): `version 1`, `disable_existing_loggers: False`; filters `require_debug_true` (`django.utils.log.RequireDebugTrue`) and `mask_link_codes` (`"()": "config.logging_filters.MaskLinkCodes"`); formatter `django.server` copied from Django's `DEFAULT_LOGGING`; handlers `console` (`StreamHandler`, filters `require_debug_true` + `mask_link_codes`) and `django.server` (`StreamHandler`, formatter `django.server`, filter `mask_link_codes`); loggers `django` → `console`, level `INFO`; `django.server` → `django.server`, level `INFO`, `propagate: False`. Every handler carries `mask_link_codes`.
- Docstrings, template comments and settings comments name FR-4, NFR-4, AD-15.

**Never:** no `nofollow`/`noarchive` beyond the planned `noindex`; no `Disallow: /` (it would hide the noindex from crawlers); no new env var or site-URL setting; no external URL, script or font; no change to G1's visible content; no seal, couple initials, date or place in any preview tag or the preview image name. Not in this story: `sensitive_post_parameters` (guest forms, Epic 2), production access logs and `SECURE_PROXY_SSL_HEADER` (no hosting story yet), `handler404` for multi-segment paths (1.8), the `admin/` route (3.1), running a browser.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Bare address | GET `/`, empty migrated DB | 200; `X-Robots-Tag: noindex`, `Referrer-Policy: same-origin`; one robots meta; the preview tags above; `<title>Invitasjon</title>`; every `://` in the HTML is `http://testserver/` | N/A |
| Two codes | seed loaded; GET `/<code of guest in household 1>/`, `/<code in household 2>/`, `/AAAAAAAAAAAAAAAAAAAAAA/` | title and every `og:` tag identical to `/` and to each other; no seed guest name, couple contact name, `R & V`, `2028`, `Hardingasete` in them | N/A |
| Redirect | GET `/hei` | 301 (APPEND_SLASH) still carries both headers | N/A |
| robots.txt | GET `/robots.txt` | 200, `text/plain; charset=utf-8`, exact body, not the G1 template, zero DB queries, `X-Robots-Tag` set | N/A |
| 404 log | GET `/<seeded code>/` | `django.request` line reads `Not Found: /[code]/`; code absent | N/A |
| CSRF log | POST `/<seeded code>/` with `Client(enforce_csrf_checks=True)` | 403; `django.security.csrf` line reads `Forbidden (…): /[code]/` | N/A |
| Server log | `django.server` record `'"%s" %s %s'` with `GET /<code>/svar/?x=1 HTTP/1.1`, 404, 0 | `"GET /[code]/svar/?x=1 HTTP/1.1" 404 0` | N/A |
| Fixed paths | `/`, `/static/css/site.css`, `/stil/`, `/robots.txt`, `HTTP/1.1` | unchanged | N/A |

</intent-contract>

## Code Map

- `config/settings.py:57-66` `MIDDLEWARE` (Security at :58, WhiteNoise at :59); add `SECURE_REFERRER_POLICY` and `LOGGING` sections (file ends at :140, `MAILERS` at :136). Django's `SecurityMiddleware` already sends `same-origin` by default; the explicit setting makes it traceable.
- `config/urls.py` -- docstring already says reserved routes go above `include("guests.urls")`; add `robots.txt` there and update the docstring (admin still 3.1).
- `guests/urls.py`, `guests/views.py` -- unchanged; `front_page` renders G1 with 404 for every code until 1.5, so the preview comparison runs on those responses and keeps passing when 1.5 returns 200 for valid codes.
- `wedding/templates/wedding/base.html:9-20` -- `<head>`; title block default `Invitasjon` at :10; `icons` block :12-18 (G1 overrides only `icons`). Add the robots meta and `{% include "wedding/components/link-preview.html" %}` after the stylesheet, outside every block; header comment :3-4 names stories.
- `tools/prepare_images.py:66-74` `PHOTOS`, `:141-143` the photo loop, `ImageOps` already imported -- add a `PREVIEW` constant and one `ImageOps.fit` call; update the module docstring.
- `static/img/README.md` table -- add the `forhandsvisning.jpg` row (Norwegian).
- `tests/test_images.py:46-61` `TARGETS` (add `"forhandsvisning.jpg": 1000`), `:63` `FRONT_PAGE` (do not add), `_jpeg_frame` returns marker and width (height is `payload[1:3]`).
- `tests/test_design_system.py:510-517` renders `base.html` without a request and asserts `"://" not in html`; `:676` same assert on `/stil/`. `tests/test_private_invitation.py:73` `_assert_is_g1` asserts `"://" not in html`. All three must become "every `://` is followed by the own host".
- `tests/conftest.py` -- shared fixtures; `production_urls` reloads URLconfs.
- `docs/manual-test-plan.md` -- last id MT-7; rows in Norwegian.
- `.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md:201-209` AD-15. `.docs/implementation-artifacts/deferred-work.md:17-19` the admin/robots entry.

## Tasks & Acceptance

**Execution:**
- [x] `tools/prepare_images.py` -- add the preview target (fit 1000×525 from `04-Illustration.jpg`), docstring names FR-4; run `uvx --with pillow==13.0.0 python -I tools/prepare_images.py` and commit `static/img/forhandsvisning.jpg`; add its row to `static/img/README.md` -- FR-4, UX-DR4.
- [x] `wedding/templates/wedding/components/link-preview.html`, `wedding/templates/wedding/base.html` -- the include with the fixed tags and a comment naming FR-4/AD-15; base gets the robots meta and the include -- FR-4, AD-15.
- [x] `config/middleware.py` -- `noindex_middleware(get_response)` setting `X-Robots-Tag: noindex` on every response; `config/logging_filters.py` -- `mask_link_codes`, `NOT_LINK_CODES`, `MaskLinkCodes` -- AD-15.
- [x] `config/settings.py` -- middleware after Security; `SECURE_REFERRER_POLICY`; `LOGGING` as in Boundaries -- AD-15, NFR-4.
- [x] `wedding/templates/wedding/robots.txt`, `config/urls.py` -- the route above the guest include and its docstring -- NFR-4, deferred-work (1.4b).
- [x] `tests/test_images.py` -- `forhandsvisning.jpg` in `TARGETS` (1000) and its JPEG height is 525.
- [x] `tests/conftest.py` -- fixture returning a checker that every `://` in an HTML string is `http://testserver/` and no `src`/`href` starts with `//`; use it in the three places listed in the Code Map (render `base.html` with `RequestFactory().get("/")`).
- [x] `tests/test_guest_privacy.py` -- every matrix row except the log rows: headers on `/`, unknown code, seeded code, `/stil/`, `/hei`, `/robots.txt`; middleware order (before WhiteNoise); `SECURE_REFERRER_POLICY == "same-origin"`; title and `og:` tags identical across codes with no names; `og:image` file found by `django.contrib.staticfiles.finders`; `rel="noreferrer"` on every `<a href="http…">` in every template under `wedding/templates` and `guests/templates`, with the checker proved on one good and one bad sample.
- [x] `tests/test_log_masking.py` -- `mask_link_codes` on the log rows and fixed paths; settings: every `LOGGING` handler has `mask_link_codes`, no `AdminEmailHandler`; end-to-end: with `settings.DEBUG = True`, swap each handler's stream on the `django` and `django.server` loggers for a `StringIO` (`handler.setStream`, restored after), make the 404 and CSRF requests and emit the server record, then assert the seeded code is absent and `/[code]/` present.
- [x] `docs/manual-test-plan.md` -- MT-8 (Playwright, Edge): open `http://127.0.0.1:8000/`, `/hei/`, `/stil/` and record every request: all go to `127.0.0.1:8000`; the document responses carry `X-Robots-Tag: noindex` and `Referrer-Policy: same-origin`; `/robots.txt` shows the four lines; `og:image` URL answers 200 `image/jpeg`. MT-9: start `uv run manage.py runserver` after `seed_testdata`, open one printed test link: the terminal shows `"GET /[code]/ HTTP/1.1" 404` and `Not Found: /[code]/`, never the code. MT-10 (Rikke, once the site is on a public address): paste a test link into Messenger and an SMS: the watercolour, «Invitasjon» and the description, no names. Result cells empty.
- [x] `README.md` -- status line (1.4c: headers, previews, masked logs), folder tree `config/` line (mellomvare og loggfilter), a sentence that the terminal shows `/[code]/` instead of link codes; `ARCHITECTURE-SPINE.md` AD-15 -- dated 2026-11-20 note: robots.txt allows crawling so `noindex` can be read, `og:image` absolute from the request host (needs `SECURE_PROXY_SSL_HEADER` when hosted behind TLS); `deferred-work.md` -- mark the robots part of the admin/robots entry done in 1.4c, admin stays with 3.1.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given `uvx --with pillow==13.0.0 python -I tools/prepare_images.py` is run again, when `git status --short static/img` is checked, then it prints nothing.
- Given any guest response including G1, when its HTML and headers are inspected by a test, then it has `noindex` as meta and `X-Robots-Tag`, `Referrer-Policy: same-origin`, a title with no names, and loads nothing from other sites.
- Given two different seeded codes, when their responses' title and Open Graph tags are compared by a test, then they are identical and contain no names.
- Given a request to a guest page that Django logs, when the configured handlers' output is read by a test, then it holds `/[code]/` and never the code.

## Spec Change Log

## Review Triage Log

### 2026-11-20 — Review pass
- verdicts: 38 findings — high 0, medium 14, low 19, false 5, maybe-false 0
- findings:
  - `[false]` `[reject]` The two-code preview comparison holds by construction because every code shows G1 (intent-alignment) — the test fetches seeded codes, so it compares real guest pages once Story 1.5 returns 200; nothing to change now.
  - `[low]` `[patch]` Nothing enforces that the page `<title>` (inside a block) is the same for every code (intent-alignment) — the two-code test now also compares `<title>`.
  - `[false]` `[reject]` "Loads nothing from other sites" does not follow the stylesheet (intent-alignment) — `test_every_url_points_to_a_local_file` (1.4a) already checks every `url()` in site.css; MT-8 in Edge saw only 127.0.0.1.
  - `[low]` `[patch]` The noreferrer check has nothing to check and misses template-variable hrefs (intent-alignment) — `<a>` with `{{` in href must carry `rel` with noreferrer.
  - `[low]` `[patch]` 403/500 bodies and headers are not checked (intent-alignment) — a CSRF 403 header test was added; the 500/400 bodies belong to Story 1.8.
  - `[medium]` `[patch]` Loggers outside the `django` tree reach `logging.lastResort` unmasked (intent-alignment) — a root logger with a masked WARNING+ handler.
  - `[low]` `[defer]` What Messenger/SMS really show (MT-10) needs a public host (intent-alignment) — deferred to the hosting work.
  - `[false]` `[reject]` Tasks unticked, logs empty, sprint-status still backlog (blind) — that is the finalize step.
  - `[low]` `[patch]` Work moved out of the story (production access logs, SECURE_PROXY_SSL_HEADER, MT-10) is not in deferred-work.md (blind) — entries added.
  - `[medium]` `[patch]` With DEBUG off nothing from Django is logged anywhere (blind) — new masked WARNING+ handler that does not depend on DEBUG.
  - `[medium]` `[patch]` Tracebacks (`exc_info`, `stack_info`) are not masked (blind) — the filter now masks exception and stack text.
  - `[medium]` `[patch]` Full URLs and `key=/<code>/` are not masked, e.g. Django's CSRF Referer message (blind) — the first segment after `scheme://host` and after `=` is masked.
  - `[low]` `[patch]` Absolute file paths are masked too, contrary to the docstring (blind) — docstring now says so.
  - `[low]` `[patch]` `NOT_LINK_CODES` is only compared with itself (blind) — the test derives the top-level routes from the URLconf, so 3.1's `admin/` fails until added.
  - `[low]` `[patch]` The Referrer-Policy test cannot fail (blind) — the test now checks the setting is written in settings.py.
  - `[low]` `[patch]` The https scheme of og:image is untested (blind) — test with `secure=True`; the own-host checker accepts the request's scheme.
  - `[low]` `[patch]` og:image becomes `:///static/…` without a request (blind) — the og:image tag sits in `{% if request %}`, with a test.
  - `[medium]` `[patch]` Static files under runserver carry no X-Robots-Tag (blind; also seen by Claude in the Playwright MT-8 run) — `whitenoise.runserver_nostatic` added.
  - `[low]` `[patch]` CSRF 403 and 500 headers are not tested (blind) — same as the 403 row above.
  - `[false]` `[reject]` MT-8 and MT-9 were never run (blind) — run by Claude with Playwright in Edge after the review was launched, and recorded.
  - `[false]` `[reject]` No session log for 1.4c (blind) — the orchestrator writes it before the PR merges.
  - `[medium]` `[patch]` Absolute URLs and query values leak the code (verification-gap, other) — same root cause as the full-URL row.
  - `[medium]` `[patch]` `require_debug_true` before `mask_link_codes` leaves the propagated record unmasked (verification-gap, other) — mask filter first on every handler.
  - `[medium]` `[patch]` In production nothing is logged (verification-gap, other) — same as the DEBUG-off row.
  - `[medium]` `[patch]` `//<code>/` is not masked (edge-case) — the path pattern accepts several leading slashes.
  - `[medium]` `[patch]` Absolute-form request lines and paths after `=` (edge-case) — same as the full-URL row.
  - `[medium]` `[patch]` exc_info / stack_info unmasked (edge-case) — same as the traceback row.
  - `[low]` `[patch]` `record.getMessage()` raising escapes into the request (edge-case) — caught; the record passes unchanged.
  - `[medium]` `[patch]` Non-django loggers emit WARNING+ through lastResort without the mask (edge-case) — same as the root-logger row.
  - `[low]` `[defer]` A SECURE_SSL_REDIRECT redirect would skip `noindex_middleware` (edge-case) — SSL redirect is not enabled; recorded for the hosting work.
  - `[low]` `[patch]` og:image without a request in context (edge-case) — same as the `{% if request %}` row.
  - `[low]` `[defer]` A DisallowedHost 400 page extending base.html would call `request.get_host` again (edge-case) — deferred to Story 1.8.
  - `[low]` `[patch]` The protocol-relative check misses srcset, action, content, poster and CSS `url(//` (edge-case) — regex extended.
  - `[low]` `[patch]` An unnamed `{% endblock %}` would hide tags from the outside-every-block test (edge-case) — both forms accepted.
  - `[low]` `[patch]` Template-variable external hrefs skip the noreferrer check (edge-case) — same as the noreferrer row above.
  - `[low]` `[patch]` `ImageOps.fit` silently upscales a smaller replacement illustration (edge-case) — the script asserts the source is at least 1000×525.
  - `[medium]` `[patch]` Claim: a request to a guest page never logs its code; `//<code>/` does (edge-case, claim) — same as the double-slash row.
  - `[medium]` `[patch]` Claim: a filter on every handler masks every path; non-django loggers reach lastResort (edge-case, claim) — same as the root-logger row.

## Design Notes

- **Allow crawling, say noindex.** A crawler blocked by robots.txt never sees `noindex` and may still list the bare URL; link previewers (Meta, Slack) ignore robots.txt anyway (research [87]–[89]). So robots.txt blocks nothing and exists to explain that and to stop `/robots.txt` rendering G1.
- **One preview everywhere.** The tags sit outside every block, so no page can override them per guest; the page `<title>` may differ by page (EXPERIENCE.md › Page titles) but never by guest.
- **Image host from the request.** Open Graph needs an absolute `og:image`; the request host is already checked by `ALLOWED_HOSTS`, so no `SITE_URL` setting (NFR-8: no `.env` needed).
- **Handler-level filter.** Records from `django.request`, `django.security.csrf` and `django.server` all pass a handler, so a filter on every handler covers future loggers too; logger-level filters would miss child loggers.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0
- `uvx --with pillow==13.0.0 python -I tools/prepare_images.py && git status --short static/img` -- expected: only `forhandsvisning.jpg` new on the first run, no output on a rerun

**Manual checks:**
- MT-8 and MT-9 are run afterwards by the orchestrator with Playwright in Edge; MT-10 waits for hosting.

## Auto Run Result

Status: done

**Summary:** Guest pages stay private. Every response carries `X-Robots-Tag: noindex` (middleware before WhiteNoise, and `runserver_nostatic` so dev static files get it too) and `Referrer-Policy: same-origin`. `base.html` holds the robots meta tag and one fixed Open Graph preview (watercolour crop `forhandsvisning.jpg`) outside every block. `/robots.txt` is routed above the catch-all and blocks nothing. A logging filter masks link codes (first path segment, after `scheme://host` and `=`, in tracebacks and stack text) on every handler, including a new DEBUG-independent WARNING+ handler on the root logger.

**Files changed:**
- `config/middleware.py`, `config/logging_filters.py`, `config/settings.py`, `config/urls.py` — noindex header, log masking, LOGGING, Referrer-Policy, robots route.
- `wedding/templates/wedding/base.html`, `wedding/templates/wedding/components/link-preview.html`, `wedding/templates/wedding/robots.txt` — meta tags, preview, robots.
- `tools/prepare_images.py`, `static/img/forhandsvisning.jpg`, `static/img/README.md` — the preview image.
- `tests/test_guest_privacy.py`, `tests/test_log_masking.py`, `tests/conftest.py` and adjusted 1.4a/1.4b tests — headers, previews, robots, masking end to end.
- `.gitattributes` (robots.txt stays LF), `README.md`, `ARCHITECTURE-SPINE.md` (AD-15 note), `deferred-work.md`, `docs/manual-test-plan.md` (MT-8, MT-9, MT-10).

**Review:** 30 rows patched (18 distinct fixes), 3 rows deferred, 5 rejected with reasons in the triage log.

**Follow-up review recommendation:** false. No high was patched. Several medium entries were patched (masking gaps, production logging, runserver static header), all covered by new tests that ran and by the Playwright MT-8/MT-9 re-run, so no unverified risk can be named.

**Verification:** `uv run pytest` 492 passed; ruff and djlint clean; image script rerun leaves `static/img` unchanged; MT-8 and MT-9 run by Claude with Playwright in Edge (before and after the patches); 1.4b's MT-5/MT-6 re-run still pass.

**Residual risks:** production access logs, `SECURE_PROXY_SSL_HEADER` and `SECURE_SSL_REDIRECT` wait for the hosting work; MT-10 (real Messenger/SMS preview) needs a public address; a DisallowedHost 400 page (Story 1.8) must not call `request.get_host` in the preview.
