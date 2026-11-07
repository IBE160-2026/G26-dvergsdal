# Review: Bestefar Sigmund walks the guest flow

> **Lens:** the most vulnerable guest. **Reviewed:** `prd.md` (draft, 2026-11-07) with `addendum.md` and `.memlog.md`. Background: `research.md` §2.2 (older users make more mistakes, blame themselves, miss vague errors, struggle with small text and strict formats [41]; about half of couples kept paper or phone for the oldest guests [40]). **Focus:** UJ-1 to UJ-3, FR-1 to FR-45, NFR-5, NFR-6. **Date:** 2026-11-07.

**Persona.** Sigmund, 78. Uses his phone for calls and texts, reads with glasses, is a little unsure of himself and blames himself when something goes wrong. He answers for himself and bestemor. Rikke sends him the link by SMS.

**Scenario walked.** Sigmund comes the whole weekend. **Bestemor comes only Saturday and Sunday.** Bestemor cannot eat gluten (fictional). Both want a cabin. Sigmund wants to pay at once, comes back later, changes the answer, and finally asks the couple a question.

**Verdict.** The PRD aims at Sigmund in the right way: a personal link with no name search and no password, "I am Sigmund" already set, one step at a time, prices before choices, a check page, a warm receipt, the couple's phone numbers on every page, and a human fallback where the couple fills in for him. The whole-household happy path is close to good. **The bestemor-only-Saturday-and-Sunday path is not.** It breaks at the first question (FR-14), where the honest answer "No" feels like declining and the easy answer "Yes" books bestemor for Friday. After that, several moments are underspecified in ways that give him silent wrong data or a reason to call: what a "day" means for someone who sleeps over, what happens to bestemor's allergy if the consent is left open or answered "No", the check page that looks like a receipt, losing the form when he is interrupted, and what he sees after tapping "I have paid". Most fixes are a sentence or two in the FRs, not new features.

**Counts:** 1 critical, 6 high, 11 medium, 9 low.

**How to read the findings.** Each finding gives severity, location, what Sigmund experiences, why it matters, a **PRD fix** (requirement level) and **UX phase** detail (for `bmad-ux`, no PRD change needed).

- **Critical:** likely to produce wrong data that looks right, or to stop him finishing.
- **High:** likely to cause a call, a give-up or a silent error on a common path.
- **Medium:** hesitation or a call on a less common path, or a gap that makes a high risk more likely.
- **Low:** polish, or rare.

## Walkthrough

Each step lists what the PRD gives him, where he hesitates (with finding numbers), and the load: **decisions** he must make and **text blocks** he must read or ignore.

### 1. The SMS arrives (FR-1, FR-4, NFR-1, FR-52 [2027])

A message from Rikke's number with a long link full of random letters. If his phone shows a preview, it has no names in it (FR-4), so it says something generic. His bank and the police have told him for years not to tap links in SMS.

- **Hesitates:** "Is this one of those scam messages?" He may wait until he can ask someone (F16). If bestemor has no smartphone, her link may also come to his phone, and he has two nearly identical messages (F24).
- **Load:** 1 decision (tap), 1 text block.

### 2. The invitation (FR-7, FR-8, FR-41, UJ-1 step 1)

He sees the couple's names, Saturday 27 May 2028, Hardingasete, "Sigmund and bestemor" as the invited, the deadline, and a big answer button. This is good: it is personal, and he knows what to do and by when. *(If time: an envelope opens first. He may wait, tap at the wrong place, or wonder what "Skip" skips, F20.)*

- **Hesitates:** his phone is set to large text, or he holds it at arm's length. The PRD sets no minimum text size, so either the text is small or the large-text setting pushes the button below the fold (F7). The button is called "RSVP" in the PRD; on Norwegian paper invitations he knows "O.S.A." (F27).
- **Load:** 1 obvious decision (answer), up to 7 optional ones (4 cards, "Ask us", call, privacy). About 6 facts in the invitation plus 4 card teasers of 2 to 3 lines each.

### 3. Reading first (FR-8 to FR-11)

He opens "Practical information" and "Hardingasete and the area" before committing. Each page has a way back (FR-11). The programme marks what costs money (FR-9).

- **Hesitates:** at 78 he wants to know whether he can drive to the cabin, how far it is to walk, whether there are steps, whether the cabin has its own bathroom, and how hard the Friday hike is. FR-10 does not ask for any of this (F17).
- **Load:** 0 required decisions.

### 4. Starting: "I am Sigmund" (FR-12, FR-13)

The form says "I am Sigmund", with a way to change it. There is a Back link and a progress sign (FR-13).

- **Hesitates:** "I am answering for bestemor too. Should I pick her when I do her part?" If he switches, the site records bestemor as the one answering, and later as the one who gave consent (F11).
- **Load:** 0 to 1 decision.

### 5. The first question, with bestemor coming Saturday and Sunday (FR-14)

"Is everyone in the household coming the whole weekend?" Yes or No, nothing chosen.

- **Hesitates, and this is the key moment.** They are both coming, so "Yes" feels right, and "No" feels like declining the invitation. If he taps "Yes", bestemor is registered for Friday, offered Friday dinner and Saturday breakfast, asked about the hike, and counted for Friday, and nothing on the screen looks wrong to him. If he taps "No", the next screen asks him to mark "who is not coming". He may mark bestemor, because she is "not coming on Friday", and she disappears from the answer (F1).
- **Load:** 1 decision, then on "No" up to 7 more (coming or not for 2 people, then 3 days for him and 2 for her) on one screen.

### 6. Which days (FR-14, FR-15)

He ticks days for bestemor. She arrives Saturday, sleeps over and leaves after breakfast on Sunday. Is that "Saturday" or "Saturday and Sunday"?

- **Hesitates:** people think in arrival, departure and nights, not in a set of days. If he ticks only Saturday, she is not offered Sunday breakfast even though she sleeps there. Nothing stops "Friday and Sunday", or a day set without Saturday, the wedding day (F2).
- **Load:** up to 5 ticks.

### 7. Meals and prices (FR-15, FR-32, FR-33)

Sigmund is offered Friday dinner, Saturday breakfast and Sunday breakfast; bestemor is offered Sunday breakfast. Each shows a price, and a short note explains why guests pay. The total changes as he ticks.

- **Hesitates:** "Isn't breakfast included when you stay in the cabin, like at a hotel?" If meals are checkboxes, an unticked breakfast means "no", even if he just did not see it (F10). The friendly price note helps (Q7 is still open on how paying for meals feels).
- **Load:** 4 decisions, 1 note, 4 prices, a moving total.

### 8. Cabin (FR-16, FR-19, FR-32)

Each of them gets a yes or no for staying overnight, with a clear note that the cabin is booked for the whole weekend and both nights are paid. "Read more" opens in place.

- **Hesitates:** "We share one cabin. Is the price for the cabin or for each of us?" FR-16 says "a cabin is booked", which sounds like one per household (F9). "Why must bestemor pay for Friday night when she isn't there?" He wants to ask, but the "Ask us" button takes him out of the form (F4).
- **Load:** 2 decisions, 1 rule, 1 price, 1 optional "Read more".

### 9. Hike and arrival (FR-17, FR-18)

He is asked about the Friday hike (yes, no or maybe), and bestemor is not, which is right. Arrival is optional, per person, with fixed choices and "Don't know".

- **Hesitates:** they arrive together, but he must answer twice. Bestemor's choices may still include Friday times (F19).
- **Load:** 1 decision, 2 optional.

### 10. Allergies and consent, for bestemor (FR-25 to FR-29)

He ticks "gluten" for bestemor. Then comes a Yes/No that starts unanswered: "I consent to …", with text about the purpose, the four people who can see it, Hardingasete's kitchen and withdrawal, and a link to the privacy page. Then a second statement: he confirms that bestemor knows about it and agrees.

- **Hesitates:** "I consent? It is her allergy, not mine." Two legal statements that mean the same to him. To be safe he may answer "No", or leave the question open. The PRD does not say what happens to the gluten tick if the consent is left open, and on "No" he is told he "can tell the couple directly", but it is not said where or how clearly (F5). If the screen lists 7 categories and a note for both of them, it holds about 20 controls (F12).
- **Load:** 1 to 2 ticks, 2 statements, the heaviest text of the whole flow.

### 11. Check page (FR-21, FR-33)

Every answer per person, the household total, a "Change" link per part, "Not provided" for skipped questions.

- **Hesitates:** the page lists his answers, so it looks like a confirmation. He may think he is done and put the phone away before pressing send. Then the household is "not answered" and Rikke calls him (F3). He also cannot see what the total is made of (F9).
- **Load:** about 16 answer lines for two people, 8 to 10 "Change" links, 1 send button.

### 12. Receipt (FR-23, FR-41, UJ-1 step 6)

A warm message in Rikke's own words, ending "You can now safely close the invitation." This is good for him.

- **Hesitates:** right after being told he can close, he is asked "Pay now or Pay later?". Which is it? If the total is 0, he is still asked to pay. Only the "Pay later" branch tells him that the link shows everything again (F8).
- **Load:** 1 decision, 2 to 3 text blocks.

### 13. Pay now: Vipps or bank (FR-34, UJ-1 step 7)

He sees the amount, the Vipps number, the account number and the message "Bryllup Sigmund".

- **Hesitates:** he must carry three values to another app. "Who am I paying, and by when?" No pay-by date exists in the PRD (F8). A QR code (If time) cannot be scanned with the phone that shows it (F21).
- **Load:** leaves the site, about 5 steps in Vipps or the bank app, then back.

### 14. "I have paid" (FR-35)

He goes back to the SMS, taps the link again, and taps "I have paid".

- **Hesitates:** nothing in the PRD tells him what happens next. Tomorrow his page may still say "not paid", because Rikke has not registered the money yet. He worries, calls, or pays again. If he tapped it before paying, or by mistake, he cannot undo it (F6).
- **Load:** 1 decision.

### 15. Coming back and changing (FR-24, FR-37, FR-38, FR-36)

Two weeks later bestemor decides to come on Friday after all. The button now says "See or change answer", and the top shows who answered and when. Good.

- **Hesitates:** the form opens filled in, and he must walk all the steps again to change one thing, with a chance of changing something else by mistake (F13). If the couple changed prices in the meantime, his total differs from his receipt for no reason he can see (F23). The new amount to pay is shown (FR-36), which helps.
- **Load:** 7 to 9 screens again for one change.

### 16. Bestemor opens her own link (UJ-2 step 5, FR-38)

She sees that Sigmund already answered, and when, instead of an empty form. This is good. If both of them answer at the same time on two phones, the last save silently wins (F25).

### 17. After the deadline (FR-41, FR-42, FR-30)

The button says "See answer", and the page explains that the deadline has passed and how to reach the couple. Payment, "I have paid", the information pages and questions still work. Good.

- **Hesitates:** if he tries on the evening of the deadline day and it is already locked, he blames himself (F22). Consent withdrawal still works, so one wrong tap deletes bestemor's allergy, and after the deadline he cannot add it back (F14).

### 18. Asking a question (FR-6, FR-43 to FR-45)

"Ask us" is on every page. He types a short question with one finger.

- **Hesitates:** "Where will the answer come?" Nothing tells him, and the question is gone from his page afterwards (F15). He would rather call, and the numbers are on every page (FR-6), which is the most useful help in the PRD.

### Load per screen, bestemor Saturday and Sunday

| # | Screen | Required decisions | Optional | Text to read or ignore |
|---|---|---|---|---|
| 1 | SMS | 1 | – | 1 message |
| 2 | Invitation | 1 | 7 | invitation (6 facts), 4 teasers, contact, footer |
| 4–5 | "I am" + first question | 1 | 1 | question, "I am" line |
| 5–6 | Who and which days (after "No") | up to 7 | – | instructions |
| 7 | Meals | 4 | – | price note, 4 prices, total |
| 8 | Cabin | 2 | 1 | rule, price, "Read more" |
| 9 | Hike and arrival | 1 | 2 | 2 short questions |
| 10 | Allergies and consent | 2 if any allergy | up to 16 | consent text (4 points), privacy link |
| 11 | Check page | 1 | 8–10 | about 16 lines, total |
| 12 | Receipt | 1 | – | thank-you, deadline, total |
| 13–14 | Pay now, "I have paid" | 1 + payment outside | – | 4 payment values |

**About 20 to 22 required decisions on 9 to 11 screens, plus about 35 optional controls.** Every form screen also carries the same 5 to 6 fixed elements: progress, Back, total, "Ask us", two phone numbers and the privacy link (F12). That is doable in 10 minutes for a confident user. For Sigmund it is tight, and the time depends on F1, F2, F5 and F12 more than on his speed.

## Findings

### At a glance

| ID | Severity | Location | Finding | Fix level |
|---|---|---|---|---|
| F1 | Critical | FR-14 | First question: "No" feels like declining, "Yes" books bestemor for Friday | PRD |
| F2 | High | FR-14, FR-15, FR-16 | "Days" do not match nights; Sunday is unclear; days can contradict each other | PRD |
| F3 | High | FR-21, FR-7, FR-24 | The check page looks like a receipt, so he never sends | PRD |
| F4 | High | FR-20, NFR-1, FR-13, FR-43, NFR-4 | An interruption, the back button or a long pause loses the form | PRD |
| F5 | High | FR-26 to FR-29 | Consent for bestemor: two statements, "No" and "unanswered" undefined | PRD |
| F6 | High | FR-35, FR-2, FR-24 | "I have paid" has no after-state and no undo | PRD |
| F7 | High | NFR-5, FR-7 | No minimum text size; large text pushes the button down | PRD |
| F8 | Medium | FR-23, FR-34 | "Safely close", then "Pay now?"; zero total; no pay-by date | PRD |
| F9 | Medium | FR-16, FR-32, FR-21 | Cabin price per person or per cabin? Total not itemised | PRD |
| F10 | Medium | FR-15, FR-32 | An unticked meal means "no"; he assumes breakfast comes with the cabin | PRD + UX |
| F11 | Medium | FR-12, FR-29 | "I am" read as a switch per person, giving a false consent record | PRD + UX |
| F12 | Medium | NFR-6, FR-6, FR-43, FR-25 | Too many fixed elements per screen; heavy allergy step | PRD + UX |
| F13 | Medium | FR-37 | Changing one thing means walking every step again | PRD |
| F14 | Medium | FR-30, FR-42 | One tap deletes bestemor's allergy, which he cannot re-add after the deadline | PRD |
| F15 | Medium | FR-43, FR-44, FR-6 | "Ask us" gives no idea how or when the answer comes | PRD |
| F16 | Medium | FR-4, §3.2, FR-52 | The link looks like a scam SMS | PRD + UX |
| F17 | Medium | FR-9, FR-10, FR-19 | No mobility or comfort information for older guests | PRD (content) |
| F18 | Medium | SM-3 | The usability test measures speed, not correct answers | PRD |
| F19 | Low | FR-18 | Arrival asked twice; choices not filtered by first day | UX |
| F20 | Low | §3.3, NFR-5 | The envelope animation may stall him | UX |
| F21 | Low | FR-34, §3.3 | QR code on the same phone; recipient name and copy aids | UX |
| F22 | Low | FR-41, FR-42 | The exact moment of the lock is not defined | PRD |
| F23 | Low | FR-33, FR-65 | His total changes by itself after a price change | PRD |
| F24 | Low | FR-1, FR-12, FR-52 | Two links on one shared phone | UX |
| F25 | Low | FR-38 | Two people answering at once: silent overwrite | PRD (optional) |
| F26 | Low | FR-5 | The dead-link message must not make him feel at fault | UX |
| F27 | Low | NFR-6 | Words: "RSVP", "husstand", legal terms | UX |

### Critical

#### F1. [Critical] The first question makes the honest answer feel like declining

- **Location:** FR-14; UJ-1 step 3; UJ-2 step 1.
- **Sigmund experiences:** "Is everyone in the household coming the whole weekend? Yes / No." They are both coming, so he taps "Yes", and bestemor is booked for Friday, offered Friday dinner and Saturday breakfast and asked about the hike. Or he reads it carefully, taps "No" with a bad feeling ("we are coming!"), and on the next screen, "mark who is not coming", he marks bestemor because she is not coming on Friday. She drops out of the answer. In both cases the check page shows something that looks reasonable to him.
- **Why it matters:** wrong counts per day, meal and bed (SM-8), corrections after a phone call (CM-1), and a wrong total that he pays. The addendum rejected a pre-ticked "everyone is coming" because skimmers would sign up people who are not coming. An unticked Yes/No that bundles two questions (who, and how long) carries the same risk in another form. Bestemor's case is likely to be common among older couples, so it belongs in the SM-3 test.
- **PRD fix:** split FR-14 into two questions, with nothing chosen in advance:
  1. **Who is coming?** One answer per person (coming / not coming), plus a shortcut "None of us can come".
  2. **For those coming: the whole weekend (Friday 26 to Sunday 28 May) or only some days?** Asked per person. "Only some days" opens the day choice (see F2).

  Update UJ-1 step 3 and UJ-2 step 1 to match. Add a partial-days person to UJ-1, or at least to the SM-3 scenario (F18).
- **UX phase:** use weekday names and dates rather than "the whole weekend", and the person's name in each question ("Is bestemor coming the whole weekend?"). On the decline path, confirm warmly that nothing more is needed from them.

### High

#### F2. [High] "Days" do not match how a guest thinks about a weekend trip

- **Location:** FR-14, FR-15, FR-16.
- **Sigmund experiences:** bestemor arrives on Saturday, sleeps over and leaves after breakfast on Sunday. Is she there "Sunday"? If he ticks only Saturday, she is not offered Sunday breakfast, although she sleeps in the cabin. Nothing stops "Friday and Sunday" or a choice without Saturday, the wedding day.
- **Why it matters:** the Sunday breakfast count, the bed count and the total can be wrong without anyone noticing (SM-8, CM-1). The admin counts are built on these rules (FR-69), so ambiguity here is also ambiguity in the expected-results list.
- **PRD fix:** in FR-14 and FR-15, define presence in the guest's terms: per person, **arrival day and departure day**, or the rule "Sunday means sleeping at Hardingasete on Saturday night or coming for Sunday breakfast". Add consistency rules: the days are consecutive; staying overnight means being there the next morning, so that breakfast is offered; and a gentle, non-blocking question if Saturday is not chosen. Add these cases to the expected-results list (FR-69).
- **UX phase:** "When does bestemor arrive?" (Friday / Saturday) and "When does she leave?" (Saturday evening / Sunday). Repeat it back in words: "Saturday to Sunday, 1 night".

#### F3. [High] The check page looks like a receipt

- **Location:** FR-21; FR-7 and FR-24 (status on return).
- **Sigmund experiences:** the page lists all his answers, so he thinks he is done and puts the phone away. Nothing is sent. Weeks later Rikke calls about his missing answer, and he is sure he answered.
- **Why it matters:** the research names this exact error: some users confuse the review page with the confirmation page [R 1.7]. It adds calls and chasing (CM-2, SM-7). FR-20's warning will not catch a locked phone (F4).
- **PRD fix:** FR-21: the page title says what to do ("Check your answer before you send it"), the page says "Your answer has not been sent yet", and the button is named after the action ("Send answer"), easy to reach without long scrolling. FR-7 and FR-24: the front page always says the answer status in words, "Not answered yet" or "Answer sent on [date] by Sigmund", so the next visit shows whether it went through.
- **UX phase:** make the receipt look clearly different from the check page, for example a large tick and the thank-you as the heading.

#### F4. [High] Anything that takes him out of the form loses his answers

- **Location:** FR-20, NFR-1, FR-13, FR-43, FR-66, NFR-4; §3.3 "Unfinished answers" (If time).
- **Sigmund experiences:** halfway through he must ask bestemor whether she wants Sunday breakfast. The phone rings. He switches to SMS to ask his daughter about the cabin. He taps "Ask us" or the privacy link. He presses the phone's own back button to go one step back. Or he leaves the form open while he has coffee. When he returns, the phone may have cleared the page and the form is empty, or the send fails because the form's security check has expired.
- **Why it matters:** NFR-1 promises that "nothing is lost without the guest knowing", but FR-20's warning only covers links inside the site. Phone browsers cannot reliably warn when he switches apps or when the page is cleared from memory, and the browser's built-in "leave page?" dialog, where it exists, has fixed text that cannot be made warm. Redoing five minutes of work is where an unsure 78-year-old gives up or calls (SM-3, CM-2). Saving an unfinished answer is If time, so v1 has no protection at all.
- **PRD fix:**
  1. NFR-1: an unsent answer survives an interruption on the same device. The form keeps a draft on the device until it is sent, and clears it after sending. This is much smaller than the If-time "continue later".
  2. FR-13: the phone's back button does what the form's Back link does: one step back, answers kept.
  3. FR-43 and FR-66: inside the form, "Ask us" and the privacy page open in place, like "Read more" (FR-19), or keep the answers.
  4. NFR-1 and NFR-4: guest forms have no time limit. If a security check fails when he sends, the answers are kept and he can send again (WCAG 2.2.1).
- **UX phase:** say on the first step that he can take his time and that nothing is sent until the last step.

#### F5. [High] Consent for bestemor's allergy: two first-person statements and an undefined "No"

- **Location:** FR-26, FR-27, FR-28, FR-29.
- **Sigmund experiences:** "I consent to …" for her information, then "I confirm that she knows about it and agrees". Both mean the same to him, and the first one is about "I", while it is her allergy. To be safe he answers "No", or leaves the question open. The PRD does not say what happens to the gluten tick if the consent is left open. On "No" he "is told he can tell the couple directly" (FR-28), but not where or how clearly. He believes the kitchen knows.
- **Why it matters:** an allergy lost without him noticing is a food-safety risk and breaks SM-8. The couple cannot see it, since nothing is stored without consent, so only a phone call can catch it (CM-2). Two statements also add load (SM-3). CM-4 forbids pushing consent, but being clear is not pushing.
- **PRD fix:**
  1. Consent is asked per person whose information is entered, next to that person, and only when something is entered.
  2. When answering for another adult, FR-26 and FR-27 become one plain statement, for example "Bestemor knows about this and agrees that …", Yes / No. FR-29 records that Sigmund gave it on her behalf.
  3. Allergy information entered and consent left open is an error at the field (FR-22), never a silent drop.
  4. On "No", a plain message in place says the allergy will not be saved and the kitchen will not know unless he tells the couple, with their phone number. The check page shows "Allergy for bestemor: not saved (no consent)".
- **UX phase:** the consent text is at most three short sentences, with the rest on the privacy page. "No" stays as easy as "Yes" (CM-4). Test the wording with the SM-3 participant.

#### F6. [High] "I have paid" has no after-state and no undo

- **Location:** FR-35, FR-2, FR-24.
- **Sigmund experiences:** he taps "I have paid", and the PRD says nothing about what he sees next. The next day his page may still say "not paid", because Rikke has not registered the money yet. He worries, calls, or pays again. If he tapped before paying ("I will pay") or by mistake, he cannot undo it. His household turns red for the couple, and Rikke contacts him about money he has not sent.
- **Why it matters:** payment mismatches (CM-3), calls (CM-2), double payments that become refunds for the couple, and an older guest who feels accused.
- **PRD fix:** FR-35: a short confirmation ("Have you paid 2 400 kr? Yes, I have paid / Not yet"). After that, the status shows "You reported payment on [date]. The couple will confirm when the money has arrived." The report can be withdrawn. FR-2 and FR-24: the guest sees the payment status in guest words: "reported, waiting for the couple", "received, thank you", "X kr remaining" or "the couple will pay back X kr".
- **UX phase:** put "I have paid" below the payment details, not as the first button on the page.

#### F7. [High] No minimum text size, and large text pushes the button down

- **Location:** NFR-5, FR-7, NFR-6.
- **Sigmund experiences:** he reads with glasses and does not always have them at hand when an SMS arrives. Small text makes him squint or pinch-zoom, and then the form slides sideways. If his phone is set to large text, an iPhone does not enlarge web pages on its own, while Android may enlarge them so the answer button falls below the fold or the layout breaks.
- **Why it matters:** the brief asked for "large readable text" for guests, and NFR-5 lost it on the way. 200 % zoom and 320 px reflow are useful but desktop-style checks; on a phone, the base text size decides whether he can read the page. This affects SM-3 directly.
- **PRD fix:** NFR-5: a minimum body text size on guest pages (for example 18 px) with generous line spacing, and guest pages that work with the phone's larger-text settings on both Android and iPhone. FR-7: at large text sizes, the priority is names, date, deadline, then the button, and the button comes before the cards. Run SM-3 on the participant's own phone with his own settings (F18).
- **UX phase:** test with the largest system text on both platforms; avoid thin or light text on sage green.

### Medium

#### F8. [Medium] After sending, three next steps compete, and there is no pay-by date

- **Location:** FR-23, FR-34, FR-24, FR-64; UJ-1 steps 6 and 7.
- **Sigmund experiences:** "You can now safely close the invitation", and right after it "Pay now or Pay later?". Should he close or choose? Only the "Pay later" branch says that the link always shows what he owes. If the total is 0 (for example only Saturday, no cabin and no paid meals, or not coming), he is still asked to pay. And by when must he pay? The PRD never says.
- **Why it matters:** this is UJ-1's own biggest risk, too many things asking for attention at once. UJ-1 "Done when" requires that he knows the link shows his answer again, in every branch. Without a pay-by date he calls, pays late, or needs a reminder (CM-2, CM-3).
- **PRD fix:** FR-23: the receipt always says that the same link in his SMS shows the answer and the amount again, and "safely close" comes last, after the payment part. FR-34: the payment step appears only when the total is above 0; with 0, the receipt says there is nothing to pay. Add a pay-by date as a setting next to the deadline (FR-64), shown on the receipt and the status page (FR-24).
- **UX phase:** keep Rikke's "Pay now / Pay later" if the usability test shows it helps. Otherwise show the payment details directly with "You can pay now or later".

#### F9. [Medium] Is the cabin price per person or per cabin? The total is not itemised

- **Location:** FR-16, FR-32, FR-33, FR-21, FR-23.
- **Sigmund experiences:** "A cabin is booked for the whole weekend" sounds like one cabin for the two of them, and then the total is twice what he expected. "Why does bestemor pay for Friday night?" The check page shows the sum, but not what it is made of.
- **Why it matters:** a surprise in the total makes users stop recognising their order [R 1.7], and costs that appear late are what makes paying feel improper [R 2.2]. It leads to wrong amounts paid (CM-3) and calls (CM-2).
- **PRD fix:** FR-32: every price states its unit ("per person, whole weekend", "per person"). FR-16: "each person who stays pays for both nights", instead of "a cabin is booked". FR-21 and FR-23: itemise the total per person and per item.
- **UX phase:** show the both-nights rule on bestemor's own row: "Bestemor comes Saturday; the cabin is still X kr for the whole weekend."

#### F10. [Medium] An unticked meal means "no"

- **Location:** FR-15, FR-32, FR-21.
- **Sigmund experiences:** he assumes breakfast comes with the cabin, as at a hotel, and leaves the breakfasts unticked. On Saturday morning at Hardingasete there is no breakfast for him.
- **Why it matters:** with checkboxes, "no" and "did not see it" look the same, and the meal counts sent to Hardingasete are wrong (SM-8). The addendum's rule of nothing ticked in advance only protects him if every choice is answered actively.
- **PRD fix:** FR-15 and FR-32: each offered paid meal gets a yes or no per person, nothing chosen in advance, or the step states plainly that meals are not included in the cabin. The check page lists meals not chosen as "Not chosen". Add a gentle, non-blocking question when a cabin is chosen without the next morning's breakfast.
- **UX phase:** group meals by day and person; put "Breakfast is not included in the cabin" next to both the cabin and the meal choices.

#### F11. [Medium] "I am Sigmund" is read as a switch per person

- **Location:** FR-12, FR-29, FR-38.
- **Sigmund experiences:** he thinks he must switch to bestemor to fill in her part. The site then records bestemor as the one answering, and later as the one who gave consent herself.
- **Why it matters:** "who answered" becomes wrong (FR-38), and the consent record becomes false (FR-29). An accurate record of who confirmed what is the only safeguard behind C2.
- **PRD fix:** FR-12: the respondent answers for the whole household; the "I am" choice only records who is answering. It is shown once, at the start, as a sentence with a way to change it ("You are answering as Sigmund. Not Sigmund? Change"), not as a person picker on each step.
- **UX phase:** every per-person question uses the person's name ("Bestemor: …"), so he never needs to switch.

#### F12. [Medium] Too many fixed elements on each screen, and the allergy step is the heaviest

- **Location:** NFR-6; FR-6, FR-13, FR-33, FR-43, FR-66 (fixed elements); FR-25.
- **Sigmund experiences:** each form step carries the question and the controls per person, plus progress, Back, the total, "Ask us", two phone numbers and the privacy link: 5 to 6 things besides the task. The allergy step can show 7 categories and a note for each of them, the consent text and two statements, about 20 controls.
- **Why it matters:** NFR-6 promises one obvious next step, and UJ-1 names "too many things asking for his attention" as the biggest risk. Each extra element is one more thing to tap by mistake (SM-3, CM-2).
- **PRD fix:** NFR-6: on form steps, help elements (contact details, "Ask us", privacy) are gathered in one "Need help?" line, in the same place on every page, which also meets WCAG 3.2.6 Consistent help. FR-25: the allergy step starts with one question, "Does anyone have allergies or special dietary needs?", with nothing chosen, and shows categories only for the person or people named.
- **UX phase:** set a budget per screen, for example one main button and at most three other elements besides the question.

#### F13. [Medium] Changing one thing means walking every step again

- **Location:** FR-37, FR-21, FR-39.
- **Sigmund experiences:** to add Friday for bestemor, he goes through 7 to 9 screens again, and on the way he may untick or change something else by mistake.
- **Why it matters:** more chances for changes he did not intend. Every change marks the household "Changed" for the couple (FR-39), so his mistakes become their work (CM-1).
- **PRD fix:** FR-37: "See or change answer" opens the answers as a check page with a "Change" link per part. After a change he returns there and sends. A change that affects other parts (days affect meals and the cabin) takes him through those parts only.
- **UX phase:** before sending, show what changed and the new total next to the old one ("Was 2 400 kr, now 3 300 kr").

#### F14. [Medium] One tap deletes bestemor's allergy, and he cannot add it back after the deadline

- **Location:** FR-30, FR-42, FR-39, FR-40 [2027].
- **Sigmund experiences:** after the deadline, the page still offers consent withdrawal next to payment and questions. A wrong tap deletes bestemor's allergy information. Adding allergies is locked after the deadline, so he must call. In v1 the couple sees only that the household "Changed", not what changed, because the history is 2027.
- **Why it matters:** food safety (SM-8), and WCAG 3.3.4, which asks that actions with legal or data consequences can be reversed, checked or confirmed. It also leads to a call (CM-2).
- **PRD fix:** FR-30: withdrawal asks for a confirmation that names the person and the consequence ("The kitchen will then not know about bestemor's allergy"), and the status page shows "Consent withdrawn on [date]". FR-39: the "Changed" item says what kind of change it was, at least "allergy consent withdrawn", even before the full history in FR-40.
- **UX phase:** make withdrawal a quiet link in the allergy section, not a button among the main actions.

#### F15. [Medium] "Ask us" gives no idea how or when the answer comes

- **Location:** FR-43, FR-44, FR-6, FR-49.
- **Sigmund experiences:** he types his question with one finger and sends it. Then nothing: no word that it arrived, or how the couple will answer, and the question is gone from his page. He waits on the site, or calls anyway.
- **Why it matters:** the question channel should save calls (SM-10), but silence causes them (CM-2). The couple answers outside the site (FR-44), and the guest's phone number is optional (FR-49), so they may not know how to reach him.
- **PRD fix:** FR-43: after sending, the guest sees a confirmation that says how the couple will answer (by phone or message) and roughly when. The question stays on his page with its date until the couple marks it answered. FR-6: the couple's phone numbers on guest pages can be tapped to call.
- **UX phase:** offer "Call Rikke" before "Ask us", for those who would rather talk.

#### F16. [Medium] The link looks like a scam SMS

- **Location:** FR-4, §3.2 (domain), FR-52 [2027], NFR-1.
- **Sigmund experiences:** a long random code, a preview with nothing he recognises, maybe an unfamiliar address. He has been warned against links in SMS, so he waits for his daughter or does not tap at all.
- **Why it matters:** a link that is never opened is a household that never answers (SM-7, CM-2). FR-4 only says what the preview must not contain, and "contain no names" as written also rules out the couple's own names.
- **PRD fix:** FR-4: no **guest** names in titles and previews, but a recognisable preview that is the same for everyone, for example "Wedding invitation – Rikke & Valdemar" with the invitation motif, if the couple accepts that Meta caches it. §3.2: choose a domain that reads as the couple's. FR-52 (2027): the message says what happens when he taps, and that he can call.
- **UX phase:** check the preview in SMS on iPhone and Android as part of the NFR-1 link test.

#### F17. [Medium] No mobility or comfort information for older guests

- **Location:** FR-9, FR-10, FR-19.
- **Sigmund experiences:** before choosing the cabin and the hike he wants to know whether he can drive to the cabin, how far he must walk, whether there are steps, whether the cabin has its own bathroom and bedding, and how steep the hike is. Nothing in the PRD requires this.
- **Why it matters:** these facts decide his answers about the cabin and the hike. Without them he calls (CM-2, SM-10), or answers and changes later (CM-1).
- **PRD fix:** FR-10: add accessibility and comfort (distances, terrain, steps, parking near the cabins, bathroom, bedding, who to talk to if walking is hard). FR-19: the cabin "Read more" includes the same. FR-9: the hike shows length and difficulty. The content depends on Hardingasete (Q1).
- **UX phase:** a short "Good to know" block on the practical page and in the cabin "Read more", not a separate page.

#### F18. [Medium] The usability test measures speed, not correct answers

- **Location:** SM-3, NFR-6; the brief's plan to test on Rikke's phone or PC.
- **Sigmund experiences:** in the test he finishes in 8 minutes without help, but bestemor is booked for Friday and her allergy was not saved. SM-3 counts that as a success.
- **Why it matters:** SM-3 is the only check before real guests for the risks in F1 to F5, F7 and F12. CM-1 only measures wrong answers in production, when it is too late.
- **PRD fix:** SM-3: "completes a household RSVP **correctly** without help in under 10 minutes". Use a written scenario: one person coming only some days, an allergy for the other with consent on their behalf, a cabin for both, and pay now. The stored answer must match the scenario in every field, and afterwards he can say what he owes, by when, and how to find his answer again (UJ-1 "Done when"). Run it at least once on his own phone with the link sent by SMS, and note each hesitation and question as a stand-in for CM-2.
- **UX phase:** write the task script and the observation sheet.

### Low

#### F19. [Low] Arrival is asked twice, and the choices are not filtered

- **Location:** FR-18.
- **Sigmund experiences:** they arrive together, but he answers once for each of them. Bestemor's list may offer Friday times although she comes on Saturday.
- **Why it matters:** repeated entry, against the spirit of WCAG 3.3.7, and a little extra load (SM-3).
- **PRD fix:** one line in FR-18: arrival choices start from the person's first day.
- **UX phase:** a "Same for everyone" option.

#### F20. [Low] The envelope animation may stall him

- **Location:** §3.3 (If time), NFR-5.
- **Sigmund experiences:** he waits, taps the seal at the wrong moment, or wonders what "Skip" would skip.
- **Why it matters:** there is no evidence on how older guests react to it [R 2.2], and it is his first impression.
- **UX phase:** it plays by itself in a few seconds and needs no tap; the skip label says what happens ("Show the invitation now"); try it with the SM-3 participant before adding it.

#### F21. [Low] The QR code is shown on the phone that would scan it

- **Location:** FR-34; §3.3 (Vipps QR).
- **Sigmund experiences:** he cannot scan a code on his own screen. He must carry three values into Vipps or his bank app, and he wonders whether the number really is Rikke's.
- **Why it matters:** wrong amounts or messages (CM-3), and hesitation.
- **UX phase:** show the QR code only on larger screens, or say it is for paying from another phone; copy buttons for number, amount and message; the account number in groups (1234 56 78901); the recipient's name as Vipps will show it.

#### F22. [Low] The exact moment of the lock is not defined

- **Location:** FR-41, FR-42.
- **Sigmund experiences:** he tries on the evening of the deadline day and finds it locked, and he blames himself.
- **Why it matters:** a call (CM-2) and lost trust.
- **PRD fix:** the deadline ends at the end of the stated day, Norwegian time, and the text says "by and including [date]". Joy locks at midnight in the event's time zone [R 1.3].

#### F23. [Low] His total changes by itself after a price change

- **Location:** FR-33, FR-65.
- **Sigmund experiences:** the receipt said 2 400 kr. A month later his page says 2 550 kr, "150 kr remaining", and he thinks he did something wrong.
- **Why it matters:** self-blame, calls (CM-2) and payment mismatches (CM-3). It is rare if prices are final before invitations go out.
- **PRD fix:** when a price change alters a household's total, the guest's status says why ("The prices were updated on [date]"), and the FR-65 warning suggests that the couple tells the households affected.

#### F24. [Low] Two links on one shared phone

- **Location:** FR-1, FR-12, FR-52 [2027].
- **Sigmund experiences:** bestemor has no smartphone, so both links arrive on his phone. He taps hers and answers as bestemor.
- **Why it matters:** the wrong respondent and consent record (see F11).
- **UX phase (and the couple's routine):** when two people share a phone, send one message with that phone owner's link; the FR-52 message says whose link it is.

#### F25. [Low] Two people answering at once overwrite each other silently

- **Location:** FR-38; decision C5.
- **Sigmund experiences:** he and bestemor answer on two phones the same evening. The last save wins without a word, and one of them believes their answer stands.
- **Why it matters:** corrections after a call (CM-1). Rare for this couple; C5 chose this on purpose.
- **PRD fix (optional):** if someone else saved after the form was opened, say so before saving ("Bestemor saved an answer at 19:42. Look at it first?"). The research describes this version check as a standard, cheap pattern [R 4.5].

#### F26. [Low] The dead-link message must not make him feel at fault

- **Location:** FR-5.
- **Sigmund experiences:** if his link is ever replaced, the old SMS opens "This is a private invitation", and he thinks he has broken something.
- **Why it matters:** this persona blames himself, and by design this page has no phone numbers.
- **UX phase:** wording that fits both unknown and replaced links and says it is not his fault, for example "This link no longer works. That is not your fault. Contact Rikke or Valdemar the way you usually do, and they will send you a new one."

#### F27. [Low] Words he does not use

- **Location:** NFR-6.
- **Sigmund experiences:** "RSVP" (he knows "O.S.A."), "husstand" (sounds like a tax form), "samtykke", "Vipps-nummer", and "melding" (he may think he must text Rikke).
- **Why it matters:** plain words are the cheapest accessibility there is (NFR-6).
- **UX phase:** "Svar på invitasjonen", "Svar innen [dato]", the names or "dere to" instead of "husstanden", and "Melding til mottaker", as his bank calls it. The PRD's English terms are working labels only.

### Small UX-phase notes (no PRD change)

- Disable the send button after the first tap, so a double tap does not land on "Pay now" on the next screen.
- After a "Change" from the check page, return to the check page, and say if the change removed something (unticking Friday removes Friday dinner).
- The error summary (FR-22) takes focus, so it is seen on a small screen.
- The progress sign does not jump when steps appear or disappear.
- Use day names with times ("fredag kl. 16") and no abbreviations.
- On the receipt, suggest keeping the SMS: "Keep the message with the link. It always takes you back here."

### Suggested PRD edits, in priority order

1. **FR-14, FR-15, FR-16, FR-32:** ask who is coming separately from how long; define days by arrival and departure, with consistency rules; state the price unit (F1, F2, F9).
2. **FR-21, FR-7, FR-24:** "not sent yet" and a "Send answer" button on the check page; the answer status in words on the front page (F3).
3. **NFR-1, FR-13, FR-43, NFR-4:** a draft kept on the device, a back button that goes one step back, help that opens in place, no time limit on guest forms (F4).
4. **FR-26 to FR-29:** one plain statement per person; an open consent is an error at the field; "not saved" shown where he will see it (F5).
5. **FR-35, FR-2, FR-24:** confirm "I have paid", show the state after it, allow undo, and use guest words for payment status (F6).
6. **NFR-5:** a minimum text size and support for the phone's large-text settings (F7).
7. **SM-3:** measure correct answers against a written scenario, on his own phone (F18).
8. **FR-23, FR-34, FR-64:** receipt order, no payment step when the total is 0, and a pay-by date (F8).

## What already works well

- **The right north star.** UJ-1 names the biggest risk, too much at once, and NFR-6 turns "one obvious next step" into a requirement. This review is measured against the PRD's own standard.
- **No name search and no password** (FR-1, FR-12, NFR-5). The most common RSVP error in the research is gone, and "I am Sigmund" is already set (WCAG 3.3.7 and 3.3.8).
- **Looking is safe.** Opening the link changes nothing (FR-3), so he can look around without breaking anything.
- **The invitation is personal and clear.** His and bestemor's names, the deadline and the button are visible without scrolling (FR-7, FR-41). He knows it is for him and what to do by when.
- **Information does not drown the button.** Short cards, "Read more" pages with a way back, and the button repeated at the bottom (FR-8, FR-11).
- **The form follows proven patterns.** One step at a time with Back and progress (FR-13), "Read more" in place (FR-19), a warning before leaving through the site's own links (FR-20), a check page with "Change" links and "Not provided" (FR-21), and errors at the field with a summary (FR-22).
- **No guessing for him.** Nothing is ticked in advance (addendum), later steps only ask about the people and days that apply (FR-15), and Saturday breakfast is offered only to those there from Friday.
- **Money is shown honestly.** Prices before choices, a friendly reason why guests pay, the cabin rule before the choice, and a total that is calculated and never typed in (FR-16, FR-32, FR-33). A change after payment tells him what remains or that the couple will pay back the difference (FR-36).
- **Forgiving input.** Fixed choices with "Don't know" and no time pickers (FR-18), and fixed allergy categories (FR-25), as the research on older users recommends [R 2.2].
- **Consent is never forced.** The answer can always be sent without it, and nothing is ticked (FR-28, CM-4).
- **A warm ending and a lasting receipt.** Rikke's own words on the receipt (FR-23, addendum), and a link that always opens his status (FR-24), so the SMS itself becomes his receipt.
- **The household cannot answer twice by accident.** Bestemor sees Sigmund's answer and its time instead of an empty form (UJ-2 step 5, FR-38).
- **The deadline is humane.** Afterwards he can still see his answer, pay, report payment, read and ask (FR-42).
- **A person is always one tap away.** The couple's phone numbers are on every page, including error pages (FR-6), which matches the research's "a person to call" and WCAG 3.2.6.
- **Calling is a designed path, not a failure of the design.** The couple can fill in his answer (FR-63) and record consent given by phone (FR-31).
- **Accessibility basics are in.** Touch targets of at least 44 × 44 px, 4.5:1 contrast with sage green flagged for checking, and respect for "reduce motion" (NFR-5).
- **The right things are measured.** CM-1 and CM-2 count the real cost of a confusing form, and SM-3 tests with an older relative before delivery.
