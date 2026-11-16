---
title: 'Story 1.3: Fictional test data and the hand-made expected-results list'
type: 'feature'
created: '2026-11-16'
status: 'in-progress'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '4445e1032ca59c16cd991d3abfc96699a141228d'
context:
  - '{project-root}/.docs/implementation-artifacts/epic-1-context.md'
  - '{project-root}/.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The examiner has no guests to try and later stories have no fixed data or hand-made results to check their numbers against (FR-47 test accounts, FR-68, FR-69, FR-72, NFR-3, AD-14, AD-16).

**Approach:** Write `wedding/fixtures/seed.toml` (people, settings, planned answers, payments) and a hand-worked `wedding/fixtures/expected.toml`, then a `seed_testdata` command that resets earlier test data and rebuilds households, guests, settings and two test admins through services with the system actor.

## Boundaries & Constraints

**Always:** Prices (2026 level, fictional): cabin 1500, Friday dinner 340, Saturday breakfast 260, Sunday breakfast 260. Deadline = today (Oslo) + 30 days. Contacts Rikke and Valdemar with impossible numbers (`+47 000 00 1xx`); other phones the same form, emails `@example.com`, Vipps `00000`, an account number failing MOD11. Fixed codes `test-<name>` padded with `0` to 22 chars. Logins `testpar` (couple) and `testhjelper` (helper), password `bryllup-test-2028`. Rows the system actor creates are test data (`is_test_data=True` on `Household` and `User`); reset deletes only those. Commit order: `seed.toml` → `expected.toml` alone (message gives the method) → code. Docstrings name FR/AD.

**Decision (Rikke, 2026-11-16):** `expected.toml` is worked out by Claude from the table below, worked out again by a separate subagent that never sees Claude's numbers, differences resolved, and then Rikke checks a few numbers herself before the commit. The commit message records all three steps. **Decision (Rikke, 2026-11-16):** a household that has not answered has no payment status; it shows as «Ikke svart» (`not_answered` in `expected.toml`), not «Ingenting å betale» (FR-60 updated).

**Never:** no answer, allergy, consent, payment or report tables (Stories 2.6c, 2.6d, 5.2, 7.2) — those parts of `seed.toml` are data only, not loaded; no code that computes counts or totals; no `loaddata`/fixtures JSON; no writes outside `wedding/services/`.

**Households** (all answers sent by the first-named person; meals: F = Friday dinner, LB = Saturday breakfast, SB = Sunday breakfast; hike asked only of those present Friday):

| Key | People: days, overnight, meals, hike, allergy | Payments |
|---|---|---|
| sigmund | Sigmund fri–sun, yes, F LB SB, no, «no allergies» + consent · bestemor fri–sun, yes, F LB SB, maybe, gluten + consent (given by Sigmund) | report 4720 Vipps; received 4720 |
| arild | Arild fri–sun, yes, F LB SB, yes, «no allergies» + consent · Marie fri–sun, yes, F LB SB, yes, unanswered · Filippa sat–sun, yes, SB, —, vegetarian without consent · Leone not coming | report 4000 bank, paid by Marie; received 4000 |
| synne | Synne sat only, no, none, —, nuts + consent, later withdrawn | none |
| tor | Tor and Hilde, not coming | none |
| eva | Eva fri–sun, yes, F, yes, shellfish + other («tåler ikke koriander») + consent | received 2300, refunded 200 |
| jonas | Jonas fri–sat, yes, F LB, maybe, «no allergies» + consent · Ida fri–sat, yes, F LB, no, «no allergies» without consent | report 4200 Vipps; nothing received |
| mona | Mona and Geir, not answered | none |

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| First run | migrated empty DB, `APP_ENV` unset | 7 households, 14 guests, 2 test users, settings from `seed.toml`; prints each guest's name and `http://127.0.0.1:8000/<code>/` and both logins | N/A |
| Second run | test data present, plus one couple-made household | same result as first run; couple-made household untouched | N/A |
| Code taken | a non-test guest holds a `seed.toml` code | nothing written | `CommandError` naming the code |
| Username taken | non-test user named `testpar` | nothing written | `CommandError` naming the user |
| Wrong env | `APP_ENV` = `production`, `prod` or `Local` | nothing written | `CommandError`: runs only with `APP_ENV` unset or `local` |
| Settings, helper | `update_settings` with a helper actor | nothing written | `NotAllowed` |

</frozen-after-approval>

## Code Map

- `wedding/services/households.py` -- `create_household(actor, guests: list[NewGuest])`, `NewGuest(name, phone, email, code)`; system actor may set fixed codes. Extend: set `is_test_data` when the actor is `SystemActor`.
- `wedding/actors.py` -- `SYSTEM`, `SystemActor`, `AdminActor`, `Actor` alias.
- `wedding/services/permissions.py` -- `require_couple`; `wedding/services/exceptions.py` -- `ServiceError`, `NotAllowed`, `InvalidHousehold` (add `InvalidSettings`).
- `wedding/models.py` -- `User.Role`, `Household`, `Guest`, `Settings` (single row pk=1, created by migration `0003`; fields listed in its docstring).
- `wedding/links.py` -- `is_code_format`, `CODE_LENGTH`.
- `config/env.py` -- `APP_ENVS`, `validate_app_env` (raises on a misspelled value; settings already refuse to start with one, so the command must also read `os.environ` itself).
- `wedding/selectors.py` -- placeholder; put the read-only conflict check here.
- `tests/test_only_services_write.py` -- will scan the new command; it must only call services.
- `README.md` -- status line, folder note («`management/commands/` og `fixtures/` er tomme»); add a test-data section.
- `wedding/fixtures/.gitkeep`, `wedding/management/commands/__init__.py` -- exist.

## Tasks & Acceptance

**Execution:**
- [x] `wedding/fixtures/seed.toml` -- settings, users and the households table above as data, keyed by household and guest key, with planned answers, allergies, consents, reports and payments -- FR-68.
- [x] `wedding/fixtures/expected.toml` -- hand-worked: every FR-54 count (households and people coming/not/unanswered, whole weekend and per day pattern, not staying and beds, each meal incl. Saturday lunch and dinner, each allergy category, the three AD-18 states, hike yes/maybe/no, payment status among coming households), per-household total, payment status, missing/refund amount and report match, per-guest allergy state, and lock cases as offsets from the deadline (day before 12:00 open, deadline 23:59:59 open, next day 00:00:00 locked, +7 days locked) -- FR-69, AD-16.
- [x] `wedding/models.py` + `wedding/migrations/0004_*.py` -- `is_test_data` BooleanField default False on `Household` and `User` -- FR-72.
- [x] `wedding/services/users.py` -- `create_admin_user(actor, username, password, role)`; system actor only for now (Story 3.1 adds its command), marks test data -- FR-47, AD-10.
- [x] `wedding/services/settings.py` -- `update_settings(actor, values: SettingsValues)`; system or couple; validates prices ≥ 0 and field lengths -- FR-64, AD-12.
- [x] `wedding/services/testdata.py` -- `reset_test_data(actor)`: system only, deletes test households (guests cascade) and test users; docstring says Story 5.2 voids payments first -- AD-4, AD-16.
- [x] `wedding/selectors.py` -- `test_data_conflicts(codes, usernames) -> list[str]` for non-test rows using them.
- [x] `wedding/management/commands/seed_testdata.py` -- env guard, load TOML, conflict check, then reset + settings + households + users in one `transaction.atomic()`, then print -- FR-68, FR-72, AD-14.
- [x] `tests/test_seed_testdata.py`, `tests/test_seed_files.py`, `tests/test_settings_service.py`, `tests/test_users_service.py` -- every matrix row; NFR-3 checks (emails, phones, MOD11 fails); codes valid and unique; every seed household and guest has an `expected.toml` entry; every FR-68 case present; no household over 8.
- [x] `ARCHITECTURE-SPINE.md` -- AD-4 stored list and AD-16: `is_test_data`, with a change note.
- [x] `README.md` -- command, test link per guest (open from Story 1.5), logins (usable from Story 3.1), status line.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check`, `uv run djlint --check .` and `uv run manage.py makemigrations --check --dry-run` run, then all pass.
- Given `git log`, when the story's commits are read, then `expected.toml` is added in its own commit before the command code, with the method in the message.

## Implementation Notes

- **Data files done by the orchestrator (do not edit them):** `seed.toml` (commit 67bad24) and `expected.toml` (55a38e0, after the PRD FR-60 change in 9360654) are committed. Read `seed.toml`'s header for its fields: `[settings]` (with `deadline_days_from_today` instead of a date), `[[users]]` (`username`, `password`, `role`), `[[households]]` (`key`, optional `answered_by`, `payment_report`, `payments`) each with `[[households.guests]]` (`key`, `name`, optional `phone`, `email`, `code`, then answer fields). Story 1.3 loads only settings, users, households and guests' `name`/`phone`/`email`/`code`; ignore the answer and payment fields. `expected.toml` has `[counts.*]`, `[households.<key>]`, `[guests]` and `[[lock]]`; test only its structure against `seed.toml` (same household and guest keys, values from the allowed sets), never numbers computed by code.
- **Expected-results check:** Claude and an independent subagent agreed on every value; Rikke checked three samples and decided `not_answered` for Mona (see the commit message of 55a38e0).
- **Small additions while implementing:** `InvalidUser` in `exceptions.py` for refused accounts (blank or taken username, unknown role, no password). The env guard treats an empty `APP_ENV` as unset, like `config/env.py`, and also refuses when the loaded `settings.APP_ENV` is not `local`. `tests/conftest.py` switches tests to Django's MD5 hasher, because each seed run hashes two passwords and the seed tests took 30 s with the real one. `oversikt.md` got the AD-16 marker in Norwegian. With no URL patterns yet, the test links show Django's start page until Story 1.5; the README says so.

## Spec Change Log

## Review Triage Log

## Design Notes

A marker field instead of matching codes: matching `seed.toml` codes cannot tell a test user from a real user with the same name, and old seed households would be orphaned if a code changed. The system actor is used only by the seed command (AD-3), so "created by the system actor" equals "test data" without a separate flag argument.

## Verification

**Commands:**
- `uv run manage.py migrate && uv run manage.py seed_testdata && uv run manage.py seed_testdata` -- expected: same printout twice, exit 0
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0
</content>
</invoke>
