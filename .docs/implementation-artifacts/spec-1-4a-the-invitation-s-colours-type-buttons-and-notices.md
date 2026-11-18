---
title: "Story 1.4a: The invitation's colours, type, buttons and notices"
type: 'feature'
created: '2026-11-18'
status: 'ready-for-dev'
route: 'dispatch'
review_loop_iteration: 0
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
- [ ] `static/fonts/` -- `imperial-script-400.woff2`, `eb-garamond-roman.woff2`, `eb-garamond-italic.woff2` (the variable `wght` fonts, declared `font-weight: 400 800`), `OFL.txt` per family, and `README.md` with source URLs and the exact `uvx --from "fonttools[woff]" pyftsubset …` commands -- UX-DR2, AD-15.
- [ ] `static/css/site.css` -- `@font-face`; `:root` tokens; base type; `.button` + `--secondary`, `--on-green`, `--destructive`; `.surface-cream` (flat `panel-cream`, sets `--focus-color`); `.notice` + four variants; `forced-colors` and `prefers-reduced-motion` blocks -- UX-DR1, 2, 15, 17, 53, 54.
- [ ] `wedding/templates/wedding/base.html` -- doctype, `lang="nb"`, viewport and color-scheme meta, CSS link via `{% static %}`, `title`/`content` blocks.
- [ ] `wedding/templates/wedding/components/notice.html` -- the include from the matrix.
- [ ] `guests/views.py`, `guests/urls.py`, `guests/templates/guests/style_sample.html`, `config/urls.py` -- `/stil/` sample page, included only when `settings.APP_ENV == "local"`; Norwegian sample texts from EXPERIENCE.md (e.g. «Obs: Svaret er ikke sendt ennå.»); a jump link at the top to a section further down, so MT-3 (smooth vs instant jump) can be checked on it.
- [ ] `tests/test_design_system.py` -- every DESIGN.md colour, spacing and radius token present with the same value (parsed from the frontmatter); no `outline: none|0`; no `@keyframes`; `scroll-behavior` only under `no-preference`; every `font-size` in rem; font files exist and every `url()` points to a local file; base template renders `lang="nb"` and the color-scheme meta; every matrix row.
- [ ] `docs/manual-test-plan.md` -- MT-2 forced colours (Windows contrast theme): button outlines, notice rules, focus ring visible; MT-3 reduced motion; MT-4 fonts show æ ø å and lining figures.
- [ ] `pyproject.toml`, `ARCHITECTURE-SPINE.md`, `README.md` -- djLint note removed; seed updated; README status line, folder note and fonts licence line.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given the site in a browser with network blocked except 127.0.0.1, when a page using the base template loads, then EB Garamond and Imperial Script render (no fallback) and no request leaves the site.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

Templates live in `wedding/templates/` because guests, dashboard and `wedding/rsvp/` all extend the same base and use the same notice, while `guests` and `dashboard` must not import each other. The notice icons are the approved mockup's SVG glyphs, not illustrations: DESIGN.md › Notice fixes their shapes, and the «never draw in code» rule covers flowers, lace, seals and programme icons.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0

**Manual checks:**
- MT-2 to MT-4 in `docs/manual-test-plan.md`.
