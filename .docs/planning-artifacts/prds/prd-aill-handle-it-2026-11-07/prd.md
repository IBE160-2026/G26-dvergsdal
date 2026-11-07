---
title: "PRD: AI'll handle it"
status: draft
created: 2026-11-07
updated: 2026-11-08
inputs:
  - ../../briefs/brief-aill-handle-it-2026-09-23/brief.md
  - ../../briefs/brief-aill-handle-it-2026-09-23/addendum.md
  - ../../briefs/brief-aill-handle-it-2026-09-23/tilbakemelding-product-brief.md
  - ../../research/user-voice-wedding-website-pre-prd-2026-11-06/research.md
  - ../../research/user-voice-wedding-website-pre-prd-2026-11-06/pre-prd-discovery.md
---

# PRD: AI'll handle it

> Draft for review. Every decision behind this document is logged in `.memlog.md`. UX and technical depth is in `addendum.md`, and the reviews are in the `review-*.md` and `reconcile-*.md` files.
>
> References in square brackets show where a requirement comes from:
> - **UJ-n:** a user journey in section 4.
> - **C, D, Q:** decisions and questions in `pre-prd-discovery.md`.
> - **R x.y:** a section of `research.md`.
> - **brief:** the product brief.
> - **review:** a finding from the PRD reviews and source checks on 2026-11-07. A name after the colon says which one, for example *pre-mortem*.
> - **GDPR Art. n:** an article of the GDPR.
> - **No tag:** written and confirmed in the PRD discussion on 2026-11-07.
>
> **[2027]** is not a source. It marks a requirement that is built for production, before invitations go out (section 3.2).
>
> IDs never change. Requirements added later take the next free number, so some appear out of order, such as SM-11 to SM-13 and FR-70 to FR-78.
>
> Quoted interface texts, such as "Send answer", are English working labels. The site is in Norwegian (NFR-6), and the UX phase sets the final wording.

## 1. Overview

### What we are building

*AI'll handle it* is a wedding website that is also the invitation. The site itself has no AI features.

- **The wedding.** Rikke and Valdemar marry on **Saturday 27 May 2028** at **Hardingasete in Hardanger**. The weekend runs from Friday 26 to Sunday 28 May.
- **For guests.** About **70 guests** each get a personal link. A household answers together through it: who is coming, which days, which meals, whether they stay in a cabin, allergies and arrival. Guests see what each option costs, the household total and how to pay. They can also ask the couple questions.
- **For the couple.** The couple and their helpers get one overview of everything.

### The problem it replaces

Today a wedding like this is run with a photo invitation on Messenger, answers in free text and an Excel sheet kept by hand. That means chasing guests for answers, miscounting meals, beds and allergies, and having no record of who has paid.

### Who it is for

- **Guests.** All ages, many of them older and not used to technology, and a few who don't read Norwegian. Most only want the practical details.
- **Households.** A couple or a family. Each person has their own link, and any one of them answers for everyone.
- **The couple, Rikke and Valdemar.** They can change everything, and they pass the final numbers to Hardingasete.
- **Helpers.** The toastmaster, maid of honour and best man. They can see everything but change nothing.
- **The examiner.** Runs the course version locally by following the README.

### Two deliveries

| | Course version (v1) | Production |
|---|---|---|
| When | Tier 1 by 27 November 2026 (section 3.1a); usability test in the first week of December; feature freeze on 10 December; delivery in mid-December 2026 (IBE160) | Online and ready by 1 November 2027 (section 3.2); invitations around December 2027; the wedding on 27 May 2028; data deleted by 31 August 2028 |
| Data | Fictional guests only | Real guests, stored in the EU/EEA |
| How it runs | Locally, following the README | Hosted, paid for by the couple |

### What matters most

Rikke's own priority is that **it must work**:

- The couple must never have to send a new invitation by hand because the site failed.
- It must be simple for guests.
- The answers must be easy for the couple to read and trust.

## 2. Goals and success metrics

### Course version (mid-December 2026)

| ID | Metric | Target | How it is checked |
|---|---|---|---|
| SM-1 | The guest flow works from start to finish on a phone (UJ-1, UJ-2). | Every step works | Automated tests and a written manual test plan |
| SM-2 | The admin counts match an expected-results list worked out by hand. | 100% | Automated tests (FR-69) |
| SM-3 | An older relative completes a household RSVP without help, and the answers match the task they were given. | Under 10 minutes, no wrong answers | Usability test in the first week of December 2026, with fictional data |
| SM-4 | The couple finds any number Hardingasete asks for. | Under 1 minute | Usability test |
| SM-5 | Someone new to the project installs and runs the app and the tests by following the README. | Within 15–20 minutes, no help | A trial run on a clean machine before delivery |
| SM-11 | Answers lock for guests at the deadline, while the couple can still change them. | Works at the boundary | Automated tests (FR-41, FR-42, FR-63) |
| SM-12 | A guest's question shows in the admin area, and is printed in the terminal when no email key is set. | Every question | Automated test (FR-44, FR-45) |
| SM-13 | Every working session with AI is logged, with the key prompts and what was accepted, changed or rejected. | Every session | Session logs in `.logs/`, used in the reflection report [brief] |

### The real wedding (2027–2028, not measured in the course)

| ID | Metric | Target |
|---|---|---|
| SM-6 | Invitations the couple must resend by hand because the site failed | Zero |
| SM-7 | Households that answer before the deadline without being chased | 90% |
| SM-8 | Allergy or bed mistakes in the numbers given to Hardingasete | Zero |
| SM-9 | Times the couple opens Excel for guest logistics | Never |
| SM-10 | Guests asking about something the site already answers | Few |

### Counter-metrics

These guard against reaching the targets above in the wrong way:

- **CM-1: Answers the couple must correct after a phone call.** A fast RSVP is worthless if many answers have to be fixed by hand. Many corrections mean the form is unclear.
- **CM-2: Guests who needed help to answer.** A high response rate is not a success if the couple had to fill in the answers for people.
- **CM-3: Payment mismatches.** Many "I have paid" reports without a matching payment mean the payment instructions are unclear.
- **CM-4: Consent is never pushed.** The allergy consent rate is not a goal. Nothing is ticked in advance, and the RSVP works without consent.

## 3. Scope

### 3.1 Course version v1 (mid-December 2026)

Every functional requirement in section 5 is in v1, except those marked **[2027]** or listed under If time (section 3.3).

### 3.1a Priority within v1

The course version is built in three tiers, so that the most important part works first and v1 is never left half-finished. [review: teacher feedback, sensorveiledning]

| Tier | Done by |
|---|---|
| **1. The usability-test build** | Friday 27 November 2026 |
| **2. The complete course version** | Thursday 10 December 2026, then feature freeze |
| **3. Cut first** | Only if time allows |

**Tier 1, the usability-test build:**

- **Foundation, built first:** the expected-results list and test data (FR-68, FR-69, FR-72), the admin accounts in the test data (FR-47), and one command to run the app and one to run the tests.
- **The guest flow:** FR-1 to FR-18, FR-21 to FR-28, FR-32 to FR-34, FR-41, FR-70, FR-71 and the rules in FR-73 to FR-75.
- **A simple admin view:** the couple's login (FR-46), the summary (FR-54, FR-55), a simple full overview (FR-57) and the allergy list (FR-58).

**Tier 2, the complete course version,** in this order:

1. Changing answers, the lock and overrides (FR-37 to FR-39, FR-42, FR-63, FR-64).
2. Questions (FR-43 to FR-45).
3. Payments (FR-35, FR-36, FR-59 to FR-61).
4. "Needs attention", the guest list and the helper role (FR-56, FR-49, FR-51, FR-46).
5. FR-19, FR-20, FR-29, FR-30, FR-66 and the full text for FR-9 and FR-10.

**Tier 3, cut first:** FR-50 (moving a guest), FR-53 (a new link), FR-31 (consent registered by the couple), FR-65 (price warning), FR-48 beyond basic responsive pages, and slowing down repeated wrong-link attempts (NFR-4) if the chosen technology doesn't provide it.

Anything in tier 3 that isn't done by 10 December moves to [2027], and the change log (section 10) says why. After the feature freeze, only bug fixes, tests and documentation are added.

### 3.2 Before invitations go out (2027)

**Ready date: 1 November 2027.** By then, every requirement marked [2027] is done and the pilot below has passed. After that, only fixes are made until the wedding. [review]

**Setup**

- **Hosting and domain.** Production hosting in the EU/EEA. The domain is fixed, and the site is live on it with HTTPS, at least a month before invitations. The domain and the hosting are paid until at least 1 September 2028.
- **Prices.** Invitations are not sent until Hardingasete's 2028 prices are confirmed.
- **Real settings.** Real prices, deadline, contact details and payment details entered as settings.
- **Email.** An email provider for guest questions that stores data in the EU (D16).
- **Agreements.** Data processing agreements with the hosting and email providers.
- **Vipps.** A fresh check of Vipps terms and prices.
- **Deferred requirements.** The requirements marked [2027] in section 5.

**Keeping the site alive** [review: pre-mortem]

- **Backups.**
  - The database is backed up daily, encrypted, and stored outside both the server and the hosting account.
  - Rikke and Valdemar are both alerted if there has been no successful backup for 24 hours.
  - A backup is taken right before every update to the site.
  - Restoring a backup is rehearsed before invitations, after any server change and right after the RSVP deadline. A rehearsal passes only if a known guest link opens the right household with its answers.
  - Backups are kept for at most 30 days, so deleted allergy information disappears from them too.
- **Monitoring.** An outside check alerts both Rikke and Valdemar on their phones within 15 minutes if the site is down. They are also warned three weeks before the domain, the certificate or the hosting expires.
- **Access.** Both Rikke and Valdemar can log in to the domain, the hosting, the backups and the server, even if a laptop is lost. A one-page guide says what to do if the site goes down.
- **Updates.** An update goes out only after all tests pass. A backup is taken first, and a check afterwards confirms that a real guest link still opens the right household and that the admin counts are unchanged. There are no updates in the last two weeks before the deadline, except fixes for a broken guest flow.

**Going live**

- **Device floor.** A few older guests are asked which phones and tablets they use. The invitation and the whole RSVP must work on those devices, including inside Messenger's and Facebook's built-in browsers. This is checked on a real old device. The invitation text and the RSVP button appear even if the animation or scripts fail.
- **Pilot.** Guests are told in advance, through a channel they trust, that a personal link is coming from Rikke or Valdemar. Then three to five friendly households, including the oldest guest and someone with an old device, get their invitations first. Each completes a full RSVP, reports "I have paid" and asks a question. At least one Vipps payment and one bank payment use exactly the details shown. The couple checks the counts, and writes down a go or no-go before the rest are sent in batches.

**Privacy in operation**

- A short record of what personal data is processed, why, and where it is stored.
- A plan for a data leak: who does what, and reporting to Datatilsynet within 72 hours when required.
- The privacy page lists the companies that process data for the couple (hosting, email).
- Guest pages load nothing, such as fonts or scripts, from other companies, so guests' visits are not shared with them.

### 3.3 If time and capacity allow

These are built only if they can be finished before the ready date (1 November 2027). Otherwise they are not built before the wedding.

- **Envelope animation.** A green envelope opens into the invitation the first time a guest visits. It can be skipped and respects the phone's "reduce motion" setting.
- **Vipps QR code.** Shown next to the Vipps number.
- **Print page.** A printer-friendly page with the numbers Hardingasete needs.
- **Speech sign-up.** Speech sign-ups that reach the toastmaster.
- **Gift list.** A simple text page, possibly with links, for example to an external wish list.
- **English.** An English version with a language button.
- **PC layout.** A layout that uses the larger screen on a PC.

### 3.4 Out of scope

- **Payment through the site.** Online payment, and Vipps payment requests sent to guests; guests pay the couple by Vipps or bank transfer.
- **Payment confirmation to guests.** Guests see what they reported paying, not the couple's registrations.
- **Sending.** The site sending invitations or reminders; the couple does this by hand.
- **Sending to Hardingasete.** The site sending numbers to Hardingasete; the couple emails them.
- **Guest logins.** Guest accounts and passwords; the link is the login.
- **AI.** AI features in the site; they would add cost, and the course does not require them.
- **Activity sign-up.** Sign-up for the treasure hunt, sauna and hot tub, or yoga; these are information only (Q6).
- **Cabin allocation.** Deciding who sleeps in which cabin; the couple does this outside the site.
- **Payment code.** A numeric household code in the payment message (D8); the message uses the household's names instead (FR-71).
- **Answering for oneself only.** The respondent answers for everyone in the household; there is no "answers for themselves" choice.
- **Lost links.** Self-service link recovery; the couple resends links by hand.
- **Change emails.** Email to the couple when a guest changes an answer.
- **Change notices to guests.** The site sending email or SMS to guests when information changes; the couple sends a message themselves if something important changes.
- **Grace period.** A grace period after the deadline (D5).
- **Guest list for guests.** A "who's coming" list that guests can see; it would show guests who else is coming.
- **Children.** Children and child prices; the wedding is child-free.
- **Diagnoses.** Diagnoses in allergy information.
- **Hosting for the course.** Hosting for the course delivery.

## 4. User journeys

Apart from Rikke and Valdemar, all people in these journeys are fictional. The guests among them are reused as test data (FR-68).

### UJ-1: Bestefar Sigmund answers for himself and bestemor

**Sigmund, 78**, is not used to technology. He gets a text message with a link and opens it on his phone.

1. **First impression.** He sees an invitation: Rikke and Valdemar are getting married on Saturday 27 May 2028 at Hardingasete, and **he and bestemor** are invited. The RSVP deadline, a note that the weekend is child-free, and a clear RSVP button are visible without scrolling. *(If time: a green envelope sealed with "R & V" opens and unfolds into the invitation the first time he visits.)*
2. **He scrolls.** Below the invitation he finds short cards for the programme, practical information, Hardingasete and the area, and one about the couple. Each card opens its own page through "Read more", so the RSVP button never gets lost. The button is repeated at the bottom.
3. **He starts his answer.** The form already shows "I am Sigmund", because it is his link. He could change it if bestemor were using his phone.
   - First he marks who is coming: both of them.
   - Then he answers that both are there the whole weekend, Friday to Sunday.
   - Next come the meals and whether they stay overnight. Prices are shown before he chooses.
   - Where he needs more context, for example about the cabins at Hardingasete and what they cost, a "Read more" box opens inside the step, so he never leaves the form.
   - If he tries to leave before sending, the site tells him his answer is not sent yet.
4. **Allergies (optional).** He chooses "No allergies or dietary needs" for himself. He fills in bestemor's dietary needs, says yes to the consent, and confirms that she knows about it and agrees.
5. **Check before sending.** The page says at the top that the answer is not sent yet. He sees all answers and the household total, changes anything that is wrong, and presses **"Send answer"**.
6. **Thank you.** He gets a clear confirmation that matches the answer:
   - Coming: "Thank you for taking the time to answer – we look forward to celebrating the big day with you!"
   - Not coming: "We're sorry you can't make it, but we completely understand."
7. **Payment.** He chooses to pay now or later.
   - **Now:** he sees the amount, the Vipps number (and a QR code, if time), the account number and the household's own payment message: "Bryllup" followed by both their names. After paying, he taps "I have paid", checks the amount and that he used Vipps, and then sees what he reported and when.
   - **Later:** he is told that the same link always shows what he owes and how to pay.
8. **Done.** The page now says: "You can now safely close the invitation."

**Done when:** Sigmund knows the answer is sent, knows what he owes, and knows the link will always show his answer again.
**Biggest risk:** too much happening at once and too many things asking for his attention. Every screen must have one obvious next step.

### UJ-2: Onkel Arild answers for a household where not everyone comes

**Arild** answers for himself, **tante Marie**, **Filippa** and **Leone**. Both daughters are adults who still live at home.

1. **One answer for everyone.** He opens his own link, and the form shows "I am Arild".
   - First he marks who is coming: Arild, Marie and Filippa are coming, and Leone is not. Nothing is ticked in advance.
   - Asked whether everyone who is coming is there the whole weekend, he answers "No", and chooses Saturday and Sunday for Filippa.
2. **The form adapts.**
   - It asks nothing more about Leone.
   - Filippa is only offered the meals on the days she is there. Saturday breakfast is only offered to those who arrive on Friday, and Saturday lunch and dinner are on the couple, so they are not asked about.
   - At the accommodation step, the form says clearly that a cabin is booked for the whole weekend: Filippa can sleep there one night, but pays for both.
   - The total matches exactly what was chosen.
3. **He checks, sends and pays**, as in UJ-1.
4. **A change of plans.** Two weeks later, before the deadline, the RSVP button has become **"See or change answer"**. The top of the form shows what was answered, by whom and when. He changes the answer.
   - If the total goes up, he sees what remains to pay.
   - If it goes down, he is told the couple has been notified and will refund the difference.
5. **Marie opens her own link.** She sees that Arild has already answered and when, instead of an empty form. If she had opened the form before Arild sent his answer, the site would have shown her his answer before she could send hers. No answer is overwritten without anyone seeing it.
6. **After the deadline** the form is locked, and the page tells them to contact the couple directly.

**The couple** sees the household marked "Changed" in the overview. *(2027: they can also open a full history of who changed what and when.)* When they have paid Arild back, they register the refund, and the household's balance is zero again.

### UJ-3: Synne has lost her link and needs a change after the deadline

**Synne** is a friend. She got a new phone, and the message with her link is gone.

1. **She sends a message** to Rikke or Valdemar.
2. **Rikke finds Synne in the admin area on her own phone**, copies Synne's link and sends it again.
3. **If a link has gone astray**, for example forwarded to the wrong person, Rikke deactivates it and creates a new one. Only that guest's link changes; the rest of the household keeps theirs. The old link only says that this is a private invitation and that the visitor should contact the couple the way they usually do. It shows no names, phone numbers or answers.
4. **After the deadline** the button only says **"See answer"**. Synne can see her household's answers but not change them, and she is told the deadline has passed and how to reach Rikke and Valdemar. She can still see how to pay, tap "I have paid", read the information pages, ask the couple a question and withdraw her allergy consent.
5. **Rikke fills in or changes the answer for her** from the admin area, in the same form the guests use. If Synne mentions an allergy on the phone, Rikke sends her the consent text by message and registers the consent when Synne replies yes. The site records who registered it, how, and when.
6. **If something goes wrong**, such as an error message or a page that won't load, Synne still sees how to reach the couple. Their phone numbers are on every guest page.

### UJ-4: Rikke checks the numbers and sends them to Hardingasete

The RSVP deadline has passed, and Hardingasete needs the final numbers soon.

1. **Rikke logs in** and first sees a **summary** (FR-54):
   - how many people and households are coming, not coming, or haven't answered
   - guests per day and how many stay overnight (beds)
   - the count per meal and per allergy category, and how many guests who are coming have nothing registered for allergies
   - how many households have paid, part paid, not paid, have nothing to pay, or are owed a refund
   - interest in the Friday hike, and when people expect to arrive
2. **Directly below is "Needs attention"** (FR-56): a clear list of what Rikke or Valdemar must handle. It shows:
   - households that haven't answered;
   - guests with nothing registered for allergies;
   - unanswered guest questions;
   - "I have paid" reports that don't match a registered payment;
   - refunds owed;
   - households that have changed their answer.

   She marks each item as handled or seen, and it leaves the list. *(2027: it also lists guests whose invitation isn't marked as sent, and households that haven't started a few weeks after it was sent, FR-77.)*
3. **She trusts the numbers** because every count opens the people behind it. When she taps "12 for Friday dinner", she sees who the 12 are. She can also open the full overview of every household, person and answer, and count for herself.
4. **"Not answered" is clear**, with names and contact details. Rikke contacts them herself. *(2027: she adds a dated note to the household, for example "Contacted 12.01".)*
5. **She types the numbers into an email to Hardingasete**: meals, guests, beds, and allergies with names and counts. *(If time: a printer-friendly page with exactly what Hardingasete needs.)* Outside the site, the couple decides who sleeps in which cabin.

**The helpers** (toastmaster, maid of honour, best man) log in and see the same overview, but cannot change anything.

### UJ-5: Rikke follows up payments

Some Vipps payments and bank transfers have come in.

1. **Rikke checks Vipps and her online bank.** Each household's own payment message makes it easy to see who paid. On the site, she registers each amount received, for example "Received 900 kr".
2. **The site works out each household's status** from the amounts: nothing to pay, not paid, part paid (X missing), paid, or refund owed (X). Only the couple and the helpers see this status.
3. **If a guest has reported "I have paid", but the amount registered as received is lower**, the household is **marked red** in the overview and listed under "Needs attention".
4. **Rikke sends reminders herself** by message. *(2027: she adds a dated note that the household has been contacted, shown in both the not-answered list and the payment overview.)*

### UJ-6: Ingrid, the examiner, runs the app

**Ingrid** grades IBE160. She doesn't know the project and uses an ordinary PC.

1. **She clones the repo and reads the README.** It says what the app does and which tools and versions she needs, with commands she can copy.
2. **She installs and starts the app** with a few commands. She needs none of Rikke's accounts or keys; the example settings file (`.env.example`) works as it is.
3. **She fills the database with fictional guests.** They are the people from these journeys, plus households that cover the rest of the expected-results list. The README lists a test link per guest and logins for a test admin and a test helper. These exist only in the test data.
4. **She opens a guest link** in a narrow window, like a phone, and goes through the whole RSVP flow. She tries wrong input and checks the receipt.
5. **She logs in as admin** and sees that the summary matches the expected-results list in the documentation.
6. **She tests the deadline** by moving it to yesterday in the admin settings. The guest can no longer change the answer; the admin still can.
7. **She sends a question as a guest.** It shows up in the admin area and is printed in the terminal, because no email key is set.
8. **She runs the tests with one command.** Among other things, they check that the admin counts match the expected-results list.

**Done when:** Ingrid has run the app and the tests within 15–20 minutes without asking Rikke anything.

## 5. Functional requirements

### 5.1 Personal links and access

- **FR-1** Each guest has their own personal link with a long random code that cannot be guessed. The link is the guest's only login; guests have no accounts or passwords. [brief, UJ-1]
- **FR-2** A link opens the guest's household and nothing else: the invitation, the household's answers, its total and its payment information. [brief]
- **FR-3** Opening a link never changes anything. Only a deliberate action by the guest, such as pressing a button, saves data. This matters because chat apps and email scanners open links by themselves. [C4, R 4.1]
- **FR-4** Page titles and link previews are the same for everyone and contain no names. [C7]
- **FR-5** Without a valid link, the site shows only a friendly message: this is a private invitation, and the visitor should contact the couple the way they usually do. This covers an unknown or deactivated link and the site's address without a link code. The message shows no names, phone numbers, date or place. [UJ-3]
- **FR-6** With a valid link, the couple's contact details are on every guest page, including error messages. [UJ-3]

### 5.2 Invitation and information pages

- **FR-7** The front page looks like an invitation. Without scrolling on a phone, it shows the couple's names, the date and place, the names of the invited household, that the weekend is child-free, the RSVP deadline and the RSVP button. [UJ-1, review]
- **FR-8** Below the invitation are short cards for Programme, Practical information, Hardingasete and the area, and About us. Each opens its own page through "Read more". The RSVP button is repeated at the bottom. [UJ-1]
- **FR-9** The programme shows the weekend day by day, marks what costs money and says what to bring. Everyone sees every activity, including the Friday hike, so a guest who sees it can still decide to come on Friday. The treasure hunt, the sauna and hot tub, and yoga are information only, with no sign-up. [Q6, brief]
- **FR-10** The practical information covers the address, times, transport and parking, dress codes, house rules (child-free, little phone use) and what to bring. [brief]
- **FR-11** Every information page has an obvious way back to the invitation. [UJ-1]

### 5.3 RSVP form

- **FR-12** The form shows "I am [name]", already set to the link's owner. The respondent can switch to another member of the household. The choice records who answered. [C6, UJ-1]
- **FR-13** The form goes step by step, with one clear task per step, a visible Back link and a sign of how far the respondent has come. FR-14 sets the first two steps, and the UX phase sets the order of the rest. [D9]
- **FR-14** The first step asks who in the household is coming: each person is marked "Coming" or "Not coming", and nothing is chosen in advance. The next step asks whether everyone who is coming is there the whole weekend, Friday to Sunday. Answering "No" lets the respondent choose the days for each person. [UJ-2, D1, review]
- **FR-15** Later steps only ask about people who are coming, and only for the days they are there. A meal is offered only on days the person is present, and Saturday breakfast only to those present from Friday. [UJ-2]
- **FR-16** For each person who is coming, the respondent answers yes or no to staying overnight. The form states clearly that a cabin is booked for the whole weekend and that both nights are paid, even if the guest sleeps there only one night. [D1, UJ-2]
- **FR-17** Each person present on Friday is asked about the Friday mountain hike: yes, no or maybe. Others are not asked. [brief]
- **FR-18** Expected arrival is optional and asked per person who is coming, with fixed choices including "Don't know". There are no time pickers. [D11]
- **FR-19** "Read more" inside a step, for example about the cabins and their price, opens in place, so the respondent never leaves the form. [UJ-1]
- **FR-20** Leaving the form before sending shows a warning that the answer is not sent yet. [UJ-1]
- **FR-21** Before sending, a check page says at the top that the answer is not sent yet. It shows every answer per person and the household total, with a "Change" link for each part. Optional questions that were skipped show as "Not provided". The button says "Send answer". [D9, R 1.7, review]
- **FR-22** Errors appear next to the field, with a hint on how to fix them. After a failed attempt to continue, a summary at the top lists each error and links to its field. [R 3.5]
- **FR-23** After sending, a receipt confirms the answer with a message that fits it: one for those who are coming and one for those who can't. "You can now safely close the invitation" appears after the payment choice (FR-34), or straight away when there is nothing to pay. [UJ-1, review]
- **FR-24** Once the household has answered, the invitation shows the household's status near the top: that the answer is sent (by whom and when), the total, what has been reported paid, and the deadline. "See or change answer" (FR-37) opens the answers. [D9, UJ-2, review]
- **FR-70** Each day is shown with its date and what happens that day. The form stops answers that contradict each other, such as staying overnight while being present only one day, and explains why. [review]
- **FR-78** An unsent answer is kept on the guest's own device if they leave or switch apps, or if the page reloads, and it is offered back when they return through their link. [review] **[2027]**

### 5.4 Allergies and consent

- **FR-25** For each person who is coming, the respondent either enters allergies and dietary needs or chooses "No allergies or dietary needs". Allergies use fixed categories (gluten, lactose, nuts, shellfish, vegetarian, vegan, other) and a short note. No diagnoses. The question is optional. [D10, C2, review]
- **FR-26** Allergy information is saved only if the respondent gives consent through a separate Yes/No choice that starts unanswered ("I consent to …"). The consent text says: [C1, UJ-4]
  - what the information is for;
  - who can see it: the couple, toastmaster, maid of honour and best man;
  - that names and allergies are passed on to Hardingasete's kitchen;
  - that consent can be withdrawn through the same link.
- **FR-27** When the respondent enters allergies for others, they confirm that those people know about it and agree. [C2]
- **FR-28** The RSVP can always be sent without consent. If allergies are entered but consent is not given, the form says plainly, before sending, that the allergy information will not be saved and that the guest can tell the couple directly. [C1, review]
- **FR-29** Consent is stored per person: when it was given, who gave it (the person, another household member or the couple) and which version of the consent text was shown. [C1, review]
- **FR-30** Consent can be withdrawn through the personal link at any time, also after the deadline. Withdrawing deletes that person's allergy information and marks the household "Changed". [C1, UJ-3, GDPR Art. 7(3)]
- **FR-31** Before the couple registers allergies for a guest, they send the guest the consent text by message, and they register the consent only when the guest replies yes. The site records who registered it, the channel, the text version and when. [UJ-3, review]

### 5.5 Prices, total and payment for guests

- **FR-32** The price of each paid option is shown before the guest chooses. The paid options are the cabin for the whole weekend, Friday dinner, Saturday breakfast and Sunday breakfast. A short, friendly note explains why guests pay: these are Hardingasete's prices, and the couple pays for Saturday lunch and dinner. [C3]
- **FR-33** The household total is visible along the way and is the same on the check page and the receipt. It is always calculated from the answers and the current prices, never typed in. [C3, D6]
- **FR-34** After sending, a household with something to pay chooses "Pay now" or "Pay later". [UJ-1, D8]
  - **Pay now** shows the amount, the Vipps number, the bank account number and the household's payment message (FR-71).
  - **Pay later** explains that the link always shows what is owed and how to pay.
- **FR-35** The guest can report "I have paid", with the amount (pre-filled with what is owed), the method (Vipps or bank) and, if someone else paid, who. Afterwards the guest sees what they reported and when, and can correct it. [UJ-1, UJ-5, review]
- **FR-36** If the total changes after the guest has reported paying, the guest sees what remains to pay, or that the couple has been told and will refund the difference. [UJ-2]
- **FR-71** Each household has its own payment message: "Bryllup" followed by the household's names. The couple can adjust it, and the site warns if two households would get the same message. [review]

### 5.6 Changing an answer, deadline and lock

- **FR-37** Before the deadline, once the household has answered, the RSVP button becomes "See or change answer" and opens the form with the answers filled in. [UJ-2]
- **FR-38** Before anyone edits, the form shows who last updated the answer and when. If someone else in the household sends an answer after the respondent opened the form, the site shows that answer (who, when and what differs) before the respondent can send. No answer is overwritten without anyone seeing it. [C5 changed, UJ-2, review]
- **FR-39** A household is marked "Changed" when a guest or the couple changes a sent answer, or when allergy consent is withdrawn. The first answer and "I have paid" reports don't count as changes. [UJ-2, review]
- **FR-40** The full history of each household's changes (who changed what, and when) is kept. For allergies, it records only that the information changed, never the content. [UJ-2, review] **[2027]**
- **FR-41** The RSVP deadline is a date: guests can answer until 23:59 Norwegian time that day. It is shown with weekday, date and time next to the RSVP button and in the household's status. All times on the site are Norwegian time. [D4, review]
- **FR-42** After the deadline, guests can no longer change who is coming, days, meals, overnight stay, the hike, arrival or allergies. [D5, UJ-3]
  - The button says "See answer". The page explains that the deadline has passed and shows how to reach Rikke and Valdemar.
  - Payment information, "I have paid", the information pages, questions and consent withdrawal still work.
  - Households that never answered see the same message.

### 5.7 Questions to the couple

- **FR-43** An "Ask us" button on every guest page lets the guest send a short question. The form says that Rikke, Valdemar and the helpers can read it, and asks guests not to write health information there. [brief, review]
- **FR-44** Questions are always stored and listed under "Needs attention". The couple answers outside the site and marks the question as answered. [brief]
- **FR-45** If an email key is configured, each question is also emailed to the couple. Otherwise it is written to the terminal. [brief]

### 5.8 Admin access and roles

- **FR-46** Admin users log in with a username and password. There are two roles: the **couple**, with full access, and **helpers**, who see everything and change nothing. [UJ-4]
- **FR-47** Rikke creates the admin accounts for the couple and the helpers with a command. There is no self-registration.
- **FR-48** Quick tasks work well on a phone: finding a guest, copying their link and seeing whether they have answered. The full overview also works on a phone, but may be designed for a PC. [UJ-3]

### 5.9 Guest list and links

- **FR-49** The couple adds, edits and removes households and guests one by one. Each guest has a name and, optionally, a phone number and an email address, which the couple enters. [brief]
- **FR-50** The couple can move a guest to another household. [brief]
- **FR-51** The couple can search for a guest by name, copy the guest's link and see their contact details. [UJ-3]
- **FR-52** For each guest, the couple can copy a warm, ready-to-send invitation message with the guest's name and link, so the right link goes to the right person. **[2027]**
- **FR-53** The couple can deactivate a guest's link and create a new one. Only that guest's link changes. [UJ-3]
- **FR-76** For each guest, the couple records that the invitation was sent, with the date and the channel (SMS, Messenger or email). Each resend is recorded with a reason, so SM-6 can be counted. [review] **[2027]**

### 5.10 Overview and "Needs attention"

- **FR-54** The admin home page starts with a summary: [UJ-4]
  - people and households who are coming, not coming, or haven't answered (FR-74);
  - guests per day;
  - how many stay overnight (beds);
  - the count per meal (FR-73) and per allergy category;
  - how many guests who are coming have nothing registered for allergies;
  - the number of households in each payment status (FR-60);
  - interest in the hike;
  - expected arrivals.
- **FR-55** Every count opens a list of the people behind it. [UJ-4]
- **FR-56** Below the summary, "Needs attention" lists: [UJ-4, UJ-5]
  - households that haven't answered;
  - guests who are coming but have nothing registered for allergies, neither allergies nor "No allergies or dietary needs";
  - unanswered questions;
  - "I have paid" reports without a matching payment (FR-61), in red;
  - refunds owed;
  - households marked "Changed".

  Each item can be marked as handled or seen, and then leaves the list.
- **FR-57** A full overview shows every household and person with their answers, contact details, total, payment status and notes. Households that haven't answered stand out. On a phone, a guest's phone number and email can be tapped to call or write. [UJ-4]
- **FR-58** An allergy list shows names and categories for everyone who consented, ready to pass on to Hardingasete. [UJ-4]
- **FR-77** The site records when a household has started: pressed Start or saved an answer, never just loaded the page. "Needs attention" also lists guests whose invitation is not yet marked as sent (FR-76), and households that haven't started a few weeks after their invitation was sent. The exact number of weeks is set in the UX phase. [C4, review] **[2027]**

### 5.11 Payments

- **FR-59** The couple registers the amounts received from each household and the refunds paid back. A registration can be corrected or undone. [UJ-5]
- **FR-60** The site works out each household's payment status by comparing the amount received, minus refunds, with the total: [UJ-5, review]
  - **nothing to pay:** the total is 0 kr and nothing has been received;
  - **not paid:** nothing has been received;
  - **part paid:** less than the total has been received, and the status shows the amount still missing;
  - **paid:** the total has been received;
  - **refund owed:** more than the total has been received, and the status shows the amount to refund.

  Only the couple and the helpers see these statuses.
- **FR-61** An "I have paid" report matches when the amount registered as received, minus refunds, is at least the amount the guest reported. A household whose report doesn't match is marked red in the overview and listed under "Needs attention". [UJ-5, review]
- **FR-62** Each household has one dated contact note, for example "Contacted 12.01: payment reminder". It shows both in the not-answered list and in the payment overview. [UJ-4, UJ-5] **[2027]**

### 5.12 Overrides and settings

- **FR-63** The couple can fill in or change any household's answer, also after the deadline, using the same form as the guests. Such changes record the admin as the author. [UJ-3, D5, review]
- **FR-64** In the admin area, the couple can change the prices, the RSVP deadline, their contact details and the payment details (Vipps number and account number). Helpers cannot. When the deadline is changed, the site repeats the new deadline in words and asks for confirmation. A deadline in the past or within two weeks also shows how many households would be locked out. [UJ-6, review]
- **FR-65** Changing prices after households have answered shows a warning with the number of households whose total will change. [UJ-6]

The text on the information pages lives in the code in v1, so changing it means changing the code (D12).

### 5.13 Privacy functions

- **FR-66** A privacy page explains: [R 3.3, review]
  - what is collected and why, including the phone numbers and email addresses the couple enters;
  - who is responsible: Rikke and Valdemar together;
  - the legal basis for each kind of information (NFR-3);
  - who can see it: the couple and the helpers, and for allergies also Hardingasete's kitchen;
  - when it is deleted;
  - the guest's rights, including withdrawing consent and complaining to Datatilsynet;
  - how to contact the couple.

  It is linked from the bottom of every page and from the consent question.
- **FR-67** The couple can delete all guest data in one operation, after a clear confirmation. This covers answers, contact details, consent records, the change history, questions, notes and payments. [review] **[2027]**

### 5.14 Local setup and test data (course version)

- **FR-68** One documented command, separate from starting the app, fills the database with fictional test data: [UJ-6, review]
  - the people from UJ-1 to UJ-3;
  - households that cover the expected-results list:
    - one that declines entirely (nothing to pay);
    - a guest who comes only on Saturday, without a cabin;
    - one that has paid;
    - one that has part paid;
    - one that is owed a refund;
    - one with an "I have paid" report and no matching payment;
    - one that hasn't answered;
    - a guest with an allergy and consent;
    - a guest who entered an allergy but didn't consent;
    - a guest who withdrew consent;
  - fictional contact details and a test link for each guest;
  - fictional prices, a deadline and contact details for the couple, plus obviously invalid payment details;
  - a test couple admin and a test helper.
- **FR-69** An expected-results list is worked out by hand for the test data before the code it checks is written, and is committed to the repository. It covers counts, totals, payment statuses and the deadline lock, and the automated tests check it. [UJ-6, brief, review]
- **FR-72** Test data never reaches the real site. The command that fills in test data refuses to run against a production site, and test accounts and test links exist only in the test data. [review]

### 5.15 Rules for counts and totals

- **FR-73** **Meals.** Guests choose the paid meals: Friday dinner, Saturday breakfast and Sunday breakfast (FR-15). Saturday lunch and dinner are paid by the couple and are not asked about; everyone present on Saturday is counted for both. Meals do not depend on staying overnight. [D2, brief, review]
- **FR-74** **People and households.** Each person is coming, not coming, or hasn't answered. A household counts as answered once an answer has been sent, and as coming when at least one person in it is coming. [brief, review]
- **FR-75** **Removed choices.** When a person is changed to not coming, or a day is removed, the choices for that person or day are removed too, so they never count in totals or numbers. [review]

## 6. Non-functional requirements

### NFR-1 Reliability (Rikke's top priority)

- A guest's link keeps working from the day it is sent until the data is deleted. The domain and the link format are fixed before invitations go out and never change afterwards.
- Links work when sent by SMS, Messenger and email: they are short enough and use only characters that are safe in links. Before invitations go out, a test link is sent through all three channels and opened on both Android and iPhone.
- Saving either succeeds and says so, or fails with a clear message and keeps what the guest entered. Nothing is lost without the guest knowing.
- In production, the site is available from the invitations until the wedding, with no planned downtime in the last two weeks before the deadline.
- In production, the backups, monitoring, access, update rules and pilot in section 3.2 apply.

### NFR-2 Correct numbers

- All counts, totals and payment statuses are calculated from the stored answers and payments, never stored separately. The rules in section 5.15 decide every count. [D6]
- Amounts are whole kroner.
- Automated tests check that the admin counts and totals match the expected-results list (FR-69).

### NFR-3 Privacy

- GDPR is assumed to apply, and allergies are treated as health data. [R 3.1, R 3.2]
- Rikke and Valdemar are jointly responsible for the data (joint controllers).
- The legal basis for each kind of information is the couple's own assessment, not legal advice: [review]

  | Information | Purpose | Legal basis | Who sees it |
  |---|---|---|---|
  | Names, households and links | Inviting guests and collecting answers | Legitimate interest | The couple and helpers |
  | Phone numbers and email addresses entered by the couple | Following up guests | Legitimate interest | The couple and helpers |
  | Answers: attendance, days, meals, overnight stay, hike, arrival | Planning the weekend and giving numbers to Hardingasete | Legitimate interest | The couple and helpers; numbers go to Hardingasete |
  | Allergies and dietary needs | Safe food from Hardingasete's kitchen | Explicit consent (GDPR Art. 9(2)(a)) | The couple and helpers; names and allergies go to Hardingasete's kitchen |
  | Consent records | Showing that consent was given | Legal obligation to prove consent (Art. 7(1)) | The couple |
  | Payments and "I have paid" reports | Keeping track of money | Legitimate interest | The couple and helpers |
  | Questions from guests | Answering guests | Legitimate interest | The couple and helpers |

- Only what is needed is collected. Guests are stored with a name and, optionally, a phone number and email so the couple can follow up. Allergies are categories and a short note, with no diagnoses.
- The repository is public. Only fictional data is used in the repository, tests, test data, screenshots, the usability test and AI tools. Apart from Rikke and Valdemar, all people named in this PRD are fictional.
- Real data lives only in the production database, hosted in the EU/EEA. Hosting and email providers that handle it have data processing agreements.
- Real data is deleted by 31 August 2028. That includes emailed copies, such as forwarded questions and the allergy list sent to Hardingasete.
- **Accepted risk.** When one adult enters allergies for another, the consent comes from the respondent's confirmation, not from the person themselves (C2). This risk was accepted on 2026-11-06. FR-29 records who gave each consent.

### NFR-4 Security

- Link codes have at least 128 bits of randomness and contain no personal data. [R 4.1]
- Guest pages are hidden from search engines and do not pass the link on to other sites. Repeated attempts with wrong links are slowed down. [R 4.1]
- Admin passwords are stored with a modern password-hashing method. [R 4.2]
- Admin sessions expire after a period of inactivity. [R 4.2]
- Forms are protected against forged submissions. [R 4.2]
- Repeated login attempts are slowed down. [R 4.2]
- Apart from a household's own answers, which its links show (FR-2), only logged-in admins see guest answers. The server, not just the page, stops helpers from changing data.
- No secrets in the repository. Real settings live in a settings file that Git ignores, and the example file contains no real values.

### NFR-5 Accessibility (self-imposed target: WCAG 2.2 AA)

- Text contrast is at least 4.5:1. [R 3.5]
- Body text on guest pages is at least 18 px. [brief, review]
- The site works at 200% zoom and at 320 px width.
- Everything can be done with a keyboard, and the keyboard focus is always visible.
- Buttons and other touch targets on guest pages are at least 44 × 44 px. The WCAG AA minimum is 24 × 24 px; larger targets suit older guests.
- Every field has a label, and errors follow FR-22.
- The site does not ask for what the link already knows, such as names.
- Any animation respects the phone's "reduce motion" setting and can be skipped.

### NFR-6 Ease of use

- Phone first, for all ages. A PC shows the phone layout; a wider layout is an If-time item (section 3.3). [brief]
- Every screen has one obvious next step.
- Plain, warm Norwegian (bokmål) with a cosy tone, also in error messages.
- An older guest can complete a household RSVP correctly and without help in under 10 minutes (SM-3).

### NFR-7 Performance and size

- Pages load in under 3 seconds on an ordinary phone on 4G.
- Sized for about 70 guests and 5 admin users. No further scaling is needed.

### NFR-8 Runnability (course version)

- The app runs locally on an ordinary PC (Windows, macOS or Linux) by following the README. It needs no separate database server and none of Rikke's accounts or keys. [brief]
- Installing and starting the app and running the tests take no more than 15–20 minutes (SM-5).

### NFR-9 Maintainability

- The code is checked by a linter and a formatter.
- All automated tests run with one command.
- Settings that differ between local and production are documented in `.env.example`.
- Stories refer to the requirement IDs in this PRD, so every feature can be traced back to a requirement.

## 7. Constraints, dependencies and assumptions

### Constraints

- **Team.** Rikke is a solo developer, early in learning to program. She builds with AI assistance, using the BMAD method.
- **Dates.** The timeline is in section 1, and the tier dates are in section 3.1a.
- **Course requirement.** The app must be full-stack with one database. The technology is chosen in the architecture document.
- **Public repository.** Everything in the repository is public, so it holds only fictional data.

### Hardingasete (asked 2026-11-06)

- **Q1: Beds and cabins.** Answered for capacity: Hardingasete has far more beds than there are guests, so the form needs no bed limit (Rikke, 2026-11-07). Outside the site, the couple allocates the cabins.
- **Q2 to Q4** are still open; see section 8.

### Assumptions

- Guests get their link digitally and can open it on a phone or a PC.

## 8. Open questions

| ID | Question | Owner | Blocks the PRD? | Revisit when |
|---|---|---|---|---|
| Q2 | When and in which format does Hardingasete need the final numbers? This sets the RSVP deadline (about two weeks before Hardingasete needs the numbers) and what the overview must show. | Rikke | No | Hardingasete replies |
| Q3 | What are Hardingasete's prices per meal and for the cabin? They are entered as settings (FR-64), and invitations are not sent until they are known (section 3.2). | Rikke | No | Hardingasete replies |
| Q4 | May guests pay Hardingasete directly? This may change FR-34. | Rikke | No | Hardingasete replies |
| Q7 | How do two or three guests, including older ones, feel about paying for meals? Affects the wording in FR-32. | Rikke | No | Before the UX text is written |
| Q8 | Is the teacher fine with the consent model differing from the first brief? (The teacher's feedback already asks for an expected-results list checked by automated tests, which FR-69 covers.) | Rikke | No | Next supervision |
| D12 | In production, should the programme and the practical information be editable in the admin area? Rikke's rule: yes, if the architecture shows it isn't much harder than keeping the text in the code with the update rules in section 3.2. | Architecture | No | bmad-architecture |
| D14 | Store link codes hashed or in plain form? | Architecture | No | bmad-architecture |
| D15 | Database and technology stack | Architecture | No | bmad-architecture |
| D16 | Email provider in production; it must store data in the EU | Rikke | No | 2027 |

## 9. Changes from the product brief

Decided during the PRD on 2026-11-07. Each change is logged in `.memlog.md`.

| Topic | Brief | PRD | Why |
|---|---|---|---|
| Helpers | Full access for all admin users | Helpers can see but not change (FR-46) | Rikke wants only the couple to change data |
| Payment status | Paid or not paid, with undo (D6) | Amounts are registered, and the status is calculated: nothing to pay, not paid, part paid, paid or refund owed (FR-59, FR-60) | Rikke needs "part paid"; a status calculated from amounts can't drift away from the money actually received |
| "I have paid" | Optional (D6) | In v1, with amount and method (FR-35, FR-61) | Catches mismatches and avoids wrong reminders. Guests don't see the couple's confirmation; their own report is enough for them |
| Payment message | No household code; "Bryllup" + name (D8) | "Bryllup" + all the household's names, with a duplicate warning (FR-71) | A single first name isn't unique enough to match payments |
| Links | One per guest (brief); research assumed one per household | One per guest, with "I am …" already set to the owner (FR-1, FR-12) | Doesn't ask for what the link knows (WCAG 3.3.7), and deactivating a link affects only one person |
| First question | Not specified | "Who is coming?" first, then "the whole weekend?" (FR-14) | A review found that "Is everyone coming the whole weekend? No" feels like declining |
| Two people answering at once | Last save wins (C5) | The later sender sees the other answer first (FR-38) | With one link per person, two household members answering at the same time is likely |
| Allergy recipients | The consent names who can see the data | The consent also says that names and allergies go to Hardingasete's kitchen (FR-26) | The couple emails the allergies with names |
| "No allergies" | Not specified | An explicit choice per person (FR-25) | Lets the couple see who hasn't answered the question |
| Gift list | Format undecided | Simple text page with links, If time | Decided by Rikke |
| Guest contact details | Not specified | Optional phone and email per guest, entered by the couple (FR-49) | Makes follow-up easier for the couple. Claude proposed storing names only (data minimisation); Rikke chose otherwise, and the privacy page explains it (FR-66) |
| Prices | Not known yet | Invitations are not sent until the 2028 prices are known (section 3.2) | Avoids totals that change after guests have answered |
| Priority | Must and If time | Three tiers within v1 (section 3.1a) | The teacher's warning about time and scope |
| Link tracking | If time | Required before invitations, with an "invitation sent" record (FR-76, FR-77) | Without it, a link that never arrived looks like a slow guest |
| Unfinished answers | If time | Required before invitations, kept on the guest's device (FR-78) | A phone call or a closed page must not lose an older guest's answer |
| Change notices to guests | If time | Out | The site would send messages itself, which the couple doesn't want |
| Running the site | Hosting in 2027 | Backups, monitoring, access, update rules, a pilot and a ready date of 1 November 2027 (section 3.2) | The pre-mortem review found that nothing kept the real site alive |
| New in v1 | — | "Needs attention" (FR-56), counts that open the people behind them (FR-55), the "Changed" marker (FR-39), settings in admin (FR-64, FR-65), the privacy page (FR-66), consent registered by the couple (FR-31), rules for counts (FR-73 to FR-75) | Came out of the user journeys and the reviews |
| Dropped | — | Email to the couple when an answer changes | Rikke: the overview is enough |

## 10. Change log

| Date | Change |
|---|---|
| 2026-11-07 | First draft: user journeys UJ-1 to UJ-6, FR-1 to FR-69, NFR-1 to NFR-9. Four FRs deferred to 2027. |
| 2026-11-07 | Round 2: FR-5, FR-6, FR-9, FR-17, FR-42, FR-47, FR-49, FR-51, FR-57, FR-66 and FR-68 clarified; guest contact details added. |
| 2026-11-07 | Round 3: NFR-1, NFR-5 and NFR-7 confirmed; helpers see contact details (FR-66). |
| 2026-11-07 | After five input reconciliations and five reviews: priority tiers (section 3.1a); first question restructured (FR-14, FR-70); no silent overwrite (FR-38); payment message and fuller "I have paid" (FR-35, FR-71); "No allergies" (FR-25); count rules (FR-73 to FR-75); deadline moment (FR-41, FR-64); test data never in production (FR-72); legal bases (NFR-3); larger text (NFR-5); course success criteria SM-11 to SM-13 restored from the brief; journeys mark what comes in 2027. |
| 2026-11-07 | Production in 2027 (section 3.2): ready date 1 November 2027, backups, monitoring, access, update rules, device floor, pilot and privacy in operation. FR-76 to FR-78 added; link tracking and unfinished answers made required before invitations; change notices to guests moved to Out; D12 left to the architecture with Rikke's rule. |
| 2026-11-08 | Polish after a structure and language review (bmad-review): a fuller reading key and a note that quoted interface texts are working labels; the whole timeline in section 1; tier contents as lists (section 3.1a); constraints that were scope decisions moved to section 3.4; Q2 to Q4 moved to section 8; UJ-3 renamed; FR-13 leaves the order of later form steps to the UX phase; repeats in NFR-8 removed; the palette contrast check and a possible 2027 improvement moved to the addendum; about 40 wording fixes that remove ambiguities and contradictions without changing what is decided. |
