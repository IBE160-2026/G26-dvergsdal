---
title: 'Story 1.3: Fictional test data and the hand-made expected-results list'
type: 'feature'
created: '2026-11-16'
status: 'done'
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
- [x] `wedding/selectors.py` -- `seed_conflicts(codes, usernames) -> list[str]` for non-test rows using them.
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

- **Review pass 1 patches** (8e7b669..13b73ba): rollback test after the reset; env-guard message shows the failing value; selector renamed `seed_conflicts`; `SETTINGS_PK` dropped from the service; `expected.toml` self-tally test; epics FR-60 «Ikke svart» (Stories 3.5, 5.3, coverage); Story 3.1 AC and AD-16 sentence that real admin accounts never use the system actor; reset wording in README, AD-16 and `testdata.py`. Sprint status set to `review` by the orchestrator. After patches: 204 tests pass; Ruff, djLint and `makemigrations --check` clean; `seed_testdata` twice gives the same output.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-16): Blind Hunter (B), Edge Case Hunter (E), Verification Gap (V).

| # | Layer | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|---|
| 1 | V, B | No test makes a service fail after `reset_test_data` inside the atomic block, so «Ingenting ble endret.» is unverified on the one path where the reset has run | medium | Pre-verified: every "writes nothing" test refuses in the conflict check or env guard, before the reset | patch |
| 2 | V, B | FR-60 «not answered» reached the PRD but not epics.md (lines 884, 1195, 1722); `payment_status(total, received, refunded)` as planned cannot return it | medium | Story 5.3 is built from the epics and would give `nothing_to_pay` for Mona, against `expected.toml`; EXPERIENCE.md's panel counts coming households only, so it is unaffected | patch (epics only) |
| 3 | V, B | Env-guard message shows the environment value («» or «local») when it is `settings.APP_ENV` that caused the refusal | low | `require_local_env`: `shown` prefers `environ_value` whenever it is not None; direct correction | patch |
| 4 | B | Story 3.1's `create_admin` has no actor: `create_admin_user` is system-only and marks every account test data, so reusing `SYSTEM` would make Rikke's real accounts deletable by the next seed | medium | `users.py` sets `is_test_data=True` unconditionally; epics.md:842 plans the command with no actor named | patch (epics Story 3.1 AC + AD-16 note) |
| 5 | B | Reset deletes a whole test household, including a guest the couple later adds to it (Story 6.4), but README says it never touches what the couple made | low | `Household.objects.filter(is_test_data=True).delete()` cascades to every guest; wording fix is direct | patch (README + AD-16 wording) |
| 6 | B | Sprint status says `in-progress` while the spec is `in-review` | low | sprint-status.yaml; set to `review` by the orchestrator | patch (orchestrator) |
| 7 | B | Selector named `test_data_conflicts` is collected by pytest when imported by name | low | pytest collects module-level `test_*` functions from test modules; rename is direct | patch |
| 8 | B | Nothing checks that `expected.toml` agrees with itself (counts vs its own `[guests]` and `[households]` tables, sub-counts summing) | low | Pure tallies of the file, allowed by AD-16; catches a typo in a later deliberate oracle change | patch |
| 9 | B | `SETTINGS_PK = 1` duplicated in `services/settings.py` (also in migration 0003 and the model constraint) | low | The migration must not import app code; the service can use `Settings.objects.get()` like guest views will | patch (service only) |
| 10 | E, B | `_validated` raises `AttributeError` on a non-string text value | low | Only reachable by editing `seed.toml` badly; a traceback there is a loud failure, and a type guard adds a branch | reject |
| 11 | E | Missing settings row (after `flush`) gives `DoesNotExist` | low | Migration 0003 creates it; `flush` breaks the whole app, not just the seed | reject |
| 12 | E | Price above the integer maximum overflows | low | Only by editing `seed.toml`; adds a guard | reject |
| 13 | E | Missing key or wrong type in `seed.toml` gives a traceback | low | Developer-edited fixture; a loud `KeyError` names the key | reject |
| 14 | E | Negative or huge `deadline_days_from_today` | low | Developer-edited fixture; a test pins it at 30 | reject |
| 15 | E | Empty households list crashes `max()` | low | `seed.toml` has 7 and a test requires every FR-68 case | reject |
| 16 | E | Race between `exists()` and `create_user` | false | `transaction_mode: IMMEDIATE` takes the write lock at `BEGIN` (AD-5) | reject |
| 17 | E | Whitespace-only password accepted | low | Django allows any password; real-account password rules belong to Story 3.1's command and validators | reject |
| 18 | E | Deadline tests can fail when run across Oslo midnight | low | A one-second window; a fix needs time patching | reject |
| 19 | B | Seed plausibility (meals vs days, `no_allergies` with categories) not checked | low | Story 2.6d loads the answers through `send_answer`, which validates them | reject |
| 20 | B | README link table can drift from `seed.toml` | low | Codes are fixed by design (AD-6) and a test pins the `test-<key>` form; a README test adds coupling | reject |
| 21 | B | Spec decision placed in **Always**; change log empty | low | The fix edits this build's spec | reject |
| 22 | B | No session log or KI-steering entry yet | false | Written at the end of the session by `sesjonslogg`, as CLAUDE.md requires | reject |

## Design Notes

A marker field instead of matching codes: matching `seed.toml` codes cannot tell a test user from a real user with the same name, and old seed households would be orphaned if a code changed. The system actor is used only by the seed command (AD-3), so "created by the system actor" equals "test data" without a separate flag argument.

## Verification

**Commands:**
- `uv run manage.py migrate && uv run manage.py seed_testdata && uv run manage.py seed_testdata` -- expected: same printout twice, exit 0
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check && uv run djlint --check .` -- expected: exit 0
