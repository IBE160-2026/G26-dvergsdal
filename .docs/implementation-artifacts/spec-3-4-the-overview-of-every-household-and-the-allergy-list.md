---
title: 'Story 3.4: The overview of every household and the allergy list'
type: 'feature'
created: '2026-11-27'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-3-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md'
warnings: [multiple-goals, oversized]
deferred: []
---

<intent-contract>

## Intent

**Problem:** Rikke cannot check one household, and cannot hand Hardingasete the allergy names: «Gjester» in the nav is plain text, «Se hva alle har svart» has no address, and the allergy counts open names only, with no categories or notes (FR-48, FR-57, FR-58, UX-DR42, UX-DR48, UX-DR49).

**Approach:** (1) a Gjester page `/admin/gjester/` (A4, simple): «N husstander · M gjester» and one row per household, unanswered first; (2) an allergy list `/admin/allergier/` (A5): name, categories and note of every coming guest whose allergy data is stored with consent, taken from one new pure rule so the list length equals the «Har allergier eller matbehov» count; (3) the addresses: nav «Gjester», «Se hva alle har svart», an «Allergilisten» link, and household rows on A3 point to the household's row on Gjester.

## Boundaries & Constraints

**Always:**
- Every rule, selector, view, template comment and test names its FR/NFR/UX-DR/AD ids. UI text and URLs Norwegian, code and spec English. Breakpoints in `em`, tokens from DESIGN.md, 44px targets, flat green, straight cream `admin-panel`s, no JavaScript. Status tags are text plus icon (`wedding/components/state-icon.html`), never colour alone.
- Both pages are behind `admin_required` (logged out: 302 to login with `next`); the couple and a helper both see them (helpers read everything, UX-DR49 line shown); both are `require_safe`; nav marks Gjester as the open page. `wedding/rsvp/views.py` (1528 lines) and `guests/` are not touched; `dashboard` imports neither `guests` nor `wedding.rsvp`; new code lives in `dashboard/` and `wedding/rules/`.
- Gjester: heading counts are `len(all_households)` and `len(facts)`. Order: not-answered households first, then the rest, each by household name (`str.casefold`, then id). Row = household name as `household_names` writes it, the tag «Ikke svart» (warning) only when not answered, and one line: «Kommer: <coming names>» + «Totalt <kroner>», «Kommer ikke» when answered and nobody comes, «Har ikke svart ennå» when not answered. Total from `household_totals`, shown with the `kroner` filter. Each `li` has `id="husstand-<household id>"`. No payment in the line until Epic 5.
- Allergy list: exactly the guests in the new rule `allergy_list(facts)`, which is `allergy_state_ids(facts, HAS_ALLERGIES)` with each guest's categories and note; so consent «Ja», not withdrawn, is checked by the same rule as Oversikt (AD-18, FR-26, FR-58). A guest with consent «Nei», no consent, withdrawn consent, «Ingen allergier» only, or not coming never appears, and neither does their note. Categories use the labels of `dashboard.counts.ALLERGY_NAMES`; the note is autoescaped and shown with its line breaks (`white-space: pre-line`).
- `h1` «Allergilisten», a count line «N personer», «Tilbake til Oversikt»; empty: «Ingen allergier registrert ennå.» (UX-DR48). Gjester empty: «Ingen husstander ennå.» (UX-DR42).
- «Se hva alle har svart» (Svar panel) is a link to `/admin/gjester/` at least 44px tall, still underlined. The Allergier panel on Oversikt gets a link «Se allergilisten» to `/admin/allergier/`. Gjester has a link «Allergilisten» too (EXPERIENCE A5: reached from A2 and A4).
- Household rows and person rows on A3 (count pages) link to `/admin/gjester/#husstand-<household id>` with the household's names as link text (a 44px target); a person's name stays text, their household names become the link.
- Tests take numbers from `wedding/fixtures/expected.toml` (`tomllib`) and the registry, never hard-coded, with `seeded_with_answers` and the named `SYNNE_UNTIL_7_2` offset (Synne's nut allergy and consent stay until Story 7.2) (FR-69, AD-16).

**Never:**
- No search «Finn en gjest», no «Legg til husstand» (Story 6.3 / 4.x), no household page A6 (Story 6.3), no tags «Stemmer ikke» or «Endret» (Epic 5, 7), no payment text, no «Trenger oppfølging» sorting (6.2), no copy-link, no edit.
- No count or filter in a template; no second copy of a consent or allergy rule; no per-household queries; no allergy text on any page except the allergy list; the allergy list is not linked from guest pages.
- No link to a page that does not exist: A3 rows link to the Gjester row, not to A6.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Gjester, seed | `/admin/gjester/` as `testpar` | «7 husstander · 14 gjester» (from `expected.toml`), 7 `li`, the not-answered household (mona) first with «Ikke svart», each other row with its `total` from `expected.toml` when it comes | — |
| Gjester, empty | No households | `h1`, «0 husstander · 0 gjester», «Ingen husstander ennå.» | — |
| Household that does not come | Tor's household answered, nobody comes | «Kommer ikke», no tag | — |
| Allergy list, seed | `/admin/allergier/` | One `li` per guest of `allergy_state_ids(HAS_ALLERGIES)`: count equals `expected.toml` `has_allergies` + `SYNNE_UNTIL_7_2`; Eva shows «Skalldyr, Annet», bestemor «Gluten» | — |
| No consent | Filippa (vegetarian, consent «Nei»), Ida | Not on the list, nothing about them on the page | — |
| Consent withdrawn | A listed guest's consent withdrawn (test adds a `Consent` withdrawn event) | Gone from the list and the note is not in the HTML | — |
| «Ingen allergier» only | Sigmund, Arild, Jonas | Not on the list | — |
| Allergy list, empty | Nobody has consented allergy data | «Ingen allergier registrert ennå.», count «0 personer» | — |
| Logged out | GET either page | 302 to `/admin/logg-inn/?next=…` | — |
| Helper | Helper opens either | Same content, plus the read-only line | — |
| Note with markup | Note `<b>x</b>` | Shown as text, escaped | — |

</intent-contract>

## Code Map

- `wedding/rules/summary.py` -- `allergy_state_ids` (L134) and `allergy_category_ids` (L141) already check consent through `allergy_state`; `GuestFacts.allergy` (an `AllergyEntry` with `cats`, `none`, `note`) and `.consent` are on the facts. Add `allergy_list(facts) -> tuple[AllergyListEntry, ...]` (guest id, categories in `ALLERGY_KEYS` order, note), built on `allergy_state_ids`; pure, `now`-free. Reuse, do not change the others.
- `wedding/rules/households.py` -- `household_names` (L34), `household_state` (L72); reuse for Gjester rows. `wedding/templatetags/money.py` `kroner` (L17) for totals.
- `dashboard/selectors.py` -- 150 lines: `guest_facts`, `household_totals`, `people_behind`, `households_behind`, `_household_names`. Add `guest_names()` (guest id and household id to name, one query, in id order) for Gjester and the allergy list; extend `Person` and `HouseholdRow` with `household_id` (A3 anchors).
- `dashboard/guest_list.py` -- New view model: `HouseholdListRow(household_id, names, answered, line)`, `build_guest_list(facts, names, totals)` (sorting rule and line text above) and `build_allergy_list(facts, names)`. No counting in templates.
- `dashboard/views.py` -- `home` (L96), `count_page`, `unknown`. Add `guests_page` and `allergies_page` after `count_page` (`admin_required`, `require_safe`, `frame(request, "guests")`). `dashboard/urls.py` L19-30: add `gjester/` (`dashboard:guests`) and `allergier/` (`dashboard:allergies`) above the `<path:rest>` catch-all. `config/logging_filters.py` / reserved segments: both are under `/admin/`, so no change; `tests/test_admin_routing.py` checks it.
- `dashboard/navigation.py` -- `NAV_ITEMS` (L33): `NavItem("guests", "Gjester", "dashboard:guests")`; update the module docstring (Gjester is built).
- `dashboard/templates/dashboard/guests.html`, `allergies.html` -- New A4 and A5. Gjester: `admin-title`, count line, «Allergilisten» link, one `admin-panel` with `ul.guest-list`, tag via `state-icon.html` (`variant="warning"`). `count.html` -- household names become a link to the Gjester row. `overview/_progress.html` (the `overview-note` paragraph) and `overview/_panel.html` -- link «Se hva alle har svart»; `Panel` in `dashboard/overview.py` gets an optional `link` (text, url name) shown by `_panel.html`, set in `_allergies`.
- `static/css/site.css` -- `.overview-row a` and `.count-back` (L1984-2000) are the 44px link pattern to copy; `.count-list` (L2001-2028) is the row pattern. Add `.guest-list`, `.status-tag` (outlined, icon plus word, `inline-flex`), `.allergy-list`, `.allergy-list__note` (`white-space: pre-line`, `overflow-wrap: anywhere`) and `.overview-note a`; `em` breakpoints only (`tests/test_form_components.py` bans px), no overflow at 180px and 20px text; forced-colours block (L2040) needs the tag border in `CanvasText`.
- `tests/helpers.py` -- gets `HELPER_LINE`, `log_in_as`, `SYNNE_UNTIL_7_2` (now in `tests/test_admin_overview.py` L24, L36 and `tests/test_overview.py` L53); `tests/test_admin_count_page.py` L19-20 imports them from there. `tests/test_summary_rules.py` (rule), `tests/test_guest_list.py` (view model, New), `tests/test_admin_guests_page.py`, `tests/test_admin_allergy_page.py` (New). Rewrite: `tests/test_admin_overview.py` L58-72 («Se hva alle har svart» is now a link) and `tests/test_admin_routing.py` L99 (Gjester is a link; Betalinger and Innstillinger stay plain). `tests/test_architecture_imports.py` stays green.
- `docs/manual-test-plan.md` -- last row is MT-78 (3.3); next free number MT-79.
- Read-only: `wedding/fixtures/expected.toml`, `wedding/fixtures/seed.toml` (household keys to names), `wedding/templates/wedding/components/state-icon.html`.

## Tasks & Acceptance

Each group is one commit of about 600 changed lines or fewer (`epic-2-retro-item-12`; keep the triage comment and Spec Change Log).

**Execution:**
- `tests/helpers.py`, `tests/test_admin_overview.py`, `tests/test_overview.py`, `tests/test_admin_count_page.py` -- commit 1: move `HELPER_LINE`, `log_in_as`, `SYNNE_UNTIL_7_2` to `tests/helpers.py`; no behaviour change (closes the 3.3 test-helper entry).
- `wedding/rules/summary.py`, `tests/test_summary_rules.py` -- commit 2: `allergy_list`; tests: consent True with categories listed; consent False, None and withdrawn (None) not listed with the same entry; «Ingen» only not listed; not coming not listed; categories in `ALLERGY_KEYS` order; note kept; length equals `len(allergy_state_ids(HAS_ALLERGIES))` (FR-58, AD-18, FR-26).
- `dashboard/selectors.py`, `dashboard/guest_list.py`, `tests/test_guest_list.py`, `tests/test_overview.py` -- commit 3: `guest_names`, `household_id` on `Person` and `HouseholdRow`, `build_guest_list`, `build_allergy_list`; tests of sort order (not answered first, then name casefold, ids breaking ties), each line variant, the empty list, and a fixed number of queries (`django_assert_num_queries`) (FR-57, FR-58, UX-DR42, NFR-2).
- `dashboard/views.py`, `dashboard/urls.py`, `dashboard/navigation.py`, `dashboard/templates/dashboard/guests.html`, `static/css/site.css`, `tests/test_admin_guests_page.py`, `tests/test_admin_routing.py` -- commit 4: Gjester page, route and nav link; tests: heading counts and rows from `expected.toml`, unanswered first with the tag, totals per household from `expected.toml`, `id` anchors, empty state, logged out 302, helper line, nav marks Gjester current, no allergy text (FR-48, FR-57, UX-DR42, UX-DR49).
- `dashboard/views.py`, `dashboard/urls.py`, `dashboard/templates/dashboard/allergies.html`, `static/css/site.css`, `tests/test_admin_allergy_page.py` -- commit 5: the allergy list page; tests: count equals `expected.toml` `has_allergies` plus the Synne offset and Oversikt's number; Eva's categories and notes shown; every non-consenting guest's allergy text absent from the HTML (checked against the seed's categories and notes); withdrawal removes a guest and their note; escaped note; empty state; logged out; helper (FR-58, UX-DR48, AD-18, FR-26).
- `dashboard/overview.py`, `dashboard/templates/dashboard/overview/_progress.html`, `_panel.html`, `dashboard/templates/dashboard/count.html`, `tests/test_admin_overview.py`, `tests/test_admin_count_page.py` -- commit 6: the three links («Se hva alle har svart», «Se allergilisten», household names on A3 to the Gjester anchor); the old plain-text assertion rewritten; a client test follows each A3 household link and finds the `id` on Gjester (FR-57, FR-55, UX-DR41).
- `docs/manual-test-plan.md` -- commit 7: MT-79 onwards, Norwegian, result cells empty, «Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`)» after `migrate`, `seed_testdata`, `runserver`. Steps: log in as `testpar` / `bryllup-test-2028`; (a) `/admin/gjester/`: read the heading counts and `li` count, compare with `expected.toml` (`counts.households.total`, people sum), the first row has the tag «Ikke svart», totals read from the rows equal `households.<key>.total`; (b) the link «Se hva alle har svart» on `/admin/` opens it, and each household link on `/admin/tall/kommer-husstander/` lands on its row; (c) `/admin/allergier/`: `li` count equals the `has_allergies` number on Oversikt, no name of a guest without consent appears (names read from `guests` with `nothing_stored` in `expected.toml`, except the Synne offset), categories of Eva and bestemor present; (d) logged out `/admin/gjester/` and `/admin/allergier/` go to login; helper sees both with the read-only line; (e) keyboard only: Tab reaches nav «Gjester», «Allergilisten», each link in reading order, Enter opens; (f) 360 × 640 and 180 × 320 at 16px and 20px (`scrollWidth` ≤ `innerWidth`, rows and links ≥ 44px, tag text wraps).
- `README.md`, `.docs/planning-artifacts/epics.md`, `EXPERIENCE.md`, `DESIGN.md`, `deferred-work.md`, `sprint-status.yaml`, `.logs/rikke/issues.md` -- commit 8: README status line and tree; epics 3.4 implementation note with dated reasons: A6 is Story 6.3, so A3 links to the Gjester row (deviation), search and «Legg til husstand» wait for 6.3/4.x, allergy list at `/admin/allergier/` shows coming guests with consent; EXPERIENCE A4 and A5 addresses and states, DESIGN status tag and guest-list row; deferred-work: close «Se hva alle har svart», the test-helper entry and the household-row entry (re-opened for Story 6.3: point A3 and Gjester rows to the real A6); sprint-status `3-4` to done; tick the issues.md item; note `epic-2-retro-item-12` applied (commit sizes listed).

**Acceptance Criteria:**
- Given the Gjester page on the seed data, when it renders, then it shows «7 husstander · 14 gjester» (from `expected.toml`), one row per household, the household that has not answered first with «Ikke svart», and the totals of `expected.toml`.
- Given no households, when Gjester renders, then it says «Ingen husstander ennå.».
- Given the allergy list, when it renders, then it lists the name, categories and note of exactly the guests whose allergy data is stored with consent, and nothing for any guest without consent (FR-58).
- Given nobody has consented allergy data, when the list renders, then it says «Ingen allergier registrert ennå.».
- Given a guest's consent is withdrawn, when the list renders, then they and their note are gone.
- Given Oversikt, when Rikke follows «Se hva alle har svart», then she lands on Gjester; given a household link on a count page, then she lands on that household's row.
- Given a logged-out visitor, when she asks for either page, then she goes to the login page; given a helper, then she sees both pages and the read-only line.
- Given both pages at 360px and 180px width and 20px text, when used, then every target is at least 44px, nothing scrolls horizontally, and every link is reachable with the keyboard alone.

## Spec Change Log

## Review Triage Log

## Design Notes

- **Why a new rule, not a selector.** The consent check must be the one Oversikt already uses (AD-18), so `allergy_list` wraps `allergy_state_ids`; the list length equals the «Har allergier eller matbehov» count by construction, and a test pins it.
- **Why the Gjester anchor, not A6.** The epics build A6 in Story 6.3 (household page); linking to a page that does not exist would be dead. Gjester rows carry `id="husstand-<id>"` so the A3 links work now, and Story 6.3 repoints them (deviation recorded in epics.md and deferred-work).
- **Names only on A3 stays.** Allergy details live only on A5, the single consent-checked place (FR-58, NFR-3).
- **Row line.** «Kommer: Sigmund og bestemor · Totalt 4 720 kr» (names from `household_names`, money from `kroner`); the payment word is added by Epic 5.
- **Decided wording (Claude, no approval item):** «Allergilisten», «Se allergilisten», «Allergilisten» link on Gjester, «Kommer ikke», «Har ikke svart ennå», «Ingen husstander ennå.», «Ingen allergier registrert ennå.», `[forslag]`.

## Verification

**Commands:**
- `uv run pytest` -- expected: all tests pass
- `uv run ruff check` -- expected: no findings
- `uv run ruff format --check` -- expected: no files would be reformatted
- `uv run djlint --check .` -- expected: no files would be updated
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes

**Manual checks (orchestrator, Playwright against Edge, MT-79 onwards):**
- Gjester and the allergy list on the seed data, numbers read from the page and `expected.toml`; logged out denied; helper view; keyboard only; 360 and 180px; 20px text: see the MT task above.
