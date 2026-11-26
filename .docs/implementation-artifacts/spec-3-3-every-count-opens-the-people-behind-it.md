---
title: 'Story 3.3: Every count opens the people behind it'
type: 'feature'
created: '2026-11-26'
status: 'in-progress'
baseline_revision: '72f691d4a8ffe7ebaa52e352e2011953acefaa02'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-3-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md'
warnings: [oversized]
deferred: []
---

<intent-contract>

## Intent

**Problem:** Every count on Oversikt (`/admin/`) is plain text, so Rikke cannot see who the 12 for «Middag fredag» are and cannot trust the numbers she sends to Hardingasete (FR-55, UX-DR41, AD-2, NFR-2).

**Approach:** (1) one registry, `dashboard/counts.py`, names each count once (slug, page title, people or households, the `wedding/rules/summary.py` call that returns its id tuple); (2) Oversikt builds its numbers from the registry and links each count above 0 to `/admin/tall/<slug>/`; (3) that page (A3) lists exactly the tuple's people or households, with the count in its heading, so the number of rows equals the count by construction and by test.

## Boundaries & Constraints

**Always:**
- Every rule, selector, view, template comment and test names its FR/NFR/UX-DR/AD ids. UI text and URLs Norwegian, code and spec English. Breakpoints in `em`, tokens from DESIGN.md, 44px targets, flat green, straight cream `admin-panel`s, no JavaScript.
- A count is `len()` of the id tuple the registry's rule call returns; Oversikt and A3 read the same tuple, so they cannot disagree. Templates, `overview.py` and the A3 view never count, filter or add.
- A count of 0 is plain text with no `<a>` (UX-DR41). A count above 0 is one link whose visible text is the count text and whose `aria-label` begins with that text's row label, for example «Kommer: 9 personer» (WCAG 2.5.3); it is not underlined away (not colour alone) and is at least 44px tall.
- A row with two numbers (persons · households; «3 ja, 2 kanskje») has one link per number above 0, each with its own slug; «kommer» and «kanskje» are separate counts and are never added.
- A3 shows names only (guest name, and for a person the household as `household_names`; for a household the same names). Never allergy details: the allergy list with categories and notes is Story 3.4 (FR-58, AD-18).
- A3 is behind `admin_required` (logged out: 302 to login with `next`); the couple and a helper both open it; the nav marks Oversikt as the open page. `wedding/rsvp/views.py` and `guests/views.py` are not touched; dashboard imports neither `guests` nor `wedding.rsvp`.
- Tests take numbers from `wedding/fixtures/expected.toml` (loaded with `tomllib`) and from the registry, never hard-coded, with the `seeded_with_answers` fixture and Story 3.2's named `SYNNE_UNTIL_7_2` offset where allergy counts are compared (FR-69, AD-16).

**Never:**
- No household page or Gjester list (3.4, 6.3), no address for «Se hva alle har svart» (3.4; it stays plain text), no allergy list (3.4), no «Trenger oppfølging» (6.2), no payments (5.x).
- No count stored, cached or computed in a template; no second copy of a rule; no per-row queries on A3 (names load in two queries); no dead link for 0.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Count above 0 | Couple clicks «9 personer» on Kommer | `/admin/tall/kommer-personer/`: `h1` «Kommer: 9 personer», a list with 9 items in id order, each the guest name and household | — |
| Households count | Clicks «5 husstander» | `h1` «Kommer: 5 husstander», 5 items naming each household | — |
| Count at 0 | Seeded count that is 0 (or no data) | Oversikt shows «0 personer» as plain text, no `<a>`; opening the address directly shows the `h1` with 0 and «Ingen personer.» | — |
| Every slug | Each slug in the registry, seeded data | Rows on A3 equal the Oversikt number and `len` of the rule tuple; known values equal `expected.toml` | — |
| Unknown slug | `/admin/tall/finnes-ikke/` | The couple's own 404 | `Http404` |
| Logged out | GET `/admin/tall/kommer-personer/` | 302 to `/admin/logg-inn/?next=…` | — |
| Helper | Helper opens A3 | Same list, plus the read-only line | — |
| Allergy count | «Nøtter» above 0 | Names only, no category or note on the page | — |

</intent-contract>

## Code Map

- `wedding/rules/summary.py` -- every rule returns a sorted id tuple (`households_by_state`, `people_by_state`, `whole_weekend`, `not_whole_weekend`, `days_only`, `other_days`, `not_staying`, `beds`, `meal_eaters`, `allergy_state_ids`, `allergy_category_ids`, `hike_ids`, `households_by_payment` L158-171). Read-only; reuse, do not change.
- `dashboard/overview.py` -- 250 lines. `Row` (L81), `_progress` (L119), `_when` (L142), `_overnight`, `_meals`, `_allergies`, `_hike`, `_payment` (L199) and `build_overview` (L220) each call a rule and `len()` it. Change: `Row.text` becomes `cells` (a tuple of `Cell(text, slug, count)`); every `len(rule(...))` moves to the registry. Keep labels, order, plurals (`persons`, `households`) and the day sub-row rules (rows only above 0; «Andre kombinasjoner»).
- `dashboard/counts.py` -- New. `Count(slug, title, kind, ids)` with `kind` `"people"` or `"households"` and `ids(facts, statuses)`; `COUNTS` and `count_for(slug)`; the payment `statuses` come from one helper moved out of `_payment` so Oversikt and A3 share it. Slugs ASCII and stable, for example `kommer-personer`, `kommer-husstander`, `hele-helgen`, `maltid-fredag-middag`, `tur-ja`, `tur-kanskje`, `betaling-ikke-betalt`. Titles are the A3 heading label («Kommer», «Allergi: Nøtter», «Middag fredag»).
- `dashboard/selectors.py` -- 100 lines; `guest_facts()`, `household_totals()`. Add `people_behind(ids)` and `households_behind(ids)`: two queries each (guests with their household's guests), returning `Person(name, household)` and `HouseholdRow(names)` in the order of `ids`. Names only.
- `dashboard/views.py` -- `home` (L96) builds the overview; add `count_page(request, slug)` after it: `admin_required`, `require_safe`, `count_for(slug)` or `Http404`, facts, statuses, `ids`, rows, render with `frame(request, "home")`. `dashboard/urls.py` L19-30: add `path("tall/<slug:slug>/", views.count_page, name="count")` above the `<path:rest>` catch-all.
- `dashboard/templates/dashboard/count.html` -- New A3: `h1` «{title}: {count text}», a back link «Tilbake til Oversikt», a `ul` of rows or the empty text. `dashboard/templates/dashboard/overview/_panel.html` and `_progress.html` -- render each cell as a link or plain text through one shared `_cell.html` include (no duplication between the two).
- `static/css/site.css` -- `.overview-row` (L1940-1975), `.overview-row dd` right-aligned, `.admin-readonly` (L1983). Add `.overview-row a` (inline-flex, `min-height: var(--space-target-min)`, underline, focus ring as the other links), `.count-list` and `.count-back` rules; `em` only (`tests/test_form_components.py` bans px breakpoints); no overflow at 180px and 20px text (long names wrap with `overflow-wrap`).
- `tests/test_counts.py`, `tests/test_overview.py`, `tests/test_admin_overview.py`, `tests/test_admin_count_page.py` -- the first and last New. `tests/test_overview.py` L39-100 loads `EXPECTED` and the `facts` fixture; `tests/test_admin_overview.py` L1-60 has `log_in_as`, `couple_page`, `PANELS` and the old «no link in panels» test to rewrite; `tests/helpers.py` `main_html`, `page_text`, `sections_of`, `make_admin`; `tests/conftest.py` `seeded_with_answers`; `tests/test_architecture_imports.py` stays green.
- `docs/manual-test-plan.md` -- MT-71 to MT-74 (L95-98) are the 3.2 format; the next free number is MT-75.
- Read-only: `wedding/fixtures/expected.toml`, `wedding/rules/households.py` `household_names` (L34).

## Tasks & Acceptance

Each group is one commit of about 600 changed lines or fewer (`epic-2-retro-item-12`; keep the triage comment and Spec Change Log).

**Execution:**
- `dashboard/counts.py`, `tests/test_counts.py` -- commit 1: the registry and the shared payment-status helper; test that slugs are unique and URL-safe, every `ids` call returns the same tuple as the rule it wraps on the seed, kind is people or households, `count_for` of an unknown slug fails (FR-55, FR-54, AD-2).
- `dashboard/selectors.py`, `tests/test_overview.py` -- commit 2: `people_behind`, `households_behind`; order equals the ids, names only, a fixed small number of queries (`django_assert_num_queries`), empty ids give an empty result (FR-55, NFR-2).
- `dashboard/overview.py`, `tests/test_overview.py` -- commit 3: rows carry cells with slug and count read from the registry; every number still equals `expected.toml` and each cell's slug opens a registry entry whose tuple length equals the cell count (FR-54, FR-55, UX-DR41, AD-2).
- `dashboard/templates/dashboard/overview/_cell.html`, `_panel.html`, `_progress.html`, `static/css/site.css`, `tests/test_admin_overview.py` -- commit 4: counts above 0 are links with `aria-label`, 0 is plain text, «Se hva alle har svart» stays plain text, no other new `<a>`; the old no-links test rewritten to this rule (UX-DR41, FR-55).
- `dashboard/views.py`, `dashboard/urls.py`, `dashboard/templates/dashboard/count.html`, `tests/test_admin_count_page.py` -- commit 5: A3 and its route; one parametrized test over every registry slug: status 200, rows equal the Oversikt number and the tuple length, and the `expected.toml` value where it lists one (the Synne offset for allergies); unknown slug 404; logged out 302 with `next`; helper sees the line; the nuts page shows no allergy text; zero count shows the empty text (FR-55, UX-DR41, FR-46).
- `docs/manual-test-plan.md` -- commit 6: MT-75 onwards, Norwegian, result cells empty, «Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`)» after `migrate`, `seed_testdata`, `runserver`. Steps: log in as `testpar` / `bryllup-test-2028`; for each link on `/admin/` (collected by selector, numbers read from the link text) open it, read the `h1` count and count the `li` items, expecting equal; a zero count has no `<a>`; the address `/admin/tall/finnes-ikke/` gives the couple's 404; logged out `/admin/tall/kommer-personer/` goes to the login page; keyboard only (Tab reaches each count link in reading order, Enter opens it, Alt+Left returns, focus ring visible); 360 × 640 and 180 × 320 at 16px and 20px text (`scrollWidth` ≤ `innerWidth`, link and back-link targets ≥ 44px).
- `README.md`, `.docs/planning-artifacts/epics.md`, `EXPERIENCE.md`, `DESIGN.md`, `deferred-work.md`, `sprint-status.yaml` -- commit 7: README status line and tree (`counts.py`, `count.html`, new tests); epics 3.3 implementation note (route `/admin/tall/<slug>/`, names only, allergy details wait for 3.4, dated reason); EXPERIENCE A3 states and the Admin summary row note (aria-label, two links per row) and DESIGN the count-link style, each dated; deferred-work: close the 3.3 half of the 3.2 entry and keep «Se hva alle har svart» open for 3.4; sprint-status `3-3` to done; note `epic-2-retro-item-12` applied (commit sizes listed).

**Acceptance Criteria:**
- Given a count above 0 on Oversikt, when Rikke follows it, then A3 lists exactly the people or households of that rule's id tuple, with the count in its `h1` (FR-55).
- Given a count of 0, when Oversikt renders, then it is plain text with no `<a>` (UX-DR41).
- Given each count on Oversikt, when a test opens its page, then the number of rows equals the count.
- Given a logged-out visitor, when she asks for an A3 address, then she goes to the login page; given an unknown slug, then the couple's own 404.
- Given Oversikt and A3 at 360px and 180px width and 20px text, when used, then every target is at least 44px, nothing scrolls horizontally, and the links are reachable with the keyboard alone.

## Spec Change Log

- 2026-11-26, implementation: commits 4 and 5 swapped (the route and A3 came before the links on Oversikt, so no link was ever dead). The shared template is `overview/_cells.html` (all cells of one row on one line) instead of a per-cell `_cell.html`, because a per-cell include left a stray space before the comma in «3 ja , 2 kanskje». `persons` and `households` moved to `dashboard/counts.py` with `count_text`; `Row.text` stays as a read-only property over `cells`. `dashboard.counts` also holds `DAY_COMBOS`, `MEALS`, `ALLERGY_NAMES`, `HIKE_NAMES` and `PAYMENTS` (label and slug per count), which `overview.py` imports. Test plan rows are MT-75 to MT-78.

## Review Triage Log

## Design Notes

- **Why a registry.** Each count is defined once, so the number on Oversikt, the link, the A3 heading and the A3 rows come from one tuple (AD-2); adding a count is one entry, and the parametrized test covers it automatically.
- **Why names only.** A3 is shared by people from Oversikt, including the allergy counts, and allergies are health data (NFR-3, AD-18). Names and household answer the question «who are the 12»; categories and notes belong to the consent-checked list of Story 3.4.
- **Link text.** `<a aria-label="Kommer: 9 personer">9 personer</a>` inside `dd` after `dt` «Kommer». The visible text is contained in the name, so speech-control users can say what they see.
- **Planned deviation.** None from the epics; the route name `tall` is new and recorded in epics.md and EXPERIENCE A3 with the reason (a count has no other natural address).

## Verification

**Commands:**
- `uv run pytest` -- expected: all tests pass
- `uv run ruff check` -- expected: no findings
- `uv run ruff format --check` -- expected: no files would be reformatted
- `uv run djlint --check .` -- expected: no files would be updated
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes

**Manual checks (orchestrator, Playwright against Edge, MT-75 onwards):**
- Each count link on Oversikt (numbers read from the page and `expected.toml`) opens a list whose item count equals it; zero counts are not links; logged out denied; keyboard only; 360 and 180px; 20px text: see the MT task above.
