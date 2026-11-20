---
title: 'Story 1.4c: Guest pages stay private: headers, link previews and logs'
type: 'feature'
created: '2026-11-20'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
warnings:
  - multiple-goals
  - oversized
deferred: []
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
- [ ] `tools/prepare_images.py` -- add the preview target (fit 1000×525 from `04-Illustration.jpg`), docstring names FR-4; run `uvx --with pillow==13.0.0 python -I tools/prepare_images.py` and commit `static/img/forhandsvisning.jpg`; add its row to `static/img/README.md` -- FR-4, UX-DR4.
- [ ] `wedding/templates/wedding/components/link-preview.html`, `wedding/templates/wedding/base.html` -- the include with the fixed tags and a comment naming FR-4/AD-15; base gets the robots meta and the include -- FR-4, AD-15.
- [ ] `config/middleware.py` -- `noindex_middleware(get_response)` setting `X-Robots-Tag: noindex` on every response; `config/logging_filters.py` -- `mask_link_codes`, `NOT_LINK_CODES`, `MaskLinkCodes` -- AD-15.
- [ ] `config/settings.py` -- middleware after Security; `SECURE_REFERRER_POLICY`; `LOGGING` as in Boundaries -- AD-15, NFR-4.
- [ ] `wedding/templates/wedding/robots.txt`, `config/urls.py` -- the route above the guest include and its docstring -- NFR-4, deferred-work (1.4b).
- [ ] `tests/test_images.py` -- `forhandsvisning.jpg` in `TARGETS` (1000) and its JPEG height is 525.
- [ ] `tests/conftest.py` -- fixture returning a checker that every `://` in an HTML string is `http://testserver/` and no `src`/`href` starts with `//`; use it in the three places listed in the Code Map (render `base.html` with `RequestFactory().get("/")`).
- [ ] `tests/test_guest_privacy.py` -- every matrix row except the log rows: headers on `/`, unknown code, seeded code, `/stil/`, `/hei`, `/robots.txt`; middleware order (before WhiteNoise); `SECURE_REFERRER_POLICY == "same-origin"`; title and `og:` tags identical across codes with no names; `og:image` file found by `django.contrib.staticfiles.finders`; `rel="noreferrer"` on every `<a href="http…">` in every template under `wedding/templates` and `guests/templates`, with the checker proved on one good and one bad sample.
- [ ] `tests/test_log_masking.py` -- `mask_link_codes` on the log rows and fixed paths; settings: every `LOGGING` handler has `mask_link_codes`, no `AdminEmailHandler`; end-to-end: with `settings.DEBUG = True`, swap each handler's stream on the `django` and `django.server` loggers for a `StringIO` (`handler.setStream`, restored after), make the 404 and CSRF requests and emit the server record, then assert the seeded code is absent and `/[code]/` present.
- [ ] `docs/manual-test-plan.md` -- MT-8 (Playwright, Edge): open `http://127.0.0.1:8000/`, `/hei/`, `/stil/` and record every request: all go to `127.0.0.1:8000`; the document responses carry `X-Robots-Tag: noindex` and `Referrer-Policy: same-origin`; `/robots.txt` shows the four lines; `og:image` URL answers 200 `image/jpeg`. MT-9: start `uv run manage.py runserver` after `seed_testdata`, open one printed test link: the terminal shows `"GET /[code]/ HTTP/1.1" 404` and `Not Found: /[code]/`, never the code. MT-10 (Rikke, once the site is on a public address): paste a test link into Messenger and an SMS: the watercolour, «Invitasjon» and the description, no names. Result cells empty.
- [ ] `README.md` -- status line (1.4c: headers, previews, masked logs), folder tree `config/` line (mellomvare og loggfilter), a sentence that the terminal shows `/[code]/` instead of link codes; `ARCHITECTURE-SPINE.md` AD-15 -- dated 2026-11-20 note: robots.txt allows crawling so `noindex` can be read, `og:image` absolute from the request host (needs `SECURE_PROXY_SSL_HEADER` when hosted behind TLS); `deferred-work.md` -- mark the robots part of the admin/robots entry done in 1.4c, admin stays with 3.1.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given `uvx --with pillow==13.0.0 python -I tools/prepare_images.py` is run again, when `git status --short static/img` is checked, then it prints nothing.
- Given any guest response including G1, when its HTML and headers are inspected by a test, then it has `noindex` as meta and `X-Robots-Tag`, `Referrer-Policy: same-origin`, a title with no names, and loads nothing from other sites.
- Given two different seeded codes, when their responses' title and Open Graph tags are compared by a test, then they are identical and contain no names.
- Given a request to a guest page that Django logs, when the configured handlers' output is read by a test, then it holds `/[code]/` and never the code.

## Spec Change Log

## Review Triage Log

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
