---
title: 'Story 2.6c: A send that fails or repeats is safe'
type: 'feature'
created: '2026-11-24'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-6b-allergies-are-stored-only-with-consent.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-6a-send-the-answer.md'
warnings:
  - oversized
deferred: []
---

<intent-contract>

## Intent

**Problem:** `send_answer` (2.6a/2.6b) has no submission id, no revision check, no total check and no failure handling: a double tap or a second tab can write twice or crash with an IntegrityError, an old draft silently overwrites a newer answer (and carries a consent «Ja» across it), a price change goes unnoticed, a failed write gives a 500, and the «Sender …» button stays busy after a failed or aborted send (NFR-1, AD-7, AD-9, AD-18, AD-20, UX-DR52; deferred-work «From Story 2.6a», «From Story 2.6b», 2.4 entries on the consent version).

**Approach:** Add `Submission` (migration `0007`) and make `send_answer` check, in its one IMMEDIATE transaction, the repeat first (return the earlier `HouseholdAnswer`), then the revision, the deadline, the consent-text version the guest saw and the total the check page showed; any refusal writes nothing and records no `Submission`. The check page's form carries a one-time submission id and the total it showed as hidden fields; the view turns refusals and database failures into a 303 back to the check page with a focused notice, keeping the draft; `rsvp-send.js` sends with `fetch` so an aborted send resets the button and shows the same failure notice.

## Boundaries & Constraints

**Always:**
- **Model (AD-20, AD-4), `wedding/models.py` + `wedding/migrations/0007_submission.py`:** `Submission` — `key` UUIDField(unique), `kind` CharField(20, choices `answer` «svar»; constant `Submission.ANSWER`), `object_id` PositiveBigIntegerField (the id of what was written: the `HouseholdAnswer`), `created_at` DateTimeField. Norwegian `verbose_name`s, `__str__` «Innsending <id>». Not in Django admin. Docstring: Story 2.6c, AD-20, NFR-1.
- **Exceptions (`wedding/services/exceptions.py`), all `ServiceError`, Norwegian `default_message`:** `RevisionConflict` (AD-9; attribute `revision`: the household's current revision), `TotalChanged` (AD-7), `ConsentTextChanged` (AD-18, FR-29).
- **Service (`wedding/services/answers.py`), new keyword-only parameters** `submission: UUID`, `revision: int`, `shown_total: int`, `consent_version: str | None`. Order inside `transaction.atomic()`: admin actor → other household (`NotAllowed`) → **repeat:** a `Submission` with `key=submission` exists → if its `HouseholdAnswer` belongs to `household` return it and write nothing, else `NotAllowed` (AD-3) → respondent/answer ids (`NotAllowed`) → missing member (`InvalidAnswer`) → **revision:** re-read `Household.revision` in the transaction; `!= revision` → `RevisionConflict(revision=current)` → deadline → normalise → allergy problems (`InvalidAnswer`) → **consent text:** any coming guest with a consent answer and `consent_version != CONSENT_TEXT_VERSION` → `ConsentTextChanged` → **total:** `household_total(answer, form_prices(settings))` `!= shown_total` → `TotalChanged` → existing writes → `Submission.objects.create(key, kind=ANSWER, object_id=sent.pk, created_at=now)`. Docstrings name Story 2.6c, AD-7, AD-9, AD-18, AD-20, NFR-1.
- **Draft format 6 (AD-8, AD-18), `wedding/rsvp/draft.py`:** add `cv: str | None` (the consent-text version shown on step 5 when the guest last posted it). `VERSION = 6`; a format 5 cookie is broken (existing pattern). `_allergies_step` sets `new.cv = CONSENT_TEXT_VERSION` on every path that returns a draft. The total is **not** stored in the draft (see Design Notes).
- **Check page (AD-7, AD-20), `_render_check` + `rsvp/check.html`:** two hidden inputs in the send form: `innsending` = a fresh `uuid4()` per render, `sum` = the rendered total. A `?sending=<reason>` query (`feilet`, `endret`, `sum`, `samtykke`; anything else ignored) adds a focused error notice (`variant="error"`, `focus=True`) at the top of the sheet. A hidden client-side failure notice (`<div data-send-failed hidden tabindex="-1">` holding the notice include with `live=True`) for the script.
- **View (`_later_step` send branch, `wedding/rsvp/views.py`):** missing/malformed `innsending` (not a UUID) or `sum` (not an int) → 303 to the check page, nothing written. Pass `submission`, `revision=draft.rev`, `shown_total`, `consent_version=draft.cv`. On success (including a repeat): 303 to `sendt/`, draft deleted. `TotalChanged` → 303 `se-over/?sending=sum`, draft unchanged. `RevisionConflict` → rewrite the draft with `rev = exc.revision`, `cons = {}`, `conf = []` (AD-18: no «Ja» across a revision change) and 303 `?sending=endret`. `ConsentTextChanged` → rewrite with `cons = {}`, `conf = []`, `cv = None`, 303 `?sending=samtykke`. `DatabaseError` (includes `IntegrityError`, `OperationalError`) → log `"Sending the answer failed (%s)"` with only the exception class name, 303 `?sending=feilet`, draft neither deleted nor rewritten. `DeadlinePassed` unchanged (closed page). Rewritten drafts go through `_settled` like any write. **Repeat without a draft:** before the «no draft → step 1» gate (`_later_step:1026`), a send POST whose `innsending` matches a `Submission` of the actor's household (new selector `submitted(household, key) -> bool` in `wedding/selectors.py`, one SELECT) goes 303 to `sendt/`, so a late second tap after the first response deleted the cookie still shows the receipt (AD-20).
- **Notice texts** (Claude decides wording; «Feil:» prefix comes from the component):
  - `feilet`: «Svaret ble ikke sendt, fordi noe gikk galt da det skulle lagres. Ingenting er tapt: alt du fylte ut, står her fortsatt. Prøv igjen med «Send svaret».» + « Går det fortsatt ikke, ring <navn> på <telefon> eller <navn> på <telefon>.» built from `page_context["contacts"]` (omit the sentence when empty; one contact → no «eller»).
  - client (script): the same, with «fordi forbindelsen ble brutt» instead of «fordi noe gikk galt da det skulle lagres».
  - `endret`: «Svaret ble ikke sendt, fordi <sent_by_name> sendte et svar for husstanden <l j. F Y> kl. <H:i> etter at du begynte. Se over svaret og send det på nytt. Samtykke til å lagre allergier må gis på nytt.» Oslo time as on the sent page; without a `HouseholdAnswer` (GuestActor only; read with `household_answer`): «… fordi svaret for husstanden er endret etter at du begynte. …».
  - `sum`: «Svaret ble ikke sendt, fordi summen har endret seg. Se over den nye summen og send svaret på nytt.»
  - `samtykke`: «Svaret ble ikke sendt, fordi teksten om lagring av allergier er endret etter at du svarte. Les den nye teksten under «Allergier og matbehov» og svar på nytt før du sender.»
- **Script (`static/js/rsvp-send.js`, UX-DR15, UX-DR52):** keep busy state and the second-submit guard. On submit: `preventDefault`, `fetch(form.action || location.href, {method: "POST", body: FormData(form) + action=send, credentials: "same-origin"})`. Response `redirected` → `location.assign(response.url)`. Any other response → append a hidden `action=send` input and `HTMLFormElement.prototype.submit.call(form)` so the server's own page (e.g. the 403 CSRF page) shows; the submission id makes that repeat safe. Network failure (`catch`) → reset label and `aria-disabled`, `busy = false`, unhide `[data-send-failed]` and focus it. Keep the `pageshow` restore. Without JavaScript the form still posts natively.
- Privacy and quality: no names, notes or codes in logs or exceptions; only `wedding/services/` writes (`tests/test_only_services_write.py` green); every new model, exception, service branch, view branch and test names its FR/NFR/AD.

**Never:**
- No draft field for the total, and no draft write on the check page's GET (AD-8).
- No «what differs» comparison on a revision conflict (AD-9 asks for it; it belongs with changing a sent answer, Story 4.1; recorded in deferred-work and AD-9's note). No answered-household redirect (Epic 4), no receipt content (2.7), no seeded answers (2.6d), no couple override mount (4.4).
- No change to step texts, `CONSENT_TEXT_VERSION`, `normalise_answer` or the consent rules of 2.6b.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| First send | new key, rev matches, total matches | rows written; one `Submission` (kind `answer`, object = `HouseholdAnswer`); revision +1 | none |
| Double tap | same key again (also after a re-send) | earlier `HouseholdAnswer` returned; no new `Consent`, revision unchanged; view → `sendt/` | none |
| Key of another household | existing key whose answer is another household's | nothing written | `NotAllowed` |
| Two tabs / devices, first sends | two keys, both drafts at rev 0 | first writes; second refused, no IntegrityError | `RevisionConflict`; view `?sending=endret`, draft rev updated, `cons`/`conf` cleared |
| Retry after refusal | conflict, then send again (new key) | handled as a new send, writes | none |
| Price changed | `shown_total` ≠ recomputed | nothing written, no `Submission` | `TotalChanged`; `?sending=sum` |
| Draft changed in another tab | tab B adds a meal; tab A sends its page | A's `sum` ≠ recomputed | as above |
| Consent text changed | a coming guest answered consent; `cv` ≠ current | nothing written | `ConsentTextChanged`; `?sending=samtykke`, consent cleared |
| Text changed, no consent answered | `cv` None, `cons` empty | sends | none |
| Database fails | `send_answer` raises `OperationalError` | nothing written, draft cookie untouched | `?sending=feilet` notice with phones |
| Late repeat, draft gone | same key, no draft cookie | 303 to `sendt/`, nothing written | none |
| Bad hidden fields | `innsending` "x" or `sum` missing | nothing written | 303 to check page |
| Network abort (browser) | fetch rejects | button back to «Send svaret», failure notice shown and focused | client-side |

</intent-contract>

## Code Map

- `wedding/services/answers.py:93-160` `send_answer` — add parameters and the checks in the order above; `:1-10` module docstring (drop «The submission id and revision check are Story 2.6c»). Reuse `household_total` (`wedding/rules/money.py`) and `form_prices` (`wedding/selectors.py:88`, importing a selector into a service is fine; or `programme_prices(settings) | {CABIN: …}` directly) with the `Settings` row the deadline check already reads (`:126-129`; read it once).
- `wedding/services/exceptions.py:48-51` — add the three exceptions after `InvalidAnswer`.
- `wedding/services/consent.py` — `CONSENT_TEXT_VERSION`; docstring: the seen version is checked at send (2.6c).
- `wedding/models.py` — append `Submission` after `Consent` (`:220+`); module docstring `:1-12` gains Story 2.6c. Migration: latest is `0006_allergy_consent.py`.
- `wedding/rsvp/draft.py:47` `VERSION`; `:54-111` `Draft` + `payload` (docstring «format version 5» → 6, `cv`); `:115-131` `PAYLOAD_KEYS`; `:253-318` `_parse` (validate `cv`: `None` or a string ≤ 20 chars, else broken); module docstring `:1-30` gains format 6.
- `wedding/rsvp/views.py` — `:1-38` module docstring; `:599-631` `_render_check` (new context `submission`, `sending_notice`, `send_failed_text`); `:887-933` `_allergies_step` (set `cv`); `:1077-1092` send branch (parse fields, call, map exceptions; it must return the rewritten draft as `new` so `handle_step:1131-1137` writes it); `render_after_csrf_failure` `:1142+` goes through `_render_check`, so it gets the hidden fields too. Import `CONSENT_TEXT_VERSION`, `household_answer`, the exceptions, `DatabaseError`, `uuid`, `logging`.
- `guests/views.py:208-239` `_rsvp` — unchanged; `page_context["contacts"]` (from `footer_contacts`, list of dicts with name and phone) feeds the phone sentence.
- `wedding/rsvp/templates/rsvp/check.html` — hidden inputs, the `sending` notice above the `csrf_failed` one, the `[data-send-failed]` block; update the template comment («No hidden fields» is no longer true).
- `static/js/rsvp-send.js` — rewrite per Always; update header comment.
- Tests: `tests/test_send_answer.py:110-112` `_send` helper gains `submission=uuid4()`, `revision=<household.revision>`, `shown_total=<computed>`, `consent_version=CONSENT_TEXT_VERSION` defaults so the 2.6a/2.6b tests keep passing; `tests/test_rsvp_send.py:41` `_send` posts the page's `innsending` and `sum` (read them from the GET of the check page); `tests/test_rsvp_draft.py:161-191` 4 KB test includes `cv`; draft format tests. `tests/helpers.py` `row_counts` gains `Submission` if it lists models.
- Docs: `README.md:9` status, `:77-81` «Svarskjemaet», `:164` services line; ARCHITECTURE-SPINE (`.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md`) AD-7 `:127`, AD-8 format note, AD-9 `:148-155`, AD-18 `:243`, AD-20 `:262`; EXPERIENCE.md `:237` «Save failed»; `docs/manual-test-plan.md` after MT-44; `.docs/implementation-artifacts/deferred-work.md:216-256`.

## Tasks & Acceptance

**Execution:**
- [ ] `wedding/models.py`, `wedding/migrations/0007_submission.py` — `Submission` (AD-20).
- [ ] `wedding/services/exceptions.py` — `RevisionConflict`, `TotalChanged`, `ConsentTextChanged`.
- [ ] `wedding/services/answers.py`, `wedding/services/consent.py` docstring — the checks and `Submission` write (AD-7, AD-9, AD-18, AD-20, NFR-1).
- [ ] `wedding/rsvp/draft.py` — format 6 with `cv`.
- [ ] `wedding/rsvp/views.py` — `cv` on step 5; hidden fields and notices on the check page; send branch mapping refusals and `DatabaseError`.
- [ ] `wedding/rsvp/templates/rsvp/check.html`, `static/js/rsvp-send.js` — hidden fields, notices, fetch send with reset.
- [ ] `tests/test_send_answer.py` — every matrix service row with `now` fixed; repeat returns the same object and adds no `Consent`/`PersonAnswer` change and no revision bump; a repeat after a re-send returns the re-send's answer; refused sends (conflict, total, consent text, deadline, other household's key) leave `Submission` count 0 and all rows unchanged; two keys at the same revision → second `RevisionConflict` with `revision` = 1; migration/model fields; `str()` has no name.
- [ ] `tests/test_rsvp_send.py` — check page has `innsending` (a UUID, different on two GETs) and `sum` equal to the shown total; posting the same form twice → one `HouseholdAnswer`, one `Submission`, both 303 to `sendt/`; the same POST again without the draft cookie → 303 `sendt/`; second draft at old revision → 303 `?sending=endret`, Set-Cookie draft with new `rev` and no `cons`, GET shows the notice with «Sigmund» and the time, re-send succeeds; price changed in `Settings` between GET and POST → `?sending=sum`; `send_answer` monkeypatched to raise `OperationalError` → `?sending=feilet`, no draft deletion cookie, GET notice contains «Prøv igjen» and both seeded phones, `caplog` has no guest name; consent version monkeypatched in `wedding.services.answers` → `?sending=samtykke` and `cons` cleared; bad `innsending`/missing `sum` → 303 check, nothing written; unknown `?sending=x` shows no notice; step 5 POST writes `cv`; the CSRF-failure check page also carries the hidden fields.
- [ ] `tests/test_rsvp_draft.py` — format 6 round trip with `cv`; format 5 broken; `cv` of wrong type or too long broken; 4 KB test with `cv`.
- [ ] `docs/manual-test-plan.md` — Norwegian rows MT-45 to MT-49, date and result cells empty, each «Kjøres av Claude med Playwright mot Edge (`channel: 'msedge'`)», before each `uv run manage.py seed_testdata` then `uv run manage.py runserver`, measured after `document.fonts.ready`. Base answer = MT-36 b) on `http://127.0.0.1:8000/test-sigmund0000000000/svar/` to `/svar/se-over/`, with bestemor «Nøtter» and «Ja» + confirmation on step 5.
  - **MT-45 (dobbel sending):** on `/svar/se-over/` read `innsending` and `sum`; send two identical POSTs at once with `page.request.post` (`Promise.all`, form data incl. `csrfmiddlewaretoken`, `action=send`). Then click «Send svaret» in the page (same `innsending`, draft cookie already deleted by the requests). Expected: both requests end on `/svar/sendt/`; the page click is a repeat and also lands on `/svar/sendt/`; `shell -c` shows one `HouseholdAnswer`, `revision` 1, one `Submission` (kind `answer`), one `Consent` for bestemor.
  - **MT-46 (endret i en annen fane og på en annen enhet):** a) Tab A on `/svar/se-over/`; tab B (same context) opens `/svar/maltider/?fra=se-over`, ticks «Frokost søndag» for bestemor, «Fortsett»; A clicks «Send svaret» → `/svar/se-over/?sending=sum`, focused notice «Feil: Svaret ble ikke sendt, fordi summen har endret seg …», the higher total shown; `shell` shows no `HouseholdAnswer`; «Send svaret» again → `/svar/sendt/`. b) After `seed_testdata`: two browser contexts X and Y both to `/svar/se-over/`; X sends; Y sends → `?sending=endret`, notice names «Sigmund» and today's date with «kl.»; the allergy block shows the FR-28 warning for bestemor (consent cleared); `shell`: `revision` 1, one `Submission`; Y sends again → `/svar/sendt/`, `revision` 2, bestemor has no `Allergy` row. c) `page.goBack()` from `/svar/sendt/` → no resubmit prompt, no new rows.
  - **MT-47 (feil ved sending):** on `/svar/se-over/`, `page.route` aborts the POST to `/svar/se-over/` (`route.abort()`); click «Send svaret». Expected: button text «Send svaret» without `aria-disabled`, the notice «Feil: Svaret ble ikke sendt, fordi forbindelsen ble brutt. Ingenting er tapt …Prøv igjen …» visible and `document.activeElement` inside it, the phone sentence with «Rikke» and «Valdemar»; `shell`: no `HouseholdAnswer`. `page.unroute`, click again → `/svar/sendt/`. Also open `/svar/se-over/?sending=feilet` on a fresh draft: the server notice with the same phones, focused.
  - **MT-48 (bare tastatur):** MT-46 a) with `page.keyboard` only: after the refusal focus is on the notice; Tab reaches «Send svaret»; Enter → `/svar/sendt/`; focused elements have `outline-style` `solid`.
  - **MT-49 (oppsett):** `/svar/se-over/?sending=feilet` and `?sending=endret` (after MT-46 b), and the client notice after an aborted send, at 360 × 640 and 180 × 320, then with 20px default text (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`) at both: `scrollWidth` ≤ `innerWidth`; the notice wraps inside the sheet; «Send svaret» ≥ 44px tall.
- [ ] `README.md` — status sentence (story 2.6c: a double tap or a second tab never sends twice, an answer changed meanwhile or a changed total is refused with a notice, a failed save keeps everything and says «Prøv igjen» with the phones); «Svarskjemaet» paragraph; services line (`exceptions.py` refusals).
- [ ] ARCHITECTURE-SPINE.md — dated notes (2026-11-24, Story 2.6c): AD-7 the snapshot is the check page form's hidden `sum`, not a draft field (reason in Design Notes); AD-8 format 6 `cv`, and the hidden `innsending`/`sum` are not answers; AD-9 the conflict notice says who and when, «what differs» moves to Story 4.1; AD-18 consent cleared on a revision conflict or consent-text change, version seen checked at send; AD-20 `Submission` fields, the hidden field name, order of checks, `DatabaseError` → `?sending=feilet`.
- [ ] `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md:237` — dated note with the five notice texts (wording decided by Claude in the goal run).
- [ ] `.docs/implementation-artifacts/deferred-work.md` — status lines «done in Story 2.6c» on: 2.4 «no consent Ja across a revision change» (`:220`), 2.4 seen version (`:229`), 2.5 total snapshot (`:236` remainder), 2.6a snapshot (`:241`) and busy reset (`:245`), 2.6b concurrent send (`:251`), each naming the file; add «From Story 2.6c» with the AD-9 «what differs» entry for Story 4.1.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass and `uv run manage.py makemigrations --check --dry-run` reports no changes.
- Given migration `0007`, when applied, then `Submission` exists with a unique submission id, a kind and the id of what was written (AD-20).
- Given the check page submitted twice with the same form, when the second POST arrives, then the guest lands on «Svaret er sendt» and the database holds one answer, one `Submission`, and the revision rose once.
- Given a draft started at an older revision, when sent, then nothing is written and the check page shows a notice that the answer changed, who sent it and when; the next send is handled as a new send.
- Given a total that changed after the check page was shown (price or another tab), when sent, then nothing is written and the check page shows the new total with a notice.
- Given a failing database write or a broken connection, when the guest sees the result, then the notice says what happened, that nothing is lost, «Prøv igjen» and the couple's phones, the draft is intact and «Send svaret» works again.

## Spec Change Log

## Review Triage Log

## Design Notes

- **Why the total snapshot is a hidden field and not in the draft:** AD-7 says «the draft stores the total shown on the check page», but the draft may only be written on «Fortsett» or «Velg» (AD-8), so it cannot record what a GET showed; and tabs share the draft cookie, so a draft field would hold tab B's total while tab A showed the old one. Only the page knows what it showed. The total is not an answer, so AD-8's «no hidden fields hold answers» still holds. The submission id is a hidden field for the same reason (one id per rendered page; AD-20 «every write form carries a one-time submission id»).
- **Why refusals redirect (303) instead of rendering:** the send POST then never becomes a page Back would resubmit (same reason as AD-7's `?feil=1`), and the script can follow every outcome with `location.assign`.
- **Why `fetch`:** a native form navigation that is aborted fires no event, so the button could only be reset by a timer. `fetch` gives a clear failure to show the notice; every other outcome is still the server's page.
- **Concurrent first sends:** `transaction_mode: IMMEDIATE` (`config/settings.py:118`) serialises the two transactions; the second then fails the revision check, and the unique `Submission.key` backs up a same-key race (an `IntegrityError` becomes `?sending=feilet`, and «Prøv igjen» returns the receipt).

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes.
