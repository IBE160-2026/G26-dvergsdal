> **Kort oppsummering (norsk)**
>
> - Hva er sjekket: to KI-gjennomganger av UX-dokumentene DESIGN.md (utseende) og EXPERIENCE.md (oppførsel). Den ene sjekket at dokumentene er komplette og henger sammen, den andre sjekket tilgjengelighet (WCAG 2.2 AA og eldre brukere som bestefar Sigmund).
> - Antall funn: 1 kritisk, 5 høy, 25 middels og 24 lav (55 i alt). Noen funn går igjen hos begge gjennomgangene, for eksempel forsiden og fokusringen.
> - Viktigst 1 (kritisk): et halvutfylt svar kan forsvinne hvis Messenger-nettleseren laster siden på nytt. Hvert steg bør lagres som et utkast på serveren.
> - Viktigst 2: forsiden lover at alt vises uten å scrolle på mobil, men målingen viser at knappen «Svar på invitasjonen» havner langt under skjermkanten. Det må bestemmes nå.
> - Viktigst 3: papirteksturen på den grønne bakgrunnen gjør den lyse teksten for svak (kontrast), og oppsettet tåler ikke 200 % zoom. I tillegg er det ikke bestemt hvor spørsmålet om ankomst (FR-18) skal stå i skjemaet.
> - Det gis ingen samlet karakter. Neste steg er å ta funnene inn i en oppdatering av DESIGN.md og EXPERIENCE.md.

# Validation Report — AI'll handle it

- **DESIGN.md:** `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md`
- **EXPERIENCE.md:** `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md`
- **Run at:** 2026-11-11T09:05:26Z

## Overall verdict

The pair is a usable contract. Every colour token has a hex value (light only, which decision D justifies), and all 12 stated contrast ratios recompute exactly. The 30 component names match one to one across DESIGN.md › Components and EXPERIENCE.md › Component Patterns. All six UJ titles are taken verbatim from the PRD, and every memlog decision has landed in a spine. Two high-impact gaps remain before stories can be written. First, the committed hero tokens most likely break FR-7's "no scrolling on a phone" promise. Second, the position of the FR-18 arrival step is still open. Neither is critical. A handful of medium component and token gaps also remain: focus on the primary button, colours for status tags, the consent block, and the admin overview table.

The accessibility review shifts the picture. Measured in a rendered harness, it confirms the rubric's hero concern as fact rather than estimate (the button sits at 797px on a 360 × 640 screen), and it adds the report's only critical finding: nothing guarantees that a half-filled household answer survives a reload in the Messenger in-app browser, which puts SM-3 at risk. It also finds that the paper texture pushes the cream-on-green pair below 4.5:1 and that the type rules break at 200 % zoom. Its own verdict is that the spines are not ready to hand to implementation until the critical and high findings are resolved. Several findings overlap between the two reviewers (hero above the fold, focus offset, copy-button failure); they are kept separate below and counted once per reviewer.

## Category verdicts

- Flow coverage — adequate
- Token completeness — adequate
- Component coverage — adequate
- State coverage — adequate
- Visual reference coverage — adequate
- Bloat & overspecification — adequate
- Inheritance discipline — strong
- Shape fit — strong

## Findings by severity

Counts combine the rubric walker and the accessibility reviewer: critical 1, high 5, medium 25, low 24.

### Critical (1)

**[Accessibility reviewer]** — An unsent answer does not survive a reload, discarded tab or timeout (EXPERIENCE § State Patterns "Not sent yet"; § Interaction Primitives "One step at a time"; § Responsive & Platform "In-app browsers")
Nothing in the spines says an unsent answer survives a reload, a discarded tab or a timeout. The only protection is a leave warning, and the spine itself admits in-app browsers "cannot be relied on" for it. Messenger and Facebook WebViews routinely reload a page when the user switches apps. Sigmund will put the phone down to ask bestemor about her allergies or take a call, then come back to a blank form. No guest-side form or CSRF token lifetime is specified either, so a "Send svaret" after a long pause may fail. Under WCAG 2.2.1 a time limit needs a warning and a way to extend it, and here the user is not even told one exists. This directly threatens SM-3 (completing alone in under 10 minutes).
Fix: Make "Fortsett" persist each step server-side as a household draft (status "ikke sendt"). On reopening the link, show "Du har et svar som ikke er sendt ennå. Fortsett der du slapp" on G2 and in the status block. State that guest pages have no session or token expiry, or that expiry is at least 20 hours, and that an expired submit keeps all input. Add the draft states to the Surface coverage list.

### High (5)

**[Flow coverage]** — Hero content does not fit above the fold on a phone (§ EXPERIENCE › Component Patterns › Hero panel; Key Flows › UJ-1 step 1; Open Questions 1; DESIGN › Layout & Spacing front-page order)
UJ-1 step 1 and the FR-7 Hero panel rule promise that names, date, place, invited names, "Barnefritt bryllup", deadline and the button are all visible without scrolling. The committed tokens most likely do not fit. At 360px wide the content box is about 292px (gutter 16 + hero inline padding 18 on each side). Image 17 (1695×928) is then about 160px tall. Adding the nav row (one or two lines at ≥44px), hero padding 30px, seal 96px, names 46px×1.2, invites, date, place, invited, child-free and deadline lines (about 30px each), and the 52px button gives about 670px or more, against roughly 560px of visible viewport at 360×640. This is left as Open Question 1 with no committed rule.
Fix: Commit a budget now. Either cap the illustration height (for example `hero-illustration.maxHeight` ≤ 110px at narrow widths), let the seal shrink at 320–360px, or move the nav words below the hero or onto one line. Then verify with a 360×640 render before the stories are written.

**[Flow coverage]** — FR-18 expected arrival has no step position (§ EXPERIENCE › Interaction Primitives › Form step order; Open Questions 3 and 5)
FR-18 (expected arrival, a v1 guest-flow requirement) has no step position. The step order in Interaction Primitives skips it, and it is listed as open. Form-step stories, the "Steg n av m" count and the check-answers grouping all depend on it.
Fix: Decide the position with Rikke (for example per person together with days, or as its own step before the hike), and record the fixed choices including "Vet ikke".

**[Accessibility reviewer]** — The paper texture breaks the 4.95:1 cream-on-green pair (DESIGN § Elevation & Depth "Paper texture"; § Contrast pairs; § Components "Nav words", "Lead-in")
Keeping the *average* colour unchanged is not enough. Overlay noise lightens individual pixels, and this pair has only 0.45 of headroom. Sampled from the render's own `--grain-green`/`--fibre-green` on `#5A6C48`:

- 17.4 % of background pixels give `#F5EEDF` text less than 4.5:1;
- the 95th percentile is 4.23:1 and the worst pixel is 3.47:1.

This text is the primary navigation and the lead-in, set in thin EB Garamond (the lead-in is italic). It fails 1.4.3 wherever a glyph lands on a light speck. The panels are fine: ink stays ≥ 7.8:1 and `ink-muted` ≥ 4.6:1 on the textured cream.
Fix: Either take the texture off the green behind text (a `page-green` band under the nav row and lead-in), or cap the green texture so that no pixel is lighter than `#5F7250` (≥ 4.5:1 with headroom), or darken `page-green` by about 2 L* so that the lightest texture pixel still passes. Write the rule "contrast is checked against the lightest texture pixel, not the average" into DESIGN § Contrast pairs.

**[Accessibility reviewer]** — The "everything above the fold" claim is false (EXPERIENCE § Component Patterns "Hero panel"; § Key Flows UJ-1 step 1; DESIGN § Layout & Spacing front-page order)
The spine states it as fact in two places. Measured bottom of the "Svar på invitasjonen" button:

- **797px** at 360 × 640, so the button and the deadline line are entirely below the fold;
- **805px** at 320 × 568;
- about 240px below the fold in a Messenger in-app browser, which leaves roughly 360 × 560 visible;
- over 1 100px at 200 % zoom.

The nav row alone takes 104px (two lines), and image 17 takes 152px. Open Question 1 suggests "cap illustration height or shrink the seal", but that is not enough. Even removing *both* leaves the button at about 630px with no margin for the in-app toolbar. Sigmund, who does not scroll speculatively, may never see the deadline or the button.
Fix: Decide it now rather than leave it open:

- move the nav row *below* the hero, or reduce it to a single "Les mer om helgen ↓" line;
- cap the illustration at about 90px tall (`object-fit: cover`), or move it below the button;
- put the deadline directly above the button;
- re-measure at 360 × 560.

Rewrite UJ-1 step 1 so it does not promise what the layout cannot deliver.

**[Accessibility reviewer]** — The reflow rules contradict each other at the zoom level older users actually use (DESIGN § Typography "Imperial Script … never below 32px … shrink to fit at 320px rather than wrap"; § Layout & Spacing; EXPERIENCE § Accessibility Floor; § Responsive & Platform)
On a phone, "200 % zoom" means Android font scaling (which Chrome now applies as page zoom) or iOS page zoom. That gives a layout viewport of about 180 CSS px, not 320. At 180px:

- the names need 17px to fit, which breaks the 32px floor, yet `white-space: nowrap` forbids wrapping, so the document becomes 296px wide and scrolls sideways (fails 1.4.10);
- the nav row becomes four lines (192px).

The render shrinks the names with `cqi` units. This means zoom does not enlarge them, which conflicts with 1.4.4. Container queries are also unsupported in iOS < 16 and older Android WebViews, and that is exactly Sigmund's old phone, where the fallback is a fixed 46px nowrap line that overflows even at 320px (measured 262px of names in a 237px box). Long bokmål compounds ("Allergiopplysningene", "Hardingasete") will also overflow narrow columns. All type tokens are in px, which ignores the browser font-size setting.
Fix:
- let the names wrap onto two lines (name / "&" / name, as in inspiration 09) below about 300px instead of shrinking;
- drop the "shrink to fit" rule and any `cqi`/JS fitting;
- specify `rem` for type tokens, `overflow-wrap: anywhere` and `hyphens: auto` (with `lang="nb"`);
- add 180 × 320 as an explicit check width in § Responsive & Platform.


### Medium (25)

**[Flow coverage]** — FR-14 read as one step instead of two (§ EXPERIENCE › Interaction Primitives; DESIGN › Components › Progress line; PRD FR-14)
FR-14 defines two steps: first who is coming, then "whole weekend?" with days per person. The memlog and EXPERIENCE make it one step: "who is coming and which days (FR-14)". The DESIGN example "Steg 2 av 6" means a different count depending on which reading is used.
Fix: State explicitly whether step 1 is one screen or two, and update the progress-line example to match.

**[Token completeness]** — Focus ring merges with the primary button (§ DESIGN › Colors `focus-on-panel`; `components.button-primary`; EXPERIENCE › Accessibility Floor)
The focus ring on cream is `focus-on-panel` `#344628`, which is the same value as the primary button fill `green-dark`. The 3px ring therefore merges with the button (1.00:1) unless there is an offset, and no offset is specified.
Fix: Add a `focus-offset` spacing token (for example 2–3px, so the cream panel shows between button and ring) and state it in Components › Primary button.

**[Token completeness]** — Status tags have no status → colour mapping (§ DESIGN › Components › Status tag; EXPERIENCE › Component Patterns › Status tag)
The status tag says "outlined text label in the state colour", but nothing maps the payment statuses ("Ingenting å betale", "Ikke betalt", "Delbetalt, 300 kr mangler", "Betalt", "Skal ha tilbake 200 kr") or "Endret" to `success`, `warning`, `error` or `ink`. Only "Stemmer ikke" → `error` is given.
Fix: Add a status → colour → icon table.

**[Component coverage]** — "One primary button per screen" conflicts with G2 (§ DESIGN › Components › Primary button; EXPERIENCE › Component Patterns › Primary button and Status block)
"One per screen" for the primary button conflicts with G2. The front page has the RSVP button in the hero and again in its own bottom panel (FR-8). Once the guest has answered, the status block adds a second "Se eller endre svar" primary button next to the hero button that becomes "Se eller endre svar" (FR-37).
Fix: Reword the rule as "one distinct primary action per screen; repeats of the same action allowed". Decide whether the hero button or the status block carries "Se eller endre svar" once the guest has answered.

**[Component coverage]** — Consent block has no component row (§ EXPERIENCE › Consent & Privacy UX; FR-26 to FR-28)
The consent block has no component row in either spine. It holds the purpose and recipients text before the choice, a Yes/No that starts unanswered, the "Jeg bekrefter at Marie vet om dette og er enig" confirmation, and the withdrawal entry. It is described only in prose, and this is the most sensitive control in the product.
Fix: Add a "Consent block" row to both Components tables: visual (panel section, text order, choice control) and behavioural (starts unanswered, never blocks sending, confirmation shown only for others).

**[Component coverage]** — No component for the A4 overview or admin nav (§ EXPERIENCE › IA A4 and admin navigation; › Responsive & Platform; DESIGN › Layout & Spacing › Admin)
Admin has no component for the A4 full overview (table on PC, stacked rows on phone, unanswered households "stand out", mismatch and "Endret" markers) or for the admin nav row. EXPERIENCE says "same word-row pattern", but DESIGN's Nav words are cream text on `page-green` with no admin variant.
Fix: Add "Overview row / table" and an admin nav variant (or say explicitly that admin reuses Nav words on green).

**[State coverage]** — Status block position on G2 is unstated (§ EXPERIENCE › IA › Receipt vs status block; DESIGN › Layout & Spacing front-page order)
The answered state of G2 puts the status block "near the top" without saying whether it sits above, inside or below the hero panel. Above the hero it pushes the FR-7 content further below the fold (see Flow coverage).
Fix: Add the status block to the numbered front-page order in DESIGN › Layout & Spacing.

**[Visual reference coverage]** — Hero illustration and seal have no specific source file (§ DESIGN › Components › Hero illustration; › Shapes)
Two downstream assets have no specific path. (1) The hero illustration is named as "image 17", but the file `../../ux/egne-bilder/04-Illustration.jpg` is never linked. (2) The seal outline is "in the renders (`#seal-shape`)", but it appears in nine `.working` files with different versions, and no one file is named.
Fix: Link the image file and name the canonical seal source (for example `mockups/illustration-3.html#seal-shape`), or export the seal to an SVG file.

**[Accessibility reviewer]** — Hint text breaks the spine's own rule, and the 18px floor holds only in the letter (DESIGN § Colors `ink-muted` "Never: … anything the guest must read to act" vs § Components "Text field … hint below in `{typography.small}` `{colors.ink-muted}`"; § Typography)
Format hints such as "for eksempel 900" are exactly what the guest must read to act, yet they are set in the smallest and lightest style. EB Garamond's x-height is 0.41, so `small` at 18px renders like about 15px Georgia (the typography render says so itself). That is below the *intent* of NFR-5's 18px floor, and it also covers the progress line and footer meta.
Fix: Set hints in `ink` at `body` size, italic if they must be told apart. Raise `small` to 19–20px, or limit it to text nobody needs to act on (timestamps, "Ikke oppgitt").

**[Accessibility reviewer]** — Focus visibility depends on an offset that is never specified (DESIGN § Colors `focus-on-panel`; § Components "Primary button", "Text field"; EXPERIENCE § Accessibility Floor)
- `focus-on-panel` is `#344628`, the same colour as the primary button fill, so with `outline-offset: 0` the ring merges into the button (1:1).
- On a text field the ring replaces a 2px `#5E594F` border with a 3px `#344628` ring. The two differ by only 1.50:1, so the focused field looks almost the same as an unfocused one.
- Rings drawn past a panel edge land on `page-green` at 1.79:1.

Fix: Add `focus-offset: 3px` as a token and make it mandatory. On fields, use a ring *plus* a thicker border, or a 3px ring offset outside a cream gap. Choose the ring colour by the surface the ring is *painted on*, not by the element's parent. Specify `:focus-visible` with no `outline: none` anywhere.

**[Accessibility reviewer]** — Field error, hint and consent semantics are left undefined (DESIGN § Components "Text field", "Choice control"; EXPERIENCE § Component Patterns "Text field", "Error summary"; § Consent & Privacy UX)
The spine places the error "between label and field" but never changes the field's visual state: border colour and width stay the same. It also never requires `aria-invalid`, or `aria-describedby` linking the hint and error to the input. The consent explanation must be read *before* Yes/No, but there is no fieldset/legend/describedby structure tying the long text to the radio group. Choice groups get no error placement at all.
Fix: Error state = `error` 3px border plus the error text with icon, `aria-invalid="true"`, and `aria-describedby="hint error"`. Every radio group is a `fieldset`, with the question as `legend` and the error inside the fieldset. Consent text goes in the fieldset, before the radios, and is referenced from the legend.

**[Accessibility reviewer]** — Feedback on server-rendered pages is planned as if it were a single-page app (EXPERIENCE § Component Patterns "Notice"; § Accessibility Floor "announced via polite live regions")
Each step, the check page, the receipt and G8 are full page loads (NFR-7 "server pages"). Live regions do not announce content that is present at load, so "Svaret er sendt" and validation results are silent to screen readers unless focus is managed. The page title is also "identical for every guest" and presumably the same for every step, which fails 2.4.2 in practice.
Fix: On every load, set `<title>` to "Steg 3 av 6: Måltider – Invitasjon", prefixed with "Feil: " when there are errors. Focus the error summary when there are errors; otherwise let focus start at the top, with the `h1` as the step question. Keep live regions for in-page changes only (running total, "Kopiert").

**[Accessibility reviewer]** — The step count "Steg n av m" moves under the guest (EXPERIENCE § Component Patterns "Progress line"; DESIGN § Components "Progress line")
If m is recalculated as steps appear or disappear, Sigmund sees "Steg 3 av 5" and then "Steg 4 av 6", which undermines the one orientation cue an older user relies on. It is also set in the smallest type (see the hint finding).
Fix: Settle m after step 1, which determines all conditional steps. Show the step name in the progress line ("Steg 2 av 6: Overnatting"), set it at `body` size, and expose it as the first line under the `h1`.

**[Accessibility reviewer]** — Browser Back on POST-driven steps is left unspecified (EXPERIENCE § Interaction Primitives "browser Back equals 'Tilbake' [ASSUMPTION]")
With server-submitted steps, Back produces "Bekreft innsending av skjema" prompts or stale pages. Older users press Back constantly.
Fix: Require Post/Redirect/Get for every step, so each step has its own GET URL and Back is always safe and shows the saved draft (see the critical finding).

**[Accessibility reviewer]** — The nav-word row has unaddressed semantics and wayfinding problems (DESIGN § Components "Nav words"; EXPERIENCE § Information Architecture "Navigation")
- Middle-dot separators written as text are read aloud ("midtpunkt") between every link, and they dangle at line starts when the row wraps.
- No render has ever shown the row.
- "Svar" is only about 44px wide at 20px with 6px padding, so NFR-5's 44 × 44 needs explicit inline padding. The spine specifies only height.
- The row has no entry for the invitation itself, so on G3 the current-page marker works but there is no way "home" except "Tilbake til invitasjonen".
- "Svar" (a noun or verb with a changing destination) competes with the primary "Svar på invitasjonen".

Fix: Use `<nav aria-label="Invitasjonen"><ul>` with the dots generated by CSS `::before` (`aria-hidden` by nature). Set an inline padding token so every word is ≥ 44 × 44. Add "Invitasjonen" as the first word on G3. Rename "Svar" to "Ditt svar", or drop it, since the button already exists.

**[Accessibility reviewer]** — The couple's names exist only in a hairline script, and there is no defined `h1` (DESIGN § Typography "Imperial Script"; EXPERIENCE § Component Patterns "Hero panel"; § Accessibility Floor "page titles … contain no names")
- The typography render itself rated Imperial Script "litt tyngre å lese" with "svært tynne oppstreker".
- On G2 the names appear nowhere else on the screen, and the tab title has no names (FR-4). A guest with low vision or cataracts gets the most important fact (whose wedding) only in the least legible type on the page.
- The renders use `<p>` for both names and card headings, and the spine never fixes the heading outline.

Fix: Set the invites line in plain text as "Rikke og Valdemar inviterer deg til bryllup", with the script names as a decorative echo above it (`aria-hidden`). Alternatively, make the `h1` the script names with a plain-text accessible name. Fix the outline: `h1` names/invitation, `h2` per card, `h1` = step question on form pages.

**[Accessibility reviewer]** — Forced colours break three things (DESIGN § Components "Hero illustration" `mix-blend-mode: darken`, "Choice control", "Primary button")
Forced colours (Windows High Contrast, Android high-contrast themes):

- In a dark forced-colour theme the panel background becomes black, and `darken` takes the minimum of the image and the backdrop, so the illustration turns into a solid black box.
- Custom choice controls whose "selected" state is a `green-dark` *background fill* lose that fill, so checked and unchecked look identical.
- Primary buttons that are links with only a background have no visible boundary.

Fix:
- bake the panel colour into the shipped JPG instead of blending at runtime; this also guarantees zero colour shift and removes a WebView compatibility risk;
- draw the check/dot as an SVG or `::after` with `currentColor`, or use native inputs with `accent-color`;
- give buttons `border: 2px solid transparent`;
- add a `@media (forced-colors: active)` check to § Accessibility Floor.


**[Accessibility reviewer]** — "Light only" is a wish with no mechanism behind it (DESIGN § Brand & Style "Light only"; EXPERIENCE § Foundation)
Samsung Internet's dark mode is a likely default browser for older Android users. It and Chrome's auto-dark force-darken pages that do not opt out. Cream panels go dark, ink goes light, and the `darken`-blended illustration collapses.
Fix: Specify `<meta name="color-scheme" content="light only">` and `:root { color-scheme: light only; }`, test in Samsung Internet with dark mode on, and record the result.

**[Accessibility reviewer]** — State colours cannot be told apart (DESIGN § Colors `error`/`success`/`warning`; § Components "Notice", "Status tag"; EXPERIENCE § Component Patterns "Status tag"; IA A4 "unanswered stand out")
Icon shape and text must do all the work, and the spine does not say how.

- The three state colours differ from each other by only 1.08–1.17:1 in luminance. To a colour-blind user, or an older eye with yellowed lenses, rust, olive and brown are the same dark brown.
- The notice spec gives one "22px icon" without saying the icons differ in shape.
- "Unanswered stand out" in A4 has no mechanism, which in practice means colour.

Fix: Specify distinct icon shapes (error = triangle/!, warning = circle/!, success = check, info = i) and a visible text prefix ("Feil:", "Obs:"). In A4, mark unanswered households with the word "Ikke svart" and sort them first.

**[Accessibility reviewer]** — The undo bar fails timing, focus and obscuring checks (EXPERIENCE § Component Patterns "Undo bar", "Attention item"; § Admin protection tiers tier 1; DESIGN § Components "Undo bar"; § Accessibility Floor 2.4.11)
- Ten seconds is not enough for a screen-reader or switch user to hear a polite announcement and travel to a bar at the bottom of the viewport.
- The "can also be unmarked later" escape hatch has no defined location, so the timed bar may be the *only* undo, which falls under 2.2.1.
- "Merk som håndtert" removes the focused row, so focus drops to `<body>`.
- A fixed bottom bar is exactly the sticky element the spine bans on guest pages (2.4.11), and at 200 % zoom it covers a large share of a phone screen.

Fix: Replace the row in place with "Merket som håndtert. Angre", move focus to "Angre", and keep it until the user leaves the page (no timer). Define where handled items can be found and unmarked (a "Vis håndterte" filter). No fixed bars in admin either.

**[Accessibility reviewer]** — Admin session expiry loses input, and the spine leaves it open (EXPERIENCE § State Patterns "Session expired"; Open Question 8)
Logging Rikke out mid-edit with no warning and no extension fails 2.2.1 unless the session lasts ≥ 20 hours.
Fix: Decide now: either a ≥ 20-hour idle session, or a warning dialog two minutes before expiry with "Fortsett å være logget inn", plus restoring the unsaved form after logging in again.

**[Accessibility reviewer]** — Dialog behaviour is underspecified for phones and screen readers (EXPERIENCE § Component Patterns "Dialog"; DESIGN § Components "Dialog")
- "Focus moves into it" does not say *to what*. For tier 2 and 3 the consequence sentence must be heard first.
- "Actions right-aligned, safest action first" is ambiguous in DOM versus visual order, and right-aligned side-by-side buttons do not survive 320px or 200 %.
- "Esc = cancel" does not exist on a phone, and scrim taps are unspecified.
- The guest leave-warning dialog has no button wording.

Fix: Use `role="alertdialog"` with `aria-labelledby` set to the heading and `aria-describedby` set to the consequence, and focus the safe button (or the heading for tier 3). Stack buttons full-width on narrow screens, safe action first in both DOM and visual order. A scrim tap equals cancel. The leave warning says "Svaret er ikke sendt ennå", with buttons "Bli og fullfør svaret" (primary) and "Gå uten å sende". Let the dialog body scroll at 200 %.

**[Accessibility reviewer]** — The "Kopier" buttons on G7 are identical and fragile in in-app browsers (DESIGN § Components "Payment details"; EXPERIENCE § Component Patterns "Payment details")
- Four buttons all named "Kopier" are ambiguous to screen readers and voice control.
- `navigator.clipboard` is missing or blocked in some Messenger and Facebook WebViews, so the button may silently do nothing while showing nothing.
- "Kopiert inline" has no announcement and no duration.

Fix: Accessible names "Kopier kontonummer" and so on (the visible label may stay "Kopier"). Feature-detect, and hide the button when copying is unsupported. Values are always selectable plain text at `body` size with lining figures. "Kopiert" goes in a polite live region and stays until the next copy.

**[Accessibility reviewer]** — The footer phone numbers, the help path for older guests, have no stated targets (DESIGN § Components "Footer band"; EXPERIENCE § Component Patterns "Footer band")
In color-themes-5 the two numbers share one paragraph separated by `<br>` at 27px line height, so two adjacent `tel:` targets are well under NFR-5's 44px, and a mis-tap calls the wrong person.
Fix: Give each contact its own ≥ 44px row: "Ring Rikke 900 00 000" and "Send SMS til Rikke", as separate full-width links. Note that `sms:` body syntax differs between iOS and Android, so link the number only.

**[Accessibility reviewer]** — Guest content must not depend on JavaScript in v1, yet the spine defers that guarantee to [2027] (EXPERIENCE § Component Patterns "Hero panel … Renders without JavaScript [2027]"; § State Patterns "Static fallback [2027]")
Read literally, the v1 invitation and form may require JS, which old phones and in-app browsers fail on first.
Fix: In v1, all guest pages and form steps are server-rendered HTML that work without JS. JS only adds the running-total update, copy buttons and the envelope. Only the envelope's fallback can wait for [2027].

### Low (24)

**[Flow coverage]** — UJ-2 refund coda has no flow beat (§ EXPERIENCE › Key Flows › UJ-2, UJ-5)
The PRD UJ-2 coda (the couple sees "Endret", pays Arild back and registers the refund so the balance is zero) has no flow beat. UJ-5 covers only received payments.
Fix: Add a refund step to UJ-5 or a closing line to UJ-2 that points to A9.

**[Token completeness]** — No tokens for busy, hover and pressed states (§ DESIGN frontmatter `components`)
No visual tokens for the busy state ("Sender …", the button ignores repeat taps) or for hover/pressed on the secondary button, destructive button and text links. Only `green-dark-hover` exists.
Fix: State whether busy buttons keep their colours, and give hover treatments for the remaining interactive components.

**[Token completeness]** — `rounded.none` unused; choice control lacks radius (§ DESIGN frontmatter; › Shapes)
`rounded.none` is defined but never used. Prose gives choice boxes `{rounded.md}`, but `components.choice-control` has no radius, and the radio button is round.
Fix: Remove `none` or use it, and add `radius` to `choice-control`.

**[Component coverage]** — Several used pieces are not named as components (§ IA; State Patterns)
Several pieces are named in IA or states but not as components: the last-updated header (G4b), the typed-confirmation input for tier 3, the multi-line question field (G10) and the admin search field (A6).
Fix: Name them as variants of Text field or Notice in both tables.

**[State coverage]** — No failure state for copy buttons (§ EXPERIENCE › Responsive & Platform; G7; A6)
There is no failure state for "Kopier" (G7) or "Kopier lenke" (A6). The clipboard API can fail in Messenger or Facebook in-app browsers, which EXPERIENCE names as a target.
Fix: When copying fails, show the value selected with "Trykk og hold for å kopiere".

**[State coverage]** — Admin loading behaviour unstated (§ EXPERIENCE › State Patterns › Loading)
Loading is defined for guest pages only ("no skeletons or spinners"). Admin loading and slow-list behaviour are unstated.
Fix: One line for admin.

**[Visual reference coverage]** — Renders linked only in the header, without captions (§ DESIGN header, › Brand & Style, › Typography, › Shapes)
DESIGN links the renders only in its header. They are not linked inline at Colors (color-themes-5), Typography (typography-1) or Hero illustration (illustration-3), and the header does not say what each render shows. Inspiration images (01, 03, 08, 09) are cited by number without links.
Fix: Move each render link to its section with a one-line caption, and link the cited images.

**[Visual reference coverage]** — Final type pairing never rendered together (§ typography-1; color-themes-5)
The final type pairing, Imperial Script with EB Garamond at 20px, was never rendered together (typography-1 pairings: S1+B2, S1+B1@20px, S4+B3). color-themes-5 predates both the illustration and the font choice.
Fix: Render the final front page (G4a + K1 + T2 + S4 + B1@20 + I7) as one mockup when promoting to `mockups/`.

**[Bloat & overspecification]** — Consent & Privacy UX restates the requirements (§ EXPERIENCE › Consent & Privacy UX)
Consent & Privacy UX largely restates FR-25 to FR-30, FR-43 and NFR-4, although the header says requirements are "not restated here".
Fix: Keep the UX decisions (explanation before Yes/No, withdrawal in two places, confirmation wording) and cite the FRs for the rest.

**[Bloat & overspecification]** — "Surface coverage" is one long run-on line (§ EXPERIENCE › State Patterns)
The "Surface coverage" paragraph is a single 150-word run-on line, which is hard to source-extract.
Fix: Turn it into a Surface | States table.

**[Bloat & overspecification]** — Decided items live in struck-through Open Questions (§ EXPERIENCE › Open Questions 6)
Open Questions keeps struck-through decided items, and the hike "kanskje" decision (memlog: shown separately in the admin summary) lives only there.
Fix: Move it into Component Patterns › Admin summary row and drop the struck items.

**[Inheritance discipline]** — Example deadline has the wrong weekday (§ EXPERIENCE › State Patterns › Locked after deadline)
The example deadline "fredag 1. desember kl. 23:59" has the wrong weekday: 1 December 2027 is a Wednesday.
Fix: Correct the weekday, or use a neutral example date.

**[Inheritance discipline]** — Frontmatter component keys drift from table names (§ DESIGN frontmatter vs › Components)
Frontmatter component keys drift from the table names: `panel` ↔ Info card, `field` ↔ Text field, `link-more` ↔ Text link / "Les mer".
Fix: Name the key in each table row, or align the names.

**[Inheritance discipline]** — EXPERIENCE frontmatter uses `title:` instead of `name:` (§ EXPERIENCE frontmatter)
EXPERIENCE frontmatter uses `title:` where the examples use `name:`.
Fix: Add `name: "AI'll handle it"`.

**[Shape fit]** — G4b is an element, not an IA surface (§ EXPERIENCE › IA)
G4b ("Last-updated header + conflict notice") is listed as an IA surface, but it is an element inside G4.
Fix: Move it to Component Patterns or State Patterns.

**[Accessibility reviewer]** — The illustration's alt text is long and read before the names (EXPERIENCE § Component Patterns "Hero illustration"; illustration-3.html alt for I7, about 200 characters)
A screen-reader user hears a description of a watercolour before learning whose wedding it is, and the venue is described in text on G3 anyway.
Fix: Use `alt=""` (decorative, since its information is in the text), or a short alt such as "Akvarell av tunet på Hardingasete."

**[Accessibility reviewer]** — The seal is marked decorative but carries live text (EXPERIENCE § Component Patterns "Wax seal" `alt=""`; renders put "R & V" in a `<span>`)
An `alt=""` on an image does not hide sibling text, so screen readers announce "R og V" before the names.
Fix: `aria-hidden="true"` on the whole seal container, or render the seal and monogram as one SVG with `alt=""`.

**[Accessibility reviewer]** — Four identical visible "Les mer" links, and the card itself is not a target (DESIGN § Components "Info card"; EXPERIENCE § Component Patterns "Info card")
The hidden "om programmet" helps screen readers but not Sigmund, who will tap the heading "Programmet" and get nothing.
Fix: Make the visible link text "Les mer om programmet", or make the heading the link with the whole card as the hit area (one link per card).

**[Accessibility reviewer]** — The respondent switch "Bytt" is a link that changes state (DESIGN § Components "Respondent line"; EXPERIENCE § Component Patterns "Text link … never submits data")
"Bytt" alone does not say what it changes, it sits first on every step, and as a link it contradicts the rule that links never change data.
Fix: Use a button with the accessible name "Bytt hvem som svarer" and `aria-expanded`, give it a ≥ 44px target, and place it after the step question rather than before.

**[Accessibility reviewer]** — Hover and pressed states give no tap feedback (DESIGN § Colors `green-dark-hover`)
`#2C3A20` against `#344628` is 1.18:1, so on a phone the "did my tap work?" signal is invisible until the "Sender …" text appears, and that appears only on submits.
Fix: The pressed state also gets the 3px offset ring, or an inset cream rule, and every button responds visibly on `:active`.

**[Accessibility reviewer]** — The lining figures are still an [ASSUMPTION] and may be stripped by subsetting (DESIGN § Typography "Figures")
EB Garamond defaults to old-style figures, which are hard for older eyes to read in "1 450 kr", "23:59" and account numbers. Subsetting tools often drop the `lnum` and `tnum` features.
Fix: Make lining figures a requirement (`font-variant-numeric: lining-nums`), keep `lnum` and `tnum` in the self-hosted WOFF2 subset, and verify in the built page. Use a non-breaking space in "1 450" so screen readers read one number.

**[Accessibility reviewer]** — The typed confirmation will fight phone keyboards (EXPERIENCE § Admin protection tiers tier 3; Voice and Tone "Tier-3 typed word")
Autocapitalise and autocorrect will turn "SLETT" into "Slett" or a suggestion. Household "names" with "og", commas or æøå invite mismatches, and a disabled destructive button does not explain itself.
Fix: Match case-insensitively with trimmed whitespace, set `autocapitalize="off" autocorrect="off" spellcheck="false"`, show the exact word to type in plain text in the label, and keep the button enabled but validate on press with an inline error.

**[Accessibility reviewer]** — The envelope reveal needs more than reduce-motion (EXPERIENCE § Envelope reveal; DESIGN § Components "Envelope reveal")
It needs:

- a cap of 5 s or less (2.2.2);
- the static invitation present in the DOM and readable by screen readers underneath, not `display: none` until the animation ends;
- focus and scroll at the top of G2 afterwards;
- "Hopp over" ≥ 44 × 44, placed on cream or `green-dark` (not on textured `page-green`, see the texture finding);
- a fail-safe: no JS or storage means no envelope.

Fix: Add these as acceptance criteria next to the [If time] item.

**[Accessibility reviewer]** — Admin density competes with targets and type size (DESIGN § Layout & Spacing "Admin"; tokens `admin-body` 18px, `admin-gap` 8px; EXPERIENCE § Accessibility Floor "admin the same [ASSUMPTION]")
Rows of 18px EB Garamond (about 15px Georgia-equivalent) with 8px gaps and 44px targets will not fit FR-48's "one phone screen" for long lists. Something will give, and the spine does not say what. Stacked mobile tables also lose header associations.
Fix: State that 44px targets win over density. Stacked rows repeat their labels as visible text ("Betalt: 900 kr"), not as CSS-only headers.

## Mechanical notes

- **Broken links:** only the three expected ones (`mockups/color-themes-5.html`, `mockups/typography-1.html`, `mockups/illustration-3.html`, linked in both headers, waiting for promotion from `.working/`). No other broken links. `.memlog.md`, `DESIGN.md`, the PRD and its addendum, `inspirasjon.md` and `stedet.md` all resolve. `imports/` is empty, as intended (the memlog references these folders in place).
- **Token references:** every `{colors.*}`, `{typography.*}`, `{spacing.*}`, `{rounded.*}` and `{components.*}` reference in both files resolves. `rounded.none` is unused.
- **Contrast:** all 12 stated pairs recompute exactly. Pairs in use but not listed, all of which pass: `error` on `field-surface` 7.52:1 and `ink-muted` on `field-surface` 6.23:1. `green-dark` on `page-green` is 1.79:1, which is correctly the reason for the "primary buttons only on cream" rule.
- **Memlog landing:** every decision and override landed. Earlier entries that were superseded (script reference 01, receipt-focused climax, card style, walnut ink, illustration style open) are correctly not carried. One weak landing: hike "kanskje" exists only in struck-through Open Questions (see Bloat & overspecification).
- **Frontmatter:** DESIGN has name, description, status, created, updated and all token groups. EXPERIENCE has title, status, created, updated and sources, but no `name`.
- **Mermaid:** none present.

## Reviewer files

- `review-rubric.md`
- `review-accessibility.md`
