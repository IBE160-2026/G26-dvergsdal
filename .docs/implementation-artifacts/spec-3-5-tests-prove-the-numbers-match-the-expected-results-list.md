---
title: 'Story 3.5: Tests prove the numbers match the expected-results list'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_revision: '6b4e06f6c65d93cf3d0b86f74c2b73b6cfb62ef0'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-3-context.md'
  - '{project-root}/wedding/fixtures/expected.toml'
warnings: [multiple-goals]
deferred:
- summary: >-
    `guest_id` and the `seed.toml` load are still duplicated between `tests/test_expected_results.py`, `tests/test_overview.py` and `tests/test_admin_allergy_page.py`.
  reason: >-
    Low harm; move them into `tests/helpers.py` the next time one of those files is touched.
- summary: >-
    Story 7.2 loads Synne's withdrawal in the seed: delete `seeded_with_synne_withdrawal`, the seed-alone pin test and `SYNNE_UNTIL_7_2`, and check that the withdrawal it stores is the same state as the fixture's `Consent.WITHDRAWN` row (also whether the `Allergy` rows are deleted).
  reason: >-
    The fixture inserts the Consent event directly because no withdrawal flow exists before 7.2.
---

<intent-contract>

## Intent

**Problem:** The checks against `expected.toml` are spread over `test_overview.py`, `test_admin_overview.py`, `test_admin_guests_page.py` and `test_admin_allergy_page.py`, each with its own Synne offset, so nobody can point at one place and say «this is the proof» (FR-69, SM-2). The README does not say what the expected-results tests check or where the hand-worked list is, and nothing stops a careless edit of `expected.toml` itself.

**Approach:** One module, `tests/test_expected_results.py`, is the FR-69 proof: every FR-54 count (the Betaling panel excluded), each household's total and each guest's status and allergy state, at three levels (rules, the count registry, the rendered pages), all read from `expected.toml`. Synne's withdrawal is applied in the test (a withdrawn `Consent` event) so the whole list holds with no offset; one separate test pins what the seed alone gives until Story 7.2. Guard tests keep `expected.toml` consistent with `seed.toml` and with itself; the README explains all of it.

## Boundaries & Constraints

**Always:**
- Every test and fixture names its FR/NFR/AD ids (FR-54, FR-69, FR-73, FR-74, NFR-2, SM-2, AD-16, AD-18, FR-26, FR-30). Code and spec English, README and manual-test rows Norwegian. Numbers are never written in a test: they come from `EXPECTED` (`tomllib`), the registry in `dashboard/counts.py` and the seed keys.
- `now`: no rule or selector behind the counts takes a clock (summary and household rules are `now`-free), so no test passes one. The module docstring says so, and a test fails if a function in `wedding.rules.summary` gains a `now` parameter without the module using it (`inspect.signature`): the day a count takes `now`, the test must pass an explicit one (epic context: explicit `now`).
- Synne: fixture `seeded_with_synne_withdrawal` runs after `seeded_with_answers` and creates Synne's `Consent.WITHDRAWN` event (explicit `at` = her given event's `at` plus one day, `given_by_name` «Synne», `text_version` of her given event), through the same model the loader reads (AD-18). With it every comparison is exact: `nuts = 0`, `has_allergies = 2`, `nothing_stored = 4`, no `SYNNE_UNTIL_7_2` anywhere in the new module. The fixture is deleted by Story 7.2 (seed loads the withdrawal) and the pin test with it.
- One test, `test_the_seed_alone_differs_from_expected_only_by_synne_until_7_2`, loads `seeded_with_answers` only and asserts the exact deviation: nut category +1, `has_allergies` +1, `nothing_stored` -1, Synne's state `has_allergies`, and every other number equal. It uses `SYNNE_UNTIL_7_2` from `tests/helpers.py` and names Story 7.2 as the time to delete it.
- The old duplicates move, not stay: `test_counts_equal_expected_toml`, `test_allergies_equal_expected_toml_except_synne_until_7_2`, `test_every_coming_guest_has_exactly_one_allergy_state_as_expected` and `test_household_totals_equal_expected_toml` leave `tests/test_overview.py` (their checks live in the new module); loader, view-model and query-count tests there stay. `SYNNE_UNTIL_7_2` stays in `tests/helpers.py` for the pin test and the page tests of 3.4 that still use it.
- `wedding/rsvp/views.py` (1528 lines), `guests/` and all app code are not touched. Test-only story, plus README, docs and the shared `tel_rows` helper.

**Never:**
- No payment panel, payment status, report match or lock case (Stories 5.3, 4.3); `[counts.payment_status_coming]`, `received`, `payment_status`, `report_matches` and `[[lock]]` are not asserted, and a test lists them as the keys this module leaves out, so a new section in `expected.toml` fails until someone decides.
- No hard-coded count, no copy of a rule in a test, no changing `expected.toml` or `seed.toml` in this story. If a test finds a mismatch, the app is wrong until a hand-count proves otherwise; any change to `expected.toml` is its own commit with the reason in the message (AD-16) and a line in `deferred-work.md`.
- No browser in the implementer's run; no retrospective is planned (last story of Epic 3, the epic retrospective is `optional`).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Rules, with withdrawal | `seeded_with_synne_withdrawal` | Every `counts.*` in the registry (households, people, days incl. `other_days`, overnight, meals, allergy categories and states, hike) equals `len()` of its id tuple | A registry count with no entry in `expected.toml` and not payment fails with its slug |
| Guest states | every key in `[guests]` | `people_by_state` status per guest, and for coming guests exactly one of the three allergy lists, the expected one; not-coming and not-answered guests are in none | — |
| Household totals | every key in `[households]` | `household_totals` equals `total`; household state matches `answered` / `coming` / `not_coming` / `not_answered` counts by key | — |
| Rendered Oversikt | `testpar` opens `/admin/` | Each panel number read from its row equals `expected.toml`; a zero is plain text | — |
| Rendered count pages | every registry slug with count above 0 | `/admin/tall/<slug>/` lists exactly as many `li` as the expected number | — |
| Rendered Gjester | `/admin/gjester/` | «N husstander · M gjester» equals `counts.households.total` and the guest sum; each household's «Totalt» equals `total` | — |
| Rendered allergy list | `/admin/allergier/` | `li` count equals `has_allergies`; names equal the guests whose state is `has_allergies`; no name from `nothing_stored` | — |
| Seed alone | `seeded_with_answers` | Differs only by Synne (pin test) | A different deviation fails, naming the number |
| Guard: keys | `expected.toml` vs `seed.toml` | Guest and household keys equal the seed's; each `[guests]` status agrees with the seed's `coming` | Names the missing or extra key |
| Guard: sums | `expected.toml` alone | people states sum to the seed's guest count; coming = sum of the three allergy states; `whole_weekend + not_whole_weekend` = coming; `beds + not_staying` = coming; day breakdown sums to `not_whole_weekend`; each category count ≤ `has_allergies` | Names the failing sum |

</intent-contract>

## Code Map

- `wedding/fixtures/expected.toml` -- read-only. Sections: `[counts.households|people|days|overnight|meals|allergy_categories|allergy_states|hike]` (asserted), `[counts.payment_status_coming]`, `[households.<key>]`, `[guests]`, `[[lock]]` (payment and lock parts excluded, see Never). Header L1-L21 says counts, totals and allergy states are Story 3.5 and that Synne holds only after 7.2.
- `wedding/fixtures/seed.toml` -- read-only. Synne L142-161: `consent = "yes"`, `consent_withdrawn = true` (ignored by `seed_testdata`, `management/commands/seed_testdata.py` L178). Guard tests read household and guest keys from here, as `tests/test_seed_files.py` does.
- `tests/test_overview.py` -- L48 `EXPECTED`, L68 `test_counts_equal_expected_toml`, L88 `..._except_synne_until_7_2`, L102 `test_every_coming_guest_...`, L121 `test_household_totals_equal_expected_toml`, `guest_id(key)` helper (L63), consent-event creation pattern at L222-239. Move the four tests out; keep the rest. Reuse `guest_facts`, `household_totals` from `dashboard/selectors.py`, `form_prices` from `wedding/selectors.py`.
- `dashboard/counts.py` -- the registry (`count_for`, `payment_statuses`, `MEALS`, `DAY_COMBOS`): iterate it instead of listing counts, so a new count without an expected value fails. `wedding/rules/summary.py`, `allergies.py`, `households.py` -- the rules; read-only, check with `inspect.signature` that none takes `now`.
- `tests/test_admin_overview.py` L19 (`EXPECTED` copy), L48 (`Svar` line), `tests/test_admin_guests_page.py`, `tests/test_admin_allergy_page.py` -- already check pieces of the pages; the new page tests reuse `log_in_as`, `page_text`, `sections_of`, `main_html` from `tests/helpers.py` and do not copy their assertions: they are the all-numbers sweep, the others stay as page-behaviour tests. Load `EXPECTED` from one place: add `load_expected()` to `tests/helpers.py` and make the four test files that parse the toml call it (removes the repeated `tomllib` block).
- `tests/conftest.py` -- `seeded_with_answers` L38; add `seeded_with_synne_withdrawal` here (it is Story 7.2's to delete) with a docstring naming 7.2.
- `tests/test_error_pages.py` L74-L86 (`_get`, `_tel_rows`) and `tests/test_front_page.py` (same `tel:` regex) -- move the shared `tel:` parsing to `tel_rows` in `tests/helpers.py` and call it from both. The three local `_get` helpers (`test_error_pages.py`, `test_practical_and_story_pages.py`, `test_programme_page.py`) differ in signature and in what they assert, so they stay: the deferred-work entry is closed with that reason.
- `README.md` -- «Tester og sjekker» (L96-122): add a subsection «Fasit-testene» (see Tasks). Status paragraph L9 and folder tree L185-186 (`tests/`) updated; shorten the status paragraph (deferred three times).
- `docs/manual-test-plan.md` -- last row MT-84 (3.4); next free number MT-85.
- `.docs/implementation-artifacts/deferred-work.md` L119-L123 (test-helper entry: still open `_get` and `tel:`), L291-L293 (Synne entry for 3.5); `sprint-status.yaml` L71 (`3-5` backlog) and L201-L210 (retro item 12).

## Tasks & Acceptance

Each group is one commit of about 600 changed lines or fewer (`epic-2-retro-item-12`; keep the triage comment and Spec Change Log).

**Execution:**
- `tests/helpers.py`, `tests/test_overview.py`, `tests/test_admin_overview.py`, `tests/test_admin_guests_page.py`, `tests/test_admin_allergy_page.py`, `tests/test_error_pages.py`, `tests/test_front_page.py` -- commit 1: `load_expected()` and `tel_rows()` in `tests/helpers.py`; the test files call them; no behaviour change (closes the `tel:` part of the helper tidy-up).
- `tests/conftest.py`, `tests/test_expected_results.py`, `tests/test_overview.py` -- commit 2: the module with the fixture, the rule and registry tests (all `counts.*` through the registry, per-guest states, per-household totals and states, the `now` signature guard, the seed-alone pin test); the four old tests deleted from `test_overview.py` in the same commit (FR-54, FR-69, FR-73, FR-74, AD-16, AD-18, FR-26, FR-30).
- `tests/test_expected_results.py` -- commit 3: the rendered-page sweep (Oversikt panels, every non-zero count page's `li` count, Gjester heading and totals, allergy list names) with `seeded_with_synne_withdrawal`, and the guard tests for `expected.toml` against `seed.toml` and its own sums, including the list of left-out sections (FR-69, SM-2, NFR-2).
- `docs/manual-test-plan.md` -- commit 4: MT-85 onwards, Norwegian, result cells empty, «Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`)» after `migrate`, `seed_testdata`, `runserver`. Steps: log in as `testpar` / `bryllup-test-2028`; (a) `/admin/`: read every panel number from the rows and compare with `expected.toml` (Synne's nut allergy still shows until 7.2: nuts one more, `has_allergies` 3, `nothing_stored` 3, and the row says nothing else differs); (b) `/admin/tall/kommer-husstander/`, `/admin/tall/senger-totalt/` and the nut-allergy count page: `li` count equals the Oversikt number; (c) `/admin/gjester/` heading and each «Totalt»; `/admin/allergier/` `li` count equals Oversikt's «Har allergier eller matbehov»; (d) logged-out `/admin/`, `/admin/gjester/`, `/admin/allergier/` and one count page go to the login; (e) keyboard only: Tab reaches each count link on Oversikt in reading order, Enter opens; (f) 360 × 640 and 180 × 320 at 16px and 20px (`scrollWidth` ≤ `innerWidth`, links ≥ 44px).
- `README.md`, `.docs/planning-artifacts/epics.md`, `wedding/fixtures/expected.toml` (header comment only, in its own commit), `deferred-work.md`, `sprint-status.yaml`, `.logs/rikke/issues.md` -- commit 5: README subsection «Fasit-testene» says (Norwegian) what the tests check (every count except Betaling, each household's total and each guest's allergy state, on rules, registry and rendered pages), that the hand-worked list is `wedding/fixtures/expected.toml` (counted by hand, a second agent and Rikke), the command `uv run pytest tests/test_expected_results.py`, that a change to the list is its own commit with the reason, and that Synne's withdrawal is applied by the test until Story 7.2; status line and `tests/` tree updated, status paragraph shortened; epics.md 3.5 implementation note, dated: Synne handled by a test fixture (deviation from «seed loads it», reason: 7.2 owns the seed change), no `now` needed and a signature guard instead, old checks moved; the `expected.toml` header (comment only) says the counts are Story 3.5 and done; deferred-work: close the Synne entry for 3.5 (re-opened for 7.2: delete fixture, pin test and `SYNNE_UNTIL_7_2`) and the helper tidy-up entry (`_get` stays by decision); sprint-status `3-5` to done and retro item 12 to `done` with the Epic 3 commit sizes; tick any issues.md item solved and add none for Rikke.

**Acceptance Criteria:**
- Given the seed data and Synne's withdrawal, when `uv run pytest tests/test_expected_results.py` runs, then every count in the registry except the payment ones, each household's total and each guest's status and allergy state equals `expected.toml` with no offset, and the rendered Oversikt, count pages, Gjester and allergy list show the same numbers.
- Given the seed alone, when the pin test runs, then the only differences from `expected.toml` are Synne's nut allergy, `has_allergies` and `nothing_stored`, named as waiting for Story 7.2.
- Given an app change that moves any number (a rule, the registry, a price), when the tests run, then at least one test in the module fails and names the key; given a careless edit of `expected.toml` (a missing guest, a sum that no longer adds up, a new section), then a guard test fails.
- Given the README, when Ingrid reads «Fasit-testene», then it says what the tests check, where the list is, how to run them and that a change to the list is its own commit with the reason.
- Given the whole suite, when `uv run pytest` runs, then it passes with no test removed except the four moved ones.

## Spec Change Log

## Review Triage Log

### 2026-11-27 — Review pass
- verdicts: 23 findings — high 0, medium 1, low 19, false 3, maybe-false 0
- findings:
  - `[medium]` `[patch]` The page tests force the three unlisted day combinations to 0 while the registry tests only check their sum (blind, edge-case) — an explicit assertion that `unlisted_expected()` is 0 makes the assumption fail loudly if expected.toml ever names them.
  - `[low]` `[patch]` `re.findall(r"<li>", …)` misses `<li class=…>` (blind, edge-case) — `<li\b`.
  - `[low]` `[patch]` `named[NOTHING_STORED]` raises KeyError when a state has no guests (blind) — `.get(state, set())`.
  - `[low]` `[patch]` The `now` guard loops over every function in `counts` without the `__module__` filter the rule modules have (edge-case) — filter added.
  - `[low]` `[patch]` README sentence «er appen feil til en tellingen …» is garbled (blind) — reworded.
  - `[low]` `[patch]` MT-90 typo «én tellesiden» (blind) — corrected.
  - `[low]` `[reject]` The `now` guard scans only summary, allergies, households and counts (blind, edge-case, verification-gap) — those are every module the counts call for their numbers; money and selectors take no clock today and the docstring says «behind the counts».
  - `[low]` `[reject]` Unlisted day combinations are checked only as a sum (blind, edge-case, intent) — expected.toml names only the five combinations; the sum catches any shift between the three and the named ones.
  - `[low]` `[reject]` The fixture inserts `Consent.WITHDRAWN` directly, not through a service (blind) — no withdrawal service exists until Story 7.2; the Consent event is the stored state AD-18 defines, and the deferred item for 7.2 says the fixture is deleted then.
  - `[low]` `[reject]` `guest_id`, `household_id` and `next()` without default give StopIteration, not a named message (edge-case) — the keys come from expected.toml and the guard test checks them against seed.toml first.
  - `[low]` `[reject]` Missing row `KeyError` in the Gjester test, `page_text(...).split()[0]`, and `assert len(links) == 1` (edge-case, blind) — test failures are loud and name the slug or household in the traceback; extra guards would only add code.
  - `[low]` `[reject]` `household_state_of` re-implements the household state rule in the test (blind) — a second, independent derivation from `expected.toml` states is the point of the proof; it reads no rule code.
  - `[low]` `[reject]` `guest_id` and `SEED` still duplicated in test files (blind) — the helper tidy-up in the spec moved `tel_rows`, `load_expected` and `FIXTURES`; the rest is deferred below.
  - `[low]` `[reject]` Intent: `now` is not passed explicitly (intent-alignment, blind) — no rule takes a clock; the guard fails the day one does. Recorded in epics.md and the spec as a deviation with the reason.
  - `[low]` `[reject]` Tests run the seed plus a Synne fixture, not the seed alone (intent-alignment) — recorded deviation; the seed-alone test pins the exact difference.
  - `[low]` `[reject]` README status paragraph replaced wholesale (blind) — the deferred README item from 3.2 and 3.3; story-to-feature traceability lives in epics.md and the specs.
  - `[low]` `[reject]` Manual rows run on the seed alone and automated tests apply the withdrawal; MT-87 «Totalt» only for coming households (blind) — MT-85 states the Synne offset; MT-87 now records the result for coming households, non-coming ones show none.
  - `[low]` `[reject]` No test shows a wrong number fails (blind) — the implementer changed `beds` 8 → 9 and five tests failed, then restored it; recorded in the result.
  - `[low]` `[reject]` Possible unused imports in `test_overview.py`, status files disagree, commit sizes, no session log (blind, edge-case) — `ruff check` passes; status is set in the finalize step; the log is step 14.
  - `[low]` `[reject]` Verification-gap «other finding»: the `now` guard is narrower than its docstring (verification-gap) — same as the scan-scope row above.
  - `[false]` `[reject]` MT-85 to MT-90 written but not run (blind, intent-alignment) — run by Claude with Playwright after review and recorded.
  - `[false]` `[reject]` Slug `allergi-notter` unverified in MT-86 (edge-case) — opened in Edge, 200 with one `li`.
  - `[false]` `[reject]` Per-guest allergy state not read back from a per-guest page (intent-alignment) — the allergy list names the guests and the states are checked at rule level; no other page shows a per-guest state.

## Design Notes

- **Why a fixture, not an offset.** The offset (`+ SYNNE_UNTIL_7_2`) proves the app agrees with a list that is almost the hand list; applying the withdrawal through the real `Consent` model proves it agrees with the hand list itself, which is what FR-69 promises. The one remaining deviation sits in a single named test, so Story 7.2 deletes three things (fixture, pin test, constant) and nothing else.
- **Registry-driven.** Iterating `dashboard/counts.py` means a new count cannot be added without an expected value; the guard against forgotten sections does the same for the toml.
- **`now`.** The counts depend on facts only. Passing a fake clock would test nothing; the signature guard keeps the promise of the epic context honest.
- **Golden shape of a registry test:**
  ```python
  for slug, expected_count in expected_counts(EXPECTED).items():
      assert len(count_for(slug).ids(facts)) == expected_count, slug
  ```
  with `expected_counts` mapping each registry slug to its place in `expected.toml` (a small table in the test, not in app code).

## Verification

**Commands:**
- `uv run pytest tests/test_expected_results.py` -- expected: all pass
- `uv run pytest` -- expected: all pass
- `uv run ruff check` -- expected: no findings
- `uv run ruff format --check` -- expected: no changes needed
- `uv run djlint --check .` -- expected: no findings

**Manual checks (orchestrator, Playwright against Edge):** MT-85 onwards as above; record the results in `docs/manual-test-plan.md` as «kjørt av Claude med Playwright».

## Auto Run Result

Status: done

**Summary:** One module, `tests/test_expected_results.py` (15 tests), is the proof that the numbers match `wedding/fixtures/expected.toml` (FR-69, NFR-2, SM-2): every FR-54 count except Betaling, each household's total and each guest's status and allergy state, checked at the rules, the count registry and the rendered pages (Oversikt, count pages, Gjester, allergy list). Synne's withdrawal is applied by a fixture so the whole list holds with no offset; one test pins what the seed alone gives until Story 7.2. Guard tests keep `expected.toml` consistent with `seed.toml` and with itself, and a guard fails if a count rule gains a `now` parameter. The README has a «Fasit-testene» section. No app code changed.

**Files changed:**
- `tests/test_expected_results.py` (new), `tests/conftest.py` (fixture), `tests/helpers.py` (`load_expected`, `tel_rows`), `test_overview.py`, `test_admin_allergy_page.py`, `test_admin_guests_page.py`, `test_error_pages.py`, `test_front_page.py`.
- `wedding/fixtures/expected.toml` (header comment only), `README.md`, `epics.md`, `deferred-work.md`, `sprint-status.yaml`, `docs/manual-test-plan.md` (MT-85 to MT-90).

**Review:** 23 findings from four layers: 6 patched (the unlisted-day assumption made explicit, `<li\b`, empty states in the allergy test, `__module__` filter in the `now` guard, README wording, a test-plan typo), 17 rejected with reasons; 2 follow-ups deferred.

**Follow-up review recommendation:** false. Test-only story, no high finding.

**Verification:** `uv run pytest` 1621 passed; ruff, ruff format and djlint clean; changing `beds` in expected.toml from 8 to 9 failed five tests. MT-85 to MT-90 run by Claude with Playwright in Edge: all Oversikt numbers equal expected.toml except Synne's known offset (Nøtter 1, 3 with allergies, 3 nothing stored); `li` counts on count pages and the allergy list match; logged-out redirects; keyboard-only over 30 links; 360 and 180 px at 18 and 22.5 px with no overflow.

**Residual risks:** The tests prove seed plus the Synne fixture; the seed alone differs by Synne until Story 7.2. The three unlisted day combinations are checked only as a sum (an explicit assertion fails if expected.toml names them).
