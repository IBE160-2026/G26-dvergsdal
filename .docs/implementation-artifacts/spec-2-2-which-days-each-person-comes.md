---
title: 'Story 2.2: Which days each person comes'
type: 'feature'
created: '2026-11-23'
status: 'ready-for-dev'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-1-start-the-answer-who-is-coming.md'
warnings:
  - oversized
deferred: []
---

<intent-contract>

## Intent

**Problem:** Step 2 «Dager» is an empty frame (Story 2.1). Guests cannot say whether everyone comes the whole weekend or pick days per person. `form_steps` assumes the whole weekend, and nothing removes choices when a person stops coming (FR-14 step 2, FR-70 dates, FR-75, AD-2, UX-DR19). Step questions and the summary texts are also spread over views and templates (deferred-work, Story 2.1 blind review).

**Approach:** Add pure day rules and `normalise_answer` in `wedding/rules/`. Teach `form_steps` the days. Build step 2 on Story 2.1's machinery. It is one address: the «Ja/Nei» question, and after «Nei» the per-person day checkboxes, with the same PRG error flow. Give the step registry a `question` field and a `DAYS` registry, and move each step's texts next to its form.

## Boundaries & Constraints

**Always:**
- **Rules (AD-2, pure, plain values):** `wedding/rules/days.py`: `DAY_KEYS = ("fri", "sat", "sun")` (the keys `seed.toml` uses) and `WHOLE_WEEKEND`. `day_error(days) -> str | None`, which is None for the six allowed sets (one day, fri+sat, sat+sun, all three), `"none"` for an empty set and `"gap"` for fri+sun without sat (FR-14, FR-70). It raises `ValueError` on an unknown key. `can_stay_overnight(days)` is an allowed set of two or more days (FR-16, FR-70). `offered_meals(days)` returns, in this order, `friday_dinner` when Friday is in the set, `saturday_breakfast` when Friday and Saturday are, and `sunday_breakfast` when Sunday is (FR-15, FR-73). These keys match `programme_prices` and `seed.toml`, and Story 2.3 reuses them. `wedding/rules/answer.py`: `normalise_answer(attendance, whole, days) -> (whole, days)` (FR-75). It keeps days only for coming members, in `DAY_KEYS` order, with unknown keys dropped. It returns `days == {}` unless `whole is False`, and `whole = None` when nobody comes. Its docstring says Story 2.3 extends it with overnight stay and meals.
- **`form_steps(attendance, days=None)`** (UX-DR19, FR-17). `days` is a sequence aligned with `attendance`, one chosen set or None per member. A coming member counts with their set when `day_error` is None; otherwise they count as the whole weekend. The result is who and days, then overnight if anyone `can_stay_overnight`, meals if anyone has `offered_meals`, allergies, and hike if anyone has `"fri"`. For None, or nobody coming, it returns what it returns today. Add `first_unfinished(steps, done, before) -> str | None`: the first applicable step before `before` (`None` = the check page) that is not in `done`.
- **Registry** `wedding/rsvp/steps.py`: `Step` gets `question`. who is «Hvem kommer?» and days is «Er alle som kommer, med hele helgen?» **[forslag]**. The frames keep their name until 2.3–2.5. `DAYS`: one `Day(key, name, date, summary)` per day key: «Fredag», «26. mai», «Fjelltur, middag og rebus» / «Lørdag», «27. mai», «Bryllupsdagen: vielse, lunsj og fest» / «Søndag», «28. mai», «Frokost og hjemreise» (summaries **[forslag]**). This is the only place the form holds dates. A test ties them to `programme.html`.
- **Draft (AD-8):** `VERSION = 2`. The payload adds `"whole": true|false|null` and `"days": {"<guest id>": [day keys]}`. The lists are non-empty, hold distinct `DAY_KEYS` and are keyed by members. Anything else is broken and deleted, as in 2.1. A v1 cookie is broken, which is fine because nothing is live. Every draft write runs `normalise_answer`. A draft keeps `"days"` in `done` only while `whole is True`, or every coming member's set passes `day_error`. This applies after step 1, after «Velg» and after step 2.
- **Step 2 GET** (FR-14, FR-70, UX-DR16, UX-DR19). It requires `"who"` done (else 302 to step 1). The order is: `h1` question (id `sporsmal`), progress «Steg n av m: Dager», respondent line, then a list of the three days: «<strong>Fredag 26. mai</strong>: Fjelltur, middag og rebus». Then one fieldset `aria-labelledby="sporsmal"` with radios `whole` = `yes` «Ja, alle er med fra fredag til søndag» / `no` «Nei, jeg velger dager for hver person» **[forslag]**. When `whole is False`, an `h2 id="velg-dager"` «Velg dagene for hver person» **[forslag]** follows. Under it is one fieldset per **coming** member (legend = name) with checkboxes `days_<id>` = `fri`/`sat`/`sun`, labelled «Fredag 26. mai» and so on, ticked from the draft. Then «Fortsett» above «Tilbake» (to step 1). Nothing is preselected (`whole` null → no radio checked). The hidden first «Fortsett» from 2.1 is kept on every step with fields.
- **Step 2 POST «Fortsett»:**
  - `whole` missing or forged: 303 → `…/dager/?feil=1`.
  - `yes`: normalise, mark `days` done, 302 → `next_step`.
  - `no`, while the draft's `whole` is not False and no `days_*` field is posted: save `whole=False` without `days` in `done`, then 302 → `…/dager/#velg-dager`. This is the reveal, not an error.
  - `no` otherwise: take the valid posted day keys of coming members. If every coming member passes `day_error`, save, mark `days` done and 302 → next. If not, save what was posted, keep `days` out of `done` and 303 → `?feil=1`.
- **Step 2 errors (GET `?feil=1`, FR-22):** the errors are computed from the draft, as in step 1. If `whole` is null, the error is «Velg «Ja» eller «Nei».» with the summary link «Svar på om alle er med hele helgen» → `#whole_yes`. If `whole` is False, each coming member is checked. `"none"` gives «Velg minst én dag for <name>.». `"gap"` gives «<name> kan ikke komme fredag og søndag uten lørdag, fordi dagene må komme etter hverandre. Velg lørdag også, eller bare én av dagene.» The summary link for both is «Velg dager for <name>» → `#days_<id>_fri` (all texts **[forslag]**). The markup is the same as step 1: error line under the legend, `aria-describedby`, `aria-invalid`, focused summary and the «Feil: » title.
- **Gating:** a later step frame or the check page redirects (302) to `first_unfinished` when that is not None. A step that is not applicable goes on as in 2.1. Step 1's valid POST still goes to `next_step` (days).
- **«Velg» on step 2** merges the posted respondent, the posted `whole` and the valid posted days, then normalises. It does not validate and redirects to `…/dager/`. **CSRF on step 2** re-renders step 2 with status 403, with the posted `whole` and days ticked. The day groups show when the posted `whole` is `no` or the draft's `whole` is False.
- **Texts next to their forms:** step 1's error line and summary text move from `views.py` into `forms.py`. Step 2's go into a `DaysForm` there too. `views.py` uses `STEPS[key].question` and no literal question.
- Each step's fields go in their own include (`rsvp/includes/who_fields.html`, `days_fields.html`), and step.html picks one by key.
- **CSS:** one block in the RSVP section for the day list. Checkboxes reuse `.choice`: 26px, `accent-color`, row ≥ 44px. No new breakpoint. If one is ever needed, it is in em. The three px breakpoints at `site.css:1376,1399,1405` are not touched, so their deferred entry stays open.
- Every rule, view, template comment and test names its FR/NFR/UX-DR/AD ids. UI text is Norwegian; code is English.

**Never:**
- No database writes, model or migration.
- No session or messages, and no hidden answer fields.
- No JavaScript.
- No overnight, meal, price or total UI (Story 2.3), and no blocking of overnight stay (Story 2.3).
- No names, dates or prices in templates.
- No `save`/`create`/`update`/`delete` method names outside `wedding/services/`, including `dict.update`; use `|`.
- No px breakpoints.
- Don't run a browser.

## I/O & Edge-Case Matrix

S = Sigmund's household (2 people), A = Arild's (Arild, Marie, Filippa, Leone), Y = Synne's (1). D = `/<code>/svar/dager/`.

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Open | A: step 1 with Leone «Kommer ikke», others coming; GET D | 200, «Steg 2 av 6: Dager», h1 question, three day lines with dates, 0 checked, no checkbox, 3 SELECTs | — |
| Ja | POST `whole=yes` | 302 → `/A/svar/overnatting/`; draft `whole` true, `days` {}, `done` has days | — |
| Reveal | POST `whole=no` (fresh) | 302 → `D#velg-dager`; GET shows Nei checked, 3 groups (not Leone), 9 unticked boxes, still «av 6» | — |
| Gap | groups shown; Filippa fri+sun, others all | 303 → `D?feil=1`; 1 summary link «Velg dager for Filippa», gap text under her legend, her boxes still ticked | field error |
| No day | groups shown; Marie nothing | `?feil=1`, «Velg minst én dag for Marie.» | field error |
| No whole | POST nothing / `whole=maybe` | `?feil=1`, «Velg «Ja» eller «Nei».» | field error |
| Valid days | Filippa sat+sun, others all | 302 → overnatting, «Steg 3 av 6» | — |
| m follows days | Y: Synne sat only | 302 → `/Y/svar/allergier/` «Steg 3 av 3»; Back to D: «Steg 2 av 3» | — |
| FR-75 | A days done (Filippa sat+sun), step 1 again with Filippa «Kommer ikke» | draft `days` has no Filippa; days stays done | — |
| New comer | A days done with Nei, step 1 again with Leone «Kommer» | 302 → D; `days` not in done; GET `/A/svar/se-over/` → 302 D | — |
| Nobody | step 1 all «Kommer ikke» after days | `whole` null, `days` {}; check page | — |
| Gate | `who` done, `days` not; GET overnatting/fjelltur/se-over | 302 → D | — |
| Broken | `days` with a non-member id, a bad key, an empty list or duplicates; `whole` = "no" | cookie deleted, step 1 empty | no 500 |
| CSRF | no token, `whole=no`, Filippa sat | 403, Nei checked, groups shown, Filippa sat ticked, no draft written | — |

</intent-contract>

## Code Map

- `wedding/rules/form_steps.py` (whole file, 49 lines): `form_steps` gets `days` and the per-step conditions. Add `first_unfinished`. Update the docstring, which says «Story 2.2 extends». `wedding/rules/households.py` is the docstring pattern. New: `wedding/rules/days.py`, `wedding/rules/answer.py`. `tests/test_rules_purity.py` keeps them pure.
- `wedding/rsvp/steps.py:14-32`: `Step` + `STEPS` get `question`. Add `Day`/`DAYS`. `:35-40` CHECK constants.
- `wedding/rsvp/draft.py`: `:33` VERSION, `:39-68` `Draft` (add `whole`, `days`, payload), `:71` `PAYLOAD_KEYS`, `:90-122` `_attendance`/`_parse` (validate the new keys the same way).
- `wedding/rsvp/forms.py`: `:13-15` the yes/no values, `:23-48` `WhoIsComingForm` (it receives the error and summary texts), `:50-62` `posted_attendance`. Add `DaysForm` (whole + `days_<id>`, `posted_whole`, `posted_days`, its texts).
- `wedding/rsvp/views.py`:
  - `:52-60` `_steps` passes days.
  - `:71-126` `_render_step`: the step-1 rows and `:116` the hard-coded question move out; it becomes generic over the step's fields.
  - `:137-149` `_switched` also merges days on step 2.
  - `:152-197` `_who_is_coming` runs normalise and resets `done`.
  - `:200-234` `_frame` gets gating via `first_unfinished`.
  - `:237-262` `handle_step` dispatches step 2.
  - `:265-310` `render_after_csrf_failure` gets the step-2 branch.
  - Module docstring `:1-14`.
- `wedding/rsvp/templates/rsvp/step.html:33-35` hidden button, `:36` h1, `:39-68` rows → include. `includes/error_summary.html`, `includes/respondent.html` are unchanged.
- `guests/views.py:230-250` `rsvp`/`rsvp_step` and `:299-332` `_rsvp_after_csrf_failure` should need no change. Keep 3 SELECTs.
- `static/css/site.css:888` RSVP form section, `.choice` ~`:981-997`. The px breakpoints at `:1376,1399,1405` stay.
- `guests/templates/guests/programme.html:39-40,103-105,189-190`: the day names and dates `DAYS` must match.
- Tests:
  - `tests/test_form_steps.py:33-48` seed shapes (now with `days` from `seed.toml`), `:82` registry test.
  - `tests/test_rsvp_draft.py:101-112` the 8-person size test (add days), `:114-140` `BROKEN`.
  - `tests/test_rsvp_who_is_coming.py`: `:49` `DAYS` constant; `:398-437` frame tests use the days frame and must move to `overnatting`; `:516` CSRF on a frame; `:602` whole flow; `:661-676` the template text test.
- Docs:
  - `docs/manual-test-plan.md:17` MT-1 (2.1), `:43` last row MT-26.
  - `README.md:9` status, `:77-81` «Svarskjemaet».
  - `ARCHITECTURE-SPINE.md:144` AD-8 format note, `:129` AD-7 addresses.
  - `EXPERIENCE.md:128` microcopy, `:200` progress line, `:283` step order.
  - `DESIGN.md:582` Form step, `:683` choice control.
  - `deferred-work.md:146` the `question` entry.

## Tasks & Acceptance

**Execution:**
- [ ] `wedding/rules/days.py`, `wedding/rules/answer.py`, `wedding/rules/form_steps.py`: the rules per Boundaries, with docstrings (FR-14, FR-15, FR-16, FR-17, FR-70, FR-73, FR-75, AD-2, UX-DR19).
- [ ] `wedding/rsvp/steps.py`: `question`, `DAYS`.
- [ ] `wedding/rsvp/draft.py`: v2 with `whole` and `days`.
- [ ] `wedding/rsvp/forms.py`: texts moved next to `WhoIsComingForm`, plus the new `DaysForm`.
- [ ] `wedding/rsvp/views.py` and `wedding/rsvp/templates/rsvp/{step.html,includes/who_fields.html,includes/days_fields.html}`: step 2, gating, normalise on every write, «Velg», the CSRF branch and docstrings.
- [ ] `static/css/site.css`: the day list block.
- [ ] `tests/test_days_rules.py`: one table of all 8 subsets of `DAY_KEYS` → `day_error`, `can_stay_overnight`, `offered_meals` (fri+sun is refused, and empty gives `"none"`); an unknown key → `ValueError`; `normalise_answer` cases from the matrix.
- [ ] `tests/test_form_steps.py`: each seed household with its seeded days gives its steps (for example Synne gives who, days, allergies; Jonas/Ida have no Sunday, so meals still apply via Friday). Also cover a refused or None set counting as the whole weekend and `first_unfinished`.
- [ ] `tests/test_rsvp_draft.py`: v2 round trip, the new broken cases, and 8 people with all days staying < 4 KB.
- [ ] `tests/test_rsvp_days.py`: every matrix row; «Velg» on step 2 keeps its choices; Enter submits as «Fortsett» (the hidden button comes first); no `<script`; Cache-Control private/no-store; 3 SELECTs; no DB rows.
- [ ] `tests/test_rsvp_who_is_coming.py`: point the frame tests at `overnatting`. Extend the template text test so no `\d{1,2}\. (januar|…|desember)` date appears in the rsvp templates. Add a test that each `DAYS` name and date appears in `programme.html`.
- [ ] `docs/manual-test-plan.md`: Norwegian rows with empty date and result cells, each «Kjøres av Claude med Playwright mot Edge» (`channel: 'msedge'`). Run `uv run manage.py seed_testdata`, then `uv run manage.py runserver`, and measure after `document.fonts.ready`.
  - **MT-1 (2.2):** follow README «Svarskjemaet» to step 2.
  - **MT-27 (real submission, steps 1–2):**
    1. Open `http://127.0.0.1:8000/test-arild000000000000/svar/`. Choose «Kommer» for Arild, Marie and Filippa, «Kommer ikke» for Leone, then «Fortsett». Expect URL `/svar/dager/`, title «Steg 2 av 6: Dager – Invitasjon», text «Fredag 26. mai», «Lørdag 27. mai» and «Søndag 28. mai», and 0 `input:checked`.
    2. «Fortsett» with nothing chosen. Expect `?feil=1`, title starting «Feil: », focus on the summary and 1 link. Click it; focus moves to `#whole_yes`.
    3. Choose «Nei» and «Fortsett». Expect 3 fieldsets, Leone not among them, and «Steg 2 av 6».
    4. Tick all days for Arild and Marie, and Fredag + Søndag for Filippa, then «Fortsett». Expect `?feil=1`, the link «Velg dager for Filippa», and the text «fredag og søndag uten lørdag» under her legend, with her two boxes still ticked.
    5. Change Filippa to Lørdag + Søndag and «Fortsett». Expect `/svar/overnatting/` and «Steg 3 av 6».
    6. `page.goBack()`. Expect Filippa's Lørdag and Søndag ticked, and no `dialog` event.
    7. On `test-synne000000000000`: «Kommer», «Nei», Lørdag, «Fortsett». Expect `/svar/allergier/` and «Steg 3 av 3». `goBack()` shows «Steg 2 av 3».
  - **MT-28 (keyboard only):** use `page.keyboard` only, on Arild's link. Fill step 1. On step 2, choose «Nei» with the arrow keys and press Enter, then tick days with Space. Enter in a checkbox goes to `/svar/overnatting/`. Every focused element has `outline-style` `solid`. The order is: «Bytt», the Ja/Nei group, Arild's three boxes, Marie's, Filippa's, «Fortsett», «Tilbake», the `tel:` links.
  - **MT-29 (layout):** Arild's step 2 with the groups shown, normal and in the error state. Run at 360 × 640 and 180 × 320. Then, with a 20px default font (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`), at 360 × 640 and 320 × 568. Expect `scrollWidth` ≤ `innerWidth`. Each `.choice` row is ≥ 44px and inside the sheet. Checkboxes are 26 × 26 at the default size. The day lines wrap inside the sheet. «Fortsett» is above «Tilbake» with ≥ 12px between them and the same width.
- [ ] `README.md`: status (2.2) and «Svarskjemaet». Steps 1–2 are built: «Ja» or «Nei» with days per person. The rest are frames until 2.3–2.5.
- [ ] `ARCHITECTURE-SPINE.md`: dated notes (2026-11-23, Story 2.2). AD-8: format v2 with `whole`/`days`. AD-7: step 2 is one address and shows the day groups after «Nei» (`#velg-dager`). Later steps redirect to the first unfinished one. AD-2: `rules/days.py`, `rules/answer.py`.
- [ ] `EXPERIENCE.md` and `DESIGN.md`: dated notes. Add the step-2 microcopy, the day list and the error texts, all **[forslag]**. Note that step 2 reveals the day groups at the same address. Note that the progress line's m counts an unchosen or refused set as the whole weekend.
- [ ] `.docs/implementation-artifacts/deferred-work.md`: mark `:146` done (`question` in the registry, texts in `forms.py`). Leave the px-breakpoint entry open, since it is untouched.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given step 2 after someone is «Kommer», when it opens, then the `h1` asks whether everyone coming is there the whole weekend, and each day shows its date and what happens (FR-14, FR-70).
- Given the whole flow through steps 1–2 in the test client, when it runs, then no database row, session or message is written, and every response is `private, no-store`.
- Given `docs/manual-test-plan.md`, when read, then MT-1 (2.2) and MT-27 to MT-29 hold the steps above with empty date and result cells.

## Spec Change Log

## Review Triage Log

## Design Notes

- **Why one address for step 2:** EXPERIENCE makes «hele helgen? / dager per person» one step. Without JavaScript, «Nei» has to reach the server before the day groups can appear. Revealing them at the same address keeps «Steg 2 av m» and «Tilbake» honest. Most households answer «Ja» and never see 9 checkboxes.
- **Why the dates live in `DAYS`:** there is no day model, and AD-17 keeps v1 info text in code. The front page and the programme hold the dates as template text. The form needs them in labels and error lines, so they live once in the registry, and a test ties them to `programme.html`.
- **Why invalid days are saved:** the `?feil=1` page must show what the guest ticked. `done` is what protects later steps and the counts, not the draft's contents.

## Verification

**Commands:**
- `uv run pytest`: expected all green, including the updated Story 2.1 tests.
- `uv run ruff check` and `uv run ruff format --check`: expected no findings.
- `uv run djlint --check .`: expected no findings.
