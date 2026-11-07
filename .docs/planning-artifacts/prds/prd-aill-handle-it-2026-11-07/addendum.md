# Addendum: PRD for AI'll handle it

This addendum keeps the detail from the PRD discussion that belongs in later documents (the UX spec and the architecture) rather than in the PRD itself. It also records the alternatives that were rejected, and why. Read it with [prd.md](prd.md), which explains the IDs and references used here. Where the two differ, the PRD applies.

## For UX (bmad-ux)

### Look, programme and intent from the brief

These come from the product brief and its addendum. The PRD carries only parts of them, so the UX work must carry them in full.

- **Look and feel.**
  - The couple's own look, not a template.
  - Palette: sage green, soft white and dark wood. Check that sage green on soft white meets the 4.5:1 text contrast in NFR-5.
  - Elegant but cosy, not overly fancy.
- **Programme.**
  - **Friday:** a daytime mountain hike for early arrivals. In the evening, a treasure hunt (rebus), then sauna and hot tub, and Friday dinner (paid).
  - **Saturday:** breakfast (paid) and optional yoga, then the wedding. The couple hosts lunch and dinner.
  - **Sunday:** breakfast (paid).
- **Staying.** The cabins are on the farmyard and are booked for the whole weekend or not at all. Guests are encouraged to stay the whole weekend, but they can come without staying overnight, for example only for the wedding day.
- **Gifts.** The gift page message from the brief: "we know the wedding may be expensive to attend and we don't expect gifts, but there is a wish list for anyone who wants one". It balances out asking guests to pay for meals and cabins.

### Tone (NFR-6)

Warm and "koselig" throughout, including error messages.

### Invitation reveal (UJ-1, FR-7; Rikke, 2026-11-07)

- The animation is If time (PRD section 3.3). The static invitation look is required in v1 (FR-7) and has to work well on its own.
- The guest first sees a green envelope sealed with a wax-style stamp reading "R & V".
- The envelope opens and unfolds into an invitation, and the unfolded invitation **is** the website.
- Once the invitation has unfolded, the envelope and the paper outline disappear. There are no folds and no sheet edges, only the content, in the same visual style as the invitation.
- The invitation says that Rikke and Valdemar are getting married on Saturday 27 May 2028 and that the named guests are invited (full content: FR-7).
- The guest should feel invited to scroll down for more information.

### Front page structure (FR-7, FR-8; agreed 2026-11-07)

1. **Top:** the invitation, with everything FR-7 lists visible without scrolling.
2. **Below:** short cards (FR-8) with two or three lines each and "Read more":
   - Programme
   - Practical information
   - Hardingasete and the area
   - About us
   - Gifts (If time)
3. **Bottom:** the RSVP button again.

### Rikke's own wording for the receipt (FR-23; Norwegian original)

Use this as the starting point for the final text:

- **Coming:** «Tusen takk for at du tok deg tiden til å svare, vi gleder oss til å feire den store dagen med deg/dere»
- **Not coming:** «Så leit at du/dere ikke har mulighet til å delta, men dette har vi full forståelse for.»
- **At the end:** «Du kan nå trygt lukke siden/invitasjonen» (placement: FR-23, changed after the reviews).

### Invitation message for sending links (FR-52) [2027]

Rikke wants the message to be warmer and cosier than Claude's first example ("Hei Sigmund! Her er invitasjonen til bryllupet vårt: [lenke]"). It must include the guest's first name. The exact wording is set in the UX phase.

### "Needs attention" behaviour (FR-56)

This table sets when each item in FR-56 leaves the list.

| Item | Leaves the list when |
|---|---|
| Household not answered | The household answers, or the couple marks it as handled |
| Guest with nothing registered for allergies | Allergies or "No allergies" are registered, or the couple marks it as handled |
| Unanswered question | The couple marks it as answered |
| "I have paid" report without a matching payment (marked red) | A matching amount is registered, or the couple marks it as handled |
| Refund owed | The refund is registered |
| Household marked "Changed" | The couple marks it as seen |

### Payment status (FR-60)

The wording shown in admin for each status. The first row that matches applies.

| Received minus refunds | Status shown |
|---|---|
| 0 kr, and the total is 0 kr | Nothing to pay |
| 0 kr | Not paid |
| Less than the total | Part paid, X kr missing |
| Exactly the total | Paid |
| More than the total | Refund owed, X kr |

### Still to settle in the UX phase

- The final Norwegian wording of every interface text. The PRD quotes English working labels.
- The order of the form steps after the first two (FR-13, FR-14).
- The wording that explains why guests pay (FR-32), once Q7 is answered (PRD section 8).
- The exact invitation message (FR-52) [2027].
- How many weeks pass before a household that hasn't started is listed under "Needs attention", and when the two FR-77 items leave the list (FR-77) [2027].

## For architecture (bmad-architecture)

Open decisions (PRD section 8): D12, D14 and D15. The other points came out of the PRD discussion. They are not a full list: the architecture must also meet every NFR and PRD section 3.2.

- **D12.** Whether the programme and the practical information become editable in the admin area in production. Rikke's rule is in PRD section 8.
- **D14.** Store link codes hashed or in plain form? Hashed codes mean the couple can't look up an existing link; they can only create a new one. That conflicts with FR-51 (copy the guest's link) unless the code can be shown again. Weigh this against the link security advice in [R 4.1].
- **D15.** The database and technology stack. The research recommends SQLite for clone-and-run (NFR-8) [R 4.4].
- **Two admin roles (FR-46).** The server, not just the page, must stop helpers from changing data. The research gives security details for admin login [R 4.2].
- **Server-calculated values (NFR-2).** Totals and payment statuses are always calculated, never stored.
- **Change marker and history (FR-39, FR-40).**
  - v1: the "Changed" marker and "last updated by X at Y".
  - 2027: the full history (FR-40), required before invitations. The data model should allow it from the start.
  - The history must never store allergy content.
- **No silent overwrite (FR-38).** Each household answer needs something like a version number, so that the site can detect, on sending, whether someone else sent a newer answer in the meantime. This is cheap only if it is planned from the start [R 4.5].
- **One form (FR-63).** The couple fills in and changes answers with the same form as the guests, not a second copy of it.
- **Times (FR-41).** All times are Norwegian time. The deadline lock is tested at the boundary, in both winter and summer time.
- **Test data (FR-68, FR-72).**
  - The README's test links use fixed codes that exist only in the test data. Real links always come from the random generator.
  - Fictional contact details should be obviously fake: email addresses on `example.com`, which is reserved for examples, and phone numbers that cannot belong to a real person.
  - Payment details must be obviously invalid, for example an account number with an invalid check digit, so that no one can pay to them by mistake.

## Rejected alternatives

The resulting scope and changes are in PRD sections 3.4 and 9. This table keeps the options that lost, and why, grouped by topic. Rows marked "Claude" or "AI review" were proposals from the AI that the couple rejected or changed.

| Alternative | Decision | Why |
|---|---|---|
| One link per household (assumed in the research [R 5]) | Rejected | One link per guest lets the site know who is answering, so the form doesn't ask for names (WCAG 3.3.7), and deactivating a link affects only that person. |
| Guests can request their own link ("send me my link") | Rejected | The site would have to send email or SMS. The couple resends links by hand. |
| Showing the couple's contact details on pages without a valid link (Claude's first proposal for UJ-3) | Rejected | Anyone typing a random address would see both phone numbers. The people who need them, friends and family, already have them. |
| "Everyone is coming" ticked in advance | Rejected | Older guests who skim would sign up people who aren't coming, which gives wrong numbers and totals. |
| An "answers for themselves" choice for other household members (AI pre-mortem review) | Rejected by Rikke | The respondent answers for everyone who is coming; this keeps the form simple. |
| Last save wins without any check (C5) | Replaced | With one link per person, two household members answering at the same time is likely. The later sender now sees the other answer first (FR-38). |
| Saving an unfinished answer in v1 | Moved to 2027 | First moved to If time; after the reviews, it is required before invitations, with the answer kept on the guest's own device (FR-78). A warning before leaving the form covers v1. |
| Payment as two states, paid or not paid (D6) | Replaced | Rikke needs "part paid". A status calculated from amounts can't drift away from the money actually received. |
| Showing guests that the couple has confirmed their payment (AI pre-mortem review) | Rejected by Rikke | For guests, their own "I have paid" report is enough. The couple's registrations stay internal. |
| Storing the prices that applied when each household answered (AI pre-mortem review) | Not needed | Invitations are not sent until the 2028 prices are known. |
| Email to the couple when an answer changes | Dropped | The "Changed" marker and "Needs attention" are enough. |
| Change notices to guests by email or SMS | Out | The site would send messages itself, which the couple doesn't want. The couple sends a message if something important changes. |
| Storing guest names only, without phone or email (Claude's data-minimisation proposal) | Rejected by Rikke | Contact details make follow-up easier for the couple, who are responsible for following up guests. The privacy page must explain what is stored and why. |
| Asking a person to confirm allergies someone else entered for them, in their own link (AI GDPR review) | Not planned | The risk was accepted in C2, and FR-29 records who gave each consent. A possible improvement for 2027. |
| Hiding questions and payments from helpers (AI GDPR review) | Rejected | The "Ask us" form tells guests that the helpers can read questions. |
| Importing the guest list from Excel | Not needed | The couple enters about 35 households by hand. |
| Cabin and bed allocation on the site | Out | The couple does it outside the site. |
| A bed limit in the form | Not needed | Hardingasete has far more beds than there are guests (Rikke, 2026-11-07). |
