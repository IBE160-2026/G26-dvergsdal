# Addendum: PRD for AI'll handle it

This addendum keeps the detail from the PRD discussion that belongs in later documents, the UX spec and the architecture, rather than in the PRD itself. It also records the alternatives that were rejected, and why.

## For UX (bmad-ux)

### Invitation reveal (UJ-1, Rikke, 2026-11-07)

- The guest first sees a green envelope sealed with a wax-style stamp reading "R & V".
- The envelope opens and unfolds into an invitation, and the unfolded invitation **is** the website.
- Once it has unfolded, the envelope and the paper outline disappear. There are no folds and no sheet edges, only the content in the same visual style.
- The invitation says that Rikke and Valdemar are getting married on Saturday 27 May 2028 and that the named guests are invited.
- The guest should feel invited to scroll down for more information.
- The animation is If time. The static invitation look is Must and has to work well on its own.

### Front page structure (agreed 2026-11-07)

1. **Top:** the invitation, with the RSVP button visible without scrolling.
2. **Below:** short cards with two or three lines each and "Read more":
   - Programme
   - Practical information
   - Hardingasete and the area
   - About us
   - Gifts (if time)
3. **Bottom:** the RSVP button again.

### Rikke's own wording for the receipt (Norwegian original)

Use this as the starting point for the final text:

- **Coming:** «Tusen takk for at du tok deg tiden til å svare, vi gleder oss til å feire den store dagen med deg/dere»
- **Not coming:** «Så leit at du/dere ikke har mulighet til å delta, men dette har vi full forståelse for.»
- **Both end with:** «Du kan nå trygt lukke siden/invitasjonen»

### Invitation message for sending links (FR-52)

Rikke wants the message to be warmer and cosier than Claude's first example ("Hei Sigmund! Her er invitasjonen til bryllupet vårt: [lenke]"). It must include the guest's first name so the couple can see that the right link goes to the right person. The exact wording is set in the UX phase.

### Tone

Warm and "koselig" throughout, including error messages. Every screen should have one obvious next step for older guests.

### "Needs attention" behaviour

| Item | Leaves the list when |
|---|---|
| Household not answered | The household answers, or the couple marks it as handled |
| Unanswered question | The couple marks it as answered |
| "I have paid" without a matching payment (red) | A matching amount is registered, or the couple marks it as handled |
| Refund owed | The refund is registered |
| Household marked "Changed" | The couple marks it as seen |

### Payment status (FR-60)

| Amount received | Status shown |
|---|---|
| 0 kr | Not paid |
| Less than the total | Part paid, X kr missing |
| Exactly the total | Paid |
| More than the total | Refund owed, X kr |

## For architecture (bmad-architecture)

- **D14.** Store link codes hashed or in plain form. Hashed codes mean the couple can't look up an existing link; they can only create a new one. That conflicts with FR-51 (copy the guest's link) unless the code can be shown again. Weigh this against [R 4.1].
- **D15.** The database and technology stack. The research recommends SQLite for clone-and-run (NFR-8) [R 4.4].
- **Two admin roles (FR-46).** The server must stop helpers from changing data, not just the page.
- **Server-calculated values (NFR-2).** Totals and payment statuses are always calculated, never stored. The research gives security detail for admin login [R 4.2].
- **Change marker and history (FR-39, FR-40).** v1 needs the "Changed" marker and "last updated by X at Y". The full history may come in 2027, but the data model should allow it from the start.

## Rejected alternatives

| Alternative | Decision | Why |
|---|---|---|
| One link per household (assumed in the research [R 5]) | Rejected | One link per guest lets the site know who is answering (WCAG 3.3.7), and deactivating a link affects only that person. |
| "Everyone is coming" ticked in advance | Rejected | Older guests who skim would sign up people who aren't coming, which gives wrong numbers and totals. |
| Payment as two states, paid or not paid (D6) | Replaced | Rikke needs "part paid". A status calculated from amounts can't drift away from the money actually received. |
| Email to the couple when an answer changes | Dropped | The "Changed" marker and "Needs attention" are enough. |
| Guests can request their own link ("send me my link") | Rejected | The site would have to send email or SMS. The couple resends links by hand. |
| Importing the guest list from Excel | Not needed | The couple enters about 35 households by hand. |
| Cabin and bed allocation on the site | Out | The couple does it outside the site. |
| A bed limit in the form | Not needed | Hardingasete has far more beds than there are guests (Rikke, 2026-11-07). |
| Saving an unfinished answer to continue later | Moved to If time | It is safer for the guest but more to build. A warning before leaving the form covers v1. |
