---
title: 'Story 2.7: The receipt and how to pay'
type: 'feature'
created: '2026-11-26'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md'
  - '{project-root}/.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/key-receipt.html'
warnings: ['oversized']
deferred: []
---

<intent-contract>

## Intent

**Problem:** After «Send svaret» the guest lands on a bare «Svaret er sendt» page (2.6a): no thank-you in Rikke's words, no summary, no total and no way to see how to pay (FR-23, FR-34, FR-71).

**Approach:** Turn `/<code>/svar/sendt/` into the receipt (G6) built from the stored answer, and add a read-only payment page `/<code>/svar/betal/` (G7, «Slik betaler du») with amount, Vipps number, account number and the derived payment message as selectable text, plus progressive-enhancement «Kopier» buttons with an empty polite live region present at load.

## Boundaries & Constraints

**Always:**
- Receipt order (EXPERIENCE › Receipt panel, DESIGN › Receipt panel): success notice holding `h1` «Svaret er sendt» + the existing sent line (unchanged from 2.6a) → Rikke's message (`<p>`, body) → `h2` «Dette har dere svart» (du-form «Dette har du svart») with the summary lines → «Totalt for husstanden: …» (`rsvp/includes/total.html`) → when owed: «Betal nå» (primary link button to `betal/`) above «Betal senere» (secondary link button to `sendt/?betal=senere`) → closing line «Du kan nå trygt lukke invitasjonen.» → plain text link «Til invitasjonen» to `/<code>/`. Nothing owed: no payment buttons; closing line directly after the total.
- Rikke's texts, exact (EXPERIENCE › Voice and Tone): coming when ≥1 person in the household comes: «Tusen takk for at du tok deg tiden til å svare, vi gleder oss til å feire den store dagen med deg!» / «… med dere!»; not coming: «Så leit at du ikke har mulighet til å delta, men dette har vi full forståelse for.» / «Så leit at dere ikke har …». du/dere by `speaks_to_one(household size)` (UX-DR51); the words live in the template, as for the hero.
- Summary lines are the check page's lines (`wedding/rsvp/summary.py` `_LINES`), built from the **stored** answer, with no «Endre» links (changing comes in Epic 4) and no per-line prices.
- Money (AD-12): total = `household_total(stored answer, form_prices(settings))`, so it equals the check page; amount owed = new rule `guest_balance(total, report)` with `report=None` (no «Jeg har betalt» until Story 5.1). «Owed» means `guest_balance(...) > 0`. Guest views/templates never read payment rows. Amounts via the `kroner` filter («4 720 kr»); meal price 0 shows as free like elsewhere.
- Payment message = new rule `payment_message(names)` → `"Bryllup " + household_names(names)` («Bryllup Sigmund og bestemor»), FR-71 derived rule; never stored (AD-4). Vipps and account number read from `site_settings()`; never hard-coded.
- Payment page: same paper sheet, no nav bar, footer band; `h1` «Slik betaler du»; a `<dl>` with rows «Beløp», «Vipps-nummer», «Kontonummer», «Betalingsmelding», each value in its own element as plain selectable text; a row whose setting is blank is left out. Each row has a `button button--secondary` «Kopier» with `hidden` and accessible name «Kopier beløpet» / «Kopier Vipps-nummeret» / «Kopier kontonummeret» / «Kopier betalingsmeldingen», `data-copy` holding the value to copy (amount as digits only, e.g. `4720`; account number as digits only; others as shown), and next to it an empty `<span class="copy-status" role="status">` present in the HTML at load. Then the closing line and «Til invitasjonen».
- `static/js/rsvp-copy.js` (deferred, only on the payment page): unhides the buttons only when `navigator.clipboard?.writeText` exists and `window.isSecureContext`; on click writes `data-copy`, clears every other `.copy-status` and puts «Kopiert» into this row's; on rejection selects the row's value text (Range on the value element) and puts «Trykk og hold for å kopiere» into the status. Never inserts a new live-region element (deferred-work 1.4a item).
- «Betal senere» (`sendt/?betal=senere`): the receipt renders an info notice with `focus=True`, below the buttons and above the closing line: «Den samme lenken viser alltid hva dere har igjen å betale, og hvordan dere betaler.» (du-form «… hva du har igjen å betale, og hvordan du betaler.»). Any other `betal` value is ignored. Only shown when owed.
- Both views: `never_cache`, `require_safe`, one `resolve_code`; unknown code → G1 404 (`_unknown_link`); no `HouseholdAnswer` → 302 to `guests:rsvp`; not gated by the deadline (they only read). Payment page with nothing owed → 302 to `guests:rsvp_sent`.
- Every new rule, selector, view and test names its FR/AD/UX-DR ids in its docstring; UI text Norwegian, code English.

**Never:**
- No «Jeg har betalt» (5.1), payment rows or `PaymentReport`, no stored/adjusted payment message or duplicate warning (5.5), no QR code, no status block or front-page change (2.8), no answered-household redirect from `/svar/` (Epic 4), no autofocus on «Betal nå» (the mockup note puts focus there; a focused link at load would skip the success heading for screen readers — decided by Claude).
- No new model, migration, session, messages framework or cookie; no write.
- No re-implementing totals, the message or line texts in views/templates.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Owes, two people | seeded Sigmund household, GET `sendt/` | «… med dere!», «Dette har dere svart», «Totalt for husstanden: 4 720 kr», «Betal nå» before «Betal senere» in DOM, closing line after them | — |
| Nothing owed, one person | seeded Synne (total 0) | «… med deg!», «Dette har du svart», «0 kr», no `betal/` link, closing line after total | — |
| Nobody coming | household all «Kommer ikke» | «Så leit at …» message, total 0, no payment buttons | — |
| Pay later | `sendt/?betal=senere`, owed | focused info notice with the link sentence | `?betal=x` → no notice |
| Pay later, nothing owed | `?betal=senere`, total 0 | no notice | — |
| Payment page | Sigmund `betal/` | 4 720 kr, `00000`, `1234.56.78900`, «Bryllup Sigmund og bestemor»; 4 hidden «Kopier» buttons, 4 empty `role="status"` spans | — |
| Payment page, nothing owed | Synne `betal/` | 302 to `sendt/` | — |
| Blank setting | `vipps_number=""` | no «Vipps-nummer» row | — |
| Not answered | Mona `sendt/` or `betal/` | 302 to `/svar/` | — |
| Unknown code | `sendt/`, `betal/` | G1, 404 | — |
| Rules | `guest_balance(4720, None)`, `(4720, 1000)`, `(4720, 5000)`, `(0, None)`; `payment_message(["Synne"])`, `(["Sigmund","bestemor"])` | 4720, 3720, 0, 0; «Bryllup Synne», «Bryllup Sigmund og bestemor» | — |

</intent-contract>

## Code Map

- `guests/views.py:255-273` `rsvp_sent` — extend: build the stored answer, steps, parts, total, balance, `one` (du/dere), `pay_later`; `_guest_context`, `_unknown_link`, `site_settings`, `household_answer`, `household_members`, `form_prices` already imported/used in this file (`:220-235`). Add `rsvp_pay` next to it; module docstring `:1-23` lists the pages.
- `guests/urls.py:40` — add `path("<str:code>/svar/betal/", views.rsvp_pay, name="rsvp_pay")` before the `<slug>` route `:41` (no step slug is `betal`; `wedding/rsvp/steps.py:155` `KEY_BY_SLUG`).
- `wedding/rsvp/templates/rsvp/sent.html` — the whole receipt; keep the success notice block as is. New `wedding/rsvp/templates/rsvp/pay.html`.
- `wedding/rsvp/summary.py:146-184` `check_parts` — add `receipt_parts(answer, *, members, respondent, steps)` returning `{name, lines}` per applicable step via the same `_LINES` (share, do not copy). `respondent` only matters for the confirmation line, which needs `Answer.confirmed`; a stored answer has none (`confirmed` is not stored), so pass `HouseholdAnswer.sent_by_id or 0`.
- `wedding/rules/answer.py:36-58` `Answer` — the value to rebuild; `whole` = True when every coming member has all three days, else False, with `days` per coming member.
- `wedding/selectors.py:122-128` `household_answer` — add `sent_answer(household) -> Answer` next to it: one query each for `PersonAnswer`, `Allergy`, latest `Consent` per guest (`event` given → True, refused → False, withdrawn/none → no entry); `AllergyEntry` from the booleans (`wedding/rules/allergies.py:27-35`, `ALLERGY_KEYS`); hike blank → no entry. Models `wedding/models.py:150-245`.
- `wedding/rules/form_steps.py:24` `form_steps(attendance, days)` — the applicable steps for the stored answer, in household order.
- `wedding/rules/money.py:22` `household_total` — reuse; add `guest_balance(total: int, report: int | None) -> int` (FR-34, FR-36, AD-12: `max(total - (report or 0), 0)`; report is the reported amount, None until Story 5.1).
- `wedding/rules/households.py:31` `household_names`, `:42` `speaks_to_one` — add `payment_message(names: Sequence[str]) -> str` (FR-71, AD-2, AD-4).
- `wedding/rsvp/templates/rsvp/includes/total.html`, `wedding/templates/wedding/components/notice.html` (`variant="info" focus=True only`), `templatetags` `kroner` filter — reuse.
- `static/js/rsvp-send.js` — style reference for a small deferred script; `static/css/site.css` — receipt/payment styles (`.receipt-summary`, `.pay-list`, `.copy-status`); breakpoints in em; tokens only.
- Tests: `tests/test_rsvp_send.py` (sent-page tests from 2.6a; update the assertions that the page has only the heading, sent line and «Til invitasjonen»), `tests/conftest.py` `seeded` (unanswered Sigmund) / `seeded_with_answers`; `tests/test_rules_purity.py` covers the new rules automatically.
- Docs: `README.md:9` status («den fullstendige kvitteringen kommer i story 2.7»), `:77` Svarskjemaet, `:165` tree (pay.html, rsvp-copy.js); `docs/manual-test-plan.md` after MT-50 (`:74`); EXPERIENCE.md microcopy rows `:148`, `:151`, `:153` (mark decided, avgjort av Claude 2026-11-26) and add the «Betal senere» sentence and «Dette har du svart»; ARCHITECTURE-SPINE AD-2 (`:71`) dated note for `guest_balance`, `payment_message`; `.docs/implementation-artifacts/deferred-work.md:5-7` (Playwright proxy done; NVDA/VoiceOver stays open for Rikke); `.logs/rikke/issues.md:64`; `sprint-status.yaml:61`.

## Tasks & Acceptance

**Execution:**
- [ ] `wedding/rules/money.py`, `wedding/rules/households.py` -- add `guest_balance` and `payment_message` with docstrings -- AD-2, AD-12, FR-71.
- [ ] `wedding/selectors.py` -- add `sent_answer(household)` -- the receipt must show what was stored, not a draft (AD-4).
- [ ] `wedding/rsvp/summary.py` -- add `receipt_parts` sharing `_LINES`; update module docstring -- FR-23, UX-DR24.
- [ ] `guests/views.py`, `guests/urls.py` -- extend `rsvp_sent`, add `rsvp_pay` -- FR-23, FR-34, FR-71, AD-12, UX-DR24, UX-DR25.
- [ ] `wedding/rsvp/templates/rsvp/sent.html`, new `pay.html`, `static/js/rsvp-copy.js`, `static/css/site.css` -- receipt and payment page per Boundaries; update template comments -- UX-DR24, UX-DR25, UX-DR51.
- [ ] `tests/test_payment_rules.py` (new) -- matrix «Rules» row, plus `payment_message` for 4 names -- AD-12, FR-71.
- [ ] `tests/test_rsvp_receipt.py` (new) -- every other matrix row with `seeded_with_answers` and hand-built answers; `sent_answer` round-trip (send via `send_answer`, read back, `household_total` equals the check page's total for the same draft); DOM order of «Betal nå» < «Betal senere» < closing line; buttons `hidden`; `role="status"` spans empty; template never names payment rows; `tests/test_rsvp_send.py` -- adjust 2.6a sent-page assertions.
- [ ] `docs/manual-test-plan.md` -- add MT-51 to MT-54 (Norwegian, result cells empty), see Verification.
- [ ] `README.md`, EXPERIENCE.md, ARCHITECTURE-SPINE.md, `deferred-work.md`, `.logs/rikke/issues.md`, `sprint-status.yaml` -- sync as in Code Map, dated 2026-11-26.

**Acceptance Criteria:**
- Given a successful send by Mona for Mona and Geir (both coming, cabin), when the browser lands on `/svar/sendt/`, then it shows «Svaret er sendt», «Sendt av Mona …», «… med dere!», «Dette har dere svart», «Totalt for husstanden: 3 000 kr», «Betal nå» above «Betal senere» and «Du kan nå trygt lukke invitasjonen.» directly below them.
- Given the receipt, when «Betal nå» is followed, then `/svar/betal/` shows 3 000 kr, `00000`, `1234.56.78900` and «Bryllup Mona og Geir» as selectable text.
- Given the payment page in a secure context with clipboard, when «Kopier» by «Kontonummer» is clicked, then the clipboard holds `12345678900` and that row's status span reads «Kopiert» while the others are empty.
- Given clipboard write fails, when «Kopier» is clicked, then the value is selected and the status reads «Trykk og hold for å kopiere».
- Given JavaScript is off, when the payment page loads, then no «Kopier» button is visible and all values are readable.

## Design Notes

- **Why a separate payment page rather than in-page reveal:** works with no JavaScript, gives Story 2.8's status block a link target («Slik betaler du», same details), and matches the mockup's second phone. «Betal senere» is a link with a query so it also needs no script.
- **Promise of «Betal senere» before 2.8:** until 2.8 the front page does not yet show the status block, so the link's promise is kept by `/svar/sendt/` and `/svar/betal/` (both reachable on the link) and fully by 2.8 next in this epic; recorded, not a gap.
- **Live region:** each row's `role="status"` span exists empty in the server HTML; the script only sets `textContent`. This closes the code side of the 1.4a deferred item; the screen-reader check is Rikke's.
- **Copy values:** digits only for amount and account number, since banking and Vipps fields reject «kr», spaces and dots.

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.
- `uv run manage.py makemigrations --check --dry-run` -- expected: no changes.

**Manual checks (run afterwards by the orchestrator with Playwright against Edge, after `uv run manage.py migrate`, `uv run manage.py seed_testdata`, `uv run manage.py runserver`; rows written by the implementer with empty result cells):**
- MT-51 Ekte sending til kvittering: MT-50's steps on `http://127.0.0.1:8000/test-mona0000000000000/svar/`; expect the first AC; then «Betal nå» → `/svar/betal/` with the second AC's values; `shell` total matches 3 000. Also `test-sigmund0000000000/svar/sendt/` shows 4 720 kr (expected.toml `households.sigmund`), `test-synne000000000000/svar/sendt/` shows 0 kr and no «Betal nå».
- MT-52 Kopier: grant `clipboard-read`/`clipboard-write`; the third AC; live-region proxy: before click every `.copy-status` is empty and has `role="status"`; after, only the clicked one has text. Then `page.route`-free failure: override `navigator.clipboard.writeText` to reject → fourth AC. With `javaScriptEnabled: false` → fifth AC.
- MT-53 Bare tastatur: from `sendt/`, Tab reaches «Betal nå», Enter opens `betal/`; Tab reaches each «Kopier», Enter gives «Kopiert»; `sendt/?betal=senere` opens with focus on the notice; focused elements have `outline-style` `solid`.
- MT-54 Oppsett: `sendt/`, `sendt/?betal=senere` and `betal/` for Sigmund at 360 × 640 and 180 × 320, with and without 20px default text size (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`): `scrollWidth` ≤ `innerWidth`, the payment message and account number wrap inside the sheet, buttons ≥ 44px high.
