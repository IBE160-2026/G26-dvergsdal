---
title: "Experience: AI'll handle it"
status: draft
created: 2026-11-10
updated: 2026-11-11
sources:
  - ../../prds/prd-aill-handle-it-2026-11-07/prd.md
  - ../../prds/prd-aill-handle-it-2026-11-07/addendum.md
  - ../../briefs/brief-aill-handle-it-2026-09-23/brief.md
  - ../../briefs/brief-aill-handle-it-2026-09-23/addendum.md
  - ../../research/user-voice-wedding-website-pre-prd-2026-11-06/research.md
  - ../../ux/inspirasjon/inspirasjon.md
  - ../../ux/stedet/stedet.md
---

# AI'll handle it — Experience Spine

> How the invitation and the admin area behave. Visual identity: [DESIGN.md](DESIGN.md); tokens are referenced by name, e.g. `{colors.page-green}`. Requirements (FR/NFR/UJ/SM) are in the [PRD](../../prds/prd-aill-handle-it-2026-11-07/prd.md) and not restated here. Decisions: [.memlog.md](.memlog.md). Renders: [mockups/color-themes-5.html](mockups/color-themes-5.html) (front page composition), [mockups/illustration-3.html](mockups/illustration-3.html) (hero order, I7). **The spines win on conflict with any render.** `[If time]` and `[2027]` follow PRD 3.2–3.3.

## Foundation

- **Form factor:** phone-first responsive web for all ages (NFR-6). A PC shows the phone layout in a centred column; a wider PC layout is [If time]. Links arrive by SMS, Messenger and email and open in the phone's browser or an in-app browser.
- **Two audiences, one visual system:** guests (about 70, many older, link = login) and admins (the couple with full access; helpers who see everything and change nothing, FR-46). Admin uses the same tokens, denser and undecorated (memlog, *Admin look*).
- **UI system:** none assumed **[ASSUMPTION — stack is an architecture decision, D15]**. Components are specified here and in DESIGN.md; any library chosen later inherits these rules.
- **Language:** Norwegian bokmål only in v1 (English is [If time]). All times Norwegian time; amounts in whole kroner (FR-41, NFR-2).
- **Light only;** no dark mode (memlog, decision D).
- **Stakes:** consumer, with personal and health-adjacent data and money. Accessibility and privacy weigh heavily.

## Information Architecture

### Guest surfaces (personal link)

| # | Surface | Reached from | Purpose |
|---|---|---|---|
| G1 | No valid link | Unknown/deactivated link, bare domain | Friendly private-invitation message; no names, phones, date or place (FR-5) |
| G2 | Invitation (front page) | The personal link | Hero with everything FR-7 lists above the fold; status block once answered; four cards; RSVP repeated; footer |
| G3 | Info pages: Programmet · Praktisk informasjon · Hardingasete og området · Om oss | Nav words, card "Les mer" | One topic each; "Tilbake til invitasjonen" at top and bottom (FR-11) |
| G3b | Gifts [If time] | Fifth card | Text and links |
| G4 | RSVP form, stepped | "Svar på invitasjonen" / "Se eller endre svar" | One task per step (FR-13) |
| G4b | Last-updated header + conflict notice | Inside G4 | Who answered when; another member's newer answer (FR-38) |
| G5 | Check page | Last form step | "Not sent yet", all answers, total, "Endre" per part, "Send svaret" (FR-21) |
| G6 | Receipt (thank-you page) | After sending | Rikke's text, summary, payment choice, closing line (FR-23, FR-34) |
| G7 | Payment details | "Betal nå", status block | Amount, Vipps, account, payment message (FR-34, FR-71) |
| G8 | "Jeg har betalt" report | G7, status block | Report and later correct a payment (FR-35, FR-36) |
| G9 | Answer view, locked | "Se svaret" after the deadline | Read-only answers; payment, report, info, questions, consent withdrawal still work (FR-42) |
| G10 | Ask us | "Spør oss" in the footer of every guest page | Short question form (FR-43) |
| G11 | Consent withdrawal | Answer view (G4/G9) **and** G12 | Delete one person's allergy data (FR-30; memlog) |
| G12 | Privacy page | Footer "Personvern", consent text | FR-66 content; withdrawal entry |
| G13 | Envelope reveal [If time] | First visit to G2 | See Interaction Primitives |
| G14–G15 | Speech sign-up, English [If time] | — | Not specified further here |

**Navigation.** A visible row of a few words at the top of G2 and G3 (e.g. Program · Praktisk · Stedet · Om oss · Svar), wrapping to two lines on narrow screens; **no hamburger** (memlog, *Guest navigation*). "Svar" goes to the form, or to the answer view once answered. Words link to the info pages, matching the cards **[ASSUMPTION — anchors vs pages not decided; FR-8 gives each card its own page]**. In the form (G4–G5) the nav row is replaced by the progress line and "Tilbake", so the only way forward is the next step **[ASSUMPTION]**. The footer band with phone numbers, "Spør oss" and "Personvern" is on every valid-link page, including error pages (FR-6).

**Receipt vs status block (decided).** After "Send svaret" the guest lands on a **separate receipt page** (G6). On later visits the **front page shows the household status block** near the top (sent by whom and when, total, reported paid, deadline) with "Se eller endre svar" (FR-24, FR-37). The receipt is not a persistent page.

### Admin surfaces (username + password)

| # | Surface | Reached from | Purpose |
|---|---|---|---|
| A1 | Login | Admin address | Username/password; slowed retries (NFR-4) |
| A2 | Home: summary + Trenger oppfølging | After login, nav "Oversikt" | FR-54 counts, then FR-56 list directly below |
| A3 | Count drill-down | Any count | The people behind the number (FR-55) |
| A4 | Full overview | Nav "Gjester", A2 | Every household and person; unanswered stand out; mismatch and "Endret" marked (FR-57) |
| A5 | Allergy list | A2, A4 | Consented names + categories for Hardingasete (FR-58) |
| A6 | Guest list: search, add, edit, remove, copy link | Nav "Gjester" | FR-49, FR-51; move guest [T3], deactivate + new link [T3] |
| A7 | Household answer via the guest form | Household in A4/A6 | Admin as author, also after deadline (FR-63) |
| A8 | Consent registration [T3] | Household person | Who, channel, text version, when (FR-31) |
| A9 | Payments | Nav "Betalinger", household | Register received/refund; correct/undo; computed status (FR-59–61) |
| A10 | Payment message edit | Household in A9 | Duplicate warning (FR-71) |
| A11 | Questions | Nav "Spørsmål", A2 item | Read full text, mark answered (FR-44) **[ASSUMPTION — a list page; FR-44 only says Needs attention]** |
| A12 | Settings | Nav "Innstillinger" | Prices, deadline, contacts, Vipps/account; couple edits, helpers read (FR-64, FR-65) |
| A13–A15 | Contact note, history, delete all data [2027] | — | Delete all = tier 3 |
| A16 | Print page for Hardingasete [If time] | A2 | — |

Admin navigation: the same word-row pattern (Oversikt · Gjester · Betalinger · Spørsmål · Innstillinger · Logg ut) **[ASSUMPTION]**. Helpers see the same pages without action controls (memlog).

## Voice and Tone

Brand posture lives in DESIGN.md › Brand & Style. Rules for words on screen:

- **Plain, warm bokmål, "koselig", also in error messages** (NFR-6). Short sentences, one idea each. No jargon ("lagre", "innsende", "feilkode").
- **The site calls itself "invitasjonen"**, never "nettsiden" or "siden" (memlog).
- **du/dere:** address the guest as **du** when one person is invited in the household, **dere** when two or more are (memlog). The site knows the household, as a hand-written card would.
- **Don't ask what the link knows** (NFR-5): names come from the link.
- **Every error says how to fix it.** Blame the form, never the guest.
- **Admin text** is neutral and brief, addressed to the couple; counts and verbs.

Rikke's receipt texts (PRD addendum), slashes resolved by the du/dere rule, punctuation added:

| Case | One invited | Two or more invited |
|---|---|---|
| Coming | «Tusen takk for at du tok deg tiden til å svare, vi gleder oss til å feire den store dagen med deg!» | «… med dere!» |
| Not coming | «Så leit at du ikke har mulighet til å delta, men dette har vi full forståelse for.» | «Så leit at dere ikke har …» |
| Closing | «Du kan nå trygt lukke invitasjonen.» | same (addresses the person at the phone) |

Microcopy. "Decided" = memlog or the couple saw and kept it in a render; all others are proposals **[ASSUMPTION — final wording is Rikke's]**:

| PRD working label / moment | Bokmål | Status |
|---|---|---|
| RSVP button | Svar på invitasjonen | render |
| See or change answer | Se eller endre svar | decided |
| See answer (after deadline) | Se svaret | proposal |
| I am [name] | Jeg er Sigmund · Bytt | proposal |
| Coming / Not coming | Kommer / Kommer ikke | proposal |
| No allergies or dietary needs | Ingen allergier eller matbehov | proposal |
| Not provided / Change | Ikke oppgitt / Endre | proposal |
| Continue / Back | Fortsett / Tilbake | proposal |
| Send answer | Send svaret | proposal |
| Not sent yet (check page) | Svaret er ikke sendt ennå. | proposal |
| Pay now / Pay later | Betal nå / Betal senere | proposal |
| I have paid | Jeg har betalt | proposal |
| Ask us | Spør oss | proposal |
| Read more | Les mer | render |
| Footer | Spørsmål? Send oss en melding: · Personvern | render |
| Lead-in | Vi gleder oss til å feire med deg/dere! (du/dere rule) | render |
| Error summary heading | For å gå videre må du rette opp følgende feil. | research (Designsystemet) |
| Invalid link | Dette er en privat invitasjon. Ta kontakt med Rikke eller Valdemar slik du pleier. | proposal (FR-5 content) |
| Don't know (arrival) | Vet ikke | proposal |
| Needs attention / Changed | Trenger oppfølging / Endret | proposal |
| Undo | Angre | decided |
| Tier-2 consequence | e.g. «3 husstander mister tilgangen» | decided (example) |
| Tier-3 typed word | the household name, or SLETT | decided |

## Component Patterns

Behavioural. Visual specs: DESIGN.md › Components (same names).

| Component | Behavioural rules |
|---|---|
| Page | Static; no scroll effects, parallax or sticky decoration. |
| Nav words | Plain links; current page marked with `aria-current="page"`. Never collapses into a menu. |
| Hero panel | Must show names, date, place, invited names, "Barnefritt bryllup", deadline (weekday, date, time) and the primary button without scrolling on a phone (FR-7, FR-41). Renders without JavaScript [2027]. |
| Wax seal | Decorative (`alt=""`); not a link. Same mark as the favicon. |
| Hero illustration | Informative image with a short Norwegian alt text describing the farmyard; never carries text. |
| Info card | Whole "Les mer" link opens the card's own page (FR-8); link text names the topic for screen readers ("Les mer om programmet"). |
| Lead-in | Static text; follows du/dere rule. |
| Primary button | One per screen, always the one obvious next step (NFR-6). On submit it shows "Sender …" and ignores repeat taps until the server answers (no double "Send svaret" / "Jeg har betalt") **[ASSUMPTION]**. |
| Secondary button | Back, cancel, "Betal senere". Never visually competes with the primary. |
| Destructive button | Tier 3 only; never the default focus; placed apart from safe actions. |
| Text link / "Les mer" | Navigates; never submits data. Opening any link never changes anything (FR-3). |
| Footer band | Contacts as `tel:`/`sms:` links; "Spør oss" opens G10; "Personvern" opens G12. Present on every valid-link guest page, including errors (FR-6). |
| Text field | Label above, hint below, error between label and field. Forgiving input: amounts accept "900", "900 kr", "1 450" **[ASSUMPTION]**. No date or time pickers (FR-18). |
| Choice control | Whole row tappable. Attendance starts with nothing selected (FR-14); consent Yes/No starts unanswered (FR-26). |
| Notice | Inline, never auto-dismissing on guest pages. Success notices are announced politely; errors assertively. |
| Error summary | Appears after a failed "Fortsett"; receives focus; each item links to and focuses its field (FR-22). Removed when errors are fixed. |
| Status block | Shown on G2 once the household has answered: sent by whom and when, total, reported paid, deadline; button "Se eller endre svar" (before deadline) or "Se svaret" (after). |
| Progress line | "Steg n av m"; m is recalculated when conditional steps appear or disappear (e.g. hike only for Friday attendees). |
| Respondent line | Preset to the link owner (FR-12). Switching changes only who is recorded as answering; answers already filled stay **[ASSUMPTION]**. |
| Running total | Recalculated on every change; removed choices drop out immediately (FR-75); identical on check page and receipt (FR-33). |
| Read-more disclosure | Expands in place inside the step; `aria-expanded`; never navigates away (FR-19). |
| Check-answers list | "Endre" jumps to that step and returns to the check page after "Fortsett"; each "Endre" has hidden context ("Endre måltider for Marie"). Skipped optional answers show "Ikke oppgitt". |
| Receipt panel | Message chosen by answer (coming / not coming); if something is owed, "Betal nå" / "Betal senere" before the closing line; nothing owed → closing line at once (FR-23). Coming message when anyone in the household is coming **[ASSUMPTION]**. |
| Payment details | Payment message is "Bryllup" + household names (FR-71). "Kopier" copies one value and confirms "Kopiert" inline. QR is [If time]. |
| Envelope reveal [If time] | See Interaction Primitives. |
| Admin summary row | Every count is a link to A3 (FR-55); zero counts show "0" and are not links. |
| Attention item | One action: "Merk som håndtert" / "Merk som sett" / "Merk som besvart" (tier 1, undo). Leaves the list per the addendum's leave rules. |
| Status tag | Text first: "Ingenting å betale", "Ikke betalt", "Delbetalt, 300 kr mangler", "Betalt", "Skal ha tilbake 200 kr" (addendum, FR-60), "Endret", "Stemmer ikke" **[ASSUMPTION — bokmål wording]**. |
| Dialog | Focus moves into it, is trapped, returns to the trigger on close; Esc = cancel. Used for tier 2 and 3 and the guest leave warning only. |
| Undo bar | Appears after tier-1 actions; "Angre" restores the item; stays at least 10 seconds and until the next action **[ASSUMPTION]**; announced politely. |

## State Patterns

| State | Where | Treatment |
|---|---|---|
| Saving | Send, report payment, admin saves | Button shows "Sender …"/"Lagrer …"; entered data stays on screen. |
| Saved | G6, G8, admin | Clear success notice with what was saved and when. Saving either succeeds and says so, or fails and says so (NFR-1). |
| Save failed | Any submit | Error notice: what happened, that nothing is lost, "Prøv igjen", and the couple's phone numbers (guest side). Input kept. |
| Validation error | G4, G8, G10, admin forms | Inline error with fix hint + error summary at top (FR-22). |
| Contradiction | G4 | Blocked with an explanation, e.g. overnight while present one day (FR-70). |
| Not sent yet | G5; leaving G4–G5 | Warning notice at top of G5 (FR-21). Leaving: in-page dialog "Svaret er ikke sendt ennå" for in-page links, plus the browser's leave prompt where supported; in-app browsers cannot be relied on (FR-20) **[ASSUMPTION]**. |
| Last updated | Top of G4 when answered | "Sist endret av Arild, 3. mars kl. 18:40" (FR-38). |
| Conflict | G4/G5 when another member sent after this form opened | Warning notice before sending: who, when, what differs; guest reviews, then sends or adjusts. No silent overwrite (FR-38). |
| Locked after deadline | G2, G4→G9 | Button becomes "Se svaret"; read-only answers; "Fristen gikk ut fredag 1. desember kl. 23:59" + contacts. Payment, "Jeg har betalt", info, "Spør oss" and consent withdrawal still work (FR-42). |
| Never answered, after deadline | G2/G9 | Same message without answers; contacts prominent; no payment block (nothing owed) **[ASSUMPTION]**. |
| Total changed after payment | G6/G8/status block | "Du har 300 kr igjen å betale" or "Rikke og Valdemar har fått beskjed og betaler tilbake 200 kr" (FR-36). |
| Allergies without consent | G5 | Warning: the allergy information will not be saved; tell the couple directly (FR-28). |
| No valid link | G1 | Single calm panel; nothing personal. |
| Static fallback | G2 | Invitation text and RSVP button appear if scripts or animation fail [2027]. |
| Helper read-only | All admin | Action buttons **hidden**, not greyed (memlog). Forms show values as text. |
| Session expired | Admin | Login page with "Du ble logget ut fordi du var borte en stund." — see Open Questions on keeping input. |
| Empty | Admin | Needs attention: "Ingenting trenger oppfølging nå."; no questions: "Ingen spørsmål ennå."; no payments: "Ingen betalinger registrert ennå."; drill-down with 0: not a link **[ASSUMPTION — wording]**. |
| Empty | Guest | Household with nothing to pay: no payment block, total shows "0 kr"; allergy step with no consent: nothing stored. |
| Loading | All | Server pages under 3 s (NFR-7); no skeletons or spinners on guest pages **[ASSUMPTION]**. |

**Surface coverage** (states each surface must implement): G1 no-link · G2 unanswered / answered (status block) / locked / never-answered-locked / static fallback · G3 normal (static) · G4 fresh / prefilled + last-updated / validation / contradiction / conflict / leave warning / locked (→G9) · G5 not-sent / allergy-without-consent / conflict / saving / save-failed · G6 coming / not coming / something owed / nothing owed · G7 normal / total changed · G8 empty / validation / saved / corrected · G9 locked / never answered · G10 empty / validation / sent / failed · G11 confirm / done / failed · G12 static · A1 error / slowed / expired · A2 normal / empty attention · A3 list / zero · A4 normal / unanswered / mismatch / changed / read-only · A5 empty ("Ingen allergier registrert ennå.") / list · A6 search empty ("Fant ingen med det navnet.") / tier-3 delete / read-only · A7 edit / after deadline / conflict · A8 tier-2 confirm / read-only · A9 register / undo / read-only · A10 duplicate-message warning / read-only · A11 empty / answered · A12 tier-2 confirm (deadline lock-out count, price-change count) / read-only.

## Interaction Primitives

- **Tap, scroll, type.** No swipe gestures, long-press, drag, carousels, autoplay, hover-only controls or infinite scroll.
- **One step at a time** in the form: "Fortsett" forward, "Tilbake" back, browser Back equals "Tilbake" **[ASSUMPTION]**.
- **Fixed choices over free input** (arrival, allergies, days) — fewer errors for older guests, countable data for the couple (research §5).
- **Form step order** after FR-14's first two: meals → overnight → Friday hike (Friday attendees) → arrival → allergies and consent → check page **[ASSUMPTION — follows UJ-1's order; see Open Questions]**.

### Admin protection tiers (decided)

Principle: **prefer undo over "Er du sikker?"** wherever possible.

| Tier | Actions | Pattern |
|---|---|---|
| 1 Easily undone | Mark seen / handled / answered in Trenger oppfølging | No confirmation; undo bar with "Angre"; can also be unmarked later. |
| 2 Important | Register or correct a payment (also undoable, FR-59), edit household, deactivate link + new link, change deadline or settings, price change, move guest, register consent **[ASSUMPTION for the last two]** | Dialog stating the consequence in plain words: the new deadline in words and, if past or within two weeks, how many households are locked out (FR-64); number of households whose total changes (FR-65). |
| 3 Irreversible | Delete guest or household; delete all guest data [2027] | Typed confirmation (household name or SLETT), destructive button placed apart, muted rust. |

Guest-side consent withdrawal: one confirmation step naming what is deleted ("Allergiopplysningene til Marie slettes.") **[ASSUMPTION]**.

### Envelope reveal [If time]

Green envelope with the "R & V" wax seal opens and unfolds into a **plain sheet** (not heart-shaped, no lace) that becomes the invitation; afterwards no envelope, folds or sheet edges (addendum; memlog override). **First visit only**, a visible **"Hopp over"** from the first frame, skipped entirely when the phone asks for reduced motion, and never blocking the static invitation underneath (NFR-5, PRD 3.2).

## Accessibility Floor

Behavioural; contrast values live in DESIGN.md. Target WCAG 2.2 AA (NFR-5).

- Body text ≥ 18px on guest pages (we use 20px); works at 200 % zoom and 320px with no horizontal scroll.
- Everything works by keyboard; focus always visible (`{colors.focus-on-panel}` on cream, `{colors.focus-on-green}` on green) and never hidden behind sticky elements (2.4.11) — hence no sticky bars on guest pages **[ASSUMPTION]**.
- Guest touch targets ≥ 44 × 44px (`{spacing.target-min}`); admin the same **[ASSUMPTION — NFR-5 names guest pages only]**.
- Every field has a visible label; groups use fieldset/legend; errors per FR-22, error summary focused.
- Status, mismatch and errors never by colour alone (1.4.1): text label + icon.
- Don't ask for what the link knows (3.3.7); admin login allows paste and password managers (3.3.8).
- `lang="nb"`; page titles describe the page type but contain no names, identical for every guest (FR-4).
- Dynamic changes (running total, conflict, saved) announced via polite live regions; errors assertive.
- Motion: only the [If time] envelope; respects reduce-motion and is skippable.

## Consent & Privacy UX

- Allergies are optional per coming person: categories (gluten, laktose, nøtter, skalldyr, vegetar, vegan, annet) + short note, or "Ingen allergier eller matbehov" (FR-25).
- When allergies are entered, the consent block explains purpose, who sees it (Rikke, Valdemar, toastmaster, forlover, best man; names and allergies go to Hardingasete's kitchen) and **how to withdraw — before the Yes/No** (research §3.2). Yes/No starts unanswered; never pushed (CM-4).
- Entering for others adds "Jeg bekrefter at Marie vet om dette og er enig" (FR-27).
- The RSVP can always be sent without consent (FR-28).
- **Withdrawal lives in two places** (memlog): the answer view next to the allergies where consent was given, and the privacy page. Works after the deadline; deletes the data and marks the household "Endret" (FR-30).
- "Spør oss" says who can read questions and asks for no health information (FR-43).
- Guest pages are noindex and pass no referrer (NFR-4). Mocks, screenshots and tests use fictional people only (NFR-3).

## Key Flows

Quality bar for every guest flow: each screen has one obvious next step (NFR-6).

### UJ-1: Bestefar Sigmund answers for himself and bestemor (Sigmund, 78, SMS link on his phone)

Quality bar (memlog override): the **whole journey from link to sent answer** must feel nice and simple, evenly at every step; the receipt is not singled out.

1. Opens the link → G2. [If time: envelope on first visit, skippable.] Sees names, date, place, "Invitert: Sigmund og bestemor", "Barnefritt bryllup", deadline and "Svar på invitasjonen" without scrolling.
2. Scrolls past the lead-in to the four cards; may open one and return with "Tilbake til invitasjonen".
3. Taps "Svar på invitasjonen" → G4. "Jeg er Sigmund" is preset. Marks both "Kommer"; "Hele helgen?" → Ja.
4. Meals and overnight, prices shown before choosing; opens "Les mer om hyttene" in place. Running total updates.
5. Allergies: "Ingen allergier eller matbehov" for himself; bestemor's categories; consent Ja; confirms she knows and agrees.
6. G5 says "Svaret er ikke sendt ennå"; he checks answers and total, presses "Send svaret".
7. **Climax:** G6 confirms in Rikke's words that the answer is sent — he understood every step, answered alone, and can see what he answered and what happens next.
8. Payment: "Betal nå" → G7 → pays → "Jeg har betalt" → G8 shows what he reported and when; or "Betal senere" → told the link always shows what he owes. Then «Du kan nå trygt lukke invitasjonen.»

Failure: send fails → error notice, answers kept, "Prøv igjen" and phone numbers. Tries to leave mid-form → "Svaret er ikke sendt ennå". Wrong input → inline error + summary.

### UJ-2: Onkel Arild answers for a household where not everyone comes (Arild for Marie, Filippa, Leone)

1. "Jeg er Arild"; marks Arild, Marie, Filippa "Kommer", Leone "Kommer ikke" (nothing pre-ticked).
2. "Hele helgen?" → Nei; picks lørdag and søndag for Filippa; each day shows its date and what happens.
3. The form adapts: nothing more about Leone; Filippa offered only her days' meals; no Saturday breakfast for her; overnight step says the cabin is the whole weekend, both nights paid.
4. **Climax:** the check page lists exactly what he chose per person, and the total matches to the krone.
5. Sends and pays as UJ-1.
6. Two weeks later: status block → "Se eller endre svar"; header shows who answered and when; he changes; total up → remaining amount, down → couple notified and will refund.
7. Marie opens her link: status block shows Arild answered and when, not an empty form.

Failure: Marie opened the form before Arild sent → conflict notice before she can send. After the deadline → locked view with contacts. Contradiction (overnight with one day) → blocked with reason.

### UJ-3: Synne has lost her link and needs a change after the deadline

1. Synne messages Rikke.
2. Rikke, on her phone: A6 → searches "Synne" → "Kopier lenke" → sends it.
3. If the link went astray: deactivate + new link (tier 2 dialog: "Synnes gamle lenke slutter å virke. De andre i husstanden beholder sine."); the old link shows G1.
4. Synne opens the link after the deadline: "Se svaret" → G9, deadline message, contacts; she can still pay, report payment, read info, ask, withdraw consent.
5. **Climax:** Rikke opens Synne's household in A7, the same form guests use, and makes the change after the deadline; it is recorded with Rikke as author.
6. Phone-reported allergy: Rikke sends the consent text, then registers consent in A8.

Failure: any error page still shows the couple's phone numbers (FR-6).

### UJ-4: Rikke checks the numbers and sends them to Hardingasete

1. Logs in → A2 summary (FR-54).
2. Below: Trenger oppfølging; marks items handled → undo bar.
3. **Climax:** taps "12 til fredagsmiddag" → A3 lists the 12 people; the numbers are trustworthy.
4. "Ikke svart" lists names with tappable phone/email; she contacts them herself.
5. Types the numbers into an email to Hardingasete (print page [If time]). Helpers see the same, without buttons.

Failure: nothing needs attention → empty state. Helper taps around → no action controls exist to fail.

### UJ-5: Rikke follows up payments

1. Checks Vipps and bank; the payment message identifies the household.
2. A9: registers "Mottatt 900 kr" (tier 2 confirm; undoable).
3. **Climax:** the status tag recalculates by itself ("Betalt" / "Delbetalt, 300 kr mangler").
4. A guest's "Jeg har betalt" exceeds what is registered → household tagged "Stemmer ikke" (error colour + icon + text) and listed in Trenger oppfølging.
5. She reminds by message herself.

Failure: wrong amount registered → "Angre"/correct (FR-59).

### UJ-6: Ingrid, the examiner, runs the app

1. Follows the README; seeds fictional guests; uses a listed test link in a narrow window.
2. Completes the RSVP, tries wrong input (errors + summary), checks the receipt.
3. Logs in as admin; summary matches the expected-results list.
4. Moves the deadline to yesterday in A12 → dialog repeats the date in words and how many households are locked out.
5. **Climax:** the guest link now shows "Se svaret", locked; the admin can still edit via A7.
6. Sends a question; it appears in A2/A11 and in the terminal. Logs in as helper: no action buttons.

Failure: logs in with wrong password → plain error, slowed retries.

## Inspiration & Anti-patterns

- **Lifted from the couple's images** ([inspirasjon.md](../../ux/inspirasjon/inspirasjon.md)): the cosy sheet feeling (01), green envelope (02, 05), colours and simple area drawings (03), sections separated rather than one uniform page (08), top links to jump to parts and "The finer details" cards with read-more (09), colours, texture and dark wood (11, 13), the *Brudeferden i Hardanger* feeling (12), illustration 17 (from 14–18).
- **Lifted from research:** GOV.UK check-answers and confirmation patterns; Designsystemet error summary; deadline next to the RSVP button (Joy); personal link instead of name search.
- **Venue photos** ([stedet.md](../../ux/stedet/stedet.md)) are information for G3 pages, not style.
- **Rejected:** heart-shaped/lace letter (08); Italian theme and olive plants (01, 03, 07); dress-code section and modern look (09); clutter (02); grey (04); bluish greens (round 1); layered offset sheets and small caps (not decided, dropped); dark green page (round 6); light sage page (round 4); gold, bling, neon, blinking, luxury feel; hamburger menu; "Everyone is coming" pre-ticked; flags for language.

## Responsive & Platform

| Context | Behaviour |
|---|---|
| Phone 320–480px | The design. Nav words wrap; names shrink to fit one line. |
| PC | Same phone column centred on the green page. Wider layout [If time]. |
| Admin on phone | Quick tasks (find guest, copy link, answered?) fit one screen (FR-48); tables become stacked rows **[ASSUMPTION]**. |
| Admin on PC | May use a wider column for A4 (FR-48) **[ASSUMPTION — width not set]**. |
| In-app browsers | Messenger/Facebook must work, checked on a real old device [2027]; leave warning has in-page fallback. |
| No JavaScript | Invitation text and RSVP button render [2027]. |

## Open Questions

1. Does everything FR-7 requires, plus seal and illustration, fit above the fold at 360 × 640 and 320px? If not: cap illustration height or shrink the seal.
2. Final bokmål for all "proposal" microcopy (Rikke).
3. Step order after the first two (proposed above).
4. Why-guests-pay wording (waits for PRD Q7).
5. Arrival fixed choices; programme times and content placeholders.
6. How "kanskje" for the hike counts in the summary.
7. Can helpers copy guest links (FR-51 names the couple; D14 decides if links can be shown at all)?
8. Admin session expiry mid-edit: is input kept (architecture)?
9. A one-line English hint for non-Norwegian guests in v1?
10. Envelope colour [If time]: `page-green` or `green-dark`?
11. Texture on the green page and edge treatment of the cream panels — kept open by the couple for later (see DESIGN.md › Elevation & Depth). Non-blocking.
