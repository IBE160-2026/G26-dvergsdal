---
title: "Story 1.4a: The invitation's colours, type, buttons and notices"
type: 'feature'
created: '2026-11-18'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'bc8399ecd4cd8f3d92aece313a0d9d3416b75fa2'
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** No page can look like the invitation yet: there is no stylesheet, no fonts, no base template and no button or notice styles for Stories 1.4b–1.8 to build on (NFR-5, UX-DR1, UX-DR2, UX-DR15, UX-DR17, UX-DR53, UX-DR54).

**Approach:** One stylesheet with every DESIGN.md token as a custom property, self-hosted WOFF2 fonts, a shared base template, the four buttons and a notice include, proved by tests that read the CSS and render the templates.

## Boundaries & Constraints

**Always:** Token names and values exactly as DESIGN.md frontmatter (`--color-<name>`, `--space-<name>`, `--radius-<name>`); type in `rem`, body 1.25rem (20px), `font-variant-numeric: lining-nums`. `color-scheme: light only` in CSS and a `<meta name="color-scheme">` in the base template; `<html lang="nb">`. Focus: 3px outline at 3px offset on `:focus-visible` and `:active`, colour from a `--focus-color` property (`focus-on-green` by default, `focus-on-panel` inside cream surfaces). Notice: 4px left rule in `currentColor`, 22px inline-SVG icon (`aria-hidden`, shape per variant: check, circle «!», triangle «!», «i»), prefix «Feil:» (error) and «Obs:» (warning) only; no live region by default, `live=True` gives `role="status"` (error: `role="alert"`); never dismisses itself. Smooth scroll only inside `@media (prefers-reduced-motion: no-preference)`. Fonts: Imperial Script and EB Garamond (roman and italic, 400–600) from the OFL sources in google/fonts, subset to Latin with æ ø å, layout features kept (`lnum`, `tnum`, small caps), OFL licence committed beside them. Docstrings and CSS section comments name UX-DR/NFR.

**Decision (Rikke, 2026-11-18):** a sample page at `/stil/` shows the colours, fonts, the four buttons on cream and on green and the four notices, so Rikke and the examiner can see them and run the forced-colours check before Story 1.5. Its URL exists only when `APP_ENV` is `local`; it holds no personal data and is listed in the README.

**Never:** no `outline: none`/`outline: 0`, no `@keyframes` or self-running motion, no external font or CSS URL, no px font sizes, no notice auto-hide, no JS. Not in this story: paper texture, sheet edge, images and the private page (1.4b), privacy headers (1.4c), nav bar, hero and page layouts (1.5–1.7), the «Sender …» busy state (2.6a), form fields and choice controls (2.1+).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Notice at load | include with `variant="error"`, text | rule, triangle icon, «Feil:» prefix, no `role`/`aria-live` | N/A |
| Notice added later | `variant="error"`, `live=True` | as above plus `role="alert"`; other variants `role="status"` | N/A |
| Info / success | `variant="info"` or `"success"` | own icon, no prefix | N/A |
| Unknown variant | `variant="oops"` | renders as info | N/A |
| Sample page, local | GET `/stil/`, `APP_ENV` local | 200, base template, every button and notice variant | N/A |
| Sample page, production | URLconf loaded with `APP_ENV=production` | `/stil/` gives 404 | N/A |

</frozen-after-approval>

## Code Map

- `config/settings.py:30` -- `APP_ENV` (local/production); `TEMPLATES` uses `APP_DIRS=True`, `DIRS=[]`; `STATICFILES_DIRS=[BASE_DIR/"static"]`, WhiteNoise in middleware. No change needed for app templates.
- `config/urls.py` -- `urlpatterns = []`; docstring says pages arrive in 1.4b/1.5.
- `static/{css,fonts,img,js}/.gitkeep` -- empty folders; replace the css and fonts `.gitkeep` with real files.
- `pyproject.toml` `[tool.djlint]` -- `allow_empty_input = true` with a comment «until Story 1.4a»; remove both once templates exist.
- `docs/manual-test-plan.md` -- table `| Id | Story | Steg | Forventet resultat | Dato | Resultat |`, Norwegian; next id MT-2.
- `ARCHITECTURE-SPINE.md` › Structural Seed (line ~297) -- add `wedding/templates/` with a dated change note.
- `.../ux-designs/.../mockups/key-form-steps.html:117-121,176,389` -- approved notice CSS and the inline SVG `<symbol>` icons to reuse; `mockups/paper-ceremony-5.html` -- token CSS reference.
- DESIGN.md frontmatter `colors`, `spacing`, `rounded`, `typography`, `components.button-*`, `focus-ring`, `notice`; Components table rows Primary/Secondary/Destructive/Outlined-on-green button, Focus ring, Notice. EXPERIENCE.md:196 (notice live-region rule), :326 (forced colours), :329 (motion).

## Tasks & Acceptance

**Execution:**
- [x] `static/fonts/` -- `imperial-script-400.woff2`, `eb-garamond-roman.woff2`, `eb-garamond-italic.woff2` (the variable `wght` fonts, declared `font-weight: 400 800`), `OFL.txt` per family, and `README.md` with source URLs and the exact `uvx --from "fonttools[woff]" pyftsubset …` commands -- UX-DR2, AD-15.
- [x] `static/css/site.css` -- `@font-face`; `:root` tokens; base type; `.button` + `--secondary`, `--on-green`, `--destructive`; `.surface-cream` (flat `panel-cream`, sets `--focus-color`); `.notice` + four variants; `forced-colors` and `prefers-reduced-motion` blocks -- UX-DR1, 2, 15, 17, 53, 54.
- [x] `wedding/templates/wedding/base.html` -- doctype, `lang="nb"`, viewport and color-scheme meta, CSS link via `{% static %}`, `title`/`content` blocks.
- [x] `wedding/templates/wedding/components/notice.html` -- the include from the matrix.
- [x] `guests/views.py`, `guests/urls.py`, `guests/templates/guests/style_sample.html`, `config/urls.py` -- `/stil/` sample page, included only when `settings.APP_ENV == "local"`; Norwegian sample texts from EXPERIENCE.md (e.g. «Obs: Svaret er ikke sendt ennå.»); a jump link at the top to a section further down, so MT-3 (smooth vs instant jump) can be checked on it.
- [x] `tests/test_design_system.py` -- every DESIGN.md colour, spacing and radius token present with the same value (parsed from the frontmatter); no `outline: none|0`; no `@keyframes`; `scroll-behavior` only under `no-preference`; every `font-size` in rem; font files exist and every `url()` points to a local file; base template renders `lang="nb"` and the color-scheme meta; every matrix row.
- [x] `docs/manual-test-plan.md` -- MT-2 forced colours (Windows contrast theme): button outlines, notice rules, focus ring visible; MT-3 reduced motion; MT-4 fonts show æ ø å and lining figures.
- [x] `pyproject.toml`, `ARCHITECTURE-SPINE.md`, `README.md` -- djLint note removed; seed updated; README status line, folder note and fonts licence line.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given the site in a browser with network blocked except 127.0.0.1, when a page using the base template loads, then EB Garamond and Imperial Script render (no fallback) and no request leaves the site.

## Implementation Notes

- **Font sources:** google/fonts at commit `7af0d90b4d532ffa4b041937b560c6df4e7b1e95` (SHA-256 of the downloaded TTFs checked against that commit). Unicode range = Google Fonts' «latin» set plus U+2190–2193 (for «← Tilbake til invitasjonen»); `--layout-features='*'` keeps `lnum`, `tnum`, `smcp`, `c2sc` and the rest. Sizes: Imperial Script 35 KB, EB Garamond roman 114 KB, italic 129 KB. Imperial Script has no arrow glyph; it is only used for the names.
- **Licence file names:** two `OFL.txt` cannot share `static/fonts/`, so they are `imperial-script-OFL.txt` and `eb-garamond-OFL.txt`.
- **Typography tokens:** the Approach says «every DESIGN.md token as a custom property», so besides colours, spacing and radii the stylesheet also has `--font-size-<role>` (rem), `--line-height-<role>`, `--letter-spacing-<role>` where DESIGN.md gives one, and `--font-weight-<role>` only where the weight is not 400. The test checks all of them against the frontmatter.
- **Sample-page layout in its own file:** `static/css/style-sample.css`, loaded only by `/stil/` through the base template's `head` block, so the real stylesheet carries no sample-only rules and the swatches need no inline `style` attributes.
- **`/stil/` condition lives in `guests/urls.py`:** `config/urls.py` always includes `guests.urls` (the guest pages will live there), and `guests/urls.py` adds `/stil/` only when `APP_ENV` is `local`. Side effect: with a non-empty URLconf, Django no longer shows its «install worked» page at `/`; `/` and the seed test links now show Django's 404 page until Story 1.4b/1.5. README updated; MT-1's recorded expected result («Djangos startside») is history and was left as is.
- **`:active` focus ring** is limited to `a, button, input, select, textarea, summary` (with `:where()`), because browsers also mark the ancestors of a pressed element as `:active`, which would draw a ring round the whole page on every tap.
- **Test warning filter:** WhiteNoise warns that `staticfiles/` is missing when the test client first runs the middleware; `pyproject.toml` ignores that one warning, since only `collectstatic` creates the folder.
- **Verified in a browser (headless Chrome, 600 px wide, all hosts except 127.0.0.1 unresolvable):** both fonts render, æ ø å and small capitals show, and the server log shows only local requests (page, two stylesheets, three fonts). MT-2 to MT-4 still need a person (Windows contrast theme, reduced-motion setting).

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-18): Blind Hunter (B), Edge Case Hunter (E), Verification Gap (V).

| # | Layer | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|---|
| 1 | V | `/stil/` test never checks that `style-sample.css` is loaded through the base template's `head` block | low | Pre-verified: no test references the sample stylesheet or the block; renaming the block passed every test | patch |
| 2 | V, B, E | MT-1's expected result («Djangos startside») can no longer be reproduced: `/` now gives Django's 404 | low | `config/urls.py` always includes `guests.urls`, so the URLconf is never empty | patch (new MT-1 row, history kept) |
| 3 | B | Spec says `in-review`, sprint status `in-progress` | low | Orchestrator sets `review` at this step, as in Story 1.3 | patch (orchestrator) |
| 4 | B | Spec Change Log empty and ticked tasks say «`OFL.txt` per family» | low | Fix edits this build's spec; deviations are in Implementation Notes | reject |
| 5 | B, E | `/stil/` toggled at import time; test reloads URLconf; an ambient `APP_ENV` flips the local test | low | Test restores the URLconf in `finally`; `APP_ENV=production` refuses to start without a real `SECRET_KEY` and hosts, so CI cannot hit it; the fix is a redesign | reject |
| 6 | B, E | `COLOUR_TOKENS` and `.sample__chip--*` can drift from DESIGN.md | low | Three hand-written lists, no check; a test is a direct addition | patch |
| 7 | B | Token tests one-way; a parser that drops keys shrinks the tests silently | low | Parametrised from the parser's output with no count; reverse check is a direct addition | patch |
| 8 | B, E | Component values (button padding, notice gap) not checked against DESIGN.md `components`; on-green `padding-block` 4px vs DESIGN «0 14px» | low | DESIGN `components` are free-form strings; on-green height is set by `min-height: 44px`, so the 4px is invisible on one line | reject |
| 9 | B, E | `test_four_buttons_are_styled` matched substrings (`.button` in `.button--secondary`) and no declarations | medium | Deleting the base `.button` rule passed; trivial tests are a warning sign in the grading guide | patch |
| 10 | B | The `:active` limit (fix of the whole-page ring) has no test | low | A bare `:active` passed the focus test | patch |
| 11 | B | Warning filter hides «No directory at» from any source | low | Direct narrowing; WhiteNoise's `stacklevel=3` attributes it to `django.core.handlers.base` | patch |
| 12 | B | Font sources cannot be re-checked: no hashes, no download step, bash-only commands | low | `static/fonts/README.md` had none; recording them is direct | patch |
| 13 | B | README folder tree misses `style-sample.css` | low | Direct correction | patch |
| 14 | B | Notice icon fixed at 22px does not grow with text size | low | 22px is the DESIGN.md `notice.icon` value and the spec's Always | reject |
| 15 | B, E | Empty `text` renders a bare «Feil:» or an empty notice | low | Only reachable by a template bug; a guard adds a branch | reject |
| 16 | B | No `.logs/` entry for this work | false | Written at the end of the session by `sesjonslogg`, as CLAUDE.md requires | reject |
| 17 | E | Include without `only` inherits a truthy `live`/`variant` from the page | low | Django `include` passes the parent context; `only` is a direct fix | patch |
| 18 | E | A `live=True` notice inserted with its text may not be announced | maybe-false | No JS inserts notices yet; settled by a screen-reader test of the first in-page insertion | defer (unverified medium) |
| 19 | E | Notice on the green page has dark text on olive | low | DESIGN and the include's comment place notices on cream; no page does otherwise | reject |
| 20 | E | `.button--on-green` on a cream surface is cream on cream | low | DESIGN.md › Outlined button: «On a cream sheet the same shape is drawn in ink»; one-line rule | patch |
| 21 | E | Disabled buttons keep pointer and hover | low | DESIGN defines no disabled button; busy state is Story 2.6a | reject |
| 22 | E | Latin Extended-A letters (ł, č) fall back to Georgia | low | Cosmetic in a rare name; needs re-subsetting all fonts | reject |
| 23 | E | `outline: 0px` passed the outline test (`\b` fails after `0px`) | low | Regex fault; direct fix | patch |
| 24 | E | `assert sizes` fails any future stylesheet without font sizes | low | Direct fix: apply to `site.css` only | patch |
| 25 | E | `_without_block` uses `replace`, which could cut identical text elsewhere | low | Needs a byte-identical copy of the block body; unlikely, fix adds code | reject |
| 26 | E | «Surfaces» section and `style-sample.css` header name no UX-DR/NFR | low | Spec Always requires it; direct addition | patch |

**After patches:** 320 tests pass; Ruff, djLint and `makemigrations --check` clean. The implementer broke a bare `:active`, `outline-width: 0px`, the primary background and the `head` block name in turn, and each was caught by its new test.

## Design Notes

Templates live in `wedding/templates/` because guests, dashboard and `wedding/rsvp/` all extend the same base and use the same notice, while `guests` and `dashboard` must not import each other. The notice icons are the approved mockup's SVG glyphs, not illustrations: DESIGN.md › Notice fixes their shapes, and the «never draw in code» rule covers flowers, lace, seals and programme icons.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0

**Manual checks:**
- MT-2 to MT-4 in `docs/manual-test-plan.md`.
