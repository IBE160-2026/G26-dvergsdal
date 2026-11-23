---
title: 'Story 2.4: Allergies and consent'
type: 'feature'
created: '2026-11-23'
status: 'done'
baseline_revision: '301d1ebf0c97725af336062f416c3775db82329d'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-3-overnight-stay-meals-and-the-running-total.md'
warnings:
  - oversized
deferred:
- summary: >-
    Story 7.1: the privacy page says that the answer in progress, including allergies a guest typed but did not consent to, lives only in the guest's own browser cookie until it is sent or expires (90 days).
  evidence: >-
    low. Blind review; AD-8 keeps everything entered in the draft and nothing is stored on the server.
- summary: >-
    Story 2.6b/2.6c: record which consent-text version the guest saw, so a version change between step 5 and sending is caught together with the revision check.
  evidence: >-
    low. Blind review; the draft holds no consent-text version today.
---

<intent-contract>

## Intent

**Problem:** Step 5 «Allergier og matbehov» (`/<code>/svar/allergier/`) is an empty frame. Guests cannot give dietary needs per person, say «Ingen allergier eller matbehov», or give or refuse consent per person, and nothing tells them that unconsented allergy data will not be saved (FR-25, FR-26, FR-27, FR-28, NFR-3, AD-8, AD-18, UX-DR21).

**Approach:** Build step 5 on the 2.3 machinery: draft format 4, PRG errors computed from the draft, «Velg», the CSRF branch, the fields include from the registry. Put the allergy rules in a new pure module `wedding/rules/allergies.py`, and extend `Answer`/`normalise_answer` so non-comers lose their allergy data (FR-75). Add a tiny no-build script that makes «Ingen allergier eller matbehov» exclusive. Nothing is written to the database: storage with consent is Story 2.6b.

## Boundaries & Constraints

**Always:**
- **Data (AD-8: the draft holds everything entered, allergies included):** per coming person `cats` (ordered subset of `ALLERGY_KEYS` = `gluten, lactose, nuts, shellfish, vegetarian, vegan, other`), `none` (bool), `note` (str, stripped, `\r\n` → `\n`, at most `NOTE_MAX = 200` characters by `len`), `consent` (True «Ja» / False «Nei» / absent = unanswered, never preset), `confirmed` (the respondent ticked «Jeg bekrefter at <name> vet om dette og er enig»).
- **Rules (AD-2, pure, plain values, docstrings name FR/AD):** in `wedding/rules/allergies.py`: `ALLERGY_KEYS`, `NOTE_MAX`, `has_allergy_info(entry)` (true for `none`, any category or a non-empty note: FR-26 counts «Ingen …» as allergy information), `allergy_problems(entry, consent, confirmed, is_respondent) -> tuple[str, ...]` with the codes `CONFLICT` (`none` together with a category or a note), `CONFIRM` (consent True, not the respondent, info entered, not confirmed), and `not_saved(...)` → the coming people whose info is entered while consent is not True (FR-28; Story 2.5's check page reuses it). The over-long note is refused before it reaches the draft (see matrix).
- **Step done:** «Fortsett» with no problem for anyone marks `allergies` done; `_settled` removes `allergies` from `done` while any coming person has a problem (as for overnight), so «Bytt» to another respondent that makes a confirmation missing reopens the step.
- **Page (DESIGN.md › Form step, Choice control, Text field, Consent block; EXPERIENCE.md › Choice control, Consent block; epics AC wins over the older mockup's single household consent):** the registry keeps question and name «Allergier og matbehov» (as the mockup). Under the respondent line: lead «Dette er valgfritt.», then the consent text section (one include, `rsvp/includes/consent_text.html`, id `samtykke-tekst`, AD-18), then one fieldset per coming person (legend = name): «Ingen allergier eller matbehov», «Eller kryss av for det som gjelder:», the seven category checkboxes (Gluten, Laktose, Nøtter, Skalldyr, Vegetar, Veganer, Annet), a `textarea` (rows 4, `maxlength="200"`) labelled «Kort merknad om <name> (valgfritt)» with hint «Skriv bare det kjøkkenet trenger å vite, ingen diagnoser. Høyst 200 tegn.», then a nested fieldset legend «Får vi lagre opplysningene om <name>?» with radios «Ja» / «Nei» and `aria-describedby="samtykke-tekst"`, then (every person except the respondent) the checkbox «Jeg bekrefter at <name> vet om dette og er enig». No total, no price.
- **Consent text (FR-26, proposal from the mockup, avgjort av Claude 2026-11-23):** «Vi lagrer allergiopplysningene bare for dem dere sier ja for, og bare for at kjøkkenet skal lage mat dere tåler.» · «Rikke og Valdemar, toastmaster og forloverne kan se dem. Navn og allergier sendes til kjøkkenet på Hardingasete.» · «Dere kan trekke samtykket tilbake når som helst med den samme lenken, også etter svarfristen. Da slettes opplysningene.» · «Dere kan sende svaret også uten å samtykke. Da lagrer vi ikke allergiopplysningene, og dere kan heller si fra til oss direkte.» (the last sentence is FR-28's «says plainly» before any choice). `CONSENT_TEXT_VERSION = "2026-11-23"` in new `wedding/services/consent.py` (AD-18: the constant lives in `wedding/services/` and changes in the same commit as the text).
- **FR-28 warning on the step:** on GET, when `not_saved` is non-empty, a warning notice (`wedding/components/notice.html`, variant `warning`, not focused, not live) above the fieldsets: «Obs: Allergiopplysningene om <names joined «, » / « og »> blir ikke lagret uten et «Ja» til samtykke. Dere kan sende svaret likevel, og heller si fra til oss direkte.» «Fortsett» is never blocked by missing consent.
- **Errors (FR-22, PRG to `?feil=1`, texts avgjort av Claude 2026-11-23):** CONFLICT under the person's legend: «Du har krysset av for «Ingen allergier eller matbehov» og fylt inn noe annet for <name>. Velg det ene.» (summary «Rett opp allergiene for <name>», target that person's «Ingen» checkbox). CONFIRM under the confirmation checkbox, which gets `aria-invalid` and `aria-describedby`: «Kryss av for at <name> vet om dette og er enig, eller svar «Nei» på samtykket.» (summary «Bekreft for <name>», target the checkbox). Note too long, Text field error (3px error border, error line between label and field): «Merknaden om <name> kan være høyst 200 tegn.» (summary «Kort ned merknaden om <name>», target the textarea).
- **Script (UX-DR21):** `static/js/rsvp-allergies.js`, vanilla, deferred, only on the allergies step: ticking «Ingen …» unticks that person's categories; ticking a category unticks «Ingen …». It never clears the note (no typed text is lost; a note with «Ingen …» is the CONFLICT error).
- Privacy: no allergy content in logs (guest views already use `sensitive_post_parameters`, AD-15/privacy section); `Cache-Control: private, no-store` as the other steps; no DB row, session or message.
- New CSS in em breakpoints only; `.text-field` follows DESIGN.md Text field (field surface, 2px border, 20px body, label 600 above, hint italic below, ≥ 44px).

**Never:**
- No model, migration or `send_answer` change (Story 2.6b stores with consent and records `Consent`).
- No clearing of allergy data when consent is «Nei» in the draft: nothing is stored yet, so «Nei» is not a withdrawal (withdrawal of stored data is Story 7.2). The warning says it will not be saved.
- No «Personvern» link in the consent text yet: the privacy page is Story 7.1 (log in deferred-work).
- No check-page content (Story 2.5), no hike step, no change to the px breakpoints at `site.css:1429-1458`.
- No hidden fields, no free-text category, no diagnoses wording.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Skip all | «Fortsett» with nothing ticked | `allergies` done, 303/302 to `/svar/fjelltur/` (Sigmund) | none |
| Sigmund's journey | Sigmund «Ingen», bestemor Laktose, bestemor consent Ja, confirmed; Sigmund consent Ja | done, no warning | none |
| Conflict | bestemor «Ingen» + Laktose | `?feil=1`, both ticks kept in the draft, CONFLICT line + summary, title «Feil: …» | not done |
| Conflict via note | «Ingen» + note «ikke koriander» | CONFLICT | not done |
| Missing confirmation | bestemor Laktose, consent Ja, no confirmation | CONFIRM error on the checkbox (epics AC test) | not done |
| Confirmation not needed | respondent's own Ja; or other's Ja with no info; or Nei/unanswered | no error | none |
| No consent | bestemor Laktose, consent unanswered or Nei | done, goes on; GET of step 5 shows the FR-28 warning naming bestemor | none |
| Note 200 / 201 | 200 chars incl. æøå; 201 chars (forged past `maxlength`) | 200 kept; 201: the note is not written (the previous note stays), the person's id is kept in the draft's `long` list until the next allergies write, error under the label | not done |
| Whitespace note | note «   » | stored as "" (no info) | none |
| Forged values | unknown category key, consent «maybe», confirmation value other than «yes», a non-coming person's fields | ignored | none |
| Stops coming | bestemor's attendance changed to «Kommer ikke» on step 1 | her cats/none/note/consent/confirmed are dropped by `normalise_answer` (FR-75) | none |
| Bytt | respondent switched to bestemor via «Velg» | posted allergy fields kept unvalidated; Sigmund now needs confirmation if he has Ja + info; step reopens | none |
| CSRF failure | POST without token | 403, posted ticks, note, consent and confirmations kept, no errors, focused notice; no draft write | — |
| Broken draft | format 3 cookie | deleted, form starts at step 1 | — |

</intent-contract>

## Code Map

- `wedding/rules/answer.py:25-40` `Answer` — add `allergies: Mapping[int, AllergyEntry]` (or plain dict), `consent: Mapping[int, bool]`, `confirmed: frozenset/Iterable[int]` with empty defaults; `:85-108` `normalise_answer` drops them for members not in `present` (FR-75). `household_total` (`wedding/rules/money.py`) ignores them. New `wedding/rules/allergies.py`; `tests/test_rules_purity.py` must cover it.
- `wedding/rsvp/steps.py:68` `Step("allergies", …, "")` → `fields_template="rsvp/includes/allergy_fields.html"`; add `ALLERGIES` (key → Norwegian label, the `MEALS` pattern at `:100-115`). Docstring `:1-21`.
- `wedding/rsvp/draft.py:39` `VERSION = 3` → 4; `:45-87` `Draft`/`payload` add `alg` `{id: {"c": [...], "n": bool, "t": str}}`, `cons` `{id: bool}`, `conf` `[ids]`, `long` `[ids]`; `:90` `PAYLOAD_KEYS`; validators next to `_key_lists`/`_night` (`:139-164`): categories via `_is_key_list` but allowing `[]`, note `str` with `len ≤ 200`, ids members, no duplicates; `_parse` `:167-202`. Module docstring lists the new broken cases; format 3 is broken.
- `wedding/rsvp/forms.py` — add `allergy_field(id)`, `allergy_none_field`, `note_field`, `consent_field`, `confirm_field` helpers (pattern `:41-58`) and `AllergiesForm` (pattern `OvernightForm` `:172-233`): texts, `posted_entries()`, `posted_consent()`, `posted_confirmed()`, `long_notes()`; module docstring.
- `wedding/rsvp/views.py`:
  - `:73-77` `REOPENED_ON_CHANGE`/`PAID_STEPS` unchanged.
  - `:119-121` `_answer` passes the new draft fields; `:145-161` `_settled` copies them back and removes `allergies` from `done` while `allergy_problems` is non-empty for anyone.
  - Add `_allergy_fields(coming, *, respondent, draft-values, show_errors)` (pattern `_overnight_fields` `:254-299`) and `_allergies_step` (pattern `_paid_step` `:557-613`); the posted-merge helper `_with_posted` `:537-554` gets an `allergies` branch (replace each coming person's entry, consent, confirmation; set `long`).
  - `:616-679` `_later_step` dispatches `allergies`; only `hike` stays a frame. `:719-798` `render_after_csrf_failure` gets the allergies branch. Docstrings `:1-26`, `:351-361`.
- `wedding/rsvp/templates/rsvp/step.html:3-32` comment, `:34-38` head block (load `rsvp-allergies.js` when `key == "allergies"`), place for the warning notice. New `rsvp/includes/allergy_fields.html` (copy the fieldset/error markup of `overnight_fields.html` and the checkbox markup of `meals_fields.html`), `rsvp/includes/consent_text.html`.
- `wedding/services/consent.py` (new): `CONSENT_TEXT_VERSION`. `tests/test_only_services_write.py` must still pass.
- `static/css/site.css:965-1011` `.form-group`/`.choice`/`.field-error` (reuse), `:1077-1090` the 2.3 block — append a Story 2.4 block (`.text-field`, nested consent fieldset spacing, «Eller kryss av …» line); breakpoints in em.
- `guests/views.py:203-260` unchanged except docstrings if they list steps; check `rsvp_step` passes the allergies slug through `handle_step` already.
- Tests to update: `tests/test_rsvp_who_is_coming.py:53,408-460,549-575` (frame tests move to `fjelltur`, which needs the allergies step done first), `tests/test_rsvp_overnight_meals.py:338` (`allergier` stays in the 204 list) and the «no `<script`» assertions (allergies now has exactly one script, `js/rsvp-allergies.js`), `tests/test_rsvp_draft.py:111-130` (v4 size test), `:134+` round trips and `BROKEN` cases.
- Seed (read-only): Sigmund's household = Sigmund + bestemor (`test-sigmund0000000000`), Arild's = Arild, Marie, Filippa, Leone (`wedding/fixtures/seed.toml`).
- Docs: `docs/manual-test-plan.md:19` (MT-1 2.3 pattern) and `:49-51` (MT-30–32 pattern); `README.md:9` status, `:77-81` «Svarskjemaet», tree (`static/js/`, `wedding/services/`); ARCHITECTURE-SPINE AD-8 (`:138-142`) and AD-18 (`:233-242`); EXPERIENCE.md `:137` microcopy row and `:211` Consent block; DESIGN.md `:682` Text field, `:692` Consent block.

## Tasks & Acceptance

**Execution:**
- [x] `wedding/rules/allergies.py`, `wedding/rules/answer.py`: `ALLERGY_KEYS`, `NOTE_MAX`, the entry type, `has_allergy_info`, `allergy_problems`, `not_saved`; `Answer` fields and `normalise_answer` dropping them for non-comers (FR-25–FR-28, FR-75, AD-2, AD-18).
- [x] `wedding/services/consent.py`: `CONSENT_TEXT_VERSION = "2026-11-23"` with a docstring (AD-18, FR-29; used by 2.6b).
- [x] `wedding/rsvp/steps.py`: `ALLERGIES` labels, the allergies `fields_template`.
- [x] `wedding/rsvp/draft.py`: format 4 with `alg`, `cons`, `conf`, `long` and their validators.
- [x] `wedding/rsvp/forms.py`: field helpers, `AllergiesForm` and every text above.
- [x] `wedding/rsvp/views.py`: `_allergy_fields`, `_allergies_step` (GET with warning and errors from the draft; POST: «Velg» keeps posted values; «Fortsett» writes, PRG on problems or a long note), `_with_posted` branch, `_settled`, `_later_step`, CSRF branch, docstrings.
- [x] `wedding/rsvp/templates/rsvp/step.html`, `rsvp/includes/allergy_fields.html`, `rsvp/includes/consent_text.html`: markup per Boundaries; every input labelled, each person's fieldset `aria-describedby` its error, the consent fieldset `aria-describedby="samtykke-tekst"`.
- [x] `static/js/rsvp-allergies.js`, `static/css/site.css`: the exclusive tick and the Story 2.4 CSS block (em breakpoints).
- [x] `tests/test_allergy_rules.py`: every matrix row at rule level (`has_allergy_info`, each problem code, respondent vs other, `not_saved` with None/False/True), `normalise_answer` dropping allergy data for a non-comer, purity.
- [x] `tests/test_rsvp_allergies.py`: every matrix row through the test client (Sigmund and Arild); the epics AC test «consent Ja for someone else with info, confirmation not ticked → field error»; the confirmation checkbox absent for the respondent and present for others, and moving after «Bytt»; consent radios start unchecked; FR-26 consent text present once; `CONSENT_TEXT_VERSION` paired with a sha256 of `consent_text.html` recorded in the test (a text change fails the test until the version and hash are updated); exactly one `<script` with src `js/rsvp-allergies.js`; Enter submits as «Fortsett»; Cache-Control private, no-store; no DB rows, session or messages; a 201-char note never reaches the cookie.
- [x] `tests/test_rsvp_draft.py`: v4; `BROKEN` cases for each new key (non-member id, unknown category, duplicate, note 201 chars, non-bool consent, non-list `conf`); size test: 8 people, each with all 7 categories, a 200-character note of varied text with æøå (different per person, deterministic), consent True, confirmed, plus the v3 fields filled → `< 4096`. If it fails, pass a compact serializer to `signing.dumps` (JSON with `ensure_ascii=False`) and record it under AD-8.
- [ ] Update `tests/test_rsvp_who_is_coming.py`, `tests/test_rsvp_overnight_meals.py`, `tests/test_rsvp_days.py` for the frame now being `fjelltur` and the allergies script.
- [x] `docs/manual-test-plan.md`: Norwegian rows, date and result cells empty, each «Kjøres av Claude med Playwright mot Edge» (`channel: 'msedge'`); before each `uv run manage.py seed_testdata`, then `uv run manage.py runserver`; measure after `document.fonts.ready`.
  - **MT-1 (2.4):** README «Svarskjemaet» to step 5.
  - **MT-33 (real submission, steps 1–5):** on `http://127.0.0.1:8000/test-sigmund0000000000/svar/`: both «Kommer», «Fortsett», «Ja», «Fortsett», «Ja» for both, «Fortsett», «Fortsett» (no meals). Expect `/svar/allergier/`, title «Steg 5 av 6: Allergier og matbehov – Invitasjon», no radio checked, the consent text, the confirmation only in bestemor's fieldset. Then: (a) with JS on, tick Laktose then «Ingen …» for bestemor → Laktose unticked; (b) with JS off (`javaScriptEnabled: false`), tick both and «Fortsett» → `?feil=1`, title starts «Feil: », focused summary link «Rett opp allergiene for bestemor», both still ticked; (c) untick «Ingen …», choose «Ja» for bestemor, «Fortsett» → error «Kryss av for at bestemor vet om dette og er enig …», link «Bekreft for bestemor» focuses the checkbox; (d) tick it, Sigmund «Ingen …» and «Ja», «Fortsett» → `/svar/fjelltur/`; (e) `page.goBack()` → `/svar/allergier/` with every choice kept, no `dialog` event; (f) set bestemor's consent to «Nei», «Fortsett», go back → the «Obs: Allergiopplysningene om bestemor blir ikke lagret …» warning, and «Fortsett» still goes to `/svar/fjelltur/`; (g) a 200-character note is accepted and typing a 201st character is not possible.
  - **MT-34 (keyboard only):** Sigmund's link, `page.keyboard` only through steps 1–5. On step 5 the Tab order is «Bytt», Sigmund's «Ingen …», his categories, his note, his Ja/Nei, bestemor's group the same plus her confirmation, «Fortsett», «Tilbake», the `tel:` links; Space toggles checkboxes; every focused element has `outline-style` `solid`; Enter in a checkbox goes to `/svar/fjelltur/`.
  - **MT-35 (layout):** Arild's step 5 in the error state (CONFLICT for Marie, CONFIRM for Filippa). Run at 360 × 640 and 180 × 320, then with 20px default text (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`) at 360 × 640 and 320 × 568: `scrollWidth` ≤ `innerWidth`; every `.choice` ≥ 44px tall and inside the sheet; the textarea inside the sheet and ≥ 44px; the warning notice and error lines wrap without overflow; «Fortsett» above «Tilbake», 12px apart.
- [x] `README.md`: status line (story 2.4), «Svarskjemaet» (step 5, consent per person, nothing stored before send, the script only enhances), tree (`static/js/rsvp-allergies.js`, `wedding/services/consent.py`).
- [ ] ARCHITECTURE-SPINE, EXPERIENCE.md, DESIGN.md: dated notes (2026-11-23, Story 2.4): AD-8 format 4 and the measured size; AD-18 `CONSENT_TEXT_VERSION` location and the hash test; AD-2 `wedding/rules/allergies.py`; EXPERIENCE microcopy rows for step 5 (texts, errors, warning, consent text) «avgjort av Claude 2026-11-23» with reasons (FR-25–FR-28; mockup proposals kept; du→dere because the respondent answers for the household); Consent block: per-person Ja/Nei inside each fieldset (epics AC, UX-DR21) replaces the mockup's single household consent, with the shared explanation once above, referenced by each consent group; DESIGN.md Consent block and Text field notes to match.
- [x] `.docs/implementation-artifacts/deferred-work.md`: add «From Story 2.4»: the «Personvern» link in the consent text (Story 7.1); Story 2.5's check page uses `not_saved` for its FR-28 warning; Story 2.6b reads `CONSENT_TEXT_VERSION` and the draft's `cons`/`conf`, and AD-18's «no consent Ja across a revision change» is enforced by the revision check of 2.6c/2.9.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given Sigmund at step 5 without JavaScript, when the page renders, then each coming person has «Ingen allergier eller matbehov», the seven categories and the note field, each has an unanswered Ja/Nei consent inside their fieldset, only bestemor's fieldset has «Jeg bekrefter at bestemor vet om dette og er enig», and the consent text names the purpose, the couple, toastmaster and forloverne, Hardingasete's kitchen and withdrawal through the same link.
- Given consent «Ja» for bestemor with Laktose and the confirmation not ticked, when Sigmund presses «Fortsett», then the step comes back at `?feil=1` with the field error on the confirmation and the summary link «Bekreft for bestemor».
- Given allergy data for bestemor and consent unanswered or «Nei», when Sigmund presses «Fortsett», then he goes on to the next step, and step 5 shows the FR-28 warning when opened again.
- Given the walk through steps 1–5 in the test client, when each response is checked, then no database row, session or message is written.
- Given `docs/manual-test-plan.md`, when read, then MT-1 (2.4) and MT-33 to MT-35 hold the steps above with empty date and result cells.

## Spec Change Log

## Review Triage Log

### 2026-11-23 — Review pass
- verdicts: 24 findings — high 0, medium 2, low 14, false 8, maybe-false 0
- findings:
  - `[false]` `[reject]` The 4 KB cookie test covers one note, and eight 200-character æøå notes escaped by JSON would exceed 4 KB (blind) — the test builds eight different notes (`_note(seed)` per person, `tests/test_rsvp_draft.py:120-188`), and the draft is signed with `compress=True`; Claude measured a worst case of eight random æøå notes of 200 characters with every category: 1 836 characters signed.
  - `[low]` `[reject]` «Ingen allergier eller matbehov» alone triggers the not-saved warning and the confirmation (blind) — decided in the spec: FR-26 counts «Ingen …» as allergy information the kitchen relies on, so it needs consent like the rest; the warning is accurate.
  - `[low]` `[reject]` A confirmation survives a switch to «Nei», so a later «Ja» arrives confirmed (blind) — the checkbox stays visible and ticked on the page (seen in Edge, MT-33 f), so the respondent sees the confirmation they gave; clearing it adds a branch for no shown harm.
  - `[low]` `[defer]` «Nei» keeps the typed allergies in the guest's own draft cookie for up to 90 days (blind) — AD-8 decision (the draft holds what was entered; nothing is stored on the server); the privacy page (Story 7.1) should say the draft lives in the browser until sent or expired.
  - `[low]` `[reject]` The browser's `maxlength` and the server's `len` count the note differently (blind) — the browser is the stricter side (UTF-16 units), so a real guest never meets the server error; only forged posts do, and they get the 201 error.
  - `[low]` `[reject]` The «Ingen …» script has no automated test and does not clear the note (blind) — the server conflict rule is tested (`test_conflict`), the script ran in Edge (MT-33 a: Laktose unticked); not clearing typed text is the spec's decision (never delete what the guest wrote).
  - `[low]` `[reject]` The conflict error does not point at the note (blind) — the line says «fylt inn noe annet for <navn>» and sits under the person's legend, next to both; marking the note too adds branches for a rare state.
  - `[low]` `[reject]` `long` is only tested for people who stop coming (blind) — `Draft` validation rejects unknown ids like every other key (shared `_member_ids` check), and «Bytt» passes through `_settled`, which filters `long`; extra tests add no new protection.
  - `[medium]` `[patch]` The consent-text hash test hashes raw bytes, so a Windows checkout with `core.autocrlf` turns the template into CRLF and the test fails (blind) — the test now hashes the text with `\r\n` normalised to `\n`.
  - `[low]` `[defer]` The draft does not record which consent-text version the guest saw (blind) — Story 2.6b records `CONSENT_TEXT_VERSION` at send; the revision safeguard is already deferred to 2.6c/2.9 in deferred-work.md; added this case to that entry.
  - `[false]` `[reject]` The process trail (session log, README of examples) is missing from the diff (blind) — the session log and PR are written after review (runner step 14).
  - `[low]` `[patch]` Blank MT results; the README says «Ingenting lagres … før svaret sendes» twice in one paragraph (blind) — MT cells are filled after the browser run (step 10, not a defect); the README's first sentence is folded into the second.
  - `[low]` `[reject]` «Velg» with a too-long note redirects without `?feil`, so the old note stays silently (edge-case) — `maxlength="200"` stops a real guest typing a 201st character (Edge, MT-33 g); only a forged post reaches it, and its next «Fortsett» shows the error.
  - `[low]` `[reject]` `draft.long` can leave step 5 not done with no visible error until posted again (edge-case) — same forged-post-only path as the row above; the next «Fortsett» on step 5 shows the error.
  - `[low]` `[reject]` `maxlength` vs `len` after `clean_note` (edge-case) — same as the blind row: the browser is stricter.
  - `[low]` `[patch]` A forged `confirm_<respondent id>` is accepted into `conf` (edge-case) — `posted_confirmed` now leaves out the respondent.
  - `[low]` `[reject]` Consent is kept for a coming member whose entry was dropped as empty (edge-case) — the consent answer is the guest's own choice and is shown on the page; Story 2.6b stores allergies only where an entry exists (its AC), so a consent without data stores nothing.
  - `[false]` `[reject]` The CSS block adds no em breakpoint although the spec lists one (edge-case) — the spec asks for em breakpoints only where needed; MT-35 at 180 px and 20 px text shows none is needed after the notice fix below.
  - `[false]` `[reject]` Verification gap layer: no gaps found — nothing to route.
  - `[false]` `[reject]` The FR-28 warning is not on the check page (intent-alignment) — the check page is Story 2.5 («later the check page»); `not_saved` is the rule it will reuse, routed in deferred-work.md.
  - `[false]` `[reject]` Consent decides nothing about database storage yet (intent-alignment) — the epics give storage with consent to Story 2.6b; this story writes nothing (tested).
  - `[false]` `[reject]` The script's clearing is only checked manually (intent-alignment) — descriptive; ran in Edge (MT-33 a).
  - `[false]` `[reject]` The 201-character server check may lack a request-level test (intent-alignment) — `test_note_200_and_201` in `tests/test_rsvp_allergies.py` posts 201 characters through the view.
  - `[medium]` `[patch]` [orchestrator] At 180 × 320 the FR-28 warning runs 47 px past the viewport: «Allergiopplysningene» cannot wrap because `.notice__text` is a flex item without `min-width: 0` — `static/css/site.css` gives `.notice__text` `min-width: 0`; re-measured in Edge.

## Design Notes

- **Why consent per person, not the mockup's one household consent:** the epics AC (2026-11-16) and FR-29 record consent per person; one shared «Ja» could not express bestemor saying no. The explanation stays once above the fieldsets so it is read before any Ja/Nei (EXPERIENCE › Consent block) without repeating it eight times.
- **Why «Nei» keeps the typed allergies in the draft:** AD-8 holds everything entered until send; nothing is stored, so there is nothing to withdraw. Clearing would lose input if the guest changes their mind. FR-28's warning makes the outcome plain.
- **Why the long-note marker:** errors are computed from the draft after PRG, but an over-long note must never reach the 4 KB cookie. `maxlength` stops it in browsers, so the `long` list only serves forged or old-browser posts.
- **Why «Ingen …» with a note is a conflict:** the kitchen needs one clear answer per person; the script clears checkboxes only, never typed text.

## Verification

**Commands:**
- `uv run pytest` -- expected: all green.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.

## Auto Run Result

## Status
done

## Summary
Step 5 «Allergier og matbehov» of the RSVP form: per coming person «Ingen allergier eller matbehov», seven categories and a note of at most 200 characters, a per-person «Ja»/«Nei» consent with nothing chosen, and a confirmation for everyone but the respondent. The consent text appears once (versioned with `CONSENT_TEXT_VERSION`), an FR-28 warning names people whose information will not be saved, and nothing is written to the database (storage with consent is Story 2.6b). Draft cookie format 4.

## Files changed
wedding/rules/{allergies,answer}.py, wedding/services/consent.py, wedding/rsvp/{steps,draft,forms,views}.py, rsvp templates (step.html, allergy_fields, consent_text), static/js/rsvp-allergies.js, static/css/site.css, guests/views.py, tests (2 new files, 4 updated), README, manual test plan, ARCHITECTURE-SPINE, DESIGN.md, EXPERIENCE.md, deferred-work.md.

## Review counts
24 findings — high 0, medium 2, low 14, false 8; 4 patched, 2 deferred, 18 rejected.

## Follow-up review recommendation
false — the patches were small (a test hash normalised, one filter, one CSS property, one README sentence) and were re-verified with the full suite and the browser checks.

## Verification
uv run pytest -q: 1106 passed; ruff check, ruff format --check, djlint --check: clean. MT-1 (2.4), MT-33, MT-34, MT-35 run by Claude with Playwright 1.56.1 in Edge, before and after the patches (the first run found the 180px warning overflow).

## Residual risks
The «Ingen …» script is covered only by the Edge runs. Screen-reader reading of the consent group's aria-describedby is not checked with NVDA/VoiceOver.
