---
title: "Review resolution: AI'll handle it UX spines"
updated: 2026-11-11
inputs: review-rubric.md, review-accessibility.md, .memlog.md (entries after the review)
---

# Review resolution

Every finding in [review-rubric.md](review-rubric.md) (R) and [review-accessibility.md](review-accessibility.md) (A), numbered in the order they appear. "OQ n" = Open Question n in [EXPERIENCE.md](EXPERIENCE.md). D = DESIGN.md, E = EXPERIENCE.md.

**Totals (55):** fixed 52 (two of them with a part deferred to an Open Question), deferred 3, rejected 0. Two fixed findings had one suggested remedy rejected in favour of another (A11, A13; reasons in the table).

## Rubric walker (R)

| # | Finding | Sev. | Outcome | Where |
|---|---|---|---|---|
| R1 | Hero content does not fit above the fold (FR-7) | high | fixed — new front page (memlog *Front page redesign*); measured 553px < 560px fold. Residual 320px case → OQ2 | D › Layout & Spacing (first-screen budget); E › Component Patterns › Hero panel; E › UJ-1 step 1 |
| R2 | FR-18 arrival step has no position | high | fixed — no arrival question (FR-18 removed in PRD) | E › Interaction Primitives › Form step order |
| R3 | FR-14 read as one step instead of two | medium | fixed — two screens per PRD FR-14; progress example "Steg 3 av 6: Overnatting" | E › Form step order; D › Components › Progress line |
| R4 | UJ-2 refund coda has no flow beat | low | fixed | E › UJ-2 step 8; UJ-5 step 5 |
| R5 | Focus ring merges with primary button | medium | fixed — `focus-width`/`focus-offset` 3px, ring colour by painted surface | D frontmatter `focus-ring`; D › Components › Focus ring |
| R6 | Status tags have no status → colour mapping | medium | fixed (mapping marked as proposal) | D › Components › Status tag |
| R7 | No busy or hover tokens | low | fixed | D frontmatter buttons/links; D › Components › Primary/Secondary/Destructive button |
| R8 | `rounded.none` unused; choice-control radius missing | low | fixed — `none` removed, `full` added for radios | D frontmatter `rounded`, `choice-control`; D › Shapes |
| R9 | "One primary per screen" conflicts with G2 | medium | fixed — "one distinct primary action; repeats allowed". Which element carries "Se eller endre svar" once answered → OQ1 | D › Components › Primary button; E › Component Patterns › Primary button |
| R10 | Consent block has no component row | medium | fixed | D › Components › Consent block; E › Component Patterns › Consent block |
| R11 | No component for A4 overview or admin nav | medium | fixed | D › Components › Overview table, Admin nav; E › Component Patterns |
| R12 | Last-updated header, typed confirmation, multi-line and search fields unnamed | low | fixed — Notice and Text field variants | D › Components › Text field, Notice; E › Component Patterns › Text field |
| R13 | Status block position on G2 unstated | medium | deferred → OQ1 (needs the couple; the new front page leaves no room above the deadline line) | E › Open Questions 1 |
| R14 | No failure state for "Kopier" | low | fixed | E › State Patterns › Copy unavailable / failed |
| R15 | Admin loading unstated | low | fixed | E › State Patterns › Loading |
| R16 | Image 17 and seal source not linked | medium | fixed — image linked; canonical `#seal-shape` in mockups/front-page-2.html | D › Components › Hero illustration; D › Shapes |
| R17 | Render links only in DESIGN header | low | fixed — renders linked in Colors, Typography, Layout, Shapes, Components with captions; images 03, 09, 17 linked | D throughout |
| R18 | Final type pairing never rendered | low | fixed — mockups/front-page-2.html shows S4 + B1@20 + I7 + G4a/K1/T2 | D › Typography, Layout & Spacing |
| R19 | Consent & Privacy UX restates FRs | low | fixed — UX decisions only, FRs cited | E › Consent & Privacy UX |
| R20 | Surface coverage is a run-on line | low | fixed — table | E › State Patterns › Surface coverage |
| R21 | Struck items in Open Questions; hike "kanskje" only there | low | fixed — struck items dropped; "kanskje" in body | E › Component Patterns › Admin summary row; D › Components › Admin summary row; E › UJ-4 |
| R22 | Example deadline weekday wrong | low | fixed — "onsdag 1. desember" | E › State Patterns › Locked; Voice and Tone; UJ-1 |
| R23 | Frontmatter component keys drift from table names | low | fixed — key shown per row | D › Components |
| R24 | EXPERIENCE frontmatter lacks `name` | low | fixed | E frontmatter |
| R25 | G4b listed as a surface | low | fixed — now states of G4 | E › IA (G4 row); State Patterns › Last updated, Conflict |

## Accessibility reviewer (A)

| # | Finding | Sev. | Outcome | Where |
|---|---|---|---|---|
| A1 | Unsent answer lost on reload/timeout | critical | fixed — FR-78 moved to tier 1: draft kept on the device (per PRD, not server-side), "Vil du fortsette der du slapp?" offer, no guest time limit loses input. Draft content privacy → OQ6 | E › Interaction Primitives › Unsent answer kept; State Patterns; UJ-1 failure path |
| A2 | Paper texture drops cream-on-green below 4.5:1 | high | fixed — texture capped so no pixel is lighter than `#5F7250` (4.53:1); lightest-pixel rule | D › Colors › Contrast pairs; D › Elevation & Depth |
| A3 | "Everything above the fold" is false | high | fixed — new front page measured at 360 × 560; UJ-1 step 1 rewritten. 320px residual → OQ2 | D › Layout & Spacing; E › Hero panel; E › UJ-1 |
| A4 | Reflow rules break at 200 % zoom | high | fixed — names stack (no shrink-to-fit, no `cqi`), `rem`, hyphenation, 180 × 320 check width, 8px gutters below 260px; measured "Valdemar" 136px fits | D › Typography; D › Layout & Spacing; E › Accessibility Floor; E › Responsive & Platform |
| A5 | Hints in `ink-muted` at `small` | medium | fixed — hints in `ink` at `body` italic; `small`/`ink-muted` only for non-actionable text | D › Colors; D › Typography; D › Components › Text field |
| A6 | Focus visibility depends on unspecified offset | medium | fixed | D › Components › Focus ring; E › Accessibility Floor |
| A7 | Field error, hint and consent semantics undefined | medium | fixed | D › Components › Text field; E › Component Patterns › Text field, Choice control, Consent block |
| A8 | Feedback planned as single-page app; identical titles | medium | fixed — focus on load, per-step titles, live regions for in-page changes only | E › Accessibility Floor; Component Patterns › Error summary, Notice; Voice and Tone |
| A9 | "Steg n av m" moves under the guest | medium | fixed — m changes only when who-comes/days answers change; step name shown; body size | E › Component Patterns › Progress line; D › Components › Progress line |
| A10 | Browser Back on POST steps | medium | fixed — each step its own address, Back always safe | E › Interaction Primitives |
| A11 | Nav-word row semantics and wayfinding | medium | fixed — `<nav>` + list, no separator characters, ≥ 44px targets. Rejected parts: renaming "Svar" (the couple chose "Svar" for the nav button and deadline link) and an extra "Invitasjonen" word on G3 (FR-11 back links cover it; it would force the bar onto two lines) | D › Components › Nav bar; E › Component Patterns › Nav bar |
| A12 | Names only in hairline script; no `h1` | medium | fixed in part — heading outline (`h1` = names, `h2` per card). Plain-text names → OQ3 (couple's taste) | E › Accessibility Floor; D › Typography table |
| A13 | Forced colours break illustration, choices, buttons | medium | fixed — blend off under forced colours, choice marks in `currentColor`/native, 2px transparent button border. Baking the panel colour into the JPG rejected: it would show a flat block against the textured panel | D › Components; E › Accessibility Floor |
| A14 | "Light only" has no mechanism | medium | fixed — `color-scheme: light only`, Samsung Internet check | D › Brand & Style; E › Foundation |
| A15 | State colours indistinguishable | medium | fixed — distinct icon shapes, word prefixes, "Ikke svart" tag and sort | D › Colors; D › Components › Notice, Status tag, Overview table |
| A16 | Undo bar timing, focus, obscuring | medium | fixed — undo in place, no timer, focus to "Angre", "Vis håndterte"; no fixed bars | D › Components › Undo (in place); E › Component Patterns; Admin protection tiers |
| A17 | Admin session expiry loses input | medium | deferred → OQ5 (architecture) | E › Open Questions 5 |
| A18 | Dialog behaviour underspecified | medium | fixed | E › Component Patterns › Dialog; D › Components › Dialog; Voice and Tone (leave warning) |
| A19 | Identical, fragile "Kopier" buttons | medium | fixed | E › Component Patterns › Payment details; Voice and Tone |
| A20 | Footer phone numbers too close | medium | fixed — each number its own ≥ 44px `tel:` row | D › Components › Footer band; E › Component Patterns › Footer band |
| A21 | Guest pages depend on JS in v1 | medium | deferred → OQ4 (PRD 3.2 scope / architecture) | E › Open Questions 4; Responsive & Platform |
| A22 | Illustration alt too long | low | fixed — «Akvarell av tunet på Hardingasete.» | E › Component Patterns › Hero illustration |
| A23 | Seal text read aloud | low | fixed — container `aria-hidden` | E › Component Patterns › Wax seal |
| A24 | Four identical "Les mer"; card not a target | low | fixed — whole card is the link's hit area | D › Components › Info card; E › Component Patterns › Info card |
| A25 | "Bytt" is a state-changing link | low | fixed — button, accessible name, after the question | D › Components › Respondent line; E › Component Patterns |
| A26 | No visible tap feedback | low | fixed — ring on `:active`, thicker borders/underlines | D › Components › Focus ring, buttons, links |
| A27 | Lining figures only an assumption | low | fixed — requirement; `lnum`/`tnum` kept in subset; non-breaking space | D › Typography |
| A28 | Typed confirmation fights phone keyboards | low | fixed | E › Admin protection tiers (tier 3) |
| A29 | Envelope reveal needs more than reduce-motion | low | fixed — acceptance list | E › Envelope reveal; D › Components › Envelope reveal |
| A30 | Admin density vs targets | low | fixed — 44px targets win; stacked rows repeat labels | D › Layout & Spacing; D › Components › Overview table |
