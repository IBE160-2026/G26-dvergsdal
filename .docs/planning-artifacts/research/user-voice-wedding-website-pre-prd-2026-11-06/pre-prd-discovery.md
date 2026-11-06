---
title: "Pre-PRD discovery: open questions, decisions, ideas and topics"
project: "AI'll handle it"
created: "2026-11-06"
updated: "2026-11-06"
status: draft
inputs:
  - "../../briefs/brief-aill-handle-it-2026-09-23/brief.md"
  - "../../briefs/brief-aill-handle-it-2026-09-23/addendum.md"
  - "../../briefs/brief-aill-handle-it-2026-09-23/tilbakemelding-product-brief.md"
  - "research.md (this folder)"
---

# Pre-PRD discovery: AI'll handle it

This note is the working basis for the PRD. It brings together what is still unclear in the brief, what the research in [research.md](research.md) shows, and which decisions need to be made before or during the PRD. References like **[R 1.3]** point to sections in research.md.

The research is evidence; this note is analysis. Where a recommendation is given, it says what it rests on.

## 1. Findings that challenge the brief

These should be discussed first, because they change something the brief already says.

| # | The brief says | The research shows | Proposal | Basis |
|---|---|---|---|---|
| C1 | "Without the consent box ticked, the answer can't be sent." | GDPR Art. 7(4): consent that a service depends on is presumed not freely given. Allergies are most likely health data (Art. 9). | Separate the consent from the RSVP itself: attendance, options and arrival can always be sent; the allergy field is optional and has its own consent box (Yes/No, unticked, "I consent to …"). Tell guests before they consent that they can withdraw it; store the time and text version; allow withdrawal through the same link. Guests who don't consent can tell the couple directly. | [R 3.2] |
| C2 | One person answers for the whole household, including allergies. | Consent is the person's **own** statement (EDPB). Third-party consent is described only for parents of children. Helsedirektoratet: relatives cannot consent on behalf of an adult. No source supports one adult consenting for another. | Proposal: the respondent fills in allergies per person and ticks "I confirm that the people I am answering for know about this and agree" + data minimisation (categories + short text). Document the residual risk honestly. Alternative: each adult confirms their own entry (safer, but breaks the "one person answers" flow). Children are not relevant (child-free). | [R 3.2, 5] |
| C3 | Guests pay for meals (Fri dinner, Sat and Sun breakfast) and the cabin. | US etiquette: guests paying for **accommodation** is accepted if it is optional and known up front; paying for **meals** is often seen as "tacky". In Scandinavia guests often pay for their own stay. No Norwegian source on guests paying for meals was found. | Keep it, but present it well: show prices **before** the form asks, explain why (Hardingasete's prices, the couple pays for Saturday lunch and dinner), use a friendly tone, and never let the total change unexpectedly. Consider asking a few guests how it comes across. | [R 1.6, 2.1, 2.2] |
| C4 | "Link tracking: which households have opened their link." | Messenger, WhatsApp and Slack fetch the link themselves when it is sent; email scanners create false opens. "Opened" based on page loads will be wrong. | Define "opened" as "the guest has done something" (e.g. clicked "Start" or saved), or filter known bots. Otherwise drop the feature. | [R 4.1] |
| C5 | "If two household members answer, the last save wins, and the form shows who last updated it and when." | Last-save-wins without a check can silently overwrite the other person's answer. The standard pattern is a version column with a conflict message. | Choose between (a) last-save-wins + visible "last updated by …" (simplest, as in the brief), and (b) optimistic locking with a conflict message. Recommendation: (a) for guests, but show "updated by X at Y" **before** they start editing; (b) only if it costs little. | [R 4.5] |
| C6 | Who answered is shown by name ("who last updated it"). | The guest is identified only by the household link, not as an individual person. | Decide how "who" is captured: the respondent chooses "I am …" from the household's names at the start. | Analysis |
| C7 | The personal link is the login. | The link's title and preview image are shown in the chat and cached by Meta. | The page title and `og:` tags must be generic, with no names. | [R 4.1] |

### Decided 2026-11-06 (Rikke)

All seven proposals were accepted. The brief was updated the same day (see its change log).

| # | Decision |
|---|---|
| C1 | Accepted. The consent is separated from the RSVP: the answer can always be sent; the allergy field is optional with its own consent. |
| C2 | Accepted. The respondent fills in allergies per person and confirms that the others know about it and agree. Categories + short text. The residual risk is documented in the brief. |
| C3 | Accepted. Prices are shown before the choices, with a short explanation and a total that doesn't change unexpectedly. |
| C4 | Accepted. "Opened" means that the guest has done something on the site, not that the page was loaded. |
| C5 | Option (a): last save wins, and "last updated by X at Y" is shown before anyone starts editing. |
| C6 | Accepted. The respondent chooses "I am …" from the household's names at the start. |
| C7 | Accepted. Page title and preview are generic, with no names. |

## 2. Decisions that must be made (and when)

**Before the PRD** = affects scope or requirements. **In the PRD** = can be decided while writing. **Architecture** = belongs in the architecture document.

| # | Decision | Options | Research-based proposal | When |
|---|---|---|---|---|
| D1 | Unit of attendance: per person per weekend, or per person **per day/event**? | (a) one yes/no for the whole weekend + options; (b) yes/no per day (Fri/Sat/Sun) | (b) gives correct counts if some people come only Saturday. Fits the git-hitched and Joy models. | Before PRD |
| D2 | Can a guest come only for the wedding day without accommodation? | Yes / no | Probably yes (accommodation is "the whole weekend or none"). Then meals must be chosen independently of accommodation. | Before PRD |
| D3 | Consent model (C1, C2) | See section 1 | See section 1 | Before PRD |
| D4 | RSVP deadline in relation to Hardingasete's deadline | Fixed date in config / admin setting | Guests' deadline about **2 weeks before** the venue's deadline for final numbers. Make the date configurable. Show the deadline next to the button and on the confirmation page. | In PRD (date: ask Hardingasete) |
| D5 | What happens after the deadline? | Locked for guests, admin can edit (brief) + grace period? | Lock as the brief says, plus a clear message with contact info. A grace period isn't needed when the admin can override. | In PRD |
| D6 | Payment status | Paid / not paid; or + "partly paid"; or amount paid | Two states + undo is enough for v1. Optional: "I have paid" self-report from the guest. Store amounts as whole øre/kroner, and always calculate totals. | In PRD |
| D7 | What happens if the total changes after payment? (admin edits, guest changes before the deadline) | Show the difference / reset status | Show "paid X, now owes Y" in admin. Must be decided, otherwise the numbers get messy. | In PRD |
| D8 | Payment reference | Household name / short household code | Short household code in the Vipps/bank message, shown on the receipt page. | In PRD |
| D9 | Form structure | Everything on one page / one step at a time (GOV.UK) / per person | Step by step with a "check your answers" page before sending, and a receipt page after. Keep the number of steps low (e.g. attendance → options → allergies → arrival/hike → check). | In PRD / UX |
| D10 | Allergy field | Free text / predefined options + free text | Predefined options (gluten, lactose, nuts, shellfish, vegetarian, vegan, other) + short free text. Gives counts in admin and helps data minimisation. Label: "Allergies or dietary needs the kitchen must know about". | In PRD |
| D11 | Arrival time | Free text / fixed choices | Fixed choices (Friday morning, Friday afternoon, Friday evening, Saturday morning) + optional comment. Avoids time pickers, which older users struggle with. | In PRD |
| D12 | Content management | Info pages in code / editable by admin | In code for v1 (simplest). Prices and the deadline as settings in admin or config, since prices aren't known yet. | In PRD |
| D13 | Helper roles | Everyone full access (brief) / limited roles | The brief says full access; the research shows limited roles are a gap in the market, but that's not necessary for 4 trusted people. Keep full access, and note it as a conscious choice. | Already decided, confirm |
| D14 | Hashed or plain tokens | Hashed / plain | Hashed is safer; plain lets admin copy the link again. Proposal: plain + regenerate option in v1 (simple), or hashed + "generate new link". | Architecture |
| D15 | Database and stack | SQLite / Postgres; Django / Laravel / JS stack | SQLite gives clone-and-run without setup. Stack is decided in architecture. | Architecture |
| D16 | Email in production (2027) | Resend / Postmark / Brevo / … | Check where data is **stored**, not just the send region (Resend stores in the US). | Later (2027) |

### Decided 2026-11-06 (Rikke)

| # | Decision |
|---|---|
| D1 | Per person, the form asks: are they coming, which days (Fri/Sat/Sun), which meals, and are they staying overnight. Hardingasete confirmed that accommodation is the whole weekend or nothing, so overnight is a single yes/no. |
| D2 | Yes. A guest can come without accommodation, for example only for the wedding day, and chooses meals independently of accommodation. |
| D3 | Decided as C1 and C2. |
| D4 | Accepted. The RSVP deadline is configurable and set about two weeks before Hardingasete's deadline, and it's shown next to the button and on the receipt page. |
| D5 | Accepted. Locked for guests after the deadline, with a clear message and contact info. No grace period; the admin can override. |
| D6 | Accepted. Paid / not paid with undo. Amounts are stored as whole numbers, and totals are always calculated. The "I have paid" self-report remains optional. |
| D7 | Accepted. If the total changes after payment, the admin sees "paid X, now owes Y". |
| D8 | **Changed.** No household code. The payment message only needs to show that it's for the wedding (for example "Bryllup" + name), because the couple won't receive many Vipps payments. |
| D9 | Accepted. Step by step with a check page before sending and a receipt page after. |
| D10 | Accepted. Predefined allergy categories + short free text. |
| D11 | Accepted with an addition. Fixed choices for arrival time, but optional and with a "Don't know" option. |
| D12, D13 | Not decided yet. Taken into the PRD. |

## 3. Information we must get from outside

These can't be answered with web research. They have to be asked.

| # | Ask whom | Question | Why it matters |
|---|---|---|---|
| Q1 | Hardingasete | How many beds/cabins are there, and how are they allocated (per person, per cabin)? | Bed limit, price model, and whether the admin needs to allocate cabins |
| Q2 | Hardingasete | When do they need final numbers for meals, beds and allergies? In what format? | Sets the RSVP deadline (D4) and what the admin overview/print should look like |
| Q3 | Hardingasete | Prices per meal and accommodation (or when they'll come)? Prices for children are irrelevant (child-free) | Price model, configurable prices |
| Q4 | Hardingasete | Should guests pay the couple, or can they pay Hardingasete directly? | Etiquette (R 2.2: paying a third party feels better), payment flow |
| Q5 | The couple | Can someone come only Saturday? Only Friday? | D1, D2 — answered 2026-11-06: yes, guests choose days and meals independently of accommodation |
| Q6 | The couple | Should Friday activities (treasure hunt, sauna) and Saturday yoga have sign-up, or just be information? | Scope of the form |
| Q7 | 2–3 guests (incl. an older one) | How does "pay for meals" come across? What would you look for on the site? | C3, information architecture |
| Q8 | The course teacher | Is it OK that the consent model differs from the brief, if it's justified? Does the "fasit" test list need to be in the PRD or only in tests? | C1, criterion 3 |
| Q9 | Check your own Vipps app | The terms (v1.5) say a personal QR code exists and that private persons can receive money "for private purposes", but they say nothing about websites. Find your own QR code in the app and decide: show the phone number only, or the QR as well? | Payment info on the receipt page. Avoid "payment request" without prior agreement (the terms forbid it) |

## 4. Users' needs (summary)

The full jobs-to-be-done table is in [R 2.3]. The most important needs, with the requirement each points to:

**Guests**
- See right away who in the household is invited and what needs to be done by when → the landing page after the link shows the household's names, the deadline and a "Start" button.
- Not have to search for themselves → personal link (already in the brief, strongly supported by research).
- Know it worked → receipt page + the link always opens the household's status.
- Know the cost before committing → prices visible before the form, the total shown along the way and unchanged at the check step.
- Not be afraid of doing it wrong (older guests) → large text, large buttons, a Back link, errors at the field, an error summary, a phone number to the couple on every page.
- Find the practical information fast → a scannable "Practical" page ordered by day (time, address, parking, transport, dress code, what to bring, weather).

**The couple**
- Reliable numbers per meal, day, bed and allergy → admin overview + printable page/CSV.
- Who is missing, and how to reach them → "not answered" list with phone/email.
- Who owes what and who has paid → payment overview per household.
- Register answers for guests who call → the admin can fill in the form on behalf of a household (the human fallback for older guests).

**Helpers**
- See what concerns them without asking → shared admin (already in the brief). Speech sign-up to the toastmaster (if time allows; research shows sign-up is often hidden from the couple).

## 5. Ideas and features worth discussing

Sorted by how strongly the research supports them. "Scope" proposes where they belong in the brief's split.

| Idea | Basis | Proposed scope |
|---|---|---|
| Check-your-answers page before sending, with "Change" per person | GOV.UK, Baymard [R 1.7] | Must (part of the RSVP) |
| Receipt/status page that the link always opens (amount, reference, account/Vipps, status, deadline) | GOV.UK confirmation, Tito [R 1.7] | Must |
| "Not answered" list with contact details | Couples' biggest pain [R 2.1] | Must (part of admin) |
| Admin can answer on behalf of a household | Older guests use phone/paper [R 2.2] | Must (part of "editing and overrides") |
| Attendance per day | Correct counts [R 1.2] | Must, if D1 = (b) |
| Contact info (phone) on every page | Older guests, "guests ask anyway" [R 2.2] | Must (cheap) |
| Generic link preview (no names in title/og) | Meta/WhatsApp [R 4.1] | Must (security, cheap) |
| Admin can regenerate a household's link | OWASP, lost links [R 4.1, 2.2] | Must (small) |
| Predefined allergy options + counts | Data minimisation, caterer [R 3, 2.1] | Must |
| CSV export / print page for Hardingasete | Standard in all products [R 1.4] | If time (already in the brief) |
| "I have paid" self-report from the guest | Reduces chasing [R 1.7] | Discuss |
| Reminders (manual list) | Joy, chasing [R 1.3, 2.1] | Out (the couple sends them themselves); the list in admin is enough |
| QR code with the personal link on a paper card for the oldest guests | Paper is still valued [R 2.2] | Outside the site (couple's choice); possible later |
| Language preset per household (English for those who need it) | Language research [R 2.2] | If time (with the English version) |
| Speech sign-up only the toastmaster sees | Swedish example [R 1.6] | If time (already in the brief) |
| "Who's coming" list visible to guests | Not researched; privacy risk | Discuss, probably no |
| Letter animation | No evidence for or against among older guests; respect "reduce motion" | If time (already in the brief); must be skippable |

## 6. Research topics still open

| Topic | Why it's open | How to close it |
|---|---|---|
| Norwegian norms for guests paying for meals at a wedding weekend | Not found online | Ask 2–3 guests (Q7); possibly Kvinneguiden forum |
| Norwegian user voice on wedding sites | Reddit/Norwegian forums not reachable to the tools | The usability test in December + conversations with guests |
| How older guests react to an animated envelope | No evidence found | Test a prototype with one older relative |
| iMessage preview: which device fetches? | Conflicting 2020 sources | Test it yourself: send the link to yourself and check the server log |
| Hardingasete's numbers and deadlines | Not public | Ask (Q1–Q4) |
| Is a confirmation enough when one person enters allergies for another adult? | No source found (datatilsynet.no could not be read) | Ask Datatilsynet's advice line (phone/email), or choose the minimisation solution in C2 |
| Does the household exemption cover a closed wedding site? | No source | Keep the conservative assumption (GDPR applies) and write it down as a decision |

## 7. Brainstorming topics (for a session with `bmad-brainstorming` or on your own)

1. **The first 10 seconds after the link:** what should the guest see first? Greeting by name, picture, deadline, "Start"? How does it feel personal without the letter animation?
2. **The money talk:** how do we say "you pay for meals and the cabin" warmly and clearly? Wording, placement, why.
3. **The RSVP flow for a family of four:** draw the steps on paper. How many screens? What if one person isn't coming?
4. **What the couple needs on Hardingasete's call:** design the admin overview from the questions the venue will ask.
5. **The weekend programme as a page:** day by day, with what's optional and what costs money, and what guests should bring (hiking boots, swimwear for the hot tub).
6. **Tone and language:** formal or personal? "Dere" or "du"? Humour in the error messages?
7. **Edge cases:** a guest who changes their mind after paying; a household that splits up; someone who loses the link; two people answering at the same time; someone coming only Saturday.
8. **The test list with fasit:** which fictional households cover all the rules (couple both coming, family with one not coming, single person with allergy, guest only Saturday, household that has paid, household that hasn't answered)?

## 8. "Fit for fight": checklist before the PRD

- [x] C1–C7 discussed and decided (section 1) — 2026-11-06
- [x] D1–D13 decided or explicitly moved into the PRD (section 2) — D1–D11 decided 2026-11-06; D12–D13 moved into the PRD
- [x] Questions Q1–Q4 sent to Hardingasete (the answers can come during the PRD; prices and deadlines are configurable) — sent 2026-11-06, awaiting reply
- [ ] Q5–Q6 answered by the couple
- [x] Brief updated with what changes (C1, C2, C3, C4, C6, C7), with a change log entry — 2026-11-06
- [ ] Start `bmad-prd` with the brief, the addendum, research.md and this note as input
