---
name: "AI'll handle it"
title: "Experience: AI'll handle it"
status: draft
created: 2026-11-10
updated: 2026-11-14
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

> How the invitation and the admin area behave. Visual identity: [DESIGN.md](DESIGN.md); tokens are referenced by name, e.g. `{colors.page-green}`. Requirements (FR/NFR/UJ/SM) are in the [PRD](../../prds/prd-aill-handle-it-2026-11-07/prd.md) and not restated here. Decisions: [.memlog.md](.memlog.md). The approved first screen of the front page is rendered in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html) (360px, with the fold line; supersedes the hero in [mockups/front-page-2.html](mockups/front-page-2.html), which still shows the cards below); key screens in [mockups/key-form-steps.html](mockups/key-form-steps.html), [mockups/key-check-page.html](mockups/key-check-page.html), [mockups/key-receipt.html](mockups/key-receipt.html) and the approved admin home in [mockups/admin-rework-1.html](mockups/admin-rework-1.html). **The spines win on conflict with any render.** `[If time]` and `[2027]` follow PRD 3.2–3.3.

## Foundation

- **Form factor:** phone-first responsive web for all ages (NFR-6). A PC shows the phone layout in a centred column; a wider PC layout is [If time]. Links arrive by SMS, Messenger and email and open in the phone's browser or an in-app browser.
- **Two audiences, one visual system:** guests (about 70, many older, link = login) and admins (the couple with full access; helpers who see everything and change nothing, FR-46). Admin uses the same tokens, denser and undecorated (memlog, *Admin look*).
- **UI system:** none assumed **[ASSUMPTION — stack is an architecture decision, D15]**. Components are specified here and in DESIGN.md; any library chosen later inherits these rules.
- **Language:** Norwegian bokmål only, no English hint line in v1 (memlog). All times Norwegian time; amounts in whole kroner (FR-41, NFR-2).
- **Light only;** no dark mode (memlog, decision D); pages declare `<meta name="color-scheme" content="light only">`, checked in Samsung Internet with dark mode on.
- **Stakes:** consumer, with personal and health-adjacent data and money. Accessibility and privacy weigh heavily.

## Information Architecture

### Guest surfaces (personal link)

| # | Surface | Reached from | Purpose |
|---|---|---|---|
| G1 | No valid link | Unknown/deactivated link, bare domain | Friendly private-invitation message; no names, phones, date or place (FR-5) |
| G2 | Invitation (front page) | The personal link | Sticky nav bar with "Svar"; hero with FR-7 content and a "Svar" link in the deadline line; four cards; RSVP panel; footer (FR-7, FR-8) |
| G3 | Info pages: Programmet · Praktisk informasjon · Hardingasete og området · Om oss | Nav words, card "Les mer" | One topic each; "Tilbake til invitasjonen" at top and bottom (FR-11) |
| G3b | Gifts [If time] | Fifth card | Text and links |
| G4 | RSVP form, stepped | RSVP button, "Se eller endre svar", draft offer | One task per step (FR-13); last-updated header and conflict notice are states of G4. Rendered: [mockups/key-form-steps.html](mockups/key-form-steps.html) |
| G5 | Check page | Last form step | "Not sent yet", all answers, total, "Endre" per part, "Send svaret" (FR-21). Rendered: [mockups/key-check-page.html](mockups/key-check-page.html) |
| G6 | Receipt (thank-you page) | After sending | Rikke's text, summary, payment choice, closing line (FR-23, FR-34). Rendered with G7 and the answered G2: [mockups/key-receipt.html](mockups/key-receipt.html) |
| G7 | Payment details | "Betal nå", status block | Amount, Vipps, account, payment message (FR-34, FR-71) |
| G8 | "Jeg har betalt" report | G7, status block | Report and later correct a payment (FR-35, FR-36) |
| G9 | Answer view, locked | "Se svaret" after the deadline | Read-only answers; payment, report, info, questions, consent withdrawal still work (FR-42) |
| G10 | Ask us | "Spør oss" in the footer of every guest page | Short question form (FR-43) |
| G11 | Consent withdrawal | Answer view (G4/G9) **and** G12 | Delete one person's allergy data (FR-30; memlog) |
| G12 | Privacy page | Footer "Personvern", consent text | FR-66 content; withdrawal entry |
| G13 | Envelope reveal [If time] | First visit to G2 | See Interaction Primitives |
| G14–G15 | Speech sign-up, English [If time] | — | Not specified further here |

**Navigation.** A sticky nav bar at the top of G2 and G3: nav words Program · Praktisk · Stedet · Om oss on the left, a **"Svar" button** on the right; no hamburger (memlog, *Guest navigation*, *Front page redesign*). The words open the info pages, matching the cards **[ASSUMPTION — anchors vs pages not decided; FR-8 gives each card its own page]**. "Svar" — in the bar and as the link in the hero's deadline line — jumps to the RSVP panel on G2 (`#svar`); from G3 it opens G2 at `#svar`. **Once the household has answered, the nav "Svar" keeps its label and goes to the household status block** (the hero's deadline-line link likewise); where the block sits on G2 is Open Question 1. In the form (G4–G5) and on the receipt (G6) there is no nav bar: the progress line and "Tilbake" do the job (as rendered in the key-screen mockups). The footer band with phone numbers, "Spør oss" and "Personvern" is on every valid-link page, including error pages (FR-6).

**Receipt vs status block (decided).** After "Send svaret" the guest lands on a **separate receipt page** (G6). On later visits G2 shows the **household status block** (FR-24, FR-37); where on G2 is Open Question 1. The receipt is not a persistent page.

### Admin surfaces (username + password)

| # | Surface | Reached from | Purpose |
|---|---|---|---|
| A1 | Login | Admin address | Username/password; slowed retries (NFR-4) |
| A2 | Home: Trenger oppfølging, answer progress, summary | After login, nav "Oversikt" | FR-56 list at the very top without scrolling; then «Svart: X av Y husstander» with «Se hva alle har svart» (FR-57); then the FR-54 summary in small panels. Approved render: [mockups/admin-rework-1.html](mockups/admin-rework-1.html); `.working/key-admin-overview.html` is the superseded first version (kept in `.working/`) |
| A3 | Count drill-down | Any count | The people behind the number (FR-55) |
| A4 | Full overview | Nav "Gjester", A2 «Se hva alle har svart» | Every household and person with what they answered; unanswered first and tagged "Ikke svart"; "Stemmer ikke" and "Endret" tagged (FR-57) |
| A5 | Allergy list | A2, A4 | Consented names + categories for Hardingasete (FR-58) |
| A6 | Guest list: search, add, edit, remove, copy link | Nav "Gjester" | FR-49, FR-51; copy link is the couple's only (helpers can neither see nor copy links; D14 decides whether links can be shown at all); move guest [T3], deactivate + new link [T3] |
| A7 | Household answer via the guest form | Household in A4/A6 | Admin as author, also after deadline (FR-63) |
| A8 | Consent registration [T3] | Household person | Who, channel, text version, when (FR-31) |
| A9 | Payments | Nav "Betalinger", household | Register received/refund; correct/undo; computed status (FR-59–61) |
| A10 | Payment message edit | Household in A9 | Duplicate warning (FR-71) |
| A11 | Questions | Nav "Spørsmål", A2 item | Read full text, mark answered (FR-44) **[ASSUMPTION — a list page; FR-44 only says Needs attention]** |
| A12 | Settings | Nav "Innstillinger" | Prices, deadline, contacts, Vipps/account; couple edits, helpers read (FR-64, FR-65) |
| A13–A15 | Contact note, history, delete all data [2027] | — | Delete all = tier 3 |
| A16 | Print page for Hardingasete [If time] | A2 | — |

Admin navigation: the Admin nav (DESIGN › Components), not sticky. Helpers see the same pages without action controls (memlog).

## Voice and Tone

Brand posture lives in DESIGN.md › Brand & Style. Rules for words on screen:

- **Plain, warm bokmål, "koselig", also in error messages** (NFR-6). Short sentences, one idea each. No jargon ("lagre", "innsende", "feilkode").
- **The site calls itself "invitasjonen"**, never "nettsiden" or "siden" (memlog).
- **du/dere:** **du** when one person is invited in the household, **dere** when two or more are (memlog).
- **Don't ask what the link knows** (NFR-5): names come from the link.
- **Every error says how to fix it.** Blame the form, never the guest.
- **Admin text** is neutral and brief, addressed to the couple; counts and verbs.

Rikke's receipt texts (PRD addendum), slashes resolved by the du/dere rule:

| Case | One invited | Two or more invited |
|---|---|---|
| Coming | «Tusen takk for at du tok deg tiden til å svare, vi gleder oss til å feire den store dagen med deg!» | «… med dere!» |
| Not coming | «Så leit at du ikke har mulighet til å delta, men dette har vi full forståelse for.» | «Så leit at dere ikke har …» |
| Closing | «Du kan nå trygt lukke invitasjonen.» | same (addresses the person at the phone) |

Microcopy. "Decided" = memlog or the couple kept it in a render; all others are proposals **[ASSUMPTION — final wording is Rikke's]**:

| Moment | Bokmål | Status |
|---|---|---|
| Nav button / hero deadline link | Svar · «**Svar** innen 4. januar 2028» (short form in the hero, no weekday or time) | decided |
| Full deadline (RSVP sheet, status block) | «Svar innen tirsdag 4. januar 2028 kl. 23:59» | decided (FR-41) |
| Hero lines | «inviterer dere til sitt bryllup» (du/dere rule: «inviterer deg til sitt bryllup») · «for Sigmund og bestemor» (replaces «Invitert: …») | decided |
| RSVP panel heading and button | Svar på invitasjonen | render |
| Child-free line | Barnefritt bryllup – vi håper dere får en fin helg for dere selv. | proposal (marked as such in the render) |
| See or change answer | Se eller endre svar | decided |
| See answer (after deadline) | Se svaret | proposal |
| Draft offer | Vil du fortsette der du slapp? · Ja, fortsett · Nei, begynn på nytt | question decided; buttons proposal |
| Draft notice on G2 | Du har et svar som ikke er sendt ennå. | proposal |
| I am [name] | Jeg er Sigmund · Bytt (accessible name "Bytt hvem som svarer") | proposal |
| Coming / Not coming | Kommer / Kommer ikke | proposal |
| No allergies or dietary needs | Ingen allergier eller matbehov · Eller kryss av for det som gjelder: | proposal |
| Field error in a choice group | e.g. «Feil: Velg «Kommer» eller «Kommer ikke» for bestemor.»; summary link «Velg om bestemor kommer» | proposal (render) |
| Not provided / Change | Ikke oppgitt / Endre | proposal |
| Continue / Back | Fortsett / Tilbake (Fortsett above Tilbake) | proposal |
| Send answer | Send svaret | proposal |
| Not sent yet (check page) | Obs: Svaret er ikke sendt ennå. | proposal |
| Check page heading | Se over svaret før du sender | proposal (render) |
| Receipt heading and sent line | Svaret er sendt · «Sendt av Sigmund tirsdag 12. oktober 2027 kl. 14:31.» | proposal (render) |
| Receipt summary / payment details | Dette har dere svart · Slik betaler du | proposal (render) |
| Status block | Svaret er sendt · Sendt av … · Totalt for husstanden: … · «Meldt betalt: 3 900 kr, 12. oktober.» · «Dere kan endre svaret fram til tirsdag 4. januar 2028 kl. 23:59.» · Se eller endre svar | button decided; rest proposal (render) |
| Leave warning | Svaret er ikke sendt ennå. Det du har fylt ut, er tatt vare på på denne telefonen. · Bli og fullfør svaret · Gå uten å sende | proposal |
| Pay now / Pay later | Betal nå / Betal senere | proposal |
| I have paid | Jeg har betalt | proposal |
| Copy | Kopier (accessible names "Kopier kontonummer" etc.) · Kopiert · Trykk og hold for å kopiere | proposal |
| Ask us | Spør oss | proposal |
| Read more | Les mer (accessible name "Les mer om programmet" etc.) | render |
| Footer | Spørsmål? Send oss en melding: · Personvern | render |
| Lead-in | Vi gleder oss til å feire med deg/dere (du/dere rule; no exclamation mark in the approved render) | render |
| Error summary heading | For å gå videre må du rette opp følgende feil. | research (Designsystemet) |
| Notice prefixes | Feil: · Obs: | proposal |
| Page title | «Steg 3 av 6: Overnatting – Invitasjon»; «Feil: » first when the step has errors | proposal |
| Invalid link | Dette er en privat invitasjon. Ta kontakt med Rikke eller Valdemar slik du pleier. | proposal (FR-5 content) |
| Needs attention / Changed / Not answered | Trenger oppfølging / Endret / Ikke svart | proposal |
| Admin attention panel | «Trenger oppfølging (7)» · «Vis alle 7» · reasons e.g. «Betalingen stemmer ikke», «Har ikke svart ennå» · empty: «Ingenting trenger oppfølging nå» (with check icon) · «Vis håndterte» | proposal (render) |
| Admin answer progress | «Svart: 28 av 30 husstander» · «Se hva alle har svart» · rows Kommer / Kommer ikke / Ikke svart ennå | proposal (render) |
| Admin summary panels | Når kommer de? (Hele helgen (fre–søn) · Ikke hele helgen · Bare lørdag–søndag / Bare lørdag / Bare fredag–lørdag) · Overnatting (Overnatter ikke · Senger totalt) · Mat · Allergier (med samtykke) (Har allergier eller matbehov · Ingen allergier eller matbehov · Har ikke svart på allergier · «Én person kan ha flere allergier.») · Betaling (husstander som kommer) | proposal (render) |
| Refund owed (admin count and attention reason) | **Skal ha penger tilbake** — replaces the render's «Tilgode», which can be read both ways | proposal |
| Hike in admin summary | Panel «Fjelltur fredag», row «5 kommer, 2 kanskje». The render's «Fottur fredag» is replaced by the spine term «Fjelltur» | «5 kommer, 2 kanskje» decided (pattern); heading proposal |
| Undo | Merket som håndtert. Angre | "Angre" decided |
| Tier-2 consequence | e.g. «3 husstander mister tilgangen» | decided (example) |
| Tier-3 typed word | the household name, or SLETT | decided |

## Component Patterns

Behavioural. Visual specs: DESIGN.md › Components (same names).

| Component | Behavioural rules |
|---|---|
| Page | Static; no scroll effects or parallax. The nav bar is the only sticky element. |
| Nav bar | `<nav aria-label="Invitasjonen">` with a list of links; current page `aria-current="page"`. Sticky only while the viewport is ≥ 400 CSS px tall (see Accessibility Floor). Never collapses into a menu. |
| Nav "Svar" button | A link to `#svar` (works without JS). Jumps to the RSVP panel; the next Tab lands on the RSVP button. Smooth scroll only under `prefers-reduced-motion: no-preference`, otherwise instant. |
| Hero sheet | The whole sheet — names, date, place, invited names and the short deadline with its "Svar" link — fits without scrolling at 360 × 560 (FR-7; measured 2026-11-14: sheet ends at 552px). The full deadline with weekday and time is next to the RSVP button (FR-41). Names are the page's `h1`; the invites line, date, place and invited line are plain paragraphs. |
| Wax seal | Decorative image, `alt=""`; not a link. Same image as the favicon. |
| Flower divider | Decorative image, `alt=""`; never carries meaning. |
| Hero illustration | Short alt: «Akvarell av tunet på Hardingasete.» Never carries text. |
| Info card | One link per card ("Les mer", accessible name "Les mer om programmet"); its hit area covers the whole card, so tapping the heading works. Opens the card's page (FR-8). Card headings are `h2`. |
| Lead-in | Static text; follows du/dere rule. |
| RSVP panel | Target of both "Svar" links (`id="svar"`, `scroll-margin-top` = bar height + 12px). Holds the child-free line, the full deadline and the RSVP button; shows the draft notice when an unsent draft exists on the device. |
| Primary button | The one distinct next step on a screen (NFR-6); repeats of the same action allowed. On submit it shows "Sender …" and ignores repeat taps until the server answers **[ASSUMPTION]**. In form steps, check page and receipt it comes **before** the secondary button, so "Fortsett" / "Send svaret" / "Betal nå" is first in reading and Tab order **[forslag]**. |
| Secondary button | Back, cancel, "Betal senere", "Nei, begynn på nytt". Never visually competes with the primary; in the form it sits below the primary. |
| Destructive button | Tier 3 only; never the default focus; placed apart from safe actions. |
| Focus ring | Shown on keyboard focus and on press; never hidden under the sticky bar (scroll padding, Accessibility Floor). |
| Text link / "Les mer" | Navigates; never submits or changes data (FR-3). |
| Footer band | Each phone number is its own `tel:` link row; "Spør oss" opens G10; "Personvern" opens G12. On every valid-link guest page, including errors (FR-6). |
| Text field | Label above, hint below, error between label and field. `aria-describedby` points to hint and error; `aria-invalid="true"` when in error. Forgiving input: amounts accept "900", "900 kr", "1 450" **[ASSUMPTION]**. No date or time pickers. Variants: multi-line (G10), search (A6, with "Fant ingen med det navnet."), typed confirmation (tier 3). |
| Choice control | Every group is a `fieldset` with the question as `legend`; its error sits inside the fieldset, right under the legend, as icon + «Feil: …» (no border on the group), and the fieldset's `aria-describedby` points to it. Whole row tappable. Attendance starts with nothing selected (FR-14); consent Ja/Nei starts unanswered (FR-26). **«Ingen allergier eller matbehov» is exclusive per person:** ticking it clears that person's category ticks, and ticking any category clears it; without scripts, a person sent with both is returned with an inline error asking to choose one **[ASSUMPTION — no-JS fallback]**. |
| Notice | Inline, never auto-dismissing on guest pages. Present at page load = not a live region; changes after load are announced (polite; errors assertive). |
| Error summary | After a failed "Fortsett" the page reloads with the summary focused; each item links to and focuses its field (FR-22); `<title>` starts with "Feil: ". Gone when errors are fixed. |
| Status block | Shown on G2 once the household has answered, headed «Svaret er sendt»: «Sendt av <name> <weekday date> kl. <time>.», «Totalt for husstanden: …», «Meldt betalt: <amount>, <date>.» (only when a payment is reported), «Dere kan endre svaret fram til <deadline>.» (du/dere rule), then "Se eller endre svar" (before deadline) or "Se svaret" (after) **[forslag — wording except the buttons]**. **It is the target of the nav "Svar" once answered** (and of the hero link); focus lands on the block's heading. Placement on G2: Open Question 1. |
| Draft offer | See Interaction Primitives › Unsent answer kept (FR-78). |
| Progress line | "Steg n av m: <step name>" right under the step `h1`. m can change only when the answers that create or remove steps change (who comes, which days); it never changes while moving forward or back otherwise. |
| Respondent line | Shown on **every form step**, under the progress line. Preset to the link owner (FR-12). "Bytt" is a button (`aria-expanded`, accessible name "Bytt hvem som svarer"), not a link. Switching changes only who is recorded as answering; filled answers stay **[ASSUMPTION]**. |
| Running total | Recalculated on every change, announced politely; removed choices drop out (FR-75); identical on check page and receipt (FR-33). |
| Read-more disclosure | Expands in place; `aria-expanded`; never navigates away (FR-19). |
| Consent block | Explanation (purpose, recipients, how to withdraw) comes **before** the Ja/Nei and is inside the fieldset, referenced from the legend. Starts unanswered, never pushed (CM-4). "Jeg bekrefter at Marie vet om dette og er enig" only when answering for others (FR-27). Sending never requires consent (FR-28). |
| Check-answers list | Page `h1` «Se over svaret før du sender», after the «Obs: Svaret er ikke sendt ennå.» notice **[forslag]**. One "Endre" per part; it jumps to that step and returns to the check page after "Fortsett"; each has hidden context ("Endre måltider"). Skipped optional answers show "Ikke oppgitt". |
| Receipt panel | Success notice with the `h1` «Svaret er sendt» and who sent it when; then the message by answer (coming / not coming), the summary and the total. If something is owed: "Betal nå" / "Betal senere", and the closing line is shown **at once, directly below them** (it does not wait for a choice); "Betal senere" adds that the link always shows what is left to pay. Nothing owed → no payment buttons; the closing line follows the summary (FR-23). Coming message when anyone in the household comes **[ASSUMPTION]**. |
| Payment details | Payment message is "Bryllup" + household names (FR-71). "Kopier" buttons are shown only where the clipboard is available; "Kopiert" in a polite live region until the next copy. If a copy fails, the value is selected with «Trykk og hold for å kopiere». Values are always plain selectable text. QR is [If time]. |
| Envelope reveal [If time] | See Interaction Primitives. |
| Admin nav | Plain links, `aria-current`, not sticky. |
| Attention panel | First thing on A2 under the Admin nav, `h2` «Trenger oppfølging (n)» (FR-56). Lists the FR-56 items; shows **as many as fit while the answer-progress line stays on the first screen** (two at 360 × 560 in the render) and then «Vis alle n», which shows the whole list on the same page **[ASSUMPTION — mechanism; the fixed count is set by measuring the build]**. Order of items **[ASSUMPTION]**: payment mismatches first (as rendered), then the rest. |
| Attention empty state | When nothing needs attention the panel reads «Ingenting trenger oppfølging nå» with a check icon (as its heading, so the page outline still says what the panel is) and «Vis håndterte» below; the answer progress moves up accordingly. |
| Answer progress | Top of A2's Svar panel: «Svart: X av Y husstander» (households that have sent, of all), a decorative bar, then the Kommer / Kommer ikke / Ikke svart ennå rows (persons · households, each a link), then «Se hva alle har svart» → A4 (FR-57). Rikke's most frequent check (memlog), so it must sit on the first screen. |
| Admin summary panel | Below the Svar panel, one panel per FR-54 group: **Når kommer de?** — Hele helgen (fre–søn); Ikke hele helgen, broken down by day combination (Bare lørdag–søndag, Bare lørdag, Bare fredag–lørdag …). **Overnatting** — Overnatter ikke first; Senger totalt as a secondary line. **Mat** — one count per meal (FR-73). **Allergier (med samtykke)** — Har allergier eller matbehov with one row per category; Ingen allergier eller matbehov; Har ikke svart på allergier (coming guests with neither). **Fjelltur fredag** — «5 kommer, 2 kanskje». **Betaling (husstander som kommer)** — Ingenting å betale, Ikke betalt, Delbetalt, Betalt, Skal ha penger tilbake (FR-60). "Stemmer ikke" is **not** a summary count: it is an attention item (FR-61) and a tag in A4. Example figures that add up: [mockups/admin-rework-1.html](mockups/admin-rework-1.html). |
| Admin summary row | Every count is a link to A3 (FR-55); zero counts show "0" and are not links. Hike: "kommer" and "kanskje" are separate counts, each its own link; "kanskje" is never added to "kommer" (FR-54, memlog). |
| Overview table | Real `<table>` on PC; stacked rows on phone repeat labels as text. Unanswered sort first. |
| Attention item | Reason, household and detail, one action: "Merk som håndtert" / "Merk som sett" / "Merk som besvart" (tier 1), with hidden context in its accessible name ("Merk som håndtert: Synne, betalingen stemmer ikke"). Leaves the list per the addendum's leave rules after the undo is gone. |
| Undo (in place) | The row is **replaced in place** by "Merket som håndtert. Angre" (no bar, no toast); focus moves to "Angre"; it stays until the page is left (no timer). Handled items can be found and unmarked through a "Vis håndterte" filter. |
| Status tag | Text first: "Ingenting å betale", "Ikke betalt", "Delbetalt, 300 kr mangler", "Betalt", "Skal ha tilbake 200 kr" (FR-60), "Endret", "Ikke svart", "Stemmer ikke" **[ASSUMPTION — bokmål wording]**. |
| Dialog | `role="alertdialog"`, labelled by its heading, described by the consequence sentence. Focus goes to the safe button (tier 2) or the heading (tier 3), is trapped, and returns to the trigger. Esc and a scrim tap = cancel. Body scrolls at 200 %. Used for tier 2 and 3, consent withdrawal and the guest leave warning. |

## State Patterns

| State | Where | Treatment |
|---|---|---|
| Saving | Send, report payment, admin saves | Button shows "Sender …"/"Lagrer …"; entered data stays on screen. |
| Saved | G6, G8, admin | Success notice with what was saved and when (NFR-1). |
| Save failed | Any submit | Error notice: what happened, that nothing is lost, "Prøv igjen", and (guest side) the couple's phone numbers. Input kept, also when the cause is an expired form token. |
| Validation error | G4, G8, G10, admin forms | Inline error with fix hint + focused error summary (FR-22). |
| Contradiction | G4 | Blocked with an explanation, e.g. overnight while present one day (FR-70). |
| Draft on device | G4 | Every change is kept on the device (FR-78); nothing reaches the server before "Send svaret". |
| Draft waiting | G2, G4 entry | G2: warning notice in the RSVP panel. Opening the form: Draft offer first (Interaction Primitives). |
| Not sent yet | G5; leaving G4–G5 | Warning notice at top of G5 (FR-21). Leaving: in-page leave dialog for in-page links, plus the browser's leave prompt where supported; in-app browsers may skip it, which the device draft covers (FR-20, FR-78). |
| Last updated | Top of G4 when answered | Info notice "Sist endret av Arild, 3. mars kl. 18:40" (FR-38). |
| Conflict | G4/G5 when another member sent after this form or draft began | Warning notice before sending: who, when, what differs; guest reviews, then sends or adjusts. No silent overwrite (FR-38). |
| Locked after deadline | G2, G4→G9 | Button becomes "Se svaret"; read-only answers; "Fristen gikk ut tirsdag 4. januar kl. 23:59" + contacts. Payment, "Jeg har betalt", info, "Spør oss" and consent withdrawal still work (FR-42). A waiting draft is not offered; the notice says the answer was not sent and to call the couple **[ASSUMPTION]**. |
| Never answered, after deadline | G2/G9 | Same message without answers; contacts prominent; no payment block **[ASSUMPTION]**. |
| Total changed after payment | G6/G8/status block | "Du har 300 kr igjen å betale" or "Rikke og Valdemar har fått beskjed og betaler tilbake 200 kr" (FR-36). |
| Allergies without consent | G5 | Warning: the allergy information will not be saved; tell the couple directly (FR-28). |
| Copy unavailable / failed | G7, A6 | Button hidden when unsupported; on failure the value is selected with «Trykk og hold for å kopiere». |
| No valid link | G1 | Single calm panel; nothing personal. |
| Static fallback | G2 | Invitation text and RSVP button appear if scripts or animation fail [2027]; see Open Question 4. |
| Helper read-only | All admin | Action buttons **hidden**, not greyed (memlog). Forms show values as text. How a helper is told the view is read-only: Open Question 15. |
| Session expired | Admin | Login page with "Du ble logget ut fordi du var borte en stund."; expiry rule is Open Question 5. |
| Empty | Admin | A2: «Ingenting trenger oppfølging nå» with check icon + «Vis håndterte» (Component Patterns › Attention empty state). Elsewhere: "Ingen spørsmål ennå." · "Ingen betalinger registrert ennå." · drill-down with 0: not a link **[ASSUMPTION — wording]**. |
| Empty | Guest | Nothing to pay: no payment block, total "0 kr"; allergy step without consent: nothing stored. |
| Loading | All | Server pages under 3 s (NFR-7); no skeletons or spinners on guest pages; admin lists render whole, no infinite loading **[ASSUMPTION]**. |

### Surface coverage

| Surface | States to implement |
|---|---|
| G1 | no link |
| G2 | unanswered · draft waiting · answered (status block) · locked · never answered, locked · static fallback [2027] |
| G3 | normal (static) |
| G4 | fresh · draft offer · prefilled + last updated · validation · contradiction · conflict · leave warning · locked (→ G9) |
| G5 | not sent · allergy without consent · conflict · saving · save failed |
| G6 | coming · not coming · something owed · nothing owed |
| G7 | normal · total changed · copy unavailable/failed |
| G8 | empty · validation · saved · corrected |
| G9 | locked · never answered |
| G10 | empty · validation · sent · failed |
| G11 | confirm · done · failed |
| G12 | static |
| A1 | error · slowed · expired |
| A2 | attention list (first items + «Vis alle n») · empty attention · undo in place · all answered (30 av 30) · read-only (helper) |
| A3 | list · zero |
| A4 | normal · unanswered · mismatch · changed · read-only |
| A5 | empty ("Ingen allergier registrert ennå.") · list |
| A6 | search empty · tier-3 delete · copy failed · read-only |
| A7 | edit · after deadline · conflict |
| A8 | tier-2 confirm · read-only |
| A9 | register · undo · read-only |
| A10 | duplicate-message warning · read-only |
| A11 | empty · answered |
| A12 | tier-2 confirm (deadline lock-out count, price-change count) · read-only |

## Interaction Primitives

- **Tap, scroll, type.** No swipe gestures, long-press, drag, carousels, autoplay, hover-only controls or infinite scroll.
- **Jump to answer.** Both "Svar" links on G2 are same-page anchors to the RSVP panel; the sticky bar never covers the target.
- **One step at a time** in the form: "Fortsett" forward, "Tilbake" back. Each step has its own address, so the browser's Back button is always safe: it shows the previous step with its answers, never a "resubmit form" prompt (Post/Redirect/Get or equivalent).
- **Fixed choices over free input** (allergies, days) — fewer errors for older guests, countable data for the couple (research §5).
- **Form step order** (Rikke, memlog; FR-14 sets steps 1–2 as two screens): 1 who is coming → 2 whole weekend? / days per person → 3 overnight → 4 meals → 5 allergies and consent → 6 Friday hike (only if someone comes Friday) → check page. There is **no arrival question**: the chosen days show when each guest arrives (FR-18 removed 2026-11-11).

### Unsent answer kept (FR-78, tier 1)

- Every change in the form is kept **on the guest's own device**, tied to the personal link, so a call, an app switch or a Messenger reload loses nothing.
- When the guest comes back through their link and a draft exists: G2's RSVP panel shows «Du har et svar som ikke er sendt ennå.» Opening the form by any route (either "Svar", the RSVP button, or a reload of a step) first shows the **Draft offer**: «Vil du fortsette der du slapp?», when it was started, "Ja, fortsett" (to the step they left, all answers filled in) and "Nei, begynn på nytt" (draft deleted; form starts from the household's sent answer, or empty).
- If someone in the household sent an answer after the draft began, the draft is still offered and the conflict notice appears before sending (FR-38).
- The draft is deleted when sending succeeds, on "Nei, begynn på nytt", and at the deadline. Where device storage is unavailable (private mode, no scripts) there is no draft and the leave warning is the only guard. What the draft may hold is Open Question 6.
- Guest pages have no time limit that loses input (WCAG 2.2.1): a send rejected for any reason keeps every answer, and pressing again works.

### Admin protection tiers (decided)

Principle: **prefer undo over "Er du sikker?"** wherever possible.

| Tier | Actions | Pattern |
|---|---|---|
| 1 Easily undone | Mark seen / handled / answered in Trenger oppfølging | No confirmation; undo in place with "Angre" (no timer); unmark later via "Vis håndterte". |
| 2 Important | Register or correct a payment (also undoable, FR-59), edit household, deactivate link + new link, change deadline or settings, price change, move guest, register consent **[ASSUMPTION for the last two]** | Dialog stating the consequence in plain words: the new deadline in words and, if past or within two weeks, how many households are locked out (FR-64); number of households whose total changes (FR-65). |
| 3 Irreversible | Delete guest or household; delete all guest data [2027] | Typed confirmation: the label shows the exact word in plain text; matching ignores case and surrounding spaces; `autocapitalize="off" autocorrect="off" spellcheck="false"`; the button stays enabled and a mismatch gives an inline error. Destructive button placed apart, muted rust. |

Guest-side consent withdrawal: one confirmation dialog naming what is deleted ("Allergiopplysningene til Marie slettes.") **[ASSUMPTION]**.

### Envelope reveal [If time]

Green envelope closed with the couple's wax seal opens and unfolds into a **plain paper sheet** (no heart shape, no lace) that becomes the hero sheet; afterwards the envelope and folds are gone, but the sheet keeps its paper edge (DESIGN › Elevation & Depth; PRD addendum updated 2026-11-14). Acceptance:

- first visit only; skipped entirely under reduced motion, without scripts or without storage;
- "Hopp over" visible and focusable from the first frame;
- 5 seconds or less;
- the static invitation is in the page and readable by screen readers underneath, not hidden until the end;
- afterwards scroll and focus are at the top of G2.

## Accessibility Floor

Behavioural; contrast values live in DESIGN.md. Target WCAG 2.2 AA (NFR-5).

- **Reflow and zoom:** body ≥ 18px on guest pages (we use 20px), type built in `rem`; no horizontal scroll at 320px or at 200 % zoom, checked at 360 × 560, 320 × 568 and **180 × 320** (a phone at 200 %). The names stack instead of shrinking (DESIGN › Typography).
- **Sticky bar and focus (2.4.11):** `html { scroll-padding-top }` equals the bar's height + `{spacing.scroll-gap}`, so nothing reached by Tab or by a link lands under the bar; the RSVP panel also has `scroll-margin-top`. The bar is **sticky only when the viewport is at least 400 CSS px tall**; on shorter or zoomed screens it scrolls away with the page. If the nav words wrap to two lines, the scroll padding follows the two-line height **[ASSUMPTION — breakpoint measured in the build]**.
- **Keyboard:** everything works by keyboard; `:focus-visible` ring always shown (DESIGN › Focus ring), never `outline: none`.
- **Targets:** ≥ 44 × 44px (`{spacing.target-min}`) on guest and admin pages; admin density never shrinks a target.
- **Structure:** `lang="nb"`; one `h1` per page (names on G2, the step question in the form, the page topic elsewhere), `h2` per card or panel. Every field has a visible label; groups use fieldset/legend; errors per FR-22.
- **Page titles:** describe the page and step ("Steg 3 av 6: Overnatting – Invitasjon"), identical for every guest and without names (FR-4); prefixed "Feil: " when the page shows errors.
- **Announcements:** each step is a new page — focus starts at the top, or on the error summary when there are errors. Live regions only for in-page changes (running total, "Kopiert", conflict appearing).
- **Colour:** status, mismatch and errors never by colour alone (1.4.1): word + icon shape.
- **Forced colours:** checked under `@media (forced-colors: active)`: illustration blend off, choice marks visible, buttons keep an outline.
- **Input:** don't ask for what the link knows (3.3.7); admin login allows paste and password managers (3.3.8).
- **Time:** no guest time limit loses input; admin expiry per Open Question 5.
- **Motion:** only the [If time] envelope and the smooth jump to the RSVP panel; both respect reduce-motion.

## Consent & Privacy UX

FR-25 to FR-31, FR-43 and NFR-3/NFR-4 set the rules; the UX decisions are:

- The explanation (purpose, who sees it, how to withdraw) comes **before** the Ja/Nei (research §3.2), inside the consent fieldset (Component Patterns › Consent block).
- **Withdrawal lives in two places** (memlog): the answer view next to the allergies where consent was given, and the privacy page; it works after the deadline.
- "Spør oss" says who can read questions and asks for no health information.
- The unsent draft (FR-78) stays on the guest's device only and is deleted on send; see Open Question 6.
- Mocks, screenshots and tests use fictional people only (NFR-3).

## Key Flows

Quality bar for every guest flow: each screen has one obvious next step (NFR-6).

### UJ-1: Bestefar Sigmund answers for himself and bestemor (Sigmund, 78, SMS link on his phone)

Quality bar (memlog override): the **whole journey from link to sent answer** must feel nice and simple, evenly at every step; the receipt is not singled out.

1. Opens the link → G2 (rendered in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html)). [If time: envelope on first visit, skippable.] On the first screen he sees a paper invitation: the seal, the farmyard, the names, «inviterer dere til sitt bryllup», the date, the place, «for Sigmund og bestemor» and «Svar innen 4. januar 2028» — and "Svar" twice: in the bar at the top and in the deadline line.
2. Scrolls past the lead-in to the four cards; may open one and return with "Tilbake til invitasjonen". The bar with "Svar" stays at the top while he scrolls.
3. Taps "Svar" (or reaches the RSVP panel by scrolling), reads "Barnefritt bryllup …", taps "Svar på invitasjonen" → G4 ([mockups/key-form-steps.html](mockups/key-form-steps.html)). "Jeg er Sigmund" is preset and stays visible on every step. Marks both "Kommer"; "Hele helgen?" → Ja.
4. Overnight, then meals, prices shown before choosing; opens "Les mer om hyttene" in place. Running total updates.
5. Allergies: "Ingen allergier eller matbehov" for himself; bestemor's categories; consent Ja; confirms she knows and agrees. Then the Friday hike step (they come Friday).
6. G5 «Se over svaret før du sender» says "Svaret er ikke sendt ennå"; he checks answers and total, presses "Send svaret" ([mockups/key-check-page.html](mockups/key-check-page.html)).
7. **Climax:** G6 says «Svaret er sendt» with the time, then confirms in Rikke's words — he understood every step, answered alone, and can see what he answered and what happens next ([mockups/key-receipt.html](mockups/key-receipt.html)).
8. Payment: "Betal nå" → G7 → pays → "Jeg har betalt" → G8 shows what he reported and when; or "Betal senere" → told the link always shows what he owes. «Du kan nå trygt lukke invitasjonen.» stands right under the two buttons from the start.

Failure: the phone rings at step 5 and Messenger reloads the page → he opens the link again, taps "Svar" and gets «Vil du fortsette der du slapp?» → "Ja, fortsett" puts him back on the allergies step with everything filled in. Send fails → error notice, answers kept, "Prøv igjen" and phone numbers. Wrong input → inline error + focused summary.

### UJ-2: Onkel Arild answers for a household where not everyone comes (Arild for Marie, Filippa, Leone)

1. "Jeg er Arild"; marks Arild, Marie, Filippa "Kommer", Leone "Kommer ikke" (nothing pre-ticked).
2. Next step: "Hele helgen?" → Nei; picks lørdag and søndag for Filippa; each day shows its date and what happens.
3. The form adapts: nothing more about Leone; Filippa offered only her days' meals; no Saturday breakfast for her; overnight step says the cabin is the whole weekend, both nights paid.
4. **Climax:** the check page lists exactly what he chose per person, and the total matches to the krone.
5. Sends and pays as UJ-1.
6. Two weeks later: status block → "Se eller endre svar"; header shows who answered and when; he changes; total up → remaining amount, down → couple notified and will refund.
7. Marie opens her link: status block shows Arild answered and when, not an empty form.
8. The couple sees the household at the top of A2 under Trenger oppfølging (changed answer; «Skal ha penger tilbake», 200 kr), pays Arild back and registers the refund in A9; the tag becomes "Betalt" (UJ-5).

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

Rendered: [mockups/admin-rework-1.html](mockups/admin-rework-1.html) (approved; replaces `.working/key-admin-overview.html`).

1. Logs in → A2. **First, without scrolling: «Trenger oppfølging»** (FR-56) — households that haven't answered, coming guests who haven't answered the allergy question, unanswered questions, "Jeg har betalt" reports that don't match ("Stemmer ikke"), refunds owed, changed answers. The first items show, then «Vis alle n». She marks items handled → each row is replaced in place by "Merket som håndtert. Angre". When nothing needs attention, the panel says «Ingenting trenger oppfølging nå».
2. **Right below: «Svart: 28 av 30 husstander»** with «Se hva alle har svart» (A4, FR-57) — her most frequent check — then the summary (FR-54) in small panels: Svar (kommer / kommer ikke / ikke svart ennå, persons and households) · Når kommer de? (hele helgen, ikke hele helgen and which days) · Overnatting (overnatter ikke, senger totalt) · Mat (per meal) · Allergier (med samtykke) (per category, ingen, har ikke svart på allergier) · Fjelltur fredag («5 kommer, 2 kanskje») · Betaling (per payment status).
3. **Climax:** she trusts the numbers because every count opens the people behind it — taps "Fredag middag 38" → A3 lists the 38 people. She can also open the full overview and count for herself.
4. "Ikke svart" lists names with tappable phone/email; she contacts them herself.
5. Types the numbers into an email to Hardingasete: meals, guests, beds, and allergies with names and counts (print page [If time]). Helpers see the same, without buttons.

Failure: nothing needs attention → empty state, and the answer progress moves up. Helper taps around → no action controls exist to fail.

### UJ-5: Rikke follows up payments

1. Checks Vipps and bank; the payment message identifies the household.
2. A9: registers "Mottatt 900 kr" (tier 2 confirm; undoable).
3. **Climax:** the status tag recalculates by itself ("Betalt" / "Delbetalt, 300 kr mangler").
4. A guest's "Jeg har betalt" exceeds what is registered → household tagged "Stemmer ikke" (error icon + text) and listed in Trenger oppfølging.
5. She reminds by message herself; refunds owed are registered the same way as received payments.

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

- **Lifted from the couple's images** ([inspirasjon.md](../../ux/inspirasjon/inspirasjon.md)): the cosy sheet feeling and the soft paper edge of the main sheet (01), green envelope (02, 05), colours and simple area drawings (03), sections separated rather than one uniform page (08), top links to jump to parts and "The finer details" cards with read-more (09), colours, texture and dark wood (11, 13), the *Brudeferden i Hardanger* feeling (12), illustration 17 (from 14–18), the couple's own wax seal (19) and gypsophila from their wedding flowers (20).
- **Lifted from research:** GOV.UK check-answers and confirmation patterns; Designsystemet error summary; deadline next to the RSVP button (Joy); personal link instead of name search.
- **Venue photos** ([stedet.md](../../ux/stedet/stedet.md)) are information for G3 pages, not style.
- **Rejected:** heart-shaped/lace letter (08); Italian theme and olive plants (01, 03, 07); dress-code section and modern look (09); clutter (02); grey (04); bluish greens (round 1); a light or chalk-white rim on the sheets, and sprigs or seals drawn in code (paper-ceremony rounds 1–3); a cropped illustration ("kuttet for mye"); layered offset sheets (dropped); a cabin-cosy rather than solemn look (memlog 100); dark green page (round 6); light sage page (round 4); gold, bling, neon, blinking, luxury feel; hamburger menu; "Everyone is coming" pre-ticked; flags for language; an arrival question.

## Responsive & Platform

| Context | Behaviour |
|---|---|
| Phone 320–480px | The design. Nav bar sticky; nav words may wrap. Names on one line from about a 274px content box (360px phones: 288px); stacked below that (320px phones). At 320px the nav words wrap to two lines (bar 104px). |
| Short or zoomed viewport (< 400 CSS px tall) | Nav bar not sticky. |
| 200 % zoom on a phone (~180 CSS px wide) | Gutter and hero padding 8px; names stacked; nav words wrap freely; no sideways scroll. |
| PC | Same phone column centred on the green page. Wider layout [If time]. |
| Admin on phone | Quick tasks fit one screen (FR-48); tables become stacked rows with visible labels. |
| Admin on PC | May use a wider column for A4 (FR-48) **[ASSUMPTION — width not set]**. |
| In-app browsers | Messenger/Facebook must work, checked on a real old device [2027]; the device draft covers reloads; copy buttons feature-detected. |
| No JavaScript | Anchors, links and form steps are plain HTML; draft, running-total updates and copy need scripts. Full no-JS guarantee: Open Question 4. |

## Open Questions

1. **Answered state of G2** (couple + FR-24): where does the status block go, now that nothing fits above the deadline line? Proposal (rendered in [mockups/key-receipt.html](mockups/key-receipt.html), second phone): it replaces the RSVP panel's content after the cards, and the hero's deadline line becomes «Svar sendt 12. oktober · Se svaret». Already decided: the nav "Svar" keeps its label and goes to the status block, and the block carries "Se eller endre svar"; only the placement and the hero line remain open.
2. **Small phones** (couple): at 320px the names stack and the deadline line falls below the first screen; at 360px it clears the fold by only 7px. Accept (the nav "Svar" stays visible), or narrow the hero's inline padding to 12px at ≤ 340px so the names stay on one line?
3. **Plain-text names** (couple's taste): add the names in plain serif for low-vision guests (e.g. «Rikke og Valdemar inviterer deg til bryllup»), or keep the names in script only?
4. **No-JS guest pages in v1** (PRD/architecture): PRD 3.2 puts the static fallback in [2027]; should all guest pages and form steps work without scripts in v1, with scripts only enhancing?
5. **Admin session expiry** (architecture): an idle session of at least 20 hours, or a warning two minutes before expiry with "Fortsett å være logget inn" — and in both cases is unsaved input restored after logging in again?
6. **Device draft content** (architecture/privacy): may the draft hold allergy categories and notes before consent is given, on a phone others may use? UX default: deleted on send, on "Begynn på nytt" and at the deadline.
7. Final bokmål for all "proposal" microcopy (Rikke).
8. Why-guests-pay wording (waits for PRD Q7).
9. Programme times and content placeholders.
10. ~~Texture on the green page~~ — **resolved 2026-11-11**: the calmer texture in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html); small cream text only on the flat nav bar (DESIGN › Elevation & Depth).
11. ~~Edge treatment of the cream panels~~ — **resolved 2026-11-11**: paper sheets with a soft hand-made edge in the sheet's own colour and a soft shadow (edge B3; DESIGN › Elevation & Depth).
12. **The front page below the hero** (cards, lead-in, RSVP panel, child-free line placement and text) — the couple does not love it yet; revisit later (non-blocking).
13. **Allergies entered without consent in the admin count** (PRD/data decision): FR-28 does not store them, so such a guest would show under «Har ikke svart på allergier» and in Trenger oppfølging although they did answer. Show them as a separate marker (e.g. «Svarte uten samtykke») instead? That needs the site to store the fact that allergies were entered without consent, but not the allergies themselves.
14. **Child-free line in the answered state** (couple): when the status block takes the RSVP panel's place, does «Barnefritt bryllup – …» still show, and where? Belongs to the 'below the hero' revisit (12).
15. **How helpers see they are read-only** (couple): action buttons are hidden, not greyed; should the admin pages also say so, e.g. a line under the nav «Du kan se alt, men ikke endre noe.», or is the missing buttons enough? The only render of the helper view is the superseded `.working/key-admin-overview.html`.
