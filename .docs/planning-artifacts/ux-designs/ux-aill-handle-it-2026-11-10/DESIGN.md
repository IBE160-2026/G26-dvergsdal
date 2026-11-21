---
name: "AI'll handle it"
description: "Rikke & Valdemar's wedding invitation as a website: cream paper sheets with soft hand-made edges on a textured olive-green page, a dark green wax seal, gypsophila and lily garlands, pictures in cream lace frames, a script name line and printed-invitation body text. Light only."
status: final
created: 2026-11-10
updated: 2026-11-20
colors:
  page-green: '#5A6C48'
  green-dark: '#344628'
  green-dark-hover: '#2C3A20'
  seal: '#344628'
  panel-cream: '#EBE4D5'
  ink: '#3B372F'
  ink-muted: '#5E594F'
  cream-on-green: '#F5EEDF'
  field-surface: '#F7F2E7'
  field-border: '#5E594F'
  divider: '#C8BFAE'
  focus-on-panel: '#344628'
  focus-on-green: '#F5EEDF'
  error: '#7C3B1D'
  success: '#3D5A2A'
  warning: '#765012'
  scrim: '#141A0C'
typography:
  display-names:
    fontFamily: 'Imperial Script'
    fontSize: 48px
    fontWeight: '400'
    lineHeight: '1.15'
  signature:
    fontFamily: 'Imperial Script'
    fontSize: 40px
    fontWeight: '400'
    lineHeight: '1.1'
  heading-page:
    fontFamily: 'EB Garamond'
    fontSize: 32px
    fontWeight: '400'
    lineHeight: '1.2'
  heading-section:
    fontFamily: 'EB Garamond'
    fontSize: 32px
    fontWeight: '400'
    lineHeight: '1.2'
  topic-title:
    fontFamily: 'EB Garamond'
    fontSize: 21px
    fontWeight: '400'
    lineHeight: '1.2'
  button-small:
    fontFamily: 'EB Garamond'
    fontSize: 19px
    fontWeight: '400'
    lineHeight: '1.1'
  heading-card:
    fontFamily: 'EB Garamond'
    fontSize: 26px
    fontWeight: '400'
    lineHeight: '1.3'
  date-line:
    fontFamily: 'EB Garamond'
    fontSize: 23px
    fontWeight: '400'
    lineHeight: '1.3'
    letterSpacing: '0.14em'
  place-line:
    fontFamily: 'EB Garamond'
    fontSize: 20px
    fontWeight: '400'
    lineHeight: '1.3'
    letterSpacing: '0.14em'
  lead-in:
    fontFamily: 'EB Garamond'
    fontSize: 24px
    fontWeight: '400'
    lineHeight: '1.4'
  invites:
    fontFamily: 'EB Garamond'
    fontSize: 20px
    fontWeight: '400'
    lineHeight: '1.3'
  button:
    fontFamily: 'EB Garamond'
    fontSize: 21px
    fontWeight: '400'
    lineHeight: '1.3'
  body:
    fontFamily: 'EB Garamond'
    fontSize: 20px
    fontWeight: '400'
    lineHeight: '1.5'
  label:
    fontFamily: 'EB Garamond'
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  jump-links:
    fontFamily: 'EB Garamond'
    fontSize: 19px
    fontWeight: '400'
    lineHeight: '1.2'
    letterSpacing: '0.08em'
  nav-button:
    fontFamily: 'EB Garamond'
    fontSize: 19px
    fontWeight: '400'
    lineHeight: '1'
  nav-words:
    fontFamily: 'EB Garamond'
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.2'
    letterSpacing: '0.02em'
  small:
    fontFamily: 'EB Garamond'
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.45'
  admin-heading:
    fontFamily: 'EB Garamond'
    fontSize: 22px
    fontWeight: '600'
    lineHeight: '1.25'
  admin-title:
    fontFamily: 'EB Garamond'
    fontSize: 28px
    fontWeight: '400'
    lineHeight: '1.2'
  admin-body:
    fontFamily: 'EB Garamond'
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.4'
rounded:
  sm: 3px
  md: 4px
  sheet: 5px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 20px
  '6': 24px
  '7': 32px
  gutter: 16px
  gutter-narrow: 8px
  gutter-small-phone: 12px
  hero-padding-inline-small-phone: 10px
  page-padding-top: 42px
  hero-padding-top: 22px
  hero-padding-bottom: 16px
  hero-padding-inline: 20px
  admin-panel-padding: 12px
  admin-gap: 8px
  content-max: 480px
  target-min: 44px
  button-height: 52px
  nav-height: 64px
  scroll-gap: 12px
  focus-width: 3px
  focus-offset: 3px
components:
  page:
    background: '{colors.page-green}'
    texture: 'calm paper grain (grain-green in mockups/paper-ceremony-5.html); zero average colour shift'
    paddingTop: '{spacing.page-padding-top}'
  nav-bar:
    background: '{colors.page-green}'
    texture: 'none (flat, so cream text keeps 4.95:1)'
    height: '{spacing.nav-height}'
    padding: '8px 12px 8px 16px'
    hairline: 'box-shadow 0 1px 0 rgba(245,238,223,.22), takes no height; 1px CanvasText border under forced colors'
    position: 'sticky top 0, only when the viewport is >= 400px tall and >= 20em (320px at the default text size) wide'
  nav-words:
    foreground: '{colors.cream-on-green}'
    typography: '{typography.nav-words}'
    gap: '12px'
    underline: 'none; current page 2px, offset 4px'
    minHeight: '{spacing.target-min}'
  nav-svar:
    background: '{colors.green-dark}'
    foreground: '{colors.cream-on-green}'
    border: '1px solid {colors.cream-on-green}'
    radius: '{rounded.md}'
    minHeight: '{spacing.target-min}'
    minWidth: 64px
    padding: '0 16px'
    minWidthSmallPhone: 56px
    paddingSmallPhone: '0 12px'
    typography: '{typography.nav-button}'
  paper-sheet:
    background: '{colors.panel-cream}'
    texture: 'grain-sheet + fibre-sheet, overlay'
    radius: '{rounded.sheet}'
    edge: 'filter edge-b3: soft wave, fine fibre, same colour as the sheet, no rim'
    shadow: 'part of edge-b3: blur 3.2px, offset 0 2.5px, #141A0C at 42 %'
    layer: 'colour, texture, edge and shadow on ::before behind the content'
    fallback: 'flat {colors.panel-cream} with {rounded.sheet} under forced-colors or without filter support'
  panel:
    sheet: '{components.paper-sheet}'
    foreground: '{colors.ink}'
    padding: '24px 22px 14px'
  hero-panel:
    sheet: '{components.paper-sheet}'
    foreground: '{colors.ink}'
    padding: '{spacing.hero-padding-top} {spacing.hero-padding-inline} {spacing.hero-padding-bottom}'
  rsvp-panel:
    sheet: '{components.paper-sheet}'
    foreground: '{colors.ink}'
    padding: '26px 22px 24px'
    jumpTarget: 'cleared by html scroll-padding-top (nav-height + scroll-gap); no scroll-margin'
  wax-seal:
    image: 'mockups/segl.png (Rikke, image tool; cut out to transparent PNG)'
    width: 74px
    position: 'centred over the hero sheet top edge, top -36px'
    shadow: 'drop-shadow 0 2px 2px rgba(12,16,8,.45)'
  hero-illustration:
    image: 'ux/egne-bilder/04-Illustration.jpg (watercolour of the farmyard, Rikke, image tool)'
    width: 262px
    height: auto
    marginTop: '-12px (its top is empty sky)'
    blend: 'mix-blend-mode: darken; normal under forced-colors'
  flower-divider:
    image: 'mockups/brudeslor.png (gypsophila, Rikke, image tool; cut out to transparent PNG)'
    width: '224px in the hero; 180px in the RSVP sheet'
    blend: 'none (white petals must stay white)'
  lily-garland:
    imageTop: 'mockups/lilje-topp.png (arches with the centre high; above the details heading)'
    imageBottom: 'mockups/lilje-bunn.png (centre low; below the last topic row)'
    width: 296px
    spacing: '8px below the top garland; 14px above the bottom garland'
    blend: 'none'
  details-section:
    background: 'none: directly on the textured {colors.page-green}, no sheet'
    foreground: '{colors.cream-on-green}'
    heading: '{typography.heading-section}, italic, centred'
    headingRule: '1px rgba(245,238,223,.5) under the heading, 12px below the text, 6px inset'
    padding: '0 2px 4px'
  topic-row:
    layout: 'picture left, text right, top-aligned, gap 14px'
    padding: '20px 0 6px'
    title: '{typography.topic-title}'
    text: '{typography.body}, italic'
  lace-frame:
    image: 'mockups/blonde.png (Rikke, image tool; recoloured to {colors.panel-cream})'
    width: 136px
    aspectRatio: '932 / 901'
    photoWindow: 'left 5.2%, top 5.3%, width 89.6%, height 89.4%; photo object-fit cover, under the frame'
    shadow: 'drop-shadow 0 1px 1.5px rgba(10,14,6,.35)'
    widthOnInfoSheet: '220px, centred at the top of the sheet body, 6px above and 14px below'
  programme-timeline:
    line: '1px rgba(59,55,47,.45), centred, along the whole list, 6px in from its top and bottom'
    dot: '6px circle in {colors.ink} on the line, level with the time'
    layout: 'events alternate right-aligned left of the line and left-aligned right of it, 18px from the line; each event overlaps the one before by 36px in height'
    time: '{typography.small}, lining and tabular figures, letter spacing 0.04em'
    name: '{typography.body}, italic, line height 1.25'
  programme-icon:
    image: 'mockups/ikoner/ikon-01-fjelltur.png … ikon-12-avreise.png (Rikke, image tool; cut out and recoloured to {colors.ink})'
    size: 56px
    position: 'above the time, on the line side, aligned with the text, 4px below'
  good-to-know:
    rule: '1px rgba(59,55,47,.25) above, 14px above the rule, 10px below'
    heading: '{typography.body}, italic («Godt å vite»)'
    list: 'bulleted, {typography.body}'
  story-sheet:
    sheet: '{components.paper-sheet}'
    foreground: '{colors.ink}'
    padding: '22px 22px 18px'
    photo: '{components.lace-frame} at 220px, centred under the heading'
    chapterLine: '{typography.body}, italic, 18px above, 4px below'
    closing: '{typography.body}, italic, centred, 18px above'
    signature: '{typography.signature}, centred'
  voluntary-line:
    foreground: '{colors.cream-on-green}'
    typography: '{typography.body}, italic, centred'
    margin: '6px 10px 0, under the jump links'
  info-page-title:
    foreground: '{colors.cream-on-green}'
    typography: '{typography.heading-page}, italic, centred'
    rule: '1px rgba(245,238,223,.5) under the title, 12px below the text, 6px inset'
  back-link:
    foreground: '{colors.cream-on-green}'
    typography: '{typography.body}'
    underline: '1px, offset 4px'
    minHeight: '{spacing.target-min}'
  jump-links:
    foreground: '{colors.cream-on-green}'
    typography: '{typography.jump-links}, small capitals'
    layout: 'centred lines of two or three words, middle dot between words (decorative), no underline'
    rowHeight: '{spacing.target-min}'
  info-sheet:
    sheet: '{components.paper-sheet}'
    foreground: '{colors.ink}'
    padding: '22px 22px 12px'
    gap: 20px
    heading: '{typography.heading-card}, italic, left'
    headingRule: '1px rgba(59,55,47,.35) under the heading, 8px below the text'
    jumpTarget: 'cleared by html scroll-padding-top (nav-height + scroll-gap); no scroll-margin'
  button-on-green:
    background: 'transparent'
    foreground: '{colors.cream-on-green}'
    border: '1.5px solid {colors.cream-on-green}'
    radius: '{rounded.md}'
    minHeight: '{spacing.target-min}'
    padding: '0 14px'
    typography: '{typography.button-small}'
  button-primary:
    background: '{colors.green-dark}'
    foreground: '{colors.cream-on-green}'
    hover: '{colors.green-dark-hover}'
    border: '2px solid transparent'
    radius: '{rounded.md}'
    minHeight: '{spacing.button-height}'
    typography: '{typography.button}'
  button-secondary:
    background: '{colors.panel-cream}'
    foreground: '{colors.green-dark}'
    border: '1.5px solid {colors.green-dark}'
    hover: 'border 3px'
    radius: '{rounded.md}'
    minHeight: '{spacing.target-min}'
  button-destructive:
    background: '{colors.panel-cream}'
    foreground: '{colors.error}'
    border: '1.5px solid {colors.error}'
    hover: 'border 3px'
    radius: '{rounded.md}'
    minHeight: '{spacing.target-min}'
  focus-ring:
    width: '{spacing.focus-width}'
    offset: '{spacing.focus-offset}'
    onPanel: '{colors.focus-on-panel}'
    onGreen: '{colors.focus-on-green}'
  link-more:
    foreground: 'inherit'
    underline: '1px, offset 4px; 2px on hover/pressed'
    minHeight: '{spacing.target-min}'
  lead-in:
    foreground: '{colors.cream-on-green}'
    typography: '{typography.lead-in}'
    padding: '26px 10px 22px'
  footer-band:
    background: '{colors.green-dark}'
    foreground: '{colors.cream-on-green}'
    padding: '22px 16px 26px'
  field:
    background: '{colors.field-surface}'
    foreground: '{colors.ink}'
    border: '2px solid {colors.field-border}'
    borderError: '3px solid {colors.error}'
    radius: '{rounded.sm}'
    minHeight: '{spacing.target-min}'
  choice-control:
    box: 26px
    border: '2px solid {colors.ink}'
    selected: '{colors.green-dark}'
    radiusCheckbox: '{rounded.md}'
    radiusRadio: '{rounded.full}'
    rowMinHeight: '{spacing.target-min}'
  notice:
    border: '4px left, currentColor'
    icon: 22px
    padding: '{spacing.2} {spacing.3}'
    radius: '{rounded.sm}'
  status-tag:
    typography: '{typography.admin-body}'
    border: '1.5px solid currentColor'
    radius: '{rounded.sm}'
  admin-panel:
    background: '{colors.panel-cream}'
    foreground: '{colors.ink}'
    padding: '{spacing.admin-panel-padding}'
    gap: '{spacing.admin-gap}'
    radius: '{rounded.sm}'
    edge: 'straight, sheet paper texture, no edge filter'
  attention-panel:
    background: '{colors.panel-cream}'
    foreground: '{colors.ink}'
    borderTop: '5px solid {colors.green-dark}'
    padding: '{spacing.admin-panel-padding}'
    radius: '{rounded.sm}'
  answer-progress:
    typography: '{typography.label}'
    barHeight: 12px
    barTrack: '{colors.cream-on-green}'
    barFill: '{colors.green-dark}'
    barBorder: '1px solid {colors.ink-muted}'
    radius: '{rounded.sm}'
  dialog:
    background: '{colors.panel-cream}'
    scrim: '{colors.scrim}'
    radius: '{rounded.sm}'
---

# AI'll handle it — Design Spine

> Visual identity for the guest invitation and the couple's admin area. Behaviour, states and flows live in [EXPERIENCE.md](EXPERIENCE.md). Decisions are logged in [.memlog.md](.memlog.md); requirements in the [PRD](../../prds/prd-aill-handle-it-2026-11-07/prd.md) and its [addendum](../../prds/prd-aill-handle-it-2026-11-07/addendum.md). Renders are linked in the sections they illustrate. **DESIGN.md and EXPERIENCE.md (the spines) win on any conflict with a render (a mockup file).**

## Brand & Style

The site **is** the invitation. A guest opening their link should think what Rikke and Valdemar said in the brain dump: *"wow, what a lovely invitation, and so easy to get an overview"* and *"wow, so cosy! I want to be part of this."* The posture is a printed wedding card from a timber farmhouse in Hardanger: classic, clean, slightly old-fashioned, warm. Nature and elegance with historic wooden-building character, never luxury.

The visual language follows from that:

- **An envelope-coloured page with paper sheets on it.** Olive-green textured page, and cream sheets with soft, hand-made edges and a soft shadow carrying the content (direction B *Konvolutten*, about half green, half cream). The sheets look like the main sheet in [inspiration 01](../../ux/inspirasjon/01-Vibe.jpg), in the sheet's own colour (memlog, *Sheet edge refined*).
- **Solemn, not cabin-cosy.** Rikke found the earlier version gave a "hytte" feeling and wanted it more festive (memlog 100). The top sheet is therefore laid out like a formal printed invitation: seal over the top edge, the farmyard drawing, the names, "inviterer dere til sitt bryllup", a flower divider, then date and place in letter-spaced small capitals.
- **A hand-pressed wax seal** in dark green with *R & V*, made by Rikke in an image tool ([06-Stamp.jpg](../../ux/egne-bilder/06-Stamp.jpg)), lying over the top edge of the invitation; also the browser-tab icon.
- **Flowers from the wedding, in four fixed places.** A gypsophila (*brudeslør*) divider made by Rikke ([07-Flowers.jpg](../../ux/egne-bilder/07-Flowers.jpg)) in the hero and, smaller, in the RSVP sheet; and two lily garlands, also Rikke's ([09-FlowersTop.jpg](../../ux/egne-bilder/09-FlowersTop.jpg), [10-FlowersBottom.jpg](../../ux/egne-bilder/10-FlowersBottom.jpg)), above and below «Alt om helgen», each bowing towards the text. Never spread over the page, not like [inspiration 05](../../ux/inspirasjon/05-Vibe.jpg).
- **«The finer details», as in [inspiration 09](../../ux/inspirasjon/09-Example.jpg).** Below the invitation, the topics stand directly on the green page with a picture on the left in a cream lace frame ([11-Frame.jpg](../../ux/egne-bilder/11-Frame.jpg)) and the text beside it. Rikke found plain cards «for enkelt og trist» (memlog, 2026-11-14).
- **One script moment.** The couple's first names in a formal copperplate-style script (as in [inspiration 09](../../ux/inspirasjon/09-Example.jpg)); everything else in a book serif that reads like a printed invitation.
- **One illustration.** A soft sage watercolour of Hardingasete in the top sheet, shown whole.
- **Real paper, not a hint of it.** Visible paper texture on page and sheets, tuned so it never changes the colours and never costs text contrast.

What it is not: gold, diamonds, metallic, glitter, neon, blinking or animated noise, clutter, luxury-brand gloss, draping, heart-shaped or lace letters (lace is only a frame around pictures), bluish "sage" greens, flowers spread over the page, sprigs or lace drawn in code. The guest list spans everyone from teenagers to bestefar Sigmund (78), so restraint and legibility outrank decoration everywhere.

**Light only.** There is no dark mode; the invitation looks the same at all times (memlog, decision D). Pages declare `color-scheme: light only` so browser auto-dark modes (Samsung Internet, Chrome) leave them alone.

## Colors

The palette was chosen over six render rounds from colours sampled in the couple's own inspiration images, then tuned by their perception (memlog, *Page green FINAL*). Final pick: page **G4a**, panel **K1 havre**, text **T2**. The five candidate greens side by side: [mockups/color-themes-5.html](mockups/color-themes-5.html) (G4a is the chosen one; the render predates the final fonts and illustration).

| Token | Hex | Role | Never |
|---|---|---|---|
| `page-green` | `#5A6C48` | The page behind everything, including the sticky nav bar (flat there, textured elsewhere): a warm, slightly less yellow olive (G4a, hue ~90°). Also the envelope in the [If time] reveal. | Text on cream; button fill (it is only 1.79:1 against `green-dark`). |
| `green-dark` | `#344628` | Primary button fill, nav "Svar" button, footer band, focus ring on panels, A2 attention-panel top rule and answer-progress bar fill. | A page background (round 6 dark page rejected). |
| `green-dark-hover` | `#2C3A20` | Primary button hover/pressed; 10.49:1 with cream text. Too close to `green-dark` (1.18:1) to be the only tap feedback — see Focus ring. | Anything but the pressed button. |
| `seal` | `#344628` | The colour the seal image was made to match; used only if the seal has to be drawn without the image (e.g. a simplified favicon). Same value as `green-dark`. | — |
| `panel-cream` | `#EBE4D5` | All content panels ("havre"); also the colour of the lace frames, so they read as the same paper (Rikke: «krem/havre som resten av det hvite»). | Large areas without texture. |
| `ink` | `#3B372F` | All text inside panels, including the names and form hints (T2 warm grey, chosen over dark green and walnut). | Text on green. |
| `ink-muted` | `#5E594F` | Only text nobody needs to act on: timestamps, "Ikke oppgitt", example-number notes. | Hints, body copy, progress line, anything the guest must read to act. |
| `cream-on-green` | `#F5EEDF` | Text, links, focus ring and the nav "Svar" button's 1px border on `page-green` and `green-dark`; the details section's text, heading rule and outlined buttons; also the empty track of the A2 answer-progress bar. | Panel background. |
| `field-surface` | `#F7F2E7` | Inside text fields, so fields read as "write here" on the panel. | Panels. |
| `field-border` | `#5E594F` | Text-field and select outline. | Decorative rules. |
| `divider` | `#C8BFAE` | 1px hairlines between admin rows and check-answer rows; never carries meaning on its own **[ASSUMPTION — no render defined a hairline]**. | Field outlines, focus. |
| `focus-on-panel` | `#344628` | Focus ring painted on cream. | — |
| `focus-on-green` | `#F5EEDF` | Focus ring painted on green and in the footer band. | — |
| `error` | `#7C3B1D` | Errors, tier-3 destructive actions, "Stemmer ikke". Sampled from the rust wax seal in inspiration 01. | Decoration; the only signal of an error. |
| `success` | `#3D5A2A` | "Svaret er sendt", saved confirmations, "Betalt", A2 «Ingenting trenger oppfølging nå». Picked by Claude for the renders; not chosen by the couple. | Primary buttons. |
| `warning` | `#765012` | "Ikke sendt ennå", unsent-draft notice, allergy-without-consent, conflict, unpaid. Picked by Claude for the renders; not chosen by the couple. | Errors. |
| `scrim` | `#141A0C` | The dimmed backdrop behind dialogs, at 60 % opacity (the near-black green of the sheet shadow; approved in the admin and privacy renders, 2026-11-15). | — |

**Dark wood** from the brief has no UI token: walnut text (text candidate T3) was rejected, so dark wood lives only in photographs of the venue and in the illustration **[ASSUMPTION]**.

`error`, `success` and `warning` differ from each other by only 1.08–1.17:1 in luminance; they read as one dark brown to many older or colour-blind eyes. State is therefore always carried by **icon shape and words**, never colour (see Components › Notice, Status tag).

### Contrast pairs (WCAG 2.x, all text ≥ 4.5:1 — NFR-5)

| Pair | Ratio | Use |
|---|---|---|
| `ink` on `panel-cream` | 9.35:1 | All panel text |
| `ink` on `field-surface` | 10.61:1 | Typed text |
| `ink-muted` on `panel-cream` / `field-surface` | 5.50 / 6.23:1 | Meta only |
| `green-dark` on `panel-cream` | 8.08:1 | Secondary button text, focus ring on cream |
| `cream-on-green` on `page-green` (flat) | **4.95:1** | Nav words in the flat nav bar — the lowest small-text pair; never smaller than 18px |
| `cream-on-green` on the green texture, averaged over 3 × 3 px | **4.50:1** worst (4.61:1 at 4 × 4 px) | Cream text of **19px or more** on the textured green: the lead-in, the details heading, topic titles and text, the outlined buttons, and on info pages the title, the back link and the jump links. Single lightest pixel `#6D8358`: 3.61:1. Measured in headless Chrome (see Elevation & Depth) |
| `cream-on-green` on `green-dark` | 8.86:1 | Buttons, nav "Svar", footer |
| `cream-on-green` on `green-dark-hover` | 10.49:1 | Pressed button |
| `error` on `panel-cream` / `field-surface` | 6.64 / 7.52:1 | Error text, destructive button |
| `success` on `panel-cream` | 6.16:1 | Success notice |
| `warning` on `panel-cream` | 5.67:1 | Warning notice |
| `field-border` vs `panel-cream` | 5.50:1 | Non-text, ≥ 3:1 required |
| `panel-cream` vs `page-green` | 4.52:1 | Panel edge against page (non-text) |
| `cream-on-green` border vs `page-green` | 4.95:1 | Nav "Svar" button outline (non-text); without it the button is 1.79:1 against the bar |

**Rule:** contrast on a textured surface is checked against the texture **averaged over an area no wider than a letter stroke** (3 × 3 px for 20px EB Garamond), never against the overall average (memlog, *Contrast method refined*). On the sheets, the single darkest pixel still passes for every pair.

The PRD addendum asks to check "sage green on soft white": `page-green` is never text on cream. The only green-on-cream pair is `green-dark` on `panel-cream`, at 8.08:1.

## Typography

Two self-hosted families, both SIL Open Font License, served from our own server as WOFF2 with Latin subsets including æ, ø, å, **keeping the `lnum` and `tnum` features** (PRD 3.2: guest pages load nothing from other companies). The Google Fonts links in the renders are a planning-mock exception only. Specimens: [mockups/typography-1.html](mockups/typography-1.html) (candidates S1–S6 and B1–B4; the chosen S4 + B1 at 20px are shown together in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html)).

- **Imperial Script** — the couple's first names only (*Rikke & Valdemar*, no surnames). Its upstrokes are hair-thin, so it is **display only**: the names at `{typography.display-names}` and the same names as a signature at the end of *Vår historie* (`{typography.signature}`, 40px) are the only Imperial Script on the site. Never for headings, labels, buttons or the admin area. The *R & V* on the seal is part of Rikke's seal image, not live text. Fallback: Georgia italic **[ASSUMPTION]**.
  - **Names wrap, never shrink.** At 48px one line needs about 274px (the 262px measured at 46px, scaled); the hero's content box is 288px on a 360px phone, so they fit on one line there. When they do not fit, the names stack on three centred lines — *Rikke* / *&* / *Valdemar* — as in inspiration 09. No shrink-to-fit, no `cqi` units, no JS fitting, no `nowrap`. *Valdemar* alone is about 142px, which fits every layout width down to 180 CSS px once the narrow-width gutters apply (Layout & Spacing). Re-measure in the build.
- **EB Garamond** — everything else. Its short x-height (0.41) is why guest body text is **20px**, above the NFR-5 floor of 18px (memlog, *Body font*). Regular and italic; weight 600 for labels and emphasis **[ASSUMPTION — the render used bold; 600 is the nearest weight to load]**. Fallback: Georgia.

Type tokens are written in px for readability; build them in `rem` (px ÷ 16) so the phone's text-size setting scales them. Running text uses `overflow-wrap: break-word` and `hyphens: auto` with `lang="nb"` so long compounds ("Allergiopplysningene") never force sideways scroll; the script names are never hyphenated.

| Role | Token | Where |
|---|---|---|
| Names | `display-names` | Hero sheet only; `h1` of the front page |
| Signature | `signature` | «Rikke & Valdemar» at the end of *Vår historie*, centred; the only other Imperial Script |
| Page title | `heading-page` | Info pages (*italic*, centred, cream on green with a cream hairline under it, like the details heading), form step question (`h1`), check page heading, receipt heading «Svaret er sendt» (32px, as rendered in the key-screen mockups) |
| Section heading | `heading-section`, *italic* | «Alt om helgen» (`h2`), on green with a cream hairline under it (Rikke: «klassisk inntrykk») |
| Topic title | `topic-title` | Programmet · Praktisk informasjon · Vår historie (`h3`); 21px so «Praktisk informasjon» fits one line beside the frame (166.9px in a 174px column; 22px needed 174.9px) |
| Topic text | `body`, *italic* | One line under each topic title, e.g. «Fra vi møttes til i dag.»; italic so it reads lighter than the title (EB Garamond has no weight below 400) |
| Card heading | `heading-card` | RSVP sheet and other panel headings (`h2`); on info pages *italic* with a thin ink hairline under it (Vielsen, Husregler …) |
| Jump links | `jump-links`, small capitals | «Hopp til» on info pages: short words such as *Vielsen · Hardingasete*, cream on green |
| Invites line | `invites`, *italic* | «inviterer dere til sitt bryllup» (du/dere rule, EXPERIENCE › Voice and Tone) |
| Date | `date-line`, small capitals | «Lørdag 27. mai 2028» in the hero |
| Place | `place-line`, small capitals | «Hardingasete · Hardanger» in the hero |
| Household line | `body`, *italic*; names upright | «for **Sigmund og bestemor**» in the hero (names upright regular, not bold) |
| Lead-in | `lead-in`, *italic* | One line on green between the hero and «Alt om helgen» |
| Small button on green | `button-small` | «Les mer» under each topic |
| Nav words | `nav-words` | Sticky nav bar, 18px, slight letter spacing; only on the flat nav bar (Elevation & Depth) |
| Nav "Svar" | `nav-button` | The button in the nav bar |
| Buttons | `button` | All other guest buttons |
| Body | `body` | All guest running text, form hints (*italic*), progress line |
| Labels | `label` | Form labels and legends |
| Small | `small` | Text nobody acts on: timestamps, "Ikke oppgitt", footer meta, and the programme times (semibold lining figures, approved by Rikke). The 18px floor; nothing on guest pages is smaller |
| Admin | `admin-title`, `admin-heading`, `admin-body` | Admin working screens, denser, 18px body (approved in the admin renders); page titles 28px; the A2 answer-progress line («Svart: 28 av 30 husstander») uses `label` (20px, 600) |

**Figures:** amounts, dates, times, phone and account numbers use lining figures (`font-variant-numeric: lining-nums`), tables also tabular (`tabular-nums`); EB Garamond defaults to old-style figures, which older eyes misread. Thousands use a non-breaking space ("1 450 kr") so screen readers read one number.

**Small capitals in three places only:** the date and the place in the hero, and the jump links on info pages. All use `font-variant-caps: all-small-caps`. The hero lines use `{typography.date-line.letterSpacing}`, as on a printed invitation (memlog, *Front page approved*); the jump links use `{typography.jump-links.letterSpacing}` (Rikke's pick of three, 2026-11-15). The text stays in normal case in the HTML, so screen readers do not spell it out. No all-caps anywhere, and no small capitals for headings: small-caps «ALT OM HELGEN» was tried and Rikke wanted it «mer i stil med resten av nettsiden» (memlog, 2026-11-15); the section heading is italic instead.

## Layout & Spacing

### Grid and gutters

Phone first (NFR-6). One centred column, maximum `{spacing.content-max}`; a PC shows the same phone column on the green page **[ASSUMPTION — 480px max]**. Side gutter `{spacing.gutter}`. No horizontal scroll at 320px or at 200 % zoom (NFR-5). On a phone, 200 % zoom means a layout width of about **180 CSS px**. Below 260px layout width, the gutter and the hero's inline padding drop to `{spacing.gutter-narrow}`. Between 260px and 340px (the smallest phones, 320px wide) the gutter is `{spacing.gutter-small-phone}` and the hero's inline padding `{spacing.hero-padding-inline-small-phone}`, so the names and the place stay on one line and the whole hero fits the first screen (Rikke chose this, 2026-11-15, [.working/small-phone-1.html](.working/small-phone-1.html)).

### Front page

Front-page order. The whole front page is approved in [mockups/front-page-3.html](mockups/front-page-3.html) (memlog, 2026-11-15), built on the first screen approved in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html) (memlog, *Front page approved*, 2026-11-11). Both supersede [mockups/front-page-2.html](mockups/front-page-2.html) (PRD FR-7, FR-8):

1. **Nav bar**, sticky (see EXPERIENCE › Accessibility Floor for when it stops sticking): nav words left, the "Svar" button right, `{spacing.nav-height}` tall, flat green.
2. **Hero sheet**, `{spacing.page-padding-top}` below the nav bar so the seal is never hidden under it: seal over the top edge → the illustration (egne-bilder 04), whole → names → «inviterer dere til sitt bryllup» → gypsophila divider → date and place in small capitals → «for Sigmund og bestemor» → deadline line *«**Svar** innen 4. januar 2028»*, where "Svar" is a link. The short deadline here has no weekday or time; the full deadline sits above the RSVP button (FR-41 asks for it next to the button). No button and no child-free line in the hero.
3. Lead-in line on green.
4. **«Alt om helgen»**, directly on the green: lily garland (top) → italic heading with a cream hairline → three topic rows, each a lace-framed picture on the left and title, one italic line and «Les mer» on the right: *Programmet* (01-Venue), *Praktisk informasjon* (03-Venue, shifted down so the buildings show), *Vår historie* (the couple: [egne-bilder/12-Us1.jpg](../../ux/egne-bilder/12-Us1.jpg), cropped to [mockups/us1-utsnitt.jpg](mockups/us1-utsnitt.jpg); «Fra vi møttes til i dag.»; called *Om oss* until 2026-11-15) → lily garland (bottom). Gifts would be a fourth row, only if built.
5. **RSVP sheet** (jump target of both "Svar" links), 20px below the garland: heading "Svar på invitasjonen", a small gypsophila (180px), «Barnefritt bryllup», the full deadline «Svar innen tirsdag 4. januar 2028 kl. 23:59», the primary button.
6. Footer band, full-bleed `green-dark`.

**Answered state** (decided 2026-11-15, [mockups/answered-1.html](mockups/answered-1.html)): the page is the same, except that the hero's deadline line becomes «Svar sendt 12. oktober · **Se svaret**», and the RSVP sheet is replaced, in the same place, by the status block (the target of the nav "Svar" and of «Se svaret»).

### First-screen budget

**First-screen budget** (measured 2026-11-14 in headless Chrome at 360px wide, fonts and images loaded; the fold is 560px, what a browser or Messenger shows on a 360 × 640 phone):

| Element | Top–bottom (px) |
|---|---|
| Nav bar · nav "Svar" | 0–64 · 10–54 |
| Seal | 74–150 |
| Hero sheet | 110–**552** |
| Illustration · names (one line) | 124–267 · 271–327 |
| Divider · date · place | 357–407 · 407–437 · 437–463 |
| «for …» · deadline line | 469–499 · 503–**530** |

The whole hero sheet fits above the fold with 8px to spare, so these values are a budget, not a starting point: any added line or larger seal pushes the sheet's end off the first screen. At 320px (re-measured 2026-11-15 with «Vår historie» as the third nav word) the nav bar stays on one line (64px) only with tighter spacing below 340px layout width: nav words 8px apart, bar padding 8px 10px 8px 12px, the "Svar" button padding 0 12px and minimum width 56px (still ≥ 44px tall); with the normal spacing, «Vår historie» wraps and the bar grows to 104px. At 320px the small-phone gutter and hero padding keep the names and the place on one line, and the deadline line ends at 530px, above the 568px fold. With the normal 16px gutter and 20px padding it ended at 611px, below the fold (Open Question 2, resolved). «Praktisk informasjon» wraps to two lines beside its frame there, which is fine. Check widths for every build: 360 × 560, 320 × 568, 180 × 320.

*(Changed 2026-11-20 in Story 1.5: in the build, with the self-hosted EB Garamond, the place line «Hardingasete · Hardanger» in small capitals at 0.14em is about 307px wide and wraps to two lines in the 288px (360) and 276px (320) content box, which the mockup's no-break spaces hid. With the spacing above, the hero ended at 578px at both 360 × 560 and 320 × 568, below the fold, so the hero's vertical spacing was tightened by 30px to end at about 548px: `page-padding-top` 46 → 42px (the seal's top stays 6px below the nav bar), `hero-padding-top` 26 → 22px, `hero-padding-bottom` 22 → 16px, the illustration's gap below 4 → 0px, the invites line and the divider 2 → 0px, the household line 6 → 2px and the deadline line 4 → 0px. The names, the type sizes and the place line's letter spacing are unchanged. The table above is the 2026-11-14 measurement; MT-11 re-measures the build. Not yet seen by Rikke: it goes to her for approval, as every deviation from the approved design does.)*

Hero spacing: padding `{spacing.hero-padding-top}` / `{spacing.hero-padding-inline}` / `{spacing.hero-padding-bottom}`; seal centred with its top 36px above the sheet's top edge; illustration pulled up 12px (its top is empty sky) with no gap below; the invites line directly below the names; the divider directly below; 2px above the household line, none above the deadline line (tightened 2026-11-20, see the note above). Topic rows: 20px above, 6px below, 14px between frame and text; the «Les mer» target supplies the bottom space. Scale is 4-based: `{spacing.1}`–`{spacing.7}`. Text in the hero and RSVP sheet is centred, the details heading too; topic text is left-aligned beside its picture; form steps, check page, receipt and admin are left-aligned (as rendered in the key-screen mockups below).

Sections are separated by green showing between the sheets and by the lily garlands around «Alt om helgen». This answers inspiration 08's "not one long page on one identical background".

### Info pages

**Info pages** (G3). *Praktisk informasjon* is approved in [mockups/info-praktisk.html](mockups/info-praktisk.html) (memlog, 2026-11-15; rounds in `.working/info-praktisk-1.html` to `-6.html`). Order, under the nav bar with «Praktisk» as the current page:

1. «← Tilbake til invitasjonen», cream link on green, 10px below the nav bar.
2. Page title, `heading-page` *italic*, centred, with a cream hairline under it. No line of text under the title (Rikke removed it as «overflødig»).
3. **Jump links**, small capitals in three centred lines, 10px below the hairline (about 132px in all with 44px lines).
4. **One paper sheet per part**, 20px apart, left-aligned: italic heading with an ink hairline, then the text; a lace-framed photo (220px) heads the sheets that have one. *Praktisk informasjon*: **Vielsen** (18-Kirka) → **Hardingasete og hyttene** (03-Venue) → **Hvordan komme seg dit** (address, route, bus, parking, «Åpne veibeskrivelse i kart») → **Husregler** → **Antrekk** → **Ta med** → **Området rundt** (12-Area). *(Changed 2026-11-20 in Story 1.6: the map button waits for Story 7.4, when the real address exists, and for a decision on the map service (AD-15, privacy page); until then «Hvordan komme seg dit» has no button.)*
5. «Tilbake til invitasjonen» as an outlined button on green, centred, 14px below the last sheet.
6. Footer band.

At 360px the page is about 3 530px (six screens) with placeholder text; the jump links are why that is acceptable.

*Programmet* is approved in [mockups/info-program.html](mockups/info-program.html) (memlog, 2026-11-15; rounds in `.working/info-program-1.html` to `-6.html`). Same frame, with «Program» as the current nav word:

1. Back link, then the title «Programmet» with its hairline.
2. Jump links *Fredag · Lørdag · Søndag* on one line, then the voluntary line on green: «Alt i programmet er frivillig. Bli med på det dere har lyst til.» *(Changed 2026-11-20 in Story 1.7: the build reuses Praktisk's jump-link markup as one list, so the three links share one line at 360px; below 22.5em they stack one per line without dots, like every jump-link list (EXPERIENCE › Jump links, Narrow widths below). Under forced colours the timeline's line and dots are drawn in CanvasText, since the system would otherwise paint them in the Canvas colour and hide them. The timeline turns one-sided below 16.25em (260px at the default text size), in em like the jump links, so it follows a larger default text size; with a px breakpoint, «Middag» and «Badstue, stamp og mingling» broke mid-word at 260px with a 20px default text size. The frontmatter wording for `programme-timeline.line` and `programme-icon.position` was corrected to match the approved mockup: the line runs along the whole list, and the icon sits on the line side, aligned with the text.)*
3. **One paper sheet per day**: the day as the italic heading, an italic date line («27. mai · bryllupsdagen»), the **programme timeline**, then **«Godt å vite»**.
4. The timeline, like «Order of events» in [inspiration 09](../../ux/inspirasjon/09-Example.jpg): a thin centre line, a small dot per event, events alternating sides and overlapping in height, each with Rikke's icon (56px) above the time (18px) and a short italic name. Only time and name sit in the timeline; what costs money, what to bring and who covers what go in «Godt å vite» (Rikke: the first three layouts were not «like estetisk fine» as 09).
5. Bottom back button and footer.

At 360px the page is about 2 930px with placeholder times.

*Vår historie* (called *Om oss* until Rikke renamed it on 2026-11-15) is approved in [mockups/info-om-oss.html](mockups/info-om-oss.html) (memlog, 2026-11-15; rounds in `.working/info-om-oss-1.html` and `-2.html`). Same frame, with «Vår historie» as the page title and current nav word, and no jump links. **One story sheet** without its own heading (the page title already says «Vår historie»): the couple's view photo ([egne-bilder/13-Us2.jpg](../../ux/egne-bilder/13-Us2.jpg)) in the lace frame, then the couple's own text ([ux/innhold/Vår historie.docx](../../ux/innhold/V%C3%A5r%20historie.docx)) in chapters, each opened by an italic line with time and place (*Sensommeren 2021 · Trondheim* … *Våren 2027 · Oslo*), then the last sentence as an italic centred closing line and «Rikke & Valdemar» as a signature. One photo only: the beach photo stays on the invitation (Rikke). At 360px the page is about 3 780px; it is read by choice, so no jump links.

### Form, check page and receipt

**Form step, check page and receipt** (one paper sheet per screen on the green page, with the same soft edge and texture as the front page; no nav bar, footer band kept). Rendered at 360px, redrawn in the paper-sheet style on 2026-11-15 (same content as the 2026-11-11 renders; Rikke approved), in [mockups/key-form-steps.html](mockups/key-form-steps.html) (steps 1, 3 and 5, an error state and the draft offer), [mockups/key-check-page.html](mockups/key-check-page.html) and [mockups/key-receipt.html](mockups/key-receipt.html) (receipt and payment details; the answered front page is in [mockups/answered-1.html](mockups/answered-1.html)):

- **Form step:** step question (`h1`) → progress line → respondent line (**on every step**) → one fieldset per person or question → running total (paid steps only) → **"Fortsett" (primary) above "Tilbake" (secondary), both full width, 12px apart, 24px below the content** **[forslag — button order]**.
- **Check page:** warning notice «Obs: Svaret er ikke sendt ennå.» first, then the `h1` «Se over svaret før du sender» **[forslag]**, the check-answers list, the running total, "Send svaret" above "Tilbake".
- **Receipt:** success notice holding the `h1` «Svaret er sendt» and the sent-by line, Rikke's message, the summary, the total, "Betal nå" above "Betal senere", and the closing line directly below them.

### No valid link and privacy page

**No valid link (G1) and Personvern (G12)**, approved in [mockups/privacy-1.html](mockups/privacy-1.html) (Rikke, 2026-11-15). G1: the textured green page with one centred paper sheet 120px from the top: `heading-card` *italic* «Dette er en privat invitasjon», the small gypsophila (180px), one line of body text. No nav bar, footer band or seal. Under the sheet, a plain cream «Personvern» link (FR-66). *(Changed 2026-11-21 in Story 1.8: the error pages reuse G1's sheet, heading and gypsophila, and never show names, date, place, seal or nav bar. 404 «Vi finner ikke denne siden» («Lenken kan ha en skrivefeil. Invitasjonen ligger der den var.»), 500 «Noe gikk galt hos oss» («Prøv igjen om litt.»), CSRF failure «Skjemaet ble ikke sendt» («Det skjer når siden har stått åpen lenge, eller når nettleseren ikke tar imot informasjonskapsler. Gå tilbake og prøv igjen.») and 400 «Siden kunne ikke vises» («Prøv å åpne lenken på nytt.»). When the address starts with a valid link, the 404, 500 and CSRF pages add the outlined back button on green, «Tilbake til invitasjonen», under the sheet (as at the bottom of an info page), and the footer band with the couple's phones; the 500 and CSRF pages then end with «Går det fortsatt ikke, send oss en melding.» Without a valid link, and always on the 400 page, they end with «Går det fortsatt ikke, ta kontakt med brudeparet direkte.» and show neither button nor footer; a 404 without a valid link is G1 itself. The wording has no mockup: it is Claude's proposal, awaiting Rikke's approval **[forslag]**.)* G12: the info-page frame (Layout › info pages) with the title «Personvern», jump links and one sheet per part; the last sheet lists each household member with a secondary button «Trekk samtykket for <name>». The withdrawal dialog is a paper sheet over the 60 % scrim with an *italic* heading, «Avbryt» (secondary, focused) and the primary «Slett allergiopplysningene». The button is primary, not Destructive, on purpose: it is the guest's only confirmation, as in Rikke's approved render. Destructive buttons are only for the couple's tier-3 actions.

### Narrow widths

**Narrow widths (200 % zoom, 180 CSS px).** Every image (illustration, garlands, gypsophila, lace frames) has `max-width: 100%` and keeps its aspect ratio. Below about 300px layout width a topic row stacks: the framed picture (up to 136px) above the text. Below about 260px the programme timeline becomes one-sided: the line moves to the left edge and every event sits to its right, left-aligned, without the overlap. Measure these breakpoints in the build (review A2-01, A2-02). *(Changed 2026-11-20 in Story 1.6: below 22.5em (360px at the default text size) each jump link takes its own line and the middle dots, which are `aria-hidden` spans since some screen readers read CSS `content` aloud, are hidden, so a dot never starts a line. Measured in Edge with the self-hosted EB Garamond, the widest line «Komme dit · Husregler · Antrekk» was about 328px with the mockup's 4px inline margin on the nav and 7px dot padding, more than the 320px it had at 360px, so «· Antrekk» wrapped onto a fourth line starting with a dot. The build drops the nav's inline margin and pads the dots 5px, so the line is about 320px of the 328px content box at 360px and the three approved lines hold; it needs about 352px with the 16px gutters, rounded up to 22.5em for a margin, in em so it follows a larger text size. The info and story sheets take `{spacing.gutter-narrow}` as their inline padding below 260px. Jump targets are cleared by the `html` scroll padding alone, with no `scroll-margin`.)*

### Admin screens

**Admin:** same tokens, denser. The admin page is the **flat** `page-green` (no texture), because admin text on the green is 18px and cream text under 19px may only stand on flat green (review A2-04). Panels use `{spacing.admin-panel-padding}` and `{spacing.admin-gap}`; lists and tables rather than cards; quick tasks (find guest, copy link, see if answered) fit one phone screen (FR-48). When density and targets collide, **44px targets win**; lists scroll.

**Admin home (A2)**, as approved in [mockups/admin-rework-1.html](mockups/admin-rework-1.html) (memlog, *Admin rework approved*; PRD FR-54, FR-56, FR-57). The earlier grouping in `.working/key-admin-overview.html` (summary first, «Dager, senger og mat» in one panel, attention list last) is **superseded** and stays in `.working/` only; the helper view is rendered in [mockups/helper-view-1.html](mockups/helper-view-1.html). Order on the page, under the Admin nav:

1. **Attention panel** «Trenger oppfølging (n)» — first, without scrolling. Shows as many items as fit while the answer-progress line below still sits on the first screen (two items at 360 × 560 in the render), then «Vis alle n». Empty: the panel heading becomes the check icon + «Ingenting trenger oppfølging nå», with «Vis håndterte» below.
2. **Svar panel** — the answer-progress line «Svart: X av Y husstander», a progress bar under it, the Kommer / Kommer ikke / Ikke svart ennå rows, and «Se hva alle har svart» (to A4, FR-57).
3. **Summary panels**, one small panel per group, in this order: *Når kommer de?* · *Overnatting* · *Mat* · *Allergier (med samtykke)* · *Fjelltur fredag* · *Betaling (husstander som kommer)*. Contents: EXPERIENCE › Component Patterns › Admin summary panel.

**Gjester (A4) and the household page (A6)**, approved in [mockups/admin-guests-1.html](mockups/admin-guests-1.html) (Rikke, 2026-11-15; the full overview and the guest list are one page). *Gjester*: the page title in `admin-title` on the green, the count «30 husstander · 70 gjester», a panel with the search field and «Legg til husstand», then the household list (Overview table). *Household page*: a back link «Alle gjester», the household name as title, then four admin panels: *Svar* · *Betaling* · *Lenker* · *Husstanden*. «Fjern husstanden» is a Destructive button 28px below the last safe button. The tier-3 dialog lies over a 60 % scrim: heading in 600 weight, the consequence sentence, the typed-confirmation field, «Avbryt» first and «Fjern husstanden» apart below.

**Betalinger (A9)**, approved in [mockups/admin-payments-1.html](mockups/admin-payments-1.html) (Rikke, 2026-11-15). Same frame as *Gjester*. *List*: title and «25 husstander som kommer», a «Til sammen» panel of summary rows (label left, amount right), then the household list with status tags stacked under the name. *Household payment page*: back link «Alle betalinger», then panels *Status* · *Registrert* (one row per entry: date, «Mottatt 600 kr», secondary «Angre») · *Registrer betaling* (two radio choices, the amount field with the hint «Dagens dato settes selv.», and the one primary button «Registrer») · *Betalingsmelding*. The tier-2 dialog has «Avbryt» (secondary, focused) above the primary «Registrer 300 kr». After saving, an admin panel with the check icon, «Registrert: mottatt 300 kr.» and «Angre» stands first under the title.

## Elevation & Depth

**Paper sheets on an envelope.** Every guest content panel is a cream sheet lying on the green page, as the main sheet in [inspiration 01](../../ux/inspirasjon/01-Vibe.jpg): a soft, slightly wavy, hand-made edge with fine fibre, in **the sheet's own colour** (no lighter rim, no inner ridge, nothing chalk-white), and a soft shadow underneath. Chosen over three rounds of edge renders (memlog, *Sheet edge* and *Sheet edge refined*; edge B3). Still **no folds, no backing sheet, no layered or offset sheets** (memlog override dropping the layered-sheet card style). Reference: [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html), filter `edge-b3`. **Admin panels keep straight edges** with the same cream paper texture and no edge filter: admin is a working tool, denser, and the attention panel's green top rule needs a straight edge (Rikke chose A in [.working/admin-edge-1.html](.working/admin-edge-1.html), 2026-11-15).

How the sheet is built, so the edge never touches the text:

- Colour, texture, edge and shadow sit on a layer **behind** the content (`::before`); only that layer is filtered. Text, links and focus rings stay sharp, and their contrast is unchanged.
- The edge is an SVG filter (displacement for the wave, fine noise for the fibre, blur 3.2px offset 2.5px at 42 % `#141A0C` for the shadow). If it is slow on old phones, the build may swap it for a pre-rendered edge image with the same look (memlog, *Technical defaults while folding in*).
- Where filters are unsupported, the sheet falls back to flat `panel-cream` with `{rounded.sheet}` corners. Under forced colours (Windows high-contrast mode) the cream becomes `Canvas` like the page, so sheets, admin panels and dialogs get a 1px `CanvasText` border there. The edge and shadow are decoration; the flat sheet is a complete design.

Depth appears in exactly five places:

- **The sheets**, as above.
- **The lace frames**: `drop-shadow(0 1px 1.5px rgba(10,14,6,.35))`, so the frame lifts slightly off the green.
- **The seal**: Rikke's image already looks like pressed, glossy wax; the page adds `drop-shadow(0 2px 2px rgba(12,16,8,.45))` so it lies *on* the sheet's top edge.
- **The sticky nav bar**: a 1px hairline of `cream-on-green` at 22 % along its bottom edge, so content visibly slides under it.
- **Dialogs**: a cream sheet over `{colors.scrim}` at 60 %; on guest pages the sheet has the paper edge, in admin the straight edge.

**Paper texture.** Page and sheets carry a fine paper grain: tiling SVG noise layers (fine grain and soft fibre, inline data-URIs, no network) blended with `overlay` around mid-grey, so the **average colour is unchanged**. The green texture is the calmer one approved in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html) (`--grain-green`). Contrast is checked against the worst case on each surface (memlog, *Technical default, measured*): the lightest 3 × 3 px average on the green, and the darkest single pixel on the sheet:

- **Green:** the grain is finer than a letter stroke, so cream text is checked against the texture averaged over 3 × 3 px: worst **4.50:1** (4.61:1 at 4 × 4 px), 0 % under 4.5:1 (memlog, *Contrast method refined*). So cream text of **19px or more** may sit on the textured green: the lead-in, the whole «Alt om helgen» section, and the title, back link and jump links of the info pages. The 3 × 3 px box (radius 1px) stays within the letter stroke down to 19px text, whose strokes are about 1.9px wide, including the 19px «Les mer» and the small-capital jump links (memlog, 2026-11-15). The single lightest pixel (`#6D8358`, 3.61:1) is no longer the test. The nav words (18px) stay on the **flat** nav bar (4.95:1). Re-measure the italic topic text in the build, since italic strokes are thinner.
- **Sheet:** the darkest pixel is `#DBCFB4`. Worst cases: `ink` 7.67:1, `ink-muted` 4.51:1, `warning` 4.65:1, `success` 5.05:1, `error` 5.44:1, `green-dark` 6.62:1. All pass.
- Re-measure on a screenshot of the built page if the texture changes. The texture is decoration: if it fails to load, the flat token colours are the design.

## Shapes

Guest sheets have a soft, hand-made edge (Elevation & Depth) over `{rounded.sheet}` (5px) corners, which is also their flat fallback. Inside the sheets everything is crisp: `{rounded.sm}` (3px) for fields, notices and tags; `{rounded.md}` (4px) for buttons and checkboxes; `{rounded.full}` only for radio buttons. No pills, no circles for surfaces, no arched or scalloped tops, no torn or ripped look (the edge is soft, not jagged).

Four organic shapes come from Rikke's own images, not from code:

- The **seal**: an uneven, hand-pressed wax disc with *R & V*, glossy dark green ([06-Stamp.jpg](../../ux/egne-bilder/06-Stamp.jpg), cut out to [mockups/segl.png](mockups/segl.png)).
- The **gypsophila divider**: two crossing sprigs with green stems and white flowers ([07-Flowers.jpg](../../ux/egne-bilder/07-Flowers.jpg), cut out to [mockups/brudeslor.png](mockups/brudeslor.png)).

- The **lily garlands**: white lilies, gypsophila and buds on green stems, one arching up for above the heading and one bowing down for below ([09-FlowersTop.jpg](../../ux/egne-bilder/09-FlowersTop.jpg), [10-FlowersBottom.jpg](../../ux/egne-bilder/10-FlowersBottom.jpg), cut out to [mockups/lilje-topp.png](mockups/lilje-topp.png) and [mockups/lilje-bunn.png](mockups/lilje-bunn.png)).
- The **lace frame**: a thin square frame with small fan scallops and eyelets ([11-Frame.jpg](../../ux/egne-bilder/11-Frame.jpg), cut out and recoloured to `panel-cream` in [mockups/blonde.png](mockups/blonde.png)). Pictures inside it are square-cut, never oval and never faded into the green (rejected in rounds 1–2).

The seal and gypsophila are cut out with [.working/cutout-segl-brudeslor.py](.working/cutout-segl-brudeslor.py), the lilies and the frame with [.working/cutout-liljer-blonde.py](.working/cutout-liljer-blonde.py), and the twelve programme icons with [.working/cutout-ikoner.py](.working/cutout-ikoner.py) (one shared scale so every line weighs the same) (all from black backgrounds; usage in each file). If Rikke replaces an image, run the script again rather than editing the PNGs. Code-drawn sprigs, seals and lace were tried and rejected ("så jalla ut", memlog 101–105; code lace L1/L2, memlog 2026-11-15).

## Components

Frontmatter key in brackets where one exists.

| Component | Visual spec |
|---|---|
| **Page** [`page`] | `{colors.page-green}` with the calm paper texture. Never plain white anywhere. |
| **Paper sheet** [`paper-sheet`] | The surface of every guest content panel: cream, textured, soft hand-made edge in its own colour, soft shadow, all on a layer behind the content. Flat `{rounded.sheet}` fallback (Elevation & Depth). |
| **Nav bar** [`nav-bar`, `nav-words`] | Full-width strip, **flat** `{colors.page-green}` (no texture), 64px, a faint cream hairline below. Nav words left (Program · Praktisk · Vår historie), `{typography.nav-words}` in `{colors.cream-on-green}`, **not underlined**, 12px apart, each ≥ 44 × 44px; no separator characters; may wrap to two lines; no hamburger. Current page: 2px underline, offset 4px (approved in the info-page renders). Sticky only on a screen at least 400px tall and 20em wide; the hairline is a box shadow, so it adds no height. *(Changed 2026-11-20 in Story 1.5: the width condition was added, in em so it follows the phone's text size, because a bar whose words wrap to several lines would cover what a link jumps to; jump targets are cleared by `scroll-padding-top` on `html` alone, since a `scroll-margin-top` on the RSVP and info sheets as well would double the gap.)* |
| **Nav "Svar" button** [`nav-svar`] | Right end of the nav bar: `{colors.green-dark}` fill, cream text, **1px `{colors.cream-on-green}` border** (dark green on page-green is only 1.79:1), ≥ 64 × 44px (below 340px layout width: 56px wide, padding 0 12px). The one primary-styled control allowed on green. |
| **Hero sheet** [`hero-panel`] | Centred, in this order: seal over the top edge, illustration, names, invites line, gypsophila divider, date and place in small capitals, «for <household>», short deadline line with the "Svar" link. Rendered in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html). |
| **Wax seal** [`wax-seal`] | Rikke's seal image, 74px wide, centred with its top 36px above the hero sheet's top edge, drop shadow. Decorative (`alt=""`). The favicon is made from the same image (at 32px and 180px). |
| **Hero illustration** [`hero-illustration`] | [Rikke's illustration 04](../../ux/egne-bilder/04-Illustration.jpg) (cool sage watercolour of the bell house and main house among pines with string lights), **shown whole** at 262px wide, pulled up 12px under the seal, `mix-blend-mode: darken` so its paper melts into the cream (`normal` under forced colours). Final file has no signature or text and ships with the app. Alternatives I5–I8: [mockups/illustration-3.html](mockups/illustration-3.html) (I7 chosen). The 150px cropped band in front-page-2.html is superseded (Rikke: "kuttet for mye"). |
| **Flower divider** [`flower-divider`] | Rikke's gypsophila image, 224px wide in the hero (between invites line and date), 180px above the child-free line in the RSVP sheet. Decorative (`alt=""`), no blend mode. |
| **Lily garland** [`lily-garland`] | Rikke's lilies, 296px wide: the top image above the details heading, the bottom image below the last topic row; both bow towards the text, so neither is rotated. Decorative (`alt=""`). With the gypsophila, the only flowers on the page. |
| **Lead-in** [`lead-in`] | One italic line on the textured green, 24px, e.g. «Vi gleder oss til å feire med dere». |
| **Details section** [`details-section`] | «Alt om helgen» directly on the textured green, no sheet: top garland, `heading-section` *italic* centred with a 1px cream hairline under it, the topic rows, bottom garland. Rendered in [mockups/front-page-3.html](mockups/front-page-3.html); the rounds that led here are in `.working/finer-details-1.html` to `-10.html`. |
| **Topic row** [`topic-row`] | Lace-framed picture left (136px), text right: `topic-title`, one line of `body` *italic*, then «Les mer» as an outlined button on green. Only «Les mer»; directions and other links live inside the topic's page. Pictures can carry information: `alt` describes them when they do, and is empty when the title says it all **[ASSUMPTION]**. |
| **Lace frame** [`lace-frame`] | Rikke's lace image in `panel-cream` over a square-cut photo that fills its window, soft drop shadow; 136px in topic rows, 220px on info sheets. Decorative (`alt=""` on the frame). Never oval, never a soft fade, never a stamp or double-line frame (rejected as «for harde»). |
| **Info page title** [`info-page-title`] | `heading-page` *italic*, centred, cream on green, 1px cream hairline under it; the page's `h1`. |
| **Back link** [`back-link`] | «← Tilbake til invitasjonen» at the top of every info page: cream, 20px, underlined, ≥ 44px. At the bottom the same words are an outlined button on green (FR-11). |
| **Jump links** [`jump-links`] | A `nav` labelled «Hopp til» under the info page title: short words in small capitals, 19px, centred in balanced lines (two or three words each), a decorative middle dot between words on the same line, no underline (they read like the nav words), each ≥ 44px tall (`{spacing.target-min}`; raised from 40px after review A2-05). Each balanced line is its own list. Rendered in [mockups/info-praktisk.html](mockups/info-praktisk.html). A large list with underlined words (round 2) was «rotete og stort»; closed sheets that open (round 3) were «ikke så fint og koselig». |
| **Info sheet** [`info-sheet`] | One paper sheet per part of an info page: `heading-card` *italic* with a 1px ink hairline under it, then `body` text; facts lead with a 600-weight label («**Adresse:** …»); lists keep their bullets; links are underlined; one outlined dark-green button where a part needs an action («Åpne veibeskrivelse i kart»). An optional lace-framed photo, 220px, centred at the top of the body. Sheets are 20px apart. |
| **Programme timeline** [`programme-timeline`] | One ordered list per day: a thin centre line, a 6px ink dot per event, events alternating left (right-aligned) and right (left-aligned), each overlapping the one before by 36px so the timeline stays compact. Each event: icon, time (`small`, lining figures), short name (`body` *italic*). Rendered in [mockups/info-program.html](mockups/info-program.html). |
| **Programme icon** [`programme-icon`] | Rikke's line drawings ([egne-bilder/14-Icons.jpg](../../ux/egne-bilder/14-Icons.jpg)), cut out to one PNG each and recoloured to `ink`, 56px, above the time. Decorative (`alt=""`): time and name carry the meaning. The same icon may repeat (breakfast on Saturday and Sunday). |
| **«Godt å vite»** [`good-to-know`] | At the foot of each day sheet, after a faint hairline: italic «Godt å vite», then a bulleted list of what costs money («**Frokosten betales selv:** [x] kr.»), what to bring and who covers what. |
| **Story sheet** [`story-sheet`] | *Vår historie*: one paper sheet without its own heading (the page title says it), a lace-framed photo (220px), chapters each opened by an italic time · place line, an italic centred closing sentence, and the names as a signature in Imperial Script 40px. Rendered in [mockups/info-om-oss.html](mockups/info-om-oss.html). |
| **Voluntary line** [`voluntary-line`] | One italic cream line under the jump links on Programmet: «Alt i programmet er frivillig. Bli med på det dere har lyst til.» |
| **Outlined button on green** [`button-on-green`] | Transparent, 1.5px `cream-on-green` border and text, 4px radius, ≥ 44px tall, `button-small` 19px. Hover/pressed: border 3px; focus ring `focus-on-green`. On a cream sheet the same shape is drawn in `ink` («Åpne veibeskrivelse i kart»). |
| **RSVP sheet** [`rsvp-panel`] | Paper sheet after «Alt om helgen»: `heading-card` "Svar på invitasjonen", small gypsophila divider, «Barnefritt bryllup» (Rikke removed the rest of the proposed line), the full deadline «Svar innen tirsdag 4. januar 2028 kl. 23:59», primary button. When an unsent draft exists, a warning notice sits above the button. |
| **Primary button** [`button-primary`] | Full panel width, 52px, cream text on dark green, 2px transparent border (visible outline in forced colours). Only on paper sheets and admin panels — the nav "Svar" is the one exception. **One distinct primary action per screen; repeats of the same action are allowed** (nav "Svar" and RSVP button). Busy: keeps its colours, label becomes "Sender …". |
| **Secondary button** [`button-secondary`] | Outlined dark green on cream; border 3px on hover/pressed. For "Tilbake", "Betal senere", "Avbryt", "Nei, begynn på nytt". In form steps, check page and receipt it sits **below** the primary button, same full width **[forslag]**. |
| **Destructive button** [`button-destructive`] | Muted rust outline on cream, placed apart (tier 3 only); border 3px on hover/pressed. Filled rust is not used **[ASSUMPTION — "muted rust" read as outline]**. |
| **Focus ring** [`focus-ring`] | 3px outline at 3px offset on `:focus-visible` and on `:active` (tap feedback). Colour by the surface the ring is **painted on**: `focus-on-panel` on cream, `focus-on-green` on green or the footer. Never `outline: none`. |
| **Text link / "Les mer"** [`link-more`] | Inherits text colour, always underlined (1px, 4px offset; 2px on hover/pressed), target ≥ 44px. Never colour alone. |
| **Footer band** [`footer-band`] | Full-bleed `{colors.green-dark}`, cream text, 20px: "Spørsmål? Send oss en melding:", then **each phone number on its own ≥ 44px row** ("Rikke 900 00 000", "Valdemar 900 00 001"), then "Personvern" as an underlined cream link. «Spør oss» was removed (Rikke, 2026-11-15; PRD FR-43 to FR-45). |
| **Text field** [`field`] | Field surface, 2px border, label above in `{typography.label}`, hint below in `{typography.body}` *italic* `{colors.ink}`. Error: 3px `{colors.error}` border and the error line (icon + text) between label and field. Variants: multi-line (≥ 4 lines, e.g. notes), search (A6), typed confirmation (tier 3). |
| **Choice control** [`choice-control`] | 26px box, 2px ink border; checkbox `{rounded.md}`, radio `{rounded.full}`; selected mark in `{colors.green-dark}` drawn so it survives forced colours (native input with `accent-color`, or a `currentColor` mark — never a background fill alone). Whole row ≥ 44px is the target. Group error (a fieldset of choices): **no border on the group**; one error line under the legend, before the first choice: 22px triangle icon + «Feil: …» in `{colors.error}` (e.g. «Feil: Velg «Kommer» eller «Kommer ikke» for bestemor.» **[forslag]**), as in [mockups/key-form-steps.html](mockups/key-form-steps.html). |
| **Notice** [`notice`] | 4px left rule, 22px icon and text in the state colour on cream. Icon shapes differ: success = check, warning = circle with "!", error = triangle with "!", info (`ink`) = "i". Error and warning also start with a word ("Feil:", "Obs:" — proposal). Variants: success, warning, error, info; last-updated header (info). |
| **Error summary** | Error notice at the top of the step panel with a heading and linked list of errors. |
| **Status block** | Paper sheet shown once answered, in the RSVP sheet's place and centred like it: `heading-card` «Svaret er sendt», the small gypsophila, «Barnefritt bryllup» (kept, Rikke 2026-11-15), then «Sendt av Sigmund tirsdag 12. oktober 2027 kl. 14:31.», «Totalt for husstanden: 3 900 kr», «Meldt betalt: 3 900 kr, 12. oktober.», «Dere kan endre svaret fram til tirsdag 4. januar 2028 kl. 23:59.», and the primary button "Se eller endre svar" **[forslag — wording except the button]**. Rendered in [mockups/answered-1.html](mockups/answered-1.html) (approved placement, 2026-11-15; it replaces the second phone of the first receipt render, removed when the receipt was redrawn on 2026-11-15). |
| **Draft offer** | Paper sheet at the top of the form: heading «Vil du fortsette der du slapp?», one line saying when the answer was started, primary "Ja, fortsett", secondary "Nei, begynn på nytt". Rendered in [mockups/key-form-steps.html](mockups/key-form-steps.html). |
| **Progress line** | "Steg 3 av 6: Overnatting" in `{typography.body}`, directly under the step question; no graphic stepper **[ASSUMPTION]**. |
| **Respondent line** | "Jeg er **Sigmund** · Bytt" ("Bytt" is a button styled as an underlined link, ≥ 44px), directly under the progress line **on every form step**, so the guest always sees who is answering; switching opens a radio list of household members in the panel **[ASSUMPTION]**. |
| **Running total** | Right-aligned "Totalt for husstanden: 1 450 kr", lining figures, `divider` hairline above, at the foot of each paid step. |
| **Read-more disclosure** | Underlined "Les mer om …" with a small chevron; expands in place with a left rule in `{colors.divider}`. |
| **Consent block** | Section at the end of the allergies step, after a `divider`: purpose and recipients text (`body`), how to withdraw, then the Ja/Nei choice under its legend, then — when answering for others — the "Jeg bekrefter …" checkbox. No special colour; nothing pre-selected. |
| **Check-answers list** | Under the `h1` «Se over svaret før du sender» **[forslag]**: one block per part (Hvem kommer · Dager · Overnatting · Måltider · Allergier og matbehov · Fjelltur fredag) with the part name and its "Endre" link on one line, then one line per person ("Sigmund: kommer"); `divider` between parts; "Ikke oppgitt" in `ink-muted`. Rendered in [mockups/key-check-page.html](mockups/key-check-page.html). |
| **Receipt panel** | Paper sheet. Success notice at top carrying the `h1` «Svaret er sendt» and «Sendt av Sigmund tirsdag 12. oktober 2027 kl. 14:31.» **[forslag]**; Rikke's message in `{typography.body}`; summary «Dette har dere svart» **[forslag]** and the running total; then "Betal nå" / "Betal senere" with the closing line «Du kan nå trygt lukke invitasjonen.» directly below them. Rendered in [mockups/key-receipt.html](mockups/key-receipt.html). |
| **Payment details** | Paper sheet «Slik betaler du» **[forslag]** listing amount, Vipps number, account number and payment message as selectable `body` text, each with a secondary "Kopier" button and «Kopiert» beside the last-used one; "Jeg har betalt" below **[ASSUMPTION]**. Rendered in [mockups/key-receipt.html](mockups/key-receipt.html). |
| **Envelope reveal** [If time] | `{colors.page-green}` envelope closed with Rikke's seal image, opening into a **plain** paper sheet that becomes the hero sheet (same edge, same seal position). No heart shape, no lace, no folds. "Hopp over" ≥ 44 × 44 on cream or `green-dark`. |
| **Admin nav** | Reuses Nav words on the green page (Oversikt · Gjester · Betalinger · Innstillinger · Logg ut), **not sticky**, no "Svar" button; approved in the admin renders. |
| **Admin panel** [`admin-panel`] | Every admin content block: `panel-cream` with the sheet paper texture, **straight edges** (no edge filter), `{rounded.sm}`, `admin-panel-padding`, `admin-gap` between panels, `admin-heading` for its `h2`. Admin page titles («Gjester», a household name) are `admin-title` (28px) in cream on the flat green. Saved confirmations («Registrert: mottatt 300 kr.» + «Angre», «Lagret.») are an admin panel with the check icon in `success`, first under the title. |
| **Helper read-only line** | Under the admin nav, for helpers only: «Du kan se alt, men ikke endre noe.» in `cream-on-green`, 20px, with a 4px cream rule on the left; not a panel and no icon. Rendered in [mockups/helper-view-1.html](mockups/helper-view-1.html). |
| **Attention panel** [`attention-panel`] | A2's first panel: cream, `admin-panel-padding`, a 5px `{colors.green-dark}` rule along the top edge so it reads as "start here" (decoration; the heading carries the meaning) **[forslag]**. `admin-heading` «Trenger oppfølging (7)», then attention items with `divider` between, then «Vis alle 7» as an underlined link (≥ 44px) after a `divider`. Rendered in [mockups/admin-rework-1.html](mockups/admin-rework-1.html). |
| **Attention empty state** | The attention panel without the top rule: its heading becomes a 26px check icon + «Ingenting trenger oppfølging nå» in `{colors.success}` (icon and words, never colour alone), then «Vis håndterte». Rendered in [mockups/admin-rework-1.html](mockups/admin-rework-1.html) (second phone). |
| **Attention item** | Admin row: reason in 600 weight («Betalingen stemmer ikke», «Har ikke svart ennå»), household and detail in `admin-body`, one secondary action ("Merk som håndtert"); mismatches also carry the "Stemmer ikke" status tag (error icon + word). |
| **Answer progress** [`answer-progress`] | Top of A2's Svar panel: «Svart: 28 av 30 husstander» in `label` (20px, 600, lining figures), then a 12px bar (track `cream-on-green`, fill `green-dark`, 1px `ink-muted` border). **The text carries the number; the bar is decoration** (`aria-hidden`, fill drawn as `CanvasText` under forced colours). |
| **Admin summary panel** | One small cream panel per group (`admin-heading` + rows). Each row: `{typography.admin-body}` label left, count right as a link (0 is plain text); ≥ 44px tall; `divider` between rows. Lead rows in 600 weight; breakdown rows indented 18px with a dotted `divider`; a secondary row («Senger totalt») in `ink-muted`; an optional italic `ink-muted` note under the rows («Én person kan ha flere allergier.»). Contents per panel: EXPERIENCE › Component Patterns. |
| **Admin summary row** | Inside a summary panel: label and count; the Svar rows show two counts («58 personer · 25 husstander»), the hike row two linked figures («5 kommer, 2 kanskje»), "kanskje" never added to "kommer". |
| **Overview table** | A4: one admin panel listing the households, `divider` between rows. Each row: the household name as a 600-weight link (≥ 44px), the status tag on its own line, then one `admin-body` line (who comes, total, payment). On PC the rows may become a table (`admin-body`, 600-weight header row). Unanswered households sort first and carry the "Ikke svart" tag. Rendered in [mockups/admin-guests-1.html](mockups/admin-guests-1.html). |
| **Undo (in place)** | After a tier-1 action the row is replaced in place by "Merket som håndtert." and an "Angre" link-button. No fixed bar, no toast (kept after the key-screen render). |
| **Status tag** [`status-tag`] | Outlined label in the state colour, icon as in Notice. Mapping **[forslag]**: "Betalt" → success · "Ikke betalt", "Delbetalt, 300 kr mangler", "Skal ha tilbake 200 kr", "Ikke svart" → warning · "Stemmer ikke" → error · "Ingenting å betale", "Endret" → ink (info). |
| **Dialog** [`dialog`] | Consequence sentence, then actions; on narrow screens buttons stack full-width, safe action first. |

## Do's and Don'ts

| Do | Don't |
|---|---|
| Cream paper sheets on the green page: textured, soft hand-made edge in the sheet's own colour, soft shadow | Folds, backing or offset sheets, a light or chalk-white rim, jagged torn edges |
| Primary buttons on paper sheets and admin panels; the nav "Svar" (with its cream border) is the only exception | A dark green button on green without the cream border |
| The nav bar is the only thing that sticks | Other sticky or fixed bars, on guest or admin pages |
| Imperial Script for the names only: 48px in the hero (stacking when needed), 40px as the signature on *Vår historie* | Script for headings, labels, buttons or admin; shrinking the names to fit |
| Small capitals for the date and place in the hero and the jump links on info pages | All-caps; small-caps headings |
| EB Garamond 20px for guest body text, hints in `ink` | Guest text under 18px; hints in `ink-muted` |
| Warm olive greens (hue ~85–100°) | Bluish sage greens (round 1), neon or saturated greens |
| Cream `#F5EEDF` text of 19px or more on the textured green; the 18px nav words only on the flat nav bar | Cream text under 19px on the textured green |
| State colour plus icon shape plus words | Red/green/brown alone to mean anything (WCAG 1.4.1) |
| One illustration (egne-bilder 04, whole) in the hero, one seal, the gypsophila in two places, the lilies around «Alt om helgen», lace frames around its pictures and the info-page photos, line icons in the programme timeline — all from Rikke's images | Icons outside the programme timeline, sprigs, leaves, ornaments sprinkled through the page; flowers, seals, lace or icons drawn in code (Claude's SVG trial icons were set aside: Rikke made her own, memlog 2026-11-15) |
| Square pictures in the cream lace frame, beside their text on the front page or at the top of their info sheet | Oval pictures, soft fades into the green, stamp or double-line frames, pictures on a sheet of their own |
| Venue photos as information: in the topic frames and on info pages, shown as taken, without a colour filter (Rikke, 2026-11-15, [.working/photo-style-1.html](.working/photo-style-1.html)) | Venue photos as style or background texture |
| Same tokens in admin, denser, no decoration, 44px targets | Seal, illustration or script on admin working screens |
| A plain paper sheet in the envelope reveal; lace only as a frame around pictures | A heart-shaped or lace letter |
| Restraint | Gold, metallic, diamonds, glitter, bling, neon, blinking, draping, clutter, luxury-brand feel, Italian or olive-plant motifs |
