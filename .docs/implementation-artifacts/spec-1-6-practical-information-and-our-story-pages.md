---
title: 'Story 1.6: Practical information and Our story pages'
type: 'feature'
created: '2026-11-20'
status: 'done'
baseline_revision: 'd24e212c40aa6d13ff3741d8cfe3b047e2741d55'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/info-praktisk.html'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/info-om-oss.html'
warnings:
  - multiple-goals
  - oversized
deferred: []
---

<intent-contract>

## Intent

**Problem:** `/<code>/praktisk/` and `/<code>/historie/` show only the info-page frame from Story 1.5 (back link, title, back button), so a guest cannot read how to get there, where to sleep, the house rules or the couple's story (FR-10 page, FR-11, AD-17, UX-DR12, UX-DR14).

**Approach:** Fill the two templates with the approved mockups' content as template text: Praktisk gets «Hopp til» jump links and seven info sheets with the mockup placeholders (real text in Story 7.4); Vår historie gets one story sheet with the couple's approved text in nine chapters and the signature. CSS for jump links, info sheet and story sheet from DESIGN.md. No view, URL or query changes.

## Boundaries & Constraints

**Always:**
- **Frame:** both pages keep `info_page.html` (back link with `<span aria-hidden="true">←</span>`, `h1`, bottom button, nav `aria-current`). Give the `h1` `id="sidetittel"`. Views, routes and the 2-SELECT count are unchanged; text lives in the templates (AD-17), dates as plain spaces (no `&nbsp;`).
- **Praktisk order:** `h1` → `<nav class="jump-links" aria-label="Hopp til">` holding three `ul`s: [Vielsen `#vielsen`, Hardingasete `#stedet`], [Komme dit `#komme-dit`, Husregler `#husregler`, Antrekk `#antrekk`], [Ta med `#ta-med`, Området `#omradet`] (EXPERIENCE.md:113). Every `li` but each list's first starts with `<span class="jump-links__dot" aria-hidden="true">·</span>`; no `·` in the nav outside such a span. Then seven `<section class="paper-sheet info-sheet" id="…" tabindex="-1" aria-labelledby="…-overskrift">`, each with `<h2 id="…-overskrift">`: Vielsen, Hardingasete og hyttene, Hvordan komme seg dit, Husregler, Antrekk, Ta med, Området rundt. Ids exactly the mockup's.
- **Praktisk text:** each section's text is `mockups/info-praktisk.html:118-182` word for word (placeholders in square brackets kept), `<b>` as `<strong>`, «programmet» linking to `{% url 'guests:programme' code %}`. Photos in a 220px lace frame (`.lace-frame.lace-frame--info`, photo `width="197" height="190"`, lace `blonde.png` `alt=""` `width="220" height="213"`): Vielsen `sted-kirka.jpg` (alt «Strandebarm kirke, en hvit trekirke med fjell bak.», `object-position: 76% 50%`), Hardingasete `sted-tunet.jpg` (alt «Tunet på Hardingasete med de gamle husene.», existing `.lace-frame__photo--tunet`), Området `sted-omradet.jpg` (alt «Fjorden og fjellene i Hardanger.»). The Vielsen images load eagerly, all later images `loading="lazy"`.
- **Vår historie:** no jump links. One `<section class="paper-sheet story-sheet" aria-labelledby="sidetittel">`: lace frame (same sizes) with `oss-utsikt.jpg` (alt «Rikke og Valdemar med utsikt.», eager) and `blonde.png`; then the nine chapters of `mockups/info-om-oss.html:132-149`, each an `h2` time · place line with the dot as `<span aria-hidden="true">·</span>` followed by its `p`; then `<p class="story-sheet__closing">` (line 150) and `<p class="story-sheet__signature">Rikke &amp; Valdemar</p>` last. The text is the approved mockup's (Rikke's Word file with her approved corrections: «moro», «At det var», comma and full stop in the Annecy parenthesis; «[stilling]» kept, Rikke's choice, open in `.logs/rikke/issues.md`).
- **CSS** (`static/css/site.css`, values from DESIGN.md `jump-links`, `info-sheet`, `story-sheet`, `lace-frame.widthOnInfoSheet`; mockup values where DESIGN has none): jump links `margin: 10px 4px 0`, centred flex-wrap lists without bullets, dot `padding: 0 7px`, links `min-height: var(--space-target-min)`, jump-links type tokens, `font-variant-caps: all-small-caps`, no underline. Info sheet `margin-top: 20px; padding: 22px 22px 12px`; `h2` italic, `padding-bottom: 8px`, `border-bottom: 1px solid rgba(59, 55, 47, 0.35)`, `margin: 0 0 10px`; `p`/`ul` `margin: 0 0 10px`, `ul` `padding-left: 22px`; `strong` `font-weight: var(--font-weight-label)`. Story sheet `margin-top: 20px; padding: 22px 22px 18px`; chapter `h2` body size and line height, italic, `margin: 18px 0 4px` (first: `2px` top); `p` `margin: 0 0 12px`; closing italic centred `margin: 18px 4px 0`; signature `var(--font-script)`, signature tokens, centred, `margin: 18px 0 2px`. `.lace-frame--info { width: 220px; margin: 6px auto 14px }` (story: `4px auto 16px`). `.info-sheet:focus` gets `outline-color: transparent` like `#svar:focus`. Below 260px: info and story sheets take `--space-gutter-narrow` inline padding, each jump link on its own line and the dots `display: none`. No `scroll-margin` anywhere (html `scroll-padding-top` already clears the bar).
- Docstrings, template comments and CSS section comments name FR/NFR/UX-DR/AD ids.

**Never:** no «Åpne veibeskrivelse i kart» (no real address yet and no map service decided: deferred to 7.4); no «Godt å vite», prices or `Settings` reads on these pages (1.7); no deg/dere logic (placeholder text stays as written until 7.4); no Programme content (1.7); no new or changed image files; no JavaScript; no text from `ux/innhold/programmet-og-praktisk.md` (7.4); no running a browser.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Praktisk | seed; GET `/test-sigmund0000000000/praktisk/` | 200, 2 SELECTs; jump-links nav after `h1`, before the first section; 7 lists items/hrefs as above; sections and `h2`s in order; each section's text = mockup's (map button excluded); img set {sted-kirka, sted-tunet, sted-omradet, blonde} | N/A |
| Jump target | any `#id` in the nav | a `section` with that `id`, `tabindex="-1"`, `aria-labelledby` = its `h2` id | N/A |
| Vår historie | GET `/test-sigmund0000000000/historie/` | 200, 2 SELECTs; no «Hopp til»; one story section labelled by `sidetittel`; 9 `h2`s in order, each with one hidden dot; section text = mockup's; signature last; img set {oss-utsikt, blonde} | N/A |
| Unknown code | `/AAAAAAAAAAAAAAAAAAAAAA/praktisk/`, `/hei/historie/` | 404 G1, unchanged (existing test) | N/A |

</intent-contract>

## Code Map

- `guests/templates/guests/practical.html:1-7`, `our_story.html:1-7` -- frame-only templates; comments say «arrives with Story 1.6». Fill `info_content`.
- `guests/templates/guests/info_page.html:15-18` -- the `h1`; add `id="sidetittel"`. `:2-10` comment.
- `guests/templates/guests/front_page.html:74-95` -- lace-frame markup to copy (photo then lace, `width`/`height`, `loading`).
- `guests/views.py:112-118` -- `INFO_PAGES` comment («until Stories 1.6 and 1.7»); `:121-130` `info_page` docstring. No logic change.
- `static/css/site.css:1-13` header comment («content arrives in 1.6 and 1.7»); `:259-262` `.small-caps`; `:781-813` lace frame (136px base, `--tunet`); `:848-850` `#svar:focus`; `:881-910` info frame; `:949-959` the 259.98px block; `:583-601` sticky query (do not touch). Tokens exist: `--font-script`, `--font-size-signature`, `--line-height-signature`, `--font-size-jump-links`, `--line-height-jump-links`, `--letter-spacing-jump-links`, `--font-weight-label`, `--space-target-min`, `--space-gutter-narrow`.
- `static/img/README.md` -- already lists sted-kirka, sted-tunet, sted-omradet, oss-utsikt (sizes 440×290, 440×661, 440×235, 440×664) and blonde (320×309).
- `tests/test_info_pages.py:49` -- `h1` regex `<h1 class="info-page__title">` breaks with the new id; `:1-10` docstring says content arrives in 1.6.
- `tests/test_design_system.py:94-160` helpers `_css`, `_block`, `_declarations`, `_bodies`; `:520-542` sticky test forbids `scroll-margin` anywhere; `:637-641` `#svar:focus` test (keep passing).
- `tests/helpers.py:25-27` `page_text`; `tests/conftest.py` fixtures `seeded`, `local_env`, `assert_loads_only_own_host`.
- `tests/test_front_page.py:40,163` -- no-write test already covers both paths.
- `docs/manual-test-plan.md` -- last id MT-15.
- `README.md:9` status line («uten innhold ennå … story 1.6 og 1.7»).
- Planning: `EXPERIENCE.md:182` (Jump links row still says `scroll-margin-top`, dots as CSS), `:186` (Info sheet row, map link); `DESIGN.md:557` (info pages item 4 lists the map button), `:589` (Narrow widths); `.docs/implementation-artifacts/deferred-work.md`.

## Tasks & Acceptance

**Execution:**
- [x] `guests/templates/guests/info_page.html` -- `id="sidetittel"` on the `h1`; comment -- UX-DR14.
- [x] `guests/templates/guests/practical.html` -- jump links and seven info sheets per Boundaries; comment names FR-10, FR-11, AD-17, UX-DR12 and that Story 7.4 replaces the placeholders -- FR-10.
- [x] `guests/templates/guests/our_story.html` -- story sheet per Boundaries; comment names UX-DR14, AD-17 and the text source -- UX-DR14.
- [x] `guests/views.py` -- `INFO_PAGES` comment and `info_page` docstring: Praktisk and Vår historie filled (1.6), Programmet in 1.7.
- [x] `static/css/site.css` -- sections «Jump links», «Info sheet», «Story sheet», `.lace-frame--info` and photo modifier for the church, `.info-sheet:focus`, additions to the 259.98px block; header comment -- UX-DR12, UX-DR14, UX-DR30, NFR-5.
- [x] `tests/test_practical_and_story_pages.py` -- every matrix row; text equality by `page_text` against the mockup files (parse `<section class="PART" id="…">…</section>` and `<section class="sheet story">…</section>`, drop the mockup's `<a class="small-btn"…>…</a>`); jump-link structure, dots `aria-hidden`, first `li` of each list without a dot; every target section attributes; images with `alt`, `width`, `height` and the eager/lazy rule; programme link in Vielsen; one `h1`; nine chapter `h2`s with one hidden dot each; signature text and position; back-link arrow hidden.
- [x] `tests/test_info_pages.py` -- `h1` regex tolerates the id; docstring updated.
- [x] `tests/test_design_system.py` -- jump links: small caps, tokens, no underline, 44px; dots hidden and links stacked inside the 259.98px block; `.info-sheet:focus` transparent outline; `var(--font-script)` used only by `.display-names` and `.story-sheet__signature`; info hairline value.
- [x] `docs/manual-test-plan.md` -- rows below (Norwegian, «Kjøres av Claude med Playwright mot Edge», date and result cells empty). Server: `uv run manage.py seed_testdata`, `uv run manage.py runserver`; P = `http://127.0.0.1:8000/test-sigmund0000000000/praktisk/`, H = `…/historie/`; measure after `document.fonts.ready` and every `main img` `complete`, `reducedMotion: 'reduce'`.
  - MT-1 (1.6): README steps, then P shows «Hopp til» and the seven sheets, H the story sheet with the signature.
  - MT-16 (jump links): at 360 × 640, for each `nav[aria-label="Hopp til"] a`: click from the top of P → `location.hash` = its href, `document.activeElement.id` = the target id, `#<id> h2` `getBoundingClientRect().top` ≥ `.nav-bar` bottom and < `innerHeight`. From the top, `Tab` to `a[href="#husregler"]` (its computed `outline-style` `solid`, `outline-color` `rgb(245, 238, 223)`) and `Enter` → same checks. At 360 × 380 (bar not sticky) click `a[href="#antrekk"]`: `#antrekk h2` top within 0…`innerHeight`.
  - MT-17 (widths): P and H at 360 × 640, 320 × 568, 180 × 320: `document.documentElement.scrollWidth` ≤ `innerWidth`; every `.lace-frame` right ≤ its sheet's right; at 180 × 320 every `.jump-links__dot` computed `display` `none` and the seven jump-link `li` have increasing `top`; `.story-sheet__signature` `scrollWidth` ≤ `clientWidth`.
  - MT-18 (screen readers): `locator('nav[aria-label="Hopp til"]').ariaSnapshot()` and every `.story-sheet h2` `ariaSnapshot()` contain no «·»; `.info-page__back` `ariaSnapshot()` contains no «←» on P and H; every `.jump-links__dot` and `.story-sheet h2 span` has `aria-hidden="true"`.
- [x] `README.md:9` -- status: Praktisk informasjon and Vår historie have content (1.6; placeholders in Praktisk until 7.4), Programmet still frame only (1.7).
- [x] `EXPERIENCE.md:182`, `:186`; `DESIGN.md:557`, `:589` -- dated notes (2026-11-20, Story 1.6): targets cleared by `html` scroll-padding only; dots are `aria-hidden` spans, since CSS `content` is read by some screen readers; below 260px one jump link per line without dots, so a dot never starts a line; the map button waits for Story 7.4 (real address) and a decision on the map service (AD-15, privacy page).
- [x] `.docs/implementation-artifacts/deferred-work.md` -- entry for Story 7.4: add «Åpne veibeskrivelse i kart» once the address exists; choose the map service, `rel="noreferrer"`, and mention it on the privacy page (7.1).

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given P and H for a seeded link, when fetched, then the top link and the bottom button both point to `/<code>/`, the arrow is `aria-hidden`, and no `<script` or external load appears (FR-11).
- Given P, when a jump link is followed by click or keyboard, then focus is on its section and the heading is below the sticky bar (UX-DR12; MT-16).
- Given `docs/manual-test-plan.md`, when read, then MT-1 (1.6) and MT-16 to MT-18 hold the steps above with empty result cells.

## Spec Change Log

## Review Triage Log

### 2026-11-20 — Review pass
- verdicts: 24 findings — high 0, medium 4, low 12, false 8, maybe-false 0
- findings:
  - `[false]` `[reject]` AC2 (focus lands, heading below the bar) is only specified, not observed (intent-alignment) — MT-16 run by Claude with Playwright in Edge: all seven links by click, #husregler by Tab + Enter, and #antrekk at 360 × 380 landed with focus on the section and the heading at 98px under a 64px bar.
  - `[false]` `[reject]` AC3's screen-reader hiding is only checked in markup (intent-alignment) — MT-18 read `ariaSnapshot()` in Edge: no «·» and no «←».
  - `[low]` `[reject]` The Imperial Script signature is checked as CSS text, not as the rendered font (intent-alignment) — the font is self-hosted and checked by MT-4 (1.4a); the screenshots show the script.
  - `[false]` `[reject]` The text oracle drops the mockup's map button (intent-alignment) — deliberate, documented in DESIGN.md, EXPERIENCE.md and deferred-work.md; the AC never names the button; Story 7.4 now has the criterion.
  - `[false]` `[reject]` The story text is compared with the mockup, not the .docx (intent-alignment) — the mockup is the approved text with Rikke's three corrections (spec Design Notes).
  - `[false]` `[reject]` The bar is cleared only where it is sticky (intent-alignment) — where it is not sticky nothing covers the heading; MT-16 at 360 × 380 passed.
  - `[false]` `[reject]` MT rows for 1.6 unrecorded (intent-alignment) — run and recorded.
  - `[false]` `[reject]` Browser-only behaviour rests on unrun manual tests (verification-gap) — MT-1 (1.6), MT-16, MT-17 and MT-18 run in Edge and recorded; a probe across 260–360px then found the jump-link wrap below.
  - `[low]` `[patch]` MT-16/17/18 wait for every `main img` to be `complete`, which never happens for lazy images (blind) — the rows now wait for the eager images only.
  - `[medium]` `[patch]` A middle dot can start a line between 260 and ~340px (blind) — confirmed in Edge at every width from 260 to 360px («· Antrekk» alone on a line); jump-link values matched to the mockup and the stacking breakpoint moved to an em-based width; MT-17 checks 260–480px.
  - `[low]` `[patch]` EXPERIENCE.md's RSVP sheet row still says `scroll-margin-top` (blind) — fixed with a dated note.
  - `[low]` `[patch]` Story 7.4 in epics.md is not updated for the deferred map button (blind) — a 7.4 criterion added with a dated note.
  - `[false]` `[reject]` Tasks unticked, sprint-status backlog, MT cells empty (blind) — the finalize step.
  - `[low]` `[patch]` A test docstring promises a du/dere check it never makes (blind) — the test now compares the Praktisk text for a one-person and a several-person household.
  - `[low]` `[patch]` Nothing stops square-bracket placeholders reaching real guests (blind) — a Story 7.4 criterion: a test fails while guest pages contain «[…]».
  - `[low]` `[patch]` The info-sheet hairline hard-codes the ink colour (blind) — derived from the ink token; the test simplified.
  - `[low]` `[patch]` `.jump-links li { display: inline-flex }` computes to `flex` (blind) — written as `flex`.
  - `[low]` `[patch]` New tests overlap and a string is defined twice (blind) — duplicates removed.
  - `[low]` `[patch]` An assertion depends on `&amp;` staying unescaped (blind) — asserts on decoded text.
  - `[low]` `[patch]` The touch half of the jump-link criterion is not tested (blind) — Claude ran `tap()` with `hasTouch` in Edge (#ta-med: focus on the section, heading at 98px); MT-16 gets the touch step.
  - `[medium]` `[patch]` Line 2 needs 328px but has 320px at 360px, so «· Antrekk» wraps (edge-case) — same root cause as the dot row above.
  - `[medium]` `[patch]` With larger text the px breakpoint lets lists wrap mid-line (edge-case) — the stacking breakpoint is em-based.
  - `[medium]` `[patch]` Claim: a dot never starts a line (edge-case, claim) — same as the dot row above.
  - `[low]` `[patch]` Claim: three lines of about 132px at 360px; the build gives four (edge-case, claim) — same as the dot row above.

## Design Notes

- **Text source.** The mockups are Rikke's approved text, so tests compare against them; the Word file (`ux/innhold/Vår historie.docx`) equals `info-om-oss.html` except the three corrections she approved (memlog 2026-11-15). Comparing to the mockup proves «their own text» without retyping it in a test.
- **Dots in HTML, not CSS.** The mockup draws the jump-link dot with `li + li::before`; generated content is read aloud by some screen readers, and the AC asks for hidden dots, so they are `aria-hidden` spans, as in the hero's place line.
- **Jump links stay inline in practical.html.** Story 1.7 is the second user; it may move them to an include then.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0
- `git status --short static/img` -- expected: no output

**Manual checks:**
- MT-1 (1.6) and MT-16 to MT-18 are run afterwards by the orchestrator with Playwright in Edge.

## Auto Run Result

Status: done

**Summary:** Praktisk informasjon has the «Hopp til» jump links (three balanced lines from 22.5em, one link per line without dots below) and seven info sheets in the AC order with the mockup's placeholder text in the templates; each sheet is a focusable jump target cleared by the sticky bar's scroll padding. Vår historie has one story sheet with the couple's photo in the lace frame, nine chapters with italic time · place `h2`s, the closing line and the Imperial Script signature. Dots and the back arrow are hidden from screen readers. The map button moved to Story 7.4.

**Files changed:**
- `guests/templates/guests/practical.html`, `our_story.html`, `info_page.html` — the two pages and the titled `h1`.
- `static/css/site.css` — jump links, info sheet, story sheet, info lace frame, `--rgb-ink`, narrow widths.
- `tests/test_practical_and_story_pages.py`, `tests/test_info_pages.py`, `tests/test_design_system.py` — text against the mockups, structure, CSS rules.
- `DESIGN.md`, `EXPERIENCE.md`, `epics.md` (Story 7.4), `deferred-work.md`, `README.md`, `docs/manual-test-plan.md` — dated notes, two 7.4 criteria, MT-1 (1.6), MT-16 to MT-18.

**Review:** 15 rows patched (the jump-link wrap found by two reviewers and confirmed in Edge, plus test and document fixes), 0 deferred, 9 rejected with reasons in the triage log.

**Follow-up review recommendation:** false. No high was patched; the medium entries (jump-link wrap and its em-based breakpoint) were re-measured in Edge at 260–480px after the fix, so no unverified risk can be named.

**Verification:** `uv run pytest` 604 passed; ruff and djlint clean; MT-1 (1.6), MT-16 (click, keyboard and touch), MT-17 (sizes and jump-link lines at 260–480px) and MT-18 (accessibility tree) run by Claude with Playwright in Edge after the patches.

**Residual risks:** the Praktisk text is still placeholders with «[…]» until Story 7.4 (which now has a test criterion for that), and the jump-link spacing (5px dot padding, no nav inline margin) differs slightly from the approved mockup because the self-hosted font is wider.
