> **Kort oppsummering (norsk)**
>
> - Hva er sjekket: to nye KI-gjennomganger av DESIGN.md og EXPERIENCE.md 15. november, etter infosidene, admin-sidene og personvern. Den ene sjekket at alt henger sammen og er komplett, den andre sjekket tilgjengelighet for bestefar Sigmund (78).
> - Antall funn: 0 kritiske, 5 høye, 16 middels og 23 lave (44 i alt). Noen funn går igjen hos begge.
> - Viktigst 1: ved 200 % zoom går tidslinja i programmet, temaradene på forsida og bildene i blonderamme ut over kanten. De trenger en regel for smale skjermer.
> - Viktigst 2: å legge til eller endre en husstand i admin har knapper, men ingen side. PRD-en (FR-24 og FR-57) beskriver fortsatt forsida og oversikten slik de var før dagens valg.
> - Viktigst 3: etter at man har bekreftet i en dialog, havner fokus på en knapp som ikke finnes lenger.
> - Resten er mest gammel tekst som ikke ble oppdatert etter dagens valg. Ingen samlet karakter gis.

# Validation Report — AI'll handle it

- **DESIGN.md:** `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md`
- **EXPERIENCE.md:** `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md`
- **Run at:** 2026-11-15T22:43

## Overall verdict

The spine pair is still a usable contract, and today's work landed well: every link, image path, source and token reference resolves, DESIGN.md keeps the spec's section order, and the new pages (info pages, admin «Gjester» and «Betalinger», no-valid-link and privacy pages) are specified and rendered. The rubric walker found no critical problems. What remains is drift: text that was not updated after today's decisions, two PRD requirements (FR-24, FR-57) that describe the UX as it was, and one admin surface (adding or editing a household) that has buttons but no page.

The accessibility review shifts the picture a little. The new components were specified with fixed pixel widths, so the 200 % zoom check (180 CSS px) that the spines themselves require now fails for the programme timeline, the front-page topic rows and the framed images. Focus after confirming a dialog goes to a button that no longer exists. Two of the spines' own rules are broken by new pages: 18px cream text on the textured green in admin, and 40px jump links against the 44px target floor. None of the 2026-11-11 fixes has regressed.

## Category verdicts

- Flow coverage — adequate
- Token completeness — strong
- Component coverage — adequate
- State coverage — adequate
- Visual reference coverage — adequate
- Bloat & overspecification — adequate
- Inheritance discipline — adequate
- Shape fit — strong

## Findings by severity

Counts combine the rubric walker and the accessibility reviewer: critical 0, high 5, medium 16, low 23.

### Critical (0)

### High (5)

**[Accessibility reviewer]** — A2-01 · The two-sided timeline has no narrow-width rule. (§ DESIGN › frontmatter `programme-timeline`, `programme-icon`; Components › Programme timeline; EXPERIENCE › Accessibility Floor (180 × 320 check))  
The two-sided timeline has no narrow-width rule. Spine arithmetic at 180px layout width (Sigmund at 200 %): 180 − 2 × 8 gutter − 2 × 22 sheet padding = 120px, so each half is 60px, and minus the 18px gap to the line each event column is **42px**. The **56px icon** does not fit, and neither do words like «Hyttene» or «Badstue,» in 20px italic. The 180px render confirms it: «Hyttene er klare» is cut off at the sheet edge, and icons push past their column. The overlap of 36px also assumes events of fixed height.  
Fix: Add a narrow layout: below 260px layout width (or whenever an event column would be under ~90px), use **one side only**, with the line and dots along the left edge, all events left-aligned and no overlap. Icons could optionally go to 40px. State it in Components › Programme timeline and add «the programme at 180px» to the check list in Layout & Spacing.

**[Accessibility reviewer]** — A2-02 · The new components are built from fixed px widths with no `max-width` rule: (§ DESIGN › frontmatter `topic-row`, `lace-frame`, `hero-illustration`, `lily-garland`, `flower-divider`; Layout & Spacing › Front-page order, Info pages)  
The new components are built from fixed px widths with no `max-width` rule: illustration 262px, lily garland 296px, gypsophila 224/180px, lace frame 136px in topic rows and 220px on info sheets. At 180px the hero content box is 148px and the info-sheet body is 120px, so the illustration and the 220px frame overflow (render: the church photo runs past the sheet edge). The topic row is fixed side by side: 136px frame + 14px gap leaves **about 10px** for the title, line and «Les mer» (render: title and button clipped off-screen). Sigmund at 200 % cannot open the info pages from the front page.  
Fix: Add a general rule in Layout & Spacing: every image is `max-width: 100%; height: auto`, and stated widths are maximums. **Topic row stacks** (picture centred above the text) below about 300px layout width. On info sheets use `width: min(220px, 100%)`. Re-run the 180 × 320 check on front-page-3, info-praktisk, info-program and info-om-oss, and record the result as was done for the names.

**[Accessibility reviewer]** — A2-03 · Returning focus to the trigger only works on **cancel**. (§ EXPERIENCE › Component Patterns › Dialog («… is trapped, and returns to the trigger»); Admin protection tiers (guest consent withdrawal); IA › A9 («After saving: «Registrert: mottatt 300 kr.» with «Angre»»); DESIGN › Layout › Betalinger)  
Returning focus to the trigger only works on **cancel**. After **confirm** the trigger is gone or meaningless. «Trekk samtykket for bestemor» disappears when the data is deleted. «Fjern husstanden» goes away with the household page. After «Registrer 300 kr» the useful place is the new confirmation panel, not the form button. Focus then falls to `body`, and a screen-reader or keyboard user gets no confirmation and loses their place. If saving is a server round trip, the render's `role="status"` confirmation is present at page load and **not announced**, which the spine's own Notice rule says («Present at page load = not a live region»). What «Angre» on that confirmation does to focus and announcements is also unspecified.  
Fix: In Component Patterns › Dialog, split the rule into cancel (return to trigger) and confirm. On confirm, focus goes to the result message: «Allergiopplysningene til bestemor er slettet.», «Registrert: mottatt 300 kr.», or on delete the «Gjester» page with a confirmation line such as «Sigmund og bestemor er fjernet.» (`tabindex="-1"`). Whether this happens in place or on a new page, the message receives focus. After «Angre», replace the message with «Angret.» and keep focus there. Add these to Surface coverage (G11 done, A6 deleted, A9 undo).

**[Flow coverage]** — R2-01 · FR-24 still says that once a household has answered, the invitation shows the status "near the top": (§ PRD FR-24 vs EXPERIENCE › IA › *Receipt vs status block*; DESIGN › Layout › *Answered state*)  
FR-24 still says that once a household has answered, the invitation shows the status "near the top": who sent it and when, the total, what has been reported paid, and the deadline. The decision of 2026-11-15 (OQ1) puts only «Svar sendt 12. oktober · Se svaret» in the hero. The full status sheet replaces the RSVP sheet at the **bottom** of G2. The PRD has no change-log row for this decision, so a story writer reading FR-24 would build a status block at the top. This also weakens plan-to-code traceability, which the course grades.  
Fix: Update FR-24 (status sent line in the hero, full status sheet in the RSVP sheet's place) and add a 2026-11-15 change-log row that cites `.working/answered-1.html` and the memlog decision.

**[State coverage]** — R2-02 · FR-49 (tier 2: (§ EXPERIENCE › IA A4 («Legg til husstand»), A6 (*Husstanden*: «Endre navn og kontaktinfo»); State Patterns › Surface coverage)  
FR-49 (tier 2: add, edit and remove households **and guests one by one**) has entry points but no surface. Nothing says where «Legg til husstand» and «Endre navn og kontaktinfo» lead, which fields they have (household name, one row per person with name, optional phone and email), how a person is added to or removed from a household, what validation applies, or how saving works. Only «Fjern husstanden» (tier 3) is specified. Removing a single guest has no control at all. No render covers this, and Surface coverage has no row for it. A builder cannot build it from the spines.  
Fix: Add a surface, for example "A6b Household edit": fields, per-person rows with «Legg til person» / «Fjern person» (and the tier that applies), validation and errors, the tier-2 dialog for an edit, and the states (new · edit · validation · saved · read-only). Add a microcopy row for it.

### Medium (16)

**[Accessibility reviewer]** — A2-04 · The spine's own rule is that cream text **under 19px** may stand only on the **flat** nav bar, because the measured worst case on the tex… (§ DESIGN › Components › Admin nav («Reuses Nav words on the green page»); Layout › Gjester / Betalinger («the count «30 husstander · 70 gjester»», back links «Alle gjester», «Alle betalinger»); Elevation & Depth › Paper texture; Do's and Don'ts)  
The spine's own rule is that cream text **under 19px** may stand only on the **flat** nav bar, because the measured worst case on the textured green is 4.50:1 with no headroom. Admin pages are the textured green (Page: «with the calm paper texture»). Yet the admin nav reuses the 18px nav words on it, and the count line and back links are `admin-body` 18px. The renders do exactly this (`.screen.tex-green` with 18px cream nav, count and back link). This applies to every admin page.  
Fix: Pick one: (a) put the admin nav, back link and title area on a **flat** `page-green` band, as the guest nav bar does; or (b) set admin cream-on-green text to ≥ 20px (`body`). Name an **Admin back link** component, add the count line to the Components table, and add «Cream text under 19px on the admin green» to Don'ts.

**[Accessibility reviewer]** — A2-05 · The spines contradict each other. (§ DESIGN › frontmatter `jump-links.rowHeight: 40px`; Components › Jump links («each ≥ 40px tall»); EXPERIENCE › Accessibility Floor › Targets («≥ 44 × 44px … on guest and admin pages»))  
The spines contradict each other. Jump links are set to 40px high, while the floor (and PRD NFR-5) requires 44px for every guest target. The lines are stacked with no gap, so each word's target is 40px tall. UJ-1 step 2 has Sigmund tapping «Komme dit» on exactly this control. The memlog records the visual pick (variant 1) but no decision to make an exception to 44px.  
Fix: Set `rowHeight` to 44px (three lines on Praktisk add 12px), or record a deliberate NFR-5 exception in the memlog and the PRD. Do not leave the conflict unresolved.

**[Accessibility reviewer]** — A2-06 · «Se svaret» means two different things. (§ EXPERIENCE › Receipt vs status block («Svar sendt 12. oktober · Se svaret»); Microcopy «See answer (after deadline) — Se svaret»; State Patterns › Locked after deadline («Button becomes "Se svaret"»); Component Patterns › Status block)  
«Se svaret» means two different things. In the answered hero it is a same-page jump to the status block, which shows a summary and another button, «Se eller endre svar». After the deadline, «Se svaret» opens the locked answer view (G9). Sigmund taps «Se svaret» expecting to see his answers and lands on a summary sheet with a differently worded button. For him that is one tap too many and two names for one thing.  
Fix: Either make the hero link go where its words say (the answer view, same target as the status block button), or name the jump for what it does, e.g. «Svar sendt 12. oktober · Se status». Keep «Se svaret» for the G9 view only. Update the Microcopy table so each label has one meaning.

**[Accessibility reviewer]** — A2-07 · The stated fallback cannot happen. (§ DESIGN › frontmatter `paper-sheet.fallback` («flat panel-cream … under forced-colors»); Elevation & Depth; Components › Dialog, Programme timeline; EXPERIENCE › Accessibility Floor › Forced colours)  
The stated fallback cannot happen. Under forced colours `panel-cream` is replaced by `Canvas`, the same colour as the page, so sheets, admin panels and **dialogs lose their edges** (none has a border). The scrim also becomes `Canvas` at 60 %, so a dialog over it has no visible boundary. The timeline line and dots are drawn as backgrounds and vanish (decorative, but the events then float). The floor's forced-colours list covers only the illustration, choice marks and buttons.  
Fix: Give sheets, admin panels and dialogs a `1px solid transparent` border (forced colours paints it `CanvasText`). Draw the timeline line as a border, not a background. Correct the fallback wording, and add «sheets, panels and dialogs keep an edge» to the Accessibility Floor forced-colours line.

**[State coverage]** — R2-03 · This row is stale after OQ1 and OQ14. (§ EXPERIENCE › Component Patterns › Status block)  
This row is stale after OQ1 and OQ14. It still ends with "Placement on G2: Open Question 1", but OQ1 is resolved. It also leaves out what DESIGN › Components › Status block and the memlog now fix: the sheet is centred, has the small gypsophila, and keeps «Barnefritt bryllup» under the heading.  
Fix: Replace the last sentence with the resolved placement (in the RSVP sheet's place, `id` = target of nav "Svar" and «Se svaret»). Add «Barnefritt bryllup» to the content order.

**[Component coverage]** — R2-04 · «Se svaret» means two different things. (§ DESIGN › Layout › *Answered state*; EXPERIENCE › Voice and Tone (row "See answer (after deadline)"); Component Patterns › Status block)  
«Se svaret» means two different things. In the answered hero line, before the deadline, it jumps to the status sheet on G2. Elsewhere it is the after-deadline label that opens the locked answer view G9. The status sheet's own button reads «Se eller endre svar» before the deadline. The answered hero line («Svar sendt 12. oktober · Se svaret») is also missing from the microcopy table.  
Fix: Give the hero link its own row in Voice and Tone (decided, Rikke 2026-11-15). Either rename one of the two uses, or state that the hero link always goes to the status sheet and that only the sheet's button goes to G4 or G9.

**[State coverage]** — R2-05 · The locked states of G2 only say that "the button becomes «Se svaret»". (§ EXPERIENCE › State Patterns › *Locked after deadline*, *Never answered, after deadline*; Surface coverage G2)  
The locked states of G2 only say that "the button becomes «Se svaret»". They do not say what the hero deadline line («**Svar** innen 4. januar 2028») or the nav "Svar" button show, or where they point, after the deadline. This matters most for a household that never answered, where the RSVP sheet has no form to open.  
Fix: Add the hero line text and the nav "Svar" target for both locked states, for example «Svarfristen gikk ut 4. januar» with the link to the locked sheet.

**[Shape fit]** — R2-06 · OQ13 contradicts itself: (§ EXPERIENCE › Open Questions 13; Key Flows › UJ-4 step 2)  
OQ13 contradicts itself: "The admin label is «Ingen allergiopplysninger lagret» instead of «Ingen allergiopplysninger lagret»". The old label «Har ikke svart på allergier» was lost in the edit. UJ-4 step 2 still lists the old label ("…ingen, har ikke svart på allergier"), although the memlog says the UJ was updated.  
Fix: In OQ13 write "instead of «Har ikke svart på allergier»". In UJ-4 step 2 use «Ingen allergiopplysninger lagret».

**[State coverage]** — R2-07 · The search field moved to A4 («Finn en gjest») when A4 and A6 were merged, but both spines still place the search variant on A6. (§ EXPERIENCE › Component Patterns › Text field ("search (A6 …)"); DESIGN › Components › Text field ("search (A6)"); EXPERIENCE › Surface coverage A4, A6)  
The search field moved to A4 («Finn en gjest») when A4 and A6 were merged, but both spines still place the search variant on A6. Surface coverage still gives A6 a "search empty" state, and A4, which now has the search, has no search-empty or empty-list state.  
Fix: Change "A6" to "A4" in both Text field rows. Move "search empty («Fant ingen med det navnet.»)" to the A4 row, and add "no households yet" to A4.

**[Component coverage]** — R2-08 · The row marked **decided** says the typed word is "the household name, or SLETT". (§ EXPERIENCE › Voice and Tone, row "Tier-3 typed word" vs row "Admin guests (A4, A6)")  
The row marked **decided** says the typed word is "the household name, or SLETT". The approved render (`mockups/admin-guests-1.html`), the memlog decision of 2026-11-15 and the A4/A6 microcopy row all use «Skriv FJERN for å bekrefte». A builder cannot tell which one is right.  
Fix: Make the tier-3 row say FJERN for removing a household, and state the word for "delete all data" [2027] separately, or drop that part.

**[Flow coverage]** — R2-09 · Since A4 and A6 were merged, the "full overview" is a list with one summary line per household, and each person's answers are on separate… (§ PRD FR-57; EXPERIENCE › Key Flows › UJ-4 step 3)  
Since A4 and A6 were merged, the "full overview" is a list with one summary line per household, and each person's answers are on separate household pages. FR-57 still describes one overview with every household's and person's answers, contact details, total and payment. UJ-4 step 3 says Rikke "can also open the full overview and count for herself", which the merged list no longer supports. The PRD has no change-log row for the merge.  
Fix: Update FR-57 (list plus household page) with a change-log row, and reword UJ-4 step 3. The other option is to state that the PC `<table>` variant shows the per-person answers.

**[Component coverage]** — R2-10 · The spines contradict each other. (§ DESIGN frontmatter `components.jump-links.rowHeight: 40px`; DESIGN › Components › Jump links ("each ≥ 40px tall"); EXPERIENCE › Accessibility Floor › Targets)  
The spines contradict each other. The Accessibility Floor requires targets of at least 44 × 44px (`{spacing.target-min}`) on guest and admin pages, but the jump links are specified at 40px.  
Fix: Use `{spacing.target-min}` for the jump-link rows, re-measure the 120px block, or write a documented exception (WCAG 2.5.8 needs only 24px) into the Accessibility Floor.

**[Visual reference coverage]** — R2-11 · Six approved decisions rely only on `.working/` files: (§ DESIGN › Layout (*Answered state*, small phones, Elevation › admin edge), DESIGN › Components › Status block, Helper read-only line; EXPERIENCE OQ1–3, OQ15, State Patterns › Helper read-only)  
Six approved decisions rely only on `.working/` files: `answered-1.html`, `helper-view-1.html`, `small-phone-1.html`, `admin-edge-1.html`, `plain-names-1.html` and `photo-style-1.html`. The workspace convention is approved renders in `mockups/` and working rounds in `.working/`. The answered status sheet and the helper line have no render in `mockups/`, even though the memlog lists them as "mocked". If `.working/` is tidied away for repo hygiene, these links break.  
Fix: Promote `answered-1.html` and `helper-view-1.html` (at least) to `mockups/` and update the links. Alternatively, state once in both headers that `.working/` files cited as "Rikke chose" are the record of the decision and are kept.

**[Component coverage]** — R2-12 · The new admin pages use pieces that have no component row or frontmatter key. (§ DESIGN › Components; DESIGN › Layout (*Gjester*, *Betalinger*); frontmatter `components`)  
The new admin pages use pieces that have no component row or frontmatter key. The **admin panel** itself (straight edge, paper texture, `admin-panel-padding`) has none. Neither do the household-page panels (*Svar*, *Betaling*, *Lenker*, *Husstanden*), the A9 «Til sammen» summary rows, the registration form, and the saved-confirmation panel («Registrert: mottatt 300 kr.» + «Angre»). The admin page title is "cream on the green (28px)", but there is no 28px type token (`heading-page` is 32px, `admin-heading` 22px).  
Fix: Add an `admin-panel` key and Components row. Add rows (visual and behavioural) for the A9 summary row and the saved confirmation. Add an `admin-title` type token, or point the title at an existing one.

**[Inheritance discipline]** — R2-13 · G1 has no footer, a deliberate choice under FR-5 (no phone numbers). (§ EXPERIENCE › IA G1; PRD FR-66)  
G1 has no footer, a deliberate choice under FR-5 (no phone numbers). FR-66 says the privacy page "is linked from the bottom of every page", so G1 now breaks that rule without saying so.  
Fix: State the exception in the G1 row. Either add a bare «Personvern» link to G1 (it carries no personal data), or narrow FR-66 to valid-link pages in the PRD.

**[State coverage]** — R2-14 · The new surfaces are thinly covered. (§ EXPERIENCE › State Patterns › Surface coverage (A9, G11, G12))  
The new surfaces are thinly covered. **A9** lists only "register · undo · read-only". It has no list-empty state (the State Patterns row "Ingen betalinger registrert ennå." is not linked to it), and it lacks the tier-2 confirm, amount validation and save-failed states. **G12** is listed as "static", but its last sheet is interactive and the render shows a "nothing stored" row («Ingen allergiopplysninger lagret.»). **G11** has no state for a household where nobody has consented allergy data.  
Fix: Extend the rows: A9 "list · list empty · register · tier-2 confirm · validation · saved + Angre · save failed · read-only". G12 "static · withdrawal list · nothing stored". G11 adds "nothing to withdraw".

### Low (23)

**[Accessibility reviewer]** — A2-08 · A plain `#id` link to a `section` moves the scroll position and the sequential-focus start point, but not focus itself. (§ EXPERIENCE › Component Patterns › Jump links («moves focus to the part … No script needed»); Status block («focus lands on the block's heading»))  
A plain `#id` link to a `section` moves the scroll position and the sequential-focus start point, but not focus itself. Some screen readers stay where they were. The spine promises focus without saying how.  
Fix: Make the targets focusable without script: `tabindex="-1"` on each part's `section` (or link to the `h2`). Same for `#svar` / `#status`. Specify that these targets show no focus ring, or a subtle one.

**[Accessibility reviewer]** — A2-09 · The programme times, including when the wedding starts, use `small` (18px), which the spine reserves for text nobody acts on. (§ DESIGN › frontmatter `programme-timeline.time` (`small`); Typography › Small («Only text nobody acts on»))  
The programme times, including when the wedding starts, use `small` (18px), which the spine reserves for text nobody acts on. 18px meets the floor, but these are the key facts of the page, set in the smallest guest type.  
Fix: Set times in `body` (20px) with lining figures, or reword the `small` rule to allow it.

**[Accessibility reviewer]** — A2-10 · «Godt å vite» holds the prices and what to bring, but the spines give it only a type style, not a heading level. (§ DESIGN › frontmatter `good-to-know.heading` («{typography.body}, italic»); Components › «Godt å vite»; EXPERIENCE › Programme timeline)  
«Godt å vite» holds the prices and what to bring, but the spines give it only a type style, not a heading level. The render uses `h3`, which is right, but nothing requires it.  
Fix: State `h3` «Godt å vite» under each day's `h2`, so screen-reader users can jump to the prices.

**[Accessibility reviewer]** — A2-11 · Middle dots and the arrow are real characters in the text. (§ EXPERIENCE › Microcopy «Vår historie chapters» («Sensommeren 2021 · Trondheim» as `h2`); Back link «← Tilbake til invitasjonen»; hero «Hardingasete · Hardanger»)  
Middle dots and the arrow are real characters in the text. Screen readers may read them as «midtpunkt» and «venstrepil», which matters most in the nine chapter headings that a user lists by heading. (The jump-link dots are already CSS.)  
Fix: Wrap decorative `·` and `←` in `aria-hidden="true"` spans, or draw them with CSS. Say so once in Component Patterns.

**[Accessibility reviewer]** — A2-12 · Two issues. (§ DESIGN › Components › Jump links («no underline», «decorative middle dot between words on the same line»))  
Two issues. (1) Small capitals with no underline and no button shape give Sigmund no sign that the words can be tapped; he relies on them in UJ-1. (2) A dot drawn by `li + li::before` cannot know where lines wrap. At 320px and 180px the renders show lines that start with «· ANTREKK» and «· LØRDAG».  
Fix: (1) Add a faint underline or the current-page style on press or focus, or a short lead word «Hopp til:» above. (2) Specify how separators handle wrapping: one list per balanced line, as the renders do, or hide the dot at line starts.

**[Accessibility reviewer]** — A2-13 · The spine contradicts itself. (§ EXPERIENCE › Microcopy «Tier-3 typed word — the household name, or SLETT — decided» vs «Admin guests» row and memlog 2026-11-15 («typed FJERN»))  
The spine contradicts itself. Typing a household name such as «Arild, Marie, Filippa og Leone» on a phone keyboard is error-prone. FJERN is the word actually chosen.  
Fix: Update the tier-3 row to «FJERN» (or one fixed short word for all tier-3 actions).

**[Accessibility reviewer]** — A2-14 · The search moved to A4 «Gjester», but the spine still places it on A6. (§ EXPERIENCE › Text field variants («search (A6, …)»); Surface coverage «A6 · search empty»; IA › A4)  
The search moved to A4 «Gjester», but the spine still places it on A6. Nor does it say whether results filter live (then a polite count or «Fant ingen med det navnet.» must be announced) or on submit.  
Fix: Move the search to A4 in both places, and specify submit-based search or a polite live result count.

**[Accessibility reviewer]** — A2-15 · «Angre» on an older registered payment removes a financial record with no confirmation, and the spine gives no way to restore it, althoug… (§ EXPERIENCE › IA › A9 («Registrert (dated entries, each with «Angre»)»); Admin protection tiers)  
«Angre» on an older registered payment removes a financial record with no confirmation, and the spine gives no way to restore it, although tier 2 lists «correct a payment».  
Fix: Treat «Angre» on a past entry as tier 2 (a dialog naming the new status), or make it reversible in place («Angret. Gjør om»).

**[Accessibility reviewer]** — A2-16 · A link to the privacy page inside the consent step takes Sigmund out of the form mid-answer: (§ EXPERIENCE › IA › G12 («Reached from … consent text»); Component Patterns › Consent block)  
A link to the privacy page inside the consent step takes Sigmund out of the form mid-answer: the leave dialog appears, and coming back depends on the draft. That conflicts with the spirit of «never navigates away» (FR-19) for in-form explanations.  
Fix: Since the consent block already holds purpose, recipients and withdrawal, drop the in-form link, or open it as a Read-more disclosure. If it stays, state that returning lands on the same step with answers kept.

**[Accessibility reviewer]** — A2-17 · The spine does not say what the **hero deadline line** shows after the deadline. (§ EXPERIENCE › State Patterns › Locked after deadline, Never answered after deadline; Receipt vs status block)  
The spine does not say what the **hero deadline line** shows after the deadline. For a household that never answered, it would still read «**Svar** innen 4. januar 2028» with a working link after the date has passed.  
Fix: Specify the hero line for the locked states, e.g. «Svarfristen gikk ut 4. januar · Ring oss» (contacts), and «Svar sendt … · Se svaret» unchanged for households that answered.

**[Shape fit]** — R2-15 · The example is «Vår historie.», which looks like a rename slip. (§ DESIGN › Typography table, row "Topic text")  
The example is «Vår historie.», which looks like a rename slip. The topic line is «Fra vi møttes til i dag.» (EXPERIENCE › Voice and Tone; DESIGN › Layout).  
Fix: Use «Fra vi møttes til i dag.» or «Hele helgen, dag for dag.»

**[Shape fit]** — R2-16 · The text still says the superseded `key-admin-overview.html` helper view "is still the only render of read-only admin (see EXPERIENCE Ope… (§ DESIGN › Layout & Spacing › *Admin home (A2)*)  
The text still says the superseded `key-admin-overview.html` helper view "is still the only render of read-only admin (see EXPERIENCE Open Question 15)". OQ15 is resolved, and `.working/helper-view-1.html` is the render now.  
Fix: Point to `helper-view-1.html` (or its promoted copy) and drop the OQ15 reference.

**[Token completeness]** — R2-17 · Several `[ASSUMPTION]` tags are settled by approved renders. (§ DESIGN › Colors `scrim`, Elevation › Dialogs, Nav bar row, Admin nav row)  
Several `[ASSUMPTION]` tags are settled by approved renders. The 60 % scrim is approved in `admin-guests-1`, `admin-payments-1` and `privacy-1`. Those three renders paint the scrim as `rgba(20,26,12,.6)` (#141A0C), not the token's #344628. The current-page 2px/4px underline is approved in `info-praktisk`. The admin nav (Oversikt · Gjester · Betalinger · Innstillinger · Logg ut) is approved in two admin renders.  
Fix: Remove those tags. Decide whether the scrim is #344628 or #141A0C and make the token match.

**[Token completeness]** — R2-18 · Below 340px the nav uses 8px gaps, padding `8px 10px 8px 12px`, and a "Svar" button with 0 12px padding and a 56px minimum width. (§ DESIGN frontmatter `nav-svar.minWidth: 64px`, `nav-bar.padding`, `nav-words.gap`; DESIGN › Components › Nav "Svar" ("≥ 64 × 44px"); DESIGN › Layout (320px paragraph))  
Below 340px the nav uses 8px gaps, padding `8px 10px 8px 12px`, and a "Svar" button with 0 12px padding and a 56px minimum width. These values are only in prose, and the Components row still says ≥ 64px wide.  
Fix: Add small-phone variants to the frontmatter (as `gutter-small-phone` already is), and make the Components row say "64px (56px below 340px)".

**[Component coverage]** — R2-19 · The component names have drifted between the spines. (§ DESIGN › Components vs EXPERIENCE › Component Patterns)  
The component names have drifted between the spines. DESIGN calls it "RSVP sheet" and EXPERIENCE calls it "RSVP panel". EXPERIENCE "Info page" has no DESIGN row. *Back link*, *Outlined button on green* and *Helper read-only line* have no behavioural row; the helper line's behaviour lives in State Patterns.  
Fix: Use one name ("RSVP sheet" matches the paper-sheet language). Add short behavioural rows, or a line saying that visual-only components need none.

**[Visual reference coverage]** — R2-20 · This file is cited as the detailed first-screen render, but its nav still reads «Program · Praktisk · Stedet · Om oss», and one card is h… (§ EXPERIENCE header and DESIGN › Components › Hero sheet → `mockups/paper-ceremony-5.html`)  
This file is cited as the detailed first-screen render, but its nav still reads «Program · Praktisk · Stedet · Om oss», and one card is headed «Om oss». The page title of `info-om-oss.html` reads «Vår historie (før «Om oss»)». The spines win, but a builder opening the "detailed" render sees a dropped page.  
Fix: Add a caption at the citation ("nav words predate 2026-11-15; see front-page-3"), or update the nav in the render.

**[Visual reference coverage]** — R2-21 · The crop of 12-Us1 used as the *Vår historie* topic picture is an orphan in `mockups/`, and no spine names it. (§ `mockups/us1-utsnitt.jpg`; DESIGN › Layout › front-page order item 4)  
The crop of 12-Us1 used as the *Vår historie* topic picture is an orphan in `mockups/`, and no spine names it. The front-page item gives Programmet (01-Venue) and Praktisk (03-Venue) but only "the couple" for *Vår historie*.  
Fix: Name `egne-bilder/12-Us1.jpg` (crop `mockups/us1-utsnitt.jpg`) in item 4.

**[Token completeness]** — R2-22 · `panel-gap` (16px) and `panel-padding` (20px) are never referenced. (§ DESIGN frontmatter `spacing.panel-gap`, `spacing.panel-padding`; `components.panel.padding`, `info-sheet`, `story-sheet`)  
`panel-gap` (16px) and `panel-padding` (20px) are never referenced. Panel paddings are written out as raw values ('24px 22px 14px', '22px 22px 12px'), and the 20px gap between sheets is stated in prose only.  
Fix: Remove the two tokens, or reference them, for example `info-sheet.gap: '{spacing.5}'`.

**[Shape fit]** — R2-23 · The example «Sist endret av Arild, 3. (§ EXPERIENCE › State Patterns › Last updated)  
The example «Sist endret av Arild, 3. mars kl. 18:40» falls after the 4 January 2028 deadline, when guests can no longer change answers (and before the invitations if read as 2027).  
Fix: Use a date inside the answering window, for example «3. november kl. 18:40».

**[Component coverage]** — R2-24 · The Info page row says "Back link first, then the jump links", but *Vår historie* has none (DESIGN says so). (§ EXPERIENCE › Component Patterns › Info page; IA › Navigation; IA G3)  
The Info page row says "Back link first, then the jump links", but *Vår historie* has none (DESIGN says so). The Navigation paragraph puts the sticky bar on "G2 and G3" only. The approved G12 render also has it, with no current word, and G12's short jump-link labels (Hva vi lagrer · Hvem ser det · Sletting · …) are not in the microcopy table.  
Fix: Say "jump links where the page has more than one part". Add G12 to the nav sentence, noting that no word is current. Add a G12 jump-link row to Voice and Tone.

**[Flow coverage]** — R2-25 · It is not clear whether «Se betalingene» on the household page opens the A9 list or that household's payment page. (§ EXPERIENCE › IA A9 ("Reached from … A6 «Se betalingene»"))  
It is not clear whether «Se betalingene» on the household page opens the A9 list or that household's payment page. The render implies the household page.  
Fix: Write "→ A9 household payment page".

**[Component coverage]** — R2-26 · The irreversible guest-side delete «Slett allergiopplysningene» is a **primary** button. (§ DESIGN › Layout (*G12*, withdrawal dialog); DESIGN › Components › Destructive button ("tier 3 only"))  
The irreversible guest-side delete «Slett allergiopplysningene» is a **primary** button. The spines have no rule for guest-side irreversible actions, so a builder could just as well use the Destructive style. The safe focus on «Avbryt» is specified.  
Fix: State that primary is deliberate for the guest-side withdrawal (one confirmation, Rikke's approved render), or switch it to Destructive.

**[Component coverage]** — R2-27 · The refund has three phrasings: (§ EXPERIENCE › Voice and Tone ("Refund owed", "Admin payments (A9)"); Component Patterns › Status tag)  
The refund has three phrasings: «Skal ha penger tilbake» (count and attention reason), «Skal ha tilbake 200 kr» (tag) and «Skal betales tilbake» (A9 «Til sammen»). Each can be defended, but no rule says which one goes where.  
Fix: Add one line mapping each context to its phrasing, or merge them.

## Reviewer files

- `review-rubric-2.md`
- `review-accessibility-2.md`
- Earlier run (2026-11-11): `review-rubric.md`, `review-accessibility.md`, `review-resolution.md`
