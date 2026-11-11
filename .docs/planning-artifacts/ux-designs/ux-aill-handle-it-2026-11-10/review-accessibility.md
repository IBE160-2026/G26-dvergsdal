---
title: "Accessibility review: AI'll handle it UX spines"
lens: accessibility (WCAG 2.2 AA + older-user usability)
reviewed: 2026-11-11
inputs: DESIGN.md, EXPERIENCE.md, .memlog.md, .working/color-themes-5.html, .working/typography-1.html, .working/illustration-3.html
key reader: bestefar Sigmund, 78, SMS link on his phone (UJ-1, SM-3, NFR-5)
---

# Accessibility review

## Verdict

The token table looks compliant, but nearly every guarantee is made on paper and fails when you measure it: the cream-on-green pair has no headroom and the paper texture already pushes it under 4.5:1, the "above the fold" hero sits about 160px below the fold on a 360 × 640 phone, and the layout rules break at the zoom level Sigmund is most likely to use. Worse, the spines never say what happens to a half-filled household answer when the Messenger in-app browser reloads, which puts SM-3 at risk. **Not ready to hand to implementation** until the critical and high findings below are resolved in the spines.

### How this was checked

- Contrast was recomputed from the hexes (WCAG 2.x relative luminance) in a scratch script. Every pair in DESIGN.md › Contrast pairs matches to two decimals.
- A spec-faithful front page was rebuilt from the renders' CSS: render texture, image 17, Imperial Script and EB Garamond from Google Fonts, plus the nav-word row that no render includes. It was rendered headless in Chrome at 360 × 640, 320 × 568 and 180 × 320 (a 360px phone at 200 % text or zoom), and the screenshot pixels were sampled for the texture finding.
- Measurements quoted below come from that harness, not from estimates.

## Findings

### Critical

- **[critical]** Nothing in the spines says an unsent answer survives a reload, a discarded tab or a timeout (EXPERIENCE § State Patterns "Not sent yet"; § Interaction Primitives "One step at a time"; § Responsive & Platform "In-app browsers"). The only protection is a leave warning, and the spine itself admits in-app browsers "cannot be relied on" for it. Messenger and Facebook WebViews routinely reload a page when the user switches apps. Sigmund will put the phone down to ask bestemor about her allergies or take a call, then come back to a blank form. No guest-side form or CSRF token lifetime is specified either, so a "Send svaret" after a long pause may fail. Under WCAG 2.2.1 a time limit needs a warning and a way to extend it, and here the user is not even told one exists. This directly threatens SM-3 (completing alone in under 10 minutes). *Fix:* make "Fortsett" persist each step server-side as a household draft (status "ikke sendt"). On reopening the link, show "Du har et svar som ikke er sendt ennå. Fortsett der du slapp" on G2 and in the status block. State that guest pages have no session or token expiry, or that expiry is at least 20 hours, and that an expired submit keeps all input. Add the draft states to the Surface coverage list.

### High

- **[high]** The paper texture breaks the 4.95:1 cream-on-green pair (DESIGN § Elevation & Depth "Paper texture"; § Contrast pairs; § Components "Nav words", "Lead-in"). Keeping the *average* colour unchanged is not enough. Overlay noise lightens individual pixels, and this pair has only 0.45 of headroom. Sampled from the render's own `--grain-green`/`--fibre-green` on `#5A6C48`:
  - 17.4 % of background pixels give `#F5EEDF` text less than 4.5:1;
  - the 95th percentile is 4.23:1 and the worst pixel is 3.47:1.
  
  This text is the primary navigation and the lead-in, set in thin EB Garamond (the lead-in is italic). It fails 1.4.3 wherever a glyph lands on a light speck. The panels are fine: ink stays ≥ 7.8:1 and `ink-muted` ≥ 4.6:1 on the textured cream. *Fix:* either take the texture off the green behind text (a `page-green` band under the nav row and lead-in), or cap the green texture so that no pixel is lighter than `#5F7250` (≥ 4.5:1 with headroom), or darken `page-green` by about 2 L* so that the lightest texture pixel still passes. Write the rule "contrast is checked against the lightest texture pixel, not the average" into DESIGN § Contrast pairs.

- **[high]** The "everything above the fold" claim is false, and the spine states it as fact in two places (EXPERIENCE § Component Patterns "Hero panel"; § Key Flows UJ-1 step 1; DESIGN § Layout & Spacing front-page order). Measured bottom of the "Svar på invitasjonen" button:
  - **797px** at 360 × 640, so the button and the deadline line are entirely below the fold;
  - **805px** at 320 × 568;
  - about 240px below the fold in a Messenger in-app browser, which leaves roughly 360 × 560 visible;
  - over 1 100px at 200 % zoom.
  
  The nav row alone takes 104px (two lines), and image 17 takes 152px. Open Question 1 suggests "cap illustration height or shrink the seal", but that is not enough. Even removing *both* leaves the button at about 630px with no margin for the in-app toolbar. Sigmund, who does not scroll speculatively, may never see the deadline or the button. *Fix:* decide it now rather than leave it open:
  - move the nav row *below* the hero, or reduce it to a single "Les mer om helgen ↓" line;
  - cap the illustration at about 90px tall (`object-fit: cover`), or move it below the button;
  - put the deadline directly above the button;
  - re-measure at 360 × 560.
  
  Rewrite UJ-1 step 1 so it does not promise what the layout cannot deliver.

- **[high]** The reflow rules contradict each other at the zoom level older users actually use (DESIGN § Typography "Imperial Script … never below 32px … shrink to fit at 320px rather than wrap"; § Layout & Spacing; EXPERIENCE § Accessibility Floor; § Responsive & Platform). On a phone, "200 % zoom" means Android font scaling (which Chrome now applies as page zoom) or iOS page zoom. That gives a layout viewport of about 180 CSS px, not 320. At 180px:
  - the names need 17px to fit, which breaks the 32px floor, yet `white-space: nowrap` forbids wrapping, so the document becomes 296px wide and scrolls sideways (fails 1.4.10);
  - the nav row becomes four lines (192px).
  
  The render shrinks the names with `cqi` units. This means zoom does not enlarge them, which conflicts with 1.4.4. Container queries are also unsupported in iOS < 16 and older Android WebViews, and that is exactly Sigmund's old phone, where the fallback is a fixed 46px nowrap line that overflows even at 320px (measured 262px of names in a 237px box). Long bokmål compounds ("Allergiopplysningene", "Hardingasete") will also overflow narrow columns. All type tokens are in px, which ignores the browser font-size setting. *Fix:*
  - let the names wrap onto two lines (name / "&" / name, as in inspiration 09) below about 300px instead of shrinking;
  - drop the "shrink to fit" rule and any `cqi`/JS fitting;
  - specify `rem` for type tokens, `overflow-wrap: anywhere` and `hyphens: auto` (with `lang="nb"`);
  - add 180 × 320 as an explicit check width in § Responsive & Platform.

### Medium

- **[medium]** Hint text breaks the spine's own rule, and the 18px floor holds only in the letter (DESIGN § Colors `ink-muted` "Never: … anything the guest must read to act" vs § Components "Text field … hint below in `{typography.small}` `{colors.ink-muted}`"; § Typography). Format hints such as "for eksempel 900" are exactly what the guest must read to act, yet they are set in the smallest and lightest style. EB Garamond's x-height is 0.41, so `small` at 18px renders like about 15px Georgia (the typography render says so itself). That is below the *intent* of NFR-5's 18px floor, and it also covers the progress line and footer meta. *Fix:* set hints in `ink` at `body` size, italic if they must be told apart. Raise `small` to 19–20px, or limit it to text nobody needs to act on (timestamps, "Ikke oppgitt").

- **[medium]** Focus visibility depends on an offset that is never specified (DESIGN § Colors `focus-on-panel`; § Components "Primary button", "Text field"; EXPERIENCE § Accessibility Floor).
  - `focus-on-panel` is `#344628`, the same colour as the primary button fill, so with `outline-offset: 0` the ring merges into the button (1:1).
  - On a text field the ring replaces a 2px `#5E594F` border with a 3px `#344628` ring. The two differ by only 1.50:1, so the focused field looks almost the same as an unfocused one.
  - Rings drawn past a panel edge land on `page-green` at 1.79:1.
  
  *Fix:* add `focus-offset: 3px` as a token and make it mandatory. On fields, use a ring *plus* a thicker border, or a 3px ring offset outside a cream gap. Choose the ring colour by the surface the ring is *painted on*, not by the element's parent. Specify `:focus-visible` with no `outline: none` anywhere.

- **[medium]** Field error, hint and consent semantics are left undefined (DESIGN § Components "Text field", "Choice control"; EXPERIENCE § Component Patterns "Text field", "Error summary"; § Consent & Privacy UX). The spine places the error "between label and field" but never changes the field's visual state: border colour and width stay the same. It also never requires `aria-invalid`, or `aria-describedby` linking the hint and error to the input. The consent explanation must be read *before* Yes/No, but there is no fieldset/legend/describedby structure tying the long text to the radio group. Choice groups get no error placement at all. *Fix:* error state = `error` 3px border plus the error text with icon, `aria-invalid="true"`, and `aria-describedby="hint error"`. Every radio group is a `fieldset`, with the question as `legend` and the error inside the fieldset. Consent text goes in the fieldset, before the radios, and is referenced from the legend.

- **[medium]** Feedback on server-rendered pages is planned as if it were a single-page app (EXPERIENCE § Component Patterns "Notice"; § Accessibility Floor "announced via polite live regions"). Each step, the check page, the receipt and G8 are full page loads (NFR-7 "server pages"). Live regions do not announce content that is present at load, so "Svaret er sendt" and validation results are silent to screen readers unless focus is managed. The page title is also "identical for every guest" and presumably the same for every step, which fails 2.4.2 in practice. *Fix:* on every load, set `<title>` to "Steg 3 av 6: Måltider – Invitasjon", prefixed with "Feil: " when there are errors. Focus the error summary when there are errors; otherwise let focus start at the top, with the `h1` as the step question. Keep live regions for in-page changes only (running total, "Kopiert").

- **[medium]** The step count "Steg n av m" moves under the guest (EXPERIENCE § Component Patterns "Progress line"; DESIGN § Components "Progress line"). If m is recalculated as steps appear or disappear, Sigmund sees "Steg 3 av 5" and then "Steg 4 av 6", which undermines the one orientation cue an older user relies on. It is also set in the smallest type (see the hint finding). *Fix:* settle m after step 1, which determines all conditional steps. Show the step name in the progress line ("Steg 2 av 6: Overnatting"), set it at `body` size, and expose it as the first line under the `h1`.

- **[medium]** Browser Back on POST-driven steps is left unspecified (EXPERIENCE § Interaction Primitives "browser Back equals 'Tilbake' [ASSUMPTION]"). With server-submitted steps, Back produces "Bekreft innsending av skjema" prompts or stale pages. Older users press Back constantly. *Fix:* require Post/Redirect/Get for every step, so each step has its own GET URL and Back is always safe and shows the saved draft (see the critical finding).

- **[medium]** The nav-word row has unaddressed semantics and wayfinding problems (DESIGN § Components "Nav words"; EXPERIENCE § Information Architecture "Navigation").
  - Middle-dot separators written as text are read aloud ("midtpunkt") between every link, and they dangle at line starts when the row wraps.
  - No render has ever shown the row.
  - "Svar" is only about 44px wide at 20px with 6px padding, so NFR-5's 44 × 44 needs explicit inline padding. The spine specifies only height.
  - The row has no entry for the invitation itself, so on G3 the current-page marker works but there is no way "home" except "Tilbake til invitasjonen".
  - "Svar" (a noun or verb with a changing destination) competes with the primary "Svar på invitasjonen".
  
  *Fix:* use `<nav aria-label="Invitasjonen"><ul>` with the dots generated by CSS `::before` (`aria-hidden` by nature). Set an inline padding token so every word is ≥ 44 × 44. Add "Invitasjonen" as the first word on G3. Rename "Svar" to "Ditt svar", or drop it, since the button already exists.

- **[medium]** The couple's names exist only in a hairline script, and there is no defined `h1` (DESIGN § Typography "Imperial Script"; EXPERIENCE § Component Patterns "Hero panel"; § Accessibility Floor "page titles … contain no names").
  - The typography render itself rated Imperial Script "litt tyngre å lese" with "svært tynne oppstreker".
  - On G2 the names appear nowhere else on the screen, and the tab title has no names (FR-4). A guest with low vision or cataracts gets the most important fact (whose wedding) only in the least legible type on the page.
  - The renders use `<p>` for both names and card headings, and the spine never fixes the heading outline.
  
  *Fix:* set the invites line in plain text as "Rikke og Valdemar inviterer deg til bryllup", with the script names as a decorative echo above it (`aria-hidden`). Alternatively, make the `h1` the script names with a plain-text accessible name. Fix the outline: `h1` names/invitation, `h2` per card, `h1` = step question on form pages.

- **[medium]** Forced colours (Windows High Contrast, Android high-contrast themes) break three things (DESIGN § Components "Hero illustration" `mix-blend-mode: darken`, "Choice control", "Primary button").
  - In a dark forced-colour theme the panel background becomes black, and `darken` takes the minimum of the image and the backdrop, so the illustration turns into a solid black box.
  - Custom choice controls whose "selected" state is a `green-dark` *background fill* lose that fill, so checked and unchecked look identical.
  - Primary buttons that are links with only a background have no visible boundary.
  
  *Fix:*
  - bake the panel colour into the shipped JPG instead of blending at runtime; this also guarantees zero colour shift and removes a WebView compatibility risk;
  - draw the check/dot as an SVG or `::after` with `currentColor`, or use native inputs with `accent-color`;
  - give buttons `border: 2px solid transparent`;
  - add a `@media (forced-colors: active)` check to § Accessibility Floor.

- **[medium]** "Light only" is a wish with no mechanism behind it (DESIGN § Brand & Style "Light only"; EXPERIENCE § Foundation). Samsung Internet's dark mode is a likely default browser for older Android users. It and Chrome's auto-dark force-darken pages that do not opt out. Cream panels go dark, ink goes light, and the `darken`-blended illustration collapses. *Fix:* specify `<meta name="color-scheme" content="light only">` and `:root { color-scheme: light only; }`, test in Samsung Internet with dark mode on, and record the result.

- **[medium]** State colours cannot be told apart, so icon shape and text must do all the work, and the spine does not say how (DESIGN § Colors `error`/`success`/`warning`; § Components "Notice", "Status tag"; EXPERIENCE § Component Patterns "Status tag"; IA A4 "unanswered stand out").
  - The three state colours differ from each other by only 1.08–1.17:1 in luminance. To a colour-blind user, or an older eye with yellowed lenses, rust, olive and brown are the same dark brown.
  - The notice spec gives one "22px icon" without saying the icons differ in shape.
  - "Unanswered stand out" in A4 has no mechanism, which in practice means colour.
  
  *Fix:* specify distinct icon shapes (error = triangle/!, warning = circle/!, success = check, info = i) and a visible text prefix ("Feil:", "Obs:"). In A4, mark unanswered households with the word "Ikke svart" and sort them first.

- **[medium]** The undo bar fails timing, focus and obscuring checks (EXPERIENCE § Component Patterns "Undo bar", "Attention item"; § Admin protection tiers tier 1; DESIGN § Components "Undo bar"; § Accessibility Floor 2.4.11).
  - Ten seconds is not enough for a screen-reader or switch user to hear a polite announcement and travel to a bar at the bottom of the viewport.
  - The "can also be unmarked later" escape hatch has no defined location, so the timed bar may be the *only* undo, which falls under 2.2.1.
  - "Merk som håndtert" removes the focused row, so focus drops to `<body>`.
  - A fixed bottom bar is exactly the sticky element the spine bans on guest pages (2.4.11), and at 200 % zoom it covers a large share of a phone screen.
  
  *Fix:* replace the row in place with "Merket som håndtert. Angre", move focus to "Angre", and keep it until the user leaves the page (no timer). Define where handled items can be found and unmarked (a "Vis håndterte" filter). No fixed bars in admin either.

- **[medium]** Admin session expiry loses input, and the spine leaves it open (EXPERIENCE § State Patterns "Session expired"; Open Question 8). Logging Rikke out mid-edit with no warning and no extension fails 2.2.1 unless the session lasts ≥ 20 hours. *Fix:* decide now: either a ≥ 20-hour idle session, or a warning dialog two minutes before expiry with "Fortsett å være logget inn", plus restoring the unsaved form after logging in again.

- **[medium]** Dialog behaviour is underspecified for phones and screen readers (EXPERIENCE § Component Patterns "Dialog"; DESIGN § Components "Dialog").
  - "Focus moves into it" does not say *to what*. For tier 2 and 3 the consequence sentence must be heard first.
  - "Actions right-aligned, safest action first" is ambiguous in DOM versus visual order, and right-aligned side-by-side buttons do not survive 320px or 200 %.
  - "Esc = cancel" does not exist on a phone, and scrim taps are unspecified.
  - The guest leave-warning dialog has no button wording.
  
  *Fix:* use `role="alertdialog"` with `aria-labelledby` set to the heading and `aria-describedby` set to the consequence, and focus the safe button (or the heading for tier 3). Stack buttons full-width on narrow screens, safe action first in both DOM and visual order. A scrim tap equals cancel. The leave warning says "Svaret er ikke sendt ennå", with buttons "Bli og fullfør svaret" (primary) and "Gå uten å sende". Let the dialog body scroll at 200 %.

- **[medium]** The "Kopier" buttons on G7 are identical and fragile in in-app browsers (DESIGN § Components "Payment details"; EXPERIENCE § Component Patterns "Payment details").
  - Four buttons all named "Kopier" are ambiguous to screen readers and voice control.
  - `navigator.clipboard` is missing or blocked in some Messenger and Facebook WebViews, so the button may silently do nothing while showing nothing.
  - "Kopiert inline" has no announcement and no duration.
  
  *Fix:* accessible names "Kopier kontonummer" and so on (the visible label may stay "Kopier"). Feature-detect, and hide the button when copying is unsupported. Values are always selectable plain text at `body` size with lining figures. "Kopiert" goes in a polite live region and stays until the next copy.

- **[medium]** The footer phone numbers, the help path for older guests, have no stated targets (DESIGN § Components "Footer band"; EXPERIENCE § Component Patterns "Footer band"). In color-themes-5 the two numbers share one paragraph separated by `<br>` at 27px line height, so two adjacent `tel:` targets are well under NFR-5's 44px, and a mis-tap calls the wrong person. *Fix:* give each contact its own ≥ 44px row: "Ring Rikke 900 00 000" and "Send SMS til Rikke", as separate full-width links. Note that `sms:` body syntax differs between iOS and Android, so link the number only.

- **[medium]** Guest content must not depend on JavaScript in v1, yet the spine defers that guarantee to [2027] (EXPERIENCE § Component Patterns "Hero panel … Renders without JavaScript [2027]"; § State Patterns "Static fallback [2027]"). Read literally, the v1 invitation and form may require JS, which old phones and in-app browsers fail on first. *Fix:* in v1, all guest pages and form steps are server-rendered HTML that work without JS. JS only adds the running-total update, copy buttons and the envelope. Only the envelope's fallback can wait for [2027].

### Low

- **[low]** The illustration's alt text is long and read before the names (EXPERIENCE § Component Patterns "Hero illustration"; illustration-3.html alt for I7, about 200 characters). A screen-reader user hears a description of a watercolour before learning whose wedding it is, and the venue is described in text on G3 anyway. *Fix:* use `alt=""` (decorative, since its information is in the text), or a short alt such as "Akvarell av tunet på Hardingasete."

- **[low]** The seal is marked decorative but carries live text (EXPERIENCE § Component Patterns "Wax seal" `alt=""`; renders put "R &amp; V" in a `<span>`). An `alt=""` on an image does not hide sibling text, so screen readers announce "R og V" before the names. *Fix:* `aria-hidden="true"` on the whole seal container, or render the seal and monogram as one SVG with `alt=""`.

- **[low]** Four identical visible "Les mer" links, and the card itself is not a target (DESIGN § Components "Info card"; EXPERIENCE § Component Patterns "Info card"). The hidden "om programmet" helps screen readers but not Sigmund, who will tap the heading "Programmet" and get nothing. *Fix:* make the visible link text "Les mer om programmet", or make the heading the link with the whole card as the hit area (one link per card).

- **[low]** The respondent switch "Bytt" is a link that changes state (DESIGN § Components "Respondent line"; EXPERIENCE § Component Patterns "Text link … never submits data"). "Bytt" alone does not say what it changes, it sits first on every step, and as a link it contradicts the rule that links never change data. *Fix:* use a button with the accessible name "Bytt hvem som svarer" and `aria-expanded`, give it a ≥ 44px target, and place it after the step question rather than before.

- **[low]** Hover and pressed states give no tap feedback (DESIGN § Colors `green-dark-hover`). `#2C3A20` against `#344628` is 1.18:1, so on a phone the "did my tap work?" signal is invisible until the "Sender …" text appears, and that appears only on submits. *Fix:* the pressed state also gets the 3px offset ring, or an inset cream rule, and every button responds visibly on `:active`.

- **[low]** The lining figures are still an [ASSUMPTION] and may be stripped by subsetting (DESIGN § Typography "Figures"). EB Garamond defaults to old-style figures, which are hard for older eyes to read in "1 450 kr", "23:59" and account numbers. Subsetting tools often drop the `lnum` and `tnum` features. *Fix:* make lining figures a requirement (`font-variant-numeric: lining-nums`), keep `lnum` and `tnum` in the self-hosted WOFF2 subset, and verify in the built page. Use a non-breaking space in "1 450" so screen readers read one number.

- **[low]** The typed confirmation will fight phone keyboards (EXPERIENCE § Admin protection tiers tier 3; Voice and Tone "Tier-3 typed word"). Autocapitalise and autocorrect will turn "SLETT" into "Slett" or a suggestion. Household "names" with "og", commas or æøå invite mismatches, and a disabled destructive button does not explain itself. *Fix:* match case-insensitively with trimmed whitespace, set `autocapitalize="off" autocorrect="off" spellcheck="false"`, show the exact word to type in plain text in the label, and keep the button enabled but validate on press with an inline error.

- **[low]** The envelope reveal needs more than reduce-motion (EXPERIENCE § Envelope reveal; DESIGN § Components "Envelope reveal"). It needs:
  - a cap of 5 s or less (2.2.2);
  - the static invitation present in the DOM and readable by screen readers underneath, not `display: none` until the animation ends;
  - focus and scroll at the top of G2 afterwards;
  - "Hopp over" ≥ 44 × 44, placed on cream or `green-dark` (not on textured `page-green`, see the texture finding);
  - a fail-safe: no JS or storage means no envelope.
  
  *Fix:* add these as acceptance criteria next to the [If time] item.

- **[low]** Admin density competes with targets and type size (DESIGN § Layout & Spacing "Admin"; tokens `admin-body` 18px, `admin-gap` 8px; EXPERIENCE § Accessibility Floor "admin the same [ASSUMPTION]"). Rows of 18px EB Garamond (about 15px Georgia-equivalent) with 8px gaps and 44px targets will not fit FR-48's "one phone screen" for long lists. Something will give, and the spine does not say what. Stacked mobile tables also lose header associations. *Fix:* state that 44px targets win over density. Stacked rows repeat their labels as visible text ("Betalt: 900 kr"), not as CSS-only headers.
