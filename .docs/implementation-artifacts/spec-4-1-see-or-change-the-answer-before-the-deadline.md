---
title: 'Story 4.1: See or change the answer before the deadline'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_revision: 'cb2a584ae4ef6868560738556b8d2d1a34e12f61'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-4-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/answered-1.html'
warnings: ['oversized']
deferred:
- summary: >-
    Story 4.2: a form opened before another member's send, then continued with no cookie draft, is seeded at the newer revision, so its first step overwrites the other member's change with no conflict notice (AD-9).
  reason: >-
    This is the subject of Story 4.2 («No answer is overwritten without anyone seeing it»); the stale revision has to travel with the opened form (for example a hidden field) for the check to fire.
---

<intent-contract>

## Intent

**Problem:** A household that has answered can only look at its status block: `/<code>/svar/` redirects there (Story 2.8), so Arild cannot change his plans, nobody sees who answered last, and the couple's «Changed» marker (`Household.changed_at`, AD-19, FR-39) does not exist (FR-37, FR-38, FR-41).

**Approach:** Before the deadline the status block gets the change-window line and the primary button «Se eller endre svar»; every form address opens the one form seeded in memory from the stored answer; the form's top shows the info notice «Sist endret av …»; `send_answer` sets `changed_at` through one helper only when the normalised content differs from the stored answer.

## Boundaries & Constraints

**Always:**
- Before the deadline (`is_past_deadline` False) an answered household's GET/HEAD of any `/<code>/svar/…` address is NOT redirected; `_rsvp` in `guests/views.py` passes `answered=True` to `handle_step`. After the deadline an answered household's GET/HEAD still goes (302) to `/<code>/#status` (Story 2.8, checked before the closed page; Story 4.3 builds the locked view). The Story 2.8 `?sending=` exemption in `_rsvp` is deleted: before the deadline every address renders, after it every address redirects. POSTs are unchanged.
- Seeded draft (new `wedding/rsvp/change.py`, `seeded_draft`, FR-37, AD-8): built in memory, never written to the cookie by a GET, from `sent_answer` (the stored `PersonAnswer`, `Allergy` and `Consent` rows). `started` now, `rev` = the household's current revision, `resp` = `_owner(actor, members)` (the opener), `att`/`whole`/`days`/`night`/`meals`/`alg`/`hike` from the stored answer, `done` = all six step keys (then `_settled`). `cons`: the stored latest consent per coming guest (given True, refused False) kept only when that event's `text_version` equals `CONSENT_TEXT_VERSION`, otherwise left out; `cv` = `CONSENT_TEXT_VERSION` when any consent is kept, else None. `conf` is empty: confirmations are never stored, so a respondent who is not the person confirms again on step 5 (AD-18; the form reopens step 5 through `_settled`). If any member has no stored `PersonAnswer` (added after the answer), `done` is empty and the form opens at step 1 with the others filled in.
- `handle_step` gets `answered: bool = False`. It uses the seeded draft when `draft is None and answered` and the request is not a POST with `action=send` on the check page; it never shows the Draft offer for a seeded draft (the offer is for a cookie draft only); a cookie draft, valid or not, wins over the seed, and a broken cookie is deleted as before. Only a POST «Fortsett» or «Velg» writes the cookie, as today (AD-8). A `send` POST without a cookie draft writes nothing and is sent (303) to step 1, so an old tab cannot re-send the stored answer (closes the Story 2.8 deferred item; a stale cookie draft is still refused by the Story 2.6c revision check).
- «Nei, begynn på nytt» deletes the cookie draft; step 1 then opens seeded from the sent answer (the stored answer is the new «empty»). Changed-household offer (Story 2.9 deferred): when `read_draft` reports `changed`, the Draft offer adds «Husstanden er endret siden du begynte. Du må se over svaret på nytt fra steg 1, og samtykke til å lagre allergier må gis på nytt.» (`household_changed` in the context).
- Status block, before the deadline, in this order after the total: `<p class="status-block__window">` «Dere kan endre svaret fram til {{ deadline|date:"l j. F Y" }} kl. 23:59.» («Du kan endre …» when `speaks_to_one`), then the primary `<a class="button">` «Se eller endre svar» to `guests:rsvp`, then the existing secondary «Slik betaler du» (only when owed). After the deadline: neither line nor button (Story 4.3 adds «Se hele svaret»). `can_change` in the front page context from `is_past_deadline`; no new SELECT.
- Draft of an answered household (Story 2.9 deferred): before the deadline a usable cookie draft shows the warning notice «Du har endringer som ikke er sendt ennå.» in the status block (one `household_members` SELECT, only when the cookie is there; a broken cookie is deleted); after the deadline the front page deletes the cookie. The draft is deleted by a successful send, as now.
- Info notice (FR-38, UX-DR28): on every form step and the check page of an answered household, above the `h1`, via `wedding/components/notice.html` variant `info`, text «Sist endret av {{ sent_by_name }}, {{ sent_at|date:"j. F" }} kl. {{ sent_at|date:"H:i" }}» in Oslo time, no year, no trailing full stop beyond the sheet's style. It names the last SEND (`HouseholdAnswer.sent_by_name`/`sent_at`, which `send_answer` already overwrites on every send), not `changed_at`: «who answered last» is the sender, and `changed_at` is only the couple's marker (shown in Epic 5). Built by `last_changed_text(answer)` in `change.py`; the context key is `last_changed`, set in `_rsvp`; the CSRF re-render does not carry it. The Draft offer does not show it.
- `Household.changed_at` (DateTimeField, null, blank; migration `0009`) is set ONLY by `mark_changed(household, now)` in new `wedding/services/changes.py` (AD-19, FR-39), called from `send_answer` inside its transaction, and only when a `HouseholdAnswer` existed before this send AND `answer_changed(stored, new)` (new pure rule, `wedding/rules/changes.py`) is True. `stored` is `sent_answer(household)` read before any write, normalised; `new` is the normalised answer. `answer_changed` compares, per household member: who is coming; `present_days`; cabin; chosen meals as sets; hike; and for each present guest whose new consent is True, the stored allergy entry (compare `frozenset(cats)`, `none`, `note`) and that the stored consent is True, for new consent False, that the stored consent is False and no stored allergy remains; a guest whose new consent is unanswered (kept) never counts. A first answer, an identical re-send and the seed never set it. Revision, `sent_by` and `sent_at` still change on every send that writes (unchanged behaviour). The helper is the only code that writes `changed_at` (`tests/test_only_services_write.py` stays green).
- Totals and balance on the receipt and the status block come from the stored answer through `_sent_money`, so a changed answer shows the new total with no new code (AD-12). A changed send twice (same `innsending`) shows the receipt, never the conflict notice, and the revision rises once (Story 2.6c order, AD-20): proved by a test.
- `wedding/rsvp/views.py` grows by at most 15 lines (the `answered` parameter, seeded-draft hook, offer flag); all new logic lives in `change.py`, `services/changes.py`, `rules/changes.py`. Do not split `views.py` (Story 4.4). Every new function, template and test names its FR/AD/UX-DR. UI Norwegian, code English; breakpoints only in em; no new script.

**Never:**
- No «what differs» display and no changes to the conflict notice (Story 4.2); `_changed_text` stays. No «Se hele svaret», locked answer view or never-answered state (Story 4.3). No couple mount (Story 4.4), no «Meldt betalt» (Story 5.1), no `changed_by` column. No stored flag, total or status (AD-4).
- Do not carry confirmations (`conf`) across from the stored answer, and never write the draft cookie on a GET.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Status block, open window | Arild's link `/test-arild000000000000/`, deadline in 30 days | block lists «Dere kan endre svaret fram til <weekday j. month Y> kl. 23:59.», primary «Se eller endre svar» → `/test-arild000000000000/svar/`, then «Slik betaler du» | — |
| One-person household | Synne `/test-synne000000000000/` | «Du kan endre svaret fram til … kl. 23:59.», button, no «Slik betaler du» (0 kr) | — |
| Open the form | GET `/test-arild000000000000/svar/`, no cookie | 200 step 1 «Hvem kommer?», info notice «Sist endret av Arild, <j. month> kl. <H:i>», Arild, Marie, Filippa «Kommer», Leone «Kommer ikke»; no Draft offer; no `Set-Cookie` | — |
| Prefilled steps | «Fortsett» through steps 2 to 6 | step 2 «Nei», Filippa Lørdag + Søndag ticked; step 3 Arild, Marie, Filippa «Ja»; step 4 stored meals ticked; step 5 Arild «Ingen allergier eller matbehov» + «Ja», Filippa «Nei»; step 6 Arild and Marie «Ja» | — |
| Change and send | Arild's link: step 3 Filippa «Ja» → «Nei», on to «Se over svaret» | check page total «Totalt for husstanden: 4 980 kr» (6 480 − 1 500); «Send svaret» → `sendt/`: «4 980 kr», «Sendt av Arild …»; revision +1, `changed_at` set | — |
| Identical re-send | Synne opens the form, «Fortsett» on every step shown, sends | saved, revision +1, `sent_at` moves, `changed_at` stays NULL | — |
| First answer | Mona (unanswered) sends | `changed_at` stays NULL | — |
| Double tap | same `innsending` posted twice for a change | second POST: 303 to `sendt/`, no conflict notice, revision +1 once, one `Submission` | — |
| Opener is not the consenter | Marie opens `/test-marie000000000000/svar/`, goes to the check page | step 5 is reopened: Arild's «Ja» needs the confirmation (consent kept, `conf` empty); gate sends her to step 5 | the CONFIRM error as today |
| Send without cookie | POST `action=send` to `se-over/` with no `rsvp_draft` | 303 to step 1, nothing written, revision unchanged | — |
| Stale cookie draft | cookie draft at revision n, household now n+1 | existing 2.6c refusal (`?sending=endret`), unchanged | — |
| Draft of answered household | cookie draft + new session, `/svar/` | Draft offer; front page status block shows «Du har endringer som ikke er sendt ennå.» | — |
| After the deadline | Arild GET `/` and `/svar/`, deadline two days back | `/` shows the block without line or button; `/svar/`, `/svar/dager/` 302 to `/#status`; the draft cookie is deleted | POST: closed page as before |
| Consent text changed | stored consent with another `text_version` | that guest's consent is not seeded; `cv` None; step 5 asks again | — |

</intent-contract>

## Code Map

- `guests/views.py:214-245` `_rsvp` — replace the redirect condition by «answered and past deadline and GET/HEAD»; read `answer = household_answer(...)` once, `_guest_context(..., answered=answer is not None)`, set `context["last_changed"] = last_changed_text(answer)` when answered; pass `answered=` to `handle_step`; update docstring (drop the `?sending=` text) and module docstring (Story 4.1). `:142-189` `front_page` — `can_change`, `draft_waiting` for answered households (shares the cookie branch), delete cookie after the deadline; docstring "An answered household's cookie is left alone" removed. `SENDING_QUERY` import then unused: remove.
- `wedding/rsvp/views.py:1300-1345` `handle_step` — `answered` parameter, seeded draft, `seeded` skips the offer at `:1327`, `changed` from `read_draft` (now `_`) to `_render_offer` `:1357-1367`; `:303-308` `_merged` unchanged (works on the seeded draft). Do not touch `_send`, `_changed_text`.
- `wedding/rsvp/change.py` (new) — `seeded_draft(actor, members, now)`, `last_changed_text(answer)`.
- `wedding/rules/changes.py` (new, pure) — `answer_changed(stored, new)`; reuses `normalise_answer`, `present_days` (`wedding/rules/answer.py`), `has_allergy_info`, `AllergyEntry`.
- `wedding/services/changes.py` (new) — `mark_changed(household, now)`; `wedding/services/answers.py:101-215` `send_answer` — read `stored` and whether an answer existed before the first write, call `mark_changed` after the revision update; extend docstring and `services/__init__.py` docstring.
- `wedding/models.py:41-63` `Household` — `changed_at`; `wedding/migrations/0009_household_changed_at.py` (new, `makemigrations`).
- `wedding/selectors.py:135-204` `household_answer`, `sent_answer` (consent events: need each coming guest's latest event's `text_version`; add a small selector `consent_versions(household) -> dict[int, str]` or extend `sent_answer`'s sibling, one SELECT).
- Templates: `guests/templates/guests/front_page.html:151-165` status block (window line, button, draft notice; update the comment), `wedding/rsvp/templates/rsvp/step.html` and `check.html` (include new `rsvp/includes/last-changed.html` above the `h1`), `rsvp/draft_offer.html` (`household_changed` paragraph). `static/css/site.css:865-901` `.rsvp`, `.status-block` — spacing for `.status-block__window` and two stacked buttons; CSS only, em breakpoints.
- Reuse: `notice.html` variant `info` (`guests/templates/guests/style_sample.html:91` already shows the exact text), `speaks_to_one`, `is_past_deadline`, `_sent_money`.
- Tests: `tests/test_front_page_status.py` (status block rows; the Story 2.8 «`/svar/` 302» and `?sending=` tests change per Always), `tests/test_rsvp_draft.py`, `tests/test_rsvp_draft_offer.py`, `tests/test_rsvp_send_views.py`, `tests/test_answers_service.py` (fixtures `seeded_with_answers`, `seeded`; codes: Arild `test-arild000000000000`, Marie `test-marie000000000000`, Synne `test-synne000000000000`, Mona `test-mona0000000000000`; numbers from `wedding/fixtures/expected.toml:87-123`: Arild 6 480, Synne 0). Query-count pins on answered pages may change by the draft check only when the cookie is present.
- Docs: `ARCHITECTURE-SPINE.md` AD-19 (`:249`, add the built note), AD-9 (`:155`, seeded draft, send needs a cookie draft), AD-11 (`:175`, answered draft cookie deleted after the deadline); `EXPERIENCE.md` `:150`, `:211`, `:246` (mark «Dere kan endre …», «Se eller endre svar», «Sist endret av …» decided by Claude 2026-11-27, Story 4.1; note the notice names the last sender); `DESIGN.md` Status block `:687`; `README.md:9` status line and the Svarskjemaet paragraph (`:94`, last sentences about `#status` and `?sending=`), folder tree if files are listed; `deferred-work.md`; `sprint-status.yaml`; `.logs/rikke/issues.md`; `docs/manual-test-plan.md` after MT-90.

## Tasks & Acceptance

**Execution:**
- [x] `wedding/models.py`, `wedding/migrations/0009_household_changed_at.py` -- add `Household.changed_at` -- FR-39, AD-19.
- [x] `wedding/rules/changes.py`, `tests/test_change_rules.py` (new) -- `answer_changed`; unit-test every difference kind (attendance, days, cabin, meal, hike, allergy entry, consent flip, kept consent = no change, identical = False) -- FR-39, AD-19.
- [x] `wedding/services/changes.py`, `wedding/services/answers.py`, `tests/test_answers_service.py` -- `mark_changed` and its call; tests: first answer does not set, changed re-send sets, identical re-send does not, double tap (same id) raises revision once and sets once, refused sends do not set, cross-household still `NotAllowed` -- FR-39, AD-19, AD-20.
- [x] `wedding/selectors.py` -- consent text versions per guest -- FR-37, AD-18.
- [x] `wedding/rsvp/change.py`, `tests/test_rsvp_change.py` (new) -- `seeded_draft`, `last_changed_text`; tests: Arild's seed equals the stored answer through `_answer`; consent of another `text_version` dropped; no `conf`; a member without `PersonAnswer` gives empty `done` -- FR-37, FR-38, AD-8, AD-18.
- [x] `wedding/rsvp/views.py` (≤ 15 added lines) -- `answered`, seeded draft, no offer for seed, no seed for `send` POST, offer `household_changed` -- FR-37, AD-8, UX-DR26.
- [x] `guests/views.py` -- `_rsvp`, `front_page`, docstrings -- FR-37, FR-41, FR-78, UX-DR10.
- [ ] templates and `static/css/site.css` -- status block, info notice include, offer paragraph -- FR-37, FR-38, UX-DR10, UX-DR28.
- [x] `tests/test_front_page_status.py`, `tests/test_rsvp_draft_offer.py`, `tests/test_rsvp_send_views.py` -- every matrix row at view level (real POST flow through the steps with `client`, final send, receipt and status block show 4 980 kr, the info notice text, no `Set-Cookie` on the seeded GET, no offer, send without cookie, after the deadline, answered draft notice); update older tests broken by the removed redirect -- FR-37, FR-38, FR-41.
- [ ] planning docs per Code Map -- dated 2026-11-27; reasons: the notice names the last sender; `conf` not carried; send needs a cookie draft; `changed_at` only, no changer name.
- [x] `.docs/implementation-artifacts/deferred-work.md` -- mark done: 2.8 stale POST, 2.9 answered-household draft cookie, 2.9 «Ja, fortsett» text; retarget «what differs» (2.6c) to Story 4.2; keep «conflict notice must not name a send as cause» open for the first non-send revision bump (4.4, Epic 7), noting that after 4.1 only sends bump it.
- [x] `docs/manual-test-plan.md` -- add MT-91 to MT-96 (Norwegian, result cells empty), see Verification -- FR-37, FR-38, UX-DR10.
- [x] `README.md`, `sprint-status.yaml` (4-1 and epic-4 in-progress), `.logs/rikke/issues.md` -- sync -- criterion 6.

**Acceptance Criteria:**
- Given Arild's household has answered and the deadline is ahead, when Marie or Arild opens their link, then the status block shows «Dere kan endre svaret fram til <weekday date> kl. 23:59.», the primary button «Se eller endre svar» to `/<code>/svar/` and, when owed, «Slik betaler du».
- Given that household, when a member opens `/<code>/svar/`, then step 1 opens with the sent answers filled in, the notice «Sist endret av Arild, <date> kl. <time>» on top and no cookie is set until «Fortsett».
- Given Arild changes Filippa's cabin to «Nei» and sends, then `send_answer` saves it, `changed_at` is set once by `mark_changed`, the receipt and status block show 4 980 kr and the revision rose by one.
- Given a re-send with the same normalised content, or the household's first answer, then `changed_at` stays NULL.
- Given a changed answer sent twice with the same `innsending`, then the second request shows the receipt, no conflict notice, and the revision rose once.
- Given an answered household and a POST `send` without a cookie draft, then nothing is written and the guest goes to step 1.
- Given the deadline has passed, when an answered household opens `/<code>/svar/…`, then it lands on `/<code>/#status` with no change line or button, and a leftover draft cookie is deleted.

## Spec Change Log

## Review Triage Log

### 2026-11-27 — Review pass
- verdicts: 20 findings — high 0, medium 2, low 14, false 4, maybe-false 0
- findings:
  - `[medium]` `[patch]` Consent text version of the seeded consent is tested only with one event per guest (verification-gap) — a test with two events of different versions pins that the latest event decides.
  - `[low]` `[patch]` `?sending=` on a non-check step before the deadline is no longer pinned after the 2.8 test was deleted (verification-gap, edge-case) — a test asserts the form (200).
  - `[low]` `[patch]` MT-91 expects a running sum right after ticking «Nei», but the sum is server-rendered (orchestrator, Playwright) — the row now says the sum shows after «Fortsett» and on the check page; measured 4 980 kr there.
  - `[medium]` `[defer]` A first POST without a cookie seeds at the newer revision, so a form opened before another member's send overwrites that step without a conflict notice (blind) — real, but it is the subject of Story 4.2 («No answer is overwritten without anyone seeing it»); entered in deferred-work.md for 4.2.
  - `[false]` `[reject]` A send POST to a non-check step is seeded instead of refused (edge-case) — `_later_step` treats `sending` only on the check page; a send action to another step is an ordinary step POST and writes nothing.
  - `[false]` `[reject]` A broken draft cookie lingers on the seeded path (edge-case) — `handle_step` deletes a broken cookie on the step response (`elif broken`, views.py line 1354).
  - `[false]` `[reject]` views.py grew more than 15 lines (edge-case, claim) — net growth is 14 lines (17 added, 3 removed).
  - `[false]` `[reject]` «kl. 23:59» is hard-coded in the template (blind) — the same text is already in the Svar innen line and the closed page; the deadline moment is one rule and the template shows the same constant as before.
  - `[low]` `[reject]` «Svaret er ikke sendt ennå.» above «Sist endret av …» contradicts (blind) — the warning is about the new changes, which really are not sent; Playwright shows both read correctly on the check page.
  - `[low]` `[reject]` An identical re-send moves `sent_at`, so the notice claims a change (blind) — the notice names the last send by design (Design Notes, ARCHITECTURE-SPINE note); `changed_at` is the couple's marker.
  - `[low]` `[reject]` `changed` is computed before the revision and idempotency checks, two extra SELECTs on refused sends (edge-case) — negligible, and moving it would split the transaction logic.
  - `[low]` `[reject]` A first consent «Nei» with nothing stored sets `changed_at` (edge-case) — the stored consent record does change, so it is a change.
  - `[low]` `[reject]` Seed keeps allergy entries without consent when the text version is old (edge-case) — step 5 then shows consent unanswered and the send is refused until it is answered.
  - `[low]` `[reject]` Empty sent_by_name or a non-Norwegian locale in `last_changed_text` (edge-case) — `sent_by_name` is always the sender's name and the site is Norwegian only.
  - `[low]` `[reject]` The `(_see_other if sending else HttpResponseRedirect)` inline choice reads poorly (blind) — one line with a comment; no behaviour defect.
  - `[low]` `[reject]` Test helpers duplicated, MARIE redefined, README paragraph long (blind) — cosmetic; README follows the existing section layout.
  - `[low]` `[reject]` Process traces missing: session log, deferred entries (blind) — written in the finalize and log steps.
  - `[low]` `[reject]` Migration header date is 2026-11-26 (blind) — generated comment only.
  - `[low]` `[reject]` The `:`boundary at 23:59:59 on the front page has no test (blind) — the deadline rule has its own boundary tests (AD-11).
  - `[low]` `[reject]` Intent alignment: the diff implements the guest-facing flow; «Sist endret av» names the last sender (intent-alignment) — documented decision, not a divergence to fix.

## Design Notes

- **Seed in memory, cookie on «Fortsett»:** AD-8 says a GET writes nothing, and the AC wants `/svar/` to open filled in. A transient draft built per request satisfies both and keeps the step handlers unchanged; the cookie draft appears only when the guest moves on.
- **Why `send` never uses the seed:** a seeded send would silently re-send the stored answer from any stale tab or after a cookie loss. Requiring a real cookie draft closes the Story 2.8 gap with no new revision logic.
- **Notice = last sender, marker = `changed_at`:** the epics line says «Sist endret av <name>» but AD-19 stores only a time. Naming the last sender reuses `sent_by_name` and `sent_at`, which every send already sets; the wording is the epics' and EXPERIENCE's.
- **Consent across a change:** consent «Ja» is seeded only for the same text version and never with `conf`, so a different respondent confirms again (AD-18). Identical re-sends still append a `Consent` event per coming guest who answered (append-only log, no change to 2.6b).

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes (after `0009`).

**Manual checks (Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`) after `uv run manage.py migrate`, `uv run manage.py seed_testdata`, `uv run manage.py runserver`; the implementer writes the rows with empty result cells; run `seed_testdata` again before each row):**
- MT-91 Se og endre svaret: `/test-arild000000000000/` (window line with the deadline date, «Se eller endre svar», «Slik betaler du»); click the button, expect `/test-arild000000000000/svar/` with the info notice and prefilled step 1; Fortsett on step 2 («Nei», Filippa Lørdag + Søndag), step 3: Filippa «Nei» (running total 4 980 kr), steps 4 to 6, «Se over svaret» total 4 980 kr, «Send svaret», receipt «4 980 kr»; front page shows 4 980 kr; `uv run manage.py shell -c "from wedding.models import Household; print(Household.objects.get(guests__code='test-arild000000000000').changed_at)"` prints a date.
- MT-92 Uendret svar og annen svarer: `/test-synne000000000000/svar/`, Fortsett on every step, send: `changed_at` NULL; `/test-marie000000000000/svar/`: Fortsett to the check page, expect step 5 asking Arild's confirmation.
- MT-93 Etter fristen: set the deadline two days back (the 2.8 shell command), Arild's `/` has no window line or button, `/svar/` lands on `/#status`; run `seed_testdata` again.
- MT-94 Utkast i et besvart svar: on Arild's form press «Fortsett» on step 1, close the context and open a new one with the saved cookies minus `rsvp_visit`: `/svar/` shows «Vil du fortsette der du slapp?», and the front page shows «Du har endringer som ikke er sendt ennå.».
- MT-95 Bare tastatur: from Arild's front page Tab to «Se eller endre svar», Enter, then Tab and Enter through all steps to «Send svaret»; focused controls have `outline-style` `solid`.
- MT-96 Oppsett: Arild's front page and step 1 at 360 × 640 and 180 × 320, with and without 20px default text (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`): `scrollWidth` ≤ `innerWidth`, «Se eller endre svar» ≥ 44px high, the window line and the info notice wrap inside the sheet.

## Auto Run Result

Status: done

**Summary:** A household that has answered can now see and change the answer before the deadline (FR-37, FR-38, FR-39, FR-41, AD-19, UX-DR10, UX-DR28). The status block shows «Dere kan endre svaret fram til … kl. 23:59.» and «Se eller endre svar»; `/<code>/svar/` opens the form filled in from the stored answer (an in-memory `seeded_draft`, no cookie until «Fortsett») with the notice «Sist endret av <name>, <date> kl. <time>»; `send_answer` sets `Household.changed_at` through `mark_changed` only when `answer_changed` finds different content. A send needs a real cookie draft (closes the Story 2.8 stale-POST item), and the answered household's draft cookie gets a front-page notice and is deleted after the deadline.

**Files changed:**
- `wedding/models.py`, `wedding/migrations/0009_household_changed_at.py`, `wedding/rules/changes.py`, `wedding/services/changes.py`, `wedding/services/answers.py`, `wedding/selectors.py`, `wedding/rsvp/change.py` (new), `wedding/rsvp/views.py` (+14 net), `guests/views.py`, templates, `static/css/site.css`.
- Tests: `test_change_rules.py`, `test_rsvp_change.py` (new), `test_answers_service.py`, `test_front_page_status.py`, `test_rsvp_draft_offer.py`, `test_rsvp_send_views.py`.
- ARCHITECTURE-SPINE, DESIGN, EXPERIENCE, README, `deferred-work.md`, `issues.md`, `sprint-status.yaml`, `docs/manual-test-plan.md` (MT-91 to MT-96).

**Review:** 20 findings from four layers: 3 patched (a test for the latest consent event deciding the seed, a test for `?sending=` on a non-check step, the MT-91 wording), 1 deferred to Story 4.2, 16 rejected with reasons.

**Follow-up review recommendation:** false. No high finding; the one real concurrency gap is Story 4.2's subject.

**Verification:** `uv run pytest` 1662 passed; ruff, ruff format and djlint clean. MT-91 to MT-96 run by Claude with Playwright in Edge: change flow gives 4 980 kr on the check page, receipt and front page, `changed_at` set; send without cookie draft 303; after the deadline no line or button and `/svar/` goes to `#status`; keyboard-only through all steps; 360 and 180 px at 16 and 20 px with no overflow, button 52 to 88 px high.

**Residual risks:** The first-step overwrite race (deferred to 4.2). The notice names the last sender, so an identical re-send moves it (by design, documented). Draft cookie behaviour on real phones is the open item from 2.9.
