# Epic 2 Context: Guests answer for their household

<!-- Generated from planning artifacts. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Let one person answer the invitation for their whole household on a phone, step by step, without help: who is coming, which days, overnight stay and meals with prices and a running total, allergies with per-person consent, and the Friday hike. The guest checks everything before sending, gets a receipt in Rikke's words with how to pay now or later, and later sees the household's status on the invitation. An interrupted answer is kept on the guest's own phone and offered back. The epic is part of the T1 usability-test build, and its saved answers are what the couple's numbers in Epic 3 count.

## Stories

- Story 2.1: Start the answer: who is coming
- Story 2.2: Which days each person comes
- Story 2.3: Overnight stay, meals and the running total
- Story 2.4: Allergies and consent
- Story 2.5: The Friday hike and the check page
- Story 2.6a: Send the answer
- Story 2.6b: Allergies are stored only with consent
- Story 2.6c: A send that fails or repeats is safe
- Story 2.6d: Test data with answers, and a real-browser send
- Story 2.7: The receipt and how to pay
- Story 2.8: The household's status on the invitation
- Story 2.9: An interrupted answer is kept on the phone

## Requirements & Constraints

- **Respondent:** the form says «Jeg er <name>», preset to the link's owner; in a household of more than one, «Bytt» picks another member, and that person is recorded as the sender. Switching never changes answers already filled in.
- **Steps:** one task per step, each with its own address, a visible «Tilbake», and a progress line «Steg n av m: <name>». Order: who is coming → whole weekend or days per person → overnight → meals → allergies and consent → Friday hike (only if someone comes Friday) → check page. Before step 1 is answered, m counts every step as if everyone comes all weekend; afterwards it follows the answers, and moving forward or back never changes it.
- **Choices:** attendance starts with nothing selected. A person's days must follow each other (no Friday + Sunday without Saturday). Overnight needs two or more days in a row; a cabin is booked and paid for the whole weekend. Paid meals are Friday dinner, Saturday breakfast (only if present Friday and Saturday) and Sunday breakfast; Saturday lunch and dinner are not asked. Contradictions are blocked with an explanation. When a person stops coming or a day is removed, their later choices are removed and never count.
- **Errors:** server-validated; a failed step redirects to its own address with `?feil=1` (POST-redirect-GET, so Back never asks to resubmit), the valid choices kept in the draft, the error next to the field («Feil: …»), and a focused error summary at the top linking to each field; the page title starts with «Feil: ». A step that fails the CSRF check is shown again with status 403, the posted choices kept and a focused error notice.
- **Money:** prices shown before choosing, with a short note on why guests pay; the household total is visible along the way, identical on check page and receipt, always computed from answers and current prices, whole kroner.
- **Allergies and consent:** fixed categories plus a note of at most 200 characters, or «Ingen allergier eller matbehov» (exclusive per person); optional. Stored only with a per-person Ja/Nei consent that starts unanswered; answering for others requires «Jeg bekrefter at <name> vet om dette og er enig». Sending never requires consent; without it the form says the allergy information will not be saved. Consent is recorded per person with who, when and the consent-text version.
- **Deadline:** guests can answer until 23:59:59 Oslo time on the deadline date; after that the form does not open and sends are refused, with the deadline and the couple's phone numbers shown.
- **Send and receipt:** the check page says the answer is not sent yet and has «Send svaret»; the receipt confirms with a coming/not-coming message by the du/dere rule, the summary and total, and «Betal nå» / «Betal senere» when something is owed. Afterwards the invitation shows a status block instead of the RSVP button, and `/<code>/svar/` leads there until changing answers is built (Epic 4).
- **Reliability:** a save either succeeds and says so, or fails clearly and keeps everything entered; a double tap, a changed price or a parallel send by another household member never loses or doubles an answer.
- **Accessibility and tone:** WCAG 2.2 AA, guest text ≥ 18px, works at 320px width and 200 % zoom (180 CSS px) and with a larger default text size, full keyboard use, touch targets ≥ 44px, every field labelled, plain warm Norwegian bokmål. An older guest completes a household answer alone in under 10 minutes.

## Technical Decisions

- **One server-rendered form:** everything works without JavaScript; scripts only enhance. Each step is a plain HTML POST, validated by the server, then POST-redirect-GET to the next applicable step. The form lives in `wedding/rsvp/` (steps, forms, templates, draft) and is mounted at `/<code>/svar/` for guests and, later, under `/admin/` for the couple's override with the actor passed in. The only fragment endpoint is the running total, `POST /<code>/svar/sum/`, which writes nothing.
- **Draft cookie:** between steps, answers live only in a cookie made with `signing.dumps(..., compress=True)`, `HttpOnly`, `SameSite=Lax`, `Secure` in production, scoped to `/<code>/` so the front page can see it. No session, hidden fields or database rows hold answers before send. It holds everything entered, the household revision it started from and when it started. A bad signature, failed decompression, old format or a draft that no longer matches the household is deleted and never causes a server error. A household is at most 8 people, and a full draft for 8 must fit in 4 KB. Guest views never touch `request.session` or the messages framework.
- **Rules:** pure functions in `wedding/rules/` with plain values and an explicit `now` decide applicable steps and days, totals (`household_total`), `normalise_answer`, allergy state, the derived payment message and `guest_balance`. Views, templates and services call them and never re-implement them. Every rule, service, view and test names its FR/NFR/AD in its docstring.
- **Deadline:** `USE_TZ`, `TIME_ZONE = "Europe/Oslo"`; one rule function, given the deadline date and `now`, decides whether the deadline has passed. It locks only guest sends that change answer content.
- **Writes:** only `wedding/services/` writes, one IMMEDIATE transaction per service, with an explicit actor; a guest service refuses ids outside the actor's household, with a test. `send_answer` creates `HouseholdAnswer` (sent by, with the name as text; sent at) and `PersonAnswer` (2.6a), `Allergy` and `Consent` (2.6b, `CONSENT_TEXT_VERSION` in `wedding/services/`), and `Submission` (2.6c). Derived values (totals, statuses) are never stored. `Household.revision` rises on each send; a draft started at an older revision is refused. A one-time submission id is checked before the revision; refused sends record no `Submission`.
- **Money:** every amount is an `int` of whole kroner; guest pages use only `guest_balance(total, report)` and never read payment rows.
- **Privacy:** guest responses send `noindex` and `Referrer-Policy: same-origin`; guest form views use `sensitive_post_parameters`; no names, codes or allergy content in logs. Errors under a valid link show the couple's phones. CSRF failures need a friendly result.
- **Quality:** Django forms with CSRF on every POST; one CSS file with the DESIGN.md tokens; every layout breakpoint in em; Ruff and djLint; seed data and expected results in TOML, seeded through `send_answer` with the system actor (2.6d).

## UX & Interaction Patterns

- Each form step is one paper sheet on the green page with no nav bar and the footer band kept: `h1` question → progress line → respondent line («Jeg er **Sigmund** · Bytt», «Bytt» a `<details>`/`<summary>` with accessible name «Bytt hvem som svarer» so it works without JavaScript, on every step) → one fieldset per person with the name as legend → running total on paid steps → «Fortsett» (primary) above «Tilbake» (secondary), full width.
- Choice control: native radio/checkbox, 26px, whole row ≥ 44px tappable; group error sits under the legend as icon + «Feil: …» with no border on the group. Error summary heading «For å gå videre må du rette opp følgende feil.».
- Notices: four variants, never auto-dismissing; a notice present at load is not a live region. Primary button busy state «Sender …».
- Check page: «Obs: Svaret er ikke sendt ennå.», `h1` «Se over svaret før du sender», one block per part with «Endre» (hidden context, e.g. «Endre måltider»), «Ikke oppgitt» for skipped answers, «Send svaret» above «Tilbake».
- Receipt and status block wording, the draft notice «Du har et svar som ikke er sendt ennå.» and the draft offer «Vil du fortsette der du slapp?» are in EXPERIENCE.md and the mockups `key-form-steps.html`, `key-check-page.html`, `key-receipt.html` and `answered-1.html`.

## Cross-Story Dependencies

- 2.1 builds the step machinery, draft cookie, deadline function and step 1; 2.2–2.5 add the later steps and the check page on it; 2.9 adds the draft notice and offer.
- 2.6a–2.6c add the models and `send_answer`; 2.6d seeds answers through it; 2.7 and 2.8 render what was sent.
- Epic 3 counts the sent answers against `expected.toml`. Epic 4 lifts the answered-household redirect (change answer), adds the deadline lock views and the couple's override mount. Epic 7 adds «Les mer» inside steps, the leave warning and consent withdrawal.
