---
title: "Story 1.4b: Paper, Rikke's images and the private-invitation page"
type: 'feature'
created: '2026-11-20'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md'
warnings:
  - multiple-goals
  - oversized
deferred: []
---

<intent-contract>

## Intent

**Problem:** Guest content can only sit on the flat `.surface-cream` from 1.4a: there is no paper sheet, no page texture, none of Rikke's images in `static/img/`, and `/` or a wrong link gives Django's 404 page (FR-5, NFR-5, UX-DR3, UX-DR4, UX-DR5, UX-DR30, UX-DR53 reflow).

**Approach:** Add the textured page and the `edge-b3` paper sheet to `site.css`, prepare Rikke's images into `static/img/` with a committed, rerunnable script, and serve the G1 private-invitation page at `/` and `/<code>/`, proved by tests and a browser-size entry in the manual test plan.

## Boundaries & Constraints

**Always:**
- Sheet per DESIGN.md › Elevation & Depth and frontmatter `components.paper-sheet`: colour, `grain-sheet` + `fibre-sheet` texture (blend `overlay`), `edge-b3` filter and shadow all on `.paper-sheet::before` (`z-index: -1`, sheet has `position: relative; isolation: isolate`); `::before` keeps `background-color: var(--color-panel-cream)` and `border-radius: var(--radius-sheet)`, so without filter support it is the flat 5px sheet. Text, links and focus rings sit on the element, never filtered.
- The sheet shares `.surface-cream`'s ink text, `--focus-color`, ink outlined button and forced-colours rules by joining those selector lists, not by copied declarations.
- Page: `body` gets the calm `grain-green` texture (`overlay`). Texture data-URIs are copied from `mockups/paper-ceremony-5.html:31-33`, written as `url("data:image/svg+xml,<svg …>")` **without `;utf8`** and with no `;` inside (the 1.4a test parser splits on `;`). Each texture's `feColorMatrix` offset + slope/2 = 0.5, so overlay leaves the average colour unchanged.
- Forced colours: sheet gets `border: 1px solid CanvasText`; `::before` and `body` drop texture and filter.
- `edge-b3` is an inline `<svg>` include (copy of `paper-ceremony-5.html:185-209`), `aria-hidden="true" focusable="false"`, zero-size via a CSS class, **no `xmlns`** (base-template test asserts no `://`).
- Images come only from Rikke's files and the approved cutouts (list in Code Map), never drawn in code. Photos and illustration as progressive JPEG, cutouts and icons as palette-quantised PNG (all browsers, old iPads included), at most 2× the largest display width, never upscaled. Budget: every file ≤ 100 KB; the front-page set (seal, illustration, gypsophila, both garlands, lace frame, `sted-middag`, `sted-tunet`, `oss-strand`) ≤ 300 KB together (NFR-7: fonts are ~280 KB more on 4G).
- Favicon from the seal (32px PNG, transparent; 180px apple-touch icon on `page-green`, since iOS paints transparency black), linked from base.html inside `{% block icons %}`.
- G1 (privacy-1.html, DESIGN.md:583): `<main>`, one centred `.paper-sheet` 120px below the top, `h1` italic in `heading-card` size «Dette er en privat invitasjon», gypsophila 180px wide (`max-width: 100%`, `alt=""`), «Virker ikke lenken din? Ta kontakt med brudeparet direkte.». Empties `icons`. Reads nothing from the database.
- Column (reusable class): max `--space-content-max`, centred, gutter `--space-gutter`; 260–339.98px → `--space-gutter-small-phone`; below 260px → `--space-gutter-narrow`, and the G1 sheet's inline padding drops to `--space-gutter-narrow` too.
- Docstrings, template comments and CSS section comments name FR/NFR/UX-DR ids.

**Never:** no seal, favicon, names, phone numbers, date, place, nav bar, footer or `tel:` on G1; no WebP/AVIF; no external URL; no `outline: none`, `@keyframes`, px font sizes or JS; no images in `static/` outside `static/img/`; no `.py` in `static/`; Pillow is not a project dependency. Not in this story: the «Personvern» link (7.1), privacy headers and Open Graph (1.4c), the resolver branch and front page on `/<code>/` (1.5), the error pages (1.8), using the other images in pages (1.5–1.7), running a browser.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Bare address | GET `/`, empty migrated DB | 200, G1 page, zero DB queries | N/A |
| Unknown code | GET `/AAAAAAAAAAAAAAAAAAAAAA/`, `/hei/` | 404 status, same G1 body, zero DB queries | N/A |
| Any code before 1.5 | GET a seeded test link | G1 page, 404 (front page arrives in 1.5) | N/A |
| Seeded data present | `seed_testdata` run, GET `/` | no guest name, couple name, phone, «2028», «Hardingasete», «Strandebarm», `segl`, `<nav`, `<footer`, `tel:` in HTML | N/A |
| Style sample | GET `/stil/`, `APP_ENV` local / production | 200 sample / 404 G1 page (code pattern is after `stil/`) | N/A |

</intent-contract>

## Code Map

- `guests/urls.py` -- `/stil/` appended only when local; add `""` and `<str:code>/` **after** it. `config/urls.py` -- docstring: `admin/` (dashboard) must be added before the guest include, since `<str:code>/` matches any segment.
- `guests/views.py` -- `style_sample` only; add the G1 views. `wedding/links.py:resolve_code` -- not called in this story (1.5 adds it).
- `wedding/templates/wedding/base.html` -- add `{% block icons %}` (favicon links) in `<head>` and the edge-filter include at the start of `<body>`.
- `static/css/site.css:241-251` `.surface-cream`; `:347-351` `.surface-cream .button--on-green`; `:394-411` forced-colours block; header comment line 7 names 1.4b.
- `tests/test_design_system.py:87-130` parsers (`_custom_properties` regex `([^;]+);`, `_rules`); `:264` `test_every_url_points_to_a_local_file` reads the nested `url(%23t)` and `http://www.w3.org/2000/svg` inside a data-URI as files/URLs and will fail; `:397` base template asserts `"://" not in html`; `:568` production `/stil/` test asserts only 404.
- Sources: `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/` `segl.png` 200×206, `brudeslor.png` 640×143, `lilje-topp.png`/`lilje-bunn.png` 760 wide, `blonde.png` 320×309, `us1-utsnitt.jpg` 400×400, `ikoner/ikon-01-fjelltur.png`…`ikon-12-avreise.png` 128px; `.docs/planning-artifacts/ux/egne-bilder/04-Illustration.jpg` 1695×928 (checked: no signature or text), `13-Us2.jpg`; venue photos `.docs/planning-artifacts/ux/stedet/01-Venue.jpg`, `03-Venue.jpg`, `12-Area.jpg`, `18-Kirka.jpg` (permission: EXPERIENCE.md:420). Cutout scripts in `.working/cutout-*.py` show the Pillow style.
- Targets in `static/img/` (display width → file width): `segl.png` 74→148, `favicon-32.png`, `apple-touch-icon.png` 180, `brudeslor.png` 224→448, `lilje-topp.png`/`lilje-bunn.png` 296→592, `blonde.png` 320, `illustrasjon.jpg` 262→524, `oss-strand.jpg` 400, `oss-utsikt.jpg` 440, `sted-middag.jpg` (01), `sted-tunet.jpg` (03), `sted-kirka.jpg` (18), `sted-omradet.jpg` (12) all 440 wide, `ikoner/ikon-NN-*.png` 56→112. Planner trial: JPEG q≈72–80 and 256-colour PNG gave a front-page set of ≈250 KB.
- `docs/manual-test-plan.md` -- last id MT-4; Norwegian.

## Tasks & Acceptance

**Execution:**
- [ ] `tools/prepare_images.py` -- reads the sources above, writes every target (resize with LANCZOS, quantise PNGs keeping alpha, progressive optimised JPEG); run with `uvx --with pillow==13.0.0 python -I tools/prepare_images.py`; docstring names UX-DR4 and NFR-7 -- reproducible, no runtime dependency.
- [ ] `static/img/` -- run the script, commit the outputs, delete `.gitkeep`; `static/img/README.md` lists each file, its source, display size and the command -- UX-DR4.
- [ ] `static/css/site.css` -- texture custom properties; textured `body`; `.paper-sheet` + `::before`; column class with the three gutters; G1 layout; joined selector lists; forced-colours additions; header comment -- UX-DR3, UX-DR5, UX-DR30, UX-DR53.
- [ ] `wedding/templates/wedding/components/paper-filters.html`, `wedding/templates/wedding/base.html` -- filter include and `icons` block.
- [ ] `guests/templates/guests/private_invitation.html`, `guests/templates/guests/style_sample.html` (one `.paper-sheet` sample), `guests/views.py`, `guests/urls.py`, `config/urls.py` -- G1 at `/` (200) and `<str:code>/` (404); the code view's docstring says Story 1.5 puts the resolver and front page here -- FR-5, UX-DR30.
- [ ] `tests/test_design_system.py` -- skip whole data-URIs in the URL test (assert they contain no `://` other than the SVG namespace); textures centre on 0.5; `.paper-sheet::before` has cream, sheet radius and `filter: url(#edge-b3)`; forced-colours sheet border and texture removal; gutter media queries use the tokens; production `/stil/` shows G1, not the sample.
- [ ] `tests/test_images.py` -- every target exists with PNG/JPEG magic bytes and the planned width; size budget; README lists every file; every `<img>` in every template has `alt`; base.html has the favicon links.
- [ ] `tests/test_private_invitation.py` -- every matrix row, with `django_assert_num_queries(0)` and on an empty migrated DB.
- [ ] `docs/manual-test-plan.md` -- MT-5 rows for 360 × 560, 320 × 568 and 180 × 320 on `/` and `/hei/`: no horizontal scroll, gutters 16 / 12 / 8px, sheet, heading, gypsophila and text visible, no seal/nav/footer; result column empty for the orchestrator's «kjørt av Claude med Playwright» run. MT-6: forced colours on `/` (1px sheet border, no texture), result empty. New MT-1 row for 1.4b: `/` shows G1.
- [ ] `README.md`, `.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md` -- status line (`/` and test links show G1 until 1.5), folder tree (`static/img/`, `tools/`), image sources line; seed gets `tools/` with a dated change note.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given `uvx --with pillow==13.0.0 python -I tools/prepare_images.py` is run again, when `git status` is checked, then `static/img/` is unchanged.
- Given `/stil/` with a `.paper-sheet` sample added, when it renders, then the sheet shows the same ink text and focus colour as `.surface-cream`.

## Spec Change Log

## Review Triage Log

## Design Notes

- **404 for a code, 200 for `/`:** the visitor sees the same page; the status tells crawlers and link scanners the code is not a page. Rendered as a normal response (`status=404`), so `DEBUG` never shows Django's technical 404 with the URL list.
- **Every code shows G1 until 1.5:** 1.4b has no guest page to resolve to, so calling the resolver would be dead code. 1.5 adds `resolve_code` and keeps G1 as the `None` branch.
- **No favicon on G1:** the seal carries the initials (EXPERIENCE.md G1), so the tab icon would leak them.
- **Golden structure:**
  ```html
  <main class="column private-invitation">
    <div class="paper-sheet private-invitation__sheet">
      <h1 class="private-invitation__heading">Dette er en privat invitasjon</h1>
      <img src="{% static 'img/brudeslor.png' %}" alt="" width="180" height="40" class="private-invitation__flowers">
      <p>Virker ikke lenken din? Ta kontakt med brudeparet direkte.</p>
    </div>
  </main>
  ```

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0
- `uvx --with pillow==13.0.0 python -I tools/prepare_images.py && git status --short static/img` -- expected: no output

**Manual checks:**
- MT-5 (sizes, run afterwards by the orchestrator with Playwright in Edge) and MT-6 in `docs/manual-test-plan.md`.
