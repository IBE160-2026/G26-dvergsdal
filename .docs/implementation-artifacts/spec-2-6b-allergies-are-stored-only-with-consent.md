---
title: 'Story 2.6b: Allergies are stored only with consent'
type: 'feature'
created: '2026-11-24'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-6a-send-the-answer.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-4-allergies-and-consent.md'
warnings:
  - oversized
deferred: []
---

<intent-contract>

## Intent

**Problem:** `send_answer` (Story 2.6a) writes days, cabin, meals and hike, but drops step 5: allergies and the per-person consent from the draft (`alg`, `cons`, `conf`) never reach the database, and no consent is recorded (FR-26, FR-28, FR-29, NFR-3, AD-18; deferred-work «From Story 2.4»).

**Approach:** Add `Allergy` (current allergy data, one per guest) and `Consent` (append-only events: given, refused, withdrawn; who, when, `CONSENT_TEXT_VERSION`) in migration `0006`. A pure rule decides each guest's outcome (store / delete / keep) from the normalised answer, and `send_answer` applies it in its existing transaction, so allergy data exists only for guests whose consent on that send is «Ja».

## Boundaries & Constraints

**Always:**
- **Models (AD-4, AD-18, FR-29), migration `0006_allergy_consent.py`:** `Allergy` — `guest` OneToOne `Guest` (CASCADE, `related_name="allergy"`), one BooleanField per `ALLERGY_KEYS` key (`gluten`, `lactose`, `nuts`, `shellfish`, `vegetarian`, `vegan`, `other`, default False), `none` bool («Ingen allergier eller matbehov»), `note` CharField(`NOTE_MAX`, blank). `Consent` — `guest` FK `Guest` (CASCADE, `related_name="consents"`), `event` CharField choices `given`/`refused`/`withdrawn` (labels «gitt», «nektet», «trukket tilbake»), `at` DateTimeField, `given_by` FK `Guest` (SET_NULL, null, `related_name="+"`; the respondent), `given_by_user` FK `User` (SET_NULL, null, `related_name="+"`; for the couple's override in 4.4, null now), `given_by_name` CharField(100) (name as text, kept), `text_version` CharField(20). Norwegian `verbose_name`s; `__str__` without names or allergy content (e.g. «Allergi for gjest <id>», «Samtykke <id>»). Docstrings name Story 2.6b, FR-26, FR-29, AD-18. Nothing derived stored.
- **Rule (AD-2, AD-18), `wedding/rules/allergies.py`:** constants `STORE`, `DELETE`, `KEEP` and `consent_outcomes(guest_ids, coming, allergies, consent) -> dict[int, str]`: for a guest not coming → `DELETE` (FR-75, NFR-3: no health data kept for someone who no longer comes); coming with consent True → `STORE`; False → `DELETE`; no entry → `KEEP` (AD-18 «unanswered on a re-send means unchanged»). Pure; add to `tests/test_rules_purity.py`.
- **Service (FR-26, FR-29, AD-3, AD-18), `wedding/services/answers.py`:** inside the existing `atomic()` after the `PersonAnswer` loop, on the normalised answer: first, if any coming guest has `allergy_problems(entry, consent, guest_id in confirmed, guest_id == respondent)` non-empty, raise `InvalidAnswer` before any write (move the check before the `PersonAnswer` loop so a refusal writes nothing). Then per guest by `consent_outcomes`: `STORE` → `update_or_create` `Allergy` from the entry when `has_allergy_info`, else delete any `Allergy` (a «Ja» with nothing entered means nothing to keep); `DELETE` → delete any `Allergy`; `KEEP` → touch nothing. For every coming guest whose consent is True or False, create one `Consent` (`given`/`refused`, `at=now`, `given_by` = respondent guest, `given_by_name` = their name, `text_version=CONSENT_TEXT_VERSION` from `wedding/services/consent.py`). No `Consent` row for unanswered or not coming. Module and function docstrings updated (Story 2.6b part).
- **FR-28 on re-send:** the check page's existing warning (`not_saved`, `AllergiesForm.warning_text`: «… blir ikke lagret uten et «Ja» til samtykke …») already names every coming person with allergy information entered and consent not «Ja», which is exactly «changed fields without a consent answer»; no new text. A view test proves it on a re-send.
- Privacy and quality: no names, categories or notes in logs, exceptions or `__str__`; not registered in Django admin (the couple's views are Epic 3/7); only `wedding/services/` writes (`tests/test_only_services_write.py` stays green); every new rule, service, model and test names its FR/NFR/AD.

**Never:**
- No draft-format change (stays 5): recording the consent-text version the guest saw on step 5 moves to Story 2.6c, which bumps the draft format once for both the total snapshot and that version (see Design Notes).
- No revision-conflict refusal, `Submission`, total snapshot or failed-send handling (2.6c); no seeded answers with allergies (2.6d); no receipt lines (2.7); no withdrawal flow or «Personvern» link (7.1/7.2); no admin allergy states or kitchen list (Epic 3).
- No change to step 5 texts, `CONSENT_TEXT_VERSION`, the consent template, or `normalise_answer`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Respondent Ja | Sigmund (respondent) gluten + note, consent Ja | `Allergy` gluten, note; `Consent` given, by Sigmund, version `2026-11-23` | none |
| Other member Ja, confirmed | bestemor lactose, Ja, confirmed | `Allergy` for bestemor; `Consent` given by Sigmund | none |
| Other member Ja, not confirmed | as above, not in `confirmed` (service called directly) | nothing written at all | `InvalidAnswer` |
| Nei, first send | bestemor nuts, Nei | no `Allergy`; `Consent` refused | none |
| Unanswered, first send | info entered, no consent | no `Allergy`, no `Consent` | none |
| «Ingen …» with Ja | `none` True, Ja | `Allergy` with `none` True, all keys False | none |
| «Ingen …» with Nei / unanswered | | no `Allergy` | none |
| Ja, nothing entered | consent Ja, empty entry | no `Allergy` (existing one deleted); `Consent` given | none |
| Re-send, unanswered | stored `Allergy`; new draft changes entry, consent unanswered | `Allergy` unchanged; no new `Consent` | none |
| Re-send, Nei | stored `Allergy`; consent Nei | `Allergy` deleted; new `Consent` refused (earlier rows kept) | none |
| Re-send, Ja with new data | stored gluten; now lactose, Ja | `Allergy` replaced by lactose; new `Consent` given | none |
| Stops coming | stored `Allergy`; re-send «Kommer ikke» | `Allergy` deleted; no `Consent` row | none |
| Refused send | other household / admin / after deadline / conflict | no `Allergy`, no `Consent` | existing exceptions |

</intent-contract>

## Code Map

- `wedding/models.py:1-12` docstring (add Story 2.6b); append `Allergy`, `Consent` after `PersonAnswer` (`:151+`, pattern `HouseholdAnswer` `:122-148`). Import `NOTE_MAX` (and optionally `ALLERGY_KEYS` for a test) from `wedding/rules/allergies.py` — rules import nothing from models, so no cycle (same as `HIKE_ANSWERS` from `rules/days.py`).
- `wedding/migrations/0006_…` — `makemigrations`; latest is `0005_householdanswer_personanswer.py`.
- `wedding/rules/allergies.py` — read: `ALLERGY_KEYS`, `NOTE_MAX`, `AllergyEntry`, `has_allergy_info`, `allergy_problems`, `not_saved`; add `consent_outcomes` + constants.
- `wedding/rules/answer.py:33-60` `Answer.allergies/consent/confirmed`; `normalise_answer` drops them for anyone not coming and drops empty entries (read-only).
- `wedding/services/answers.py` — `send_answer`; `_answer_ids` already covers `allergies`, `consent`, `confirmed`. `wedding/services/consent.py` `CONSENT_TEXT_VERSION` (docstring: «Story 2.6b records it» → now recorded). `wedding/services/exceptions.py` `InvalidAnswer` reused.
- `wedding/rsvp/views.py:154-166` `_answer` already passes `alg`, `cons`, `conf`; `:1080` the send call — unchanged. `:1-33` module docstring: mention that allergies are stored with consent (2.6b).
- `wedding/rsvp/forms.py:383` `warning_text`, `wedding/rsvp/summary.py:155-185` — the FR-28 warning, read-only.
- Tests: extend `tests/test_send_answer.py` (service), `tests/test_allergy_rules.py` (rule), `tests/test_rsvp_send.py` (view journey and re-send warning). Helpers in `tests/helpers.py`; seeds `test-sigmund0000000000` (Sigmund + bestemor), `test-arild000000000000`.
- Docs: `README.md:9` status and `:81` «Svarskjemaet» («Allergier lagres først med samtykke når svaret sendes (story 2.6b)» → built), tree if new files; ARCHITECTURE-SPINE AD-4 stored-list and AD-18 dated notes; `docs/manual-test-plan.md` after MT-41; `.docs/implementation-artifacts/deferred-work.md:216-228`.

## Tasks & Acceptance

**Execution:**
- [ ] `wedding/rules/allergies.py` — `STORE`/`DELETE`/`KEEP`, `consent_outcomes` (AD-18, FR-75, NFR-3).
- [ ] `wedding/models.py`, migration `0006` — `Allergy`, `Consent` (FR-26, FR-29, AD-4, AD-18).
- [ ] `wedding/services/answers.py`, `wedding/services/consent.py` docstring — conflict/confirm refusal before writes, apply outcomes, record consent events (FR-26, FR-29, AD-18).
- [ ] `wedding/rsvp/views.py` — module docstring only.
- [ ] `tests/test_allergy_rules.py`, `tests/test_rules_purity.py` — `consent_outcomes` truth table: Ja/Nei/unanswered × coming/not coming.
- [ ] `tests/test_send_answer.py` — every matrix row with `now` fixed, for the respondent and for another member, on a first send and on a re-send (epics AC); `Consent` fields (event, at, given_by, given_by_name, `text_version == CONSENT_TEXT_VERSION`, `given_by_user` None); earlier `Consent` rows survive a re-send; refused sends write no `Allergy`/`Consent`; migration fields (one Boolean per `ALLERGY_KEYS`, no derived field); `str()` of both models contains no name, category or note; with `caplog` at DEBUG a send logs no name or note.
- [ ] `tests/test_rsvp_send.py` — test-client journey on Sigmund's link: Sigmund gluten Ja, bestemor nuts Nei → after send, `Allergy` only for Sigmund, two `Consent` rows (given, refused); then a fresh draft re-send where Sigmund's allergy is changed with consent unanswered → the check page shows the FR-28 warning naming Sigmund, and after send his `Allergy` is unchanged.
- [ ] `docs/manual-test-plan.md` — Norwegian rows MT-42 to MT-44, date and result cells empty, each «Kjøres av Claude med Playwright mot Edge» (`channel: 'msedge'`); before each `uv run manage.py seed_testdata`, then `uv run manage.py runserver`; measure after `document.fonts.ready`:
  - **MT-42 (ekte sending med samtykke):** `http://127.0.0.1:8000/test-sigmund0000000000/svar/`: both coming, whole weekend, any cabin/meals, step 5: Sigmund «Gluten», note «Tåler litt», «Ja»; bestemor «Nøtter», «Nei»; step 6 any; «Se over svaret» shows the Obs warning naming bestemor only; «Send svaret» → `/svar/sendt/`. `uv run manage.py shell -c` prints for the household: one `Allergy` (Sigmund: `gluten` True, note «Tåler litt»), none for bestemor; `Consent` rows Sigmund `given`, bestemor `refused`, both `given_by_name` «Sigmund», `text_version` «2026-11-23». Then a second pass: open `/svar/` again, same answers but bestemor «Ja» with «Jeg bekrefter at bestemor vet om dette og er enig» ticked and Sigmund's consent left unanswered with «Laktose» added → shell shows bestemor `nuts` True, Sigmund's row unchanged (gluten only), and four `Consent` rows in total.
  - **MT-43 (bare tastatur):** the MT-42 first pass with `page.keyboard` only (Tab, Space, arrow keys, Enter) from `/svar/` to `/svar/sendt/`; the consent radios and the confirm checkbox are reachable; focused elements have `outline-style` `solid`; the shell shows the same rows as MT-42's first pass.
  - **MT-44 (oppsett):** step 5 (`/svar/allergier/`) with both people's entries and the confirm box shown, and «Se over svaret» with the Obs warning; at 360 × 640 and 180 × 320, then with 20px default text (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`) at both: `scrollWidth` ≤ `innerWidth`; radios and checkboxes ≥ 44px tall rows; the warning wraps inside the sheet.
- [ ] `README.md` — status sentence (story 2.6b: allergies are stored only for people with «Ja», «Nei» deletes them, unanswered on a re-send keeps them, each consent recorded with who, when and the text version); «Svarskjemaet» paragraph updated.
- [ ] ARCHITECTURE-SPINE.md — dated notes (2026-11-24, Story 2.6b): AD-4 stored list gains `Allergy`/`Consent` fields and migration `0006`; AD-18: `consent_outcomes`, «Ja with nothing entered deletes», «not coming deletes (FR-75)», version recorded at send and the seen-version check moved to 2.6c.
- [ ] `.docs/implementation-artifacts/deferred-work.md` — mark the 2.4 entry «Story 2.6b reads CONSENT_TEXT_VERSION …» done in 2.6b for storage; the «no consent Ja across a revision change» part stays with 2.6c/2.9. Mark the «record which consent-text version the guest saw» entry as moved to Story 2.6c (draft format bump shared with the total snapshot). Add «From Story 2.6b» if review defers anything.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass and `uv run manage.py makemigrations --check --dry-run` reports no changes.
- Given migration `0006`, when applied, then it creates `Allergy` and `Consent`, and a `Consent` row holds the event (given/refused/withdrawn), when, who (guest or user, and the name as text) and `CONSENT_TEXT_VERSION`, so Story 7.2 adds `withdrawn` rows without a migration.
- Given a send through «Send svaret» on the check page, when one person consented «Ja» and another «Nei», then the database holds allergy data only for the «Ja» person and one consent event per answered person.
- Given a re-send, when a person's consent is unanswered, then their stored allergy data is unchanged, and the check page warned before sending that the changes are not saved.
- Given a re-send with «Nei» for a person with stored data, then that data is deleted and a `refused` event is added.
- Given the consent tests, then they cover «Ja», «Nei» and unanswered on a first send and a re-send, for the respondent and for another member.

## Spec Change Log

## Review Triage Log

## Design Notes

- **Why the seen-version check moves to 2.6c:** catching a text change between step 5 and sending needs the version in the draft, which is a format bump (5 → 6). 2.6c already must add the total snapshot to the draft; one bump for both avoids two migrations of the cookie. 2.6b records the version current at send, which equals the seen one unless the text changed mid-answer — the same window 2.6c closes.
- **Why «not coming» deletes without a consent event:** FR-75 says choices that depended on coming are removed and never count, and NFR-3 minimisation means no health data for someone not coming; no consent was answered, so no event.
- **Why «Ja» with nothing entered deletes:** when consent is answered, the step's content is the truth; Epic 4 prefills the form from stored data, so emptied fields with «Ja» means removal.
- **Why refuse CONFLICT/CONFIRM in the service:** the step gate already blocks them, but the service is the only writer (AD-3) and must not store a «Ja» for someone else without the FR-27 confirmation.

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes.
