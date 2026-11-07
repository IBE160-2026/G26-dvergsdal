---
title: "PRD: AI'll handle it"
status: draft
created: 2026-11-07
updated: 2026-11-07
inputs:
  - ../../briefs/brief-aill-handle-it-2026-09-23/brief.md
  - ../../briefs/brief-aill-handle-it-2026-09-23/addendum.md
  - ../../briefs/brief-aill-handle-it-2026-09-23/tilbakemelding-product-brief.md
  - ../../research/user-voice-wedding-website-pre-prd-2026-11-06/research.md
  - ../../research/user-voice-wedding-website-pre-prd-2026-11-06/pre-prd-discovery.md
---

# PRD: AI'll handle it

> Draft for review. Every decision behind this document is logged in `.memlog.md`. UX and technical depth is in `addendum.md`.
>
> References in square brackets show where a requirement comes from:
> - **UJ-n:** a user journey in section 4.
> - **C, D, Q:** decisions and questions in `pre-prd-discovery.md`.
> - **R x.y:** a section of `research.md`.
> - **brief:** the product brief.

## 1. Overview

### What we are building

AI'll handle it is a wedding website that is also the invitation.

- **The wedding.** Rikke and Valdemar marry on **Saturday 27 May 2028** at **Hardingasete in Hardanger**. The weekend runs from Friday 26 to Sunday 28 May.
- **For guests.** About **70 guests** each get a personal link. A household answers together through it: who is coming, which days, which meals, whether they stay in a cabin, allergies and arrival. Guests see what each option costs, the household total and how to pay. They can also ask the couple questions.
- **For the couple.** The couple and their helpers get one overview of everything.

### The problem it replaces

Today a wedding like this is run with a photo invitation on Messenger, answers in free text and an Excel sheet kept by hand. That means chasing guests for answers, miscounting meals, beds and allergies, and having no record of who has paid.

### Who it is for

- **Guests.** All ages, many of them older and not used to technology, and a few who don't read Norwegian. Most only want the practical details.
- **Households.** A couple or a family. Each person has their own link, and any one of them can answer for everyone.
- **The couple, Rikke and Valdemar.** They can change everything, and they pass the final numbers to Hardingasete.
- **Helpers.** The toastmaster, maid of honour and best man. They can see everything but change nothing.
- **The examiner.** Runs the course version locally by following the README.

### Two deliveries

| | Course version (v1) | Production |
|---|---|---|
| When | Mid-December 2026 (IBE160) | Online in 2027; invitations sent around December 2027; data deleted by 31 August 2028 |
| Data | Fictional guests only | Real guests, stored in the EU/EEA |
| How it runs | Locally, following the README | Hosted, paid for by the couple |

### What matters most

Rikke's own priority is that **it must work**:

- The couple must never have to send a new invitation by hand because the site failed.
- It must be simple for guests.
- The answers must be easy for the couple to read and trust.

The site itself has no AI features.

## 2. Goals and success metrics

### Course version (mid-December 2026)

| ID | Metric | Target | How it is checked |
|---|---|---|---|
| SM-1 | The guest flow works from start to finish on a phone (UJ-1, UJ-2). | Every step works | Automated tests and a written manual test plan |
| SM-2 | The admin counts match an expected-results list worked out by hand. | 100 % | Automated tests (FR-69) |
| SM-3 | An older relative completes a household RSVP without help. | Under 10 minutes | Usability test in the first week of December 2026, with fictional data |
| SM-4 | The couple finds any number Hardingasete asks for. | Under 1 minute | Usability test |
| SM-5 | Someone new to the project installs and runs the app and the tests by following the README. | Within 15–20 minutes, no help | A trial run on a clean machine before delivery |

### The real wedding (2027–2028, not measured in the course)

| ID | Metric | Target |
|---|---|---|
| SM-6 | Invitations the couple must resend by hand because the site failed | Zero |
| SM-7 | Households that answer before the deadline without being chased | 90 % |
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

Every functional requirement in section 5 is in v1, except those marked **[2027]** or listed under If time.

### 3.2 Before invitations go out (2027)

- **Hosting.** Production hosting in the EU/EEA, on a domain that is fixed before any invitation is sent.
- **Real settings.** Real prices, deadline, contact details and payment details entered as settings.
- **Backups.** Daily backups, with a restore tested before invitations are sent.
- **Email.** An email provider for guest questions that stores data in the EU (D16).
- **Agreements.** Data processing agreements with the hosting and email providers.
- **Vipps.** A fresh check of Vipps terms and prices.
- **Deferred requirements.** The requirements marked [2027] in section 5, and any If-time items not done in v1.

### 3.3 If time and capacity allow

- **Envelope animation.** A green envelope opens into the invitation the first time a guest visits. It can be skipped and respects the phone's "reduce motion" setting.
- **Unfinished answers.** The guest can save an unfinished answer and continue later.
- **Vipps QR code.** Shown next to the Vipps number.
- **Print page.** A printer-friendly page with the numbers Hardingasete needs.
- **Speech sign-up.** Only the toastmaster sees the sign-ups.
- **Gift list.** A simple text page, possibly with links, for example to an external wish list.
- **Link tracking.** Shows which households have started: pressed Start or saved an answer. Loading the page does not count (C4).
- **English.** An English version with a language button.
- **Change notices to guests.** An email or SMS when information changes.
- **PC layout.** A layout that uses the larger screen on a PC.

### 3.4 Out of scope

- **Payment.** Online payment, and Vipps payment requests sent to guests.
- **Sending.** The site sending invitations or reminders; the couple does this by hand.
- **Hardingasete.** The site sending numbers to Hardingasete; the couple emails them.
- **Guest logins.** Guest accounts and passwords; the link is the login.
- **AI.** AI features in the site.
- **Activity sign-up.** Sign-up for the treasure hunt, sauna and hot tub, or yoga; these are information only (Q6).
- **Cabin allocation.** Deciding who sleeps in which cabin; the couple does this outside the site.
- **Payment code.** A household code in the payment message (D8).
- **Lost links.** Self-service link recovery; the couple resends links by hand.
- **Change emails.** Email to the couple when a guest changes an answer.
- **Deadline rules.** A grace period after the deadline (D5).
- **Conflicts.** Conflict detection when two people save at the same time; the last save applies (C5).
- **Guest list for guests.** A "who's coming" list that guests can see; it would show guests who else is coming.
- **Children.** Children and child prices; the wedding is child-free.
- **Diagnoses.** Diagnoses in allergy information.
- **Hosting for the course.** Hosting for the course delivery.

## 4. User Journeys

### UJ-1: Bestefar Sigmund answers for himself and bestemor

**Sigmund, 78**, is not used to technology. He gets a text message with a link and opens it on his phone.

1. **First impression.** He sees an invitation: Rikke and Valdemar are getting married on Saturday 27 May 2028 at Hardingasete, and **he and bestemor** are invited. The RSVP deadline and a clear RSVP button are visible without scrolling. *(If time: a green envelope sealed with "R & V" opens and unfolds into the invitation the first time he visits.)*
2. **He scrolls.** Below the invitation he finds short cards for the programme, practical information, Hardingasete and the area, and about the couple. Each card opens its own page through "Read more", so the RSVP button never drowns. The button is repeated at the bottom.
3. **He starts his answer.** The form already shows "I am Sigmund", because it is his link. He could change it if bestemor were using his phone. Then he answers step by step for both of them: who is coming, which days, which meals and whether they stay overnight. Prices are shown before he chooses. Where he needs more context, for example about the cabins at Hardingasete and what they cost, a "Read more" box opens inside the step, so he never leaves the form. If he tries to leave before sending, the site tells him his answer is not sent yet.
4. **Allergies (optional).** He fills in bestemor's dietary needs and confirms that she knows about it and agrees.
5. **Check before sending.** He sees all answers and the household total, and can change anything that is wrong.
6. **Thank you.** He gets a clear confirmation that matches the answer:
   - Coming: "Thank you for taking the time to answer – we look forward to celebrating the big day with you!"
   - Not coming: "We're sorry you can't make it, but we completely understand."
   - Both end with: "You can now safely close the invitation."
7. **Payment.** He chooses to pay now or later.
   - **Now:** he sees the amount, the Vipps number (and a QR code, if time), the account number and the message to write ("Bryllup Sigmund"). Afterwards he can tap "I have paid".
   - **Later:** he is told that the same link always shows what he owes and how to pay.

**Done when:** Sigmund knows the answer is received, knows what he owes, and knows the link will always show his answer again.
**Biggest risk:** too much happening at once and too many things asking for his attention. Every screen must have one obvious next step.

### UJ-2: Onkel Arild answers for a household where not everyone comes

**Arild** answers for himself, **tante Marie**, **Filippa** and **Leone**. Both daughters are adults who still live at home.

1. **One answer for everyone.** He opens his own link, and the form shows "I am Arild". The first question asks whether all four are coming the whole weekend. Nothing is ticked in advance. He answers "No", and the form then lets him say that **Leone is not coming** and that **Filippa is only coming Saturday and Sunday**.
2. **The form adapts.** It asks nothing more about Leone. Filippa is only offered the meals on the days she is there, and Saturday breakfast is only offered to those who arrive on Friday. When he reaches accommodation, the form says clearly that a cabin is booked for the whole weekend: Filippa can sleep there one night, but pays for both. The total matches exactly what was chosen.
3. **He checks, sends and pays**, as in UJ-1.
4. **A change of plans.** Two weeks later, before the deadline, the RSVP button has become **"See or change answer"**. The top of the form shows what was answered, by whom and when. He changes the answer.
   - If the total goes up, he sees what remains to pay.
   - If it goes down, he is told the couple has been notified and will refund the difference.
5. **Marie opens her own link.** She sees that Arild has already answered and when, instead of an empty form, so the household never sends two answers.
6. **After the deadline** the form is locked, and the page tells them to contact the couple directly.

**The couple** sees the household marked "Changed" in the overview and can open a history of who changed what and when. When they have paid Arild back, they register the refund and the household's balance is zero again.

### UJ-3: Synne has lost her link

**Synne** is a friend. She got a new phone, and the message with her link is gone.

1. **She sends a message** to Rikke or Valdemar.
2. **Rikke finds Synne in the admin area on her phone**, copies Synne's link and sends it again.
3. **If a link has gone astray**, for example forwarded to the wrong person, Rikke deactivates it and creates a new one. Only that guest's link changes; the rest of the household keeps theirs. The old link only says that this is a private invitation and that the visitor should contact the couple the way they usually do. It shows no names, phone numbers or answers.
4. **After the deadline** the button only says **"See answer"**. Synne can see her household's answers but not change them, and she is told the deadline has passed and how to reach Rikke and Valdemar. She can still see how to pay, tap "I have paid", read the information pages, ask the couple a question and withdraw her allergy consent.
5. **Rikke fills in or changes the answer for her** from the admin area. If Synne tells Rikke about an allergy by phone, Rikke ticks that Synne consented verbally, and the site records who registered it and when.
6. **If something goes wrong**, such as an error message or a page that won't load, Synne still sees how to reach the couple. Their phone numbers are on every page.

### UJ-4: Rikke checks the numbers and sends them to Hardingasete

The RSVP deadline has passed, and Hardingasete needs the final numbers soon.

1. **Rikke logs in** and first sees a **summary**:
   - how many have answered yes, no, or not answered
   - guests per day and how many stay overnight (beds)
   - count per meal and per allergy type
   - interest in the Friday hike, and when people expect to arrive
2. **Directly below is "Needs attention"**: a clear list of what Rikke or Valdemar must handle. It shows households that haven't answered, unanswered guest questions, "I have paid" reports that don't match a registered payment, refunds owed, and households that have changed their answer. She marks each item as handled or seen, and it leaves the list.
3. **She trusts the numbers** because every count opens the people behind it. When she taps "12 for Friday dinner", she sees who the 12 are. She can also open the full overview of every household, person and answer, and count for herself.
4. **"Not answered" is clear**, with names. Rikke contacts them herself and adds a dated note to the household, for example "Contacted 12.01".
5. **She types the numbers into an email to Hardingasete**: meals, guests, beds, and allergies with names and counts. *(If time: a printer-friendly page with exactly what Hardingasete needs.)* The couple decides who sleeps in which cabin outside the site.

**The helpers** (toastmaster, maid of honour, best man) log in and see the same overview, but cannot change anything.

### UJ-5: Rikke follows up payments

Some Vipps payments and bank transfers have come in.

1. **Rikke checks Vipps and her online bank**, then registers each amount received on the site, for example "Received 900 kr".
2. **The site works out each household's status** from the amount: not paid, part paid (X missing), paid, or refund owed (X).
3. **If a guest has tapped "I have paid" but no matching payment is registered**, the household is **marked red** in the overview and listed under "Needs attention".
4. **Rikke sends reminders herself** by message, and adds a dated note that the household has been contacted. The same note shows in the not-answered list and the payment overview.

### UJ-6: Ingrid, the examiner, runs the app

**Ingrid** grades IBE160. She doesn't know the project and uses an ordinary PC.

1. **She clones the repo and reads the README.** It says what the app does and which tools and versions she needs, with commands she can copy.
2. **She installs and starts the app** with a few commands. She needs none of Rikke's accounts or keys; the example settings file (`.env.example`) works as it is.
3. **She fills the database with fictional guests.** They are the people from these journeys: Sigmund and bestemor, Arild's household, Synne, plus a few more households that cover the rest of the expected-results list. The README lists a test link per guest and logins for a test admin and a test helper.
4. **She opens a guest link** in a narrow window, like a phone, and goes through the whole RSVP flow. She tries wrong input and checks the receipt.
5. **She logs in as admin** and sees that the summary matches the expected-results list in the documentation.
6. **She tests the deadline** by moving it to yesterday in the admin settings. The guest can no longer change the answer; the admin still can.
7. **She sends a question as a guest.** It shows up in the admin area and is printed in the terminal, because no email key is set.
8. **She runs the tests with one command.** Among other things, they check that the admin counts match the expected-results list.

**Done when:** Ingrid has run the app and the tests in under 15–20 minutes without asking Rikke anything.

## 5. Functional requirements

### 5.1 Personal links and access

- **FR-1** Each guest has their own personal link with a long random code that cannot be guessed. The link is the guest's only login; guests have no accounts or passwords. [brief, UJ-1]
- **FR-2** A link opens the guest's household and nothing else: the invitation, the household's answers, its total and its payment status. [brief]
- **FR-3** Opening a link never changes anything. Only a deliberate action by the guest, such as pressing a button, saves data. Chat apps and email scanners open links by themselves. [C4, R 4.1]
- **FR-4** Page titles and link previews are the same for everyone and contain no names. [C7]
- **FR-5** Without a valid link, the site shows only a friendly message: this is a private invitation, and the visitor should contact the couple the way they usually do. This covers an unknown or deactivated link and the site's address on its own. The message shows no names, phone numbers, date or place. [UJ-3]
- **FR-6** With a valid link, the couple's contact details are on every guest page, including error messages. [UJ-3]

### 5.2 Invitation and information pages

- **FR-7** The front page looks like an invitation. Without scrolling on a phone, it shows the couple's names, the date and place, the names of the invited household, the RSVP deadline and the RSVP button. [UJ-1]
- **FR-8** Below the invitation are short cards for Programme, Practical information, Hardingasete and the area, and About us. Each opens its own page through "Read more". The RSVP button is repeated at the bottom. [UJ-1]
- **FR-9** The programme shows the weekend day by day, marks what costs money and says what to bring. Everyone sees every activity, including the Friday hike, so a guest who sees it can still decide to come on Friday. The treasure hunt, the sauna and hot tub, and yoga are information only, with no sign-up. [Q6, brief]
- **FR-10** The practical information covers the address, times, transport and parking, dress codes, house rules (child-free, little phone use) and what to bring. [brief]
- **FR-11** Every information page has an obvious way back to the invitation. [UJ-1]

### 5.3 RSVP form

- **FR-12** The form shows "I am [name]", already set to the link's owner. The respondent can switch to another member of the household. The choice records who answered. [C6, UJ-1]
- **FR-13** The form goes step by step, with one clear task per step, a visible Back link and a sign of how far the respondent has come. [D9]
- **FR-14** The first question asks whether everyone in the household is coming the whole weekend. Nothing is chosen in advance. Answering "No" lets the respondent mark who is not coming, and which days (Friday, Saturday, Sunday) each of the others comes. [UJ-2, D1]
- **FR-15** Later steps only ask about people who are coming, and only for the days they are there. A meal is offered only on days the person is present, and Saturday breakfast only to those present from Friday. [UJ-2]
- **FR-16** Each person who is coming answers yes or no to staying overnight. The form states clearly that a cabin is booked for the whole weekend and that both nights are paid, even if the guest sleeps there only one night. [D1, UJ-2]
- **FR-17** Each person present on Friday is asked about the Friday mountain hike: yes, no or maybe. Others are not asked. [brief]
- **FR-18** Expected arrival is optional and asked per person who is coming, with fixed choices including "Don't know". There are no time pickers. [D11]
- **FR-19** "Read more" inside a step, for example about the cabins and their price, opens in place, so the respondent never leaves the form. [UJ-1]
- **FR-20** Leaving the form before sending shows a warning that the answer is not sent yet. [UJ-1]
- **FR-21** Before sending, a check page shows every answer per person and the household total, with a "Change" link for each part. Optional questions that were skipped show as "Not provided". [D9, R 1.7]
- **FR-22** Errors appear next to the field, with a hint on how to fix them. After a failed attempt to continue, a summary at the top lists each error and links to its field. [R 3.5]
- **FR-23** After sending, a receipt confirms the answer with a message that fits it. There is one message for those who are coming and one for those who can't, and both end with "You can now safely close the invitation." [UJ-1]
- **FR-24** Once the household has answered, the link always opens its status: the answers, who last updated them and when, the total, how to pay and the deadline. [D9, UJ-2]

### 5.4 Allergies and consent

- **FR-25** Allergies and dietary needs are optional and given per person who is coming. They use fixed categories (gluten, lactose, nuts, shellfish, vegetarian, vegan, other) and a short note. No diagnoses. [D10, C2]
- **FR-26** Allergy information is saved only if the respondent gives consent through a separate Yes/No choice that starts unanswered ("I consent to …"). The text says:
  - what the information is for;
  - who can see it: the couple, toastmaster, maid of honour and best man;
  - that names and allergies are passed on to Hardingasete's kitchen;
  - that consent can be withdrawn through the same link.

  [C1, UJ-4]
- **FR-27** When the respondent enters allergies for others, they confirm that those people know about it and agree. [C2]
- **FR-28** The RSVP can always be sent without consent. In that case no allergy information is stored, and the guest is told they can tell the couple directly. [C1]
- **FR-29** The site stores when consent was given, who gave it and which version of the consent text was shown. [C1]
- **FR-30** Consent can be withdrawn through the personal link at any time, also after the deadline. Withdrawing deletes that person's allergy information and marks the household "Changed". [C1, UJ-3, GDPR Art. 7(3)]
- **FR-31** When the couple registers allergies for a guest, they confirm that the guest consented by phone or message. The site records who registered it and when. [UJ-3]

### 5.5 Prices, total and payment for guests

- **FR-32** The price of each paid option is shown before the guest chooses. The paid options are the cabin for the whole weekend, Friday dinner, Saturday breakfast and Sunday breakfast. A short, friendly note explains why guests pay: these are Hardingasete's prices, and the couple pays for Saturday lunch and dinner. [C3]
- **FR-33** The household total is visible along the way and is the same on the check page and the receipt. It is always calculated from the answers and the current prices, never typed in. [C3, D6]
- **FR-34** After sending, the guest chooses "Pay now" or "Pay later". [UJ-1, D8]
  - **Pay now** shows the amount, the Vipps number, the bank account number and the message to write, for example "Bryllup Sigmund".
  - **Pay later** explains that the link always shows what is owed and how to pay.
- **FR-35** The guest can report "I have paid". The report is stored with the time and shown to the couple. [UJ-1, UJ-5]
- **FR-36** If the total changes after a payment, the guest sees what remains to pay, or that the couple has been told and will refund the difference. [UJ-2]

### 5.6 Changing an answer, deadline and lock

- **FR-37** Before the deadline, once the household has answered, the RSVP button becomes "See or change answer" and opens the form with the answers filled in. [UJ-2]
- **FR-38** Before anyone edits, the form shows who last updated the answer and when. The last saved answer applies. [C5, UJ-2]
- **FR-39** Every change after the first answer marks the household "Changed" for the couple. [UJ-2]
- **FR-40** The full history of each household's changes (who changed what, and when) is kept. [UJ-2] **[2027]**
- **FR-41** The RSVP deadline is shown next to the RSVP button and on the receipt. [D4]
- **FR-42** After the deadline, guests can no longer change who is coming, days, meals, overnight stay, the hike, arrival or allergies. [D5, UJ-3]
  - The button says "See answer". The page explains that the deadline has passed and shows how to reach Rikke and Valdemar.
  - Payment information, "I have paid", the information pages, questions and consent withdrawal still work.
  - Households that never answered see the same message.

### 5.7 Questions to the couple

- **FR-43** An "Ask us" button on every guest page lets the guest send a short question. [brief]
- **FR-44** Questions are always stored and listed under "Needs attention". The couple answers outside the site and marks the question as answered. [brief]
- **FR-45** If an email key is configured, each question is also emailed to the couple. Otherwise it is written to the console. [brief]

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

### 5.10 Overview and "Needs attention"

- **FR-54** The admin home page starts with a summary: [UJ-4]
  - people and households who have answered yes, answered no, or not answered;
  - guests per day;
  - how many stay overnight (beds);
  - the count per meal and per allergy category;
  - interest in the hike;
  - expected arrivals.
- **FR-55** Every count opens a list of the people behind it. [UJ-4]
- **FR-56** Below the summary, "Needs attention" lists: [UJ-4, UJ-5]
  - households that haven't answered;
  - unanswered questions;
  - "I have paid" reports without a matching payment, in red;
  - refunds owed;
  - households marked "Changed".

  Each item can be marked as handled or seen, and then leaves the list.
- **FR-57** A full overview shows every household and person with their answers, contact details, total, payment status and notes. Households that haven't answered stand out. On a phone, a guest's phone number and email can be tapped to call or write. [UJ-4]
- **FR-58** An allergy list shows names and categories for everyone who consented, ready to pass on to Hardingasete. [UJ-4]

### 5.11 Payments

- **FR-59** The couple registers the amounts received from each household, and refunds paid back. A registration can be corrected or undone. [UJ-5]
- **FR-60** The site works out each household's payment status from the amounts: not paid, part paid (with the amount missing), paid, or refund owed (with the amount). [UJ-5]
- **FR-61** A household whose "I have paid" report has no matching registration is marked red in the overview and listed under "Needs attention". [UJ-5]
- **FR-62** Each household has one dated contact note, for example "Contacted 12.01: payment reminder". It shows both in the not-answered list and in the payment overview. [UJ-4, UJ-5] **[2027]**

### 5.12 Overrides and settings

- **FR-63** The couple can fill in or change any household's answer, also after the deadline. Such changes record the admin as the author. [UJ-3, D5]
- **FR-64** In the admin area, the couple can change the prices, the RSVP deadline, their contact details and the payment details (Vipps number and account number). Helpers cannot. [UJ-6]
- **FR-65** Changing prices after households have answered shows a warning with the number of households whose total will change. [UJ-6]

The text on the information pages lives in the code in v1, so changing it means changing the code (D12).

### 5.13 Privacy functions

- **FR-66** A privacy page explains: [R 3.3]
  - what is collected and why, including the phone numbers and email addresses the couple enters;
  - who can see it: the couple and the helpers, and for allergies also Hardingasete's kitchen;
  - the legal basis;
  - when it is deleted;
  - the guest's rights, including withdrawing consent and complaining to Datatilsynet;
  - how to contact the couple.

  It is linked from the bottom of every page and from the consent question.
- **FR-67** The couple can delete all guest data in one operation, after a clear confirmation. **[2027]**

### 5.14 Local setup and test data (course version)

- **FR-68** One documented command fills the database with fictional test data: [UJ-6]
  - the people from UJ-1 to UJ-3;
  - extra households that cover the expected-results list: one that has paid, one that hasn't answered, and a single guest with an allergy;
  - fictional contact details and a test link for each guest;
  - a test couple admin and a test helper.
- **FR-69** An expected-results list, worked out by hand for the test data, is documented and checked by the automated tests. [UJ-6, brief]

## 6. Non-functional requirements

### NFR-1 Reliability (Rikke's top priority)

- A guest's link keeps working from the day it is sent until the data is deleted. The domain and the link format are fixed before invitations go out and never change afterwards.
- Links work when sent by SMS, Messenger and email: they are short enough and use only characters that are safe in links. Before invitations go out, a test link is sent through all three channels and opened on both Android and iPhone.
- Saving either succeeds and says so, or fails with a clear message and keeps what the guest entered. Nothing is lost without the guest knowing.
- In production, the database is backed up daily, and restoring a backup is tested before invitations are sent.
- In production, the site is available from the invitations until the wedding, with no planned downtime in the last week before the deadline.

### NFR-2 Correct numbers

- All counts, totals and payment statuses are calculated from the stored answers and payments, never stored separately.
- Amounts are whole kroner.
- Automated tests check that the admin counts and totals match the expected-results list (FR-69).

### NFR-3 Privacy

- GDPR is assumed to apply, and allergies are treated as health data. [R 3.1, R 3.2]
- Only what is needed is collected. Guests are stored with a name and, optionally, a phone number and email so the couple can follow up. Allergies are categories and a short note, with no diagnoses.
- Only fictional data is used in the repository, tests, test data, screenshots, the usability test and AI tools.
- Real data lives only in the production database, hosted in the EU/EEA. Hosting and email providers that handle it have data processing agreements.
- Real data is deleted by 31 August 2028.

### NFR-4 Security

- Link codes have at least 128 bits of randomness and contain no personal data. [R 4.1]
- Guest pages are hidden from search engines and do not pass the link on to other sites. Repeated attempts with wrong links are slowed down. [R 4.1]
- Admin passwords are stored with a modern password-hashing method. [R 4.2]
- Admin sessions expire after a period of inactivity. [R 4.2]
- Forms are protected against forged submissions. [R 4.2]
- Repeated login attempts are slowed down. [R 4.2]
- Only logged-in admins see guest answers. The server, not just the page, stops helpers from changing data.
- No secrets in the repository. Real settings live in a settings file that Git ignores, and the example file contains no real values.

### NFR-5 Accessibility (self-imposed target: WCAG 2.2 AA)

- Text contrast is at least 4.5:1. This must be checked for sage green on soft white. [R 3.5]
- The site works at 200 % zoom and at 320 px width.
- Everything can be done with a keyboard, and the keyboard focus is always visible.
- Buttons and other touch targets on guest pages are at least 44 × 44 px. The WCAG AA minimum is 24 × 24 px; larger targets suit older guests.
- Every field has a label, and errors follow FR-22.
- The site does not ask for what the link already knows, such as names.
- Any animation respects the phone's "reduce motion" setting and can be skipped.

### NFR-6 Ease of use

- Phone first, for all ages. A PC shows the phone layout; a wider layout is If time.
- Every screen has one obvious next step.
- Plain, warm Norwegian (bokmål) with a cosy tone, also in error messages.
- An older guest can complete a household RSVP without help in under 10 minutes (SM-3).

### NFR-7 Performance and size

- Pages load in under 3 seconds on an ordinary phone on 4G.
- Sized for about 70 guests and 5 admin users. No further scaling is needed.

### NFR-8 Runnability (course version)

- The app runs locally on an ordinary PC (Windows, macOS or Linux) by following the README. It needs no separate database server and none of Rikke's accounts or keys.
- Without an email key, emails are written to the console.
- Filling the database with test data is a separate, documented step.
- Installing, starting and running the tests take no more than 15–20 minutes (SM-5).

### NFR-9 Maintainability

- The code is checked by a linter and a formatter.
- All automated tests run with one command.
- Settings that differ between local and production are documented in `.env.example`.
- Stories refer to the requirement IDs in this PRD, so every feature can be traced back to a requirement.

## 7. Constraints, dependencies and assumptions

### Constraints

- **Team.** Rikke is a solo developer, early in learning to program. She builds with AI assistance, using the BMAD method.
- **Dates.** The course delivery is due mid-December 2026, and the usability test is in the first week of December 2026.
- **Course requirement.** The app must be full-stack with one database. The technology is chosen in the architecture document.
- **No AI in the site.** It would add cost, and the course does not require it.
- **Payment outside the site.** Guests pay by Vipps or bank transfer to the couple.

### Waiting for Hardingasete (asked 2026-11-06)

- **Q1: Beds and cabins.** Answered for capacity: Hardingasete has far more beds than there are guests, so the form needs no bed limit (Rikke, 2026-11-07). The couple allocates the cabins outside the site.
- **Q2: Final numbers.** When and in which format Hardingasete needs the final numbers. This sets the RSVP deadline, about two weeks earlier, and what the overview must show.
- **Q3: Prices.** The prices per meal and for the cabin. These are entered as settings (FR-64).
- **Q4: Payment.** Whether guests may pay Hardingasete directly. This may change FR-34.

### Assumptions

- Guests get their link digitally and can open it on a phone or a PC.
- The couple sends all links and reminders themselves.

## 8. Open questions

| ID | Question | Owner | Blocks the PRD? | Revisit when |
|---|---|---|---|---|
| Q2–Q4 | Hardingasete's answers (section 7) | Rikke | No | Hardingasete replies |
| Q7 | How do two or three guests, including older ones, feel about paying for meals? Affects the wording in FR-32. | Rikke | No | Before the UX text is written |
| Q8 | Is the teacher fine with the consent model differing from the first brief? Must the expected-results list be in the PRD, or only in the tests? | Rikke | No | Next supervision |
| D14 | Store link codes hashed or in plain form? | Architecture | No | bmad-architecture |
| D15 | Database and technology stack | Architecture | No | bmad-architecture |
| D16 | Email provider in production; it must store data in the EU | Rikke | No | 2027 |

## 9. Changes from the product brief

Decided during the PRD on 2026-11-07. Each change is logged in `.memlog.md`.

| Topic | Brief | PRD | Why |
|---|---|---|---|
| Helpers | Full access for all admin users | Helpers can see but not change (FR-46) | Rikke wants only the couple to change data |
| Payment status | Paid or not paid, with undo (D6) | Amounts are registered, and the status is calculated: not paid, part paid, paid or refund owed (FR-59, FR-60) | Rikke needs "part paid"; a status calculated from amounts can't drift away from the money actually received |
| "I have paid" | Optional (D6) | In v1 (FR-35, FR-61) | Catches mismatches and avoids wrong reminders |
| Links | One per guest (brief); research assumed one per household | One per guest, with "I am …" already set to the owner (FR-1, FR-12) | Doesn't ask for what the link knows (WCAG 3.3.7), and deactivating a link affects only one person |
| Allergy recipients | The consent names who can see the data | The consent also says that names and allergies go to Hardingasete's kitchen (FR-26) | The couple emails the allergies with names |
| Gift list | Form open | Simple text page with links, If time | Decided by Rikke |
| Guest contact details | Not specified | Optional phone and email per guest, entered by the couple (FR-49) | Makes follow-up easier for the couple. Claude proposed storing names only (data minimisation); Rikke chose otherwise, and the privacy page explains it (FR-66) |
| New in v1 | — | "Needs attention" (FR-56), counts that open the people behind them (FR-55), the "Changed" marker (FR-39), settings in admin with a price warning (FR-64, FR-65), the privacy page (FR-66), verbal consent recorded by the couple (FR-31) | Came out of the user journeys |
| Dropped | — | Email to the couple when an answer changes | Rikke: the overview is enough |
