---
title: 'Story 2.3: Overnight stay, meals and the running total'
type: 'feature'
created: '2026-11-23'
status: 'done'
baseline_revision: '895b2be381eabe79c0f1eb8c01438dccc1ed1511'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
  - '{project-root}/.docs/implementation-artifacts/spec-2-2-which-days-each-person-comes.md'
warnings:
  - oversized
deferred:
- summary: >-
    Story 4.5: with a cabin or meal price of 0 the pay note («hver gjest betaler selv») and the cabin lead («Begge nettene betales …») on steps 3–4 still say guests pay; adjust the texts together with the programme's price-0 entry.
  evidence: >-
    low. Blind review; no price is 0 until the couple can edit Settings in Story 4.5.
---

<intent-contract>

## Intent

**Problem:** Steps 3 «Overnatting» and 4 «Måltider» are empty frames. Guests cannot choose a cabin or paid meals, see prices first, or see the household total (FR-15, FR-16, FR-32, FR-33, FR-70, FR-73, NFR-2, AD-2, AD-7, AD-12, UX-DR19). Three deferred items are routed here: one shared kroner display, which the programme should use too (spec-1-7). Later `done` keys and dependent choices should drop when step 1 or 2 changes (spec-2-2, FR-75). And `step.html` branches on the step key (spec-2-2).

**Approach:** Add the `Answer` value, the extended `normalise_answer` and `household_total` as pure rules. Build steps 3 and 4 on the 2.2 machinery: draft format 3, PRG errors, «Velg» and the CSRF branch. Render the total on the server on both paid steps. Add a small script that posts the step to `POST /<code>/svar/sum/` and swaps in the server's fragment. Add one `kroner` filter for both the form and the programme.

## Boundaries & Constraints

**Always:**
- **Rules (AD-2, plain values):**
  - In `wedding/rules/days.py`, add `MEAL_KEYS = ("friday_dinner", "saturday_breakfast", "sunday_breakfast")`, the order `offered_meals` uses.
  - `wedding/rules/answer.py`: a frozen dataclass `Answer(attendance, whole, days, night, meals)`.
    - `night` is `{guest_id: bool}`. `meals` is `{guest_id: [meal keys]}`.
    - Add `present_days(answer) -> dict[int, frozenset]`. It covers the coming members only. When `whole is not False`, each gets `WHOLE_WEEKEND`. When `whole is False`, each gets their chosen set if `day_error` allows it, and `WHOLE_WEEKEND` otherwise. This matches `form_steps`, so a half-made choice never drops anything.
  - `normalise_answer(answer) -> Answer` (FR-75). It applies the 2.2 rules for `whole` and `days`, then:
    - `night` keeps only coming members. A `True` survives only when `can_stay_overnight(present)` holds; otherwise the key is removed (unanswered).
    - `meals` keeps only coming members and only keys in `offered_meals(present)`, in that order. Empty lists are dropped.
  - New `wedding/rules/money.py`: `CABIN = "cabin_weekend"` and `household_total(answer, prices) -> int` (FR-33, AD-12, NFR-2).
    - It normalises first, then adds `prices[CABIN]` for each `night` True and `prices[meal]` for each chosen meal.
    - The cabin is paid per person who stays (expected.toml). The result is whole kroner as an int.
    - It is the only total; views and templates never add prices themselves.
- **Kroner display (spec-1-7 deferred):** `wedding/templatetags/money.py` has the filter `kroner(amount: int) -> str`. It writes thousands with a no-break space and « kr»: `0`→«0 kr», `340`→«340 kr», `1450`→«1 450 kr». It is used for every amount in the form. The programme's three «Godt å vite» prices use `{{ prices.x|kroner }}.` too. The programme's price-0 line stays with Story 4.5.
- **Prices:** `wedding/selectors.py` gets `form_prices(settings)`, which is `programme_prices(settings) | {CABIN: settings.price_cabin_weekend}`. `guests/views.py` `_rsvp` passes `prices=form_prices(settings)` into `handle_step` and `render_after_csrf_failure` (new keyword). That is still 3 SELECTs per request. A price of 0 is allowed: the form shows that option with no price (Rikke 2026-11-21) and leaves out the cabin price line.
- **Registry** `wedding/rsvp/steps.py`:
  - `Step` gets `fields_template` (spec-2-2 deferred). It is `rsvp/includes/{who,days,overnight,meals}_fields.html`, and `""` for the allergies and hike frames.
  - Questions (avgjort av Claude 2026-11-23: «Hvem …?»/«Hvilke …?» need no du/dere, because the registry text is the same for every household and Eva is alone; the mockup's «Skal dere overnatte på Hardingasete?» was [forslag]):
    - overnight: «Hvem skal overnatte på Hardingasete?»
    - meals: «Hvilke måltider skal vi bestille?»
  - `MEALS`: `Meal(key, name)` with «Middag fredag», «Frokost lørdag», «Frokost søndag».
  - `FormMount.total_url(key)` gives `f"{base_path}sum/?steg={slug}"`.
- **step.html:** the `h1` always has `id="sporsmal"`. It includes `fields_template` from the context, with no branching on `key`. When `total` is in the context (paid steps only), the page shows:
  - `rsvp/includes/total.html`: `<p class="form-total">Totalt for husstanden: <strong>…</strong></p>`.
  - Then an empty `<p class="visually-hidden" role="status" id="total-status"></p>`, already in the page at load (spec-1-4a deferred).
  - The form gets `data-total-url`, and `{% block head %}` adds `<script src="{% static 'js/rsvp-total.js' %}" defer></script>`.
  - Steps 1–2 and the frames still have no `<script`.
- **Draft v3 (AD-8):** `VERSION = 3`. The payload adds `"night": {"<id>": bool}` and `"meals": {"<id>": [distinct MEAL_KEYS, non-empty]}`, with members only. Anything else is broken, and so is a v2 cookie (nothing is live).
  - `_settled` runs `normalise_answer` on an `Answer` built from the draft and writes back all five parts.
  - `"overnight"` stays in `done` only while every coming member has a `night` entry.
- **Reopen on change (spec-2-2 deferred, FR-75):** `handle_step` keeps `present_days` of the draft it read (None when `who` is not done). When the settled new draft's `present_days` differ, it removes `overnight`, `meals`, `allergies` and `hike` from `done`. This covers step 1, step 2 and «Velg». A new day or a new comer therefore sends the guest back through the steps that now ask more.
- **Step 3 GET** (FR-16, FR-32, FR-70):
  - `h1`, progress «Steg n av m: Overnatting» and the respondent line.
  - The lead «Hyttene er leid for hele helgen, fra fredag 26. mai til søndag 28. mai. Begge nettene betales, også for den som bare sover der én natt.» The dates are built from `DAYS`.
  - The price line «Hytte hele helgen: <b>1 500 kr</b> per person».
  - The note `PAY_NOTE`: «Dette er Hardingasetes priser, og hver gjest betaler selv. Lunsj og middag på bryllupsdagen dekker vi.»
  - One fieldset per **coming** member, with the name as legend. Radios `overnight_<id>` = `yes` «Ja, hytte hele helgen – 1 500 kr» / `no` «Nei», checked from the draft.
  - Then the total, «Fortsett» and «Tilbake» (to step 2).
  - All texts are avgjort av Claude 2026-11-23 and live in `forms.py` (`OvernightForm`).
- **Step 3 POST «Fortsett»:**
  - Every coming member needs `yes` or `no`. `yes` for someone who cannot stay overnight is refused (FR-70).
  - If everything is valid: save, mark `overnight` done, and 302 → `next_step`.
  - If not: save the valid answers (not a refused `yes`), and 303 → `…/overnatting/?feil=1`.
- **Step 3 errors, computed from the draft:**
  - A member with no `night` entry who can stay gets «Velg «Ja» eller «Nei» for <name>.».
  - A member with no entry who cannot stay gets «For å overnatte må man være med minst to dager på rad, og <name> kommer bare <dag>. Velg «Nei», eller gå tilbake og velg flere dager for <name>.» Here `<dag>` is the lowercase `DAYS` name.
  - The summary link is «Velg overnatting for <name>» → `#overnight_<id>_yes`. The markup is the same as in 2.2.
- **Step 4 GET** (FR-15, FR-32, FR-73):
  - `h1`, progress and the respondent line.
  - `PAY_NOTE`, and the hint «Kryss av for måltidene hver person skal ha. Det er greit å ikke velge noen.»
  - One fieldset per coming member with a non-empty `offered_meals(present)`. Its checkboxes `meals_<id>` carry the meal keys, labelled «Middag fredag – 340 kr», ticked from the draft.
  - Saturday lunch and dinner are never asked about.
  - Then the total, «Fortsett» and «Tilbake».
- **Step 4 POST «Fortsett»:** each shown member's meals are replaced by the posted offered keys; forged or unoffered keys are ignored. Mark `meals` done and 302 → `next_step`. There is no error state, because choosing no meal is fine.
- **«Velg» on steps 3–4** merges the respondent and the valid posted choices without validating, and does not mark the step done. It redirects to the same step.
- **CSRF on steps 3–4** re-renders with status 403 and the posted choices checked. The total comes from the draft merged with what was posted. No draft is written.
- **`POST /<code>/svar/sum/?steg=<overnatting|maltider>`** (AD-7):
  - Route `guests:rsvp_total`, placed before `<slug>`. The view uses `never_cache`, `sensitive_post_parameters` and `require_POST`, and resolves the code (G1 404 for an unknown one).
  - It returns **204** after the deadline, without a usable draft (none, broken, `who` not done) and for any other `steg`.
  - Otherwise it merges the posted choices of that step into a copy of the draft, computes `household_total` and returns `rsvp/includes/total.html` with 200.
  - It never sets or deletes a cookie and writes nothing. It makes 3 SELECTs.
- **`static/js/rsvp-total.js`** (about 30 lines, vanilla, no build; delete `static/js/.gitkeep`):
  - On `change` in `form[data-total-url]`, POST `new FormData(form)` to the URL with `credentials: "same-origin"` (the CSRF token is in the form).
  - Only on 200: replace `.form-total` with the fragment's element, and set `#total-status`'s `textContent` to its text.
  - Ignore failures; the server value on the next page is the truth.
- **CSS** (`static/css/site.css`, RSVP section):
  - `.form-total`: right-aligned, `border-top: 1px solid var(--color-divider)`, `padding-top: var(--space-3)`, `margin-top: var(--space-6)`, `font-variant-numeric: lining-nums tabular-nums`.
  - `.form-price` and `.form-note` are body text with token spacing.
  - Radios and checkboxes reuse `.choice`. No new breakpoint; if one is ever needed, it is in em.
- Every rule, view, template comment, JS header and test names its FR/NFR/UX-DR/AD ids. UI text is Norwegian; code is English.

**Never:**
- No database write, model or migration.
- No session, messages or hidden fields.
- No price, name or date as template text.
- No total computed outside `household_total`.
- No `save`/`create`/`update`/`delete` names outside `wedding/services/`.
- No px breakpoints.
- No allergies, hike or check-page content (Stories 2.4–2.5), and no «Les mer om hyttene» (Story 7.3).
- Don't run a browser.

## I/O & Edge-Case Matrix

S = Sigmund + bestemor, A = Arild's household, E = Eva (alone), Y = Synne. Prices are the seed's: cabin 1500, dinner 340, breakfasts 260. O = `/<code>/svar/overnatting/`, M = `/<code>/svar/maltider/`.

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Open O | S: steps 1–2 «Ja» | 200 «Steg 3 av 6», 2 fieldsets, «Hytte hele helgen: 1 500 kr per person», PAY_NOTE, «Totalt for husstanden: 0 kr», 1 `<script`, empty `#total-status` | — |
| Both stay | POST both `yes` | 302 → M; GET M total «3 000 kr», 3 meals each | — |
| Missing | POST only Sigmund `yes` | 303 → `O?feil=1`; 1 link «Velg overnatting for bestemor»; Sigmund still Ja; total 1 500 kr | field error |
| One day | A: Filippa days `["sat"]`, others all; Filippa `yes` | 303 `?feil=1`; her text «… kommer bare lørdag …»; her radios unchecked | field error (FR-70) |
| Meals | S both stay, M: Sigmund all three, bestemor `sunday_breakfast` + forged `lunch` | 302 → allergier; total 3 000 + 860 + 260 = 4 120 kr | forged key ignored |
| Filippa meals | A: Filippa sat+sun | her group only «Frokost søndag – 260 kr» | — |
| No meals | Y: sat only | steps who, days, allergies (O/M skipped as in 2.2) | — |
| FR-75 day removed | A all done, Filippa stays + Frokost søndag; step 2 again, Filippa `sat` only | `night` has no Filippa, her meal gone; overnight/meals/allergies/hike not in `done`; se-over → 302 O | — |
| FR-75 not coming | S done; step 1 bestemor «Kommer ikke» | bestemor's night/meals removed; later steps reopened | — |
| Same presence | A done; step 2 Nei with all days for all | `done` keeps overnight and meals | — |
| Price 0 | cabin price 0 | «Ja, hytte hele helgen», no price line, total 0 kr | — |
| Sum | O loaded, POST sum `?steg=overnatting` both `yes` | 200 fragment «3 000 kr», no Set-Cookie, 3 SELECTs | — |
| Sum refused | no draft / `?steg=dager` / after deadline | 204 | no 500 |
| Broken | v2 cookie, `night` non-bool, meals unknown key/empty/dup, non-member | cookie deleted, step 1 | no 500 |
| CSRF | no token on O, bestemor `yes` | 403, her Ja checked, total includes it, no draft written | — |

</intent-contract>

## Code Map

- `wedding/rules/answer.py` (whole, 40 lines): `normalise_answer` becomes `Answer → Answer`. Add `present_days`. Its docstring promised the 2.3 extension. `wedding/rules/days.py:259` `DAY_KEYS`, `:291-312` `can_stay_overnight`/`offered_meals` (add `MEAL_KEYS`). New: `wedding/rules/money.py`. `tests/test_rules_purity.py` covers the new module.
- `wedding/rsvp/steps.py`:
  - `:170-191`: `Step`/`STEPS` get `fields_template` and the two questions.
  - `:194-217`: `DAYS` pattern for `MEALS`.
  - `:227-244`: `FormMount` gets `total_url`.
- `wedding/rsvp/draft.py`: `:37` VERSION, `:43-79` `Draft` and `payload`, `:82` `PAYLOAD_KEYS`, `:121-171` the validators and `_parse` (copy the `_days` pattern).
- `wedding/rsvp/forms.py`: `:18-35` constants and field-name helpers, `:90-141` the `DaysForm` pattern. Add `OvernightForm` (texts, `posted_night`), `MealsForm` (`posted_meals`) and `PAY_NOTE`.
- `wedding/rsvp/views.py`:
  - `:85-95` `_steps`.
  - `:107-116` `_settled`, which now builds an `Answer`.
  - `:160-206` `_days_fields`, the pattern for `_overnight_fields`/`_meals_fields`.
  - `:209-250` `_render_step`: add `fields_template` from `STEPS`, plus `total` and `total_url`.
  - `:326-400` the step-2 handlers are the pattern.
  - `:403-454` `_later_step`: dispatch to overnight/meals, and the frames are now only allergies/hike.
  - `:457-482` `handle_step`: add `prices` and the reopen-on-change rule.
  - `:485-548` `render_after_csrf_failure`.
  - Add `render_total`.
  - Module docstring `:1-20`.
- `wedding/rsvp/templates/rsvp/step.html:2-23` comment, `:38` h1 id, `:41-45` include branch. New: `includes/overnight_fields.html`, `includes/meals_fields.html`, `includes/total.html` (copy `days_fields.html`'s fieldset/error markup).
- `guests/views.py:179` `programme_prices` use, `:201-243` `_rsvp`/`rsvp`/`rsvp_step` (add `rsvp_total`), `:299-331` `_rsvp_after_csrf_failure`. `guests/urls.py`: add the `sum/` path before `<slug>`. `wedding/selectors.py:69-84` `programme_prices`, the pattern for `form_prices`.
- `guests/templates/guests/programme.html:93,174,217`: switch to `|kroner` (`{% load money %}`).
- `static/css/site.css`: `:517` `.visually-hidden`, `:976-993` `.choice`, `:1030-1035` `.form-actions`, `:1037-1061` the 2.2 block, which is the pattern for the new block. `static/js/.gitkeep` is replaced.
- Fixtures (read-only): `wedding/fixtures/seed.toml` (Sigmund, bestemor, Arild's household, Eva, Synne) and `wedding/fixtures/expected.toml:86-121` totals (4720, 6480, 0, 1840, 4200). `household_total` must reproduce these.
- Tests:
  - `tests/test_days_rules.py:60-95` normalise cases (new signature).
  - `tests/test_rsvp_days.py:155,254,276,322,440-461` («no `<script`» on `overnatting` and the frame list), `:517,526`.
  - `tests/test_rsvp_who_is_coming.py:51` `OVERNIGHT`, `:406-460` and `:537-560` frame tests (move to `allergier`), `:695` template text test.
  - `tests/test_rsvp_draft.py:106` the 8-person size test, `:123` round trip, `:142` `BROKEN`.
  - `tests/test_programme_page.py:255-304` (the `kr.` assertions and the source count at `:291-294`).
  - `tests/helpers.py:77-87` `checked_radios`/`ticked_boxes`.
- Docs:
  - `docs/manual-test-plan.md:18` MT-1 (2.2), `:47` last row MT-29.
  - `README.md:9` status, `:77-81` «Svarskjemaet», `:160-175` tree.
  - ARCHITECTURE-SPINE: AD-2 `:71`, AD-7 `:126-129`, AD-8 `:144`.
  - `EXPERIENCE.md:128-131` microcopy, `:205` running total.
  - `DESIGN.md:582` form step, `:695` running total.
  - `deferred-work.md:58,179,187` (to close).

## Tasks & Acceptance

**Execution:**
- [x] `wedding/rules/days.py`, `wedding/rules/answer.py`, `wedding/rules/money.py`: `MEAL_KEYS`, `Answer`, `present_days`, the extended `normalise_answer` and `household_total`, with docstrings (FR-15, FR-16, FR-33, FR-70, FR-73, FR-75, NFR-2, AD-2, AD-12).
- [x] `wedding/templatetags/__init__.py`, `wedding/templatetags/money.py`: the `kroner` filter (spec-1-7 deferred).
- [x] `wedding/selectors.py`: `form_prices`.
- [x] `wedding/rsvp/steps.py`: `fields_template`, the two questions, `MEALS`, `total_url`.
- [x] `wedding/rsvp/draft.py`: v3 with `night` and `meals`.
- [x] `wedding/rsvp/forms.py`: `OvernightForm`, `MealsForm`, `PAY_NOTE`, the field-name helpers and all the texts.
- [x] `wedding/rsvp/views.py` and the templates `rsvp/step.html`, `rsvp/includes/{overnight_fields,meals_fields,total}.html`: steps 3–4, `_settled` with `Answer`, reopen-on-change, «Velg», the CSRF branch, `render_total`, the include from the registry, and the docstrings.
- [x] `guests/views.py`, `guests/urls.py`: pass `prices`, and add the `rsvp_total` view and route.
- [x] `guests/templates/guests/programme.html`: `|kroner`.
- [x] `static/js/rsvp-total.js` (remove `static/js/.gitkeep`), `static/css/site.css`: the script and the CSS block.
- [x] `tests/test_answer_rules.py`:
  - Table-driven over all 8 subsets of `DAY_KEYS`: `can_stay_overnight` and `offered_meals` per allowed set, i.e. every allowed day combination (epics AC).
  - `present_days`.
  - `normalise_answer` drops night and meals for a non-comer and for a removed day, and keeps them for an unchosen or refused set.
  - `household_total`: each paid option alone, everything (Sigmund 4 720), the Arild, Eva and Jonas/Ida totals from expected.toml, Filippa sat+sun 1 760, Synne sat-only 0, nobody coming 0, removed choices never counting, and price 0.
  - `kroner`: 0, 340, 1 450, 12 345.
  - Move the 2.2 normalise tests here or update them in place in `tests/test_days_rules.py`.
- [x] `tests/test_rsvp_overnight_meals.py`:
  - Every matrix row.
  - «Velg» on steps 3–4 keeps choices.
  - Enter submits as «Fortsett».
  - Steps 1–2 and the frames have no `<script`; steps 3–4 have exactly one, with src `js/rsvp-total.js`.
  - `#total-status` is present and empty.
  - Cache-Control is private, no-store.
  - 3 SELECTs per request, including `sum/`.
  - No DB rows or session.
  - Totals use U+00A0.
- [x] Update `tests/test_rsvp_days.py`, `tests/test_rsvp_who_is_coming.py` (frames → `allergier`), `tests/test_rsvp_draft.py` (v3, BROKEN cases, 8 people with every field < 4 KB) and `tests/test_programme_page.py` (`|kroner`, plus a price ≥ 1000 shown as «1 450 kr.»).
- [x] `docs/manual-test-plan.md`: Norwegian rows with empty date and result cells, each «Kjøres av Claude med Playwright mot Edge» (`channel: 'msedge'`). Before each: `uv run manage.py seed_testdata`, then `uv run manage.py runserver`; measure after `document.fonts.ready`.
  - **MT-1 (2.3):** README «Svarskjemaet» to step 4.
  - **MT-30 (real submission, steps 1–4):**
    1. On `http://127.0.0.1:8000/test-sigmund0000000000/svar/`: both «Kommer», «Fortsett», «Ja», «Fortsett». Expect `/svar/overnatting/`, title «Steg 3 av 6: Overnatting – Invitasjon», «1 500 kr per person» and «Totalt for husstanden: 0 kr».
    2. With JS on, choose «Ja» for Sigmund. Wait for the response. Expect the total «1 500 kr» and `#total-status` text «Totalt for husstanden: 1 500 kr».
    3. «Fortsett». Expect `?feil=1`, the link «Velg overnatting for bestemor», Sigmund's «Ja» still chosen and the total «1 500 kr».
    4. Choose «Ja» for bestemor. Expect «3 000 kr». Then «Fortsett» → `/svar/maltider/`, «3 000 kr».
    5. Tick all three for Sigmund and «Frokost søndag» for bestemor. Expect «4 120 kr». «Fortsett» → `/svar/allergier/`.
    6. `page.goBack()`. Expect `/svar/maltider/` with the 4 boxes ticked, «4 120 kr» and no `dialog` event.
    7. On Arild's link: Arild, Marie and Filippa «Kommer», Leone not. «Nei»; Arild and Marie all days, Filippa Lørdag only. On overnight, choose «Ja» for Filippa and «Fortsett». Expect «kommer bare lørdag» under her legend.
    8. With JavaScript disabled (`javaScriptEnabled: false`), repeat 1, 4 and 5. Expect the same totals after each «Fortsett».
  - **MT-31 (keyboard only):** use Sigmund's link with `page.keyboard` only, through steps 1–4.
    - The order on step 3 is «Bytt», Sigmund's Ja/Nei, bestemor's, «Fortsett», «Tilbake», `tel:`.
    - Arrow keys change the total.
    - Every focused element has `outline-style` `solid`.
    - Enter in a checkbox on step 4 goes to `/svar/allergier/`.
  - **MT-32 (layout):** Arild's step 3 in the error state, and step 4 with Filippa's group. Run at 360 × 640 and 180 × 320, then with 20px default text (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`) at 360 × 640 and 320 × 568.
    - `scrollWidth` ≤ `innerWidth`.
    - Every `.choice` is ≥ 44px and inside the sheet.
    - The amount «1 500 kr» never breaks over lines.
    - `.form-total` is right-aligned inside the sheet.
    - «Fortsett» is above «Tilbake», 12px apart.
- [x] `README.md`: the status line (2.3), «Svarskjemaet» (steps 3–4, the total, and that the total also updates while the guest chooses, with JavaScript; `POST /<kode>/svar/sum/`) and the tree (`static/js/`, `wedding/templatetags/`).
- [x] ARCHITECTURE-SPINE, EXPERIENCE.md, DESIGN.md: dated notes (2026-11-23, Story 2.3):
  - AD-2: `Answer`, `present_days`, `rules/money.py`.
  - AD-7: `sum/?steg=` and its 204 cases, the visible total vs the empty status region, and reopen-on-change.
  - AD-8: format 3.
  - The microcopy for steps 3–4, PAY_NOTE, the error texts and the questions, all «avgjort av Claude 2026-11-23» with the reason (FR-16/FR-32/FR-70 and the form-step pattern; «Hvem/Hvilke» avoid du/dere).
  - In DESIGN, the running total component: the visible `.form-total` is not live, and the empty `role="status"` beside it gets the text.
- [x] `.docs/implementation-artifacts/deferred-work.md`: mark the three entries done, at `:58` (kroner, spec-1-7), `:179` (reopen/FR-75, spec-2-2) and `:187` (include from registry, spec-2-2). Leave the price-0 programme entry (`:62`, Story 4.5) open.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given the seed households, when `household_total` runs on each household's seeded answer and `form_prices` of the seed settings, then it equals that household's `total` in `expected.toml`.
- Given steps 1–4 walked in the test client without JavaScript, when each page renders, then the total shown equals `household_total` of the draft, and no database row, session or message is written.
- Given `docs/manual-test-plan.md`, when read, then MT-1 (2.3) and MT-30 to MT-32 hold the steps above with empty date and result cells.

## Spec Change Log

## Review Triage Log

### 2026-11-23 — Review pass
- verdicts: 21 findings — high 0, medium 1, low 12, false 8, maybe-false 0
- findings:
  - `[low]` `[reject]` The error-summary link for a member whose days block a stay focuses «Ja» although the line says «Velg «Nei»» (blind) — every summary link goes to the group's first input (FR-22, the 2.1 convention); the error line under the legend is read with the group, and the arrow keys reach «Nei». A special case adds a branch for a rare state.
  - `[low]` `[reject]` A refused «Ja» is dropped, so the group shows nothing chosen after the redirect (blind) — decided in the spec (the stay cannot be saved; `normalise_answer` would remove it), and the error line names the reason; MT-30 trinn 7 shows Filippa's group with the explanation.
  - `[false]` `[reject]` Step 4 can render with no meal fieldsets (blind) — `form_steps` (`wedding/rules/form_steps.py:50`) leaves out «meals» when nobody present is offered a paid meal, so the step is never shown empty.
  - `[low]` `[defer]` The pay note and the cabin lead still say guests pay when a price is 0 (blind) — belongs with the price-0 entry routed to Story 4.5, which first lets the couple save a 0.
  - `[low]` `[reject]` `kroner` raises on None or a string (blind) — every caller passes an int from `form_prices`/Settings or `household_total`; a guard adds a branch for input that never reaches it.
  - `[low]` `[reject]` A CSRF failure on `sum/` is untested (blind) — the script accepts only 200 and leaves the server-rendered total in place; nothing is written; the next «Fortsett» shows the right total.
  - `[low]` `[reject]` `render_total` does not check step order (blind) — it writes nothing and returns only the household's own total from its own draft; documented by the implementer; same as the edge-case row.
  - `[low]` `[patch]` The script rewrites the status region on every change, so the same total is announced again (blind) — `rsvp-total.js` now writes the status text only when the total changed.
  - `[low]` `[reject]` `OvernightForm`/`MealsForm` extend `forms.Form` without fields, and the CSRF branch repeats the step choice (blind) — same pattern as `DaysForm` after 2.2 (no unused field declarations); the form classes hold the texts and validation in one place.
  - `[false]` `[reject]` The process trail is missing from the diff (blind) — the session log, issues and PR are written after review (step 14); «avgjort av Claude» follows Rikke's goal-run rule of 2026-11-23; the cookie format bump is recorded in the spec and ARCHITECTURE-SPINE AD-8.
  - `[low]` `[reject]` `kroner` on non-int input (edge-case) — same as the blind row: callers always pass ints.
  - `[low]` `[reject]` When the newest request fails, an older total may stay on screen (edge-case) — needs a network failure mid-typing; the server re-renders the total on «Fortsett», which is the truth (AD-7); a retry adds complexity.
  - `[low]` `[reject]` `sum/` is not gated by step order (edge-case) — same as the blind row.
  - `[false]` `[reject]` The live update in the browser is not verified (intent-alignment) — MT-1 (2.3), MT-30, MT-31 and MT-32 were run by Claude in Edge after the review: 0 → 1 500 → 3 000 → 4 120 kr, `#total-status` filled, arrows change the sum.
  - `[false]` `[reject]` FR-75 via «Endre» on the check page is not exercised (intent-alignment) — the check page is Story 2.5; the rule and the step-2 re-post path are tested, which is what «for example» allows now.
  - `[false]` `[reject]` «Identical on check page and receipt» is not shown (intent-alignment) — those pages are Stories 2.5/2.6; both use `household_total`, the single rule this story adds.
  - `[false]` `[reject]` The AC2 explanation is only server-tested (intent-alignment) — descriptive, no defect; also seen in Edge (MT-30 trinn 7).
  - `[false]` `[reject]` The table test covers all 8 subsets, beyond the AC (intent-alignment) — descriptive, no defect.
  - `[medium]` `[patch]` [orchestrator] At 180 px the error summary on step 3 runs past the sheet: «må du» and «overnatting» are cut at the right edge (screenshot svar-steg3-180-16.png) — fixed in `static/css/site.css` so long words wrap inside the box; re-measured in Edge.
  - `[false]` `[reject]` Verification gap layer: no gaps found — nothing to route.
  - `[low]` `[patch]` [implementer] In `test_one_day_is_blocked` the assertion that Filippa is absent from the draft's `night` uses the wrong key type, so it checks nothing — the assertion now uses the stored key type.

## Design Notes

- **Why a one-day person is still asked about overnight:** the epics AC and EXPERIENCE › Contradiction ask for «blocked with an explanation» when someone present one day chooses overnight. The radios stay, and «Ja» is refused with the reason. A refused «Ja» is not saved, because `normalise_answer` would remove it anyway (FR-75). So the error page shows the reason with nothing chosen, and «Nei» is the fix.
- **Why later steps reopen on a presence change:** meals and the hike are optional, so "complete" cannot be derived for them. A new day or a new comer adds questions the guest never saw. Comparing `present_days` before and after a write catches every path, including step 1, step 2 and «Velg», in one place.
- **Why the total has two elements:** the visible total is in the page at load, so it must not be a live region (UX-DR17). The empty `role="status"` gets only text, following the spec-1-4a deferred rule. The fragment comes from the same template the page uses, so the two cannot differ.

## Verification

**Commands:**
- `uv run pytest`: expected all green.
- `uv run ruff check` and `uv run ruff format --check`: expected no findings.
- `uv run djlint --check .`: expected no findings.

## Auto Run Result

## Status
done

## Summary
Steps 3 «Overnatting» and 4 «Måltider» of the RSVP form, with prices shown before any choice, the one-day block with an explanation, and the household total rendered on the server and updated by a small script through `POST /<kode>/svar/sum/`. One `kroner` filter («1 500 kr») also used on the programme. Later steps reopen when the people or days present change (FR-75). The step registry names each step's include.

## Files changed
wedding/rules/{answer,days,money}.py, wedding/templatetags/money.py, wedding/selectors.py, wedding/rsvp/{steps,draft,forms,views}.py, rsvp templates (step.html, overnight_fields, meals_fields, total), guests/{views,urls}.py, programme.html, static/js/rsvp-total.js, static/css/site.css, tests (2 new files, 6 updated), README, manual test plan, ARCHITECTURE-SPINE, DESIGN.md, EXPERIENCE.md, deferred-work.md.

## Review counts
21 findings — high 0, medium 1, low 12, false 8; 3 patched, 1 deferred, 17 rejected.

## Follow-up review recommendation
false — the patches were small (CSS wrapping, one JS condition, one test assertion) and were re-verified with the full suite and the browser checks.

## Verification
uv run pytest -q: 1021 passed; ruff check, ruff format --check, djlint --check: clean. MT-1 (2.3), MT-30, MT-31, MT-32 run by Claude with Playwright 1.56.1 in Edge, before and after the patches.

## Residual risks
The script is covered only by the Edge runs, not by automated tests. Screen-reader announcement of the status region is not checked with NVDA/VoiceOver.
