---
title: 'Story 2.1: Start the answer: who is coming'
type: 'feature'
created: '2026-11-21'
status: 'done'
baseline_revision: 'f644b6615edff2e4fa16068cfba33b83eec95148'
review_loop_iteration: 0
followup_review_recommended: false
context:
  - '{project-root}/.docs/implementation-artifacts/epic-2-context.md'
warnings:
  - oversized
  - multiple-goals
deferred:
  - summary: >-
      No README step or MT row reaches the closed page after the deadline by hand.
    evidence: |-
      Blind review. The closed page is tested in pytest only; Story 4.3 builds the locked states after the deadline and should add the manual route.
    location: >-
      guests/templates/guests/rsvp_closed.html
    severity: low
  - summary: >-
      Step questions, the summary text and the yes/no values are spread over views, forms and templates.
    evidence: |-
      Blind review. Steps 2-6 get their questions in Stories 2.2-2.5; a `question` field in the step registry (wedding/rsvp/steps.py) belongs with them.
    location: >-
      wedding/rsvp/views.py
    severity: low
  - summary: >-
      The couple's branches of `_owner` and `_merged` (non-guest actor) are untested.
    evidence: |-
      Blind review. They serve the couple's mount (AD-7); Story 4.4 mounts the form for the couple and must test them.
    location: >-
      wedding/rsvp/views.py
    severity: low
  - summary: >-
      Two household members with the same name cannot be told apart on the form.
    evidence: |-
      Blind review. No seed household has duplicates; the household-editing story should warn or require distinct names.
    location: >-
      wedding/rsvp/templates/rsvp/step.html
    severity: low
  - summary: >-
      The RSVP form CSS uses raw px values next to the spacing tokens.
    evidence: |-
      Blind review. Values follow DESIGN.md Form step; mapping them to tokens joins the Impeccable pass (epic 1 retro action 8).
    location: >-
      static/css/site.css
    severity: low
  - summary: >-
      `Settings.rsvp_deadline = date.max` makes `is_past_deadline` overflow.
    evidence: |-
      Edge-case review. No form can set the deadline yet; the settings-editing story should validate the date.
    location: >-
      wedding/rules/deadline.py
    severity: low
  - summary: >-
      The CSRF 403 re-render is still a POST response, so Back to it asks for a resubmission.
    evidence: |-
      Orchestrator, after the PRG fix for invalid «Fortsett». Rare (expired token or blocked cookies) and the page holds nothing the guest loses; revisit if usability tests meet it.
    location: >-
      wedding/rsvp/views.py
    severity: low
---

<intent-contract>

## Intent

**Problem:** The RSVP sheet has no button and `/<code>/svar/` is not routed. There is no step machinery, no draft cookie and no deadline function, so no later Epic 2 story can build on anything (FR-12, FR-13, FR-14 step 1, FR-22, FR-41, AD-7, AD-8, AD-11). Two Epic 1 retro fixes are routed here: guest read views accept POST, and guest responses may be cached (deferred-work, B6/B7).

**Approach:** Build the one RSVP form in `wedding/rsvp/`: a step registry, a signed draft cookie, step 1 «Hvem kommer?» with server validation, PRG, the error summary, «Bytt», and a CSRF-failure re-render. The later steps (2.2–2.5) and the check page are routed now as empty step frames, so «Fortsett» has somewhere real to go. Add `is_past_deadline` and `form_steps` in `wedding/rules/`, the front-page button, the closed page after the deadline, `@require_safe` + `never_cache` on guest views, and a few small deferred tidy-ups that touch the same files.

## Boundaries & Constraints

**Always:**
- **Rules (pure, AD-2):** `wedding/rules/deadline.py` `is_past_deadline(deadline: date, now: datetime) -> bool`. It is True from 00:00:00 Europe/Oslo on the day after `deadline` (use `zoneinfo`). It raises `ValueError` for a naive `now` (FR-41, AD-11). `wedding/rules/form_steps.py`: `STEP_KEYS = ("who", "days", "overnight", "meals", "allergies", "hike")`. `form_steps(attendance: Sequence[bool] | None) -> tuple[str, ...]` returns all six for `None` (step 1 not completed: everyone, whole weekend, so the hike counts), and also when anyone is coming (days are unknown until 2.2, so it assumes the whole weekend). It returns `("who",)` when nobody is coming. `step_position(steps, key) -> tuple[int, int]` gives (n, m). `next_step(steps, key) -> str | None` returns `None` for the check page. `previous_step(steps, key) -> str | None` returns `None` before step 1. Story 2.2 extends `form_steps` with days.
- **Registry** `wedding/rsvp/steps.py`: each key has a slug and a Norwegian name: who `""` «Hvem kommer», days `dager` «Dager», overnight `overnatting` «Overnatting», meals `maltider` «Måltider», allergies `allergier` «Allergier og matbehov», hike `fjelltur` «Fjelltur fredag». The check page is `CHECK_SLUG = "se-over"`. Step 1 lives at `/<code>/svar/` and the others at `/<code>/svar/<slug>/`. A `FormMount(base_path, cookie_path, exit_url)` builds the addresses. For guests it is `/<code>/svar/`, `/<code>/` and `/<code>/#svar`; the couple's mount comes in 4.4.
- **Draft** `wedding/rsvp/draft.py` (AD-8): cookie `rsvp_draft`, value `signing.dumps(payload, salt="wedding.rsvp.draft", compress=True)`. Payload: `{"v": 1, "started": ISO UTC, "rev": household.revision, "resp": guest id, "att": {"<guest id>": true|false}, "done": [step keys]}`. Set with `httponly=True`, `samesite="Lax"`, `secure=settings.IS_PRODUCTION`, `path=mount.cookie_path` and `max_age` 90 days (a backstop only: the server decides with the deadline function). A draft is broken, and gets deleted with the same path and the form starts empty with no server error, when any of these holds: bad signature, payload not zlib, not JSON, `v` != 1, wrong types, `resp` or an `att` key not in the household, or an unknown `done` key. (2.9 later drops changed members instead of deleting.) The draft is never written before the first «Fortsett» or «Velg».
- **Step 1** (FR-12–FR-14, FR-22, UX-DR16, UX-DR18, UX-DR19). One paper sheet with a `<form method="post" novalidate>` and `{% csrf_token %}`. In order: `h1` «Hvem kommer?», then `p` «Steg n av m: Hvem kommer», then the respondent line «Jeg er <strong>name</strong> · Bytt», then one `fieldset` per member (in id order, legend = name) with radios «Kommer»/«Kommer ikke». Nothing is checked unless the draft holds it. Then «Fortsett» (primary `button`) above «Tilbake» (secondary link to the previous address). Title «Steg n av m: Hvem kommer – Invitasjon». No nav bar; the footer band is kept. No `<script>`.
- **Errors:** an unanswered or forged value on «Fortsett» saves the valid posted choices to the draft (without marking step 1 done) and redirects with 303 to the step's address with `?feil=1` (PRG, amended 2026-11-21, see Spec Change Log). A GET with `?feil=1` shows an error for every member without a saved answer; with none missing it shows the step without errors. The title gets the prefix «Feil: ». At the top of the sheet is an error summary: an error notice with `tabindex="-1"`, `autofocus`, heading «For å gå videre må du rette opp følgende feil.» and one link per error, «Velg om <name> kommer», pointing to that person's first radio `id`. Inside the fieldset, under the legend, is an error line (icon + «Feil: Velg «Kommer» eller «Kommer ikke» for <name>.»), referenced by the fieldset's `aria-describedby`, and the radios get `aria-invalid="true"`.
- **Valid «Fortsett»** (`action` missing or `continue`): write the draft (keep `started`/`rev` if it exists, else now/current revision), replace `att` for every member, add `"who"` to `done`, then 302 to `next_step`'s address (check page when nobody comes). Nothing is written to the database (AD-7, AD-8).
- **«Bytt»** (households of 2+ only). Markup: `<details>` + `<summary>Bytt<span class="visually-hidden"> hvem som svarer</span></summary>`, which exposes button role and expanded state natively without JS. Inside: a fieldset with legend «Hvem svarer?», one radio `respondent` per member (the current one checked) and a secondary submit `name="action" value="switch"` «Velg» (godkjent av Rikke 2026-11-23). On `switch`: set `resp` if the id is a member (else unchanged), merge every posted valid `att` value into the draft without validating and without marking `done`, then 302 to the same step. On «Fortsett» a valid posted `respondent` is applied too. Default respondent = the link owner (FR-12).
- **Step frames** (2.2–2.5 replace them). GET renders `h1` = the name, the progress line, the respondent line with Bytt and «Tilbake». The check frame renders `h1` «Se over svaret før du sender» and «Tilbake» only. Any frame redirects to step 1 when `"who"` is not in `done`, and a step not in `form_steps` redirects to the next applicable address. A POST to a frame handles only `switch`; anything else redirects to the same address.
- **Deadline:** every `/svar/` route (GET and POST) checks `is_past_deadline(settings.rsvp_deadline, timezone.now())` first. When it has passed, it renders `guests/rsvp_closed.html` (extends `error_page.html`, 200, writes nothing): heading «Svarfristen har gått ut», message «Fristen gikk ut {{ deadline|date:"l j. F Y" }} kl. 23:59. Send oss en melding, så finner vi ut av det.» (godkjent av Rikke 2026-11-23), the back button and the footer phones. The front-page locked states are Story 4.3.
- **CSRF on a step** (UX-DR52): `guests.views.csrf_failure` resolves `request.path_info`. For a POST to `guests:rsvp`/`guests:rsvp_step` with a resolving code and an open deadline, it re-renders that step with the posted valid choices pre-checked and no field errors. At the top is an error notice (focused like the summary): «Skjemaet ble ikke sendt. Det skjer når siden har stått åpen lenge, eller når nettleseren ikke tar imot informasjonskapsler. Det du fylte ut, står her fortsatt. Prøv igjen.» (godkjent av Rikke 2026-11-23). Status 403, no draft cookie written, and a fresh token in the page. Any exception falls back to the current generic page.
- **Guest views:** `rsvp` and `rsvp_step` in `guests/views.py` are thin. They call `resolve_code` first (an unknown code gives G1 404 after exactly 1 query), then `site_settings()`, the deadline check, `household_members`, then `wedding.rsvp.views`. They are decorated with `never_cache`, `sensitive_post_parameters()` and `require_http_methods(["GET", "HEAD", "POST"])`. GET and POST each run 3 SELECTs and no other query. `front_page` and `info_page` get `@require_safe` + `@never_cache`; `csrf_failure` gets `@never_cache` (deferred B6/B7).
- **Front page:** after the RSVP sheet's deadline line, `<a class="button" href="{% url 'guests:rsvp' code %}">Svar på invitasjonen</a>`. It is shown for every household in 2.1 (Story 2.8 swaps it for the status block, and Story 4.3 adds the after-deadline state).
- **CSS** (`static/css/site.css`, a new «RSVP form» section with DESIGN tokens): form sheet, progress line, respondent line + details panel, `fieldset` without a border, `.choice` rows (whole row clickable, ≥ 44px, native radio 26px with `accent-color: var(--color-green-dark)`), field error line (22px icon, error colour), error summary (notice + list, links ≥ 44px), actions (column, 12px gap, 24px top margin, both full width). Every new breakpoint is in em, and the layout must hold at 180 CSS px and at 20px default text.
- Every new rule, view, template comment and test names its FR/NFR/UX-DR/AD ids. UI text is Norwegian; code is English.

**Never:** no session or messages use, and no database row before send (no model or migration in 2.1). No hidden fields carrying answers. No JavaScript. No days/overnight/meals/allergies/hike questions (2.2–2.5), no draft notice or offer (2.9), no send (2.6a), no answered-household redirect (2.8), no locked front page (4.3). No hard-coded names, prices or dates in code or templates: names come from `household_members`, the deadline from `site_settings`. No calls named `save`/`delete`/`create`/`update`/`bulk_*` outside `wedding/services/`, including `dict.update` (`tests/test_only_services_write.py` flags the method name on any receiver). No px breakpoints. Don't run a browser (the orchestrator runs the MT rows).

## I/O & Edge-Case Matrix

Seeded; S = `test-sigmund0000000000` (household Sigmund + bestemor), A = Arild's code (4 people), Y = Synne's code (1 person), U = unknown code. Names come from `seed.toml` in tests.

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Open step 1 | GET `/S/svar/`, no cookie | 200, «Steg 1 av 6: Hvem kommer», «Jeg er Sigmund», 2 fieldsets, no `checked`, Bytt present; no `rsvp_draft` set; 3 SELECTs | — |
| One person | GET `/Y/svar/` | no `<details`/«Bytt» | — |
| Unknown code | GET/POST `/U/svar/`, `/U/svar/dager/` | G1 404, 1 query | — |
| Missing answer | POST S Sigmund=coming only, then follow the redirect | 303 to `/S/svar/?feil=1` with the draft (att Sigmund=true, `done` empty); the GET: title «Feil: Steg 1 av 6…», summary with 1 link to bestemor's first radio, error under her legend, Sigmund still checked | field error |
| Forged value | POST value `maybe` or an id from another household | same as missing; foreign id ignored | field error |
| Valid, someone comes | POST both answered | 302 → `/S/svar/dager/`; cookie path `/S/`, HttpOnly, SameSite=Lax, not Secure locally; payload `done=["who"]` | — |
| Valid, nobody comes | POST A all «Kommer ikke» | 302 → `/A/svar/se-over/`; revisiting step 1 shows «Steg 1 av 1» | — |
| Back | GET `/S/svar/` after valid POST | both radios checked as saved, «Steg 1 av 6» | — |
| Bytt | POST `action=switch`, respondent=bestemor, Sigmund=coming | 302 → `/S/svar/`; «Jeg er bestemor»; Sigmund checked; `who` not done | foreign respondent id → unchanged |
| Frame early | GET `/S/svar/dager/` without `who` done | 302 → `/S/svar/` | — |
| Broken draft | bad signature / signed non-zlib / `v: 0` / foreign `resp` | 200 empty step 1, cookie deleted (`max-age=0`, path `/S/`) | no 500 |
| After deadline | deadline = yesterday (`update_settings` with SYSTEM in the test), GET and POST `/S/svar/` and `/S/svar/dager/` | 200 «Svarfristen har gått ut», weekday-date line, back button, `tel:` rows; no draft cookie written | — |
| Deadline boundary | `is_past_deadline(d, …)` | 23:59:59.999999 Oslo → False; next day 00:00:00 → True; winter → 23:00Z, summer → 22:00Z, also on 2028-03-26 and 2028-10-29 | naive `now` → ValueError |
| CSRF | `Client(enforce_csrf_checks=True)` POST `/S/svar/` without token, Sigmund=coming | 403, h1 «Hvem kommer?», Sigmund checked, «Prøv igjen», no `rsvp_draft`; re-POST with the page's token → 302 | fallback generic page on error |
| Read views | test-client POST `/S/`, `/S/program/` | 405 | — |

</intent-contract>

## Code Map

- `guests/views.py:1-15` docstring; `:87-94` `_not_found` (rename `_unknown_link`, deferred tidy-up), `:171` `NOT_FOUND` (→ `PAGE_NOT_FOUND`); `:97-109` `_guest_context` (contacts, deadline); `:112-128` `front_page`, `:142-159` `info_page` (add decorators); `:177-200` `_reachable`, `:217-224` `csrf_failure` (add the step re-render branch before the generic render).
- `guests/urls.py:25-31` -- add `path("<str:code>/svar/", views.rsvp, name="rsvp")` and `path("<str:code>/svar/<str:slug>/", views.rsvp_step, name="rsvp_step")` (an unknown slug → `Http404` → «Vi finner ikke denne siden»). Update the docstring. `config/urls.py:1-21` docstring.
- `guests/templates/guests/front_page.html:16` comment, `:148-161` RSVP sheet. `guests/templates/guests/error_page.html` -- frame for `rsvp_closed.html` (`code`, `contacts` in context).
- `wedding/rsvp/__init__.py` -- docstring. New: `steps.py`, `draft.py`, `forms.py` (`WhoIsComingForm(members)` with fields `attendance_<id>`), `views.py` (`handle_step(request, *, actor, mount, members, step, page_context)`, `render_after_csrf_failure(...)`), `templates/rsvp/step.html`, `templates/rsvp/check_frame.html`, and includes for the respondent line and error summary.
- `config/settings.py:85-98` -- `TEMPLATES["DIRS"] = [BASE_DIR / "wedding" / "rsvp" / "templates"]` (the Structural Seed puts form templates in `wedding/rsvp/`); `:31` `IS_PRODUCTION`; `:46-58` INSTALLED_APPS (pin the `runserver_nostatic` order, deferred B8).
- `wedding/selectors.py:87-94` `household_guest_names` -- add `household_members(household) -> list[tuple[int, str]]` beside it (one SELECT, id order). `:38-44` `site_settings`, `:47-66` `footer_contacts`.
- `wedding/rules/households.py` -- pattern for docstrings; `wedding/rules/__init__.py` purity note (`zoneinfo` is stdlib, allowed). `wedding/links.py:201-213` `resolve_code`. `wedding/services/settings.py:52` `update_settings(SYSTEM, …)` to move the deadline in tests.
- `wedding/templates/wedding/components/notice.html` (include with `only`), `footer-band.html`, `base.html` (blocks `title`, `content`).
- `static/css/site.css:337-341` focus ring (covers `input`, `summary`), `:349-425` buttons, `:439-475` notice, `:514` `.visually-hidden`, `:850-880` RSVP sheet, `:934-935` bottom buttons; px breakpoints at `:1219`, `:1242`, `:1248` stay (allowlisted, routed below).
- Tests: `tests/test_front_page.py:155-160` and `tests/test_error_pages.py:347-351` (duplicate `_row_counts` → `tests/helpers.py`); `tests/test_front_page.py:280-296` asserts no `/svar/` (update); `tests/test_error_pages.py:129` (`/U/svar/` 404 with 1 query, stays green), `:262-273` CSRF on `/S/` (stays 403); `tests/test_guest_privacy.py:110-171` headers and the middleware-order test; `tests/conftest.py` `seeded`; `tests/test_only_services_write.py:18-27`; `tests/test_rules_purity.py`.
- Docs: `docs/manual-test-plan.md:38` (last row MT-22); `README.md:9` status, `:152-193` tree (`:193` says `rsvp/` is empty); `ARCHITECTURE-SPINE.md` AD-7 (`:119`), AD-8 (`:130`), AD-11 (`:164`), Structural Seed (`:287`); `DESIGN.md:575-581`, `:682`, `:686`; `EXPERIENCE.md:128`, `:201`, `:235`; `.docs/implementation-artifacts/deferred-work.md:74`, `:89-91`, `:101-103`, `:109-111`.

## Tasks & Acceptance

**Execution:**
- [x] `wedding/rules/deadline.py`, `wedding/rules/form_steps.py` -- the rules per Boundaries, with docstrings (FR-14, FR-41, AD-11, UX-DR19).
- [x] `wedding/selectors.py` -- `household_members`.
- [x] `config/settings.py` -- the template `DIRS` with a comment (AD-7).
- [x] `wedding/rsvp/{__init__,steps,draft,forms,views}.py` + `wedding/rsvp/templates/rsvp/*` -- the registry, draft, step 1, Bytt, frames, CSRF re-render.
- [x] `guests/views.py`, `guests/urls.py`, `config/urls.py` -- `rsvp`, `rsvp_step`, decorators, the `csrf_failure` branch, renames, docstrings. `guests/templates/guests/rsvp_closed.html` -- the closed page.
- [x] `guests/templates/guests/front_page.html` -- the button; update the comment.
- [x] `static/css/site.css` -- the RSVP form section.
- [x] `tests/helpers.py` -- move `_row_counts` as `row_counts()`; use it in test_front_page/test_error_pages.
- [x] `tests/test_deadline.py`, `tests/test_form_steps.py` -- table-driven rule tests (both sides of the boundary, both DST change days, naive `now`; `form_steps` for None/some/none coming over every seed household shape; `step_position`/`next_step`/`previous_step`).
- [x] `tests/test_rsvp_draft.py` -- round trip, cookie attributes (Secure only with `IS_PRODUCTION`), every broken case → deleted + empty step, no 500.
- [x] `tests/test_rsvp_who_is_coming.py` -- every matrix row. Add a full flow (GET, invalid POST, valid POST, frame, switch) that asserts: row counts unchanged, `Session` count 0, no `sessionid`/`messages` cookie, `messages.add_message` never called (monkeypatched to fail), no `<script` in any step, 3 SELECTs per request, and `Cache-Control` has `private` and `no-store` on every response.
- [x] `tests/test_guest_privacy.py` -- next to the header tests: `Cache-Control` private/no-store on the front page, the three info pages, step 1 and the step redirect; POST → 405 on `/S/` and each info page; `whitenoise.runserver_nostatic` comes before `django.contrib.staticfiles` in `INSTALLED_APPS`.
- [x] `tests/test_front_page.py` -- the RSVP button test replaces «no `/svar/`» (href `/S/svar/`, class `button`, after the deadline line, no `<button`).
- [x] `tests/test_form_components.py` -- the form CSS (26px radio, `accent-color`, row `min-height` 44px, group border none, actions gap/margin), and every `@media`/`@container` width in `site.css` is in em except the allowlisted `339.98px`, `299.98px`, `259.98px` (the new components get their own file, as the deferred tidy-up asked).
- [x] `docs/manual-test-plan.md` -- add Norwegian rows with empty date/result cells, each with «Kjøres av Claude med Playwright mot Edge» (`channel: 'msedge'`). Server: `uv run manage.py seed_testdata`, then `uv run manage.py runserver`. Measure after `document.fonts.ready`.
  - **MT-1 (2.1):** follow README's «Svarskjemaet»: open `http://127.0.0.1:8000/test-sigmund0000000000/`, click «Svar på invitasjonen» → step 1.
  - **MT-23 (a real submission):** on Sigmund's link, click «Svar på invitasjonen» → URL `/svar/`, title «Steg 1 av 6: Hvem kommer – Invitasjon», 0 `input:checked`. Pick «Kommer» for Sigmund and click «Fortsett» → URL `/svar/?feil=1`, title starts «Feil: », `document.activeElement` is the error summary, 1 summary link. Click it → focus on bestemor's first radio. Pick «Kommer» for both and click «Fortsett» → URL `/svar/dager/`, text «Steg 2 av 6: Dager». `page.goBack()` → both «Kommer» checked, and no `dialog` event fired. The `rsvp_draft` cookie has `path` `/test-sigmund0000000000/`, `httpOnly` true, `sameSite` `Lax`. Open «Bytt», pick bestemor, click «Velg» → «Jeg er bestemor». On Synne's link `test-synne000000000000` there is no «Bytt». On Arild's link with all four «Kommer ikke» → URL `/svar/se-over/`.
  - **MT-24 (keyboard only):** use only `page.keyboard` (Tab/Shift+Tab/Space/arrows/Enter). Fill step 1 for Sigmund and reach `/svar/dager/`. Open «Bytt» with Enter (`details.open` true), switch to bestemor and «Velg». Every focused element has `outline-style` `solid`, and the order is: summary of «Bytt», Sigmund's group, bestemor's group, «Fortsett», «Tilbake», the `tel:` links.
  - **MT-25 (layout):** step 1 for Arild, normal and in the error state, at 360 × 640 and 180 × 320, and in a context with a 20px default font size (CDP `Page.setFontSizes` `{ fontSizes: { standard: 20 } }`) at 360 × 640 and 320 × 568. Expected: `scrollWidth` ≤ `innerWidth`; each `.choice` row ≥ 44px tall and inside the sheet; radios 26 × 26 at the default size; «Fortsett» is above «Tilbake» with ≥ 12px between them and the same width; each summary link ≥ 44px tall.
  - **MT-26 (CSRF in the browser):** on step 1 pick «Kommer» for Sigmund, run `context.clearCookies({ name: 'csrftoken' })`, click «Fortsett» → status 403, h1 «Hvem kommer?», Sigmund still «Kommer», the notice holds «Prøv igjen». Pick bestemor and click «Fortsett» → `/svar/dager/`.
- [x] `README.md` -- status (2.1), a short section «Svarskjemaet» (open a test link, click «Svar på invitasjonen»; only step 1 is built, the rest are frames until 2.2–2.5; the deadline is 30 days ahead), tree lines for `wedding/rsvp/` and its templates, and remove «Mappen `rsvp/` er tom».
- [x] `ARCHITECTURE-SPINE.md` -- dated notes (2026-11-21, Story 2.1): AD-7 step addresses and slugs, with step 1 at `/<code>/svar/`; AD-8 cookie name `rsvp_draft`, format `v: 1`, 90-day backstop; AD-11 the function is `is_past_deadline` in `wedding/rules/deadline.py`; Structural Seed: rsvp templates through `TEMPLATES["DIRS"]`.
- [x] `DESIGN.md:686` and `EXPERIENCE.md:128,201` -- dated notes: «Bytt» is a `<details>`/`<summary>` (works without JS) with «Velg» **[forslag]**. `EXPERIENCE.md:235` and the states table: the closed page and the CSRF-on-step notice wording **[forslag]**.
- [x] `.docs/implementation-artifacts/deferred-work.md` -- mark done: `:89-91` (require_safe/Cache-Control), `:101-103` (runserver_nostatic test), `:74` (decided: the 400 stays impersonal, because the step forms are urlencoded with fewer than 20 fields, so only a forged request can trip `RequestDataTooBig`/`TooManyFieldsSent`), and the `:109-111` parts done here (rename, `_row_counts`, form tests in their own file). Add a new entry: convert the three px breakpoints (`site.css:1219,1242,1248`) to em, re-measured at 20px, in the Impeccable pass (retro action 8) or the next story touching them.

**Acceptance Criteria:**
- Given the repo, when `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `uv run djlint --check .` run, then all pass.
- Given any household before the deadline, when the front page renders, then the RSVP sheet has the primary link «Svar på invitasjonen» to `/<code>/svar/`, and the step opens with nothing selected (FR-14).
- Given the whole guest flow, when it runs without JavaScript in the test client, then it completes step 1, writes no database row and no session, and never uses messages (AD-1, AD-8).
- Given any guest response under `/<code>/`, when it is returned, then it carries `Cache-Control` with `private` and `no-store`, plus the existing `noindex` and `same-origin` headers (AD-15).
- Given `docs/manual-test-plan.md`, when read, then MT-1 (2.1) and MT-23 to MT-26 hold the steps above with empty date and result cells.

## Spec Change Log

- **2026-11-21 — invalid «Fortsett» uses PRG too.** Trigger: the orchestrator's MT-23 run in Edge: `page.goBack()` from `/svar/dager/` to the error page failed with `net::ERR_CACHE_MISS`, because that page was a POST response; the epic's AC says Back works without a resubmit prompt. Trying `Cache-Control: private, no-cache` and no cache headers on that response did not help, so the cause is the POST entry itself. Amended: the **Errors** rule (inside the intent contract, because it contradicted the story's own AC in epics.md, which wins), matrix row «Missing answer», and MT-23 (pick Sigmund before the first «Fortsett», as row 54 always meant: one summary link). Known-bad state avoided: a history entry that only a resubmission can restore. KEEP: the error summary, error lines, focus, «Feil: » title and texts are unchanged; only how the error page is reached changes. Applied as a review patch rather than a full re-derivation, because the change is confined to the invalid-POST branch. Godkjent av Rikke 2026-11-23 («punkt 1: ja»). The CSRF 403 re-render stays a POST response (rare, and it has nothing to resubmit that the guest would lose); noted in deferred-work.

## Review Triage Log

### 2026-11-21 — Review pass
- verdicts: 34 findings — high 1, medium 7, low 15, false 11, maybe-false 0
- findings:
  - `[medium]` `[patch]` `@never_cache` on `csrf_failure`, `page_not_found` and `server_error` is asserted by no test, though the 403 step re-render shows names and choices (verification-gap) — `Cache-Control` private/no-store asserted on the CSRF re-render and in `_assert_private_headers` for every error page.
  - `[low]` `[patch]` A new draft's `rev` is only tested against revision 0 (verification-gap) — test sets the household revision to 3 and asserts the new draft carries it.
  - `[low]` `[patch]` A CSRF failure on «Velg» with a posted respondent is untested (verification-gap, other) — test added.
  - `[false]` `[reject]` Focus, Back without a prompt and Enter behaviour are only checked in markup (intent-alignment) — MT-23, MT-24 and MT-26 were run in Edge; they found the Back defect below, which is fixed and re-run.
  - `[false]` `[reject]` The CSRF re-render returns 403 rather than 200 (intent-alignment) — the AC names no status; 403 is the spec's recorded choice, marked [forslag] in EXPERIENCE.md.
  - `[false]` `[reject]` «Bytt» records the respondent only in the draft (intent-alignment) — AD-8: nothing is stored until 2.6a sends the answer.
  - `[false]` `[reject]` A view-level deadline test depends on `TIME_ZONE` (intent-alignment) — `TIME_ZONE` is Europe/Oslo in settings, and the rule itself is tested in Oslo time on both DST days.
  - `[false]` `[reject]` The diff reaches guest read views, settings and error pages beyond the story's ACs (intent-alignment) — those are the deferred-work entries routed to 2.1 (B6/B7/B8), named in the spec.
  - `[false]` `[reject]` NFR-5/NFR-6/UX-DR17 have no AC of their own (intent-alignment) — NFR-5's 44px targets are measured in MT-25 (all rows ≥ 44px).
  - `[false]` `[reject]` Sprint status not updated (blind) — the finalize step.
  - `[false]` `[reject]` No session log (blind) — written in the log step of this run.
  - `[false]` `[reject]` MT rows not run while in review (blind) — run by Claude in Edge after review and recorded.
  - `[low]` `[defer]` No README/MT way to reach the closed page by hand (blind) — Story 4.3 builds the locked states after the deadline and its MT rows; routed there.
  - `[medium]` `[patch]` Enter inside a radio is only checked in markup (blind) — Claude pressed Enter on a focused radio in Edge; MT-24 gets the step.
  - `[medium]` `[patch]` A CSRF failure after the deadline shows the generic page, not the closed page (blind) — `_rsvp_after_csrf_failure` renders the closed page after the deadline, with a test.
  - `[medium]` `[patch]` The draft's 90 days are only enforced by the browser (blind) — `signing.loads(..., max_age=MAX_AGE)`, with a test.
  - `[low]` `[patch]` Member-id set rebuilt five times and the CSRF path keeps a broken draft (blind) — one helper; the CSRF re-render deletes a broken draft.
  - `[low]` `[defer]` Summary text, yes/no values and the step-1 question are spread over views, forms and templates (blind) — the questions of steps 2–6 arrive in 2.2–2.5; a `question` field in the registry belongs with them.
  - `[low]` `[defer]` The non-guest branches of `_owner`/`_merged` are untested (blind) — they are the couple's mount (AD-7, FormMount in the spec); Story 4.4 mounts and tests them.
  - `[low]` `[defer]` Two members with the same name are indistinguishable (blind) — pre-existing data rule: the couple sets names; no seed household has duplicates; routed to the household-editing story.
  - `[low]` `[defer]` New form CSS mixes raw px with spacing tokens (blind) — the values follow DESIGN.md › Form step; mapping to tokens joins the Impeccable pass (retro action 8).
  - `[low]` `[reject]` README Status paragraph is long (blind) — readable, and a README restructure is not this story's; no user harm.
  - `[medium]` `[patch]` CSRF failure after the deadline shows the generic page (edge-case) — same as the blind row above.
  - `[low]` `[patch]` An unknown slug after the deadline gives 404, not the closed page (edge-case) — the 404 is right for an address that does not exist; the AD-11 note and `guests/urls.py` docstring now say «every step address».
  - `[medium]` `[patch]` The server never expires a draft (edge-case) — same as the blind max_age row.
  - `[low]` `[patch]` `started` may lie in the future (edge-case) — a `started` more than a minute ahead is a broken draft, with a test.
  - `[low]` `[defer]` `Settings.rsvp_deadline = date.max` overflows (edge-case) — no form can set that date yet; validating the deadline belongs to the settings-editing story.
  - `[false]` `[reject]` «Velg» after step 1 is done merges unvalidated attendance (edge-case) — only the valid values `yes`/`no` of known members are merged, so every member still has a valid answer and the steps follow it.
  - `[false]` `[reject]` «Fortsett» applies a respondent chosen in a closed «Bytt» (edge-case) — spec decision («Fortsett» also applies a changed respondent); the radios are only reachable with «Bytt» open.
  - `[low]` `[patch]` The CSRF re-render keeps a broken draft (edge-case) — same as the blind helper row.
  - `[low]` `[patch]` `bad_request` has no `never_cache`; the APPEND_SLASH 301 has no Cache-Control (edge-case, claim) — `bad_request` gets `@never_cache`; the 301 carries no content, so the claim is narrowed to pages in the spec's AC.
  - `[medium]` `[patch]` Claim: every `/svar/` address shows the closed page after the deadline (edge-case, claim) — same as the deadline rows above.
  - `[high]` `[patch]` [orchestrator] Back after an invalid «Fortsett» fails with `net::ERR_CACHE_MISS` in Edge (the resubmit prompt the AC forbids) — the error page was a POST response; tested with no-cache and with no cache headers, both still failed. An invalid «Fortsett» now saves the valid choices to the draft and redirects (303) to `/svar/?feil=1`, which shows the errors for unanswered members; Back works. Spec amended (Change Log).
  - `[low]` `[patch]` [orchestrator] MT-23 says «Fortsett» with nothing chosen gives one summary link; it gives two (spec row 54 picks Sigmund first) — MT-23 now picks «Kommer» for Sigmund before the first «Fortsett».

## Design Notes

- **Why frames:** «Fortsett» must land on a real next step address (MT-23), and building days early would take over 2.2. The frames are the shared step template with no fields, so 2.2–2.5 replace content, not code paths.
- **Why `<details>` for «Bytt»:** AD-1 requires no-JS; `summary` gives the button role and expanded state that EXPERIENCE asks for, and AD-7 already uses `<details>` for «Les mer». Typed answers survive a switch, because `switch` merges the posted choices into the draft before the redirect (PRG, no resubmit prompt).
- **Why autofocus:** it focuses the error summary and the CSRF notice without a script; both have `tabindex="-1"`.

## Verification

**Commands:**
- `uv run pytest` -- expected: all green, including the existing `test_error_pages.py` and `test_private_invitation.py` unchanged in behaviour.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.
- `uv run djlint --check .` -- expected: no findings.

## Auto Run Result

Status: done

**Summary:** The front page has «Svar på invitasjonen», and `/<code>/svar/` is step 1 «Hvem kommer?»: one Kommer/Kommer ikke group per household member, nothing preselected, «Jeg er … · Bytt» (a `<details>` with «Velg»), server validation with a focused error summary, and PRG to the next applicable step for valid and (after review) invalid answers. Answers between steps live only in the signed `rsvp_draft` cookie (no session, no rows); steps 2–6 and the check page are routed frames that Stories 2.2–2.5 fill. `is_past_deadline` (Oslo midnight) closes every step address with a closed page. Guest read views got `@require_safe`, and guest and error pages `Cache-Control: private, no-store`.

**Files changed:**
- `wedding/rules/deadline.py`, `wedding/rules/form_steps.py` — the deadline and step rules.
- `wedding/rsvp/{steps,draft,forms,views}.py`, `wedding/rsvp/templates/rsvp/*` — the form, draft cookie and step templates.
- `guests/views.py`, `guests/urls.py`, `config/urls.py`, `config/settings.py`, `guests/templates/guests/{front_page,rsvp_closed}.html`, `wedding/selectors.py`, `wedding/templates/wedding/components/{notice,state-icon}.html`, `static/css/site.css`.
- Tests: `test_deadline.py`, `test_form_steps.py`, `test_rsvp_draft.py`, `test_rsvp_who_is_coming.py`, `test_form_components.py`, plus helpers, privacy, front-page and error-page tests.
- `README.md`, `docs/manual-test-plan.md`, `ARCHITECTURE-SPINE.md`, `DESIGN.md`, `EXPERIENCE.md`, `deferred-work.md`, `epic-2-context.md`.

**Review:** 34 findings — 16 patched, 6 deferred, 12 rejected (plus one orchestrator deferral). The high one came from the browser: Back after an invalid «Fortsett» failed with `net::ERR_CACHE_MISS`; fixed with PRG to `/svar/?feil=1` and a Spec Change Log entry.

**Follow-up review recommendation:** false. The one high was a behaviour defect re-verified in Edge after the fix (Back works, 0 dialogs), and the patched mediums are each pinned by new tests.

**Verification:** `uv run pytest` 840 passed; ruff and djlint clean; MT-1 (2.1), MT-23, MT-24 (incl. Enter in a radio), MT-25 (360/180px and 20px text, normal and error state) and MT-26 run by Claude with Playwright in Edge 158 after the patches.

**Residual risks:** the spec's Errors rule inside the intent contract was amended (logged) because it contradicted the story's Back-button AC; the CSRF 403 page is still a POST response; the closed-page, «Velg» and CSRF wording were [forslag] and are now godkjent av Rikke 2026-11-23 («Punkt 2: ja»).
