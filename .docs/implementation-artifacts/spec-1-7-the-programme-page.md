---
title: 'Story 1.7: The programme page'
type: 'feature'
created: '2026-11-20'
status: 'done'
baseline_revision: 'ad21cc14004c43282a8636c2844abc3c1ea19b3f'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/info-program.html'
warnings:
  - oversized
deferred: []
---

<intent-contract>

## Intent

**Problem:** `/<code>/program/` shows only the info-page frame from Story 1.5, so a guest cannot see the weekend day by day, what costs money or what to bring before answering (FR-9 page, UX-DR13).

**Approach:** Fill `programme.html` with the approved mockup `info-program.html` as template text (AD-17): «Hopp til» Fredag · Lørdag · Søndag, the voluntary line, and one info sheet per day with its date line, a CSS-only alternating timeline (`ol`, Rikke's icons, `<time>`, short name) and «Godt å vite». The three meal prices come from `Settings` through a new selector, never from the template. Placeholder times until Story 7.4.

## Boundaries & Constraints

**Always:**
- **Order in `info_content`:** `<nav class="jump-links" aria-label="Hopp til">` with ONE `ul`: Fredag `#fredag`, Lørdag `#lordag`, Søndag `#sondag`; the 2nd and 3rd `li` start with `<span class="jump-links__dot" aria-hidden="true">·</span>` (same markup and classes as `practical.html:17-45`, no new jump-link CSS). Then `<p class="voluntary-line">Alt i programmet er frivillig. Bli med på det dere har lyst til.</p>`. Then three `<section class="paper-sheet info-sheet programme-day" id="…" tabindex="-1" aria-labelledby="…-overskrift">`, each: `<h2 id="…-overskrift">` (Fredag / Lørdag / Søndag) → `<p class="programme-day__date">` (26. mai / 27. mai `<span aria-hidden="true">·</span>` bryllupsdagen / 28. mai) → `<ol class="programme-timeline">` → `<div class="good-to-know"><h3>Godt å vite</h3><ul>…</ul></div>`.
- **Each event** `li`: `<img class="programme-timeline__icon" src="{% static 'img/ikoner/…' %}" alt="" width="56" height="56">`, `<time class="programme-timeline__time" datetime="HH:MM">HH:MM</time>`, `<span class="programme-timeline__name">…</span>`. Events, icons and placeholder times exactly `info-program.html:145,154,163`: Fri 10:00 Fjelltur (01-fjelltur), 15:00 Hyttene er klare (02-hytte), 17:00 Middag (04-middag), 19:00 Rebus (03-rebus), 21:00 Badstue, stamp og mingling (05-stamp); Sat 08:00 Yoga (07-yoga), 09:00 Frokost (06-frokost), 13:30 Vi drar til kirka (08-bil), 14:00 Vielsen (09-ringer), 16:00 Lunsj utenfor kirka (10-lunsj), 19:00 Middag og fest (11-fest); Sun 09:00 Frokost (06-frokost), 12:00 Hyttene skal være tomme (12-avreise). Friday's icons load eagerly; Saturday's and Sunday's `loading="lazy"`.
- **«Godt å vite»** text word for word `info-program.html:146,155,164`, `<b>` as `<strong>`, each «[x]» replaced by `{{ prices.friday_dinner }}`, `{{ prices.saturday_breakfast }}`, `{{ prices.sunday_breakfast }}` (rendered «340 kr.» with the seed). No digit price anywhere in the template.
- **Prices:** new selector `programme_prices(settings=None) -> dict[str, int]` in `wedding/selectors.py` (keys `friday_dinner`, `saturday_breakfast`, `sunday_breakfast`; same shape as `footer_contacts`). `info_page` reads `site_settings()` once and passes it to `_guest_context` and, for `page == "programme"` only, to `programme_prices`; still 2 SELECTs on every info page, 3 on the front page.
- **CSS** (`static/css/site.css`, new section «Programme» after «Story sheet»; values from DESIGN.md `programme-timeline`, `programme-icon`, `good-to-know`, `voluntary-line`, mockup `info-program.html:73-91` where DESIGN has none): voluntary line `margin: 6px 10px 0`, centred, italic, `line-height: 1.35`. Date line `margin: -4px 0 6px`, italic. Timeline `position: relative; margin: 8px 0 6px; padding: 0; list-style: none`; `::before` 1px line at `left: 50%`, `top: 6px; bottom: 6px`, `rgba(var(--rgb-ink), 0.45)`; `li` `width: 50%`, odd right-aligned with `padding: 0 18px 0 0`, `:nth-child(even)` `margin-left: 50%`, left-aligned, `padding: 0 0 0 18px`; `li + li { margin-top: -36px }`; `li::after` 6px ink circle at `top: 69px`, `right: -3px` (even: `left: -3px`); icon `display: block`, 56px, `margin: 0 0 4px auto` (even: `0 auto 4px 0`); time `display: block`, `var(--font-size-small)`, `line-height: 1.3`, `letter-spacing: 0.04em`, `lining-nums tabular-nums`; name `display: block`, italic, `line-height: 1.25`. Good-to-know `margin: 14px 0 0; padding-top: 10px; border-top: 1px solid rgba(var(--rgb-ink), 0.25)`; `h3` `margin: 0 0 4px`, italic, `var(--font-size-body)`/`var(--line-height-body)`; `ul` `margin: 0; padding-left: 20px`; `li` `margin: 0 0 4px`. Every programme selector must outrank `.info-sheet p` / `.info-sheet ul` (0,1,1): prefix with `.programme-day`. Inside the existing `@media (max-width: 259.98px)` block: one-sided timeline: line `left: 3px`, every `li` (odd and even) `width: auto; margin-left: 0; padding: 0 0 0 18px; text-align: left`, `li + li { margin-top: var(--space-3) }`, icons `margin: 0 auto 4px 0`, dots `left: 0; right: auto`. Inside `@media (forced-colors: active)`: line and dots `forced-color-adjust: none; background: CanvasText`. No `scroll-margin`; no new `rgb` triplet (use `--rgb-ink`).
- Docstrings, template comments and CSS section comments name FR-9, UX-DR13, AD-17 (and AD-12/FR-32 for prices, NFR-5/UX-DR30/UX-DR53 for narrow and forced colours).

**Never:** no text from `ux/innhold/programmet-og-praktisk.md` and no real times (Story 7.4); no du/dere logic (the decided voluntary line says «dere», EXPERIENCE.md:115; same text for every household); no sign-up or form (FR-9: information only); no new price field or migration; no thousands formatting or money helper (Story 2.3 shows the first amount ≥ 1000); no new image files; no JavaScript; no `scroll-margin`; no change to the jump-link CSS or its 22.5em breakpoint; no running a browser.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Programme | seed; GET `/test-sigmund0000000000/program/` | 200, 2 SELECTs; nav after `h1`, voluntary line after nav, then 3 sections in order; each section's text = mockup section's with «[x]» → seed price (340 / 260 / 260); img set = the 12 icons used (06-frokost twice) | N/A |
| Prices from Settings | `update_settings(SYSTEM, …)` with dinner 415, Sat 255, Sun 265 | «Middagen betales selv: 415 kr.», «Frokosten betales selv: 255 kr.» in `#lordag`, «… 265 kr.» in `#sondag` | N/A |
| One invited | GET `/test-synne000000000000/program/` | `main` text identical to Sigmund's | N/A |
| Unknown code | `/AAAAAAAAAAAAAAAAAAAAAA/program/`, `/hei/program/` | 404 G1, unchanged (`tests/test_info_pages.py:78`) | N/A |

</intent-contract>

## Code Map

- `guests/templates/guests/programme.html:1-7` -- frame-only template; comment says «arrive with Story 1.7». Fill `info_content`, add `{% load static %}`.
- `guests/templates/guests/practical.html:17-45` -- jump-link markup to copy; `:46-50` section attributes (`tabindex="-1"`, `aria-labelledby="…-overskrift"`).
- `guests/templates/guests/info_page.html:2-19` -- frame comment; `h1 id="sidetittel"`. No change needed beyond comment accuracy.
- `guests/views.py:1-11` module docstring; `:77-90` `_guest_context` (reads `site_settings()` itself today); `:93-109` `front_page`; `:112-120` `INFO_PAGES` comment («Programmet holds only the frame until Story 1.7»); `:123-134` `info_page`.
- `wedding/selectors.py` -- `site_settings` and `footer_contacts(settings=None)` (pattern for `programme_prices`). `wedding/models.py:99-102` -- `price_friday_dinner`, `price_saturday_breakfast`, `price_sunday_breakfast` exist (no `price_*` added). `wedding/migrations/0003_settings_row.py` sets them to 0; `wedding/fixtures/seed.toml:33-36` 340 / 260 / 260.
- `wedding/services/settings.py:36-60` -- `SettingsValues`, `update_settings` (use with `SYSTEM` from `wedding/actors.py` in tests, as `tests/test_settings_service.py:17-48` does).
- `static/css/site.css:1-17` header comment («The programme arrives in 1.7»); `:933-991` jump links (reuse, do not touch); `:993-1026` info sheet; `:1028-1072` story sheet (insert «Programme» after it); `:1112-1124` the 259.98px block; `:1132-1166` forced colours; `:81` `--rgb-ink`; `:155-156` `--font-size-small`. `body` already has `overflow-wrap: break-word`.
- `static/img/ikoner/` -- 12 icons, 112×112 (shown at 56); listed in `static/img/README.md:24-26`.
- `tests/test_practical_and_story_pages.py:84-117` -- helpers `_attrs`, `_main`, `_sections`, `_get` and the mockup-parsing pattern to mirror (do not import from a test module; copy or move shared helpers to `tests/helpers.py`).
- `tests/test_info_pages.py:1-12` -- docstring says the programme's content arrives in 1.7.
- `tests/test_front_page.py:163` -- no-write test already covers `program/` with 2 queries.
- `tests/test_design_system.py:38-45` query constants (`NARROW_QUERY`, `FORCED_COLORS_QUERY`); `:94-160` helpers `_css`, `_block`, `_declarations`, `_bodies`; `ROOT`, `DESIGN`; `:707-727` pattern for "values follow DESIGN"; the `--rgb-ink` triplet-count assertion must keep passing.
- `docs/manual-test-plan.md` -- last ids MT-1 (1.6), MT-18; MT-16 row is the template for the new jump-link row.
- `README.md:9` -- status line («Programmet har bare rammen til story 1.7»).
- `DESIGN.md:566` (programme item 2, «on one line»); `.docs/implementation-artifacts/deferred-work.md`.

## Tasks & Acceptance

**Execution:**
- [x] `wedding/selectors.py` -- add `programme_prices(settings: Settings | None = None)`; docstring FR-9, FR-32, AD-12 (one source with the RSVP form).
- [x] `guests/views.py` -- `_guest_context(actor, settings, current="")` takes the read row; `front_page` and `info_page` call `site_settings()` once; `info_page` adds `prices` for `programme`; update module docstring, `INFO_PAGES` comment and docstrings (Programmet filled in 1.7).
- [x] `guests/templates/guests/programme.html` -- content per Boundaries; comment names FR-9, UX-DR13, AD-17, that prices come from Settings and that Story 7.4 replaces the placeholder times.
- [x] `static/css/site.css` -- «Programme» section, narrow-width and forced-colour additions, header comment -- UX-DR13, UX-DR30, UX-DR53, NFR-5.
- [x] `tests/test_programme_page.py` -- every matrix row; jump links (one list, hrefs, hidden dots, first `li` without dot, between `h1` and first section); voluntary line position and text; section attributes, `h2` and date line (Saturday dot `aria-hidden`); per day the event names, icons, `alt=""`, 56×56 and `<time datetime>` equal to the Boundaries list and times ascending; `h3` «Godt å vite» after the `ol`; section text vs mockup with «[x]» substituted; eager/lazy rule; template source: every « kr» follows `}}` and no `[x]`; `programme_prices` returns the row's three ints without a query when given the row.
- [x] `tests/test_info_pages.py` -- docstring: programme content tested in `test_programme_page.py`.
- [x] `tests/test_design_system.py` -- timeline, icon, good-to-know and voluntary-line values vs DESIGN; one-sided rules inside `NARROW_QUERY`; CanvasText line and dots inside `FORCED_COLORS_QUERY`; no `scroll-margin`.
- [x] `docs/manual-test-plan.md` -- rows below (Norwegian, «Kjøres av Claude med Playwright mot Edge», `reducedMotion: 'reduce'`, measure after `document.fonts.ready` and every `main img:not([loading="lazy"])` `complete`; date and result cells empty). Server: `uv run manage.py seed_testdata`, `uv run manage.py runserver`; G = `http://127.0.0.1:8000/test-sigmund0000000000/program/`.
  - MT-1 (1.7): README steps, then G shows «Hopp til» Fredag · Lørdag · Søndag, the voluntary line, three day sheets with icons and «Godt å vite» with «340 kr» and «260 kr».
  - MT-19 (jump links): at 360 × 640, for each `nav[aria-label="Hopp til"] a` click from the top → `location.hash` = href, `document.activeElement.id` = target id, `#<id> h2` top ≥ `.nav-bar` bottom and < `innerHeight`. From the top `Tab` to `a[href="#lordag"]` (`outline-style` `solid`, `outline-color` `rgb(245, 238, 223)`) and `Enter` → same checks. New context `hasTouch: true`: `locator('a[href="#sondag"]').tap()` → same checks. At 360 × 380 click `a[href="#sondag"]` → `#sondag h2` top within 0…`innerHeight`. At 360 × 640 the three links share one `top` (one line); at 320 × 568 and 180 × 320 every `.jump-links__dot` `display` `none` and the three `li` tops increase.
  - MT-20 (timeline and widths): line x = `ol.getBoundingClientRect().left + parseFloat(getComputedStyle(ol, '::before').left)` for each `.programme-timeline`. At 360 × 640, 320 × 568 and 260 × 640: odd `li` right ≤ line x + 1 and even `li` left ≥ line x − 1 (alternating). At 259 × 640 and 180 × 320: for every `li`, its `img`, `time` and `.programme-timeline__name` left > line x (one-sided), and each `li` top ≥ the previous `li` bottom (no overlap). At all five sizes plus 360 × 640: `document.documentElement.scrollWidth` ≤ `innerWidth`, every `.programme-timeline__name` `scrollWidth` ≤ `clientWidth`, every `li` right ≤ its section's right.
  - MT-21 (screen readers, forced colours): `locator('nav[aria-label="Hopp til"]').ariaSnapshot()` and `locator('#lordag .programme-day__date').ariaSnapshot()` contain no «·»; `locator('.programme-timeline').first().ariaSnapshot()` lists 5 list items and no `img`; every `.programme-timeline img` has `alt=""`. With `page.emulateMedia({ forcedColors: 'active' })`: `getComputedStyle(ol, '::before').backgroundColor` and `getComputedStyle(li, '::after').backgroundColor` equal `getComputedStyle(ol).color`.
- [x] `README.md:9` -- status: Programmet has the day sheets with timeline and «Godt å vite»; prices from the settings; placeholder times until 7.4 (1.7).
- [x] `DESIGN.md:566` -- dated note (2026-11-20, Story 1.7): one line at 360px; below 22.5em the three links stack without dots like every jump-link list (EXPERIENCE › Jump links); timeline line and dots in CanvasText under forced colours.
- [x] `.docs/implementation-artifacts/deferred-work.md` -- two entries: Story 7.4: the programme's placeholder times are plain («10:00», as approved), so the «[…]» placeholder test does not catch them; replace them from the content draft and decide du/dere for «dere» lines. Story 2.3: when the form picks a kroner display (thousands, e.g. «1 450 kr»), use it for the programme's prices too.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given G for a seeded link, when fetched, then it has no `<script`, loads only its own host, and one `h1` «Programmet» with «Program» as the current nav word (FR-11).
- Given the couple changes a meal price in Settings, when G is fetched again, then «Godt å vite» shows the new price (FR-9, FR-32).
- Given G in Edge, when a jump link is followed by click, keyboard or tap, then focus is on its day sheet and its heading is below the sticky bar (MT-19); and below about 260px every event is right of the line with no horizontal scroll (MT-20).
- Given `docs/manual-test-plan.md`, when read, then MT-1 (1.7) and MT-19 to MT-21 hold the steps above with empty result cells.

## Spec Change Log

- 2026-11-21 (review): the one-sided timeline rules moved from the existing `@media (max-width: 259.98px)` block to their own `@media (max-width: 16.2487em)` block, and the dot's `top: 69px` became `calc(60px + 0.65 * var(--font-size-small) - 3px)`. Why: measured in Edge, with a 20px default text size words broke mid-word at 260px and the dot drifted 5.5px off the time at 24px; both now follow the text size, as the jump links did in Story 1.6. Boundaries above keep the original wording; the code and DESIGN.md's dated note are authoritative.

## Review Triage Log

### 2026-11-20 — Review pass
- verdicts: 23 findings — high 0, medium 3, low 11, false 9, maybe-false 0
- findings:
  - `[low]` `[patch]` The timeline line runs from 6px above the first event to 6px above the list's end, not «between the first and last dot» as DESIGN.md says (blind) — the approved mockup draws it this way (`info-program.html:76,87`), so the look stays; DESIGN.md gets a dated note that the line spans the whole list as in the approved mockup.
  - `[low]` `[patch]` DESIGN.md, the CSS comment and the test say the icon sits «on the side away from the line», but on left-hand events it sits next to the line (blind) — the code matches the approved mockup (`margin: 0 0 4px auto`); the wording is corrected (DESIGN.md dated note, CSS comment, test name and docstring).
  - `[medium]` `[patch]` The dot is fixed at `top: 69px` while the time is in rem, so with larger default text it drifts off the time (blind) — measured in Edge: 0.3px off at a 16px root, 5.5px at 24px; the dot's top now follows `--font-size-small`.
  - `[medium]` `[patch]` The one-sided switch is a px breakpoint, so with larger default text the halves get too narrow (blind) — measured in Edge at 260px with a 20px root: «Middag» and «Badstue, stamp og mingling» break mid-word; the one-sided rules move to an em-based query (16.25em = 260px at 16px), as Story 1.6 did for the jump links.
  - `[low]` `[patch]` MT-20 never checks that each dot is level with its time (blind) — MT-20 gets the check (dot centre within 2px of the time's centre), also with larger default text.
  - `[low]` `[reject]` Under a dark forced-colours theme the ink PNG icons can vanish on the black sheet (blind) — the icons are decorative (`alt=""`); time, name, line and dots stay in CanvasText, so nothing is lost to the reader; a backplate would be a design change for Rikke, noted in issues.md.
  - `[low]` `[patch]` The forced-colours test also asserts «no scroll-margin», which the sticky-nav test already covers (blind) — the duplicate assertion is removed.
  - `[false]` `[reject]` The view adds prices by matching the string «programme» (blind) — one page needs extra context; Praktisk's future map link is template text (AD-17), so no second consumer is planned and no caller can diverge.
  - `[low]` `[patch]` The «no price in the template» test only looks at «… kr» patterns, so «340 kroner» or «340,-» would pass (blind) — the test now allows digits only in the times, dates and the 56px image sizes.
  - `[low]` `[patch]` The ceremony time is in Praktisk («kl. [14:00]») and the programme («14:00») with nothing tying them (blind) — the Story 7.4 deferred entry now names both pages.
  - `[low]` `[patch]` A price of 0 (fresh migrate, or a meal the couple pays for) shows «Middagen betales selv: 0 kr.» and nothing records it (blind) — a deferred-work entry for Story 4.5 (settings admin): a meal price of 0 must be handled before the couple can save it.
  - `[false]` `[reject]` Sprint status, task boxes and triage log are not updated (blind) — the finalize step does that.
  - `[low]` `[reject]` `<time datetime="10:00">` carries no date (blind) — a valid time string; no calendar export is planned, and the date is in the sheet's heading and date line.
  - `[low]` `[patch]` Price 0 contradicts «betales selv» (edge-case) — same root cause and fix as the price-0 row above.
  - `[false]` `[reject]` Prices could be missing on another route and render as « kr.» (edge-case) — `programme.html` is rendered only by `info_page` for «programme», which always adds `prices`; `test_prices_follow_the_settings` covers it.
  - `[medium]` `[patch]` The 69px dot drifts with larger default text (edge-case) — same as the dot row above.
  - `[false]` `[reject]` MT-1 (1.7) and MT-19 to MT-21 are not run (verification-gap) — run by Claude with Playwright in Edge 157: all OK, recorded in the test plan.
  - `[false]` `[reject]` AC3 (one-sided below 260px, no horizontal scroll) is checked only as CSS text (intent-alignment) — MT-20 measured in Edge at 259 × 640 and 180 × 320: every icon, time and name right of the line, no overlap, `scrollWidth` = `innerWidth`.
  - `[false]` `[reject]` Alternation is checked only as CSS text (intent-alignment) — MT-20 measured odd events left of and even events right of the line at 360, 320 and 260px.
  - `[low]` `[reject]` Events are checked against the mockup, not EXPERIENCE.md (intent-alignment) — the two agree today (EXPERIENCE.md:116); the mockup is the approved text, and a second oracle would duplicate the list.
  - `[false]` `[reject]` Prices from Settings go beyond the story (intent-alignment) — AC2 asks «Godt å vite» to mark what costs money; reading the existing fields keeps one source (AD-12) and adds no field.
  - `[false]` `[reject]` «Jump links on one line» differs from DESIGN.md (intent-alignment) — MT-19 measured one line at 360px and stacked links at 320 and 180px; DESIGN.md has the dated note.
  - `[false]` `[reject]` Guests cannot yet decide which days to come (intent-alignment) — the story keeps placeholder times until Story 7.4 by design; the deferred entry covers it.

## Design Notes

- **Prices.** All three meal prices exist on `Settings` (Story 1.2), so no field is invented. The selector returns plain ints; the template writes «<n> kr.» as the mockup does. A fresh `migrate` without seed shows «0 kr.»; that is acceptable because invitations are not sent until the 2028 prices are entered (PRD 3.2). Thousands formatting waits for Story 2.3, the first page with an amount ≥ 1000.
- **Jump links reused, not included.** Same classes and markup as Praktisk, so no CSS is duplicated; an include would need the labels in Python or a list literal Django templates cannot express, and the text belongs in the template (AD-17).
- **Day sheets are info sheets.** The mockup gives them the same padding, heading hairline and jump-target behaviour as Praktisk, so `.info-sheet` is reused and `.programme-day` adds only the timeline parts.
- **Placeholder times stay unbracketed** as approved in the mockup; Story 7.4 owns the real times (deferred entry).

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0
- `git status --short static/img wedding/migrations` -- expected: no output

**Manual checks:**
- MT-1 (1.7) and MT-19 to MT-21 are run afterwards by the orchestrator with Playwright in Edge.

## Auto Run Result

Status: done

**Summary:** Programmet has the «Hopp til» links (Fredag · Lørdag · Søndag, same markup as Praktisk), the voluntary line and one info sheet per day with its date line, a CSS-only alternating timeline (`ol`, Rikke's icons with `alt=""`, `<time>`, short name) and «Godt å vite». The three meal prices come from `Settings` through the new `programme_prices` selector, read with the one settings query the view already makes. Below 16.25em (260px at the default text size) the timeline is one-sided; under forced colours the line and dots are CanvasText. Times are the mockup's placeholders until Story 7.4.

**Files changed:**
- `wedding/selectors.py`, `guests/views.py` — `programme_prices`; the settings row is read once per page and passed on.
- `guests/templates/guests/programme.html` — the page.
- `static/css/site.css` — «Programme» section, em-based one-sided timeline, forced-colour line and dots.
- `tests/test_programme_page.py` (new), `tests/test_design_system.py`, `tests/helpers.py`, `tests/test_practical_and_story_pages.py`, `tests/test_info_pages.py` — page structure and text against the mockup, prices from Settings, CSS values; shared HTML helpers moved to `tests/helpers.py`.
- `DESIGN.md`, `deferred-work.md`, `README.md`, `docs/manual-test-plan.md` — dated notes, three deferred entries (7.4 times and text with the ceremony time on both pages, 2.3 kroner display, 4.5 price 0), MT-1 (1.7), MT-19 to MT-21.

**Review:** 11 rows patched (the dot following the text size and the em breakpoint, both measured in Edge, plus DESIGN wording, tests and deferred entries), 0 deferred, 12 rejected with reasons in the triage log.

**Follow-up review recommendation:** false. No high was patched; the two medium fixes were re-measured in Edge after patching (dot drift 0px at 16px and 20px default text; one-sided at 320px with 20px text, no word broken), so no unverified risk can be named.

**Verification:** `uv run pytest` 628 passed; ruff and djlint clean; MT-1 (1.7), MT-19 (click, keyboard, touch, short viewport, lines), MT-20 (alternating at 360/320/260px, one-sided at 259/180px, dots level with the time, larger default text) and MT-21 (accessibility tree, emulated forced colours) run by Claude with Playwright in Edge 157 after the patches.

**Residual risks:** times and text are placeholders until Story 7.4; a meal price of 0 would read «betales selv: 0 kr.» until Story 4.5 decides; under a real dark contrast theme the ink icons may be hard to see (decorative; not tested with a real Windows theme).
