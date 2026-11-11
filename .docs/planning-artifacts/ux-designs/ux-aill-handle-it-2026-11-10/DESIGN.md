---
name: "AI'll handle it"
description: "Rikke & Valdemar's wedding invitation as a website: flat cream panels on a textured olive-green page, a dark green wax seal, a script name line and printed-invitation body text. Light only."
status: draft
created: 2026-11-10
updated: 2026-11-11
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
    fontSize: 46px
    fontWeight: '400'
    lineHeight: '1.15'
  monogram:
    fontFamily: 'Imperial Script'
    fontSize: 23px
    fontWeight: '400'
    lineHeight: '1'
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
    fontSize: 24px
    fontWeight: '400'
    lineHeight: '1.3'
  lead-in:
    fontFamily: 'EB Garamond'
    fontSize: 23px
    fontWeight: '400'
    lineHeight: '1.4'
  invites:
    fontFamily: 'EB Garamond'
    fontSize: 21px
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
  hero-padding-top: 14px
  hero-padding-bottom: 18px
  hero-padding-inline: 18px
  admin-panel-padding: 12px
  admin-gap: 8px
  content-max: 480px
  target-min: 44px
  button-height: 52px
  nav-height: 52px
  scroll-gap: 12px
  focus-width: 3px
  focus-offset: 3px
components:
  page:
    background: '{colors.page-green}'
    texture: 'paper-grain; zero average colour shift; on page-green no pixel lighter than #5F7250'
  nav-bar:
    background: '{colors.page-green}'
    texture: 'same as page'
    height: '{spacing.nav-height}'
    padding: '4px 10px 4px 14px'
    shadow: '0 2px 6px rgba(20,24,14,.28)'
    position: 'sticky top 0, only when viewport height >= 400px'
  nav-words:
    foreground: '{colors.cream-on-green}'
    typography: '{typography.nav-words}'
    gap: '11px'
    underline: '1px, offset 4px'
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
  panel:
    background: '{colors.panel-cream}'
    foreground: '{colors.ink}'
    radius: '{rounded.sm}'
    padding: '{spacing.panel-padding}'
    shadow: 'none'
  hero-panel:
    background: '{colors.panel-cream}'
    foreground: '{colors.ink}'
    radius: '{rounded.sm}'
    padding: '{spacing.hero-padding-top} {spacing.hero-padding-inline} {spacing.hero-padding-bottom}'
  rsvp-panel:
    background: '{colors.panel-cream}'
    foreground: '{colors.ink}'
    radius: '{rounded.sm}'
    padding: '22px 18px 20px'
    scrollMarginTop: 'nav-height + scroll-gap'
  wax-seal:
    fill: '{colors.seal}'
    foreground: '{colors.cream-on-green}'
    size: 68px
    rotate: -5deg
    typography: '{typography.monogram}'
  hero-illustration:
    width: 'full hero-panel width (bleeds over the inline padding)'
    height: 150px
    objectFit: cover
    objectPosition: '50% 58%'
    blend: 'mix-blend-mode: darken; normal under forced-colors'
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
    padding: '22px 10px 20px'
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

- **An envelope-coloured page with cream sheets on it.** Olive-green textured page, flat cream panels carrying the content (direction B *Konvolutten*, about half green, half cream).
- **A hand-pressed wax seal** in dark green with *R & V*, at the top of the invitation and as the browser-tab icon.
- **One script moment.** The couple's first names in a formal copperplate-style script (as in [inspiration 09](../../ux/inspirasjon/09-Example.jpg)); everything else in a book serif that reads like a printed invitation.
- **One illustration.** A soft sage watercolour of Hardingasete in the top panel.
- **Real paper, not a hint of it.** Visible paper texture on page and panels, tuned so it never changes the colours and never costs text contrast.

What it is not: gold, diamonds, metallic, glitter, neon, blinking or animated noise, clutter, luxury-brand gloss, draping, heart-shaped or lace letters, bluish "sage" greens. The guest list spans everyone from teenagers to bestefar Sigmund (78), so restraint and legibility outrank decoration everywhere.

**Light only.** There is no dark mode; the invitation looks the same at all times (memlog, decision D). Pages declare `color-scheme: light only` so browser auto-dark modes (Samsung Internet, Chrome) leave them alone.

## Colors

The palette was chosen over six render rounds from colours sampled in the couple's own inspiration images, then tuned by their perception (memlog, *Page green FINAL*). Final pick: page **G4a**, panel **K1 havre**, text **T2**. The five candidate greens side by side: [mockups/color-themes-5.html](mockups/color-themes-5.html) (G4a is the chosen one; the render predates the final fonts and illustration).

| Token | Hex | Role | Never |
|---|---|---|---|
| `page-green` | `#5A6C48` | The page behind everything, including the sticky nav bar: a warm, slightly less yellow olive (G4a, hue ~90°). | Text on cream; button fill (it is only 1.79:1 against `green-dark`). |
| `green-dark` | `#344628` | Primary button fill, nav "Svar" button, footer band, focus ring on panels. | A page background (round 6 dark page rejected). |
| `green-dark-hover` | `#2C3A20` | Primary button hover/pressed; 10.49:1 with cream text. Too close to `green-dark` (1.18:1) to be the only tap feedback — see Focus ring. | Anything but the pressed button. |
| `seal` | `#344628` | Wax seal body. Same value as `green-dark`, separate token so the seal can be tuned alone. | — |
| `panel-cream` | `#EBE4D5` | All content panels ("havre"). | Large areas without texture. |
| `ink` | `#3B372F` | All text inside panels, including the names and form hints (T2 warm grey, chosen over dark green and walnut). | Text on green. |
| `ink-muted` | `#5E594F` | Only text nobody needs to act on: timestamps, "Ikke oppgitt", example-number notes. | Hints, body copy, progress line, anything the guest must read to act. |
| `cream-on-green` | `#F5EEDF` | Text, links, focus ring and the nav "Svar" button's 1px border on `page-green` and `green-dark`. | Panel background. |
| `field-surface` | `#F7F2E7` | Inside text fields, so fields read as "write here" on the panel. | Panels. |
| `field-border` | `#5E594F` | Text-field and select outline. | Decorative rules. |
| `divider` | `#C8BFAE` | 1px hairlines between admin rows and check-answer rows; never carries meaning on its own **[ASSUMPTION — no render defined a hairline]**. | Field outlines, focus. |
| `focus-on-panel` | `#344628` | Focus ring painted on cream. | — |
| `focus-on-green` | `#F5EEDF` | Focus ring painted on green and in the footer band. | — |
| `error` | `#7C3B1D` | Errors, tier-3 destructive actions, "Stemmer ikke". Sampled from the rust wax seal in inspiration 01. | Decoration; the only signal of an error. |
| `success` | `#3D5A2A` | "Svaret er sendt", saved confirmations, "Betalt". Renderer's own value, not chosen by the couple. | Primary buttons. |
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
| `cream-on-green` on `page-green` | **4.95:1** | Nav words, lead-in — the lowest text pair; never smaller than 18px |
| `cream-on-green` on lightest allowed texture pixel `#5F7250` | 4.53:1 | Texture limit on green (see Elevation & Depth) |
| `cream-on-green` on `green-dark` | 8.86:1 | Buttons, nav "Svar", seal monogram, footer |
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

Two self-hosted families, both SIL Open Font License, served from our own server as WOFF2 with Latin subsets including æ, ø, å, **keeping the `lnum` and `tnum` features** (PRD 3.2: guest pages load nothing from other companies). The Google Fonts links in the renders are a planning-mock exception only. Specimens: [mockups/typography-1.html](mockups/typography-1.html) (candidates S1–S6 and B1–B4; the chosen S4 + B1 at 20px are shown together in [mockups/front-page-2.html](mockups/front-page-2.html)).

- **Imperial Script** — the couple's first names (*Rikke & Valdemar*, no surnames) and the *R & V* seal monogram. Its upstrokes are hair-thin, so it is **display only**: the names at `{typography.display-names}` are the only Imperial Script anyone must read; the 23px monogram sits inside the decorative, screen-reader-hidden seal. Never for headings, labels, buttons or the admin area. Fallback: Georgia italic **[ASSUMPTION]**.
  - **Names wrap, never shrink.** One line needs a 262px content box (measured, fonts loaded); when it does not fit, the names stack on three centred lines — *Rikke* / *&* / *Valdemar* — as in inspiration 09. No shrink-to-fit, no `cqi` units, no JS fitting, no `nowrap`. *Valdemar* alone is 136px, which fits every layout width down to 180 CSS px once the narrow-width gutters apply (Layout & Spacing).
- **EB Garamond** — everything else. Its short x-height (0.41) is why guest body text is **20px**, above the NFR-5 floor of 18px (memlog, *Body font*). Regular and italic; weight 600 for labels and emphasis such as the invited names **[ASSUMPTION — the render used bold; 600 is the nearest weight to load]**. Fallback: Georgia.

Type tokens are written in px for readability; build them in `rem` (px ÷ 16) so the phone's text-size setting scales them. Running text uses `overflow-wrap: break-word` and `hyphens: auto` with `lang="nb"` so long compounds ("Allergiopplysningene") never force sideways scroll; the script names are never hyphenated.

| Role | Token | Where |
|---|---|---|
| Names | `display-names` | Hero panel only; `h1` of the front page |
| Seal | `monogram` | Seal and favicon |
| Page title | `heading-page` | Info pages, form step question (`h1`), receipt heading **[ASSUMPTION — size not rendered]** |
| Card heading | `heading-card` | Card and RSVP panel headings (`h2`) |
| Date | `date-line` | "Lørdag 27. mai 2028" in the hero |
| Lead-in | `lead-in`, *italic* | One line on green between hero and cards |
| Invites line | `invites`, *italic* | "inviterer deg til bryllup" |
| Nav words | `nav-words` | Sticky nav bar (rendered at 18px; cream on green at the floor size, so the texture limit is mandatory) |
| Nav "Svar" | `nav-button` | The button in the nav bar |
| Buttons | `button` | All other guest buttons |
| Body | `body` | All guest running text, form hints (*italic*), progress line |
| Labels | `label` | Form labels and legends |
| Small | `small` | Only text nobody acts on: timestamps, "Ikke oppgitt", footer meta. The 18px floor; nothing on guest pages is smaller |
| Admin | `admin-heading`, `admin-body` | Admin working screens **[ASSUMPTION — denser, 18px body]** |

**Figures:** amounts, dates, times, phone and account numbers use lining figures (`font-variant-numeric: lining-nums`), tables also tabular (`tabular-nums`); EB Garamond defaults to old-style figures, which older eyes misread. Thousands use a non-breaking space ("1 450 kr") so screen readers read one number. No all-caps, no letter-spaced small caps (the small-caps card style was explicitly not decided).

## Layout & Spacing

Phone first (NFR-6). One centred column, maximum `{spacing.content-max}`; a PC shows the same phone column on the green page **[ASSUMPTION — 480px max]**. Side gutter `{spacing.gutter}`. No horizontal scroll at 320px or at 200 % zoom (NFR-5); on a phone 200 % zoom means a layout width of about **180 CSS px**, so below 260px layout width the gutter and the hero's inline padding drop to `{spacing.gutter-narrow}`.

Front-page order, as approved in [mockups/front-page-2.html](mockups/front-page-2.html) (memlog, *Front page redesign* and *New front page approved*; PRD FR-7, FR-8):

1. **Nav bar**, sticky (see EXPERIENCE › Accessibility Floor for when it stops sticking): nav words left, the "Svar" button right, `{spacing.nav-height}` tall.
2. **Hero panel**: seal (68px) → illustration (150px band, full panel width) → names → invites line → date → place → "Invitert: …" → deadline line *"**Svar** innen onsdag 1. desember 2027 kl. 23:59"*, where "Svar" is a link. No button and no child-free line in the hero.
3. Lead-in line on green.
4. Four info cards, `{spacing.panel-gap}` apart (Gifts as a fifth only if built).
5. **RSVP panel** (jump target of both "Svar" links): heading "Svar på invitasjonen", the child-free line, the deadline, the primary button.
6. Footer band, full-bleed `green-dark`.

The answered state (where the status block goes) is Open Question 1 in EXPERIENCE.

**First-screen budget** (measured at 360px wide, fonts and image loaded; the fold is 560px, what a browser or Messenger shows on a 360 × 640 phone): nav "Svar" bottom 48px, deadline "Svar" link 525px, deadline line bottom **553px**. The margin is 7px, so the hero values below are a budget, not a starting point — any added line or larger seal pushes the deadline off the first screen. At 320px the names stack (the hero content box is 252px) and the deadline drops below the fold; the nav "Svar" stays visible (Open Question 2). Check widths for every build: 360 × 560, 320 × 568, 180 × 320.

Hero spacing: padding `{spacing.hero-padding-top}` / `{spacing.hero-padding-inline}` / `{spacing.hero-padding-bottom}`; seal margin −4px above, 6px below; illustration 8px below; 8px above the date, the invited line and the deadline line. Cards: padding 20/20/12px (the "Les mer" target supplies the bottom space). Scale is 4-based: `{spacing.1}`–`{spacing.7}`. Text in the hero, cards and RSVP panel is centred; form steps, check page, receipt and admin are left-aligned **[ASSUMPTION — renders only showed the front page]**.

Sections are separated by green showing between panels, which answers inspiration 08's "not one long page on one identical background".

**Admin:** same tokens, denser. Panels use `{spacing.admin-panel-padding}` and `{spacing.admin-gap}`; lists and tables rather than cards; quick tasks (find guest, copy link, see if answered) fit one phone screen (FR-48). When density and targets collide, **44px targets win**; lists scroll.

## Elevation & Depth

Flat. Panels lie directly on the page with **no shadow, no fold, no backing sheet, no loose or torn sheet edge** (PRD addendum *Invitation reveal*; memlog override dropping the layered-sheet card style). Hierarchy comes from the cream-on-green contrast and from typography.

Depth appears in exactly three places:

- **The seal**: a small drop shadow (0 1.5px 1.2px, dark green-black at ~42 %) and faint inner rings, so it reads as pressed wax.
- **The sticky nav bar**: `0 2px 6px rgba(20,24,14,.28)` below it, so content visibly slides under it.
- **Dialogs**: a cream panel over `{colors.scrim}` at 60 %; no shadow **[ASSUMPTION]**.

**Paper texture.** Page and panels carry a fine paper grain: two tiling SVG noise layers (fine grain and soft fibre, inline data-URIs, no network) blended with `overlay` around mid-grey, so the **average colour is unchanged**. On `page-green` the texture is **weakened so every pixel keeps cream text ≥ 4.5:1**: no pixel lighter than `#5F7250` (4.53:1). The renders' green texture does *not* meet this (17 % of pixels under 4.5:1, worst 3.47:1, accessibility review) and must not be copied as-is; production is re-measured on a screenshot against the lightest pixel (memlog, *Technical defaults*). Panel texture is fine as rendered (ink ≥ 7.8:1, `ink-muted` ≥ 4.6:1). The texture is decoration: if it fails to load, the flat token colours are the design.

**Open, to be discussed later (non-blocking):** the couple want to revisit (1) the texture on the green page and (2) the edge treatment of the cream panels (straight vs softer, more paper-like edges, and the corner radius). Until then the weakened green texture and the flat, straight-edged panels above are the working default. Any paper-like edge must still respect the PRD addendum: no folds and no loose-sheet look.

## Shapes

Paper with barely softened corners: `{rounded.sm}` (3px) for panels, fields, notices and tags; `{rounded.md}` (4px) for buttons and checkboxes; `{rounded.full}` only for radio buttons. No pills, no circles for surfaces, no arched or scalloped panel tops.

The **seal** is the one organic shape: an uneven, hand-pressed wax outline (as [inspiration 03](../../ux/inspirasjon/03-Vibe.jpg); the couple wanted a "larger, less perfect" seal than 05), rotated −5°. Canonical outline: the `#seal-shape` symbol in [mockups/front-page-2.html](mockups/front-page-2.html); reuse it, do not redraw.

## Components

Frontmatter key in brackets where one exists.

| Component | Visual spec |
|---|---|
| **Page** [`page`] | `{colors.page-green}` with the weakened paper texture. Never plain white anywhere. |
| **Nav bar** [`nav-bar`, `nav-words`] | Full-width strip on green with the page texture, 52px, shadow below. Nav words left (Program · Praktisk · Stedet · Om oss), `{typography.nav-words}` in `{colors.cream-on-green}`, underlined, 11px apart, each ≥ 44 × 44px; no separator characters; may wrap to two lines; no hamburger. Current page: 2px underline **[ASSUMPTION]**. |
| **Nav "Svar" button** [`nav-svar`] | Right end of the nav bar: `{colors.green-dark}` fill, cream text, **1px `{colors.cream-on-green}` border** (dark green on page-green is only 1.79:1), ≥ 64 × 44px. The one primary-styled control allowed on green. |
| **Hero panel** [`hero-panel`] | Centred. Seal, illustration, names, invites, date, place, invited names, deadline line with the "Svar" link. |
| **Wax seal** [`wax-seal`] | 68px, dark green, uneven edge, cream *R & V* in Imperial Script at 23px. Same artwork, simplified, is the favicon. |
| **Hero illustration** [`hero-illustration`] | [Image 17](../../ux/inspirasjon/17-Illustration.jpg) (cool sage watercolour of the bell house and main house among pines with string lights), cropped to a **150px band** (`object-fit: cover`, `object-position: 50% 58%`) spanning the full panel width, `mix-blend-mode: darken` so its paper melts into the cream (`normal` under forced colours). Final file has no signature or text and ships with the app. Alternatives I5–I8: [mockups/illustration-3.html](mockups/illustration-3.html) (I7 chosen; full-height there, cropped here). |
| **Info card** [`panel`] | `{typography.heading-card}`, two or three lines of `{typography.body}`, then a "Les mer" link whose target covers the whole card. Centred. |
| **Lead-in** [`lead-in`] | One italic line on green, e.g. "Vi gleder oss til å feire med dere!" |
| **RSVP panel** [`rsvp-panel`] | Cream panel after the cards: `heading-card` "Svar på invitasjonen", child-free line ("Barnefritt bryllup – …", placement and text a proposal), deadline line, primary button. When an unsent draft exists, a warning notice sits above the button. |
| **Primary button** [`button-primary`] | Full panel width, 52px, cream text on dark green, 2px transparent border (visible outline in forced colours). Only on cream panels — the nav "Svar" is the one exception. **One distinct primary action per screen; repeats of the same action are allowed** (nav "Svar" and RSVP button). Busy: keeps its colours, label becomes "Sender …". |
| **Secondary button** [`button-secondary`] | Outlined dark green on cream; border 3px on hover/pressed. For "Tilbake", "Betal senere", "Avbryt", "Nei, begynn på nytt". |
| **Destructive button** [`button-destructive`] | Muted rust outline on cream, placed apart (tier 3 only); border 3px on hover/pressed. Filled rust is not used **[ASSUMPTION — "muted rust" read as outline]**. |
| **Focus ring** [`focus-ring`] | 3px outline at 3px offset on `:focus-visible` and on `:active` (tap feedback). Colour by the surface the ring is **painted on**: `focus-on-panel` on cream, `focus-on-green` on green or the footer. Never `outline: none`. |
| **Text link / "Les mer"** [`link-more`] | Inherits text colour, always underlined (1px, 4px offset; 2px on hover/pressed), target ≥ 44px. Never colour alone. |
| **Footer band** [`footer-band`] | Full-bleed `{colors.green-dark}`, cream text, 20px: "Spørsmål? Send oss en melding:", then **each phone number on its own ≥ 44px row** ("Rikke 900 00 000", "Valdemar 900 00 001"), then "Spør oss" and "Personvern" as underlined cream links. |
| **Text field** [`field`] | Field surface, 2px border, label above in `{typography.label}`, hint below in `{typography.body}` *italic* `{colors.ink}`. Error: 3px `{colors.error}` border and the error line (icon + text) between label and field. Variants: multi-line (G10 question, ≥ 4 lines), search (A6), typed confirmation (tier 3). |
| **Choice control** [`choice-control`] | 26px box, 2px ink border; checkbox `{rounded.md}`, radio `{rounded.full}`; selected mark in `{colors.green-dark}` drawn so it survives forced colours (native input with `accent-color`, or a `currentColor` mark — never a background fill alone). Whole row ≥ 44px is the target. |
| **Notice** [`notice`] | 4px left rule, 22px icon and text in the state colour on cream. Icon shapes differ: success = check, warning = circle with "!", error = triangle with "!", info (`ink`) = "i". Error and warning also start with a word ("Feil:", "Obs:" — proposal). Variants: success, warning, error, info; last-updated header (info). |
| **Error summary** | Error notice at the top of the step panel with a heading and linked list of errors. |
| **Status block** | Cream panel shown once answered: sent by/when, total, reported paid, deadline, "Se eller endre svar". Position: Open Question 1 in EXPERIENCE. |
| **Draft offer** | Cream panel at the top of the form: heading «Vil du fortsette der du slapp?», one line saying when the answer was started, primary "Ja, fortsett", secondary "Nei, begynn på nytt". |
| **Progress line** | "Steg 3 av 6: Overnatting" in `{typography.body}`, directly under the step question; no graphic stepper **[ASSUMPTION]**. |
| **Respondent line** | "Jeg er **Sigmund**" with a "Bytt" button styled as an underlined link (≥ 44px), placed after the step question; switching opens a radio list of household members in the panel **[ASSUMPTION]**. |
| **Running total** | Right-aligned "Totalt for husstanden: 1 450 kr", lining figures, `divider` hairline above, at the foot of each paid step. |
| **Read-more disclosure** | Underlined "Les mer om …" with a small chevron; expands in place with a left rule in `{colors.divider}`. |
| **Consent block** | Section at the end of the allergies step, after a `divider`: purpose and recipients text (`body`), how to withdraw, then the Ja/Nei choice under its legend, then — when answering for others — the "Jeg bekrefter …" checkbox. No special colour; nothing pre-selected. |
| **Check-answers list** | Rows per person/part: label left, answer right or below on narrow screens, "Endre" link per part, `divider` between rows, "Ikke oppgitt" in `ink-muted`. |
| **Receipt panel** | Cream panel, success notice at top, Rikke's message in `{typography.body}`, summary, then payment choice. |
| **Payment details** | Cream panel listing amount, Vipps number, account number and payment message as selectable `body` text, each with a secondary "Kopier" button **[ASSUMPTION]**. |
| **Envelope reveal** [If time] | `{colors.page-green}` envelope with the `{colors.green-dark}` wax seal, opening into a **plain** sheet that becomes the hero panel. No heart shape, no lace. "Hopp over" ≥ 44 × 44 on cream or `green-dark`. |
| **Admin nav** | Reuses Nav words on the green page (Oversikt · Gjester · Betalinger · Spørsmål · Innstillinger · Logg ut), **not sticky**, no "Svar" button **[ASSUMPTION]**. |
| **Admin summary row** | `{typography.admin-body}` label and count; count is a link; the hike row shows "kanskje" as its own figure ("5 kommer, 2 kanskje"). `divider` between rows. |
| **Overview table** | A4: on PC a table in a cream panel (`admin-body`, 600-weight header row, `divider` rows); on phone stacked rows that repeat each label as visible text ("Betalt: 900 kr"). Unanswered households sort first and carry the "Ikke svart" tag. |
| **Attention item** | Admin row: reason, household, one action ("Merk som håndtert"); mismatches carry the error icon and "Stemmer ikke". |
| **Undo (in place)** | After a tier-1 action the row is replaced in place by "Merket som håndtert." and an "Angre" link-button. No fixed bar. |
| **Status tag** [`status-tag`] | Outlined label in the state colour, icon as in Notice. Mapping **[ASSUMPTION — proposal]**: "Betalt" → success · "Ikke betalt", "Delbetalt, 300 kr mangler", "Skal ha tilbake 200 kr", "Ikke svart" → warning · "Stemmer ikke" → error · "Ingenting å betale", "Endret" → ink (info). |
| **Dialog** [`dialog`] | Consequence sentence, then actions; on narrow screens buttons stack full-width, safe action first. |

## Do's and Don'ts

| Do | Don't |
|---|---|
| Cream panels on the green page, flat, with paper texture | Shadows, folds, backing sheets on panels (edge treatment itself is still open — see Elevation & Depth) |
| Primary buttons on cream panels; the nav "Svar" (with its cream border) is the only exception | A dark green button on green without the cream border |
| The nav bar is the only thing that sticks | Other sticky or fixed bars, on guest or admin pages |
| Imperial Script for the names (46px, stacking when needed) and the seal | Script for headings, labels, buttons or admin; shrinking the names to fit |
| EB Garamond 20px for guest body text, hints in `ink` | Guest text under 18px; hints in `ink-muted` |
| Warm olive greens (hue ~85–100°) | Bluish sage greens (round 1), neon or saturated greens |
| Cream `#F5EEDF` text on green at 18px or larger, on a texture capped at `#5F7250` | Cream text on the renders' unweakened green texture |
| State colour plus icon shape plus words | Red/green/brown alone to mean anything (WCAG 1.4.1) |
| One illustration (17) in the hero, cropped to 150px | Icons, sprigs, leaves, ornaments sprinkled through the page |
| Venue photos as information on info pages | Venue photos as style or background texture |
| Same tokens in admin, denser, no decoration, 44px targets | Seal, illustration or script on admin working screens |
| A plain sheet in the envelope reveal | A heart-shaped or lace letter |
| Restraint | Gold, metallic, diamonds, glitter, bling, neon, blinking, draping, clutter, luxury-brand feel, Italian or olive-plant motifs |
