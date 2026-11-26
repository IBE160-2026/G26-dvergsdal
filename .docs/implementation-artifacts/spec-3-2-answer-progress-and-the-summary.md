---
title: 'Story 3.2: Answer progress and the summary'
type: 'feature'
created: '2026-11-26'
status: 'ready-for-dev'
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

**Problem:** Oversikt (`/admin/`) is an empty frame. The couple cannot see how many households have answered or the numbers Hardingasete asks for, `allergy_state` and `payment_status` do not exist, and the helper read-only line is still missing (FR-48, FR-54, FR-73, FR-74, NFR-2, AD-2, AD-12, AD-18, UX-DR39, UX-DR40, UX-DR49).

**Approach:** (1) pure rules in `wedding/rules/` return id lists (counts are their lengths), plus `allergy_state` and `payment_status`; (2) one dashboard selector loads every guest's facts without filtering on answer content; (3) `dashboard/overview.py` turns rules into a view model (Norwegian labels, plurals, bar percent); (4) Oversikt renders the Svar panel and six summary panels from that model, and the frame shows the helper line.

## Boundaries & Constraints

**Always:**
- Every rule, selector, view, template comment and test names its FR/NFR/UX-DR/AD ids. UI text Norwegian, code and spec English. Breakpoints in `em`, tokens from DESIGN.md, 44px targets, flat green, straight cream `admin-panel`s, no JavaScript.
- A count is `len()` of an id tuple returned by a rule function (AD-2); templates and `overview.py` never count, filter or add. A count of 0 is plain text (3.3 makes counts above 0 links; here every count is plain text, since the lists page does not exist yet).
- Tests compare the app's numbers with `wedding/fixtures/expected.toml` (loaded with `tomllib`, never hard-coded numbers), loading the seed through the `seeded_with_answers` fixture and passing `now` explicitly where a rule takes it (FR-69, AD-16).
- Allergy data counts only for a guest with latest consent «Ja» not withdrawn (AD-18); every coming guest has exactly one of `has_allergies` / `no_allergies` / `nothing_stored`.
- Payment panel: received and refunded are 0 until Story 5.2, so a household that comes owes `total` (not_paid) or nothing (nothing_to_pay). Household totals come only from `household_total` with `form_prices()` (AD-12).
- Dashboard imports neither `guests` nor `wedding.rsvp` (architecture test stays green). `wedding/rsvp/views.py` and `guests/views.py` are not touched; no logic in templates.

**Never:**
- No drill-down pages or count links (3.3), no household list or allergy list page (3.4), no «Trenger oppfølging» content (Story 6.2), no payments (5.x). No «Stemmer ikke» count (attention item, FR-61).
- «Se hva alle har svart» is plain text with no link until Story 3.4 sets its `url`; no dead link.
- Never add Hike «Nei» to «kommer» or «kanskje»; never sum them.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Seeded data | Logged-in couple, `seeded_with_answers` | Every panel number equals `expected.toml` (answered, coming/not coming/not answered for persons and households, days, beds, meals, categories, allergy states, hike, payment statuses) except Synne's three allergy numbers (see Design Notes) | — |
| No data | Couple, no households | «Svart: 0 av 0 husstander», bar 0 %, all rows 0, no divide by zero | — |
| Logged out | GET `/admin/` | 302 to login (unchanged) | — |
| Helper | Helper logs in | Same numbers, plus «Du kan se alt, men ikke endre noe.» under the nav; the couple sees no such line; the login page and error pages show none | — |
| Guest not in a sent answer | Guest in an answered household without a `PersonAnswer` | Counts as «Ikke svart ennå» for the person | — |
| Withdrawn/refused consent | Latest consent event is «withdrawn» or «refused» | `nothing_stored`, no category counted | — |

</intent-contract>

## Code Map

- `wedding/rules/allergies.py` -- `has_allergy_info`, `AllergyEntry`, `ALLERGY_KEYS`. Add `allergy_state(entry, consent)` and the three state keys (`HAS_ALLERGIES`, `NO_ALLERGIES`, `NOTHING_STORED`): consent not True gives `nothing_stored`; else `none` (no cats, no note) gives `no_allergies`; else cats or note gives `has_allergies`; consent True with no entry gives `nothing_stored`.
- `wedding/rules/money.py` -- `household_total`, `guest_balance`. Add `payment_status(answered, total, received, refunded)`: not answered gives `not_answered`; net = received - refunded; total 0 and net 0 gives `nothing_to_pay`; net > total gives `refund_owed` (also total 0 with net > 0); net == total gives `paid`; 0 < net < total `part_paid`; else `not_paid`. Keys as `expected.toml` (`paid`, `part_paid`, `not_paid`, `nothing_to_pay`, `refund_owed`).
- `wedding/rules/households.py` -- `person_state`, `household_state`, `COMING`/`NOT_COMING`/`NOT_ANSWERED` (reuse, do not copy).
- `wedding/rules/days.py` -- `DAY_KEYS`, `MEAL_KEYS`, `HIKE_ANSWERS` (reuse).
- `wedding/rules/summary.py` -- New. `GuestFacts` frozen dataclass (guest_id, household_id, answered, coming, days, cabin, meals, hike, allergy, consent) as plain values. Rules returning sorted id tuples: `households_by_state`, `people_by_state`, `whole_weekend`, `not_whole_weekend`, `days_only(combo)`, `not_staying`, `beds`, `meal_eaters(meal)` (incl. `saturday_lunch`/`saturday_dinner`: coming and present Saturday, FR-73), `allergy_state_ids(state)`, `allergy_category_ids(category)`, `hike_ids(answer)`, `households_by_payment(status)` (takes household statuses). `now` is not needed here.
- `wedding/selectors.py` -- `sent_answer` (L147-193) shows how rows, allergies and consent events become facts (latest event; «withdrawn» removes). Read-only evidence for the new loader; do not grow it.
- `dashboard/selectors.py` -- New. `guest_facts()`: all guests with their `PersonAnswer`, `Allergy`, latest `Consent` and `HouseholdAnswer` in about five queries, no filter on answer content; `household_totals(facts, prices)` builds an `Answer` per household and calls `household_total`.
- `dashboard/overview.py` -- New. `build_overview(facts, totals)` returns a plain view model: `progress` (answered, total, percent 0-100, three rows with persons and households text), `panels` in order Når kommer de? · Overnatting · Mat · Allergier (med samtykke) · Fjelltur fredag · Betaling (husstander som kommer), each a title and rows of (label, count text). Norwegian plural helper `person/personer`, `husstand/husstander`. Lengths of rule tuples only.
- `dashboard/views.py` -- `home` (L96-105) renders Oversikt; it calls the selector and `build_overview`. `dashboard/navigation.py` -- `nav_items`; add `frame(request)` giving `nav_items` and `read_only` (True for role helper) so errors and pages share it; `dashboard/errors.py` `_frame` (L36) reuses it.
- `dashboard/templates/dashboard/home.html` -- replace the placeholder panel; include `dashboard/overview/_attention.html` (only a template comment, the place Story 6.2 fills), `_progress.html`, `_panel.html` (one include for all six, `h2`, `dl` rows). `admin_base.html` -- add the helper line under the `<nav>`.
- `static/css/site.css` -- admin section (L1795-1905) holds `.admin-panel`; add «Overview» rules (`.answer-bar`, `.overview-rows`, `.admin-readonly`), 20px cream-on-green line with a 4px cream left rule (DESIGN.md L699), rows wrap on 360px and 180px, em breakpoints only; `tests/test_form_components.py` bans px breakpoints.
- `tests/test_summary_rules.py`, `tests/test_overview.py`, `tests/test_admin_overview.py` -- New. `tests/test_answer_rules.py` L32-33 shows loading `EXPECTED`; `tests/test_admin_login.py` L30-35 `couple`/`log_in`; `tests/helpers.py` `make_admin`, `page_text`; `tests/conftest.py` `seeded_with_answers`.
- `wedding/fixtures/expected.toml` -- read-only source of truth; not edited.

## Tasks & Acceptance

Each group is one commit (about 600 changed lines or fewer; epic-2-retro-item-12).

**Execution:**
- `wedding/rules/allergies.py`, `wedding/rules/money.py`, `tests/test_allergy_rules.py`, `tests/test_payment_rules.py` -- commit 1: `allergy_state` and `payment_status`, all states, boundaries (net equal to total, total 0 with refund, not answered ignores amounts) (FR-60, FR-74, AD-18, AD-2).
- `wedding/rules/summary.py`, `tests/test_summary_rules.py` -- commit 2: the id-list rules on small hand-made facts (empty input, whole vs partial, Saturday lunch and dinner, categories, hike, a guest without answer) (FR-54, FR-73, FR-74, AD-2).
- `dashboard/selectors.py`, `dashboard/overview.py`, `tests/test_overview.py` -- commit 3: loader and view model; seeded data equals `expected.toml` for every count, each household's total, each guest's allergy state, payment panel from totals with received 0; no data gives zeros; a query-count bound on the loader (FR-54, FR-69, NFR-2, AD-12, AD-16).
- `dashboard/views.py`, `dashboard/navigation.py`, `dashboard/errors.py`, templates, `static/css/site.css`, `tests/test_admin_overview.py` -- commit 4: Oversikt page and helper line; HTML test with the seeded data (panel order, `h2` names, `aria-hidden` bar, «Svart: X av Y husstander» built from `expected.toml`, plain-text 0, no `<a>` inside the panels except nav, no «Se hva alle har svart» link), helper vs couple line, no line on login/error pages, logged out redirect, existing admin tests updated (the placeholder sentence) (FR-46, FR-48, UX-DR39, UX-DR40, UX-DR49).
- `docs/manual-test-plan.md` -- commit 5: MT-71 onwards (Norwegian, result cells empty), «Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`)» after `migrate`, `seed_testdata`, `runserver`: log in as `testpar` / `bryllup-test-2028` and open `/admin/`: «Svart: 6 av 7 husstander» (read from `expected.toml`), all six panels in order; helper login (`testhjelper` / `bryllup-test-2028`) shows the line; logged out `/admin/` goes to login; keyboard only (Tab reaches nav words and «Logg ut», no stop on plain-text counts); 360 × 640 and 180 × 320 at 16px and 20px (`scrollWidth` ≤ `innerWidth`, targets ≥ 44px, the answer line and bar on the first screen at 360 × 640).
- `README.md`, `.docs/planning-artifacts/epics.md`, `EXPERIENCE.md`, `DESIGN.md`, `deferred-work.md`, `sprint-status.yaml` -- commit 6: status line and tree (`rules/summary.py`, `dashboard/selectors.py`, `overview.py`, new tests); epics 3.2 note: counts are plain text until 3.3, «Se hva alle har svart» is plain text until 3.4, Synne's offset until 7.2, payment statuses with received 0, dated reasons; mark the helper-line deferred item done; add deferred: Story 3.3 links counts and Story 3.4 sets the url; `epic-2-retro-item-12` applied (commits split as above) and the commit sizes noted.

**Acceptance Criteria:**
- Given the admin home with the seed data, when it renders, then the Svar panel shows «Svart: 6 av 7 husstander» (values from `expected.toml`), an `aria-hidden` bar, the rows Kommer / Kommer ikke / Ikke svart ennå with persons and households, and the plain text «Se hva alle har svart»; a place for «Trenger oppfølging» is kept above it.
- Given the summary panels, when they render, then they appear in the order of the epics AC, Saturday lunch and dinner count everyone present on Saturday, the hike panel reads «n kommer, n kanskje», and each coming guest has exactly one allergy state.
- Given every count, when it is computed, then it is the length of an id tuple from `wedding/rules/summary.py`, and `payment_status` covers all five FR-60 statuses and «not answered».
- Given the admin home on a 360px phone (and 180px, and 20px text), when used, then every target is at least 44px and nothing scrolls horizontally.
- Given a helper, when Oversikt opens, then «Du kan se alt, men ikke endre noe.» stands under the nav; the couple do not see it.

## Spec Change Log

## Review Triage Log

## Design Notes

- **Why `GuestFacts` plain values.** Rules stay pure (`tests/test_rules_purity.py`) and testable without a database; the selector is the only place that reads models.
- **Synne until Story 7.2.** The seed does not yet load her withdrawn consent, so the app shows her nut allergy: nuts 1, `has_allergies` 3, `nothing_stored` 3. Tests assert `expected.toml` values plus one named offset constant (`SYNNE_UNTIL_7_2`) with a comment; Story 7.2 removes it. `expected.toml` is not edited.
- **Payment panel before payments.** Expected statuses assume payments (Story 5.3), so Story 3.2 tests the panel as: total 0 gives `nothing_to_pay`, else `not_paid`, using each household's `total` from `expected.toml`. Story 3.5 excludes the panel (epics).
- **Row shape.** Each row is a `dl` pair (label, count text, e.g. «9 personer · 5 husstander») that wraps, so it needs no horizontal space at 180px.
- **Query use.** `guest_facts()` loads in about five queries; no per-household queries (30 households).

## Verification

**Commands:**
- `uv run pytest` -- expected: all tests pass
- `uv run ruff check` -- expected: no findings
- `uv run ruff format --check` -- expected: no files would be reformatted
- `uv run djlint --check .` -- expected: no files would be updated
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes

**Manual checks (orchestrator, Playwright against Edge, MT-71 onwards):**
- Couple sees progress and summary with seeded data (numbers read from the selectors or `expected.toml`, never hard-coded), helper line, logged-out denial, keyboard only, 360 and 180px, 20px text: see the MT task above.
