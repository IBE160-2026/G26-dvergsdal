---
title: 'Story 1.2: Households, guests and personal links'
type: 'feature'
created: '2026-11-16'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '7276cbe082a37bc0fd6bc6bf3456b525e3e526f1'
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
  - '{project-root}/.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** There are no households, guests or links yet, so no guest page and no seed data (Story 1.3) can be built. Each guest needs one unguessable code that opens only their own household (FR-1, FR-2), and opening it must never write (FR-3).

**Approach:** Add `Household`, `Guest` and single-row `Settings` in one migration plus a data migration for the `Settings` row; add actor types, a `create_household` service (the only writer) and the one resolver `resolve_code` in `wedding/links.py`.

## Boundaries & Constraints

**Always:** Code English, user-facing messages Norwegian bokmål. Docstrings name FR/NFR/AD. Codes from `secrets.token_urlsafe(16)` (22 chars, `[A-Za-z0-9_-]`), unique (and so indexed), no personal data. Money is `int` whole kroner. Each service is one `transaction.atomic()` and takes an explicit actor. Household revision starts at 0. At most 8 and at least 1 guest per household (Rikke confirmed 8). Small commits, one concern each.

**Never:** no views, URLs, templates or CSS; no tables beyond `Household`, `Guest`, `Settings`; no stored derived values (no household name field: «for Sigmund og bestemor» is derived from guest names in Story 1.5); no `changed_at` (Epic 4); no `Submission` (Story 2.6c); no seed command or fixtures (Story 1.3); no raw SQL.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Known code | code of guest A in household 1 | `GuestActor(guest=A, household=1)` | N/A |
| Unknown code | 22 valid chars, no match | `None` | N/A |
| Wrong format | 21 or 23 chars, `""`, a char like `+` or `/` | `None`, no database query | N/A |
| Create, couple | `AdminActor` with role `couple`, 1–8 names | household (revision 0) + guests with fresh distinct codes | N/A |
| Create, helper | `AdminActor` with role `helper` | nothing written | `NotAllowed` |
| Create, 0 or 9 guests, or a blank name | system or couple actor | nothing written | `InvalidHousehold` (Norwegian message) |
| Fixed code | system actor, code in valid format | guest gets that code | N/A |
| Fixed code refused | couple actor with a code, or system actor with a badly formed code | nothing written | `InvalidHousehold` |

</frozen-after-approval>

## Code Map

- `wedding/models.py` -- has only `User` (role `couple`/`helper`); add the new models here (AD-1: all models in one file).
- `wedding/migrations/0001_initial.py` -- User only; add `0002` (schema, `makemigrations` output, Ruff-formatted) and `0003` (data). `tests/test_project_setup.py` already runs `makemigrations --check`.
- `wedding/links.py`, `wedding/services/__init__.py` -- docstring-only placeholders from Story 1.1 that say "arrives in Story 1.2"; update their docstrings.
- `tests/test_rules_purity.py` -- AST-scanner pattern (`utf-8-sig`, scanner tested on a bad `tmp_path` module) to reuse for the writer scan.
- No code in `config/`, `wedding/`, `guests/`, `dashboard/` calls `.save/.delete/.create/.update` today (grep, migrations excluded).
- Prices (PRD FR-32): cabin whole weekend, Friday dinner, Saturday breakfast, Sunday breakfast. Payment details (FR-64): Vipps number, account number.

## Tasks & Acceptance

**Execution:**
- [x] `wedding/models.py` -- `Household(revision PositiveIntegerField default 0)`; `Guest(household FK CASCADE related_name="guests", name ≤100, phone blank, email EmailField blank, code CharField(22, unique))`, ordered by id; `Settings` with `contact_1_name/phone`, `contact_2_name/phone`, `price_cabin_weekend`, `price_friday_dinner`, `price_saturday_breakfast`, `price_sunday_breakfast` (PositiveIntegerField), `rsvp_deadline` DateField, `vipps_number`, `account_number` (CharField, blank), and a `CheckConstraint(condition=Q(pk=1))` -- FR-1, FR-49, FR-64, AD-4, AD-9.
- [x] `wedding/migrations/0002_*.py`, `0003_settings_row.py` -- schema, then `RunPython` creating `Settings(pk=1)` with placeholders: names Rikke and Valdemar, blank phones/Vipps/account, prices 0, deadline 2028-01-04 (EXPERIENCE.md's example); reverse deletes it.
- [x] `wedding/actors.py` -- frozen dataclasses `GuestActor(guest, household)`, `AdminActor(user)` (`is_couple`), `SystemActor`, and `SYSTEM`; no Django writes -- AD-3, AD-6.
- [x] `wedding/links.py` -- `CODE_LENGTH`, `is_code_format(code)`, `new_code()`, `resolve_code(code) -> GuestActor | None` (format check before query, `select_related`) -- AD-6, FR-1, FR-2.
- [x] `wedding/services/exceptions.py` -- `ServiceError` with a Norwegian `message`, `NotAllowed`, `InvalidHousehold`; `require_couple(actor)` in `wedding/services/permissions.py` -- AD-10.
- [x] `wedding/services/households.py` -- `create_household(actor, guests: list[NewGuest]) -> Household`; `NewGuest(name, phone="", email="", code=None)`; system or couple only; validate count, names, fixed codes; atomic -- AD-3, AD-6, FR-49.
- [x] `wedding/rules/households.py` -- `MAX_HOUSEHOLD_SIZE = 8`, `household_size_problem(count) -> str | None` (pure) -- AD-8 cap.
- [x] `tests/test_links.py`, `tests/test_households.py`, `tests/test_settings_model.py` -- every matrix row; codes distinct across 50 guests; actor of household 1 exposes no household-2 guest; `resolve_code` runs only SELECT queries and changes no row counts (`CaptureQueriesContext`); `Settings` row exists after migrate, a second row is refused, migration reverse works; rule bounds 0/1/8/9.
- [x] `tests/test_only_services_write.py` -- AST scan of `config/`, `wedding/`, `guests/`, `dashboard/` (excluding `wedding/services/`, `migrations/`) for calls to `save`, `delete`, `create`, `get_or_create`, `update_or_create`, `bulk_create`, `bulk_update`, `update`; scanner tested on a bad `tmp_path` module -- AD-3.
- [x] `ARCHITECTURE-SPINE.md` (Structural Seed + change note), `epics.md` (Story 1.5 AC + change-log row), `README.md` (folder tree) -- record `wedding/actors.py` and the HTTP-level FR-3 test moving to 1.5.
- [ ] `sprint-status.yaml` -- story 1.2 status as the workflow moves.

**Acceptance Criteria:**
- Given a fresh database, when `uv run manage.py migrate` runs, then exactly one `Settings` row exists and only `Household`, `Guest`, `Settings` tables were added.
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check`, `uv run djlint --check .` run, then all pass.

## Design Notes

FR-3 is tested at the resolver here because no guest view exists until Story 1.5; Story 1.5 gets an AC to repeat the test over HTTP GET. The writer scan flags every listed method name on any receiver; nothing outside services matches today, so it has no allow list. A later false positive (say `dict.update`) is narrowed in the story that meets it. A random 128-bit code collides with negligible probability, so `new_code()` does not retry; the unique constraint is the backstop.

## Verification

**Commands:**
- `uv run manage.py migrate && uv run manage.py makemigrations --check --dry-run` -- expected: no changes
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0

## Implementation Notes

- **Commits:** models and `0002` → `0003` data migration with `test_settings_model.py` → size rule → `actors.py` → `links.py` with `test_links.py` → services with `test_households.py` → writer scan → epics (FR-3 over HTTP in 1.5) → architecture (`actors.py`) → README.
- **Beyond the matrix, small and inside the intent:** `create_household` also refuses a name over 100 characters (SQLite does not enforce `max_length`) and a fixed code already in use or repeated in the same call, with `InvalidHousehold` instead of a raw `IntegrityError`. Names, phones and emails are stored stripped. Tests added for a code that differs only in letter case and for a failure halfway through (the transaction leaves no household).
- **Field sizes the spec left open:** phones 30 characters (`PHONE_MAX_LENGTH`), Vipps and account number 20. `Guest.code` is `max_length=22` as a literal, because `links.py` imports the models; a test keeps it equal to `CODE_LENGTH`.
- **Ruff RUF012:** `Meta.ordering` and `Meta.constraints` are tuples, not lists, so the migration was generated from the tuple form.
- **Reverse test:** reversing a migration on SQLite needs `django_db(transaction=True)`; `serialized_rollback=True` restores the migrated row first, so the test starts from a fresh `migrate`.
- **Not done here:** `sprint-status.yaml` is left at `in-progress` for the workflow to move. No session log was written by the implementing sub-agent; the main session logs the story.
- **Task verification (orchestrator):** diff read against the spec; every matrix row has a passing test; 103 tests passed, none skipped.
- **Review pass 1 patches** (31bcd61..26d875e): phone ≤ 30 and email format checked in `_validate_guests`; trimming test with edge spaces; «To personer kan ikke ha samme lenkekode.» for a repeated fixed code; `Actor` alias in `actors.py` used by `create_household` and `require_couple`; writer-scan docstrings say exactly what is scanned; reverse test cites the Story 1.2 AC, not FR-3; the epics change-log row says Claude decided. Sprint-status set to `review` by the orchestrator. After patches: 106 tests pass, Ruff, djLint and `makemigrations --check` clean.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-16): Blind Hunter (B), Edge Case Hunter (E), Verification Gap (V).

| # | Layer | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|---|
| 1 | V | Phone and email trimming has no test | low | Pre-verified: the test input has no edge spaces on phone or email, so dropping `.strip()` keeps it green | patch |
| 2 | V, B, E | Phone over 30 chars and malformed email are stored silently | medium | `objects.create` runs no validators and SQLite ignores `max_length`; the service already checks name length for the same reason, so contact data is inconsistent | patch |
| 3 | V, B, E | Writer scan misses related-manager writes (`add`, `set`, …) and raw SQL | low | True, but no such call exists, AD-5 forbids raw SQL, and adding `add`/`set`/`clear` would flag `set.add`, `dict.clear`; the docstrings overclaim "fails if code … writes" | patch (docstrings say exactly what is scanned) |
| 4 | B | Spec says `in-review`, sprint-status says `in-progress` | low | `sprint-status.yaml` line 40 | patch (orchestrator: `review`) |
| 5 | B | No session log or record of steering | false | Written at the end of the session by `sesjonslogg`, as CLAUDE.md requires; the technical choices are recorded in this spec, which Rikke approved | reject |
| 6 | B, E | Raw `IntegrityError` can escape (code collision, race between `exists()` and `create`) | false | `transaction_mode: IMMEDIATE` (AD-5) takes the write lock at `BEGIN`, so no other writer runs between check and insert; a 128-bit collision is negligible (Design Notes) | reject |
| 7 | B, E | `require_couple` lets an inactive couple user through | low | `ModelBackend` refuses inactive users at login and `get_user`, so an inactive user never becomes an `AdminActor`; fix adds a guard | reject |
| 8 | B | Actors typed `object`; no `Actor` alias | low | Every later service signature will repeat `object`, hiding the AD-3 contract; direct correction | patch |
| 9 | B, E | `GuestActor` does not check `guest.household == household` | low | Only `resolve_code` builds one (AD-6: one resolver); fix adds a guard | reject |
| 10 | B | FR-3 cited for the migration-reverse test | low | Reversibility is not FR-3; the `0003` docstring is right (epics AC ties the row to FR-3) | patch (test docstring only) |
| 11 | B | Spec logs empty; epics change-log row does not say who decided | low | Spec part edits this build's spec (reject); epics row lacks "Claude decided", unlike earlier rows | patch (epics row only) |
| 12 | B | Implementation note says `constraints` is a tuple in the migration; it is a list | low | True, but the fix edits this build's spec | reject |
| 13 | B | Same fixed code twice in one call says «allerede i bruk» | low | Not yet in use; misleads a seed-file author in Story 1.3; direct text correction | patch |
| 14 | B | README gives no way to inspect the data or the placeholder settings | low | Nothing user-visible yet; Story 1.3 adds the seed command and test links to the README | reject |
| 15 | E | Name of only zero-width/control characters passes | low | Unlikely from the couple or the seed file; fix adds a guard | reject |
| 16 | E | `None` phone/email raises `AttributeError` | false | `NewGuest` defaults are `""`; callers are typed internal code, and failing loudly on input never shown reachable is correct | reject |
| 17 | E | Any code can pass `SYSTEM` and skip the role check | low | AD-3 limits it to the seed command by convention and review; a runtime guard would need caller inspection | reject |
| 18 | E | Transactional reverse test flushes the `Settings` row for later transactional tests or `--reuse-db` | low | pytest-django runs transactional tests last and the README runs without `--reuse-db`; already noted in Implementation Notes for later stories | reject |
