# Review resolution 2

How the findings in [review-rubric-2.md](review-rubric-2.md) and [review-accessibility-2.md](review-accessibility-2.md) (2026-11-15) were handled. Summary: [validation-report.md](validation-report.md).

Rikke decided one finding (R2-02: she asked for a render of the household page and approved it, on condition that a household can have one person). The rest were technical or alignment fixes decided by the facilitator with the reasons below, following the rule that pure technical fixes do not need the couple.

Result: 43 fixed, 1 part fixed and part declined, 0 rejected.

| ID | Severity | Outcome | What changed |
|---|---|---|---|
| R2-01 | high | fixed | PRD FR-24 rewritten to the decided placement, with a change-log row. |
| R2-02 | high | fixed | New surface A6a «Legg til / endre husstand», rendered and approved by Rikke (mockups/admin-household-1.html); a household may have one person. |
| R2-03 | medium | fixed | Status block row: placement resolved, content order with gypsophila and «Barnefritt bryllup», id="status". |
| R2-04 | medium | fixed | With A2-06: the hero's «Se svaret» always jumps to the status block; the after-deadline button is «Se hele svaret» (→ G9). |
| R2-05 | medium | fixed | With A2-17: hero line and nav "Svar" specified for both locked states. |
| R2-06 | medium | fixed | OQ13 wording and UJ-4 label corrected. |
| R2-07 | medium | fixed | With A2-14: search on A4, submit-based, result count in a polite live region; A4 empty states added. |
| R2-08 | medium | fixed | With A2-13: typed word is FJERN. |
| R2-09 | medium | fixed | PRD FR-57 rewritten (list + household page) with a change-log row; UJ-4 step 3 reworded. |
| R2-10 | medium | fixed | With A2-05: jump links 44px (`{spacing.target-min}`); renders updated. |
| R2-11 | medium | fixed | answered-1.html and helper-view-1.html promoted to mockups/ and all links updated. The four A/B comparison files (small-phone, plain-names, admin-edge, photo-style) stay in .working/ as decision records. |
| R2-12 | medium | fixed | New `admin-panel` component (frontmatter + row) and `admin-title` 28px token. |
| R2-13 | medium | fixed | G1 gets a plain «Personvern» link under the sheet (FR-66); G12 without a valid link shows the general parts only. Render updated. |
| R2-14 | medium | fixed | Surface coverage extended for A9, G11, G12, A6, A6a. |
| R2-15 | low | fixed | Topic text example. |
| R2-16 | low | fixed | A2 paragraph points to mockups/helper-view-1.html. |
| R2-17 | low | fixed | Settled [ASSUMPTION] tags removed (scrim, dialogs, admin nav, current-page underline); scrim token set to #141A0C as in the approved renders. |
| R2-18 | low | fixed | Small-phone nav values in frontmatter and the Nav "Svar" row. |
| R2-19 | low | fixed | «RSVP sheet» used in both spines; visual-only components noted in Component Patterns. |
| R2-20 | low | fixed | Caption at the paper-ceremony-5 citation. |
| R2-21 | low | fixed | Front-page item 4 names 12-Us1 and its crop. |
| R2-22 | low | fixed | Unused `panel-gap` and `panel-padding` removed. |
| R2-23 | low | fixed | Example date inside the answering window. |
| R2-24 | low | fixed | Info page row, Navigation (G12) and a G12 jump-link microcopy row. |
| R2-25 | low | fixed | «Se betalingene» → the household's payment page. |
| R2-26 | low | fixed | Primary for the guest's withdrawal stated as deliberate. |
| R2-27 | low | fixed | One microcopy row maps the three refund phrasings to their places. |
| A2-01 | high | fixed | Narrow widths: timeline one-sided below about 260px. |
| A2-02 | high | fixed | Narrow widths: images max-width 100 %, topic rows stack below about 300px. |
| A2-03 | high | fixed | Dialog: on confirm, focus moves to the result message (role=status, tabindex=-1). |
| A2-04 | medium | fixed | Admin page is flat page-green (no texture); admin renders updated. |
| A2-05 | medium | fixed | See R2-10. |
| A2-06 | medium | fixed | See R2-04. |
| A2-07 | medium | fixed | Forced colours: 1px CanvasText border on sheets, admin panels and dialogs (DESIGN + Accessibility Floor). |
| A2-08 | low | fixed | Jump and «Svar» targets get tabindex=-1. |
| A2-09 | low | fixed by rewording | Programme times stay 18px semibold (Rikke approved the look); the `small` rule now names them. |
| A2-10 | low | fixed | «Godt å vite» is an h3. |
| A2-11 | low | fixed | Decorative · and ← are aria-hidden (new Component Patterns row). |
| A2-12 | low | part fixed, part declined | (2) each balanced line is its own list, so a dot never starts a line. (1) declined: the plain small-caps jump links are the look Rikke chose after two rejected rounds; they are a shortcut, and every part is also reached by scrolling. |
| A2-13 | low | fixed | See R2-08. |
| A2-14 | low | fixed | See R2-07. |
| A2-15 | low | fixed | «Angre» on an older payment is tier 2 (dialog). |
| A2-16 | low | fixed | The consent text keeps its FR-66 link; «Tilbake» from G12 returns to the same step with the answers kept (FR-78 draft). |
| A2-17 | low | fixed | See R2-05. |
