---
title: 'Story 2.6d: Test data with answers, and a real-browser send'
type: 'feature'
created: '2026-11-25'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-6c-a-send-that-fails-or-repeats-is-safe.md'
warnings:
  - oversized
deferred: []
---

<intent-contract>

## Intent

**Problem:** `seed_testdata` loads households but none of the answers, allergies and consents written in `seed.toml`, so the admin numbers of Epic 3 have nothing to count. Three loose ends from earlier stories sit on the seed: it keeps `Submission` rows pointing at answers it deleted (2.6c), it silently overwrites the one `Settings` row while its help says it replaces only its own test data, and its «Fant ikke eller kunne ikke lese» path and role labels are untested (epic 1 retro).

**Approach:** After creating the households, the command builds an `Answer` per answered household from `seed.toml` and sends it through `send_answer` with the system actor (FR-68, AD-3, AD-16). The reset service also removes the test households' `Submission` rows. The settings replacement is stated plainly in the help, output and README. The manual test plan gets one real-browser send on the unanswered seeded household (Mona).

## Boundaries & Constraints

**Always:**
- Answers go only through `send_answer(SYSTEM, household=…, respondent=<answered_by guest id>, answer=…, now=timezone.now(), submission=uuid4(), revision=household.revision, shown_total=household_total(answer, form_prices(settings)), consent_version=CONSENT_TEXT_VERSION)`, inside the command's existing `transaction.atomic()`; a `ServiceError` keeps the «Testdata ble ikke lagt inn … Ingenting ble endret.» path.
- Mapping per guest (seed field → `Answer`): `coming` → `attendance`; `whole` = True when every coming guest has `days == ["fri","sat","sun"]`, else False with `days` set for every coming guest; `overnight` → `night`; `meals` → `meals`; `hike` → `hike` (only when present); `no_allergies`/`allergy_categories`/`allergy_note` → `AllergyEntry(cats=tuple(...), none=..., note=...)`; `consent` «yes»/«no» → True/False (absent: no entry); a guest whose `consent` is given by `consent_by` ≠ themselves goes into `confirmed` (FR-27). `consent_by` must equal the household's `answered_by` (the respondent records consent, FR-29); otherwise raise `CommandError` naming the key, before writing.
- Households without `answered_by` (Mona) stay unanswered. `consent_withdrawn` is ignored here (Story 7.2), as are `payment_report`/`payments` (Story 5.2).
- `reset_test_data` deletes `Submission` rows with `kind=ANSWER` whose `object_id` is a `HouseholdAnswer` of a test household, before deleting the households (AD-4, AD-20). Rows for real households stay.
- The command keeps replacing the `Settings` row every run (the deadline must be 30 days from today so the form is open, epics 1.3), and says so: help text and a printed line «Innstillingene er erstattet med testverdiene fra seed.toml.» Module docstrings state it too.
- Every function and test docstring names its FR/AD ids. UI/output text Norwegian, code English.

**Never:**
- No new model, migration, view or template change; no change to `send_answer`, the rules, `seed.toml` data or `expected.toml`.
- No hidden command option for tests; no direct `PersonAnswer`/`Allergy`/`Consent` writes in the command.
- The implementer does not run a browser; the orchestrator runs the MT row.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| First run | empty DB | 6 `HouseholdAnswer` (all but Mona), 6 `Submission` (`answer`), every household `revision` 1 except Mona 0; `PersonAnswer` for all 12 guests of answered households | — |
| Second run | after a run, plus a real couple household with a sent answer | still 6 test `Submission`s, each `object_id` is an existing `HouseholdAnswer`; the real household's answer and `Submission` untouched; printout identical | — |
| Allergies | first run | `Allergy` for Sigmund (none), bestemor (gluten), Arild (none), Eva (shellfish, other, note «Tåler ikke koriander.»), Jonas (none), Synne (nuts); none for Marie, Filippa, Ida, Leone, Tor, Hilde, Mona, Geir | — |
| Consents | first run | `given`: Sigmund, bestemor (given_by Sigmund), Arild, Eva, Jonas, Synne; `refused`: Filippa (given_by Arild), Ida (given_by Jonas); all `text_version` = `CONSENT_TEXT_VERSION` | — |
| Totals | first run | `household_total` of the stored answers equals `expected.toml` `households.<key>.total` for every answered household (sigmund 4720, arild 6480, synne 0, tor 0, eva 1840, jonas 4200) | — |
| Bad consent_by | seed with `consent_by` ≠ `answered_by` (tmp file via monkeypatched `SEED_PATH`) | `CommandError` naming the guest key; snapshot unchanged | nothing written |
| Missing / invalid seed.toml | `SEED_PATH` to a missing file; to a file with `not = toml =` | `CommandError` starting «Fant ikke eller kunne ikke lese»; snapshot unchanged | nothing written |

</intent-contract>

## Code Map

- `wedding/management/commands/seed_testdata.py:1-12` docstring (Story 2.6d loads answers; settings replaced); `:41-45` help; `:47-90` `handle` — `create_household` returns the `Household`; keep a key→household and key→guest-id map, then send answers after the users; `:92-106` `print_summary` (add the settings line; role labels from `ROLE_NAMES` `:36`); `:128-134` `load_seed`. Add a pure helper `seed_answer(household_seed, ids) -> (respondent_id, Answer)` here (or a small module next to it) so tests can call it.
- `wedding/services/answers.py:108-215` `send_answer` — reuse, read-only. System actor skips the deadline; revision check needs `household.revision` (0 after create).
- `wedding/rules/answer.py:36-58` `Answer`; `wedding/rules/allergies.py:27-35` `AllergyEntry`; `wedding/rules/money.py` `household_total`; `wedding/selectors.py:91` `form_prices`; `wedding/services/consent.py:12` `CONSENT_TEXT_VERSION`.
- `wedding/services/testdata.py:1-26` — add the `Submission` delete; docstring.
- `wedding/models.py:126-145` `HouseholdAnswer` (cascades with household), `:234` `Consent.guest` cascade, `:265-286` `Submission` (`object_id` plain int, so it does not cascade).
- `wedding/fixtures/seed.toml:7-12` header comment («Story 1.3 loads …»; answers now loaded by 2.6d). `wedding/fixtures/expected.toml:57,67` Synne: nuts 0 / nothing_stored hold only after Story 7.2 loads the withdrawal.
- `tests/conftest.py:38-41` `seeded` — used by ~20 form/send test files that assume Sigmund's household is unanswered at revision 0. Keep `seeded` as that state: run the command, then delete `Submission`, `HouseholdAnswer`, `PersonAnswer`, `Allergy`, `Consent` and set every `Household.revision` to 0 (docstring says why: form tests start before any answer, as before 2.6d). Add `seeded_with_answers` = the plain command.
- `tests/test_seed_testdata.py:25-58` helpers (`seed()`, `snapshot()` — add `HouseholdAnswer`, `Submission`, `Consent` counts), `:120-133` print test, `:136-159` second-run test, `:205-228` monkeypatched `SEED_PATH` pattern to reuse.
- Docs: `README.md:9` status, `:37-43` seed section, `:75`; `docs/manual-test-plan.md` after MT-49 (`:71`); `ARCHITECTURE-SPINE.md` AD-16 (`:214`); `.docs/implementation-artifacts/deferred-work.md:98`, `:268`; `.docs/implementation-artifacts/sprint-status.yaml:145-151`; `.logs/rikke/issues.md:99`.

## Tasks & Acceptance

**Execution:**
- [ ] `wedding/management/commands/seed_testdata.py` -- build and send each answered household's `Answer` per Always; validate `consent_by` before any write; help, docstring and printed settings line -- FR-68, AD-3, AD-16.
- [ ] `wedding/services/testdata.py` -- delete the test households' answer `Submission`s first -- AD-4, AD-20, closes deferred `:268`.
- [ ] `tests/conftest.py` -- `seeded` (unanswered, revision 0) and `seeded_with_answers` per Code Map.
- [ ] `tests/test_seed_testdata.py` -- every matrix row; per guest `PersonAnswer` fields equal `seed.toml` (coming, days, cabin, meals, hike); `HouseholdAnswer.sent_by_name` = the `answered_by` guest's name; Mona/Geir have no `PersonAnswer`; print contains «(brudeparet)» and «(hjelper)» on the testpar/testhjelper lines and the settings line; missing and invalid `seed.toml`; a pre-existing real `HouseholdAnswer` + `Submission` survive a second run. Tests for the pure mapping helper (whole True/False, confirmed, consent absent).
- [ ] `wedding/fixtures/seed.toml`, `wedding/fixtures/expected.toml` -- comments only: who loads what now; Synne's nuts/nothing_stored hold after Story 7.2.
- [ ] `docs/manual-test-plan.md` -- row MT-50 (below) with date and result empty; a dated note above MT-45 that from 2.6d Sigmund's household is seeded as answered (revision 1), so re-runs of MT-36–49 see revisions one higher.
- [ ] `README.md` -- status sentence (story 2.6d: seeded households have answers, allergies and consents, except Mona/Geir); seed section: settings are replaced every run, answers sent through the send service, old submissions removed; `:75` now names only 5.2 and 7.2 as later.
- [ ] `ARCHITECTURE-SPINE.md` AD-16 -- dated note (2026-11-25, Story 2.6d): answers loaded through `send_answer` with the system actor; reset removes `Submission`s; the seed replaces `Settings` on purpose (fresh deadline), stated in help and output.
- [ ] `.docs/implementation-artifacts/deferred-work.md` -- status «done in Story 2.6d» on `:98` (settings: stated plainly, with reason) and `:268`, naming files; new entry for Story 3.5: Synne's nut allergy and consent are stored until Story 7.2 loads the withdrawal, so 3.5's counts against `expected.toml` must load the withdrawal first or be ordered after 7.2.
- [ ] `.docs/implementation-artifacts/sprint-status.yaml` -- `epic-1-retro-item-5`: append «2.6d part done 2026-11-25» to the action and keep `status: open` (the 4.5 part remains). `.logs/rikke/issues.md:99` -- tick, citing story 2.6d.

**MT-50 (Norwegian, «Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`)»):** Kjør `uv run manage.py seed_testdata` og `uv run manage.py runserver`. Mål etter `document.fonts.ready`. Åpne `http://127.0.0.1:8000/test-mona0000000000000/svar/`: «Kommer» for Mona og Geir, «Fortsett»; «Ja» (hele helgen), «Fortsett»; «Ja» for begge på overnatting, «Fortsett»; ingen måltider, «Fortsett»; steg 5 uten valg, «Fortsett»; «Nei» for begge på fjellturen, «Fortsett»; på `/svar/se-over/` klikk «Send svaret». Så `uv run manage.py shell -c` som leser radene, og til slutt `seed_testdata` på nytt. Forventet: «Totalt for husstanden» 3 000 kr på «Se over svaret»; ender på `/svar/sendt/` med «Sendt av Mona»; `shell`: Monas husstand har ett `HouseholdAnswer` (`sent_by_name` «Mona»), `revision` 1, to `PersonAnswer` med `coming` og `cabin` sann, ingen `Allergy`/`Consent` for Mona og Geir, `Submission.objects.count()` 7 og den nyeste peker på Monas svar; etter ny `seed_testdata`: 6 `Submission`, Mona uten svar. Ingen layout endres, så ingen 20px-sjekk.

**Acceptance Criteria:**
- Given an empty local database, when `uv run manage.py seed_testdata` runs, then the stored answers, allergies and consents match `seed.toml` (except the withdrawal, 7.2) and each answered household's total equals `expected.toml`.
- Given the command has run and a real household has sent an answer, when it runs again, then the printout is identical, there are 6 test `Submission`s all pointing at existing answers, and the real answer and its `Submission` are unchanged.
- Given the command runs, when its output is read, then it says the settings were replaced and labels the users «(brudeparet)» and «(hjelper)».
- Given a missing or unreadable `seed.toml`, when the command runs, then it stops with «Fant ikke eller kunne ikke lese …» and nothing is written.
- Given the manual test plan, when this story is done, then MT-50 records one real-browser send on a seeded guest link.

## Spec Change Log

## Review Triage Log

## Design Notes

- **Why settings stay replaced:** writing them only over the migration placeholders would freeze the deadline at the first run's date + 30, so a re-run a month later gives a closed form, against epics 1.3 («a deadline relative to today so the form is open»). The seed runs only with `APP_ENV=local` (FR-72), so the honest fix is to say it plainly.
- **Why `seeded` strips answers:** ~20 test files drive Sigmund's form from an unanswered household; the fixture keeps that start state explicitly instead of each test changing revision and counts. `seeded_with_answers` and `test_seed_testdata.py` cover the real seed.
- **Why Mona for MT-50:** the only seeded household with no answer, so the browser send is a first send and the rows are easy to tell apart.

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes.
