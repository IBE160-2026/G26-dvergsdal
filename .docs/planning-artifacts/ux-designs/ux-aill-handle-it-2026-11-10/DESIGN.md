---
name: "AI'll handle it"
description: "Rikke & Valdemar's wedding invitation as a website: cream paper sheets with soft hand-made edges on a textured olive-green page, a dark green wax seal, a gypsophila divider, a script name line and printed-invitation body text. Light only."
status: draft
created: 2026-11-10
updated: 2026-11-14
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
  scrim: '#344628'
typography:
  display-names:
    fontFamily: 'Imperial Script'
    fontSize: 48px
    fontWeight: '400'
    lineHeight: '1.15'
  heading-page:
    fontFamily: 'EB Garamond'
    fontSize: 32px
    fontWeight: '400'
    lineHeight: '1.2'
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
  panel-gap: 16px
  panel-padding: 20px
  page-padding-top: 46px
  hero-padding-top: 26px
  hero-padding-bottom: 22px
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
    borderBottom: '1px rgba(245,238,223,.22)'
    position: 'sticky top 0, only when viewport height >= 400px'
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
    scrollMarginTop: 'nav-height + scroll-gap'
  wax-seal:
    image: 'mockups/segl-19.png (Rikke, image tool; cut out to transparent PNG)'
    width: 74px
    position: 'centred over the hero sheet top edge, top -36px'
    shadow: 'drop-shadow 0 2px 2px rgba(12,16,8,.45)'
  hero-illustration:
    image: 'inspiration 17 (watercolour of the farmyard)'
    width: 262px
    height: auto
    marginTop: '-12px (its top is empty sky)'
    blend: 'mix-blend-mode: darken; normal under forced-colors'
  flower-divider:
    image: 'mockups/brudeslor-20.png (gypsophila, Rikke, image tool; cut out to transparent PNG)'
    width: '224px in the hero; 180px in the RSVP panel'
    blend: 'none (white petals must stay white)'
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

> Visual identity for the guest invitation and the couple's admin area. Behaviour, states and flows live in [EXPERIENCE.md](EXPERIENCE.md). Decisions are logged in [.memlog.md](.memlog.md); requirements in the [PRD](../../prds/prd-aill-handle-it-2026-11-07/prd.md) and its [addendum](../../prds/prd-aill-handle-it-2026-11-07/addendum.md). Renders are linked in the sections they illustrate. **The spines win on any conflict with a render.**

## Brand & Style

The site **is** the invitation. A guest opening their link should think what Rikke and Valdemar said in the brain dump: *"wow, what a lovely invitation, and so easy to get an overview"* and *"wow, so cosy! I want to be part of this."* The posture is a printed wedding card from a timber farmhouse in Hardanger: classic, clean, slightly old-fashioned, warm. Nature and elegance with historic wooden-building character, never luxury.

The visual language follows from that:

- **An envelope-coloured page with paper sheets on it.** Olive-green textured page, and cream sheets with soft, hand-made edges and a soft shadow carrying the content (direction B *Konvolutten*, about half green, half cream). The sheets look like the main sheet in [inspiration 01](../../ux/inspirasjon/01-Vibe.jpg), in the sheet's own colour (memlog, *Sheet edge refined*).
- **Solemn, not cabin-cosy.** Rikke found the earlier version gave a "hytte" feeling and wanted it more festive (memlog 100). The top sheet is therefore laid out like a formal printed invitation: seal over the top edge, the farmyard drawing, the names, "inviterer dere til sitt bryllup", a flower divider, then date and place in letter-spaced small capitals.
- **A hand-pressed wax seal** in dark green with *R & V*, made by Rikke in an image tool ([19-Stamp.jpg](../../ux/inspirasjon/19-Stamp.jpg)), lying over the top edge of the invitation; also the browser-tab icon.
- **Flowers from the wedding, used sparingly.** One gypsophila (*brudeslør*) divider, also made by Rikke ([20-Flowers.jpg](../../ux/inspirasjon/20-Flowers.jpg)): in the hero, and smaller above the RSVP button. Discreet, not like [inspiration 05](../../ux/inspirasjon/05-Vibe.jpg).
- **One script moment.** The couple's first names in a formal copperplate-style script (as in [inspiration 09](../../ux/inspirasjon/09-Example.jpg)); everything else in a book serif that reads like a printed invitation.
- **One illustration.** A soft sage watercolour of Hardingasete in the top sheet, shown whole.
- **Real paper, not a hint of it.** Visible paper texture on page and sheets, tuned so it never changes the colours and never costs text contrast.

What it is not: gold, diamonds, metallic, glitter, neon, blinking or animated noise, clutter, luxury-brand gloss, draping, heart-shaped or lace letters, bluish "sage" greens, flowers spread over the page, sprigs drawn in code. The guest list spans everyone from teenagers to bestefar Sigmund (78), so restraint and legibility outrank decoration everywhere.

**Light only.** There is no dark mode; the invitation looks the same at all times (memlog, decision D). Pages declare `color-scheme: light only` so browser auto-dark modes (Samsung Internet, Chrome) leave them alone.

## Colors

The palette was chosen over six render rounds from colours sampled in the couple's own inspiration images, then tuned by their perception (memlog, *Page green FINAL*). Final pick: page **G4a**, panel **K1 havre**, text **T2**. The five candidate greens side by side: [mockups/color-themes-5.html](mockups/color-themes-5.html) (G4a is the chosen one; the render predates the final fonts and illustration).

| Token | Hex | Role | Never |
|---|---|---|---|
| `page-green` | `#5A6C48` | The page behind everything, including the sticky nav bar (flat there, textured elsewhere): a warm, slightly less yellow olive (G4a, hue ~90°). Also the envelope in the [If time] reveal. | Text on cream; button fill (it is only 1.79:1 against `green-dark`). |
| `green-dark` | `#344628` | Primary button fill, nav "Svar" button, footer band, focus ring on panels, A2 attention-panel top rule and answer-progress bar fill. | A page background (round 6 dark page rejected). |
| `green-dark-hover` | `#2C3A20` | Primary button hover/pressed; 10.49:1 with cream text. Too close to `green-dark` (1.18:1) to be the only tap feedback — see Focus ring. | Anything but the pressed button. |
| `seal` | `#344628` | The colour the seal image was made to match; used only if the seal has to be drawn without the image (e.g. a simplified favicon). Same value as `green-dark`. | — |
| `panel-cream` | `#EBE4D5` | All content panels ("havre"). | Large areas without texture. |
| `ink` | `#3B372F` | All text inside panels, including the names and form hints (T2 warm grey, chosen over dark green and walnut). | Text on green. |
| `ink-muted` | `#5E594F` | Only text nobody needs to act on: timestamps, "Ikke oppgitt", example-number notes. | Hints, body copy, progress line, anything the guest must read to act. |
| `cream-on-green` | `#F5EEDF` | Text, links, focus ring and the nav "Svar" button's 1px border on `page-green` and `green-dark`; also the empty track of the A2 answer-progress bar. | Panel background. |
| `field-surface` | `#F7F2E7` | Inside text fields, so fields read as "write here" on the panel. | Panels. |
| `field-border` | `#5E594F` | Text-field and select outline. | Decorative rules. |
| `divider` | `#C8BFAE` | 1px hairlines between admin rows and check-answer rows; never carries meaning on its own **[ASSUMPTION — no render defined a hairline]**. | Field outlines, focus. |
| `focus-on-panel` | `#344628` | Focus ring painted on cream. | — |
| `focus-on-green` | `#F5EEDF` | Focus ring painted on green and in the footer band. | — |
| `error` | `#7C3B1D` | Errors, tier-3 destructive actions, "Stemmer ikke". Sampled from the rust wax seal in inspiration 01. | Decoration; the only signal of an error. |
| `success` | `#3D5A2A` | "Svaret er sendt", saved confirmations, "Betalt", A2 «Ingenting trenger oppfølging nå». Renderer's own value, not chosen by the couple. | Primary buttons. |
| `warning` | `#765012` | "Ikke sendt ennå", unsent-draft notice, allergy-without-consent, conflict, unpaid. Renderer's own value, not chosen by the couple. | Errors. |
| `scrim` | `#344628` | Behind dialogs, at 60 % opacity **[ASSUMPTION]**. | — |

**Dark wood** from the brief has no UI token: walnut text (T3) was rejected, so dark wood lives only in photographs of the venue and in the illustration **[ASSUMPTION]**.

`error`, `success` and `warning` differ from each other by only 1.08–1.17:1 in luminance; they read as one dark brown to many older or colour-blind eyes. State is therefore always carried by **icon shape and words**, never colour (see Components › Notice, Status tag).

### Contrast pairs (WCAG 2.x, all text ≥ 4.5:1 — NFR-5)

| Pair | Ratio | Use |
|---|---|---|
| `ink` on `panel-cream` | 9.35:1 | All panel text |
| `ink` on `field-surface` | 10.61:1 | Typed text |
| `ink-muted` on `panel-cream` / `field-surface` | 5.50 / 6.23:1 | Meta only |
| `green-dark` on `panel-cream` | 8.08:1 | Secondary button text, focus ring on cream |
| `cream-on-green` on `page-green` (flat) | **4.95:1** | Nav words in the flat nav bar — the lowest small-text pair; never smaller than 18px |
| `cream-on-green` on the lightest pixel of the green texture (`#6D8358`) | 3.61:1 | Only large text (≥ 24px, needs 3:1): the lead-in. Measured in headless Chrome on `mockups/paper-ceremony-5.html`'s texture (see Elevation & Depth) |
| `cream-on-green` on `green-dark` | 8.86:1 | Buttons, nav "Svar", footer |
| `cream-on-green` on `green-dark-hover` | 10.49:1 | Pressed button |
| `error` on `panel-cream` / `field-surface` | 6.64 / 7.52:1 | Error text, destructive button |
| `success` on `panel-cream` | 6.16:1 | Success notice |
| `warning` on `panel-cream` | 5.67:1 | Warning notice |
| `field-border` vs `panel-cream` | 5.50:1 | Non-text, ≥ 3:1 required |
| `panel-cream` vs `page-green` | 4.52:1 | Panel edge against page (non-text) |
| `cream-on-green` border vs `page-green` | 4.95:1 | Nav "Svar" button outline (non-text); without it the button is 1.79:1 against the bar |

**Rule:** contrast on a textured surface is checked against the **lightest texture pixel**, not the average.

The PRD addendum asks to check "sage green on soft white": green is never text on cream here; the green-on-cream pair in use is `green-dark` on `panel-cream` at 8.08:1.

## Typography

Two self-hosted families, both SIL Open Font License, served from our own server as WOFF2 with Latin subsets including æ, ø, å, **keeping the `lnum` and `tnum` features** (PRD 3.2: guest pages load nothing from other companies). The Google Fonts links in the renders are a planning-mock exception only. Specimens: [mockups/typography-1.html](mockups/typography-1.html) (candidates S1–S6 and B1–B4; the chosen S4 + B1 at 20px are shown together in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html)).

- **Imperial Script** — the couple's first names only (*Rikke & Valdemar*, no surnames). Its upstrokes are hair-thin, so it is **display only**: the names at `{typography.display-names}` are the only Imperial Script on the site. Never for headings, labels, buttons or the admin area. The *R & V* on the seal is part of Rikke's seal image, not live text. Fallback: Georgia italic **[ASSUMPTION]**.
  - **Names wrap, never shrink.** At 48px one line needs about 274px (the 262px measured at 46px, scaled); the hero's content box is 288px on a 360px phone, so they fit on one line there. When they do not fit, the names stack on three centred lines — *Rikke* / *&* / *Valdemar* — as in inspiration 09. No shrink-to-fit, no `cqi` units, no JS fitting, no `nowrap`. *Valdemar* alone is about 142px, which fits every layout width down to 180 CSS px once the narrow-width gutters apply (Layout & Spacing). Re-measure in the build.
- **EB Garamond** — everything else. Its short x-height (0.41) is why guest body text is **20px**, above the NFR-5 floor of 18px (memlog, *Body font*). Regular and italic; weight 600 for labels and emphasis such as the invited names **[ASSUMPTION — the render used bold; 600 is the nearest weight to load]**. Fallback: Georgia.

Type tokens are written in px for readability; build them in `rem` (px ÷ 16) so the phone's text-size setting scales them. Running text uses `overflow-wrap: break-word` and `hyphens: auto` with `lang="nb"` so long compounds ("Allergiopplysningene") never force sideways scroll; the script names are never hyphenated.

| Role | Token | Where |
|---|---|---|
| Names | `display-names` | Hero sheet only; `h1` of the front page |
| Page title | `heading-page` | Info pages, form step question (`h1`), check page heading, receipt heading «Svaret er sendt» (32px, as rendered in the key-screen mockups) |
| Card heading | `heading-card` | Card and RSVP panel headings (`h2`) |
| Invites line | `invites`, *italic* | «inviterer dere til sitt bryllup» (du/dere rule) |
| Date | `date-line`, small capitals | «Lørdag 27. mai 2028» in the hero |
| Place | `place-line`, small capitals | «Hardingasete · Hardanger» in the hero |
| Invited line | `body`, *italic*; names upright | «for **Sigmund og bestemor**» in the hero (names upright regular, not bold) |
| Lead-in | `lead-in`, *italic* | One line on green between hero and cards; 24px so it may sit on the textured green (Elevation & Depth) |
| Nav words | `nav-words` | Sticky nav bar, 18px, slight letter spacing; only on the flat nav bar (Elevation & Depth) |
| Nav "Svar" | `nav-button` | The button in the nav bar |
| Buttons | `button` | All other guest buttons |
| Body | `body` | All guest running text, form hints (*italic*), progress line |
| Labels | `label` | Form labels and legends |
| Small | `small` | Only text nobody acts on: timestamps, "Ikke oppgitt", footer meta. The 18px floor; nothing on guest pages is smaller |
| Admin | `admin-heading`, `admin-body` | Admin working screens **[ASSUMPTION — denser, 18px body]**; the A2 answer-progress line («Svart: 28 av 30 husstander») uses `label` (20px, 600) |

**Figures:** amounts, dates, times, phone and account numbers use lining figures (`font-variant-numeric: lining-nums`), tables also tabular (`tabular-nums`); EB Garamond defaults to old-style figures, which older eyes misread. Thousands use a non-breaking space ("1 450 kr") so screen readers read one number.

**Small capitals in two places only:** the date and the place in the hero, set with `font-variant-caps: all-small-caps` and `{typography.date-line.letterSpacing}`, as on a printed invitation (memlog, *Front page approved*). The text stays in normal case in the HTML, so screen readers do not spell it out. No all-caps anywhere, and no small capitals for headings: the small-caps card headings in `paper-ceremony-5.html` below the hero were never decided (memlog, 2026-11-14) and wait for the below-the-hero revisit (EXPERIENCE Open Question 12).

## Layout & Spacing

Phone first (NFR-6). One centred column, maximum `{spacing.content-max}`; a PC shows the same phone column on the green page **[ASSUMPTION — 480px max]**. Side gutter `{spacing.gutter}`. No horizontal scroll at 320px or at 200 % zoom (NFR-5); on a phone 200 % zoom means a layout width of about **180 CSS px**, so below 260px layout width the gutter and the hero's inline padding drop to `{spacing.gutter-narrow}`.

Front-page order. The first screen is approved in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html) (memlog, *Front page approved*, 2026-11-11), which supersedes [mockups/front-page-2.html](mockups/front-page-2.html) for the nav bar and the hero; front-page-2 still shows the order of the cards below (PRD FR-7, FR-8):

1. **Nav bar**, sticky (see EXPERIENCE › Accessibility Floor for when it stops sticking): nav words left, the "Svar" button right, `{spacing.nav-height}` tall, flat green.
2. **Hero sheet**, `{spacing.page-padding-top}` below the nav bar so the seal is never hidden under it: seal over the top edge → illustration 17, whole → names → «inviterer dere til sitt bryllup» → gypsophila divider → date and place in small capitals → «for Sigmund og bestemor» → deadline line *«**Svar** innen 4. januar 2028»*, where "Svar" is a link. The short deadline here has no weekday or time; the full deadline sits above the RSVP button (FR-41 asks for it next to the button). No button and no child-free line in the hero.
3. Lead-in line on green.
4. Four info cards, `{spacing.panel-gap}` apart (Gifts as a fifth only if built).
5. **RSVP sheet** (jump target of both "Svar" links): heading "Svar på invitasjonen", a small gypsophila (180px), the child-free line, the full deadline «Svar innen tirsdag 4. januar 2028 kl. 23:59», the primary button.
6. Footer band, full-bleed `green-dark`.

Items 3–5 are the part of the front page the couple wants to revisit (EXPERIENCE Open Question 12). The answered state (where the status block goes) is Open Question 1.

**First-screen budget** (measured 2026-11-14 in headless Chrome at 360px wide, fonts and images loaded; the fold is 560px, what a browser or Messenger shows on a 360 × 640 phone):

| Element | Top–bottom (px) |
|---|---|
| Nav bar · nav "Svar" | 0–64 · 10–54 |
| Seal | 74–150 |
| Hero sheet | 110–**552** |
| Illustration · names (one line) | 124–267 · 271–327 |
| Divider · date · place | 357–407 · 407–437 · 437–463 |
| «for …» · deadline line | 469–499 · 503–**530** |

The whole hero sheet fits above the fold with 8px to spare, so these values are a budget, not a starting point: any added line or larger seal pushes the sheet's end off the first screen. At 320px the nav words wrap to two lines (bar 104px), the names and the place wrap, and the deadline line ends at 651px, below the fold; the nav "Svar" stays visible (Open Question 2). Check widths for every build: 360 × 560, 320 × 568, 180 × 320.

Hero spacing: padding `{spacing.hero-padding-top}` / `{spacing.hero-padding-inline}` / `{spacing.hero-padding-bottom}`; seal centred with its top 36px above the sheet's top edge; illustration pulled up 12px (its top is empty sky) with 4px below; invites 2px below the names; divider 2px below; 6px above the invited line, 4px above the deadline line. Cards: padding 24/22/14px (the "Les mer" target supplies the bottom space). Scale is 4-based: `{spacing.1}`–`{spacing.7}`. Text in the hero, cards and RSVP sheet is centred; form steps, check page, receipt and admin are left-aligned (as rendered in the key-screen mockups below).

Sections are separated by green showing between panels, which answers inspiration 08's "not one long page on one identical background".

**Form step, check page and receipt** (one cream panel per screen on the green page; no nav bar, footer band kept). Rendered at 360px in [mockups/key-form-steps.html](mockups/key-form-steps.html) (steps 1, 3 and 5, an error state and the draft offer), [mockups/key-check-page.html](mockups/key-check-page.html) and [mockups/key-receipt.html](mockups/key-receipt.html) (receipt, payment details, and the answered front page per EXPERIENCE Open Question 1):

- **Form step:** step question (`h1`) → progress line → respondent line (**on every step**) → one fieldset per person or question → running total (paid steps only) → **"Fortsett" (primary) above "Tilbake" (secondary), both full width, 12px apart, 24px below the content** **[forslag — button order]**.
- **Check page:** warning notice «Obs: Svaret er ikke sendt ennå.» first, then the `h1` «Se over svaret før du sender» **[forslag]**, the check-answers list, the running total, "Send svaret" above "Tilbake".
- **Receipt:** success notice holding the `h1` «Svaret er sendt» and the sent-by line, Rikke's message, the summary, the total, "Betal nå" above "Betal senere", and the closing line directly below them.

**Admin:** same tokens, denser. Panels use `{spacing.admin-panel-padding}` and `{spacing.admin-gap}`; lists and tables rather than cards; quick tasks (find guest, copy link, see if answered) fit one phone screen (FR-48). When density and targets collide, **44px targets win**; lists scroll.

**Admin home (A2)**, as approved in [mockups/admin-rework-1.html](mockups/admin-rework-1.html) (memlog, *Admin rework approved*; PRD FR-54, FR-56, FR-57). The earlier grouping in `.working/key-admin-overview.html` (summary first, «Dager, senger og mat» in one panel, attention list last) is **superseded** and stays in `.working/` only; its helper view is still the only render of read-only admin (see EXPERIENCE Open Question 15). Order on the page, under the Admin nav:

1. **Attention panel** «Trenger oppfølging (n)» — first, without scrolling. Shows as many items as fit while the answer-progress line below still sits on the first screen (two items at 360 × 560 in the render), then «Vis alle n». Empty: the panel heading becomes the check icon + «Ingenting trenger oppfølging nå», with «Vis håndterte» below.
2. **Svar panel** — the answer-progress line «Svart: X av Y husstander», a progress bar under it, the Kommer / Kommer ikke / Ikke svart ennå rows, and «Se hva alle har svart» (to A4, FR-57).
3. **Summary panels**, one small panel per group, in this order: *Når kommer de?* · *Overnatting* · *Mat* · *Allergier (med samtykke)* · *Fjelltur fredag* · *Betaling (husstander som kommer)*. Contents: EXPERIENCE › Component Patterns › Admin summary panel.

## Elevation & Depth

**Paper sheets on an envelope.** Every guest content panel is a cream sheet lying on the green page, as the main sheet in [inspiration 01](../../ux/inspirasjon/01-Vibe.jpg): a soft, slightly wavy, hand-made edge with fine fibre, in **the sheet's own colour** (no lighter rim, no inner ridge, nothing chalk-white), and a soft shadow underneath. Chosen over three rounds of edge renders (memlog, *Sheet edge* and *Sheet edge refined*; edge B3). Still **no folds, no backing sheet, no layered or offset sheets** (memlog override dropping the layered-sheet card style). Reference: [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html), filter `edge-b3`.

How the sheet is built, so the edge never touches the text:

- Colour, texture, edge and shadow sit on a layer **behind** the content (`::before`); only that layer is filtered. Text, links and focus rings stay sharp, and their contrast is unchanged.
- The edge is an SVG filter (displacement for the wave, fine noise for the fibre, blur 3.2px offset 2.5px at 42 % `#141A0C` for the shadow). If it is slow on old phones, the build may swap it for a pre-rendered edge image with the same look (memlog, *Technical defaults while folding in*).
- Under forced colours, or where filters are unsupported, the sheet falls back to flat `panel-cream` with `{rounded.sheet}` corners. The edge and shadow are decoration; the flat sheet is a complete design.

Depth appears in exactly four places:

- **The sheets**, as above.
- **The seal**: Rikke's image already looks like pressed, glossy wax; the page adds `drop-shadow(0 2px 2px rgba(12,16,8,.45))` so it lies *on* the sheet's top edge.
- **The sticky nav bar**: a 1px hairline of `cream-on-green` at 22 % along its bottom edge, so content visibly slides under it.
- **Dialogs**: a cream sheet over `{colors.scrim}` at 60 % **[ASSUMPTION]**.

**Paper texture.** Page and sheets carry a fine paper grain: tiling SVG noise layers (fine grain and soft fibre, inline data-URIs, no network) blended with `overlay` around mid-grey, so the **average colour is unchanged**. The green texture is the calmer one approved in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html) (`--grain-green`). Contrast is checked against the worst texture pixel (memlog, *Technical default, measured*):

- **Green:** the lightest pixel is `#6D8358`, which gives cream text 3.61:1. So cream text on the *textured* green must be **large (≥ 24px)**, where 3:1 is enough: that is the lead-in. Smaller cream text, the nav words, sits only in the **flat** nav bar (4.95:1). The weakened-texture rule from the first review (cap at `#5F7250`) is superseded; weakening it that far removed the grain.
- **Sheet:** the darkest pixel is `#DBCFB4`. Worst cases: `ink` 7.67:1, `ink-muted` 4.51:1, `warning` 4.65:1, `success` 5.05:1, `error` 5.44:1, `green-dark` 6.62:1. All pass.
- Re-measure on a screenshot of the built page if the texture changes. The texture is decoration: if it fails to load, the flat token colours are the design.

## Shapes

Guest sheets have a soft, hand-made edge (Elevation & Depth) over `{rounded.sheet}` (5px) corners, which is also their flat fallback. Inside the sheets everything is crisp: `{rounded.sm}` (3px) for fields, notices and tags; `{rounded.md}` (4px) for buttons and checkboxes; `{rounded.full}` only for radio buttons. No pills, no circles for surfaces, no arched or scalloped tops, no torn or ripped look (the edge is soft, not jagged).

Two organic shapes come from Rikke's own images, not from code:

- The **seal**: an uneven, hand-pressed wax disc with *R & V*, glossy dark green ([19-Stamp.jpg](../../ux/inspirasjon/19-Stamp.jpg), cut out to [mockups/segl-19.png](mockups/segl-19.png)).
- The **gypsophila divider**: two crossing sprigs with green stems and white flowers ([20-Flowers.jpg](../../ux/inspirasjon/20-Flowers.jpg), cut out to [mockups/brudeslor-20.png](mockups/brudeslor-20.png)).

Both are cut out with [.working/cutout-segl-brudeslor.py](.working/cutout-segl-brudeslor.py), because the seal lies over the green edge and white petals would disappear if blended into the cream. If Rikke replaces an image, run the script again rather than editing the PNGs. Code-drawn sprigs and seals were tried and rejected ("så jalla ut", memlog 101–105).

## Components

Frontmatter key in brackets where one exists.

| Component | Visual spec |
|---|---|
| **Page** [`page`] | `{colors.page-green}` with the calm paper texture. Never plain white anywhere. |
| **Paper sheet** [`paper-sheet`] | The surface of every guest content panel: cream, textured, soft hand-made edge in its own colour, soft shadow, all on a layer behind the content. Flat `{rounded.sheet}` fallback (Elevation & Depth). |
| **Nav bar** [`nav-bar`, `nav-words`] | Full-width strip, **flat** `{colors.page-green}` (no texture), 64px, a faint cream hairline below. Nav words left (Program · Praktisk · Stedet · Om oss), `{typography.nav-words}` in `{colors.cream-on-green}`, **not underlined**, 12px apart, each ≥ 44 × 44px; no separator characters; may wrap to two lines; no hamburger. Current page: 2px underline, offset 4px **[ASSUMPTION]**. |
| **Nav "Svar" button** [`nav-svar`] | Right end of the nav bar: `{colors.green-dark}` fill, cream text, **1px `{colors.cream-on-green}` border** (dark green on page-green is only 1.79:1), ≥ 64 × 44px. The one primary-styled control allowed on green. |
| **Hero sheet** [`hero-panel`] | Centred, in this order: seal over the top edge, illustration, names, invites line, gypsophila divider, date and place in small capitals, «for <household>», short deadline line with the "Svar" link. Rendered in [mockups/paper-ceremony-5.html](mockups/paper-ceremony-5.html). |
| **Wax seal** [`wax-seal`] | Rikke's seal image, 74px wide, centred with its top 36px above the hero sheet's top edge, drop shadow. Decorative (`alt=""`). The favicon is made from the same image (at 32px and 180px). |
| **Hero illustration** [`hero-illustration`] | [Image 17](../../ux/inspirasjon/17-Illustration.jpg) (cool sage watercolour of the bell house and main house among pines with string lights), **shown whole** at 262px wide, pulled up 12px under the seal, `mix-blend-mode: darken` so its paper melts into the cream (`normal` under forced colours). Final file has no signature or text and ships with the app. Alternatives I5–I8: [mockups/illustration-3.html](mockups/illustration-3.html) (I7 chosen). The 150px cropped band in front-page-2.html is superseded (Rikke: "kuttet for mye"). |
| **Flower divider** [`flower-divider`] | Rikke's gypsophila image, 224px wide in the hero (between invites line and date), 180px above the child-free line in the RSVP sheet. Decorative (`alt=""`), no blend mode. The only flowers on the page. |
| **Info card** [`panel`] | Paper sheet. `{typography.heading-card}`, two or three lines of `{typography.body}`, then a "Les mer" link whose target covers the whole card. Centred. |
| **Lead-in** [`lead-in`] | One italic line on the textured green, 24px, e.g. «Vi gleder oss til å feire med dere». |
| **RSVP sheet** [`rsvp-panel`] | Paper sheet after the cards: `heading-card` "Svar på invitasjonen", small gypsophila divider, child-free line («Barnefritt bryllup – …», placement and text a proposal), the full deadline «Svar innen tirsdag 4. januar 2028 kl. 23:59», primary button. When an unsent draft exists, a warning notice sits above the button. |
| **Primary button** [`button-primary`] | Full panel width, 52px, cream text on dark green, 2px transparent border (visible outline in forced colours). Only on cream panels — the nav "Svar" is the one exception. **One distinct primary action per screen; repeats of the same action are allowed** (nav "Svar" and RSVP button). Busy: keeps its colours, label becomes "Sender …". |
| **Secondary button** [`button-secondary`] | Outlined dark green on cream; border 3px on hover/pressed. For "Tilbake", "Betal senere", "Avbryt", "Nei, begynn på nytt". In form steps, check page and receipt it sits **below** the primary button, same full width **[forslag]**. |
| **Destructive button** [`button-destructive`] | Muted rust outline on cream, placed apart (tier 3 only); border 3px on hover/pressed. Filled rust is not used **[ASSUMPTION — "muted rust" read as outline]**. |
| **Focus ring** [`focus-ring`] | 3px outline at 3px offset on `:focus-visible` and on `:active` (tap feedback). Colour by the surface the ring is **painted on**: `focus-on-panel` on cream, `focus-on-green` on green or the footer. Never `outline: none`. |
| **Text link / "Les mer"** [`link-more`] | Inherits text colour, always underlined (1px, 4px offset; 2px on hover/pressed), target ≥ 44px. Never colour alone. |
| **Footer band** [`footer-band`] | Full-bleed `{colors.green-dark}`, cream text, 20px: "Spørsmål? Send oss en melding:", then **each phone number on its own ≥ 44px row** ("Rikke 900 00 000", "Valdemar 900 00 001"), then "Spør oss" and "Personvern" as underlined cream links. |
| **Text field** [`field`] | Field surface, 2px border, label above in `{typography.label}`, hint below in `{typography.body}` *italic* `{colors.ink}`. Error: 3px `{colors.error}` border and the error line (icon + text) between label and field. Variants: multi-line (G10 question, ≥ 4 lines), search (A6), typed confirmation (tier 3). |
| **Choice control** [`choice-control`] | 26px box, 2px ink border; checkbox `{rounded.md}`, radio `{rounded.full}`; selected mark in `{colors.green-dark}` drawn so it survives forced colours (native input with `accent-color`, or a `currentColor` mark — never a background fill alone). Whole row ≥ 44px is the target. Group error (a fieldset of choices): **no border on the group**; one error line under the legend, before the first choice: 22px triangle icon + «Feil: …» in `{colors.error}` (e.g. «Feil: Velg «Kommer» eller «Kommer ikke» for bestemor.» **[forslag]**), as in [mockups/key-form-steps.html](mockups/key-form-steps.html). |
| **Notice** [`notice`] | 4px left rule, 22px icon and text in the state colour on cream. Icon shapes differ: success = check, warning = circle with "!", error = triangle with "!", info (`ink`) = "i". Error and warning also start with a word ("Feil:", "Obs:" — proposal). Variants: success, warning, error, info; last-updated header (info). |
| **Error summary** | Error notice at the top of the step panel with a heading and linked list of errors. |
| **Status block** | Cream panel shown once answered, left-aligned: `heading-card` «Svaret er sendt», then «Sendt av Sigmund tirsdag 12. oktober 2027 kl. 14:31.», «Totalt for husstanden: 3 900 kr», «Meldt betalt: 3 900 kr, 12. oktober.», «Dere kan endre svaret fram til tirsdag 4. januar 2028 kl. 23:59.», and the primary button "Se eller endre svar" **[forslag — wording except the button]**. Rendered in [mockups/key-receipt.html](mockups/key-receipt.html) (second phone). Position: Open Question 1 in EXPERIENCE. |
| **Draft offer** | Cream panel at the top of the form: heading «Vil du fortsette der du slapp?», one line saying when the answer was started, primary "Ja, fortsett", secondary "Nei, begynn på nytt". Rendered in [mockups/key-form-steps.html](mockups/key-form-steps.html). |
| **Progress line** | "Steg 3 av 6: Overnatting" in `{typography.body}`, directly under the step question; no graphic stepper **[ASSUMPTION]**. |
| **Respondent line** | "Jeg er **Sigmund** · Bytt" — "Bytt" a button styled as an underlined link (≥ 44px) — directly under the progress line **on every form step**, so the guest always sees who is answering; switching opens a radio list of household members in the panel **[ASSUMPTION]**. |
| **Running total** | Right-aligned "Totalt for husstanden: 1 450 kr", lining figures, `divider` hairline above, at the foot of each paid step. |
| **Read-more disclosure** | Underlined "Les mer om …" with a small chevron; expands in place with a left rule in `{colors.divider}`. |
| **Consent block** | Section at the end of the allergies step, after a `divider`: purpose and recipients text (`body`), how to withdraw, then the Ja/Nei choice under its legend, then — when answering for others — the "Jeg bekrefter …" checkbox. No special colour; nothing pre-selected. |
| **Check-answers list** | Under the `h1` «Se over svaret før du sender» **[forslag]**: one block per part (Hvem kommer · Dager · Overnatting · Måltider · Allergier og matbehov · Fjelltur fredag) with the part name and its "Endre" link on one line, then one line per person ("Sigmund: kommer"); `divider` between parts; "Ikke oppgitt" in `ink-muted`. Rendered in [mockups/key-check-page.html](mockups/key-check-page.html). |
| **Receipt panel** | Cream panel. Success notice at top carrying the `h1` «Svaret er sendt» and «Sendt av Sigmund tirsdag 12. oktober 2027 kl. 14:31.» **[forslag]**; Rikke's message in `{typography.body}`; summary «Dette har dere svart» **[forslag]** and the running total; then "Betal nå" / "Betal senere" with the closing line «Du kan nå trygt lukke invitasjonen.» directly below them. Rendered in [mockups/key-receipt.html](mockups/key-receipt.html). |
| **Payment details** | Cream panel «Slik betaler du» **[forslag]** listing amount, Vipps number, account number and payment message as selectable `body` text, each with a secondary "Kopier" button and «Kopiert» beside the last-used one; "Jeg har betalt" below **[ASSUMPTION]**. Rendered in [mockups/key-receipt.html](mockups/key-receipt.html). |
| **Envelope reveal** [If time] | `{colors.page-green}` envelope closed with Rikke's seal image, opening into a **plain** paper sheet that becomes the hero sheet (same edge, same seal position). No heart shape, no lace, no folds. "Hopp over" ≥ 44 × 44 on cream or `green-dark`. |
| **Admin nav** | Reuses Nav words on the green page (Oversikt · Gjester · Betalinger · Spørsmål · Innstillinger · Logg ut), **not sticky**, no "Svar" button **[ASSUMPTION]**. |
| **Attention panel** [`attention-panel`] | A2's first panel: cream, `admin-panel-padding`, a 5px `{colors.green-dark}` rule along the top edge so it reads as "start here" (decoration; the heading carries the meaning) **[forslag]**. `admin-heading` «Trenger oppfølging (7)», then attention items with `divider` between, then «Vis alle 7» as an underlined link (≥ 44px) after a `divider`. Rendered in [mockups/admin-rework-1.html](mockups/admin-rework-1.html). |
| **Attention empty state** | The attention panel without the top rule: its heading becomes a 26px check icon + «Ingenting trenger oppfølging nå» in `{colors.success}` (icon and words, never colour alone), then «Vis håndterte». Rendered in [mockups/admin-rework-1.html](mockups/admin-rework-1.html) (second phone). |
| **Attention item** | Admin row: reason in 600 weight («Betalingen stemmer ikke», «Har ikke svart ennå»), household and detail in `admin-body`, one secondary action ("Merk som håndtert"); mismatches also carry the "Stemmer ikke" status tag (error icon + word). |
| **Answer progress** [`answer-progress`] | Top of A2's Svar panel: «Svart: 28 av 30 husstander» in `label` (20px, 600, lining figures), then a 12px bar (track `cream-on-green`, fill `green-dark`, 1px `ink-muted` border). **The text carries the number; the bar is decoration** (`aria-hidden`, fill drawn as `CanvasText` under forced colours). |
| **Admin summary panel** | One small cream panel per group (`admin-heading` + rows). Each row: `{typography.admin-body}` label left, count right as a link (0 is plain text); ≥ 44px tall; `divider` between rows. Lead rows in 600 weight; breakdown rows indented 18px with a dotted `divider`; a secondary row («Senger totalt») in `ink-muted`; an optional italic `ink-muted` note under the rows («Én person kan ha flere allergier.»). Contents per panel: EXPERIENCE › Component Patterns. |
| **Admin summary row** | Inside a summary panel: label and count; the Svar rows show two counts («58 personer · 25 husstander»), the hike row two linked figures («5 kommer, 2 kanskje»), "kanskje" never added to "kommer". |
| **Overview table** | A4: on PC a table in a cream panel (`admin-body`, 600-weight header row, `divider` rows); on phone stacked rows that repeat each label as visible text ("Betalt: 900 kr"). Unanswered households sort first and carry the "Ikke svart" tag. |
| **Undo (in place)** | After a tier-1 action the row is replaced in place by "Merket som håndtert." and an "Angre" link-button. No fixed bar, no toast (kept after the key-screen render). |
| **Status tag** [`status-tag`] | Outlined label in the state colour, icon as in Notice. Mapping **[ASSUMPTION — proposal]**: "Betalt" → success · "Ikke betalt", "Delbetalt, 300 kr mangler", "Skal ha tilbake 200 kr", "Ikke svart" → warning · "Stemmer ikke" → error · "Ingenting å betale", "Endret" → ink (info). |
| **Dialog** [`dialog`] | Consequence sentence, then actions; on narrow screens buttons stack full-width, safe action first. |

## Do's and Don'ts

| Do | Don't |
|---|---|
| Cream paper sheets on the green page: textured, soft hand-made edge in the sheet's own colour, soft shadow | Folds, backing or offset sheets, a light or chalk-white rim, jagged torn edges |
| Primary buttons on cream panels; the nav "Svar" (with its cream border) is the only exception | A dark green button on green without the cream border |
| The nav bar is the only thing that sticks | Other sticky or fixed bars, on guest or admin pages |
| Imperial Script for the names only (48px, stacking when needed) | Script for headings, labels, buttons or admin; shrinking the names to fit |
| Small capitals for the date and place in the hero only | All-caps; small-caps headings |
| EB Garamond 20px for guest body text, hints in `ink` | Guest text under 18px; hints in `ink-muted` |
| Warm olive greens (hue ~85–100°) | Bluish sage greens (round 1), neon or saturated greens |
| Cream `#F5EEDF` text under 24px only on the flat nav bar; 24px or larger may sit on the textured green | Small cream text on the textured green |
| State colour plus icon shape plus words | Red/green/brown alone to mean anything (WCAG 1.4.1) |
| One illustration (17, whole) in the hero, one seal, the gypsophila divider in two places — all from Rikke's images | Icons, sprigs, leaves, ornaments sprinkled through the page; flowers or seals drawn in code |
| Venue photos as information on info pages | Venue photos as style or background texture |
| Same tokens in admin, denser, no decoration, 44px targets | Seal, illustration or script on admin working screens |
| A plain paper sheet in the envelope reveal | A heart-shaped or lace letter |
| Restraint | Gold, metallic, diamonds, glitter, bling, neon, blinking, draping, clutter, luxury-brand feel, Italian or olive-plant motifs |
