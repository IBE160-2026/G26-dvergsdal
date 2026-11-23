---
title: 'Story 2.5: The Friday hike and the check page'
type: 'feature'
created: '2026-11-23'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-4-allergies-and-consent.md'
warnings:
  - oversized
deferred: []
---

<intent-contract>

## Intent

**Problem:** Step 6 «Fjelltur fredag» (`/<code>/svar/fjelltur/`) and the check page (`/<code>/svar/se-over/`) are empty frames. Guests cannot answer the hike, cannot see what they answered before sending, cannot jump back to change one part, and the check page does not give the FR-28 warning (FR-17, FR-21, FR-28, UX-DR23; deferred-work «Story 2.5: the check page shows the FR-28 warning with `not_saved`»).

**Approach:** Build step 6 on the step-3 pattern (one Ja/Nei/Kanskje radio group per person present on Friday, required, PRG errors computed from the draft) with draft format 5. Fill the check page from a new summary module that turns the draft into one block per applicable part, with «Endre» links carrying `?fra=se-over` so «Fortsett» returns to the check page (or to the first step that the change reopened). «Send svaret» is shown but sending is Story 2.6a: its POST writes nothing.

## Boundaries & Constraints

**Always:**
- **Data (AD-8):** draft key `hike` `{id: "yes" | "no" | "maybe"}`; `VERSION = 5` (format 4 is broken and deleted). Rule constant `HIKE_ANSWERS = ("yes", "no", "maybe")` in `wedding/rules/days.py`. `Answer.hike: Mapping[int, str]` (default empty); `normalise_answer` keeps a hike answer only for a member in `present_days` whose set contains `"fri"` and whose value is in `HIKE_ANSWERS` (FR-17, FR-75). `household_total` ignores it.
- **Hike step (FR-17, DESIGN.md › Form step, Choice control):** registry `Step("hike", "fjelltur", "Fjelltur fredag", "Hvem blir med på fjellturen fredag?", "rsvp/includes/hike_fields.html")`. Lead `form-note`: «Fjellturen er fredag, for dem som kommer tidlig. Svar «Kanskje» hvis dere ikke har bestemt dere ennå.» One fieldset per coming member present on Friday (legend = name), radios «Ja» / «Nei» / «Kanskje», nothing checked until chosen; nobody else is asked. No total, no price. It is skipped and not counted when nobody is present Friday (`form_steps` already does this).
- **Hike done:** «Fortsett» marks `hike` done; `_settled` removes it from `done` while any Friday-present member has no hike answer (as for overnight). Error (PRG `?feil=1`, step-3 markup): line «Velg «Ja», «Nei» eller «Kanskje» for <name>.», summary link «Svar om fjellturen for <name>» to that group's first radio. «Velg» keeps posted answers unvalidated.
- **Return to the check page (UX-DR23, AD-7):** constant `FROM_QUERY = "fra"`; only the value `CHECK_SLUG` counts. When the step's request has `?fra=se-over`, a valid «Fortsett» on any step (1–6) redirects to `mount.url(first_unfinished(steps, done, None))` (None → check page) instead of `next_step`; its error redirect is `?feil=1&fra=se-over`; step 2's «Nei» reveal keeps `fra` before `#velg-dager`; «Velg» redirects keep `fra`; «Tilbake» on that step links to the check page. The step forms have no `action`, so the POST keeps the query. Without `fra` nothing changes.
- **Check page (FR-21, DESIGN.md › Check-answers list, mockup `key-check-page.html`), new template `rsvp/check.html` (delete `check_frame.html`):** same paper sheet, no nav bar, footer band. Order: warning notice `text="Svaret er ikke sendt ennå."` (renders «Obs: …», not focused, not live); `h1` «Se over svaret før du sender»; a `ul` of blocks, one per applicable step in step order, each with `h2` = step name and the link «Endre<span class="visually-hidden"> {name lowercased}</span>» to `mount.url(key)?fra=se-over` on one line, then one `p` per line; `divider` between blocks; then `rsvp/includes/total.html` with `_total` (no script, no status region); then a `form method="post"` with CSRF and the primary button «Send svaret» (`name="action" value="send"`) above the secondary link «Tilbake» (to the last applicable step). Page title «Se over svaret før du sender – Invitasjon». No respondent line.
- **Block lines (texts avgjort av Claude 2026-11-23, from the mockup):** names joined «a, b og c»; «Ikke oppgitt» lines in `ink-muted` (class `check-list__missing`).
  - Hvem kommer: every member «<name>: kommer» / «<name>: kommer ikke».
  - Dager: each coming member «<name>: hele helgen» (whole, or no «Nei») or the chosen days «<name>: lørdag 27. mai og søndag 28. mai» (`DAYS` labels, weekday lowercased).
  - Overnatting: each member who could stay (`can_stay_overnight`) «<name>: hytte hele helgen» / «<name>: overnatter ikke».
  - Måltider: each member offered a meal «<name>: middag fredag og frokost søndag» (`MEALS` names lowercased, `offered_meals` order) / «<name>: ingen måltider».
  - Allergier og matbehov: each coming member «<name>: ingen allergier eller matbehov», or the categories lowercased («<name>: laktose og nøtter»), or «<name>: Ikke oppgitt» (muted) without info; for a member with categories, «Merknad om <name>: <note>» (`linebreaksbr`) or «Merknad om <name>: Ikke oppgitt» (muted); for a member with info, «Samtykke for <name>: ja» / «… nei» / «… Ikke oppgitt» (muted), plus «Du har bekreftet at <name> vet om det og er enig.» when confirmed and not the respondent. When `not_saved` (from `wedding/rules/allergies.py`) names anyone, a warning notice inside the block with `AllergiesForm.warning_text(names)` (FR-28).
  - Fjelltur fredag: each Friday-present member «<name>: ja» / «nei» / «kanskje».
- **Check page POST (Story 2.6a builds sending):** «Velg» is not on the page; any POST redirects (303) to the check page and writes nothing. A CSRF failure on the check page keeps the generic 403 page (`render_after_csrf_failure` returns None for `CHECK`).
- Privacy and quality: no allergy content in logs; `Cache-Control: private, no-store` like the steps; no DB row, session or message; no hidden fields; every new rule/view/test names its FR/AD/UX-DR; CSS breakpoints only in em.

**Never:**
- No `send_answer`, model, migration or `Submission` (Stories 2.6a–2.6c); no «Sender …» busy script.
- No per-line prices on the check page: `wedding/rules/money.py` says no view or template adds prices itself; only `household_total` (deviation from the mockup, recorded in DESIGN.md).
- No change to who the steps reopen (`REOPENED_ON_CHANGE`), to the px breakpoints in `site.css`, or to steps 1–5's texts.
- No sprint-status action items (none belong to 2.5).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Sigmund's journey | both whole weekend; Sigmund «Kanskje», bestemor «Nei», «Fortsett» | `hike` done, redirect `/svar/se-over/` | none |
| Missing answer | bestemor unanswered | `?feil=1`, Sigmund's choice kept, error + summary, title «Feil: …» | not done |
| Only some Friday | Arild's household: Filippa only Saturday | Filippa has no hike group and no Fjelltur line | none |
| Nobody Friday | everyone Saturday–Sunday | hike step skipped, «Steg n av m» without it, `/svar/fjelltur/` redirects to the check page; no Fjelltur block | none |
| Friday removed | after a hike answer, the person's days change to Sat–Sun | hike answer dropped (FR-75) | none |
| Forged value | `hike_<id>=perhaps`, or a non-Friday member's field | ignored | none |
| Endre, no change | check page → «Endre måltider» (`?fra=se-over`) → «Fortsett» | back on `/svar/se-over/` | none |
| Endre adds a day | «Endre dager» → Filippa all days → «Fortsett» | lands on `/svar/overnatting/` (via the check page's gate), then the steps in order, then the check page | none |
| Endre, error | «Endre hvem som kommer» with fra, invalid post | `/svar/?feil=1&fra=se-over`; fixing it and «Fortsett» returns to the check page | — |
| Endre, Tilbake | step opened with fra | «Tilbake» links to `/svar/se-over/` | none |
| Unconsented allergies | bestemor Laktose, consent unanswered | check page Allergier block shows the FR-28 warning naming bestemor | none |
| Send svaret | POST to the check page | 303 to `/svar/se-over/`, no draft change, no DB row | — |
| CSRF on hike | POST without token | 403, posted radios kept, focused notice; no draft write | — |
| Old draft | format 4 cookie | deleted, form starts at step 1 | — |

</intent-contract>

## Code Map

- `wedding/rules/days.py` — add `HIKE_ANSWERS` (FR-17). `wedding/rules/answer.py:30-55` `Answer` add `hike`; `:98-128` `normalise_answer` filters it (Friday-present, valid value). Module docstrings. `tests/test_rules_purity.py` covers rules.
- `wedding/rules/form_steps.py` — read-only: `form_steps` already drops `hike` when nobody is present Friday; `first_unfinished(steps, done, None)` is the return-to-check target.
- `wedding/rules/allergies.py` — read-only: `not_saved`, `has_allergy_info`, `EMPTY`.
- `wedding/rsvp/steps.py:79` hike `Step` → question and `fields_template`; docstring `:1-26` (step 6 no longer a frame). Add `HIKE` labels `{"yes": "Ja", "no": "Nei", "maybe": "Kanskje"}`. `CHECK_SLUG` `:139`.
- `wedding/rsvp/draft.py:45` `VERSION = 5`; `Draft` `:48-80` add `hike: dict[int, str]`; `payload` `:87-107` `"hike"`; `PAYLOAD_KEYS` `:110`; validator next to `_bools` `:189` (member ids, value in `HIKE_ANSWERS`); `_parse` `:234`. Docstring lists format 4 as broken.
- `wedding/rsvp/forms.py` — `hike_field(id)` (pattern `:58` `overnight_field`), `HikeForm` (pattern `OvernightForm` `:204-266`): `LEAD`, `CHOICES`, `error_text`, `summary_text`, `posted_hike()`.
- `wedding/rsvp/summary.py` (new) — `check_parts(...)` → list of `{key, name, url, hidden, lines: [{text, missing}], warning}` built from the draft's `Answer`, `present_days`, `can_stay_overnight`, `offered_meals`, `not_saved`, the `DAYS`/`MEALS`/`ALLERGIES`/`HIKE` labels; one shared `join_words` (reuse it in `AllergiesForm.warning_text` instead of its inline join, `forms.py:375`).
- `wedding/rsvp/views.py`:
  - `:85` `CHECK_TEMPLATE = "rsvp/check.html"`; add `FROM_QUERY`; docstring `:1-31`.
  - `:138-149` `_answer` passes `draft.hike`; `:183-209` `_settled` copies `hike` back and removes `hike` from `done` while a Friday-present coming member has no answer.
  - Add `_hike_fields` (pattern `_overnight_fields` `:302-347`) and `_hike_step` (pattern `_paid_step` `:710-766` without total); `_with_posted` `:663-707` gets a `hike` branch.
  - Add `_from_check(request) -> bool` and `_continue_url(request, mount, steps, draft, step)`; use it for every valid «Fortsett» redirect in `_who_is_coming` `:582-583`, `_which_days` `:660`, `_paid_step` `:766`, `_allergies_step` `:815`, `_hike_step`; keep `fra` on error/«Velg»/`#velg-dager` redirects (`:571,575,646,648,650,659,763,765,812,814`). `_render_step` `:462-510`: `back_url` = check page when `_from_check(request)`.
  - `:513-518` `_render_check` → builds `check_parts`, `_total`, back URL, renders `rsvp/check.html`; `_later_step` `:818-890` takes `prices` already; dispatch `hike` to `_hike_step`; the CHECK POST stays «redirect, no write».
  - `:930-1019` `render_after_csrf_failure` gets the hike branch.
- `wedding/rsvp/templates/rsvp/step.html:3-32` comment (no frame left; drop the «hike is a frame» sentence). New `rsvp/includes/hike_fields.html` (copy `overnight_fields.html` markup). New `rsvp/check.html`; delete `rsvp/check_frame.html`.
- `static/css/site.css` — append a Story 2.5 block: `.check-list` (no bullets, `divider` between items), `.check-list__head` (h2 + «Endre» on one line, wrapping with `flex-wrap`), `.check-list__missing` (`ink-muted`); em breakpoints only.
- Tests to update: frame tests on `fjelltur`/`se-over` in `tests/test_rsvp_who_is_coming.py`, `tests/test_rsvp_days.py`, `tests/test_rsvp_allergies.py` (all now reach a real hike step or check page); `tests/test_rsvp_draft.py` v5, `BROKEN` cases and the 8-person size test with `hike` filled; `tests/test_form_steps.py` read-only.
- Seed (read-only): Sigmund + bestemor (`test-sigmund0000000000`); Arild, Marie, Filippa, Leone (`test-arild000000000000`), `wedding/fixtures/seed.toml`.
- Docs: `docs/manual-test-plan.md:53-55` (MT-33–35 pattern); `README.md:9` status, `:77+` «Svarskjemaet», tree; ARCHITECTURE-SPINE AD-8 (format 5); EXPERIENCE.md microcopy rows `:140,143,144` and Check-answers list `:213`; DESIGN.md Check-answers list `:693`; `.docs/implementation-artifacts/deferred-work.md:213-215`.

## Tasks & Acceptance

**Execution:**
- [ ] `wedding/rules/days.py`, `wedding/rules/answer.py`: `HIKE_ANSWERS`, `Answer.hike`, `normalise_answer` filter (FR-17, FR-75, AD-2).
- [ ] `wedding/rsvp/steps.py`: hike question, fields template, `HIKE` labels, docstring.
- [ ] `wedding/rsvp/draft.py`: format 5 with `hike` and its validator.
- [ ] `wedding/rsvp/forms.py`: `hike_field`, `HikeForm` with the texts above; `warning_text` uses `join_words`.
- [ ] `wedding/rsvp/summary.py`: `join_words`, `check_parts` with every line rule above (FR-21, FR-28, UX-DR23).
- [ ] `wedding/rsvp/views.py`: hike step, `_settled`/`_answer`/`_with_posted`/CSRF branches, `fra` handling and `_continue_url`, `_render_check`, docstrings.
- [ ] `wedding/rsvp/templates/rsvp/includes/hike_fields.html`, `rsvp/check.html`, `rsvp/step.html` comment; delete `rsvp/check_frame.html`.
- [ ] `static/css/site.css`: Story 2.5 block.
- [ ] `tests/test_hike_rules.py` (or extend `tests/test_answer_rules.py` if it exists): normalise keeps/drops hike per Friday presence and value.
- [ ] `tests/test_rsvp_hike_check.py`: every matrix row through the test client; the epics ACs: hike only for Friday-present people; skipped and not counted when nobody Friday; check page order (notice text, `h1`, the six `h2` in order for Sigmund, total equal to `household_total`); «Ikke oppgitt» for a skipped note; FR-28 warning; each «Endre» href and hidden text («Endre måltider»); «Fortsett» from each step with `fra` returns to the check page; adding a day via «Endre dager» ends at `/svar/overnatting/` with `follow=True`; «Send svaret» is the first button and comes before «Tilbake»; POST writes nothing; no DB rows, session or messages through steps 1–6 and the check page; Cache-Control private, no-store.
- [ ] Update `tests/test_rsvp_who_is_coming.py`, `tests/test_rsvp_days.py`, `tests/test_rsvp_allergies.py`, `tests/test_rsvp_overnight_meals.py`, `tests/test_rsvp_draft.py` for the hike step, the check page and format 5.
- [ ] `docs/manual-test-plan.md`: Norwegian rows, date and result cells empty, each «Kjøres av Claude med Playwright mot Edge» (`channel: 'msedge'`); before each `uv run manage.py seed_testdata`, then `uv run manage.py runserver`; measure after `document.fonts.ready`.
  - **MT-1 (2.5):** README «Svarskjemaet» to the check page.
  - **MT-36 (real submission):** `http://127.0.0.1:8000/test-sigmund0000000000/svar/`: both «Kommer», «Fortsett», «Ja», «Fortsett», «Ja» for both, «Fortsett», «Fortsett», Laktose for bestemor (no consent), «Fortsett». Expect `/svar/fjelltur/`, title «Steg 6 av 6: Fjelltur fredag – Invitasjon», no radio checked. a) Only Sigmund «Kanskje», «Fortsett» → `?feil=1`, title starts «Feil: », focused summary link «Svar om fjellturen for bestemor», Sigmund's choice kept. b) bestemor «Nei», «Fortsett» → `/svar/se-over/`: «Obs: Svaret er ikke sendt ennå.» above `h1` «Se over svaret før du sender», `h2`s Hvem kommer, Dager, Overnatting, Måltider, Allergier og matbehov, Fjelltur fredag; «Merknad om bestemor: Ikke oppgitt»; the FR-28 warning naming bestemor; «Totalt for husstanden: 3 000 kr»; «Send svaret» above «Tilbake». c) «Endre måltider» → `/svar/maltider/?fra=se-over` with no box ticked; tick «Frokost søndag» for bestemor, «Fortsett» → `/svar/se-over/` with the new line and a higher total. d) «Endre hvem som kommer», «Tilbake» → `/svar/se-over/`. e) `page.goBack()` twice → no `dialog` event. f) On Arild's link: Arild, Marie, Filippa «Kommer», Leone not; «Nei»; Arild and Marie all days, Filippa Saturday only; through to the hike step → groups for Arild and Marie only; on the check page «Endre dager», Filippa all days, «Fortsett» → `/svar/overnatting/`, then «Fortsett» through to `/svar/se-over/` with a Fjelltur line for Filippa only after answering her on the hike step.
  - **MT-37 (keyboard only):** Sigmund's link with `page.keyboard` through steps 1–6 to the check page. On step 6 the Tab order is «Bytt», Sigmund's radio group, bestemor's, «Fortsett», «Tilbake», `tel:` links; arrows choose; Enter goes to `/svar/se-over/`. On the check page the order is the six «Endre» links, «Send svaret», «Tilbake», `tel:` links; every focused element has `outline-style` `solid`; Enter on «Endre fjelltur fredag» opens `/svar/fjelltur/?fra=se-over`, Enter in a radio returns to `/svar/se-over/`.
  - **MT-38 (layout):** Arild's step 6 in the error state and his check page (with an FR-28 warning). Run at 360 × 640 and 180 × 320, then with 20px default text (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`) at 360 × 640 and 180 × 320: `scrollWidth` ≤ `innerWidth`; every `.choice` ≥ 44px tall and inside the sheet; each «Endre» link inside the sheet and ≥ 44px tall (or 24px with spacing per WCAG 2.5.8); block headings and lines wrap without overflow; «Send svaret» above «Tilbake», 12px apart, same width.
- [ ] `README.md`: status line (story 2.5: hike step, check page; sending is story 2.6a), «Svarskjemaet» (step 6, check page, «Endre» returns there, «Send svaret» does not send yet), tree (`wedding/rsvp/summary.py`).
- [ ] ARCHITECTURE-SPINE, EXPERIENCE.md, DESIGN.md: dated notes (2026-11-23, Story 2.5): AD-8 format 5 (`hike`) and the measured size; AD-7 the `?fra=se-over` return rule; EXPERIENCE microcopy rows for step 6 (question, lead, choices, error) and the check page lines «avgjort av Claude 2026-11-23» with reasons (FR-17, FR-21, mockup proposals kept; per-person day lines instead of the mockup's «Begge» so mixed days read the same way); «Ikke oppgitt / Endre», «Obs: Svaret er ikke sendt ennå.» and the heading marked decided; Check-answers list: no per-line prices (AD-12: only `household_total`), blocks only for applicable steps, «Tilbake» from an «Endre» step returns to the check page.
- [ ] `.docs/implementation-artifacts/deferred-work.md`: mark the 2.4 entry «Story 2.5: the check page shows the FR-28 warning …» `status: done in Story 2.5 (wedding/rsvp/summary.py)`; add «From Story 2.5»: Story 2.6a gives «Send svaret» its POST handler (the check page's POST only redirects today), the «Sender …» busy state and a friendly CSRF result on the check page.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given Sigmund and bestemor coming all weekend, when step 6 renders, then each has an unanswered Ja/Nei/Kanskje group, and the progress line reads «Steg 6 av 6: Fjelltur fredag».
- Given a household where nobody comes Friday, when the respondent finishes step 5, then they land on the check page and no progress line counted the hike.
- Given every step done, when the check page opens, then the notice «Obs: Svaret er ikke sendt ennå.» comes before the `h1` «Se over svaret før du sender», the blocks follow step order with each person's answer, the total equals `household_total`, skipped optional answers say «Ikke oppgitt», and unconsented allergies show the FR-28 warning.
- Given an «Endre» link, when used and «Fortsett» pressed, then the step opens with its answers filled in and the guest returns to the check page, unless the change added a person or a day, in which case the next step with new questions comes first.
- Given the check page, when it renders, then «Send svaret» is the primary button above «Tilbake», and posting it writes nothing.
- Given `docs/manual-test-plan.md`, when read, then MT-1 (2.5) and MT-36 to MT-38 hold the steps above with empty date and result cells.

## Spec Change Log

## Review Triage Log

## Design Notes

- **Why `?fra=se-over` and not «all done → check page»:** a guest walking back with «Tilbake» and pressing «Fortsett» expects the next step, not a jump to the end; only an «Endre» link signals «I came from the check page». The query is navigation, not an answer, so AD-8's «no hidden fields» holds; the step form has no `action`, so the POST keeps it.
- **Why the extra hop when a change reopens steps:** `handle_step` clears `REOPENED_ON_CHANGE` after the step handler returns, so `_continue_url` may still point at the check page; the check page's own gate (`first_unfinished`) then sends the guest to the first reopened step. That is one 302 more, and the gate is already tested; recomputing in `handle_step` would duplicate the gate.
- **Why the hike is required:** like overnight, the couple counts «kommer» and «kanskje» (FR-54), and «Kanskje» already covers the undecided, so an unanswered group would only be a forgotten one.
- **Why blocks only for applicable steps:** a block for a step the guest never saw would have no answers and an «Endre» to an address that redirects away.

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.
