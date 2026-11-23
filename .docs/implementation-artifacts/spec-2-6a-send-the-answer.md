---
title: 'Story 2.6a: Send the answer'
type: 'feature'
created: '2026-11-24'
status: 'done'
baseline_revision: '63ff928552705c7ab6bbb46263ee96e7a4a1b848'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-5-the-friday-hike-and-the-check-page.md'
warnings:
  - oversized
deferred:
- summary: "Story 2.6c: the «Sender …» button stays busy if the navigation is aborted (Esc or a network failure) or the send fails; reset it so the guest can try again."
  evidence: "Edge Case Hunter and Blind review; reload restores it today."
---

<intent-contract>

## Intent

**Problem:** «Send svaret» on the check page (`/<code>/svar/se-over/`) writes nothing: its POST only redirects back (Story 2.5). No answer reaches the database, so the couple gets nothing, and a CSRF failure on the check page shows the generic 403 page (FR-74, NFR-2, AD-3, AD-4, AD-9; deferred-work «From Story 2.5»).

**Approach:** Add `HouseholdAnswer` and `PersonAnswer` (one migration) and the service `send_answer` in `wedding/services/answers.py`, which writes the normalised draft answer in one IMMEDIATE transaction with an explicit actor, refuses guest sends after the deadline and outside the actor's household, and raises `Household.revision`. The check page's POST calls it, deletes the draft cookie and redirects (303) to a minimal sent page `/<code>/svar/sendt/` that Story 2.7 turns into the full receipt. A small script gives «Send svaret» the «Sender …» busy state, and a CSRF failure on the check page re-renders it with the friendly notice.

## Boundaries & Constraints

**Always:**
- **Models (AD-4, FR-74), migration `0005_householdanswer_personanswer.py`:** `HouseholdAnswer` — `household` OneToOne (CASCADE, `related_name="answer"`), `sent_by` FK `Guest` (`SET_NULL`, null), `sent_by_name` CharField(100) (the name as text, kept if the guest is removed), `sent_at` DateTimeField. `PersonAnswer` — `guest` OneToOne (CASCADE, `related_name="answer"`), `coming` bool, `friday`/`saturday`/`sunday` bool, `cabin` bool, `friday_dinner`/`saturday_breakfast`/`sunday_breakfast` bool, `hike` CharField(5, choices `HIKE_ANSWERS` labelled by `HIKE`, blank). Norwegian `verbose_name`s like the existing models. Nothing derived (no totals, no statuses). Module docstring names Story 2.6a.
- **Service (AD-3, AD-9, FR-41, FR-74, NFR-2):** `send_answer(actor, *, household, respondent: int, answer: Answer, now) -> HouseholdAnswer`, one `transaction.atomic()` (IMMEDIATE via settings). Order: refuse `AdminActor` with `NotAllowed` (the couple's override is Story 4.4); a `GuestActor` whose `household.pk` differs, or any id in `answer.attendance`, the respondent or another answer mapping that is not a guest of `household`, raises `NotAllowed`; every guest of the household must have an attendance entry, else `InvalidAnswer`; a `GuestActor` with `is_past_deadline(Settings.objects.get().rsvp_deadline, now)` raises `DeadlinePassed` (the system actor is not deadline-bound; it seeds in 2.6d). Then `normalise_answer`, `present_days`; `update_or_create` one `PersonAnswer` per guest (days from `present_days`, `cabin` = `night.get(id) is True`, meals from `meals`, `hike` = `hike.get(id, "")`; a person not coming gets all False/blank); `update_or_create` the `HouseholdAnswer` with `sent_by` = respondent guest, `sent_by_name` = their name, `sent_at` = `now`; `Household.objects.filter(pk=...).update(revision=F("revision") + 1)`. A refusal writes nothing. New exceptions in `wedding/services/exceptions.py`: `DeadlinePassed` («Svarfristen har gått ut.»), `InvalidAnswer` («Svaret ble ikke sendt.»).
- **FR-74 rules (AD-2):** in `wedding/rules/households.py`: `person_state(coming: bool | None) -> str` (`"coming"`, `"not_coming"`, `"not_answered"` for None) and `household_state(answered: bool, coming: Iterable[bool]) -> str` (`"not_answered"` unless answered; then `"coming"` when any is True, else `"not_coming"`). Pure, no ORM; `tests/test_rules_purity.py` covers them. Constants for the three strings.
- **Selector:** `household_answer(household) -> HouseholdAnswer | None` in `wedding/selectors.py`.
- **Check page POST (AD-7, AD-8):** `_later_step` gets `actor`. A POST with `action=send` on the check page (after the existing gate): if any member is missing from `draft.att`, 303 to step 1; else `send_answer(actor, household=<actor's household for GuestActor>, respondent=draft.resp, answer=_answer(draft, members), now=timezone.now())`, then `delete_draft` on a 303 to `mount.sent_url()` and return `(response, None)`. Any other POST keeps today's 303 back to the check page. `DeadlinePassed` propagates; `guests/views.py` `_rsvp` catches it and renders `RSVP_CLOSED` with the guest context (deadline and phones, FR-41). `FormMount.sent_url()` → `f"{base_path}sendt/"`.
- **Sent page (UX-DR24 frame; Story 2.7 completes it):** URL `guests:rsvp_sent` `<str:code>/svar/sendt/` placed before the `<slug>` route; `never_cache`, GET/HEAD only. Unknown code → G1 404. No `HouseholdAnswer` → 302 to `/<code>/svar/`. Otherwise template `rsvp/sent.html` (in `wedding/rsvp/templates/`): same paper sheet, no nav bar, footer band; a success notice holding `h1` «Svaret er sendt» and «Sendt av <sent_by_name> <weekday j. month Y> kl. <H:i>.» in Oslo time (EXPERIENCE microcopy row «Receipt heading and sent line»); then the secondary link button «Til invitasjonen» to `/<code>/`. Title «Svaret er sendt – Invitasjon». Wording «avgjort av Claude 2026-11-24». Not gated by the deadline (it only reads).
- **Busy state (UX-DR15):** `static/js/rsvp-send.js`, loaded with `defer` on the check page only; the form gets `data-send-form`. On `submit`: if already busy, `preventDefault()`; else mark busy, set the button text «Sender …» and `aria-disabled="true"` (never `disabled`, so `action=send` is still posted). On `pageshow` with `persisted`, restore «Send svaret» and clear the busy flag. CSS in `site.css` (Story 2.6a block, replacing the «arrives with Story 2.6a» comment): `.button[aria-disabled="true"]` keeps its colours with `cursor: progress`; em breakpoints only.
- **CSRF on the check page (UX-DR52):** `render_after_csrf_failure` handles `CHECK` when the draft exists, `who` is done and `first_unfinished(steps, draft.done, None)` is None: renders the check page via `_render_check` with `csrf_failed=True` and status 403, the same focused error notice as the steps (above the «Obs» notice), no draft write; otherwise None (generic page). `check.html` includes the notice when `csrf_failed`.
- Privacy and quality: no names or answers in logs; check and sent pages `Cache-Control: private, no-store`; no session, messages or hidden fields; only `wedding/services/` writes (`tests/test_only_services_write.py` stays green); every new rule, service, view and test names its FR/NFR/AD/UX-DR in its docstring.

**Never:**
- No `Allergy`, `Consent` or consent-version storage (2.6b), no `Submission`, revision-conflict refusal, total-snapshot comparison or save-failure notice (2.6c), no seeded answers (2.6d), no receipt message, summary, total or payment buttons (2.7), no answered-household redirect or front-page status block (2.8).
- No change to step texts, the draft format (stays 5), `REOPENED_ON_CHANGE`, or px breakpoints.
- No sprint-status action items (epic-1-retro-item-5 belongs to 2.1/2.6d).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Sigmund sends | full draft (MT-36 b answers), POST `action=send` | 1 `HouseholdAnswer` (sent_by Sigmund), 2 `PersonAnswer`, revision 0→1, draft cookie deleted, 303 `/svar/sendt/` | none |
| Bytt | respondent switched to bestemor, send | `sent_by_name` «bestemor» | none |
| Nobody coming | both «Kommer ikke», send | 2 rows `coming=False`, all other fields False/blank | none |
| Partial days | Arild's household, Filippa Saturday only, Leone not coming | Filippa `saturday` only, `hike` blank; Leone all False | none |
| Re-send | second full send | rows updated, still 1 `HouseholdAnswer`, revision 2 | none |
| After deadline | `now` past deadline (service) or view | nothing written; closed page with deadline and phones | `DeadlinePassed` |
| Other household | guest actor, `household` or an answer id from another household | nothing written | `NotAllowed` |
| Admin actor | `AdminActor` | nothing written | `NotAllowed` |
| Missing member | household gained a guest not in `draft.att` | 303 to `/svar/`, nothing written | — |
| No action | POST without `action=send` | 303 to `/svar/se-over/`, nothing written | — |
| Unfinished | send POST with a step not done | gate redirect, nothing written | — |
| Sent page, no answer | GET `/svar/sendt/` before any send | 302 to `/svar/` | — |
| CSRF on check page | POST without token, full draft | 403, check page with focused notice, no write, draft kept | — |
| Double tap (JS) | second submit while busy | prevented in the browser | (server-side repeat: 2.6c) |

</intent-contract>

## Code Map

- `wedding/models.py` — append `HouseholdAnswer`, `PersonAnswer`; docstring `:1-10` adds Story 2.6a. Import `HIKE_ANSWERS` from `wedding/rules/days.py:27` and labels `HIKE` from `wedding/rsvp/steps.py` (or inline the three labels if the import would be circular; check `wedding/rsvp/steps.py` imports).
- `wedding/migrations/0005_…` — `makemigrations`; latest is `0004_is_test_data.py`.
- `wedding/services/answers.py` (new) — `send_answer`; patterns: `wedding/services/households.py:34-62` (`transaction.atomic`, actor checks, refusals), `wedding/services/permissions.py`. `wedding/services/exceptions.py` add two classes. `wedding/services/__init__.py` docstring lists the module.
- `wedding/rules/answer.py:37-140` — read-only: `Answer`, `normalise_answer`, `present_days`. `wedding/rules/deadline.py` `is_past_deadline` read-only. `wedding/rules/households.py` add FR-74 rules.
- `wedding/selectors.py:100-115` — pattern for `household_answer`.
- `wedding/rsvp/steps.py:~150` `FormMount` add `sent_url()`.
- `wedding/rsvp/views.py`: docstring `:1-33` (sending is built); `_answer` `:150`; `_render_check` `:593-620` gains `csrf_failed=False, status=200`; `_later_step` `:993-1072` gains `actor` and the send branch (replaces the comment at `:1059-1061`); `handle_step` `:1097-1100` passes `actor`; `render_after_csrf_failure` `:1112-1206` CHECK branch (today `step != CHECK` falls to `return None`).
- `wedding/rsvp/templates/rsvp/check.html` — comment (sends now), `data-send-form` on the form, CSRF notice (copy `rsvp/step.html:49-51`), `<script defer src="{% static 'js/rsvp-send.js' %}">` (see how `step.html` loads `rsvp-total.js`). New `rsvp/sent.html` (pattern `check.html`, notice component `wedding/components/notice.html` variant `success`).
- `guests/views.py:203-230` `_rsvp` catches `DeadlinePassed`; new `rsvp_sent` view (resolver, `household_answer`, `_guest_context`); `guests/urls.py:32-34` new route before `<slug>`; docstring `:1-16`.
- `static/js/rsvp-send.js` (new; style of `static/js/rsvp-total.js`), `static/css/site.css:354` comment and busy rule.
- Tests: new `tests/test_send_answer.py` (service + FR-74 rules), new `tests/test_rsvp_send.py` (views); update `tests/test_rsvp_hike_check.py` cases that assert «POST writes nothing» (now: non-send POST writes nothing; send writes) and the no-DB-rows test (stop before send). Helpers in `tests/helpers.py`, seed codes `test-sigmund0000000000`, `test-arild000000000000`.
- Docs: `README.md:9` status, `:77+` «Svarskjemaet», tree (`wedding/services/answers.py`, `static/js/rsvp-send.js`); ARCHITECTURE-SPINE AD-4/AD-7 dated notes; EXPERIENCE.md microcopy row `:147` (heading and sent line used now) and «Saving» `:235` (busy state built); `docs/manual-test-plan.md` after MT-38; `.docs/implementation-artifacts/deferred-work.md:204-208`.

## Tasks & Acceptance

**Execution:**
- [x] `wedding/models.py`, migration `0005` — the two models (AD-4, FR-74).
- [x] `wedding/rules/households.py` — `person_state`, `household_state` (FR-74, AD-2).
- [x] `wedding/services/exceptions.py`, `wedding/services/answers.py` — `send_answer` with all refusals (AD-3, AD-9, FR-41, NFR-2).
- [x] `wedding/selectors.py` — `household_answer`.
- [x] `wedding/rsvp/steps.py`, `wedding/rsvp/views.py` — `sent_url`, send branch, `actor` through `_later_step`, CSRF branch for the check page, docstrings.
- [x] `guests/views.py`, `guests/urls.py` — `DeadlinePassed` → closed page; `rsvp_sent` view and route.
- [x] `wedding/rsvp/templates/rsvp/check.html`, new `rsvp/sent.html`, `static/js/rsvp-send.js`, `static/css/site.css` — busy state, CSRF notice, sent page.
- [x] `tests/test_send_answer.py` — every service row of the matrix with `now` fixed (deadline day 23:59:59 Oslo accepted, next day 00:00 refused, nothing written), cross-household and admin refusals, re-send updates, revision raised, sent_by/sent_by_name, FR-74 rule truth table, migration fields (no total/status field on either model).
- [x] `tests/test_rsvp_send.py` — through the test client: Sigmund's full journey then send (rows, cookie deleted with `max-age=0` on path `/<code>/`, 303 to `sendt/`); sent page content (`h1`, sent line in Oslo time, link to `/<code>/`), 302 without answer, Cache-Control private no-store; deadline passed at send (closed page, no rows); missing member; non-send POST; CSRF on the check page (403, notice, no cookie set); the check page has `data-send-form` and the script tag; no session rows or messages.
- [x] `tests/test_rsvp_hike_check.py` — adjust the «POST writes nothing» and no-DB-rows assertions.
- [x] `docs/manual-test-plan.md` — Norwegian rows, date and result cells empty, each «Kjøres av Claude med Playwright mot Edge» (`channel: 'msedge'`); before each `uv run manage.py seed_testdata`, then `uv run manage.py runserver`; measure after `document.fonts.ready`:
  - **MT-1 (2.6a):** README «Svarskjemaet» to the sent page.
  - **MT-39 (real send):** `http://127.0.0.1:8000/test-sigmund0000000000/svar/` through MT-36 b) to `/svar/se-over/`. a) With `page.route` delaying the POST 2 s, click «Send svaret» twice: the button reads «Sender …» with `aria-disabled="true"` and exactly one POST is sent. b) Lands on `/svar/sendt/`: title «Svaret er sendt – Invitasjon», `h1` «Svaret er sendt», «Sendt av Sigmund <today> kl. <HH:MM>.», link «Til invitasjonen» to `/test-sigmund0000000000/`; no `rsvp_draft` cookie. c) `uv run manage.py shell -c` prints the household's `HouseholdAnswer` (`sent_by_name` Sigmund), two `PersonAnswer` rows (both `coming`, all days, `cabin` True, bestemor `sunday_breakfast` per MT-36 c, hikes «maybe»/«no») and `revision` 1. d) `page.goBack()` → no `dialog` event, lands on `/svar/` with no radio checked (draft gone). e) Arild's link: switch respondent to Marie with «Bytt», answer, send → shell shows `sent_by_name` Marie, Leone `coming` False.
  - **MT-40 (keyboard only):** Sigmund's link to the check page with `page.keyboard`; Tab to «Send svaret», Enter → `/svar/sendt/`; on the sent page Tab order is «Til invitasjonen», `tel:` links; focused elements have `outline-style` `solid`.
  - **MT-41 (layout):** the sent page and the check page in the busy state (route held). At 360 × 640 and 180 × 320, then with 20px default text (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`) at both: `scrollWidth` ≤ `innerWidth`; «Sender …» fits on the button without overflow, button ≥ 44px tall; the sent line wraps inside the sheet.
- [x] `README.md` — status (story 2.6a: «Send svaret» saves the answer and shows «Svaret er sendt»; the full receipt is story 2.7), «Svarskjemaet», tree.
- [x] ARCHITECTURE-SPINE, EXPERIENCE.md — dated notes (2026-11-24, Story 2.6a): AD-4 the two models and fields; AD-7 the send POST, `sendt/` address and that the total snapshot moves to 2.6c; EXPERIENCE the sent page frame wording «avgjort av Claude» and the busy state built on «Send svaret».
- [x] `.docs/implementation-artifacts/deferred-work.md` — mark the 2.5 entry done in 2.6a for POST handler, busy state and CSRF; add «From Story 2.6a»: Story 2.6c stores the shown total in the draft and compares it at send (moved with the reason in Design Notes).

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass and `uv run manage.py makemigrations --check` reports no changes.
- Given migration `0005`, when applied, then it creates `HouseholdAnswer` (sent by, sender's name as text, sent at) and `PersonAnswer`, with no total or status field.
- Given «Send svaret» on a valid draft, when posted, then the answer is written in one transaction, the respondent is the sender, `Household.revision` rises by one, the draft cookie is deleted and the guest lands on «Svaret er sendt».
- Given scripts, when «Send svaret» is pressed, then it reads «Sender …» and further taps send nothing.
- Given a guest send after the deadline, when it reaches `send_answer`, then nothing is written and the guest sees the closed page with the deadline and the couple's phones.
- Given `send_answer` tests, then a guest actor cannot write to another household, and person/household states follow FR-74.
- Given the check page posted without a CSRF token, then it is shown again with status 403 and the focused notice, and nothing is written.

## Spec Change Log

## Review Triage Log

### 2026-11-24 — Review pass
- verdicts: 26 findings — high 0, medium 0, low 11, false 14, maybe-false 1
- findings:
  - `[false]` `[reject]` NotAllowed/InvalidAnswer from send_answer give a 500 (edge-case) — `read_draft` rejects a draft whose `resp` or attendance key is not a member (wedding/rsvp/draft.py:287), and the view redirects to step 1 when a member lacks attendance before calling the service; no reachable path raises either.
  - `[false]` `[reject]` Two concurrent sends race on update_or_create and raise IntegrityError (edge-case) — the database runs `transaction_mode: IMMEDIATE` (config/settings.py:118), so the second send waits for the write lock and then updates the existing rows.
  - `[low]` `[reject]` A non-guest actor reaching the send branch passes `household=None` (edge-case) — no non-guest mount of the form exists until Story 4.4, which must pass a real household; an admin is refused before `household` is read.
  - `[maybe-false]` `[reject]` A guest moved to another household keeps a stale PersonAnswer (edge-case) — guests are moved only by the couple's admin (Epic 4); the next send of the new household overwrites it. If true it would be low; settle in Epic 4's guest editing.
  - `[low]` `[defer]` An aborted navigation leaves the button at «Sender …» (edge-case) — only Esc or a network failure; reload restores it. Routed to Story 2.6c (failing sends).
  - `[low]` `[patch]` The view's missing-member branch is never exercised (verification-gap) — added a test where nobody comes, a member joins, and the send redirects to step 1 with nothing written.
  - `[false]` `[reject]` InvalidAnswer unhandled on the view path (verification-gap, other) — same refutation as the first row.
  - `[false]` `[reject]` The busy state is checked only as source text (verification-gap, other) — MT-39 and MT-41 ran it in Edge: «Sender …», `aria-disabled="true"`, the second submit prevented, exactly one POST.
  - `[false]` `[reject]` «One IMMEDIATE transaction» rests on global settings (intent-alignment) — that is how the architecture makes every transaction IMMEDIATE (AD-4); `send_answer` runs in one `atomic()` block.
  - `[false]` `[reject]` «Ignores more taps» is not run (intent-alignment) — run in Edge by MT-39 a).
  - `[low]` `[reject]` The deadline view test stubs `is_past_deadline` (intent-alignment) — the service test uses the real rule with a real date; the stub only isolates the view's handling.
  - `[false]` `[reject]` AD-3 is tested only at the service (intent-alignment) — the guard lives in the service by design; the view cannot address another household.
  - `[false]` `[reject]` Admin refused and system actor not bound by the deadline go beyond the ACs (intent-alignment) — decided in the spec for Stories 4.4 and 2.6d.
  - `[low]` `[reject]` `household=None` for a non-guest (intent-alignment) — same as the third row.
  - `[false]` `[reject]` FR-74 states appear in no view (intent-alignment) — the AC asks for the states as rules; their views are Stories 2.8 and 4.x.
  - `[false]` `[reject]` The draft is deleted in the view, not in `send_answer` (intent-alignment) — a cookie is an HTTP concern; the services take no response (AD-4); tested by the view tests and MT-39 b).
  - `[false]` `[reject]` NotAllowed/InvalidAnswer reach Django unhandled (blind) — same refutation as the first row.
  - `[false]` `[reject]` `draft.resp` may be None or a non-member (blind) — `read_draft` refuses such a draft (draft.py:287).
  - `[low]` `[reject]` A system actor would crash on `household=None` (blind) — same as the third row.
  - `[low]` `[reject]` `person_state`/`household_state` are unused in production (blind) — the story's AC requires them as rules; Stories 2.8 and 4.x use them; tested.
  - `[low]` `[patch]` `wedding/models.py` imports `HIKE` labels from the form package `wedding.rsvp.steps` (blind) — the labels moved to `wedding/rules/days.py` next to `HIKE_ANSWERS`; steps.py imports them from there.
  - `[false]` `[reject]` Concurrent double send gives IntegrityError and is not deferred (blind) — IMMEDIATE transactions (row 2); repeated sends are Story 2.6c by the epic.
  - `[low]` `[defer]` Busy button: no reset on failure, nothing announced to screen readers (blind) — failure reset deferred with row 5; the label change is on the focused button and the page title changes on arrival, so no live region added.
  - `[low]` `[patch]` Hover/active still thicken the outline of the busy button (blind) — `.button[aria-disabled="true"]` now keeps the 2px border on hover and press.
  - `[false]` `[reject]` The sent page has no status role or focus, and no way to change the answer (blind) — it is a new page whose title and h1 say «Svaret er sendt»; changing the answer is Story 2.8.
  - `[low]` `[patch]` No test that revision rises by one on a re-send, and the Norwegian date is untested (blind) — a re-send test added; MT-39 showed «mandag 23. november 2026 kl. 17:51» in Edge.

## Design Notes

- **Why a minimal sent page now:** sending needs a landing that confirms it; EXPERIENCE G6 is a separate page, and 2.7's AC starts from «the receipt opens». 2.6a gives the address and the heading/sent line; 2.7 adds Rikke's message, summary, total and payment. Back after send reaches the empty form until 2.8 redirects answered households.
- **Why the total snapshot moves to 2.6c:** 2.6c owns «the recalculated total differs → refuse». Storing it now would add a draft field nothing reads and a second format bump, and writing it from the check page's GET would break AD-8's «written only on Fortsett or Velg». 2.6c decides both together.
- **Why `aria-disabled` not `disabled`:** a disabled submitter is left out of the form data, so `action=send` would be lost.
- **Why the system actor skips the deadline:** seeding (2.6d) must work whatever the settings' deadline is; FR-41 binds guests.

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes.

## Auto Run Result

Status: done

**Summary:** «Send svaret» on the check page now sends the answer: `send_answer` writes one `PersonAnswer` per guest and the household's `HouseholdAnswer` (sender, name, time) in one IMMEDIATE transaction, raises `Household.revision`, and refuses an admin actor, another household, a missing member and a guest after the deadline. The draft cookie is deleted and the guest lands on «Svaret er sendt» (`/svar/sendt/`). The button shows «Sender …» with `aria-disabled` and ignores further taps; a CSRF failure on the check page shows the check page with the focused notice. FR-74 states are pure rules. The total snapshot (AD-8) moved to Story 2.6c.

**Files changed:**
- `wedding/models.py`, `wedding/migrations/0005_householdanswer_personanswer.py` — the two answer models.
- `wedding/services/answers.py`, `wedding/services/exceptions.py`, `wedding/selectors.py`, `wedding/rules/households.py`, `wedding/rules/days.py` — sending, refusals, FR-74 states, hike labels.
- `wedding/rsvp/views.py`, `wedding/rsvp/steps.py`, `guests/views.py`, `guests/urls.py`, `wedding/rsvp/templates/rsvp/check.html`, `sent.html`, `static/js/rsvp-send.js`, `static/css/site.css` — send branch, sent page, busy state, CSRF notice.
- `tests/test_send_answer.py`, `tests/test_rsvp_send.py`, `tests/test_rsvp_hike_check.py`, `tests/test_design_system.py`.
- `README.md`, `docs/manual-test-plan.md`, `ARCHITECTURE-SPINE.md`, `EXPERIENCE.md`, `deferred-work.md`.

**Review:** 26 findings — 4 patched (missing-member check before the gate with a test, hike labels moved out of the form package, busy button without hover/press ring, stricter re-send test), 2 deferred to 2.6c, 20 rejected with reasons in the triage log.

**Follow-up review recommendation:** false. Only low findings were patched, and the browser checks were re-run after the patches.

**Verification:** `uv run pytest` 1191 passed; ruff, ruff format and djlint clean; `makemigrations --check` clean. MT-1 (2.6a), MT-39, MT-40, MT-41 run by Claude with Playwright in Edge 158 after the patches, with the database rows read through `manage.py shell`.

**Residual risks:** a busy button is not reset after an aborted send (2.6c); «Tilbake» after a send shows the empty form until Story 2.8; the total snapshot and revision conflict are 2.6c.
