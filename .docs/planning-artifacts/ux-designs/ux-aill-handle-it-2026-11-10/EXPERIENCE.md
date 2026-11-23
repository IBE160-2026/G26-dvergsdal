---
name: "AI'll handle it"
title: "Experience: AI'll handle it"
status: final
created: 2026-11-10
updated: 2026-11-16
sources:
  - ../../prds/prd-aill-handle-it-2026-11-07/prd.md
  - ../../prds/prd-aill-handle-it-2026-11-07/addendum.md
  - ../../briefs/brief-aill-handle-it-2026-09-23/brief.md
  - ../../briefs/brief-aill-handle-it-2026-09-23/addendum.md
  - ../../research/user-voice-wedding-website-pre-prd-2026-11-06/research.md
  - ../../ux/inspirasjon/inspirasjon.md
  - ../../ux/stedet/stedet.md
  - ../../ux/egne-bilder/egne-bilder.md
  - ../../ux/innhold/Vår historie.docx
---

# AI'll handle it — Experience Spine

> How the invitation and the admin area behave. Visual identity: [DESIGN.md](DESIGN.md); tokens are referenced by name, e.g. `{colors.page-green}`. Requirements (FR/NFR/UJ/SM) are in the [PRD](../../prds/prd-aill-handle-it-2026-11-07/prd.md) and not restated here. Decisions: [.memlog.md](.memlog.md). The whole approved front page is rendered in [mockups/front-page-3.html](mockups/front-page-3.html) (360px, with screen lines; approved 2026-11-15), its first screen in more detail in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html) (its nav words predate 2026-11-15; front-page-3 has the current ones) (both supersede [mockups/front-page-2.html](mockups/front-page-2.html)); key screens in [mockups/key-form-steps.html](mockups/key-form-steps.html), [mockups/key-check-page.html](mockups/key-check-page.html), [mockups/key-receipt.html](mockups/key-receipt.html) and the approved admin home in [mockups/admin-rework-1.html](mockups/admin-rework-1.html). **DESIGN.md and EXPERIENCE.md (the spines) win on any conflict with a render (a mockup file).** `[If time]` and `[2027]` follow PRD 3.2–3.3. `[T3]` marks the PRD's third priority tier (cut first if time runs short), not protection tier 3.

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
| G1 | No valid link | Unknown/deactivated link, bare domain | One paper sheet on the green page, no nav and no footer: «Dette er en privat invitasjon», the gypsophila, «Virker ikke lenken din? Ta kontakt med brudeparet direkte.» No names, phones, date, place or seal (the seal carries the initials; FR-5). A plain «Personvern» link sits under the sheet, because FR-66 asks for it on every page; from G1 the privacy page shows only the general parts. Approved in [mockups/privacy-1.html](mockups/privacy-1.html) |
| G2 | Invitation (front page) | The personal link | Sticky nav bar with "Svar"; hero with FR-7 content and a "Svar" link in the deadline line; lead-in; «Alt om helgen» with three topics; RSVP sheet; footer (FR-7, FR-8) |
| G3 | Info pages: Programmet · Praktisk informasjon · Vår historie | Nav words, topic "Les mer" | One topic each; "Tilbake til invitasjonen" at top and bottom (FR-11); jump links under the title; one paper sheet per part. **Praktisk informasjon** (approved, [mockups/info-praktisk.html](mockups/info-praktisk.html)): Vielsen (in Strandebarm kirke, with its time) · Hardingasete og hyttene · Hvordan komme seg dit (address, route, bus, parking, map link) · Husregler · Antrekk · Ta med · Området rundt (FR-10; Rikke, 2026-11-15). The cabin times live in Programmet, not here. **Programmet** (approved, [mockups/info-program.html](mockups/info-program.html)): jump links Fredag · Lørdag · Søndag, the voluntary line, one sheet per day with a timeline of events (icon, time, short name) and «Godt å vite» (prices, what to bring, who covers what) (FR-9). **Vår historie** (approved, [mockups/info-om-oss.html](mockups/info-om-oss.html); called *Om oss* until 2026-11-15): one sheet without its own heading, with the couple's view photo, their own text in chapters (time · place lines), a closing line and their signed names |
| G3b | Gifts [If time] | Fourth topic row | Text and links |
| G4 | RSVP form, stepped | RSVP button, "Se eller endre svar", draft offer | One task per step (FR-13); last-updated header and conflict notice are states of G4. Rendered: [mockups/key-form-steps.html](mockups/key-form-steps.html) |
| G5 | Check page | Last form step | "Not sent yet", all answers, total, "Endre" per part, "Send svaret" (FR-21). Rendered: [mockups/key-check-page.html](mockups/key-check-page.html) |
| G6 | Receipt (thank-you page) | After sending | Rikke's text, summary, payment choice, closing line (FR-23, FR-34). Rendered with G7: [mockups/key-receipt.html](mockups/key-receipt.html) |
| G7 | Payment details | "Betal nå", status block | Amount, Vipps, account, payment message (FR-34, FR-71) |
| G8 | "Jeg har betalt" report | G7, status block | Report and later correct a payment (FR-35, FR-36) |
| G9 | Answer view, locked | «Se hele svaret» on the status block after the deadline | Read-only answers; payment, report, info, consent withdrawal still work (FR-42) |
| G10 | ~~Ask us~~ | — | **Removed 2026-11-15**: guests call or message the couple, whose numbers are in the footer (PRD FR-43 to FR-45) |
| G11 | Consent withdrawal | Answer view (G4/G9) **and** G12 (its last sheet lists each household member's allergy data with «Trekk samtykket for <name>») | Delete one person's allergy data (FR-30; memlog) |
| G12 | Privacy page | Footer "Personvern", consent text | The info-page frame (back link, title «Personvern», jump links, one sheet per part): Hva vi lagrer, og hvorfor · Hvem som ser det · Når det slettes · Rettighetene dine · Trekke samtykket. FR-66 and NFR-3 content in plain words; contacts in the footer. Approved in [mockups/privacy-1.html](mockups/privacy-1.html) |
| G13 | Envelope reveal [If time] | First visit to G2 | See Interaction Primitives |
| G14–G15 | Speech sign-up, English [If time] | — | Not specified further here |

**Navigation.** A sticky nav bar at the top of G2, G3 and G12 (on G12 no word is current): nav words Program · Praktisk · Vår historie on the left, a **"Svar" button** on the right; no hamburger (memlog, *Guest navigation*, *Front page redesign*; «Stedet» dropped with its page, 2026-11-15). The words open the info pages, matching the three topics (FR-8 gives each topic its own page). "Svar" — in the bar and as the link in the hero's deadline line — jumps to the RSVP sheet on G2 (`#svar`); from G3 it opens G2 at `#svar`. **Once the household has answered, the nav "Svar" keeps its label and goes to the household status block** (so does the hero's deadline-line link). The status block sits where the RSVP sheet was (decided 2026-11-15, Open Question 1). In the form (G4–G5) and on the receipt (G6) there is no nav bar: the progress line and "Tilbake" do the job (as rendered in the key-screen mockups). The footer band with phone numbers and "Personvern" is on every valid-link page, including error pages (FR-6).

**Receipt vs status block (decided).** After "Send svaret" the guest lands on a **separate receipt page** (G6). On later visits G2 shows the **household status block** (FR-24, FR-37) in the RSVP sheet's place, and the hero's deadline line reads «Svar sendt 12. oktober · Se svaret» (decided 2026-11-15, [mockups/answered-1.html](mockups/answered-1.html)). The receipt is not a persistent page.

### Admin surfaces (username + password)

| # | Surface | Reached from | Purpose |
|---|---|---|---|
| A1 | Login | Admin address | Username/password; slowed retries (NFR-4) |
| A2 | Home: Trenger oppfølging, answer progress, summary | After login, nav "Oversikt" | FR-56 list at the very top without scrolling; then «Svart: X av Y husstander» with «Se hva alle har svart» (FR-57); then the FR-54 summary in small panels. Approved render: [mockups/admin-rework-1.html](mockups/admin-rework-1.html); `.working/key-admin-overview.html` is the superseded first version (kept in `.working/`) |
| A3 | Count drill-down | Any count | The people behind the number (FR-55) |
| A4 | Gjester: all households (full overview and guest list in one) | Nav "Gjester", A2 «Se hva alle har svart» | **One page** for the full overview and the guest list (the full overview and the guest list merged into A4, Rikke 2026-11-15, [mockups/admin-guests-1.html](mockups/admin-guests-1.html)): search «Finn en gjest», «Legg til husstand», then one row per household: the name (link to its page, A6), a status tag («Ikke svart», «Stemmer ikke», «Endret») and one line with who comes, the total and payment. Unanswered first, then households that need follow-up, then by name (FR-49, FR-57) |
| A5 | Allergy list | A2, A4 | Consented names + categories for Hardingasete (FR-58) |
| A6 | Household page | A household in A4 or the search | Panels **Svar** (who sent and when, then each person's answers and a tappable phone number, «Endre svaret» → A7), **Betaling** (total, status tag, «Se betalingene» → A9), **Lenker** («Kopier lenke» per person, «Kopiert» beside it), **Husstanden** («Endre navn og kontaktinfo», tier 2; «Fjern husstanden» last and apart, tier 3). Rendered in [mockups/admin-guests-1.html](mockups/admin-guests-1.html). Only the couple can copy links. Helpers can neither see nor copy them (D14 decides whether links can be shown at all); move guest [T3], deactivate + new link [T3] (FR-49, FR-51, FR-57) |
| A6a | Add or edit a household | A4 «Legg til husstand», A6 «Endre navn og kontaktinfo» | One admin panel per person (fieldset with the name as legend; «Person 1» when new): «Navn» (required; hint «Slik navnet skal stå på invitasjonen.»), «Telefon (valgfritt)», «E-post (valgfritt)». «Legg til en person til» adds a fieldset and moves focus to its name field. Each person has «Fjern <name> fra husstanden» (Destructive, tier 3, typed FJERN; hidden when only one person is left, since a household may have one person). «Lagre husstanden» (new) or «Lagre endringene» (edit, tier-2 dialog naming what changes, e.g. that the payment message changes too, with the FR-71 duplicate warning); «Avbryt» as a link. Errors: error summary at the top and the error at the field; typed text is kept. Each person gets their own link when saved (FR-51). Approved in [mockups/admin-household-1.html](mockups/admin-household-1.html) (FR-49) |
| A7 | Household answer via the guest form | Household in A4/A6 | Admin as author, also after deadline (FR-63) |
| A8 | Consent registration [T3] | Household person | Who, channel, text version, when (FR-31) |
| A9 | Payments | Nav "Betalinger" (list), A6 «Se betalingene» (→ that household's payment page) | **List** of the households that come: panel «Til sammen» (Skal betales · Mottatt · Mangler · Skal betales tilbake), then one row per household (name link, status tags, «Totalt …, mottatt …», the guest's report if any), sorted stemmer ikke → skal ha tilbake → delbetalt → ikke betalt → betalt → ingenting å betale. **Household payment page**: Status (tags, Totalt, Mottatt, what the guest reported), Registrert (dated entries, each with «Angre»), Registrer betaling (Mottatt fra gjesten / Betalt tilbake til gjesten, Beløp, «Registrer» → tier-2 dialog naming the new status), Betalingsmelding (→ A10). After saving: «Registrert: mottatt 300 kr.» with «Angre», and the status recalculated. Approved in [mockups/admin-payments-1.html](mockups/admin-payments-1.html) (FR-59–61) |
| A10 | Payment message edit | «Endre betalingsmeldingen» on the household payment page | A field with the message; duplicate warning before saving (FR-71) |
| A11 | ~~Questions~~ | — | **Removed 2026-11-15** with G10 (PRD FR-43 to FR-45) |
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

Microcopy. "Decided" = memlog or the couple kept it in a render; all others are proposals **[forslag]** (final wording is Rikke's):

| Moment | Bokmål | Status |
|---|---|---|
| Nav button / hero deadline link | Svar · «**Svar** innen 4. januar 2028» (short form in the hero, no weekday or time) | decided |
| Full deadline (RSVP sheet, status block) | «Svar innen tirsdag 4. januar 2028 kl. 23:59» | decided (FR-41) |
| Hero lines | «inviterer dere til sitt bryllup» (du/dere rule: «inviterer deg til sitt bryllup») · «for Sigmund og bestemor» (replaces «Invitert: …») | decided |
| RSVP sheet heading and button | Svar på invitasjonen | render |
| Child-free line | Barnefritt bryllup | decided (Rikke removed «– vi håper dere får en fin helg for dere selv.», 2026-11-15) |
| Details heading | Alt om helgen | render (kept by Rikke through rounds 3–10) |
| Topic titles and lines | Programmet · «Hele helgen, dag for dag.» / Praktisk informasjon · «Reise, hyttene, tunet og området rundt.» / Vår historie · «Fra vi møttes til i dag.» | titles, «Vår historie» and «Fra vi møttes til i dag.» decided (Rikke renamed «Om oss», 2026-11-15); the other lines placeholders |
| Info page back links | «← Tilbake til invitasjonen» (top) · «Tilbake til invitasjonen» (bottom button) | decided (FR-11; kept by Rikke) |
| Praktisk informasjon parts | Vielsen · Hardingasete og hyttene · Hvordan komme seg dit · Husregler · Antrekk · Ta med · Området rundt | decided (Rikke, 2026-11-15); the texts inside are placeholders the couple writes |
| Jump links (Personvern) | Hva vi lagrer · Hvem ser det / Sletting · Rettighetene dine / Trekke samtykket | proposal (render, [mockups/privacy-1.html](mockups/privacy-1.html)) |
| Jump links (Praktisk informasjon) | Vielsen · Hardingasete / Komme dit · Husregler · Antrekk / Ta med · Området (shorter than the headings; `nav` labelled «Hopp til») | decided (Rikke picked variant 1, 2026-11-15) |
| Map link | Åpne veibeskrivelse i kart | proposal |
| Programme voluntary line | Alt i programmet er frivillig. Bli med på det dere har lyst til. | decided (Rikke, 2026-11-15) |
| Programme events | Fredag: Fjelltur · Hyttene er klare · Middag · Rebus · Badstue, stamp og mingling / Lørdag: Yoga · Frokost · Vi drar til kirka · Vielsen · Lunsj utenfor kirka · Middag og fest / Søndag: Frokost · Hyttene skal være tomme | decided names and order (Rikke); times placeholders |
| Paid item | «**Frokosten betales selv:** [x] kr.» | render (kept by Rikke); prices from Hardingasete |
| Drinks and hosting | «Lunsj og middag dekker vi. Det blir dessverre ikke åpen bar, men vi dekker drikke til maten og litt ekstra.» · «Til lunsjen serverer vi cider fra Hardanger.» | decided (Rikke's own words; «spanderer» and «betaler festen» rejected) |
| Vår historie chapters | Sensommeren 2021 · Trondheim / 2022 · Trondheim / 2023 · Trondheim / Høsten 2024 · Firenze / Starten av 2025 · Annecy / Våren 2025 · Italia / Høsten 2025 · Trondheim / Sommeren 2026 · Asia / Våren 2027 · Oslo | decided (Rikke rewrote her text so each paragraph opens with its time; «Våren 2027» hers) |
| Vår historie text | The couple's own words, [ux/innhold/Vår historie.docx](../../ux/innhold/V%C3%A5r%20historie.docx); «[stilling]» still to fill in | decided (theirs) |
| Optional activities | «Yoga er for den som vil. Ta med treningstøy.» · «Badstue og stamp er for den som vil. Ta med badetøy.» | decided |
| See or change answer | Se eller endre svar | decided |
| Helper read-only line | Du kan se alt, men ikke endre noe. | decided (Rikke, 2026-11-15) |
| Answered hero line | «Svar sendt 12. oktober · Se svaret» — «Se svaret» always jumps to the status block on the same page | decided (Rikke, 2026-11-15) |
| See the locked answer (after deadline) | «Se hele svaret» on the status block, opens G9. Not «Se svaret», which is the hero's jump to the status block | proposal (renamed 2026-11-15 after review A2-06) |
| Draft offer | Vil du fortsette der du slapp? · Ja, fortsett · Nei, begynn på nytt | question decided; buttons proposal |
| Draft notice on G2 | Du har et svar som ikke er sendt ennå. | proposal |
| I am [name] | Jeg er Sigmund · Bytt (accessible name "Bytt hvem som svarer"); in the panel «Hvem svarer?» and «Velg» *(added 2026-11-21 in Story 2.1)* | «Velg»: godkjent av Rikke 2026-11-23; the rest proposal |
| Coming / Not coming | Kommer / Kommer ikke | proposal |
| Step 2 question and choices | «Er alle som kommer, med hele helgen?» · «Ja, alle er med fra fredag til søndag» · «Nei, jeg velger dager for hver person» · after «Nei»: «Velg dagene for hver person» *(added 2026-11-23 in Story 2.2)* | decided (avgjort av Claude 2026-11-23: de følger FR-14 og FR-70 og formstegmønsteret i DESIGN.md, og ingenting i PRD eller DESIGN taler imot) |
| Step 2 day list | «**Fredag 26. mai**: Fjelltur, middag og rebus» · «**Lørdag 27. mai**: Bryllupsdagen: vielse, lunsj og fest» · «**Søndag 28. mai**: Frokost og hjemreise»; the checkboxes say «Fredag 26. mai» and so on *(added 2026-11-23 in Story 2.2)* | decided (avgjort av Claude 2026-11-23: de følger FR-14 og FR-70 og formstegmønsteret i DESIGN.md, og ingenting i PRD eller DESIGN taler imot) |
| Step 2 errors | «Velg «Ja» eller «Nei».» (summary: «Svar på om alle er med hele helgen») · «Velg minst én dag for <name>.» · «<name> kan ikke komme fredag og søndag uten lørdag, fordi dagene må komme etter hverandre. Velg lørdag også, eller bare én av dagene.» (summary for both: «Velg dager for <name>») *(added 2026-11-23 in Story 2.2)* | decided (avgjort av Claude 2026-11-23: de følger FR-14 og FR-70 og formstegmønsteret i DESIGN.md, og ingenting i PRD eller DESIGN taler imot) |
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
| Read more | Les mer (accessible name "Les mer om programmet" etc.) | render |
| Footer | Spørsmål? Send oss en melding: · Personvern | render |
| Lead-in | Vi gleder oss til å feire med deg/dere (du/dere rule; no exclamation mark in the approved render) | render |
| Error summary heading | For å gå videre må du rette opp følgende feil. | research (Designsystemet) |
| Notice prefixes | Feil: · Obs: | proposal |
| Page title | «Steg 3 av 6: Overnatting – Invitasjon»; «Feil: » first when the step has errors | proposal |
| Invalid link | «Dette er en privat invitasjon» · «Virker ikke lenken din? Ta kontakt med brudeparet direkte.» | decided (Rikke, 2026-11-15; the earlier proposal named Rikke and Valdemar, which FR-5 forbids) |
| Privacy page | Personvern · Hva vi lagrer, og hvorfor · Hvem som ser det · Når det slettes · Rettighetene dine · Trekke samtykket · «Trekk samtykket for bestemor» · the sentences in [mockups/privacy-1.html](mockups/privacy-1.html) | headings and structure decided; the sentences are proposals built on FR-66 and NFR-3 |
| Needs attention / Changed / Not answered | Trenger oppfølging / Endret / Ikke svart | proposal |
| Admin attention panel | «Trenger oppfølging (7)» · «Vis alle 7» · reasons e.g. «Betalingen stemmer ikke», «Har ikke svart ennå» · empty: «Ingenting trenger oppfølging nå» (with check icon) · «Vis håndterte» | proposal (render) |
| Admin guests (A4, A6) | «Finn en gjest» · «Legg til husstand» · «Alle gjester» · «Endre svaret» · «Se betalingene» · «Kopier lenke» · «Kopiert» · «Endre navn og kontaktinfo» · «Fjern husstanden» · tier 3: «Fjerne Sigmund og bestemor?», «Skriv FJERN for å bekrefte», «Avbryt» | proposal (render, [mockups/admin-guests-1.html](mockups/admin-guests-1.html)) |
| Admin payments (A9) | «Til sammen» · «Skal betales» · «Mottatt» · «Mangler» · «Skal betales tilbake» · «Alle betalinger» · «Registrert» · «Registrer betaling» · «Mottatt fra gjesten» / «Betalt tilbake til gjesten» · «Dagens dato settes selv.» · tier 2: «Registrere 300 kr mottatt fra Synne?», «Da er 900 kr av 900 kr mottatt, og Synne står som betalt. Du kan angre etterpå.» · after: «Registrert: mottatt 300 kr.» «Angre» · «Det stemmer nå.» · «Endre betalingsmeldingen» | proposal (render, [mockups/admin-payments-1.html](mockups/admin-payments-1.html)) |
| Admin answer progress | «Svart: 28 av 30 husstander» · «Se hva alle har svart» · rows Kommer / Kommer ikke / Ikke svart ennå | proposal (render) |
| Admin summary panels | Når kommer de? (Hele helgen (fre–søn) · Ikke hele helgen · Bare lørdag–søndag / Bare lørdag / Bare fredag–lørdag) · Overnatting (Overnatter ikke · Senger totalt) · Mat · Allergier (med samtykke) (Har allergier eller matbehov · Ingen allergier eller matbehov · Ingen allergiopplysninger lagret · «Én person kan ha flere allergier.») · Betaling (husstander som kommer) | proposal (render) |
| Refund owed | Where: count row on A2 and attention reason «Skal ha penger tilbake»; status tag «Skal ha tilbake 200 kr» (with the amount); A9 «Til sammen» row «Skal betales tilbake» (the couple's sum to pay back). Replaces the render's «Tilgode», which can be read both ways | proposal |
| Hike in admin summary | Panel «Fjelltur fredag», row «5 kommer, 2 kanskje». The render's «Fottur fredag» is replaced by the spine term «Fjelltur» | «5 kommer, 2 kanskje» decided (pattern); heading proposal |
| Undo | Merket som håndtert. Angre | "Angre" decided |
| Tier-2 consequence | e.g. «3 husstander mister tilgangen» | decided (example) |
| Tier-3 typed word | FJERN, for removing a household or one person («Skriv FJERN for å bekrefte»); matching ignores case. Delete all data [2027] gets its own word when it is designed | decided (Rikke approved FJERN in the render, 2026-11-15) |

## Component Patterns

Behavioural. Visual specs: DESIGN.md › Components (same names). Visual-only components (Back link, Outlined button on green, Helper read-only line) need no row here; the helper line's behaviour is in State Patterns.

| Component | Behavioural rules |
|---|---|
| Page | Static; no scroll effects or parallax. The nav bar is the only sticky element. |
| Nav bar | `<nav aria-label="Invitasjonen">` with a list of links; current page `aria-current="page"`. Sticky only while the viewport is ≥ 400 CSS px tall (see Accessibility Floor). Never collapses into a menu. |
| Nav "Svar" button | A link to `#svar` (works without JS). Jumps to the RSVP sheet; the next Tab lands on the RSVP button. Smooth scroll only under `prefers-reduced-motion: no-preference`, otherwise instant. |
| Hero sheet | The whole sheet — names, date, place, invited names and the short deadline with its "Svar" link — fits without scrolling at 360 × 560 (FR-7; measured 2026-11-14: sheet ends at 552px). The full deadline with weekday and time is next to the RSVP button (FR-41). Names are the page's `h1`; the invites line, date, place and household line are plain paragraphs. |
| Wax seal | Decorative image, `alt=""`; not a link. Same image as the favicon. |
| Flower divider | Decorative image, `alt=""`; never carries meaning. |
| Hero illustration | Short alt: «Akvarell av tunet på Hardingasete.» Never carries text. |
| Details section | «Alt om helgen» is a `section` labelled by its `h2`; the garlands are decorative (`alt=""`). Topics are a list in reading order: Programmet, Praktisk informasjon, Vår historie (Gifts last, if built). |
| Topic row | Topic title is `h3`. One "Les mer" per topic (accessible name "Les mer om programmet" etc.), a link that opens the topic's page (FR-8); no other buttons in the topic rows, so directions sit inside Praktisk informasjon. The picture is not a link **[ASSUMPTION]**. |
| Lace frame | Decorative wrapper; the photo inside has a short alt when it carries information (e.g. «Tunet på Hardingasete en kveld.»), and `alt=""` when the title says it all **[ASSUMPTION]**. |
| Lead-in | Static text; follows du/dere rule. |
| Info page | `h1` is the page title; the nav word for the page carries `aria-current="page"`. Back link first, then the jump links (where the page has more than one part; *Vår historie* has none), the parts in reading order, and the bottom back button. G12 (Personvern) uses the same frame. Static; nothing to fill in. |
| Jump links | A `nav` with `aria-label="Hopp til"` holding a list of in-page links (`#vielsen` …); the middle dots are `aria-hidden` spans, not read aloud. Following a link moves focus to the part: each target `section` has `tabindex="-1"` (no visible ring on it), and the `scroll-padding-top` on `html` (bar height + 12px) keeps its heading clear of the sticky bar. The same applies to `#svar` and `#status`. No script needed. Each balanced line is its own list, so a dot never starts a line; below 22.5em (360px at the default text size) each link takes its own line and the dots are hidden. *(Changed 2026-11-20 in Story 1.6: targets are cleared by the `html` scroll padding only, since a `scroll-margin-top` as well would add up with it; the dots are `aria-hidden` spans rather than CSS, since some screen readers read CSS `content` aloud; below 22.5em one jump link per line without dots, so a dot never starts a line: with the self-hosted EB Garamond the widest line «Komme dit · Husregler · Antrekk» needs about 320px (with 5px dot padding and no inline margin on the nav) plus the two 16px gutters, about 352px, rounded up for a margin; the breakpoint is in em so it follows a larger text size.)* |
| Decorative characters | Middle dots («Sensommeren 2021 · Trondheim», «Hardingasete · Hardanger») and the back-link arrow «←» are wrapped in `aria-hidden="true"` spans (or drawn with CSS), so screen readers do not read «midtpunkt» or «venstrepil». |
| Story sheet | A `section` labelled by the page's `h1` «Vår historie»; chapter lines are `h2`, so a screen-reader user can jump between chapters. The signature is plain text («Rikke & Valdemar»), not an image. The photo has a short alt («Rikke og Valdemar med utsikt.»). |
| Programme timeline | Each day is an `ol` in time order; the alternating sides are CSS only, so screen readers and the tab order read the events top to bottom. Times are `<time>` elements. Icons are decorative (`alt=""`). «Godt å vite» is an `h3` under the day's `h2`. No sign-up here: the hike is chosen in the RSVP form, the rest is information only (FR-9, Q6). |
| Info sheet | A `section` labelled by its `h2` (`id` = jump target). Facts come first in the sheet. «Åpne veibeskrivelse i kart» is a plain link to a map service with the address filled in, opened in the same tab **[ASSUMPTION — which map service and whether it leaves the site: architecture, privacy page]**. Photos carry a short alt (e.g. «Strandebarm kirke, en hvit trekirke med fjell bak.»). *(Changed 2026-11-20 in Story 1.6: the map link waits for Story 7.4, when the real address exists, and for a decision on the map service (AD-15, privacy page); the build has no map link until then.)* |
| RSVP sheet | Target of both "Svar" links (`id="svar"`; the `scroll-padding-top` on `html`, bar height + 12px, keeps it clear of the sticky bar). *(Changed 2026-11-20 in Story 1.6: this row said `scroll-margin-top`; since Story 1.5 the build clears every jump target with the `html` scroll padding alone, because the two would add up.)* Holds the child-free line, the full deadline and the RSVP button; shows the draft notice when an unsent draft exists on the device. |
| Primary button | The one distinct next step on a screen (NFR-6); repeats of the same action allowed. On submit it shows "Sender …" and ignores repeat taps until the server answers **[ASSUMPTION]**. In form steps, check page and receipt it comes **before** the secondary button, so "Fortsett" / "Send svaret" / "Betal nå" is first in reading and Tab order **[forslag]**. |
| Secondary button | Back, cancel, "Betal senere", "Nei, begynn på nytt". Never visually competes with the primary; in the form it sits below the primary. |
| Destructive button | Tier 3 only; never the default focus; placed apart from safe actions. |
| Focus ring | Shown on keyboard focus and on press; never hidden under the sticky bar (scroll padding, Accessibility Floor). |
| Text link / "Les mer" | Navigates; never submits or changes data (FR-3). |
| Footer band | Each phone number is its own `tel:` link row; "Personvern" opens G12. On every valid-link guest page, including errors (FR-6). |
| Text field | Label above, hint below, error between label and field. `aria-describedby` points to hint and error; `aria-invalid="true"` when in error. Forgiving input: amounts accept "900", "900 kr", "1 450" **[ASSUMPTION]**. No date or time pickers. Variants: multi-line (notes), search (A4 «Finn en gjest»; searches on submit, then a polite live region says «3 treff» or «Fant ingen med det navnet.»), typed confirmation (tier 3). |
| Choice control | Every group is a `fieldset` with the question as `legend`; its error sits inside the fieldset, right under the legend, as icon + «Feil: …» (no border on the group), and the fieldset's `aria-describedby` points to it. Whole row tappable. Attendance starts with nothing selected (FR-14); consent Ja/Nei starts unanswered (FR-26). **«Ingen allergier eller matbehov» is exclusive per person:** ticking it clears that person's category ticks, and ticking any category clears it; without scripts, if a person has both ticked when the step is sent, the step comes back with an inline error asking the guest to choose one **[ASSUMPTION — no-JS fallback]**. |
| Notice | Inline, never auto-dismissing on guest pages. Present at page load = not a live region; changes after load are announced (polite; errors assertive). |
| Error summary | After a failed "Fortsett" the page reloads with the summary focused; each item links to and focuses its field (FR-22); `<title>` starts with "Feil: ". Gone when errors are fixed. *(Changed 2026-11-21 in Story 2.1: "reloads" is a redirect, `/svar/?feil=1`, not a POST response, so Back never asks to resubmit; the valid choices are kept in the draft.)* |
| Status block | Shown on G2 once the household has answered, headed «Svaret er sendt»: «Sendt av <name> <weekday date> kl. <time>.», «Totalt for husstanden: …», «Meldt betalt: <amount>, <date>.» (only when a payment is reported), «Dere kan endre svaret fram til <deadline>.» (du/dere rule), then "Se eller endre svar" (before deadline) or «Se hele svaret» (after, opens G9) **[forslag — wording except the buttons]**. Content order: heading, the small gypsophila, «Barnefritt bryllup», then the lines above. **It is the target of the nav "Svar" once answered** (and of the hero link «Se svaret»); `id="status"`, focus lands on the block's heading. It sits in the RSVP sheet's place (decided 2026-11-15, [mockups/answered-1.html](mockups/answered-1.html)). |
| Draft offer | See Interaction Primitives › Unsent answer kept (FR-78). |
| Progress line | "Steg n av m: <step name>" right under the step `h1`. m changes only when an answer that adds or removes steps changes (who comes, which days). Moving forward or back alone never changes it. *(Added 2026-11-23 in Story 2.2: a person whose days are not chosen yet, or not allowed (Friday and Sunday without Saturday), counts as the whole weekend, so m never shrinks on a half-made choice.)* |
| Respondent line | Shown on **every form step**, under the progress line. Preset to the link owner (FR-12). "Bytt" is a button (`aria-expanded`, accessible name "Bytt hvem som svarer"), not a link. Switching changes only who is recorded as answering; filled answers stay **[ASSUMPTION]**. *(Changed 2026-11-21 in Story 2.1: «Bytt» is a `<details>`/`<summary>`, so it works without JavaScript; the summary gives the button role and the expanded state, and its accessible name is «Bytt hvem som svarer». The panel holds the fieldset «Hvem svarer?» with one radio per member, the current respondent chosen, and a secondary «Velg» button (godkjent av Rikke 2026-11-23). «Velg» posts the whole step, so the answers already chosen are kept in the draft without being checked, and the step reloads with the new name.)* |
| Running total | Recalculated by the server on every step, and with scripts also on every change (architecture AD-7), announced politely; removed choices drop out (FR-75); identical on check page and receipt (FR-33). |
| Read-more disclosure | Expands in place; `aria-expanded`; never navigates away (FR-19). |
| Consent block | Explanation (purpose, recipients, how to withdraw) comes **before** the Ja/Nei and is inside the fieldset, referenced from the legend. Starts unanswered, never pushed (CM-4). It covers everything on the step, including «Ingen allergier eller matbehov»: nothing from the allergy step is stored without it (architecture AD-18, Rikke 2026-11-16). "Jeg bekrefter at Marie vet om dette og er enig" only when answering for others (FR-27). Sending never requires consent (FR-28). The «Personvern» link in the consent text (FR-66) opens G12; «Tilbake» from there returns to the same step with the answers kept (the FR-78 draft). |
| Check-answers list | Page `h1` «Se over svaret før du sender», after the «Obs: Svaret er ikke sendt ennå.» notice **[forslag]**. One "Endre" per part; it jumps to that step and returns to the check page after "Fortsett"; each has hidden context ("Endre måltider"). Skipped optional answers show "Ikke oppgitt". |
| Receipt panel | Success notice with the `h1` «Svaret er sendt» and who sent it when; then the message by answer (coming / not coming), the summary and the total. If something is owed: "Betal nå" / "Betal senere", and the closing line is shown **at once, directly below them** (it does not wait for a choice); "Betal senere" adds that the link always shows what is left to pay. Nothing owed → no payment buttons; the closing line follows the summary (FR-23). The coming message is shown when at least one person in the household comes **[ASSUMPTION]**. |
| Payment details | Payment message is "Bryllup" + household names (FR-71). "Kopier" buttons are shown only where the clipboard is available; "Kopiert" in a polite live region until the next copy. If a copy fails, the value is selected with «Trykk og hold for å kopiere». Values are always plain selectable text. QR is [If time]. |
| Envelope reveal [If time] | See Interaction Primitives. |
| Admin nav | Plain links, `aria-current`, not sticky. |
| Attention panel | First thing on A2 under the Admin nav, `h2` «Trenger oppfølging (n)» (FR-56). Lists the FR-56 items; shows **as many as fit while the answer-progress line stays on the first screen** (two at 360 × 560 in the render) and then «Vis alle n», which shows the whole list on the same page **[ASSUMPTION — mechanism; the fixed count is set by measuring the build]**. Order of items **[ASSUMPTION]**: payment mismatches first (as rendered), then the rest. |
| Attention empty state | When nothing needs attention the panel reads «Ingenting trenger oppfølging nå» with a check icon (as its heading, so the page outline still says what the panel is) and «Vis håndterte» below; the answer progress moves up accordingly. |
| Answer progress | Top of A2's Svar panel: «Svart: X av Y husstander» (households that have sent, of all), a decorative bar, then the Kommer / Kommer ikke / Ikke svart ennå rows (persons · households, each a link), then «Se hva alle har svart» → A4 (FR-57). Rikke's most frequent check (memlog), so it must sit on the first screen. |
| Admin summary panel | Below the Svar panel, one panel per FR-54 group: **Når kommer de?** — Hele helgen (fre–søn); Ikke hele helgen, broken down by day combination (Bare lørdag–søndag, Bare lørdag, Bare fredag–lørdag …). **Overnatting** — Overnatter ikke first; Senger totalt as a secondary line. **Mat** — one count per meal (FR-73). **Allergier (med samtykke)** — Har allergier eller matbehov with one row per category; Ingen allergier eller matbehov; Ingen allergiopplysninger lagret (coming guests with neither). **Fjelltur fredag** — «5 kommer, 2 kanskje». **Betaling (husstander som kommer)** — Ingenting å betale, Ikke betalt, Delbetalt, Betalt, Skal ha penger tilbake (FR-60). "Stemmer ikke" is **not** a summary count: it is an attention item (FR-61) and a tag in A4. Example figures that add up: [mockups/admin-rework-1.html](mockups/admin-rework-1.html). |
| Admin summary row | Every count is a link to A3 (FR-55); zero counts show "0" and are not links. Hike: "kommer" and "kanskje" are separate counts, each its own link; "kanskje" is never added to "kommer" (FR-54, memlog). |
| Overview table | A4's household list: on phone one row per household (name as link, status tag, one summary line), on PC the same rows may become a real `<table>` (FR-48). Unanswered sort first. Each person's full answers are on the household page (A6). |
| Attention item | Reason, household and detail, one action: "Merk som håndtert" / "Merk som sett" (tier 1), with hidden context in its accessible name ("Merk som håndtert: Synne, betalingen stemmer ikke"). Leaves the list, under the addendum's leave rules, once «Angre» is gone (when the page is left). |
| Undo (in place) | The row is **replaced in place** by "Merket som håndtert. Angre" (no bar, no toast); focus moves to "Angre"; it stays until the page is left (no timer). Handled items can be found and unmarked through a "Vis håndterte" filter. |
| Status tag | Text first: "Ingenting å betale", "Ikke betalt", "Delbetalt, 300 kr mangler", "Betalt", "Skal ha tilbake 200 kr" (FR-60), "Endret", "Ikke svart", "Stemmer ikke" **[ASSUMPTION — bokmål wording]**. |
| Dialog | `role="alertdialog"`, labelled by its heading, described by the consequence sentence. Focus goes to the safe button (tier 2) or the heading (tier 3) and is trapped. On **cancel** it returns to the trigger. On **confirm** the trigger may be gone, so focus moves to the result message (a `role="status"` element with `tabindex="-1"`, e.g. «Registrert: mottatt 300 kr.», «Allergiopplysningene til bestemor er slettet.», «Husstanden er fjernet.» at the top of A4), which is also announced. Esc and a scrim tap = cancel. The dialog body scrolls at 200 % zoom. Used for tier 2 and 3, consent withdrawal and the guest leave warning. |

## State Patterns

| State | Where | Treatment |
|---|---|---|
| Saving | Send, report payment, admin saves | Button shows "Sender …"/"Lagrer …"; entered data stays on screen. |
| Saved | G6, G8, admin | Success notice with what was saved and when (NFR-1). |
| Save failed | Any submit | Error notice: what happened, that nothing is lost, "Prøv igjen", and (guest side) the couple's phone numbers. Input kept, also when the cause is an expired form token. *(Added 2026-11-21 in Story 2.1: a form step that fails the CSRF check is shown again with status 403, the posted choices kept and a focused error notice at the top: «Feil: Skjemaet ble ikke sendt. Det skjer når siden har stått åpen lenge, eller når nettleseren ikke tar imot informasjonskapsler. Det du fylte ut, står her fortsatt. Prøv igjen.» (godkjent av Rikke 2026-11-23); the phones are in the footer band.)* |
| Validation error | G4, G8, admin forms | Inline error with fix hint + focused error summary (FR-22). |
| Contradiction | G4 | Blocked with an explanation, e.g. staying overnight while coming only one day (FR-70). |
| Draft on device | G4 | Each step is kept on the device when the guest presses «Fortsett» (FR-78). The server checks every step but stores nothing before "Send svaret" (architecture AD-8). |
| Draft waiting | G2, G4 entry | G2: warning notice in the RSVP sheet. Opening the form: Draft offer first (Interaction Primitives). |
| Not sent yet | G5; leaving G4–G5 | Warning notice at top of G5 (FR-21). Leaving: in-page links open the leave dialog, and the browser shows its own leave prompt where supported. In-app browsers may skip that prompt; the device draft covers this case (FR-20, FR-78). |
| Last updated | Top of G4 when answered | Info notice "Sist endret av Arild, 3. november kl. 18:40" (FR-38). |
| Conflict | G4/G5 when another member sent after this form or draft began | Warning notice before sending: who, when, what differs; guest reviews, then sends or adjusts. No silent overwrite (FR-38). |
| Locked after deadline | G2, G4→G9 | The hero line keeps «Svar sendt … · Se svaret» (to the status block); the status block's button becomes «Se hele svaret» (→ G9); read-only answers; "Fristen gikk ut tirsdag 4. januar kl. 23:59" + contacts. Payment, "Jeg har betalt", info and consent withdrawal still work (FR-42). A waiting draft is not offered; the notice says the answer was not sent and to call the couple **[ASSUMPTION]**. *(Added 2026-11-21 in Story 2.1: until Story 4.3 builds the locked states, every `/<code>/svar/` address after the deadline shows a closed page in the error pages' frame: «Svarfristen har gått ut», «Fristen gikk ut <weekday date> kl. 23:59. Send oss en melding, så finner vi ut av det.», the back button and the footer phones (godkjent av Rikke 2026-11-23).)* |
| Never answered, after deadline | G2/G9 | The hero line becomes «Svarfristen gikk ut 4. januar · **Ring oss**» (link to the footer's phone numbers); the nav "Svar" goes to the RSVP sheet's place, which shows the deadline message and the contacts instead of the RSVP button; no answers and no payment block **[forslag]**. |
| Total changed after payment | G6/G8/status block | "Du har 300 kr igjen å betale" or "Rikke og Valdemar har fått beskjed og betaler tilbake 200 kr" (FR-36). |
| Allergies without consent | G5 | Warning: the allergy information will not be saved; tell the couple directly (FR-28). |
| Copy unavailable / failed | G7, A6 | Button hidden when unsupported; on failure the value is selected with «Trykk og hold for å kopiere». |
| No valid link | G1 | A single calm paper sheet; nothing personal. *(Changed 2026-11-21 in Story 1.8: also every other wrong address that does not start with a valid link, with status 404.)* |
| Error page | 404, 500, CSRF failure, 400 | G1's sheet with what happened, never Django's own page (FR-5, FR-6). Under a valid link (404, 500, CSRF): the outlined back button on green «Tilbake til invitasjonen» and the footer band with the couple's phones, and «Går det fortsatt ikke, send oss en melding.» Otherwise, and always for 400: nothing personal and «Går det fortsatt ikke, ta kontakt med brudeparet direkte.» Wording in DESIGN.md › No valid link and privacy page; it has no mockup; it was Claude's proposal and was approved as built (godkjent av Rikke 2026-11-23) *(added 2026-11-21 in Story 1.8)*. |
| Static fallback | G2 | Invitation text and RSVP button appear if scripts or animation fail [2027]; see Open Question 4. |
| Helper read-only | All admin | Action buttons **hidden**, not greyed (memlog). Forms show values as text. A line under the admin nav says so: «Du kan se alt, men ikke endre noe.» (Rikke, 2026-11-15, [mockups/helper-view-1.html](mockups/helper-view-1.html)). |
| Session expired | Admin | Login page with "Du ble logget ut fordi du var borte en stund."; expiry rule is Open Question 5. |
| Empty | Admin | A2: «Ingenting trenger oppfølging nå» with check icon + «Vis håndterte» (Component Patterns › Attention empty state). Elsewhere: "Ingen betalinger registrert ennå." · drill-down with 0: not a link **[ASSUMPTION — wording]**. |
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
| G11 | confirm · done («Allergiopplysningene til … er slettet.») · failed · nobody in the household has allergy data stored |
| G12 | static · withdrawal list (per person: data stored, or «Ingen allergiopplysninger lagret.») · without a valid link (from G1: the general parts only, no withdrawal sheet) |
| A1 | error · slowed · expired |
| A2 | attention list (first items + «Vis alle n») · empty attention · undo in place · all answered (30 av 30) · read-only (helper) |
| A3 | list · zero |
| A4 | normal · unanswered · mismatch · changed · search results · search empty · no households yet («Ingen husstander ennå. Legg til den første.») · read-only |
| A5 | empty ("Ingen allergier registrert ennå.") · list |
| A6 | normal · copied · copy failed · tier-3 delete · read-only (no links, no buttons) |
| A6a | new · edit · validation · tier-2 save confirm · tier-3 remove person · saved («Lagret.») · save failed |
| A7 | edit · after deadline · conflict |
| A8 | tier-2 confirm · read-only |
| A9 | list · nothing to pay yet («Ingen betalinger registrert ennå.») · register · validation (amount) · tier-2 confirm · saved + «Angre» · undo of an older entry (tier-2 dialog) · save failed · read-only |
| A10 | duplicate-message warning · read-only |
| A12 | tier-2 confirm (deadline lock-out count, price-change count) · read-only |

## Interaction Primitives

- **Tap, scroll, type.** No swipe gestures, long-press, drag, carousels, autoplay, hover-only controls or infinite scroll.
- **Jump to answer.** Both "Svar" links on G2 are same-page anchors to the RSVP sheet; the sticky bar never covers the target.
- **One step at a time** in the form: "Fortsett" forward, "Tilbake" back. Each step has its own address, so the browser's Back button is always safe: it shows the previous step with its answers, never a "resubmit form" prompt (Post/Redirect/Get or equivalent).
- **Fixed choices over free input** (allergies, days) — fewer errors for older guests, countable data for the couple (research §5).
- **Form step order** (Rikke, memlog; FR-14 sets steps 1–2 as two screens): 1 who is coming → 2 whole weekend? / days per person → 3 overnight → 4 meals → 5 allergies and consent → 6 Friday hike (only if someone comes Friday) → check page. There is **no arrival question**: the chosen days show when each guest arrives (FR-18 removed 2026-11-11). *(Added 2026-11-23 in Story 2.2: step 2 is one screen at one address. «Nei» shows the day groups on the same page after a round trip to the server (no JavaScript), at `#velg-dager`, so «Steg 2 av m» and «Tilbake» stay the same; most households answer «Ja» and never see the checkboxes.)*

### Unsent answer kept (FR-78, tier 1)

- Every step the guest completes is kept **on the guest's own device**, in a cookie tied to the personal link, so a call, an app switch or a Messenger reload loses nothing already moved past (architecture AD-8). Input typed on the current step, before «Fortsett», is not yet kept.
- When the guest comes back through their link and a draft exists: G2's RSVP sheet shows «Du har et svar som ikke er sendt ennå.» Opening the form by any route (either "Svar", the RSVP button, or a reload of a step) first shows the **Draft offer**: «Vil du fortsette der du slapp?», when it was started, "Ja, fortsett" (to the step they left, all answers filled in) and "Nei, begynn på nytt" (draft deleted; form starts from the household's sent answer, or empty).
- If someone in the household sent an answer after the draft began, the draft is still offered and the conflict notice appears before sending (FR-38).
- The draft is deleted when sending succeeds and on "Nei, begynn på nytt", and is not offered after the deadline. It works without scripts and holds everything entered, allergies included (Open Question 6, resolved). Where cookies are blocked the form cannot be sent at all, since the form protection needs a cookie; the error page then shows the couple's phone numbers.
- Guest pages have no time limit that loses input (WCAG 2.2.1): a send rejected for any reason keeps every answer, and pressing again works.

### Admin protection tiers (decided)

Principle: **prefer undo over "Er du sikker?"** wherever possible.

| Tier | Actions | Pattern |
|---|---|---|
| 1 Easily undone | Mark seen / handled in Trenger oppfølging | No confirmation; undo in place with "Angre" (no timer); unmark later via "Vis håndterte". |
| 2 Important | Register or correct a payment (also undoable, FR-59); «Angre» on an older registered payment (not the one just saved), edit household, deactivate link + new link, change deadline or settings, price change, move guest, register consent **[ASSUMPTION for the last two]** | Dialog stating the consequence in plain words: the new deadline in words and, if past or within two weeks, how many households are locked out (FR-64); number of households whose total changes (FR-65). |
| 3 Irreversible | Delete guest or household; delete all guest data [2027] | Typed confirmation: the label shows the exact word in plain text; matching ignores case and surrounding spaces; `autocapitalize="off" autocorrect="off" spellcheck="false"`; the button stays enabled and a mismatch gives an inline error. Destructive button placed apart, muted rust. |

Guest-side consent withdrawal: one confirmation dialog naming what is deleted: «Trekke samtykket for bestemor?», «Allergiopplysningene til bestemor slettes. Kjøkkenet får ikke vite om laktoseallergien.», «Avbryt» (focused) and «Slett allergiopplysningene» (Rikke approved the wording, 2026-11-15, [mockups/privacy-1.html](mockups/privacy-1.html)). Afterwards the sheet says «Allergiopplysningene til bestemor er slettet.» and the household is tagged «Endret» in admin.

### Envelope reveal [If time]

Green envelope closed with the couple's wax seal opens and unfolds into a **plain paper sheet** (no heart shape, no lace) that becomes the hero sheet; afterwards the envelope and folds are gone, but the sheet keeps its paper edge (DESIGN › Elevation & Depth; PRD addendum updated 2026-11-14). Acceptance:

- first visit only; skipped entirely under reduced motion, without scripts or without storage;
- "Hopp over" visible and focusable from the first frame;
- 5 seconds or less;
- the static invitation is in the page and readable by screen readers underneath, not hidden until the end;
- afterwards scroll and focus are at the top of G2.

## Accessibility Floor

Behavioural; contrast values live in DESIGN.md. Target WCAG 2.2 AA (NFR-5).

- **Reflow and zoom:** body ≥ 18px on guest pages (we use 20px), type built in `rem`; no horizontal scroll at 320px or at 200 % zoom, checked at 360 × 560, 320 × 568 and **180 × 320** (a phone at 200 %). The names stack instead of shrinking (DESIGN › Typography). Images never exceed their column, topic rows stack and the programme timeline becomes one-sided below set widths (DESIGN › Layout & Spacing › Narrow widths).
- **Sticky bar and focus (2.4.11):** `html { scroll-padding-top }` equals the bar's height + `{spacing.scroll-gap}`, so nothing reached by Tab or by a link lands under the bar; nothing sets `scroll-margin-top` as well, since the two would add up. The bar is **sticky only when the viewport is at least 400 CSS px tall and at least 20em wide** (320 CSS px at the default text size); on shorter, narrower or zoomed screens, and with a larger default text size, it scrolls away with the page, so a bar whose words wrap never covers a jump target. *(Changed 2026-11-20 in Story 1.5: the bar is sticky only when the layout is also at least 320 CSS px wide; narrower, as at 200 % zoom (about 180 CSS px) on a tall phone, the nav words wrap to several lines and a sticky bar would cover what a link jumps to, so it scrolls away as on short screens. After review the same day the width condition became 20em, so it also follows a larger default text size. The scroll padding sits only on `html`, inside the same condition; DESIGN.md's `scrollMarginTop` for the RSVP and info sheets is met by it, and setting both would double the gap.)*
- **Keyboard:** everything works by keyboard; `:focus-visible` ring always shown (DESIGN › Focus ring), never `outline: none`.
- **Targets:** ≥ 44 × 44px (`{spacing.target-min}`) on guest and admin pages; admin density never shrinks a target.
- **Structure:** `lang="nb"`; one `h1` per page (names on G2, the step question in the form, the page topic elsewhere), `h2` per section or panel, `h3` per topic in «Alt om helgen». Every field has a visible label; groups use fieldset/legend; errors per FR-22.
- **Page titles:** describe the page and step ("Steg 3 av 6: Overnatting – Invitasjon"), identical for every guest and without names (FR-4); prefixed "Feil: " when the page shows errors.
- **Announcements:** each step is a new page — focus starts at the top, or on the error summary when there are errors. Live regions only for in-page changes (running total, "Kopiert", conflict appearing).
- **Colour:** status, mismatch and errors never by colour alone (1.4.1): word + icon shape.
- **Forced colours (Windows high-contrast mode):** checked under `@media (forced-colors: active)`: illustration blend off, choice marks visible, buttons keep an outline, and paper sheets, admin panels and dialogs get a 1px `CanvasText` border so their edges survive (DESIGN › Elevation & Depth).
- **Input:** don't ask for what the link knows (3.3.7); admin login allows paste and password managers (3.3.8).
- **Time:** no guest time limit loses input; admin expiry per Open Question 5.
- **Motion:** only the [If time] envelope and the smooth jump to the RSVP sheet; both respect reduce-motion.

## Consent & Privacy UX

FR-25 to FR-31 and NFR-3/NFR-4 set the rules; the UX decisions are:

- The explanation (purpose, who sees it, how to withdraw) comes **before** the Ja/Nei (research §3.2), inside the consent fieldset (Component Patterns › Consent block).
- **Withdrawal lives in two places** (memlog): the answer view next to the allergies where consent was given, and the privacy page; it works after the deadline.
- The unsent draft (FR-78) is kept on the guest's device and deleted on send. Each step passes through the server, which stores nothing before "Send svaret" and stores allergy information only with consent (Open Question 6, resolved; architecture AD-8, AD-18).
- Mocks, screenshots and tests use fictional people only (NFR-3).

## Key Flows

Quality bar for every guest flow: each screen has one obvious next step (NFR-6).

### UJ-1: Bestefar Sigmund answers for himself and bestemor (Sigmund, 78, SMS link on his phone)

Quality bar (memlog override): the **whole journey from link to sent answer** must feel nice and simple, evenly at every step; the receipt is not singled out.

1. Opens the link → G2 (rendered in [mockups/front-page-3.html](mockups/front-page-3.html)). [If time: envelope on first visit, skippable.] On the first screen he sees a paper invitation: the seal, the farmyard, the names, «inviterer dere til sitt bryllup», the date, the place, «for Sigmund og bestemor» and «Svar innen 4. januar 2028» — and "Svar" twice: in the bar at the top and in the deadline line.
2. Scrolls past the lead-in to «Alt om helgen» between the lily garlands: three topics, each with a picture in a lace frame; may open one with "Les mer" — on Praktisk informasjon he taps «Komme dit» in the jump links to check the parking ([mockups/info-praktisk.html](mockups/info-praktisk.html)) — and return with "Tilbake til invitasjonen". The bar with "Svar" stays at the top while he scrolls.
3. Taps "Svar" (or reaches the RSVP sheet by scrolling), reads «Barnefritt bryllup», taps "Svar på invitasjonen" → G4 ([mockups/key-form-steps.html](mockups/key-form-steps.html)). "Jeg er Sigmund" is preset and stays visible on every step. Marks both "Kommer"; "Hele helgen?" → Ja.
4. Overnight, then meals, prices shown before choosing; opens "Les mer om hyttene" in place. Running total updates.
5. Allergies: "Ingen allergier eller matbehov" for himself; bestemor's categories; consent Ja; confirms she knows and agrees. Then the Friday hike step (they come Friday).
6. G5 «Se over svaret før du sender» says "Svaret er ikke sendt ennå"; he checks answers and total, presses "Send svaret" ([mockups/key-check-page.html](mockups/key-check-page.html)).
7. **Climax:** G6 says «Svaret er sendt» with the time, then confirms it in Rikke's words. He has understood every step, answered alone, and can see what he answered and what happens next ([mockups/key-receipt.html](mockups/key-receipt.html)).
8. Payment: "Betal nå" → G7 → pays → "Jeg har betalt" → G8 shows what he reported and when; or "Betal senere" → told the link always shows what he owes. «Du kan nå trygt lukke invitasjonen.» stands right under the two buttons from the start.

Failure: the phone rings at step 5 and Messenger reloads the page → he opens the link again, taps "Svar" and gets «Vil du fortsette der du slapp?» → "Ja, fortsett" puts him back on the allergies step with everything filled in. Send fails → error notice, answers kept, "Prøv igjen" and phone numbers. Wrong input → inline error + focused summary.

### UJ-2: Onkel Arild answers for a household where not everyone comes (Arild for Marie, Filippa, Leone)

1. "Jeg er Arild"; marks Arild, Marie, Filippa "Kommer", Leone "Kommer ikke" (nothing pre-ticked).
2. Next step: "Hele helgen?" → Nei; picks lørdag and søndag for Filippa; each day shows its date and what happens.
3. The form adapts: nothing more about Leone; Filippa offered only her days' meals; no Saturday breakfast for her; the overnight step says the cabin is booked for the whole weekend, so both nights are paid.
4. **Climax:** the check page lists exactly what he chose per person, and the total matches to the krone.
5. Sends and pays as UJ-1.
6. Two weeks later: status block → "Se eller endre svar"; header shows who answered and when; he changes; if the total goes up, he sees the remaining amount; if it goes down, the couple is notified and will refund the difference.
7. Marie opens her link: status block shows Arild answered and when, not an empty form.
8. The couple sees the household at the top of A2 under Trenger oppfølging (changed answer; «Skal ha penger tilbake», 200 kr), pays Arild back and registers the refund in A9; the tag becomes "Betalt" (UJ-5).

Failure: Marie opened the form before Arild sent → conflict notice before she can send. After the deadline → locked view with contacts. Contradiction (staying overnight while coming one day) → blocked with reason.

### UJ-3: Synne has lost her link and needs a change after the deadline

1. Synne messages Rikke.
2. Rikke, on her phone: Gjester (A4) → searches «Synne» → Synne's household page (A6) → «Kopier lenke» → sends it.
3. If the link went astray: deactivate + new link (tier 2 dialog: "Synnes gamle lenke slutter å virke. De andre i husstanden beholder sine."); the old link shows G1.
4. Synne opens the link after the deadline: «Se svaret» → the status block → «Se hele svaret» → G9, deadline message, contacts; she can still pay, report payment, read info and withdraw consent.
5. **Climax:** Rikke opens Synne's household in A7, the same form guests use, and makes the change after the deadline; it is recorded with Rikke as author.
6. Phone-reported allergy: Rikke sends the consent text, then registers consent in A8.

Failure: any error page still shows the couple's phone numbers (FR-6).

### UJ-4: Rikke checks the numbers and sends them to Hardingasete

Rendered: [mockups/admin-rework-1.html](mockups/admin-rework-1.html) (approved; replaces `.working/key-admin-overview.html`).

1. Logs in → A2. **First, without scrolling: «Trenger oppfølging»** (FR-56) — households that haven't answered, coming guests who haven't answered the allergy question, "Jeg har betalt" reports that don't match ("Stemmer ikke"), refunds owed, changed answers. The first items show, then «Vis alle n». She marks items handled → each row is replaced in place by "Merket som håndtert. Angre". When nothing needs attention, the panel says «Ingenting trenger oppfølging nå».
2. **Right below: «Svart: 28 av 30 husstander»** with «Se hva alle har svart» (A4, FR-57) — her most frequent check — then the summary (FR-54) in small panels: Svar (kommer / kommer ikke / ikke svart ennå, persons and households) · Når kommer de? (hele helgen, ikke hele helgen and which days) · Overnatting (overnatter ikke, senger totalt) · Mat (per meal) · Allergier (med samtykke) (per category, ingen, ingen allergiopplysninger lagret) · Fjelltur fredag («5 kommer, 2 kanskje») · Betaling (per payment status).
3. **Climax:** she trusts the numbers because every count opens the people behind it — taps "Fredag middag 38" → A3 lists the 38 people. She can also open «Gjester» (A4) and each household's page (A6) to check one household.
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
5. **Climax:** the guest link now shows the status block with «Se hele svaret», locked; the admin can still edit via A7.
6. Logs in as helper: no action buttons, and the line «Du kan se alt, men ikke endre noe.» under the nav.

Failure: logs in with wrong password → plain error, slowed retries.

## Inspiration & Anti-patterns

- **Lifted from the couple's images** ([inspirasjon.md](../../ux/inspirasjon/inspirasjon.md)): the cosy sheet feeling and the soft paper edge of the main sheet (01), green envelope (02, 05), colours and simple area drawings (03), sections separated rather than one uniform page (08), top links to jump to parts and "The finer details" with a framed picture beside each topic (09), colours, texture and dark wood (10, 12), the *Brudeferden i Hardanger* feeling (11). **The couple's own images** ([egne-bilder.md](../../ux/egne-bilder/egne-bilder.md); moved out of the inspiration folder and renumbered on 2026-11-15) are used on the site itself: illustration 04 (chosen from 01–05), the wax seal (06), gypsophila (07) and lilies (09, 10) from their wedding flowers, the lace frame (11), the photos of the couple (12 on the front page, 13 on *Vår historie*) and the programme icons (14). Reconciled per input in reconcile-inspirasjon.md, reconcile-stedet.md, reconcile-egne-bilder.md and reconcile-sources.md.
- **Lifted from research:** GOV.UK check-answers and confirmation patterns; Designsystemet error summary; deadline next to the RSVP button (Joy); personal link instead of name search.
- **Venue photos** ([stedet.md](../../ux/stedet/stedet.md)) are information for the topic frames and G3 pages, not style. Rikke has permission to use them on the site, including 18-Kirka.jpg (2026-11-16).
- **Rejected** (each is a choice the couple made against a proposal or an inspiration image; details in the memlog):

| Rejected | Why, in the couple's words where they gave them | Where it was tried |
|---|---|---|
| Heart-shaped or lace letter | «Gir ikke helt riktig følelse» | Inspiration 08 |
| Italian theme, olive plants | «Vi skal gifte oss i Norge» | Inspiration 01, 03, 07 |
| A special dress code; a modern look | No special dress code; «for enkelt og moderne». The *Antrekk* part only gives practical advice | Inspiration 09 |
| Clutter; grey | «Litt rotete»; «litt grått» | Inspiration 02, 04 |
| Bluish greens; dark green page; light sage page | Rikke picked the warm olive instead | Colour rounds 1, 4 and 6 |
| Gold, bling, neon, blinking, luxury feel | Brain dump | — |
| A light or chalk-white rim on the sheets; sprigs or seals drawn in code | Rikke's own images instead | Paper-ceremony rounds 1–3 |
| A cropped illustration | «Kuttet for mye» | Illustration rounds |
| Layered offset sheets | Dropped | Card-style round |
| A cabin-cosy rather than solemn look | Solemn and classic (memlog 100) | Front page rounds |
| Hamburger menu; flags for language; «Everyone is coming» pre-ticked | Accessibility and research | Discovery |
| An arrival question | Dropped from the form | Review 2026-11-11 |
| Plain cards below the hero | «For enkelt og trist» | `.working/finer-details-1.html` to `-10.html` |
| Stamp and double-line picture frames; oval or soft-faded pictures; lace drawn in code; white lace | «For harde»; cream lace from Rikke's image instead | Same rounds |
| A small-caps section heading; a separate Hardingasete topic; a Directions button on the front page | — | Same rounds |
| The «Spør oss» form | Guests call or message the couple | 2026-11-15 |
| Info pages: text straight on the green; a large underlined jump list; closed sheets that open like an accordion; a line of text under the title; a separate «Tider» sheet | «Rotete og stort»; «ikke så fint og koselig»; «overflødig» | `.working/info-praktisk-1.html` to `-6.html` |
| Programme: a time column, times above each event, two plain timelines; Claude's SVG trial icons | Not «like estetisk fine» as inspiration 09; Rikke made her own icons | `.working/info-program-1.html` to `-6.html` |
| The words «spanderer» and «betaler festen» | Felt wrong; the couple covers some of the drinks, not the party | Programme rounds |
| A soft colour filter on the photos | Rikke kept the photos as taken | `.working/photo-style-1.html` |

## Responsive & Platform

| Context | Behaviour |
|---|---|
| Phone 320–480px | The design. Nav bar sticky; nav words may wrap. Names on one line from about a 274px content box (360px phones: 288px); on 320px phones the narrower small-phone gutter and hero padding keep them on one line, and the whole hero fits the first screen (deadline line ends at 530px); they stack only on narrower layouts (see the 200 % zoom row). At 320px the three nav words stay on one line (bar 64px) with the tighter nav spacing below 340px (DESIGN › Layout & Spacing; re-measured 2026-11-15 with «Vår historie»). |
| Short or zoomed viewport (< 400 CSS px tall) | Nav bar not sticky. |
| 200 % zoom on a phone (~180 CSS px wide) | Gutter and hero padding 8px; names stacked; nav words wrap freely; no sideways scroll. |
| PC | Same phone column centred on the green page. Wider layout [If time]. |
| Admin on phone | Quick tasks fit one screen (FR-48); tables become stacked rows with visible labels. |
| Admin on PC | May use a wider column for A4 (FR-48) **[ASSUMPTION — width not set]**. |
| In-app browsers | Messenger/Facebook must work, checked on a real old device [2027]; the device draft covers reloads; copy buttons feature-detected. |
| No JavaScript | Every guest and admin page works without scripts, including the form steps, the draft and the confirmations (Open Question 4, resolved; architecture AD-1, AD-7). Running-total updates within a step, the leave warning and copy buttons need scripts. |

## Open Questions

Numbers stay fixed, because the memlog and the logs refer to them.

### Still open

7. Final bokmål for all microcopy marked "proposal" or **[forslag]** (Rikke).
9. Programme times and content placeholders.

### Resolved

- 1. Answered state of G2 — resolved 2026-11-15 ([mockups/answered-1.html](mockups/answered-1.html); IA › Receipt vs status block).
- 2. Small phones — resolved 2026-11-15 ([.working/small-phone-1.html](.working/small-phone-1.html); DESIGN › Layout & Spacing).
- 3. Plain-text names — resolved 2026-11-15: script only ([.working/plain-names-1.html](.working/plain-names-1.html)).
- 4. No-JS guest pages in v1 — resolved 2026-11-16 in the architecture: every guest and admin page, form steps included, works without scripts; scripts only enhance ([ARCHITECTURE-SPINE.md](../../architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md) AD-1, AD-7).
- 5. Admin session expiry — resolved 2026-11-16 (Rikke): 20 hours without use, renewed by every request; no warning and no restore of unsaved input; «Logg ut» on every admin page (AD-13).
- 6. Device draft content — resolved 2026-11-16 (Rikke): the draft holds everything entered, allergies included, until send or «Begynn på nytt». Each step passes through the server, which stores nothing before send (AD-8). «Ingen allergier eller matbehov» also needs consent to be stored (AD-18).
- 8. Why-guests-pay wording — resolved 2026-11-16 (PRD Q7 closed): older guests find paying fine, so FR-32's short, friendly note is enough; its final words are part of question 7.
- 10. Texture on the green page — resolved 2026-11-11 (DESIGN › Elevation & Depth).
- 11. Edge treatment of the sheets — resolved 2026-11-11: edge B3 (DESIGN › Elevation & Depth).
- 12. The front page below the hero — resolved 2026-11-15 ([mockups/front-page-3.html](mockups/front-page-3.html)).
- 13. Allergies entered without consent in the admin count — resolved 2026-11-15: no marker; the label is «Ingen allergiopplysninger lagret».
- 14. Child-free line in the answered state — resolved 2026-11-15: it stays in the status block.
- 15. How helpers see they are read-only — resolved 2026-11-15 ([mockups/helper-view-1.html](mockups/helper-view-1.html); State Patterns).
