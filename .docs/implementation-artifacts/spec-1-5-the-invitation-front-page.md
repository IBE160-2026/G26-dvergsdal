---
title: 'Story 1.5: The invitation front page'
type: 'feature'
created: '2026-11-20'
status: 'done'
baseline_revision: 'f0a920b24b6455399bdccca64a84b08b2bb8fe5d'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/front-page-3.html'
warnings:
  - multiple-goals
  - oversized
deferred:
  - summary: >-
      An unknown second segment under a valid code (for example /<code>/svar/) shows Django's own 404 instead of G1.
    evidence: |-
      Same case as the multi-segment paths deferred by 1.4b; Story 1.8's handler404 should render a G1-style page for every unmatched path.
    location: >-
      guests/urls.py
    severity: low
---

<intent-contract>

## Intent

**Problem:** Every `/<code>/`, valid or not, shows G1 with 404 (`guests/views.py:front_page`), so a guest never sees the invitation, and the three topic pages have no address (FR-2, FR-6–FR-8, FR-11, FR-41, UX-DR6–9, UX-DR11, UX-DR12, UX-DR51).

**Approach:** The view resolves the code with `wedding.links.resolve_code`, keeps G1 (404) for `None`, and renders the approved front page (front-page-3.html; DESIGN.md and EXPERIENCE.md win) from the household, `Settings` and two new pure rules. Three info pages get the frame only. Tests prove structure, privacy and no writes over HTTP; browser checks become MT rows for the orchestrator.

## Boundaries & Constraints

**Always:**
- **Routes** (`guests/urls.py`, after `""`): `<str:code>/` → `front_page` (name `front_page`), `<str:code>/program/` (`programme`), `<str:code>/praktisk/` (`practical`), `<str:code>/historie/` (`our_story`): paths from the architecture memlog (line 51), recorded in AD-6 by this story. All four call `resolve_code`; `None` → `render(request, PRIVATE_INVITATION, status=404)`, unchanged G1.
- **Reads only:** front page = exactly 3 SELECTs (resolver, the household's guest names, `Settings.objects.get()`), info page = 2; well-formed unknown code = 1, malformed = 0. No session, messages, `request.user`, `{% csrf_token %}`, cookies or `<script>`. Never `get_or_create`/`first()` on `Settings`.
- **Rules** (pure, `wedding/rules/`): `households.household_names(names) -> str` («Synne», «Sigmund og bestemor», «Arild, Marie, Filippa og Leone», `""` for none; order as given) and `households.speaks_to_one(household_size) -> bool` (`== 1`, UX-DR51); `contacts.tel_number(phone) -> str` (a leading `+` and the digits only, «+47 000 00 101» → «+4700000101»; `""` when no digit; FR-6). Words «deg»/«dere» live in templates.
- **Selectors** (`wedding/selectors.py`): `site_settings()` = `Settings.objects.get()`; `household_guest_names(household)` = names ordered by id.
- **Page order** (front page): nav bar → `<main class="column …">` with hero sheet, lead-in, «Alt om helgen» `section`, RSVP sheet → footer band. Text exactly: nav `<nav aria-label="Invitasjonen">` with a `ul` of «Program», «Praktisk», «Vår historie» (no separator characters) and the link «Svar» (`#svar` on the front page, `{% url 'guests:front_page' code %}#svar` on info pages); hero: `segl.png` (`alt=""`), `illustrasjon.jpg` (alt «Akvarell av tunet på Hardingasete.»), `h1` «Rikke & Valdemar» as three spans, «inviterer deg|dere til sitt bryllup», `brudeslor.png` 224px (`alt=""`), «Lørdag 27. mai 2028» and «Hardingasete · Hardanger» (small caps, the dot in `<span aria-hidden="true">`), «for <household_names>» (names upright), «<a href="#svar">Svar</a> innen {{ deadline|date:"j. F Y" }}»; lead-in «Vi gleder oss til å feire med deg|dere»; `h2` «Alt om helgen» between `lilje-topp.png` and `lilje-bunn.png`; a `ul` of three topic rows: `blonde.png` frame (`alt=""`) over `sted-middag.jpg` (alt «Der vi skal spise middag på Hardingasete.») + `h3` «Programmet» + «Hele helgen, dag for dag.»; `sted-tunet.jpg` (`object-position: 50% 82%`, alt «Tunet på Hardingasete, der vi skal bo og feire.») + «Praktisk informasjon» + «Reise, hyttene, tunet og området rundt.»; `oss-strand.jpg` (alt «Rikke og Valdemar på stranda.») + «Vår historie» + «Fra vi møttes til i dag.»; each «Les mer» followed by `<span class="visually-hidden"> om programmet</span>` (and « om praktisk informasjon», « om vår historie») as `.button.button--on-green` to its page; RSVP `section id="svar" tabindex="-1" aria-labelledby` its `h2` «Svar på invitasjonen», `brudeslor.png` 180px, «Barnefritt bryllup», «Svar innen {{ deadline|date:"l j. F Y" }} kl. 23:59».
- **Footer band** (`wedding/components/footer-band.html`, used by every valid-link page): «Spørsmål? Send oss en melding:» then one `<a href="tel:{{ contact.tel }}">{{ contact.name }} {{ contact.phone }}</a>` row per contact whose `tel_number` is not empty, contact 1 first; with no phone at all the whole `<footer>` is left out.
- **Info frame** (`guests/info_page.html`): back link «<span aria-hidden="true">←</span> Tilbake til invitasjonen» to the front page, `h1` (italic `heading-page`, cream hairline), empty `{% block info_content %}`, bottom `.button.button--on-green` «Tilbake til invitasjonen», nav word `aria-current="page"`. Titles «Programmet – Invitasjon», «Praktisk informasjon – Invitasjon», «Vår historie – Invitasjon»; the front page keeps «Invitasjon».
- **CSS** values from DESIGN.md frontmatter `components` and Layout & Spacing (tokens where they exist, rem font sizes, raw px/rgba from DESIGN where no token exists). Nav: flat `page-green`, min-height `--space-nav-height`, padding 8px 12px 8px 16px, words gap 12px, hairline `box-shadow: 0 1px 0 rgba(245,238,223,.22)`, `z-index: 3`; `.nav-bar__svar` per `nav-svar`; below 340px the tighter values. `@media (min-height: 400px) and (min-width: 320px)`: nav `position: sticky; top: 0` and `html { scroll-padding-top: calc(var(--space-nav-height) + var(--space-scroll-gap)) }` (no `scroll-margin-top` on `#svar`: the two add up). `.hero { container-type: inline-size }` and `@container (max-width: 13.7em) { .hero__names > span { display: block } }` (274px ÷ 20px). Topic rows stack below 300px. Below 260px hero, RSVP and info sheets take `--space-gutter-narrow` inline padding; hero takes `--space-hero-padding-inline-small-phone` from 260 to 339.98px. Forced colours: illustration `mix-blend-mode: normal`, nav `border-bottom: 1px solid CanvasText`. `#svar:focus` gets `outline-color: transparent` (a non-interactive jump target; visible under forced colours). `.visually-hidden` utility.
- Every `<img>` has `width`/`height`; images below the hero get `loading="lazy"`.
- Docstrings, template comments and CSS section comments name FR/NFR/UX-DR/AD ids.

**Never:** no RSVP button or `/svar/` route (2.1), draft notice, answered state or status block (2.x); no «Personvern» link (7.1); no info-page content or jump links (1.6, 1.7); no `handler404`/500 (1.8); no JavaScript, no new or changed image files, no wedding date or place from the database (template text, AD-17); no `&nbsp;` or `nowrap` in dates (at 180 CSS px a no-break date overflows the sheet); no names or codes in `<title>` or preview tags; no running a browser (the orchestrator runs the MT rows).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Two invited | seed; GET `/test-sigmund0000000000/` | 200; «for Sigmund og bestemor», «inviterer dere», «feire med dere»; no other household's names; 3 SELECTs | N/A |
| One invited | GET `/test-synne000000000000/` | «for Synne», «inviterer deg», «feire med deg» | N/A |
| Four invited | GET `/test-arild000000000000/` | «for Arild, Marie, Filippa og Leone» | N/A |
| Unsafe name | guest named `<b>Ola</b>` | shown escaped (`&lt;b&gt;Ola&lt;/b&gt;`) | N/A |
| Deadline | `rsvp_deadline` 2028-01-04 / 2027-12-31 | «Svar innen 4. januar 2028» + «Svar innen tirsdag 4. januar 2028 kl. 23:59» / «… fredag 31. desember 2027 kl. 23:59» | N/A |
| Phones | «+47 000 00 101», «+47 000 00 102» / contact 2 blank / both blank | two rows, `href="tel:+4700000101"`, text «Rikke +47 000 00 101» / one row / no `<footer>`, no `tel:` | N/A |
| Info page | GET `/<code>/program/`, `/praktisk/`, `/historie/` | 200; its title and `h1`; that nav word `aria-current="page"`, the others none; back links to `/<code>/`; nav «Svar» to `/<code>/#svar`; footer; 2 SELECTs | N/A |
| Unknown code | `/AAAAAAAAAAAAAAAAAAAAAA/` and `…/program/` / `/hei/`, `/hei/praktisk/` | 404, the same G1 body as `/`; 1 / 0 queries | N/A |
| No writes | every valid GET above | row counts and `Household.revision` unchanged, only SELECTs, no `Set-Cookie`, no session row | N/A |

</intent-contract>

## Code Map

- `guests/views.py:44-66` -- `PRIVATE_INVITATION`, `private_invitation`, `front_page` (docstring promises the resolver here, G1 for `None`); add `info_page` with an `INFO_PAGES` map (key → template) and a private footer-contacts helper.
- `guests/urls.py:20-26` -- `stil/` first when local, then `""` and `<str:code>/`; module docstring names 1.5.
- `config/urls.py:1-11` -- docstring lists what `guests.urls` holds.
- `wedding/links.py:34-46` `resolve_code` -- format check then one `select_related` SELECT; returns `GuestActor(guest, household)` (`wedding/actors.py:60-65`).
- `wedding/selectors.py` -- only `seed_conflicts` today; add the two selectors.
- `wedding/rules/households.py:1-18` -- size rule; `wedding/rules/__init__.py` says pure only (`tests/test_rules_purity.py`).
- `wedding/models.py:35-53` Household docstring («for Sigmund og bestemor» derived in 1.5); `:81-114` Settings (`contact_N_name/phone`, `rsvp_deadline`). Migration `0003_settings_row.py` default: blank phones, deadline 2028-01-04.
- `wedding/templates/wedding/base.html:11` title block, `:22-23` `head` block, `:27-28` `content` block.
- `guests/templates/guests/private_invitation.html:3-12` -- comment says «until Story 1.5».
- `static/css/site.css` -- header comment `:1-9`; `.display-names` `:237-243`; `.small-caps` `:251-253`; `.paper-sheet` `:275-290`; `.column` `:306-310`; `.button--on-green` `:375-388`; narrow widths `:490-504`; forced colours `:512-536`; motion `:542-546`. Values to copy: `mockups/front-page-3.html:36-84` (nav, hero, lead-in, details, rows, lace frame, footer).
- `static/img/` -- all front-page files exist (sizes: segl 148×152, illustrasjon 524×287, brudeslor 448×100, lilje-topp 592×145, lilje-bunn 592×129, blonde 320×309, sted-middag 440×548, sted-tunet 440×661, oss-strand 400×400); `tests/test_images.py:63-73` `FRONT_PAGE` and the 300 KB budget.
- `tests/test_private_invitation.py:27,94-120` -- 22-char unknown code asserted with 0 queries; seeded-link-is-G1 test. `tests/test_guest_privacy.py:142-146` (seeded link 404), `:237-254` (preview same for every code), `:285-297` (`fixed` routes must be in `NOT_LINK_CODES`: excludes only `""` and `<str:code>/`). `tests/test_log_masking.py:181-197` (seeded code expected 404). `tests/test_links.py:1-5` docstring. `tests/conftest.py` `assert_loads_only_own_host` (`tel:` has no `://`).
- `docs/manual-test-plan.md` -- last id MT-10; Norwegian; MT-1/MT-9 add rows per story.
- `README.md:9` status, `:31`, `:64`, `:66` (G1/404 sentences), `:150` `guests/` tree line.
- `ARCHITECTURE-SPINE.md:114` AD-6 URL bullet; `EXPERIENCE.md:319` Accessibility Floor › Sticky bar and focus.

## Tasks & Acceptance

**Execution:**
- [x] `wedding/rules/households.py`, `wedding/rules/contacts.py` -- `household_names`, `speaks_to_one`, `tel_number` as in Boundaries -- AD-2, AD-4, FR-6, FR-7, UX-DR51.
- [x] `wedding/selectors.py` -- `site_settings`, `household_guest_names` -- FR-2, FR-3.
- [x] `guests/views.py`, `guests/urls.py`, `config/urls.py` -- resolver branch in `front_page`, `info_page`, four routes, docstrings -- AD-6, FR-2, FR-3, FR-5, FR-11.
- [x] `wedding/templates/wedding/components/footer-band.html`, `guests/templates/guests/components/nav-bar.html`, `guests/templates/guests/guest_page.html` (base + nav + main block + footer), `guests/templates/guests/front_page.html`, `guests/templates/guests/info_page.html`, `guests/templates/guests/programme.html`, `guests/templates/guests/practical.html`, `guests/templates/guests/our_story.html`; update the G1 template comment -- FR-6–FR-8, FR-11, FR-41, UX-DR6–9, UX-DR11, UX-DR12, UX-DR51.
- [x] `static/css/site.css` -- sections nav bar, guest page column, hero, lead-in, details and topic rows, lace frame, RSVP sheet, footer band, info frame, visually-hidden, sticky/scroll-padding query, container query, narrow widths, forced colours; header comment -- UX-DR6–9, UX-DR11, UX-DR12, UX-DR30, UX-DR53, NFR-5.
- [x] `tests/test_guest_page_rules.py` -- `household_names` (0–4 names, order kept), `speaks_to_one` (1 vs 2, 8), `tel_number` («+47 000 00 101» → «+4700000101», «900 00 000», «(+47) 900-00-000» → «+4790000000», «» and «ukjent» → «»).
- [x] `tests/test_front_page.py` -- every matrix row for `/<code>/`; section order (nav < hero < lead-in < `Alt om helgen` < `id="svar"` < footer); hero order (`segl.png` < `illustrasjon.jpg` < `<h1` < invites < `brudeslor.png` < date < place < «for» < deadline); one `h1`; `Les mer` hrefs and accessible names; FR-2 for every seeded household (its names present, every other seeded guest name absent by `\b`); FR-3 no-write for the front page and the three info pages (row counts, `Household.revision`, SELECT-only via `CaptureQueriesContext`, `response.cookies` empty, `Session.objects.count() == 0`); rendered `<img src>` set under `/static/img/` equals `test_images.FRONT_PAGE`; no `<script`; `assert_loads_only_own_host`.
- [x] `tests/test_info_pages.py` -- info-page matrix row for all three; unknown and malformed codes on each give G1 404 with 1/0 queries.
- [x] `tests/test_private_invitation.py`, `tests/test_guest_privacy.py`, `tests/test_log_masking.py`, `tests/test_links.py` -- G1 query counts per format; seeded link → 200 front page with the headers (and each info page); preview test extended to each info page for two seeded codes (same title and og tags per page, no names); `fixed` routes exclude routes starting with `<str:code>/`; `_EXTERNAL_LINK` skips hrefs starting with `tel:` (they reach no site), proved with a good sample `<a href="tel:{{ contact.tel }}">`; log test gets its 404 from `/AAAAAAAAAAAAAAAAAAAAAA/`, the seeded code answers 200, and the code still never appears; resolver docstring points to `test_front_page.py`.
- [x] `tests/test_design_system.py` -- sticky and scroll-padding only inside the 400px/320px query; `@container` block stacks the names' spans and sets no font size; forced colours drop the illustration blend; `.visually-hidden` exists.
- [x] `docs/manual-test-plan.md` -- rows below (Norwegian, «kjøres av Claude med Playwright mot Edge», date and result cells empty). Server: `uv run manage.py seed_testdata`, `uv run manage.py runserver`; links `http://127.0.0.1:8000/test-sigmund0000000000/` (S, «dere») and `http://127.0.0.1:8000/test-synne000000000000/` (Y, «deg»). Measure after `document.fonts.ready` and every `.hero img` `complete`.
  - MT-1 (1.5): README steps, then S shows the invitation, not G1.
  - MT-9 (1.5): terminal shows `"GET /[code]/ HTTP/1.1" 200` for S and `404` + `Not Found: /[code]/` for `/AAAAAAAAAAAAAAAAAAAAAA/`; the code never.
  - MT-11 (first screen): S and Y at 360 × 560 and 320 × 568: `.hero` `getBoundingClientRect().bottom` ≤ 560 / 568; `h1` one line (height < 2 × its line height); at 300 × 568 and 180 × 320 the three name spans have increasing `top`; at 180 × 320 topic rows stacked (frame above text); every size `document.documentElement.scrollWidth` ≤ `innerWidth`.
  - MT-12 (jump to `#svar`, `reducedMotion: 'reduce'`): 360 × 640: nav computed `position` `sticky`; click nav «Svar», then from the top Tab to the hero «Svar» and press Enter: hash `#svar`, `#svar h2` top ≥ nav bottom. 360 × 380 and 300 × 640: nav `static`, after the click `#svar h2` top within 0…viewport height. From `/test-sigmund0000000000/program/` nav «Svar» lands on `/test-sigmund0000000000/#svar` with the same check.
  - MT-13 (bar and footer): 320 × 568 and 360 × 560: the three nav `li` share one `top`, nav height 64 ± 1, each nav word ≥ 44 tall, «Svar» ≥ 44 tall and ≥ 56 (320) / 64 (360) wide; every `a[href^="tel:"]` ≥ 44 tall.
  - MT-14 (4G, NFR-7): viewport 360 × 640, CDP `Network.enable`, `Network.setCacheDisabled {cacheDisabled: true}`, `Network.emulateNetworkConditions {offline: false, latency: 165, downloadThroughput: 1012500, uploadThroughput: 168750}` (Chrome DevTools «Fast 4G»: 9 / 1.5 Mbit/s × 0.9, 60 ms × 2.75); open S with `waitUntil: 'load'`; record `loadEventEnd` of the navigation entry and the last `largest-contentful-paint` (buffered observer); three runs, median. Pass: both < 3000 ms and `document.fonts.check('48px "Imperial Script"')`. Second row, information only: «Slow 4G» (`latency: 562.5, downloadThroughput: 180000, uploadThroughput: 84375`).
- [x] `README.md` -- status line (1.5: front page and info-page frame), `:31`/`:64` (test links open the invitation; `/` and unknown codes show G1), `:66` (`200` for a test link), `guests/` tree line; `ARCHITECTURE-SPINE.md` AD-6 -- dated 2026-11-20 note naming `/<code>/program/`, `/praktisk/`, `/historie/` (from the memlog; `/svar/` and `/personvern/` follow in 2.1 and 7.1); `EXPERIENCE.md:319` -- dated note: sticky also needs ≥ 320px layout width (a wrapped bar would cover jump targets), scroll padding only on `html` (DESIGN's `scrollMarginTop` is met by it; both together double the gap).

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given seeded codes from two households, when their front pages and each info page are fetched, then title and Open Graph tags match per page, name nobody, and every response has `X-Robots-Tag: noindex` and `Referrer-Policy: same-origin`.
- Given a seeded test link, when the front page and its three info pages are fetched with GET, then no row is created or changed and only SELECTs run (FR-3 over HTTP).
- Given the rendered front page, when its images are collected, then they are exactly the nine `FRONT_PAGE` files and it has no script.
- Given `docs/manual-test-plan.md`, when read, then MT-1, MT-9 (1.5) and MT-11 to MT-14 hold the steps above with empty result cells.

## Spec Change Log

## Review Triage Log

### 2026-11-20 — Review pass
- verdicts: 28 findings — high 1, medium 5, low 16, false 6, maybe-false 0
- findings:
  - `[high]` `[patch]` The hero does not fit above the fold: `.hero` bottom is 578px at 360×560 and 320×568 (orchestrator, Playwright in Edge, MT-11) — hero spacing reduced; re-measured.
  - `[low]` `[patch]` MT-12 expects the bar `static` below the sticky query, but it is `position: relative` (orchestrator, MT-12) — the row now says «ikke `sticky`»; behaviour was right (heading visible).
  - `[false]` `[reject]` Browser outcomes (fold, #svar jump, 44px, 4G) are only plans with empty results (intent-alignment) — MT-1, MT-9, MT-11 to MT-15 were run by Claude with Playwright in Edge and recorded.
  - `[low]` `[reject]` Sticky also needs a minimum width, so at ~180 CSS px the bar scrolls away (intent-alignment) — deliberate and recorded in EXPERIENCE.md: a 64px sticky bar on a 180px-wide zoomed screen would cover too much; «Svar» stays in the hero and in the bar at the top.
  - `[low]` `[reject]` The footer is left out when no phone is usable (intent-alignment) — FR-6 asks for the numbers from Settings; a footer with no number to call would be an empty promise; documented in the template.
  - `[low]` `[reject]` Italic heading, hairline and italic lines are not tested (intent-alignment) — visual styling, checked in the Playwright screenshots; a CSS-text test would add nothing.
  - `[false]` `[reject]` «deg»/«dere» also in the lead-in goes beyond the hero AC (intent-alignment) — UX-DR51 applies to every text addressed to the guest.
  - `[false]` `[reject]` FR-7's «jump to the RSVP button» conflicts with the story's exclusion (intent-alignment) — the AC says the RSVP sheet `#svar`, which is implemented; the button arrives in 2.1.
  - `[medium]` `[patch]` The footer's no-digit rule is only tested with an empty phone (verification-gap) — parametrized over `""` and `"ukjent"`, plus a both-unusable case.
  - `[false]` `[reject]` Manual rows for 1.5 are empty (verification-gap, other) — same as the intent row above: run and recorded.
  - `[medium]` `[patch]` DESIGN.md still says scroll-margin on the sheets, sticky on height only and a border instead of a box-shadow (blind) — DESIGN.md updated with a dated reason.
  - `[low]` `[patch]` EXPERIENCE.md keeps the old sentence about `scroll-margin-top` and the open [ASSUMPTION] (blind) — sentences fixed, the dated note kept.
  - `[medium]` `[patch]` Larger text wraps the rem-sized nav words at px widths ≥ 320, so the bar outgrows the scroll padding and covers `#svar` (blind) — the width condition is em-based.
  - `[false]` `[reject]` sprint-status, session log and deferred notes are missing (blind) — the orchestrator does these after the build.
  - `[false]` `[reject]` In-review before the manual tests were run (blind) — run and recorded before finalizing.
  - `[low]` `[patch]` MT-14 has a duplicate id, a conflicting «fonts.ready» line and an unused Y link (blind) — Slow 4G is MT-15; wording fixed.
  - `[low]` `[patch]` Test helpers copied across five test files and a cross-module import (blind) — moved to tests/conftest.py and a helper module.
  - `[low]` `[patch]` Two tests assert the same query count (blind) — the duplicate removed.
  - `[medium]` `[patch]` The footer contact list is built in guests/views.py although the footer is shared with Story 1.8's error pages; `Settings` imported only for a hint (blind) — moved to `wedding/selectors.py`.
  - `[low]` `[patch]` Both views repeat the same setup (blind) — one helper for the shared guest-page context.
  - `[low]` `[reject]` The info pages are empty (blind) — Stories 1.6 and 1.7 fill them in this same run; a temporary «kommer» line would be removed again.
  - `[low]` `[patch]` The sticky CSS test reads comments, and the hairline colour is repeated (blind) — comments stripped; one custom property.
  - `[medium]` `[patch]` Larger default font size wraps the nav and hides `#svar` under the bar (edge-case) — same as the em-based query row.
  - `[low]` `[reject]` A guest deleted between `resolve_code` and the name lookup renders an empty «for» line (edge-case) — reads are not in one transaction, but deleting a guest is an admin action (6.5) that happens rarely and the next load is right; a guard adds a branch for a race nobody will meet.
  - `[low]` `[reject]` A missing or duplicated Settings row makes every link answer 500 (edge-case) — the data migration creates exactly one row and no service deletes it (Story 1.2); the error page is Story 1.8.
  - `[low]` `[defer]` An unknown second segment under a valid code (`/<code>/svar/`) shows Django's own 404 (edge-case) — the same multi-segment case already deferred to Story 1.8's handler404.
  - `[low]` `[patch]` «+47 (0) 900 00 000» dials a wrong number (edge-case) — `tel_number` drops a «(0)» trunk prefix, with a rule test.
  - `[low]` `[patch]` The filter-set test crashes with AttributeError on a `backdrop-filter`-only rule (edge-case) — the match is asserted first.

## Design Notes

- **Names stack by container query.** Natural wrapping gives «Rikke &» / «Valdemar»; DESIGN wants three lines. A container query in `em` follows the phone's text size, unlike a px media query; browsers without it keep the natural wrap. 274px is DESIGN's estimate: MT-11 re-measures it.
- **Sticky needs width too.** At 180 CSS px wide and ≥ 400px tall (200 % zoom on a tall phone) the words wrap to several lines and the bar would cover `#svar`; scrolling away is what EXPERIENCE already does for short screens.
- **4G profile.** Chrome's «Fast 4G» is its 4G preset («Slow 4G» is the old «Fast 3G»); fonts (≈ 279 KB) plus hero images make the first load ≈ 330 KB, and lazy images keep the rest off it.
- Golden hero names: `<h1 class="display-names hero__names"><span>Rikke</span> <span>&amp;</span> <span>Valdemar</span></h1>`.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0
- `git status --short static/img` -- expected: no output (no image changes)

**Manual checks:**
- MT-1, MT-9, MT-11 to MT-14 are run afterwards by the orchestrator with Playwright in Edge.

## Auto Run Result

Status: done

**Summary:** A valid personal link now opens the invitation's front page: sticky nav bar (sticky at ≥ 400px tall and ≥ 20em wide), hero sheet (seal, illustration, names as `h1`, «deg»/«dere», date, place, household names, deadline with «Svar» link), lead-in, «Alt om helgen» with three lace-framed topic rows, the RSVP sheet `#svar` with the full deadline, and the footer band with `tel:` links. The three info pages (`/<code>/program/`, `/praktisk/`, `/historie/`) have the frame only. Unknown codes still get G1 with 404. Opening any page writes nothing (FR-3, tested over HTTP).

**Files changed:**
- `wedding/rules/households.py`, `wedding/rules/contacts.py`, `wedding/selectors.py` — household names, «deg»/«dere», `tel_number`, settings and footer contacts.
- `guests/views.py`, `guests/urls.py`, `guests/templates/guests/*`, `wedding/templates/wedding/components/footer-band.html` — front page, info-page frame, nav bar, footer.
- `static/css/site.css` — nav bar, hero, «Alt om helgen», RSVP sheet, footer, info frame, narrow widths, forced colours.
- `tests/` — new rule, front-page and info-page tests; shared fixtures moved to `conftest.py` and `helpers.py`; 1.4b/1.4c tests updated for a valid code giving 200.
- `DESIGN.md`, `EXPERIENCE.md`, `ARCHITECTURE-SPINE.md` (AD-6), `README.md`, `docs/manual-test-plan.md` — dated notes, MT-1/9/11–15.

**Review:** 15 rows patched (one high: the hero did not fit above the fold), 1 deferred, 12 rejected with reasons in the triage log.

**Follow-up review recommendation:** false. The one high (hero above the fold) was patched and then re-measured in Edge (548px at 360×560 and 320×568), so no unverified risk can be named. Patched counts: high 1, medium 4, low 10.

**Verification:** `uv run pytest` 578 passed; ruff and djlint clean; MT-1, MT-9 and MT-11 to MT-15 run by Claude with Playwright in Edge after the patches (all pass; Fast 4G median load 484 ms, LCP 580 ms); 1.4b and 1.4c browser checks still pass.

**Residual risks:** the hero spacing change (30px less, in DESIGN.md) and the place line wrapping as «HARDINGASETE · / HARDANGER» need Rikke's approval; unknown second segments show Django's 404 until Story 1.8.
