---
title: 'Story 2.9: An interrupted answer is kept on the phone'
type: 'feature'
created: '2026-11-26'
status: 'done'
baseline_revision: '3f7265a5cb3c2e9718fd6ef6816bf15c8d2b60ed'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/key-form-steps.html'
warnings: [oversized]
deferred:
- summary: >-
    The Draft offer relies on the browser dropping the session cookie `rsvp_visit`; phones and in-app browsers (Messenger) may keep session cookies, so a returning guest may see the step instead of the offer.
  reason: >-
    Cannot be checked in Edge; needs a check on Rikke's own phone and Messenger (issues.md) and can be revisited in Story 4.1 or the usability test.
- summary: >-
    After a household change, «Ja, fortsett» opens step 1 with consent cleared and no message telling the guest why.
  reason: >-
    Rare (the couple edits a household mid-answer); a new text and state belong with Story 4.1's household-change messages.
- summary: >-
    A CSRF failure on the offer's POST shows the step page with the CSRF notice instead of the offer again.
  reason: >-
    Rare (expired token); the guest gets a clear notice and can continue.
- summary: >-
    An answered household's draft cookie gets no notice or offer and is not deleted, also after the deadline.
  reason: >-
    Story 4.1 reopens the form for answered households and decides it there; recorded in deferred-work.md.
---

<intent-contract>

## Intent

**Problem:** The draft cookie (Stories 2.1–2.6c) already keeps the answers, but nothing tells a returning guest that they exist: the front page says nothing, the form silently resumes, and a draft whose household has changed is thrown away as "broken" (draft.py docstring: «Story 2.9 will drop changed members instead of deleting»). Bestefar Sigmund must be offered his half-finished answer after Messenger reloads (FR-78, UX-DR26).

**Approach:** (1) The front page's RSVP sheet shows the warning notice «Du har et svar som ikke er sendt ennå.» when a usable draft cookie exists. (2) Any GET of a form address with a draft, at the start of a visit, shows the Draft offer sheet instead of the step; «Ja, fortsett» and «Nei, begynn på nytt» are POST buttons. A visit is marked by a browser-session cookie `rsvp_visit` (no answers in it). (3) `read_draft` drops members no longer in the household instead of treating the draft as broken, clears consent, and sends the guest to step 1. (4) After the deadline: no notice, no offer, the cookie is deleted (AD-11, `is_past_deadline`).

## Boundaries & Constraints

**Always:**
- No JavaScript; the offer is a server-rendered paper sheet with two POST buttons in one `<form>` with `{% csrf_token %}` (AD-1, AD-7). Breakpoints in `em`.
- The draft is still written only on a POST (AD-8): «Fortsett», «Velg», «Ja, fortsett». A GET may delete the draft cookie (deadline, broken) but never writes it.
- `rsvp_visit`: value `"1"`, no `max_age`/`expires` (browser-session cookie), path `mount.cookie_path`, `HttpOnly`, `SameSite=Lax`, `Secure` when `settings.IS_PRODUCTION`. Set on every response that writes the draft, on «Ja, fortsett» and on «Nei, begynn på nytt». It holds no answer (AD-8 «no hidden fields/session hold answers» still holds).
- The offer is shown when: method GET/HEAD, a usable draft exists (after member dropping), and no `rsvp_visit` cookie. It replaces the requested step's page (status 200, same URL), whatever step or the check page was requested.
- «Ja, fortsett» (`action=resume`): writes the (cleaned) draft, sets `rsvp_visit`, 303 to `mount.url(first_unfinished(steps, draft.done, None))` (the check page when all applicable steps are done); a changed household → step 1.
- «Nei, begynn på nytt» (`action=restart`): deletes `rsvp_draft`, sets `rsvp_visit`, 303 to step 1 (`mount.base_path`), which then starts empty. ("From the sent answer" needs Story 4.1: an answered household never reaches the form today.)
- Household changed = any id in `resp`/`att`/`days`/`night`/`meals`/`alg`/`cons`/`conf`/`long`/`hike` that is not a member, or, when `"who"` is in `done`, a member missing from `att`. Then: those ids are dropped everywhere, `resp` becomes the link owner if dropped, `done = []`, `cons = {}`, `conf = []`, `cv = None` (AD-18: no consent «Ja» across a household change; deferred-work 2.4/2.6b entry). `rev` is kept (the 2.6c revision check still guards the send).
- Every rule, view, template comment and test names its FR/AD/UX-DR ids (FR-78, AD-8, AD-11, UX-DR26).
- UI text Norwegian, code English.

**Never:**
- No Django session, messages framework, DB row or hidden answer fields (AD-8).
- No notice or offer for a household that has answered (Story 2.8 redirects its form GETs to `#status`; the status block replaces the sheet). Its draft cookie is left untouched for Story 4.1 (EXPERIENCE: offered later with the conflict notice).
- Not in scope: the stale-tab POST of an answered household (issues.md, routed to Story 4.1); recording the consent-text version the guest saw beyond what 2.6c already does (`cv`, deferred low item stays open); the leave warning dialog (needs JS).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Notice on front page | GET `/<code>/`, valid draft cookie, unanswered, before deadline | RSVP sheet holds the warning notice «Obs: Du har et svar som ikke er sendt ennå.» above the button | — |
| No draft | GET `/<code>/` or `/<code>/svar/` without cookie | No notice; step 1 as today | — |
| Offer on entry | GET any `/<code>/svar/…` step or `se-over/`, draft, no `rsvp_visit` | Draft offer sheet: `h1` «Vil du fortsette der du slapp?», start line, «Ja, fortsett», «Nei, begynn på nytt» | — |
| Within a visit | Same GET with `rsvp_visit` set | The step as today (no offer) | — |
| Ja | POST `action=resume` | 303 to first unfinished step (or `se-over/`), answers filled in; draft + `rsvp_visit` set | — |
| Nei | POST `action=restart` | 303 to `/<code>/svar/`, `rsvp_draft` deleted (Max-Age=0), `rsvp_visit` set; step 1 empty | — |
| Household changed | Draft names Geir, Geir deleted/moved; or a member added after step 1 | Offer shown; Ja → 303 to step 1, only current members, dropped persons' answers gone, consent cleared | Never 500, never "broken" |
| After deadline | Draft cookie, deadline passed | `/<code>/`: no notice, response deletes `rsvp_draft`; `/<code>/svar/…`: closed page, deletes `rsvp_draft` | — |
| Answered household | Draft cookie, household has answered | Front page: status block, no notice; cookie not deleted; form GETs still → `#status` | — |
| Broken draft | Bad signature / old format | No notice; front page and form delete the cookie; no offer | — |
| POST resume/restart without draft | `action=resume` with no/broken draft | 303 to step 1, sets `rsvp_visit`, deletes a broken cookie | — |

</intent-contract>

## Code Map

- `wedding/rsvp/draft.py` -- `_parse` (≈L267) returns None on any non-member key; `_member_key` (L160), `_attendance` (L166), `_bools`/`_key_lists`/`_allergy_entries`/`_id_list`/`_hike` all reject non-members. `read_draft` (≈L332) returns `(draft, broken)`. Change: parse ids as any positive int, then filter to `member_ids`; add a `changed` result. Module docstring (L1–31) lists what is broken: rewrite the member sentences. `Draft.started` is the UTC ISO start time for the offer line. Add `VISIT_COOKIE`, `mark_visit(response, mount)`, `has_visit(request)`.
- `wedding/rsvp/views.py` -- `handle_step` (L1279–1314): reads the draft, dispatches `_who_is_coming`/`_later_step`, writes normalised draft. Insert the offer/resume/restart branch here, before dispatch. `_owner` (L159) gives the link owner. `_steps` (L178) and `first_unfinished` (imported L105) give the resume target. `_see_other` (L334) for 303s. `render_after_csrf_failure` (L1317) and `render_total` (L1432) call `read_draft` too: adapt to the new return shape, no offer there. `_changed_text` (L643) shows the Oslo date format `dateformat.format(local, 'l j. F Y')` + `'H:i'` to reuse.
- `wedding/rsvp/templates/rsvp/step.html` -- the step sheet layout to mirror; new `rsvp/draft_offer.html` (same base, paper sheet on green, no nav bar, footer band).
- `guests/views.py` -- `front_page` (L159–189, `@require_safe`) gets the notice flag and deadline delete; needs `household_members` (already imported for `_rsvp`) only when the cookie is present. `_rsvp` (L240–287): after-deadline branch (L271) must also delete the draft cookie on the closed page; the answered redirect (L262–270) stays first. `_guest_mount` (L232) gives the cookie path.
- `guests/templates/guests/front_page.html` -- RSVP sheet L182–196: notice goes between `rsvp__deadline` and the button (DESIGN.md L675 «a warning notice sits above the button»).
- `wedding/templates/wedding/components/notice.html` -- `{% include … with variant="warning" text="…" only %}`; the warning variant adds «Obs:» itself, so `text` is «Du har et svar som ikke er sendt ennå.».
- `wedding/rules/deadline.py` -- `is_past_deadline(deadline, now)`, the one deadline function (AD-11).
- `tests/test_rsvp_draft.py` -- existing broken-draft tests (L318–352); tests that build a cookie by hand and then GET now need `rsvp_visit` set (or expect the offer). `tests/test_front_page.py`, `tests/test_front_page_status.py` for front-page patterns; `tests/conftest.py` `seeded` fixture (Mona + Geir unanswered, Marie answered).
- `wedding/fixtures/seed.toml` L243–258 -- Mona (`test-mona0000000000000`) and Geir, the unanswered test household.

## Tasks & Acceptance

**Execution:**
- `wedding/rsvp/draft.py` -- Make member checks tolerant: accept any digit-string/int id in every per-member field, then drop ids not in `member_ids`; drop a non-member `resp` (caller replaces it). Return `ReadResult`-style `(draft, broken, changed)` from `read_draft` (or a small dataclass), where `changed` follows the Always definition and the returned draft is already cleaned (`done=[]`, `cons={}`, `conf=[]`, `cv=None` when changed). Add `VISIT_COOKIE = "rsvp_visit"`, `mark_visit(response, mount)` and `has_visit(request)`. Update the docstring (AD-8, FR-78, Story 2.9) -- the household-changed rule moves from "broken" to "cleaned".
- `wedding/rsvp/views.py` -- In `handle_step`: if `changed` and `resp` was dropped, set `resp = _owner(actor, members)`. GET/HEAD with a draft and no visit → render `rsvp/draft_offer.html` (context: `page_context`, the start line text, form action = current path). POST `action=resume` / `action=restart` handled before step dispatch as in Always (also `?fra` ignored). Every draft write also calls `mark_visit`. Adapt `render_after_csrf_failure` and `render_total` to the new read result. Extend the module docstring (Story 2.9, FR-78, AD-8, UX-DR26).
- `wedding/rsvp/templates/rsvp/draft_offer.html` -- New: extends the base like `step.html`, one paper sheet: `h1` «Vil du fortsette der du slapp?», `<p>` «Du begynte på svaret {weekday} {j. F} kl. {H:i}. Det du har fylt ut, er tatt vare på på denne telefonen.» (Oslo time; year omitted like the mockup), then one form: primary `<button name="action" value="resume">Ja, fortsett</button>`, secondary `<button … value="restart">Nei, begynn på nytt</button>` below it, full width. `<title>` «Vil du fortsette der du slapp? – Invitasjon». Comment block names FR-78, AD-8, UX-DR26.
- `static/css/…` (the stylesheet `step.html` uses) -- only if the offer needs a rule the step sheet lacks; reuse `.button`/secondary button classes; no px breakpoints.
- `guests/views.py` -- `front_page`: when unanswered and `rsvp_draft` is present: past deadline → render without notice and `delete_draft`; else `read_draft` with `household_members` → `draft_waiting` true for a usable draft, delete a broken one. Answered: ignore the cookie. `_rsvp`: closed page response deletes the draft cookie (AD-11). Docstrings name FR-78, AD-8, AD-11, UX-DR26 and the extra SELECT only when the cookie is present.
- `guests/templates/guests/front_page.html` -- `{% if draft_waiting %}` warning notice above the RSVP button.
- `tests/test_rsvp_draft_offer.py` -- New: every I/O matrix row; AD-8 AC test: GET `/<code>/` with the cookie set at path `/<code>/` sees the notice; offer on step 1, a later step and `se-over/`; Ja target with done steps and with all done; Nei deletes the cookie and step 1 has nothing checked; Geir deleted → Ja → step 1 lists only Mona, `cons`/`conf` empty in the written cookie; member added after step 1 → step 1; deadline (monkeypatch `timezone.now` or settings deadline) → no notice and `Max-Age=0` for `rsvp_draft` on front page and form; answered household (Marie) → no notice, cookie not deleted; `rsvp_visit` attributes (no Max-Age, HttpOnly, path); no session rows.
- `tests/test_rsvp_draft.py` and other `tests/test_rsvp_*.py` -- Replace "non-member key is broken" expectations with the drop rule; add `rsvp_visit` where a test sets the cookie by hand and expects a step.
- `docs/manual-test-plan.md` -- Add MT-59 to MT-64 (Norwegian, result cells empty, each «Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`)», after `migrate` + `seed_testdata` + `runserver`, on `test-mona0000000000000`): MT-59 fill step 1 and 2, new context with only cookies whose `expires` > 0 from `storageState` (a closed browser drops session cookies), open `/test-mona…/` → notice; tap «Svar på invitasjonen» → offer; «Ja, fortsett» → step 3 with step 1–2 answers kept when opening «Tilbake». MT-60 same, «Nei, begynn på nytt» → step 1 with nothing checked, front page without notice. MT-61 after step 1, `Guest.objects.filter(code="test-geir0000000000000").delete()` via `manage.py shell -c`, restart context → Ja → step 1 shows only Mona; reseed after. MT-62 deadline two days back (MT-56 command) → front page without notice, `rsvp_draft` gone from the context's cookies; reseed after. MT-63 keyboard only: Tab to «Ja, fortsett», Enter; focus ring `outline-style: solid`. MT-64 offer and front page with notice at 360×640 and 180×320, 16px and 20px (CDP `Page.setFontSizes`): `scrollWidth` ≤ `innerWidth`, both buttons ≥ 44px high and inside the sheet.
- `.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md` -- AD-8 «A broken draft» bullet: dated note (2026-11-26, Story 2.9): a household change no longer makes the draft broken; non-members are dropped, consent cleared, the form opens at step 1 (epics Story 2.9 AC), and the `rsvp_visit` session cookie marks a visit. AD-11: note that the front page and closed page delete the draft.
- `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md` -- Microcopy rows L126–127: mark decided (avgjort av Claude 2026-11-26, Story 2.9) incl. the start line; Interaction Primitives L299: note what "opening the form" means (a new browser visit, `rsvp_visit`), that «Ja» goes to the first unfinished step, and that answered households get no offer until Story 4.1.
- `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md` -- Draft offer row L687: dated note that the buttons are one POST form, secondary below primary.
- `README.md` -- status line (Story 2.9 done, epic 2 complete), mention the `rsvp_visit` cookie where the draft cookie is described.
- `.docs/implementation-artifacts/deferred-work.md` -- Mark the 2.4/2.6b «no consent Ja across a revision change» entry as covered by 2.6c + 2.9; leave the consent-text-version entry open with "not taken in 2.9".

**Acceptance Criteria:**
- Given an unanswered household with a draft cookie at path `/<code>/`, when the guest GETs `/<code>/` before the deadline, then the RSVP sheet shows «Obs: Du har et svar som ikke er sendt ennå.» above «Svar på invitasjonen».
- Given a draft and a fresh browser visit, when the guest GETs `/<code>/svar/`, any later step or `se-over/`, then the page is the Draft offer with «Vil du fortsette der du slapp?», the start time line, «Ja, fortsett» and «Nei, begynn på nytt», and no step fields.
- Given the offer, when «Ja, fortsett» is posted, then the response is 303 to the first unfinished step (or `se-over/`), and that step's GET shows the saved answers checked; when «Nei, begynn på nytt» is posted, then `rsvp_draft` is deleted and step 1 shows nothing checked.
- Given a draft naming a guest no longer in the household, when «Ja, fortsett» is posted, then the response is 303 to `/<code>/svar/`, step 1 lists only current members, and the written draft holds no id of the removed guest and no consent answers.
- Given a draft cookie after the deadline, when the guest GETs `/<code>/` or a form address, then no notice or offer appears and the response deletes `rsvp_draft`.
- Given the whole guest flow including the offer, then no session row is created (AD-8).

## Spec Change Log

## Review Triage Log

### 2026-11-26 — Review pass
- verdicts: 24 findings — high 0, medium 2, low 8, false 14, maybe-false 0
- findings:
  - `[medium]` `[patch]` The front-page notice for a changed-household draft is not tested (verification-gap) — no test GETs `/<code>/` with a draft naming a deleted member; a regression would silently delete Mona's draft. Test added.
  - `[low]` `[patch]` `test_a_member_missing_from_step_1_goes_to_step_1` was loosened to `in (302, 303)` (verification-gap, blind, edge) — the test now pins the one status the path returns.
  - `[low]` `[patch]` `render_total` passes `members[0][0]` as owner while the other readers use `_owner(actor, members)` (verification-gap, blind, edge) — inconsistent fallback respondent; uses the same owner rule now.
  - `[false]` `[reject]` `ReadResult.changed` is never read (verification-gap) — tests in test_rsvp_draft.py read it; kept as the documented result of the cleaning, used by the tests to tell changed from usable.
  - `[false]` `[reject]` A cleaned draft is never rewritten on GET (verification-gap) — intended by AD-8 (no write on GET); every reader cleans via `read_draft`.
  - `[medium]` `[defer]` The offer depends on session cookies being dropped; phones and in-app browsers (Messenger) may keep them (blind, intent-alignment) — real and unverifiable here; recorded in EXPERIENCE/AD-8 by the implementer; a check on Rikke's own phone goes to issues.md, and Story 4.1/usability test can revisit.
  - `[low]` `[defer]` The guest is not told why «Ja, fortsett» starts at step 1 after a household change (blind) — rare (couple edits household mid-answer); a notice is a new text and state; deferred to Story 4.1 with the other household-change messages.
  - `[false]` `[reject]` A cleaned draft gets a false revision-conflict message at send (blind) — `Household.revision` rises only in `send_answer` (wedding/services/answers.py:211); adding, removing or moving a guest does not change it.
  - `[low]` `[defer]` No deferred-work entry for the answered-household draft handed to Story 4.1 (blind) — entry added with source_spec 2.9.
  - `[false]` `[reject]` The spec records only status, not the decisions (blind) — the spec written in step 2 holds the decisions (visit cookie, first unfinished step, cleaning); the diff only shows frontmatter because the spec was committed before the baseline.
  - `[false]` `[reject]` The offer page has no nav or link back (blind) — like every form step (rsvp/step.html), per DESIGN.md › form steps; the footer band stays.
  - `[false]` `[reject]` «på denne telefonen» assumes a phone (blind) — approved text from EXPERIENCE.md and the mockup (UX-DR26).
  - `[low]` `[patch]` The template comment says «no hidden fields» but `{% csrf_token %}` renders one (blind) — comment corrected.
  - `[low]` `[defer]` A CSRF failure on the offer POST shows the step page with the CSRF notice instead of the offer (blind, edge) — the guest gets a clear notice and can continue; rare (expired token); deferred.
  - `[false]` `[reject]` HEAD getting the offer is untested (blind) — Django's test client HEAD goes through the same branch as GET (`request.method in ("GET", "HEAD")`); low value.
  - `[false]` `[reject]` `?fra` ignored by `_answer_offer` untested (blind) — no code reads it there; nothing to break.
  - `[false]` `[reject]` POST to a step without `rsvp_visit` untested (blind) — existing step tests post without the cookie and pass.
  - `[false]` `[reject]` `render_total` with a cleaned draft untested (blind) — covered by the owner fix; the total does not depend on the respondent.
  - `[low]` `[reject]` The closed page and front page leave `rsvp_visit` (blind) — holds no answer and dies with the browser session; harmless.
  - `[low]` `[reject]` README status paragraph is long (blind) — pre-existing structure; a README tidy-up belongs to the epic 2 retrospective.
  - `[false]` `[reject]` New MT rows not run while README says epic 2 is done (blind) — MT-59 to MT-64 run in Edge and recorded.
  - `[false]` `[reject]` Couple's override mount reaches the offer (edge) — `handle_step` is called only from the guest mount (guests/views.py:306); no couple mount exists yet.
  - `[false]` `[reject]` «Ja» goes to the first unfinished step, not the last page seen (intent-alignment) — decided in the spec; the draft stores no last page and in the forward flow they are the same; MT-59 confirmed step 3.
  - `[false]` `[reject]` «Nei» never starts from a sent answer (intent-alignment) — answered households get the status page (2.8) until Story 4.1 reopens the form; recorded in the spec and AD-11.

## Design Notes

- **Why a session cookie for the visit:** the offer must come "first" on any route, yet the PRG redirect to the next step is also a GET, and AD-8 forbids writing the draft on a GET. A browser-session cookie set on every POST separates "inside a visit" from "came back": a closed in-app browser or a killed Messenger web view loses it, which is exactly the FR-78 case. A reload inside a still-living tab shows the step itself with all answers, which meets the story's goal (nothing lost). Recorded in EXPERIENCE/AD-8.
- **«Ja» target:** the draft does not record the last page seen (a GET cannot write it), so "the step they left" is the first unfinished applicable step, the check page when all are done.
- **Wording decisions (Claude, 2026-11-26):** notice and offer texts from EXPERIENCE L126–127 and the mockup are kept verbatim; start line without year (the mockup), Oslo time, weekday from Django's Norwegian locale.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass, incl. `tests/test_rsvp_draft_offer.py`
- `uv run ruff check` -- expected: no errors
- `uv run ruff format --check` -- expected: no changes
- `uv run djlint --check .` -- expected: no changes

**Manual checks (if no CLI):**
- MT-59 to MT-64 rows exist in `docs/manual-test-plan.md` with empty result cells (the orchestrator runs them with Playwright in Edge).

## Auto Run Result

Status: done

**Summary:** A guest who leaves the RSVP form and comes back in a new browser session gets «Obs: Du har et svar som ikke er sendt ennå.» on the front page and «Vil du fortsette der du slapp?» on any form address, with when the answer was started, «Ja, fortsett» (first unfinished step with every answer filled in) and «Nei, begynn på nytt» (draft deleted, empty step 1). A browser-session cookie `rsvp_visit` (no answers) tells a return from moving between steps, since AD-8 forbids writes on GET. A draft whose household changed is cleaned instead of thrown away: people no longer in the household are dropped, consent is cleared and the form opens at step 1. After the deadline the front page and the closed page delete the draft with no notice.

**Files changed:**
- `wedding/rsvp/draft.py` — `read_draft` cleans changed households, `rsvp_visit` helpers.
- `wedding/rsvp/views.py`, `wedding/rsvp/templates/rsvp/draft_offer.html` — the offer and its two answers; running total uses the same owner rule.
- `guests/views.py`, `guests/templates/guests/front_page.html` — notice, deadline and broken-draft deletion.
- `tests/test_rsvp_draft_offer.py` (new), `tests/test_rsvp_draft.py`, `tests/test_rsvp_days.py`, `tests/test_rsvp_send.py`.
- ARCHITECTURE-SPINE (AD-8, AD-11), EXPERIENCE.md, DESIGN.md, README.md, deferred-work.md, docs/manual-test-plan.md (MT-59 to MT-64).

**Review:** 24 findings — 4 patched (front-page notice test after a removed member, exact 302 in the send test, same owner in the running total, template comment), 4 deferred, 16 rejected with reasons in the triage log.

**Follow-up review recommendation:** false. No high finding; the medium patch is a test, and the browser rows were re-run after the fixes.

**Verification:** `uv run pytest` 1338 passed; ruff and djlint clean; MT-59 to MT-64 run by Claude with Playwright 1.56.1 in Edge after the patches, including a simulated browser restart (only cookies with expires > 0 kept), keyboard only, 360 and 180px at 16 and 20px text.

**Residual risks:** whether a real phone or Messenger drops the session cookie when the app is closed is untested; if it does not, the guest lands on the step with all answers filled in rather than the offer (the answer is still kept).
