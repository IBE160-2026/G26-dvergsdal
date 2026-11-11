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
    lineHeight: '1.2'
  monogram:
    fontFamily: 'Imperial Script'
    fontSize: 32px
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
    lineHeight: '1.35'
  lead-in:
    fontFamily: 'EB Garamond'
    fontSize: 23px
    fontWeight: '400'
    lineHeight: '1.4'
  invites:
    fontFamily: 'EB Garamond'
    fontSize: 21px
    fontWeight: '400'
    lineHeight: '1.5'
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
  none: 0px
  sm: 3px
  md: 4px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 20px
  '6': 24px
  '7': 32px
  gutter: 16px
  panel-gap: 16px
  panel-padding: 20px
  hero-padding-block: 30px
  hero-padding-inline: 18px
  admin-panel-padding: 12px
  admin-gap: 8px
  content-max: 480px
  target-min: 44px
  button-height: 52px
components:
  page:
    background: '{colors.page-green}'
    texture: 'paper-grain, zero average colour shift'
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
    padding: '{spacing.hero-padding-block} {spacing.hero-padding-inline}'
  wax-seal:
    fill: '{colors.seal}'
    foreground: '{colors.cream-on-green}'
    size: 96px
    rotate: -5deg
    typography: '{typography.monogram}'
  hero-illustration:
    width: '100%'
    blend: 'mix-blend-mode: darken'
  button-primary:
    background: '{colors.green-dark}'
    foreground: '{colors.cream-on-green}'
    hover: '{colors.green-dark-hover}'
    radius: '{rounded.md}'
    minHeight: '{spacing.button-height}'
    typography: '{typography.button}'
  button-secondary:
    background: '{colors.panel-cream}'
    foreground: '{colors.green-dark}'
    border: '1.5px solid {colors.green-dark}'
    radius: '{rounded.md}'
    minHeight: '{spacing.target-min}'
  button-destructive:
    background: '{colors.panel-cream}'
    foreground: '{colors.error}'
    border: '1.5px solid {colors.error}'
    radius: '{rounded.md}'
    minHeight: '{spacing.target-min}'
  link-more:
    foreground: 'inherit'
    underline: '1px, offset 4px'
    minHeight: '{spacing.target-min}'
  nav-words:
    foreground: '{colors.cream-on-green}'
    typography: '{typography.body}'
    minHeight: '{spacing.target-min}'
  lead-in:
    foreground: '{colors.cream-on-green}'
    typography: '{typography.lead-in}'
  footer-band:
    background: '{colors.green-dark}'
    foreground: '{colors.cream-on-green}'
  field:
    background: '{colors.field-surface}'
    foreground: '{colors.ink}'
    border: '2px solid {colors.field-border}'
    radius: '{rounded.sm}'
    minHeight: '{spacing.target-min}'
  choice-control:
    box: 26px
    border: '2px solid {colors.ink}'
    selected: '{colors.green-dark}'
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

> Visual identity for the guest invitation and the couple's admin area. Behaviour, states and flows live in [EXPERIENCE.md](EXPERIENCE.md). Decisions are logged in [.memlog.md](.memlog.md); requirements in the [PRD](../../prds/prd-aill-handle-it-2026-11-07/prd.md) and its [addendum](../../prds/prd-aill-handle-it-2026-11-07/addendum.md). Supporting renders: [mockups/color-themes-5.html](mockups/color-themes-5.html), [mockups/typography-1.html](mockups/typography-1.html), [mockups/illustration-3.html](mockups/illustration-3.html). **The spines win on any conflict with a render.**

## Brand & Style

The site **is** the invitation. A guest opening their link should think what Rikke and Valdemar said in the brain dump: *"wow, what a lovely invitation, and so easy to get an overview"* and *"wow, so cosy! I want to be part of this."* The posture is a printed wedding card from a timber farmhouse in Hardanger: classic, clean, slightly old-fashioned, warm. Nature and elegance with historic wooden-building character, never luxury.

The visual language follows from that:

- **An envelope-coloured page with cream sheets on it.** Olive-green textured page, flat cream panels carrying the content (direction B *Konvolutten*, about half green, half cream).
- **A hand-pressed wax seal** in dark green with *R & V*, at the top of the invitation and as the browser-tab icon.
- **One script moment.** The couple's first names in a formal copperplate-style script; everything else in a book serif that reads like a printed invitation.
- **One illustration.** A soft sage watercolour of Hardingasete in the top panel.
- **Real paper, not a hint of it.** Visible paper texture on page and panels, tuned so it never changes the colours.

What it is not: gold, diamonds, metallic, glitter, neon, blinking or animated noise, clutter, luxury-brand gloss, draping, heart-shaped or lace letters, bluish "sage" greens. The guest list spans everyone from teenagers to bestefar Sigmund (78), so restraint and legibility outrank decoration everywhere.

**Light only.** There is no dark mode; the invitation looks the same at all times (memlog, decision D).

## Colors

The palette was chosen over six render rounds from colours sampled in the couple's own inspiration images, then tuned by their perception (memlog, *Page green FINAL*). Final pick: page **G4a**, panel **K1 havre**, text **T2**.

| Token | Hex | Role | Never |
|---|---|---|---|
| `page-green` | `#5A6C48` | The page behind everything: a warm, slightly less yellow olive (G4a, hue ~90°). | Text on cream; button fill (it is only 1.79:1 against `green-dark`). |
| `green-dark` | `#344628` | Primary button fill, footer band, focus ring on panels. | A page background (round 6 dark page rejected). |
| `green-dark-hover` | `#2C3A20` | Primary button hover/pressed. Derived in the typography render for the earlier dark green; still 10.49:1 with cream text. | Anything but the pressed button. |
| `seal` | `#344628` | Wax seal body. Same value as `green-dark`, separate token so the seal can be tuned alone. | — |
| `panel-cream` | `#EBE4D5` | All content panels ("havre"). | Large areas without texture. |
| `ink` | `#3B372F` | All text and headings inside panels, including the names (T2 warm grey, chosen over dark green and walnut). | Text on green. |
| `ink-muted` | `#5E594F` | Hints, example labels, timestamps, "Ikke oppgitt". From the round-3 render. | Body copy, anything the guest must read to act. |
| `cream-on-green` | `#F5EEDF` | Text, links and focus ring on `page-green` and `green-dark`. | Panel background. |
| `field-surface` | `#F7F2E7` | Inside text fields, so fields read as "write here" on the panel. From the typography render. | Panels. |
| `field-border` | `#5E594F` | Text-field and select outline (5.50:1 against the panel, 6.23:1 against the field). From the typography render. | Decorative rules. |
| `divider` | `#C8BFAE` | 1px hairlines between admin rows and check-answer rows. **[ASSUMPTION]** no render defined a hairline; dividers never carry meaning on their own. | Field outlines, focus. |
| `focus-on-panel` | `#344628` | 3px focus ring on cream. | — |
| `focus-on-green` | `#F5EEDF` | 3px focus ring on green and in the footer band. | — |
| `error` | `#7C3B1D` | Errors, tier-3 destructive actions, "Stemmer ikke" (mismatch). Sampled from the rust wax seal in inspiration 01. | Decoration; the only signal of an error (always with text and icon). |
| `success` | `#3D5A2A` | "Svaret er sendt", saved confirmations. Renderer's own value (rounds 2–3), not chosen by the couple. | Primary buttons. |
| `warning` | `#765012` | "Ikke sendt ennå", allergy-without-consent warning, conflict notice. Renderer's own value (round 2), not chosen by the couple. | Errors. |
| `scrim` | `#344628` | Behind admin dialogs, at 60 % opacity **[ASSUMPTION]**. | Guest pages except the in-form leave warning. |

**Dark wood** from the brief has no UI token: walnut text (T3) was rejected, so dark wood lives only in photographs of the venue and in the illustration **[ASSUMPTION]**.

### Contrast pairs (WCAG 2.x, all text ≥ 4.5:1 — NFR-5)

| Pair | Ratio | Use |
|---|---|---|
| `ink` on `panel-cream` | 9.35:1 | All panel text |
| `ink` on `field-surface` | 10.61:1 | Typed text |
| `ink-muted` on `panel-cream` | 5.50:1 | Hints, meta |
| `green-dark` on `panel-cream` | 8.08:1 | Secondary button text, focus ring |
| `cream-on-green` on `page-green` | **4.95:1** | Lead-in, nav words — the lowest text pair; never set it smaller than `{typography.body}` |
| `cream-on-green` on `green-dark` | 8.86:1 | Buttons, seal monogram, footer |
| `cream-on-green` on `green-dark-hover` | 10.49:1 | Pressed button |
| `error` on `panel-cream` | 6.64:1 | Error text, destructive button |
| `success` on `panel-cream` | 6.16:1 | Success notice |
| `warning` on `panel-cream` | 5.67:1 | Warning notice |
| `field-border` vs `panel-cream` | 5.50:1 | Non-text, ≥ 3:1 required |
| `panel-cream` vs `page-green` | 4.52:1 | Panel edge against page (non-text) |

The PRD addendum asks to check "sage green on soft white": green is never text on cream here; the green-on-cream pair in use is `green-dark` on `panel-cream` at 8.08:1.

## Typography

Two self-hosted families, both SIL Open Font License, served from our own server as WOFF2 with Latin subsets including æ, ø, å (PRD 3.2: guest pages load nothing from other companies). The Google Fonts links in the renders are a planning-mock exception only.

- **Imperial Script** — the couple's first names (*Rikke & Valdemar*, first names only, no surnames) and the *R & V* seal monogram. Chosen for closeness to the names in inspiration 09: large decorative capitals, connected lowercase, moderate loops. Its upstrokes are hair-thin, so it is **display only, never below `{typography.monogram}` (32px)**, never for headings, labels, buttons or the admin area. Names sit on one line at `{typography.display-names}` and shrink to fit at 320px rather than wrap. Fallback: Georgia italic **[ASSUMPTION]**.
- **EB Garamond** — everything else. Its short x-height (0.41) is why guest body text is **20px**, above the NFR-5 floor of 18px, so bestefar Sigmund can read it (memlog, *Body font*). Regular and italic; weight 600 for labels and emphasis such as the invited names **[ASSUMPTION — the render used bold; 600 is the nearest available weight to load]**. Fallback: Georgia.

| Role | Token | Where |
|---|---|---|
| Names | `display-names` | Hero panel only |
| Seal | `monogram` | Seal and favicon |
| Page title | `heading-page` | Info pages, form step question, receipt heading **[ASSUMPTION — size not rendered]** |
| Card heading | `heading-card` | "Programmet", "Praktisk informasjon", etc. |
| Date | `date-line` | "Lørdag 27. mai 2028" in the hero |
| Lead-in | `lead-in`, *italic* | One line on green between hero and cards |
| Invites line | `invites`, *italic* | "inviterer deg til bryllup" |
| Buttons | `button` | All guest buttons |
| Body | `body` | All guest running text |
| Labels | `label` | Form labels and legends |
| Small | `small` | Hints, example text, footer meta — the 18px floor; nothing on guest pages is smaller |
| Admin | `admin-heading`, `admin-body` | Admin working screens **[ASSUMPTION — denser, 18px body]** |

Figures: amounts, dates, times and phone numbers use lining figures, and tables use tabular figures (EB Garamond defaults to old-style figures) **[ASSUMPTION]**. No all-caps, no letter-spaced small caps (the small-caps card style was explicitly not decided).

## Layout & Spacing

Phone first (NFR-6). One centred column, maximum `{spacing.content-max}`; a PC shows the same phone column on the green page **[ASSUMPTION — 480px max]**. Side gutter `{spacing.gutter}`. No horizontal scroll at 320px or at 200 % zoom (NFR-5).

Front-page order (PRD addendum *Front page structure*, memlog *Hero panel order*):

1. Nav words on green (wrap to two lines on narrow screens).
2. **Hero panel**: seal → illustration → names → invites line → date → place → "Invitert: …" → "Barnefritt bryllup" → deadline → primary button.
3. Lead-in line on green.
4. Four info cards, `{spacing.panel-gap}` apart (Gifts as a fifth only if built).
5. The RSVP button again, in **its own cream panel** — primary buttons always sit on cream panels (memlog, round 6 finding).
6. Footer band, full-bleed `green-dark`.

Scale is 4-based: `{spacing.1}`–`{spacing.7}`. Panel interiors `{spacing.panel-padding}`; hero `{spacing.hero-padding-block}` × `{spacing.hero-padding-inline}`. Text in the hero and cards is centred; form steps, check page, receipt and admin are left-aligned **[ASSUMPTION — renders only showed the front page centred]**.

Sections are separated by green showing between panels, which answers inspiration 08's "not one long page on one identical background".

**Admin:** same tokens, denser. Panels use `{spacing.admin-panel-padding}` and `{spacing.admin-gap}`; lists and tables rather than cards; quick tasks (find guest, copy link, see if answered) fit one phone screen (FR-48).

## Elevation & Depth

Flat. Panels lie directly on the page with **no shadow, no fold, no backing sheet, no loose or torn sheet edge** (PRD addendum *Invitation reveal*: once unfolded "there are no folds and no sheet edges"; memlog override dropping the layered-sheet card style). Hierarchy comes from the cream-on-green contrast and from typography.

Depth appears in exactly two places:

- **The seal**: a small drop shadow (about 0 1.5px 1.2px, dark green-black at ~40 %) and faint inner rings, so it reads as pressed wax.
- **Admin dialogs**: a cream panel over `{colors.scrim}` at 60 %; still no shadow **[ASSUMPTION]**.

**Paper texture.** Both the page and the panels carry a fine paper grain: two tiling SVG noise layers (a fine grain and a soft fibre, inline data-URIs, no network) blended with `overlay` around mid-grey, so the **average colour is unchanged**. Round 2's texture darkened cream by ~4 lightness points and was part of why the couple found the cream "too dark"; any production texture must be re-checked for zero colour shift. The texture is decoration: if it fails to load, the flat token colours are the design.

**Open, to be discussed later (non-blocking):** the couple want to revisit (1) the texture on the green page and (2) the edge treatment of the cream panels (straight vs softer, more paper-like edges, and the corner radius). Until then the renders' texture and the flat, straight-edged panels above are the working default. Any paper-like edge must still respect the PRD addendum: no folds and no loose-sheet look.

## Shapes

Paper with barely softened corners: `{rounded.sm}` (3px) for panels, fields, notices and tags; `{rounded.md}` (4px) for buttons and choice boxes. No pills, no circles for surfaces, no arched or scalloped panel tops.

The **seal** is the one organic shape: an uneven, hand-pressed wax outline (as inspiration 03; the couple wanted a "larger, less perfect" seal than 05), rotated −5°. The outline path is in the renders (`#seal-shape`) and should be reused, not redrawn.

## Components

| Component | Visual spec |
|---|---|
| **Page** | `{colors.page-green}` with paper texture. Never plain white anywhere. |
| **Nav words** | A row of short words on green above the hero (e.g. Program · Praktisk · Stedet · Om oss · Svar), `{typography.body}` in `{colors.cream-on-green}`, underlined, each ≥ `{spacing.target-min}` tall, middle-dot separators; wraps to two lines; no hamburger icon. Current page: thicker underline **[ASSUMPTION]**. |
| **Hero panel** | `{components.hero-panel}`, centred. Contains seal, illustration, names, details, deadline and the primary button. |
| **Wax seal** | `{components.wax-seal}`: 96px, dark green, uneven edge, cream *R & V* in Imperial Script. Same artwork, simplified, is the favicon. |
| **Hero illustration** | Image 17 (cool sage watercolour of the bell house and main house among pines with string lights), full panel width, `mix-blend-mode: darken` so its paper melts into the cream, `{spacing.3}` below. Final file must contain no signature or text. Shipped with the app, not hot-linked from planning folders. |
| **Info card** | `{components.panel}` with `{typography.heading-card}`, two or three lines of `{typography.body}`, then a "Les mer" link. Centred. |
| **Lead-in** | One italic line on green, e.g. "Vi gleder oss til å feire med dere!" |
| **Primary button** | `{components.button-primary}`: full panel width, 52px tall, cream text on dark green. Only on cream panels. One per screen. |
| **Secondary button** | `{components.button-secondary}`: outlined dark green on cream. For "Tilbake", "Betal senere", "Avbryt". |
| **Destructive button** | `{components.button-destructive}`: muted rust outline on cream, placed apart from other actions (tier 3 only). Filled rust is not used **[ASSUMPTION — "muted rust" read as outline]**. |
| **Text link / "Les mer"** | Inherits text colour, always underlined (1px, 4px offset), hit area ≥ 44px. Links are never distinguished by colour alone. |
| **Footer band** | Full-bleed `{colors.green-dark}`, cream text: "Spørsmål? Send oss en melding:", both phone numbers, "Spør oss" and "Personvern" as underlined cream links. |
| **Text field** | `{components.field}`: field surface, 2px border, label above in `{typography.label}`, hint below in `{typography.small}` `{colors.ink-muted}`. |
| **Choice control** | `{components.choice-control}`: 26px box (square for checkbox, round for radio), 2px ink border; selected = `{colors.green-dark}` fill with cream mark **[ASSUMPTION]**. Whole row is the target, ≥ 44px. |
| **Notice** | `{components.notice}`: 4px left rule and 22px icon in the state colour, text in that colour on cream. Variants: success, warning, error, info (`ink`). |
| **Error summary** | A notice (error) at the top of the step panel with a heading and linked list of errors. |
| **Status block** | A cream panel near the top of the front page once answered: sent by/when, total, reported paid, deadline, and the "Se eller endre svar" primary button. |
| **Progress line** | Plain text "Steg 2 av 6" in `{typography.small}` above the step question; no graphic stepper **[ASSUMPTION]**. |
| **Respondent line** | One line at the top of every form step: "Jeg er **Sigmund**" with an underlined "Bytt" link; switching opens a radio list of household members inside the panel **[ASSUMPTION]**. |
| **Running total** | A right-aligned line "Totalt for husstanden: 1 450 kr" with lining figures, `divider` hairline above, at the foot of each paid step. |
| **Read-more disclosure** | Underlined "Les mer om …" with a small chevron; expands in place inside the panel with a left rule in `{colors.divider}`. |
| **Check-answers list** | Rows per person/part: label left, answer right or below on narrow screens, "Endre" link per part, `divider` between rows, "Ikke oppgitt" in `ink-muted`. |
| **Receipt panel** | Cream panel, success notice at top, Rikke's message in `{typography.body}`, summary, then payment choice. |
| **Payment details** | Cream panel listing amount, Vipps number, account number and payment message, each on its own line with a secondary "Kopier" button **[ASSUMPTION]**. |
| **Envelope reveal** [If time] | Green envelope with the same wax seal opening into a **plain** sheet that becomes the hero panel. No heart shape, no lace. |
| **Admin summary row** | `{typography.admin-body}` label and count; count is a link. Compact, left-aligned, `divider` between rows. |
| **Attention item** | Admin row: reason, household, one action ("Merk som håndtert"); mismatches carry the error icon and the word "Stemmer ikke". |
| **Status tag** | `{components.status-tag}`: outlined text label in the state colour (payment status, "Endret"). Never colour alone. |
| **Dialog** | `{components.dialog}`: consequence sentence, then actions right-aligned, safest action first. |
| **Undo bar** | A cream panel strip at the bottom of the admin viewport: "Merket som håndtert. Angre". |

## Do's and Don'ts

| Do | Don't |
|---|---|
| Cream panels on the green page, flat, with paper texture | Shadows, folds, backing sheets on panels (edge treatment itself is still open — see Elevation & Depth) |
| Primary buttons on cream panels only | A dark green button on a green background |
| Imperial Script for the names and seal, large | Script for headings, labels, buttons, admin or anything under 32px |
| EB Garamond 20px for guest body text | Guest text under 18px anywhere |
| Warm olive greens (hue ~85–100°) | Bluish sage greens (round 1), neon or saturated greens |
| Cream `#F5EEDF` text on green at body size or larger | Small or thin cream text on `page-green` (4.95:1 has no headroom) |
| State colour plus text plus icon | Red/green alone to mean anything (WCAG 1.4.1) |
| One illustration (17) in the hero | Icons, sprigs, leaves, ornaments sprinkled through the page |
| Venue photos as information on info pages | Venue photos as style or background texture |
| Same tokens in admin, denser, no decoration | Seal, illustration or script on admin working screens |
| A plain sheet in the envelope reveal | A heart-shaped or lace letter |
| Restraint | Gold, metallic, diamonds, glitter, bling, neon, blinking, draping, clutter, luxury-brand feel, Italian or olive-plant motifs |
