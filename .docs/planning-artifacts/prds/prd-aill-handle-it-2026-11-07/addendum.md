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

1. **Top:** the invitation, with the RSVP button visible without scrolling. It also says that the weekend is child-free (FR-7).
2. **Below:** short cards with two or three lines each and "Read more":
   - Programme
   - Practical information
   - Hardingasete and the area
   - About us
   - Gifts (if time)
3. **Bottom:** the RSVP button again.

### Look, programme and intent from the brief (preserve)

These come from the product brief and its addendum. The PRD's requirements don't carry them, but the UX work must.

- **Look and feel.**
  - The couple's own look, not a template.
  - Palette: sage green, soft white and dark wood.
  - Elegant but cosy, not overly fancy.
- **Programme.**
  - **Friday:** a daytime mountain hike for early arrivals. In the evening, a treasure hunt (rebus), then sauna and hot tub, and Friday dinner (paid).
  - **Saturday:** optional yoga, then the wedding. The couple hosts lunch and dinner. Saturday breakfast is paid.
  - **Sunday:** breakfast (paid).
  - The cabins are on the farmyard and are booked for the whole weekend or not at all.
- **Staying.** Guests are encouraged to stay the whole weekend, but they can come without staying overnight, for example only for the wedding day.
- **Gifts.** The gift page message from the brief: "we know the wedding may be expensive to attend and we don't expect gifts, but there is a wish list for anyone who wants one". It balances asking guests to pay for meals and cabins.
- **House rules.** Child-free, and minimal phone use.

### Rikke's own wording for the receipt (Norwegian original)

Use this as the starting point for the final text:

- **Coming:** «Tusen takk for at du tok deg tiden til å svare, vi gleder oss til å feire den store dagen med deg/dere»
- **Not coming:** «Så leit at du/dere ikke har mulighet til å delta, men dette har vi full forståelse for.»
- **At the end:** «Du kan nå trygt lukke siden/invitasjonen». Following the reviews, this appears after the payment choice, or straight away when there is nothing to pay (FR-23).

### Invitation message for sending links (FR-52)

Rikke wants the message to be warmer and cosier than Claude's first example ("Hei Sigmund! Her er invitasjonen til bryllupet vårt: [lenke]"). It must include the guest's first name so the couple can see that the right link goes to the right person. The exact wording is set in the UX phase.

### Tone

Warm and "koselig" throughout, including error messages. Every screen should have one obvious next step for older guests.

### "Needs attention" behaviour

| Item | Leaves the list when |
|---|---|
| Household not answered | The household answers, or the couple marks it as handled |
| Guest with nothing registered for allergies | Allergies or "No allergies" are registered, or the couple marks it as handled |
| Unanswered question | The couple marks it as answered |
| "I have paid" without a matching payment (red) | A matching amount is registered, or the couple marks it as handled |
| Refund owed | The refund is registered |
| Household marked "Changed" | The couple marks it as seen |

### Payment status (FR-60)

The status compares the amount received, minus refunds, with the household's total. Only the couple and the helpers see it.

| Received minus refunds | Status shown |
|---|---|
| 0 kr, and the total is 0 kr | Nothing to pay |
| 0 kr | Not paid |
| Less than the total | Part paid, X kr missing |
| Exactly the total | Paid |
| More than the total | Refund owed, X kr |

## For architecture (bmad-architecture)

- **D14.** Store link codes hashed or in plain form. Hashed codes mean the couple can't look up an existing link; they can only create a new one. That conflicts with FR-51 (copy the guest's link) unless the code can be shown again. Weigh this against [R 4.1].
- **D15.** The database and technology stack. The research recommends SQLite for clone-and-run (NFR-8) [R 4.4].
- **Two admin roles (FR-46).** The server must stop helpers from changing data, not just the page.
- **Server-calculated values (NFR-2).** Totals and payment statuses are always calculated, never stored. The research gives security detail for admin login [R 4.2].
- **Change marker and history (FR-39, FR-40).** v1 needs the "Changed" marker and "last updated by X at Y". The full history may come in 2027, but the data model should allow it from the start, and it must never store allergy content.
- **No silent overwrite (FR-38).** Each household answer needs something like a version number, so that sending can detect that someone else sent a newer answer in the meantime. This is cheap only if it is planned from the start [R 4.5].
- **One form (FR-63).** The couple fills in and changes answers with the same form as the guests, not a second copy of it.
- **Times (FR-41).** All times are Norwegian time. The deadline lock is tested at the boundary, in both winter and summer time.
- **Test data guard (FR-72).** The README's test links use fixed codes that exist only in the test data. Real links always come from the random generator. The command that fills in test data refuses to run against a production site.

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
| Storing guest names only, without phone or email (Claude's data-minimisation proposal) | Rejected by Rikke | Contact details make follow-up easier for the couple, who are responsible. The privacy page must explain what is stored and why. |
| Showing the couple's contact details on pages without a valid link (Claude's first proposal for UJ-3) | Rejected | Anyone typing a random address would see both phone numbers. The people who need them, friends and family, already have them. |
| Saving an unfinished answer to continue later | Moved to If time | It is safer for the guest but more to build. A warning before leaving the form covers v1. |
| Last save wins without any check (C5) | Replaced | With one link per person, two household members answering at the same time is likely. The later sender now sees the other answer first (FR-38). |
| An "answers for themselves" choice for other household members (pre-mortem review) | Rejected by Rikke | The respondent answers for everyone who is coming; this keeps the form simple. |
| Showing guests that the couple has confirmed their payment (pre-mortem review) | Rejected by Rikke | Toward guests, their own "I have paid" report is enough. The couple's registrations stay internal. |
| Remembering which prices each household answered with (pre-mortem review) | Not needed | Invitations are not sent until the 2028 prices are known. |
| Asking a person to confirm allergies someone else entered for them (GDPR review) | Not planned | The risk was accepted in C2, and FR-29 records who gave each consent. A possible improvement for 2027. |
| Hiding questions and payments from helpers (GDPR review) | Rejected | The "Ask us" form tells guests that the helpers can read questions. |

## Test data note (FR-68, FR-72)

- **Contact details.** Fictional contact details in the test data should be obviously fake: email addresses on `example.com`, which is reserved for examples, and phone numbers that cannot belong to a real person.
- **Payment details.** These must be obviously invalid, for example an account number that fails the bank's check digit, so that no one can pay to them by mistake.
