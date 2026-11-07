---
title: "Pre-mortem review: PRD for AI'll handle it"
reviewer: "Pre-mortem (adversarial)"
reviewed: "prd.md, addendum.md and .memlog.md as of 2026-11-07"
created: 2026-11-07
---

# Pre-mortem review: PRD for AI'll handle it

**The exercise.** It is January 2028. The invitations went out in December 2027 by SMS, Messenger and email to about 70 guests. Something went badly wrong, and Rikke and Valdemar fell back to manual invitations, phone calls or Excel. The stories below explain how, and test each one against `prd.md`, `addendum.md` and the decisions in `.memlog.md`.

The owner's biggest fear: *"We must never have to send a new invitation by hand because the site failed."* Secondary fears: wrong numbers to Hardingasete (meals, beds, allergies), money confusion, and older guests failing to answer.

**Verdict: not safe to run for real as written.** The guest flow, link privacy and counting rules are specified with care, and the course version is well protected. But the PRD specifies the product, not its operation. NFR-1 names the right outcomes (links never break, nothing is lost) and almost none of the mechanisms that would prevent or detect failure once a beginner runs the site for real: no alerting, no backups that survive the server, no wall between the demo and production, no record of who was sent a link, no pilot. In 7 of the 12 stories a guest discovered the failure before the couple did; in 3 more nobody noticed for weeks. The site itself never raised an alarm that led to the fix. Three stories end with invitations re-sent by hand (one of them all 70), and one with a reportable breach of health data.

**Findings:** 3 critical, 12 high, 10 medium, 1 low (26 in total). Ten challenge a recorded decision. Many are cheap if decided before the architecture; the "When" line on each finding says how soon.

## Failure stories

Each story is a separate way the project could fail, not one timeline. In all of them, the couple sent the links on the evening of Sunday 19 December 2027.

### S1. The weekend the padlock broke

**What happened.** On Sunday 2 January 2028 the site's HTTPS certificate expired. Its automatic renewal had stopped when Rikke moved the site to a bigger server plan in November, and nothing checked it. Every guest link opened a full-page security warning; inside Messenger's built-in browser it did not open at all.
**Why.** NFR-1 promises the site is available "from the invitations until the wedding", but no requirement makes anything watch the site, the certificate, the domain or the hosting subscription, or tells anyone when they fail.
**Who noticed.** Tante Gunn, on Tuesday, who phoned to ask whether the wedding site had been hacked.
**Damage.** Two and a half days without a site, in the week many households had set aside to answer. Two guests deleted the message as a scam and needed new messages by hand; four households answered by phone and Rikke typed it in (CM-2). Others learned to click through a security warning. While fixing it, Rikke found that the domain had been registered for one year and expires in March 2028, before the RSVP deadline, with renewal reminders going to an inbox nobody reads. UJ-3 step 6 promised that guests still see the couple's phone numbers when "a page won't load"; with the server unreachable, nothing showed anything.
**PRD check.** Neither prevented nor revealed. → PM-3, PM-17.

### S2. The rebuild that took the backups with it

**What happened.** On Tuesday 11 January a system update on the server failed halfway and the site started returning errors. Rikke pasted the server log into an AI assistant (the log held guest names and complete personal links) and followed its suggestion to rebuild the server from the hosting panel. The rebuild wiped the disk. The nightly backups met NFR-1 to the letter, and a restore had been tested in October. They were in a folder on the same disk.
**Why.** NFR-1 and §3.2 ask for daily backups and one restore test. They do not ask for a copy outside the server and the hosting account, for an alarm when backups stop, or for any safe way for a beginner to operate the server.
**Who noticed.** Rikke, at once. There was nothing to restore.
**Damage.** The worst case. Every answer, consent record, payment registration and link code was gone, and all 70 links showed "private invitation". The couple rebuilt the guest list from old messages and a spreadsheet, created 70 new links, sent every invitation again by hand with an apology, and asked the 24 households that had already answered to do it again. Payment status was rebuilt from Vipps and bank history in Excel. And pasting the log into an AI tool broke the PRD's own rule that real data never goes into AI tools (NFR-3).
**PRD check.** Fully compliant with NFR-1, and still a total loss. → PM-1, PM-3, PM-24.

### S3. The demo came along to production

**What happened.** At go-live in October 2027, Rikke set up the server by following the README she wrote for the examiner: install, migrate, seed. She then deleted the fictional households in the admin area and entered the real ones. The test admin and test helper stayed; their usernames and passwords are printed in the public README (UJ-6 step 3, FR-68). So did Valdemar's fictional phone number on every guest page, and the seed's bank account number. On Tuesday 28 December she corrected the parking text, which lives in code (D12), and redeployed by repeating the README steps. The seed step reset the database.
**Why.** The PRD keeps real data out of the repository but never keeps the repository's demo out of production. The seed command can run anywhere, test accounts can exist next to real health data, seed settings look like real ones, and a text change is a code deploy with no defined safe procedure.
**Who noticed.** Arild, who texted that his link now said "private invitation".
**Damage.** Last night's backup brought most answers back; six households that answered that day had to answer again. The incident review found logins to the test admin from an address in Molde in November: a classmate checking whether the course app was live. Real guests' allergy data had been open to anyone who read the README, a personal data breach to be reported to Datatilsynet within 72 hours and explained to every guest. Two guests had paid 450 kr each to the seed account number, which passed the bank's check digit and belonged to a stranger.
**PRD check.** Not prevented. NFR-3 and NFR-4 protect the repository, not production. → PM-2, PM-14.

### S4. The links that never arrived

**What happened.** The couple sent all 70 links in one evening from two phones. Rikke put each link in a friendly sentence, "(her er invitasjonen din: https://…)". On three guests' phones the closing bracket became part of the link, and they landed on "this is a private invitation, contact the couple", which an 80-year-old reads as "this isn't for you". Valdemar's aunt and uncle never saw their Messenger messages: they are not Facebook friends with Rikke, so the messages sat in message requests. Two older guests ignored a link by SMS from a number they had not saved, as they have been taught to do with scams. Two great-aunts without smartphones got their links by email, to an address their son checks once a month. And on her phone, "copy link" failed silently once, so Rikke pasted the previous guest's link: Synne received Sigmund's invitation.
**Why.** The only delivery requirement is a test link opened on the couple's own phones (NFR-1). The site records nothing about who was sent what, link tracking is If time, and a delivery failure looks exactly like a slow guest.
**Who noticed.** Only Synne, who wrote back. The rest came out six weeks later, when Rikke worked through the not-answered list by phone.
**Damage.** Eleven invitations re-sent by hand; Sigmund's link deactivated and replaced (FR-53 worked as designed). Six weeks of answering time lost for those households. SM-6 cannot even be measured, because nothing records a resend or its reason.
**PRD check.** Partly. FR-53 repairs a wrong link once someone reports it. Nothing reveals silent non-delivery, and the NFR-1 channel test would have passed. → PM-4, PM-5, PM-25.

### S5. Three older guests who thought they had answered

**What happened.** Tante Gunn (81) opened her link on an iPad that stopped getting updates years ago; the page stayed white. Onkel Per started in Messenger's built-in browser, switched to his messages to ask his son about Friday, and came back to an empty form. No "not sent yet" warning ever appeared. Kåre (84) went through every step, read his answers on the check page, took it for the receipt and put the phone away. In the same weeks, the envelope animation, finished in November because §3.2 pulls every unfinished If-time item into 2027, failed to start on an older iPhone and left a closed envelope with no way in.
**Why.** No device floor is defined, and the channel test uses modern phones. FR-20 relies on a warning that phone browsers do not reliably show, and never show when the guest switches apps or the phone closes the page in the background. FR-21 dropped the research's statement that nothing is sent until the guest confirms [R 1.7]. Saving unfinished answers is If time. SM-3 would not catch any of it: it measures time, not whether the answer arrived.
**Who noticed.** Nobody until mid-January; all of them sat in "not answered". Kåre was offended to be reminded about an answer he believed he had sent.
**Damage.** Four households answered by phone (CM-2), typed in by Rikke. The guests the PRD was designed around failed first, and their families now call the site "complicated".
**PRD check.** Not prevented. NFR-5 and NFR-6 make the flow good on a good phone; nothing makes it survive an old device, an app switch or a misread check page. → PM-6, PM-7, PM-15, PM-22.

### S6. Christmas Eve at Arild's

**What happened.** Arild and Marie got their links at the same moment on 19 December and left them for later. On Christmas Eve, at the table, both opened the form on their own phones. Arild answered carefully: Leone not coming, Filippa Saturday and Sunday only, Filippa's coeliac disease registered with consent. Marie had opened her form earlier, been interrupted, and pressed Send ten minutes after Arild, with Filippa there the whole weekend and no allergies. Last save wins.
**Why.** C5 chose last save wins, with "last updated by X at Y" shown before editing (FR-38). That only helps when one person saves before the other opens the form. Giving each household member their own link and sending all links at once makes this overlap likely, not rare.
**Who noticed.** Valdemar saw "Changed" on his phone, glanced at it and marked it as seen, which removed it for Rikke too. On 10 January Arild asked why the site said they owed about 600 kr more when he had already paid.
**Damage.** The overwrite was found only because the money changed. Had the totals been equal, Filippa's gluten allergy would have been missing from the list for Hardingasete (SM-8). A refund, an awkward call, and a family that now distrusts the form.
**PRD check.** Not prevented. "Changed" says that something changed, not that one answer erased another, and either partner can clear it for both. → PM-8, PM-13, PM-21.

### S7. Bestemor was a "no"

**What happened.** Bestefar Sigmund answered on his own link. Bestemor has her own link, so he assumed she would answer for herself. The first question asked whether everyone in the household was coming the whole weekend. He chose "No", and the next screen asked who was not coming. To answer only for himself, he ticked bestemor.
**Why.** FR-14 forces the respondent to decide for every household member; there is no "she'll answer herself" and no "don't know yet". One link per person makes "my link, my answer" the natural belief, and the household form contradicts it. SM-3's usability test would not catch it: it measures time to finish, not whether the answer is right.
**Who noticed.** Nobody. A "no" takes bestemor off the not-answered list and out of "Needs attention". She never opened her link, because Sigmund said "it's done". It came out at a family birthday on Saturday 15 January, when she talked about the dress she had bought.
**Damage.** Wrong numbers per day, meal and bed, with no signal anywhere. The same trap exists for adult children with their own links. The couple now phones every household where someone answered "not coming" for another person: the chasing the site was meant to end.
**PRD check.** Not prevented. It is designed in. → PM-9, PM-22.

### S8. The deadline that came on 3 January

**What happened.** In early January, Hardingasete moved its date for final numbers, so Rikke changed the RSVP deadline on her phone from 15 March to 01.03.2028, meaning Wednesday 1 March. The settings field read the date month-first. At 01:00 on Monday 3 January (midnight UTC), the form locked for every guest. Twenty households that had not answered were told the deadline had passed and to contact Rikke and Valdemar (FR-42). The instruction worked perfectly, for everyone at once.
**Why.** The PRD never defines the deadline: a date or a moment, inclusive or not, which time zone, how summer time is handled, how it is shown back to the couple. FR-65 warns before a price change; nothing warns before a deadline change that locks households out.
**Who noticed.** Guests, within the hour, by phone and Messenger.
**Damage.** Three days of phone answers before the couple understood; nine households' answers typed in from calls; receipts already in guests' hands said 15 March while the site said the deadline had passed. Even with the date fixed, the deadline would have closed at the start of its own day rather than the end, so guests answering on the evening of the deadline would have been locked out.
**PRD check.** Not prevented: FR-64 accepts any value without confirmation. → PM-10.

### S9. Hardingasete's 2028 price list

**What happened.** Invitations went out with Hardingasete's 2027 prices. On Wednesday 5 January Hardingasete sent its 2028 prices: Friday dinner 45 kr more, breakfasts 20 kr more, and cabins priced per cabin (four to six beds) instead of per person. Rikke entered the new prices. FR-65 warned that 23 households' totals would change; FR-33 left her no other option, because every total is calculated from the current prices.
**Why.** The PRD treats a price change as a warning to the couple, not as something guests live through. And the per-person cabin price was never confirmed: Q1 was answered for capacity only and Q3 is open, but the form, the totals and the payment flow all assume it.
**Who noticed.** Guests. The 14 households that had already paid in full now saw "part paid, 40–130 kr missing" with no explanation. Sigmund phoned, upset: "We paid what you asked."
**Damage.** Money confusion across half the guest list, a round of apologetic messages, and a decision to absorb the difference that the site could not express. Rikke registered made-up payments to clear the statuses, corrupting the payment record. The per-cabin price depends on who shares a cabin, which is decided outside the site, so Rikke built an Excel sheet to split cabin costs (SM-9 failed).
**PRD check.** Partly. FR-65 warns the couple; nothing protects the guests or gives the couple a policy. → PM-11, PM-18, PM-19.

### S10. "Bryllup Kari"

**What happened.** By mid-January, Vipps and the bank showed 27 payments from 21 households. The messages said "Bryllup", "bryllup kari", "fra mamma og pappa" and "Bryllup Kari" (there are two Karis), and several transfers came from joint accounts in names no guest has. One couple both paid. Filippa paid her own share apart from Arild. Rikke registered 900 kr on the wrong Kari's household: the right Kari's "I have paid" turned red and she got a reminder, while the other Kari's household showed "paid" without having paid. Then Rikke moved Filippa to her boyfriend's household (FR-50): Arild's household flipped to "refund owed 1,450 kr" and Filippa's new household to "not paid".
**Why.** D8 removed any household reference, and FR-34's own example, "Bryllup Sigmund", is not unique. "I have paid" stores only a time, with no amount, method or payer, and "matching" in FR-61 is undefined. FR-50 does not say what happens to answers or money when a person moves.
**Who noticed.** The right Kari, offended by the reminder.
**Damage.** Wrong reminders, a refund almost paid to the wrong household, and an Excel reconciliation of Vipps and bank exports against households: the very record the site was supposed to replace. CM-3 spiked, although the payment instructions were clear.
**PRD check.** Partly. FR-61 flags a mismatch but cannot tell whose mismatch it is. → PM-12, PM-23.

### S11. The preliminary numbers

**What happened.** On Thursday 20 January Hardingasete asked for preliminary bed numbers and known allergies, to hold the cabins. The summary showed 41 staying overnight and four people with dietary needs. The other 48 attending guests showed nothing, and nobody could tell the 44 with no needs from the four who skipped the step or declined the consent text. One of them was tante Gunn, who has coeliac disease and thought "consent" sounded like signing something. Rikke typed the counts and four names into an email on her phone. Over the next two weeks, three households changed their days and one withdrew allergy consent (FR-30), all shown as a plain "Changed".
**Why.** The allergy summary shows registered needs only, so silence looks like "none". The PRD has no record of what was sent to Hardingasete or what changed since, no way to copy lists out of the site, and puts cabin allocation in a spreadsheet by design.
**Who noticed.** Nobody, yet. In this story, the kitchen finds out at Friday dinner on 26 May.
**Damage.** The preliminary list is wrong in both directions, and nothing in the site says what changed after it was sent. Rikke retyped names into the email and into the cabin spreadsheet, misspelling one. SM-8 is already at risk in January.
**PRD check.** Partly. FR-55 lets Rikke see who is behind each count, but nothing tells her to look for the people with nothing registered, or for changes since sending. → PM-13, PM-19, PM-20.

### S12. The best man leaves

**What happened.** After a falling-out in early January, the best man was replaced. His helper login could still read every guest's phone number, allergies and questions. FR-47 creates admin accounts by a command on the server; nothing removes or deactivates one, and only Rikke can reach the server. On Friday 14 January Valdemar forgot his password just before a meeting at Hardingasete where the venue asked for numbers. There is no reset, and Rikke was at work without her laptop. Meanwhile a guest's question through "Ask us" ("Will my ex be there? I'd rather not sit near him") had been read by all three helpers.
**Why.** Admin accounts have a beginning but no end, the couple's work depends on one laptop's server access, and "Ask us" does not say who reads the questions.
**Who noticed.** Rikke, when she tried to remove the best man and found no way except editing the production database by hand.
**Damage.** Health data open for nine days to someone the couple no longer trusts; Valdemar unable to answer the venue; an embarrassed guest. Rikke finally deleted the account by running a database command an AI assistant wrote, against production, without a backup first.
**PRD check.** Not prevented. FR-46 and NFR-4 stop helpers from changing data, but nothing manages an account's lifetime. → PM-16, PM-26, PM-3.

## Findings

**Severity.** *Critical:* can trigger the owner's worst case (mass re-invitation), total data loss or a health-data breach, and nothing in the PRD stops it. *High:* likely wrong numbers, money confusion across many households, or guests failing to answer, and nothing reveals it quickly. *Medium:* plausible, with a smaller blast radius or partial cover. *Low:* minor.

**When.** *v1:* decide or build for the course version, usually because the data model or architecture depends on it. *Architecture:* settle in bmad-architecture. *Before invitations:* 2027. *PRD now:* a scope or wording change in this document.

| ID | Severity | Finding | Location | When |
|---|---|---|---|---|
| PM-1 | critical | Backups can die with the server | NFR-1, §3.2 | Before invitations |
| PM-2 | critical | Nothing keeps the demo out of production | Missing (FR-47, FR-68, UJ-6, NFR-3, NFR-4) | v1 |
| PM-3 | critical | No one is told when the site breaks, and no one owns keeping it alive | NFR-1, §3.2 | Before invitations |
| PM-4 | high | Delivery failures are invisible | §3.3 Link tracking, FR-52, SM-6 | v1 data model; before invitations |
| PM-5 | high | The go-live test proves too little | NFR-1, §3.2 | Before invitations |
| PM-6 | high | No device floor | NFR-1, NFR-6, NFR-7 | Architecture |
| PM-7 | high | An unsent answer can vanish without anyone knowing | FR-20, FR-21, §3.3 | v1; before invitations |
| PM-8 | high | Last save wins will overwrite households, allergies included | FR-38, §3.4 Conflicts | Architecture |
| PM-9 | high | The form cannot say "she'll answer herself" | FR-14, FR-12, FR-24 | v1 |
| PM-10 | high | The deadline has no defined moment | FR-41, FR-42, FR-64 | v1 |
| PM-11 | high | A price change silently rewrites what guests owe | FR-33, FR-65, NFR-2 | v1 |
| PM-12 | high | Payments cannot be matched reliably | FR-34, FR-35, FR-61, §3.4 | v1 |
| PM-13 | high | Silence looks like "no allergies" | FR-25, FR-54, FR-58 | v1 |
| PM-14 | high | Every text change is a production deploy, with no safety net | D12 note after FR-65, NFR-9 | Architecture; before invitations |
| PM-15 | high | 2027 is an open-ended build window right before go-live | §3.2, §3.3 | PRD now |
| PM-16 | medium | Admin accounts can be created but never removed or recovered | FR-46, FR-47, NFR-4 | v1 |
| PM-17 | medium | UJ-3's fallback promise fails exactly when the site is down | UJ-3 step 6, FR-6, FR-52 | Before invitations |
| PM-18 | medium | The per-person price model is assumed, not confirmed | FR-16, FR-32, §7 | Architecture |
| PM-19 | medium | SM-9 contradicts the scope, and numbers are retyped by hand | SM-9, §3.3, §3.4, FR-58 | PRD now |
| PM-20 | medium | No record of what was sent to Hardingasete | FR-54, UJ-4 | Before invitations |
| PM-21 | medium | "Handled" and "seen" are anonymous and shared | FR-56, FR-46 | v1 |
| PM-22 | medium | SM-3 measures speed, not correctness | SM-3 | v1 (December 2026) |
| PM-23 | medium | Moving a guest has undefined effects on answers and money | FR-50, FR-59, FR-60 | v1 |
| PM-24 | medium | Production logs leak links and personal data, and the operator relies on AI help | NFR-3, NFR-4 | Architecture |
| PM-25 | medium | Guests who will not use a link have no planned path | §7 Assumptions, §3.3 English | Before invitations |
| PM-26 | low | "Ask us" does not say the helpers read the questions | FR-43, FR-46 | v1 |

### PM-1. Backups can die with the server (critical)

- **Location:** NFR-1, fourth bullet; §3.2 Backups.
- **Stories:** S2, S3.
- **Gap:** NFR-1 is met by nightly copies on the same disk, or by provider snapshots that vanish with the account, plus one restore test months before the failure. Nothing requires a copy that the server cannot take down with it, an alarm when backups stop, repeated drills, or a backup before risky operations. The database holds every link code, so losing it without a usable backup is the owner's worst case: all 70 invitations re-sent by hand, and every household asked to answer again.
- **Fix:**
  - Backups are stored outside the server and outside the hosting account, so deleting, rebuilding or losing either cannot remove them. The couple also holds a recent copy themselves.
  - Backups are encrypted, because they contain health data, and are deleted with everything else by 31 August 2028 (NFR-3).
  - If no successful backup exists for the last 24 hours, Rikke and Valdemar are both alerted (PM-3).
  - A restore to a separate machine is rehearsed before invitations, after any server change, and right after the RSVP deadline. The drill passes only if a known guest link opens the right household with its answers and payments.
  - A backup is taken immediately before every deploy or server change (PM-14).
- **When:** Before invitations. The architecture should make the database easy to copy and restore.

### PM-2. Nothing keeps the demo out of production (critical)

- **Location:** Missing. Touches FR-47, FR-68, UJ-6 step 3, NFR-3, NFR-4, NFR-8 and the addendum's "Test data note".
- **Stories:** S3.
- **Gap:** The README must publish logins for a test admin and a test helper, and fixed test links (UJ-6). The PRD keeps real data out of the repository but never keeps the repository's demo out of production. The seed command can run against the live database; test accounts can sit next to real guests' health data; seed settings (phone numbers, account number, Vipps number, deadline, prices) look like real values. The test-data note makes phone numbers and emails obviously fake, but says nothing about payment details.
- **Fix:**
  - Production starts empty. The seed command refuses to run when the site is set up as production, or when the database holds any household the seed did not create.
  - The site refuses to run as production, or blocks the admin area with a warning, while any test account, test link or fictional household exists.
  - Seed payment details are invalid by construction (for example, an account number that fails the bank's check digit), and guest pages show no payment details until the couple has entered and confirmed real ones.
  - Guest pages stay closed until the couple has confirmed every setting (prices, deadline, contact details, payment details) in a go-live check.
  - Real guests' links always come from the random generator. The fixed codes printed in the README exist only in seed data.
- **When:** v1, because the seed command and settings are built now. The go-live check comes before invitations.

### PM-3. No one is told when the site breaks, and no one owns keeping it alive (critical)

- **Location:** NFR-1, first and fifth bullets; §3.2 Hosting; otherwise missing.
- **Stories:** S1, S2, S12; underlies most of the others.
- **Gap:** NFR-1 says the site is available "from the invitations until the wedding" and that links work "until the data is deleted". Nothing makes it so. There is no check that the site is up; no warning before the certificate, the domain or the hosting subscription expires; no alert when backups or email forwarding stop; no named owners; and no way for Valdemar to act if Rikke's laptop is gone. With a beginner as operator, guests find the failures.
- **Fix:**
  - An outside check of the guest site and its database runs every few minutes and alerts Rikke and Valdemar on their phones within 15 minutes of an outage or a burst of errors.
  - Alerts at least three weeks before the certificate, the domain or the hosting subscription expires, and when a payment for any of them fails.
  - Before invitations, the domain is registered and the hosting paid until at least 1 September 2028. Renewal notices go to an inbox both of the couple read.
  - Both Rikke and Valdemar can log in to the domain registrar, the hosting account, the backup storage and the server. The access details survive a lost laptop.
  - The admin home shows a health line: time of the last successful backup, whether email forwarding works, and errors in the last 24 hours.
  - A one-page runbook covers what to do when the site is down, how to restore, how to renew, and whom to ask.
- **When:** Before invitations.

### PM-4. Delivery failures are invisible (high)

- **Location:** §3.3 Link tracking (If time); FR-52 [2027]; SM-6; NFR-4 (slowing wrong links); a "sent" record is missing.
- **Stories:** S4.
- **Gap:** The couple sends 70 links by hand, over three channels, from two phones. The site records nothing about it: not who was sent a link, by whom or how, and not whether the guest ever got in. Link tracking, the only early signal, is If time. A mangled link, a message stuck in Messenger requests or ignored as a scam, and a wrong pasted link all look exactly like a slow guest until someone works through the not-answered list weeks later. SM-6 cannot even be measured, because nothing records a resend or why it happened.
- **Challenges a recorded decision:** the brief put link tracking in If time, and the PRD kept it there, although the memlog's own scope principle says "[2027] = what only matters with real guests". Tracking is exactly that.
- **Fix:**
  - For each guest, the couple records "invitation sent" (date, channel, who sent it). Every resend is recorded with a reason (lost, wrong person, site problem), and SM-6 counts all of them, not only those blamed on the site.
  - Link tracking as defined in C4 (pressed Start or saved an answer) is required before invitations.
  - "Needs attention" lists guests not yet marked as sent, and households that have not started some days after sending.
  - The admin shows how many visits per day hit an unknown or deactivated link (a count only, no codes). A spike means links are breaking on the way.
  - A link still opens when a messaging app adds trailing punctuation, a bracket or a space. The unknown-link page says the link may be incomplete and to contact whoever sent it, still without names or details (FR-5).
  - Copying a link or message on the couple's phone confirms what was copied ("Sigmund's invitation copied"), and a failed copy says so.
  - Slowing down wrong-link attempts never blocks a valid link, even for a family sharing one home network.
- **When:** The "sent" record in the v1 data model; tracking and the rest before invitations.

### PM-5. The go-live test proves too little (high)

- **Location:** NFR-1, second bullet; §3.2.
- **Stories:** S4, S5.
- **Gap:** The only pre-launch test is sending "a test link" by SMS, Messenger and email and opening it on an Android phone and an iPhone: in practice a bare link on the couple's own modern phones. It would not catch the real message mangling the link, an in-app browser losing the form, an old device, wrong payment details, email forwarding that does not work, or guests ignoring an unknown sender. This extends the Round 3 decision in the memlog, which is necessary but not enough.
- **Fix:** a staged go-live, written as requirements:
  - The domain is live with HTTPS at least a month before invitations.
  - Guests are told in advance, through a channel they already trust, that a personal link will come from Rikke or Valdemar. Each partner sends to their own side.
  - Pilot: three to five real, friendly households, including the oldest guest and someone with an old device, get the exact FR-52 message through each channel. Each completes a full RSVP to the receipt, taps "I have paid" and asks a question. At least one Vipps payment and one bank payment are made using exactly the details on screen. The couple then checks the counts, the payment registration and the question email.
  - A written go/no-go before the rest are sent. The rest go out in batches, with a check of the admin after the first, at a time when the couple can respond within hours for the next three days.
- **When:** Before invitations.

### PM-6. No device floor (high)

- **Location:** NFR-1, second bullet; NFR-6; NFR-7; §3.3 Envelope animation.
- **Stories:** S5.
- **Gap:** The guests are "many of them older and not used to technology". Many use hand-me-down tablets and phones that no longer update, and open links inside Messenger's built-in browser. The PRD defines no minimum device or browser. A site that works on Rikke's phone can show a blank page on tante Gunn's iPad, and nobody is told.
- **Fix:**
  - Before the architecture, define a device floor from what the oldest guests actually use (ask a few of them), including the built-in browsers of Messenger and Facebook.
  - The invitation, the information pages and the full RSVP work on that floor, verified on a real old device before invitations (part of PM-5).
  - The invitation content and the RSVP button appear even if scripts or the animation fail. The envelope may never stand between a guest and the invitation.
- **When:** Architecture, because the front-end approach decides this.

### PM-7. An unsent answer can vanish without anyone knowing (high)

- **Location:** FR-20; FR-21; §3.3 Unfinished answers; NFR-1, third bullet.
- **Stories:** S5.
- **Gap:** NFR-1 protects a failed save, not an answer that never reaches Send. FR-20 relies on a "not sent yet" warning that phone browsers do not reliably show, and that never appears when the guest switches apps or the phone closes the page in the background. FR-21 dropped the research's advice that the check page says nothing is sent until the guest confirms [R 1.7], so some guests take the check page for the receipt. Saving unfinished answers is If time.
- **Challenges a recorded decision:** memlog, "leaving before sending triggers a 'your answer is not sent yet' confirm. Saving an unfinished answer to continue later is If time."
- **Fix:**
  - Replace FR-20 with an outcome: an unsent answer is kept on the guest's device when they leave, switch apps or reload, and is offered back when they return through their link. This promotes "Unfinished answers" to before invitations.
  - The check page says at the top that the answer is not sent yet, and the button says what it does ("Send answer").
  - With link tracking (PM-4), the couple sees households that started but never sent, and can call them.
- **When:** Check-page wording in v1; keeping unsent answers before invitations at the latest.

### PM-8. Last save wins will overwrite households, allergies included (high)

- **Location:** FR-38; §3.4 Conflicts (C5); FR-63; FR-12.
- **Stories:** S6.
- **Gap:** "Last updated by X at Y" only helps when one person saves before the other opens the form. With one link per person and all links sent at once, two household members filling in the form at the same time is the expected case, not an edge case. The couple can collide with a guest the same way (FR-63). The later save silently replaces the earlier one, including allergy information and consent that the second person never saw. Research [R 4.5] described the standard way to detect this; C5 chose not to.
- **Challenges a recorded decision:** C5 ("last save wins"), combined with one link per guest (memlog) and the plan to send all links at once.
- **Fix:**
  - When a respondent sends, and the household's answer was saved by someone else after they opened the form, the site does not overwrite silently. It shows the newer answer (who, when, what differs) and asks the respondent to review before sending.
  - A save never deletes allergy information or consent that was not shown in the respondent's form.
  - The "Changed" marker says when one answer replaced another person's answer.
- **When:** Architecture (affects v1).

### PM-9. The form cannot say "she'll answer herself" (high)

- **Location:** FR-14; FR-12; FR-24; UJ-2 step 5.
- **Stories:** S7.
- **Gap:** FR-14 makes the respondent decide for everyone: either all are coming the whole weekend, or the respondent marks who is not coming and which days the others come. There is no "answers for themselves" and no "don't know yet". One link per person makes "my link, my answer" the natural belief, so a guest who only wants to answer for themselves must mark the others as not coming, or guess their days. A wrong "no" is worse than no answer: it takes the person off the not-answered list and out of "Needs attention", so nothing ever flags it.
- **Challenges a recorded decision:** memlog, the household answers at once, with "Are all of you coming the whole weekend?" as the first question; and one link per guest.
- **Fix:**
  - For each other household member, the respondent can choose "answers for themselves" (or "don't know yet"). That person stays "not answered" and appears in "Needs attention".
  - When that person opens their own link, the form asks only about them and shows what the others answered.
  - When someone answered on your behalf, your link opens with that answer and a plain question: "Sigmund answered for you on 19 December: not coming. Is this right?"
  - The check page and receipt state each person's status in plain words ("Kari: not coming").
- **When:** v1 (form and data model).

### PM-10. The deadline has no defined moment (high)

- **Location:** FR-41; FR-42; FR-64; UJ-6 step 6.
- **Stories:** S8.
- **Gap:** The deadline is never defined: a date or a moment, inclusive or not, in which time zone, and what happens when summer time starts (26 March 2028). FR-64 lets the couple change it to any value with no confirmation and no warning, while FR-65 at least warns before a price change. One wrong entry locks every unanswered household at once, and the receipts guests already hold show a different date.
- **Fix:**
  - The deadline is a date. Guests can answer until 23:59 Norwegian time on that date, and every page shows it with weekday and time ("innen onsdag 1. mars 2028 kl. 23.59").
  - When the couple sets or changes the deadline, the site repeats it in words and asks for confirmation. A date in the past, or within two weeks, shows a warning with the number of households that would be locked out, as FR-65 does for prices.
  - All times shown to guests and admins are Norwegian time, including "last updated by X at Y".
  - Automated tests cover the lock at the boundary, in both winter and summer time.
- **When:** v1.

### PM-11. A price change silently rewrites what guests owe (high)

- **Location:** FR-33 ("the current prices"); FR-65; FR-36; NFR-2.
- **Stories:** S9.
- **Gap:** Hardingasete's prices will probably change between the invitations and the wedding (2028 prices; Q3 is open). FR-33 recalculates every total from the current prices, so a price change reaches guests as an unexplained new amount, turns paid households into "part paid", and gives the couple no way to honour the price the guest was shown. FR-65 warns the couple with a count, not with names or amounts.
- **Challenges a recorded decision:** memlog, "Changing prices after households have answered shows a warning with how many totals will change."
- **Fix:**
  - Decide the policy and write it down. Recommended: a household's total uses the prices in force when it last sent its answer; new prices apply to new or changed answers, unless the couple explicitly applies them to everyone. Totals are still calculated, never typed in, so NFR-2 holds.
  - If a total changes without the guest changing anything, the guest's status page says why and when.
  - A price change never turns a paid household into "part paid" or puts it in "Needs attention" unless the couple chose to apply it.
  - FR-65's warning lists the households and the amounts.
  - Invitations do not go out until the prices for 2028 are confirmed, or the invitation says plainly that prices may be adjusted and how guests will be told.
- **When:** v1, because the data model must record which prices a total used.

### PM-12. Payments cannot be matched reliably (high)

- **Location:** FR-34; FR-35; FR-61; §3.4 Payment code (D8).
- **Stories:** S10.
- **Gap:** Without a household reference, the couple matches 35 households' payments by free-text messages ("Bryllup", "bryllup kari") and by payer names that are often not the guests' (joint accounts, parents, partners). FR-34's own example, "Bryllup Sigmund", is not unique. "I have paid" stores only a time, with no amount, method or payer, and FR-61 never defines "matching". One wrong registration makes one household falsely paid and another falsely red.
- **Challenges a recorded decision:** D8, which dropped the household code because "the couple won't receive many Vipps payments" (memlog: message "e.g. 'Bryllup Sigmund'").
- **Fix:**
  - Each household gets a unique, readable payment message set by the couple, for example "Bryllup" and the household's full names. The site warns about duplicates and shows the message on "Pay now" and on the status page.
  - "I have paid" records the amount (prefilled with what is owed), the method (Vipps or bank) and the payer, if someone else paid.
  - "Matching" is defined, for example as a registered amount at least as large as the reported amount, and a report is checked again when the total changes.
  - After "I have paid", the guest sees "You reported payment on [date]; Rikke and Valdemar will confirm it", not "Not paid".
  - The status page shows each person's share, for families who pay separately.
- **When:** v1.

### PM-13. Silence looks like "no allergies" (high)

- **Location:** FR-25; FR-28; FR-30; FR-54; FR-58; SM-8.
- **Stories:** S11, S6.
- **Gap:** The admin sees only consented allergy entries. A guest with no needs, a guest who skipped the step, and a guest who declined the consent text all look the same: nothing. Since most guests have no needs, the few who skipped or declined are hidden in the crowd, and "gluten 2, lactose 1" reads as complete. A withdrawn consent or a changed allergy shows only as a generic "Changed".
- **Fix:**
  - Add an explicit "No allergies or dietary needs" answer per attending person, so that "nothing registered" shrinks to the few who skipped the step or declined consent: a list the couple can actually follow up. The GDPR review should confirm whether a "none" answer needs the same consent.
  - The summary and the allergy list show how many attending guests have nothing registered, and "Needs attention" lists them before numbers are sent to Hardingasete.
  - Allergy changes and consent withdrawals show as "Allergy changed", with the date, and stay until a couple member handles them.
- **When:** v1.

### PM-14. Every text change is a production deploy, with no safety net (high)

- **Location:** The note after FR-65 (D12); NFR-9; NFR-1, fifth bullet.
- **Stories:** S3, S2.
- **Gap:** Programme times, parking and transport details change in the months before a wedding. With the text in code, every change is a code deploy to the live site, by a beginner, in the middle of the answer period. The PRD sets no rule for deploys: no tests before, no backup before, no check afterwards that real links still work, no way back.
- **Challenges a recorded decision:** D12 (memlog: "Information page text lives in code in v1 (Rikke asks AI to change it)"). Fine for v1; a standing risk in production.
- **Fix:**
  - Before invitations, make at least the programme and the practical information editable by the couple in the admin area. If D12 stays, require the rest of this list.
  - A production deploy happens only after all tests pass.
  - A backup is taken right before each deploy, and there is a documented way back.
  - After each deploy, a check confirms that a real guest link opens the right household and that the admin counts are unchanged.
  - No deploys in the last two weeks before the deadline, except fixes for a broken guest flow.
- **When:** Decide in the architecture; in place before invitations.

### PM-15. 2027 is an open-ended build window right before go-live (high)

- **Location:** §3.2 Deferred requirements ("any If-time items not done in v1"); §3.3 Change notices to guests.
- **Stories:** S5, S3.
- **Gap:** §3.2 moves every unfinished If-time item into the months before invitations: envelope animation, English, PC layout, speech sign-up, gift list and change notices. A beginner builds them with AI help a year after the course, with no date after which only fixes are allowed. Change notices are the worst: they make the site send personal messages to guests, contradict §3.4 ("Sending"), need another data processor, and one template bug can put one guest's link in other guests' inboxes. That is the one bug that forces re-issuing every link.
- **Challenges a recorded decision:** memlog, "Email/SMS to guests when information changes stays If time."
- **Fix:**
  - Set a "ready for invitations" date (for example 1 November 2027) by which all [2027] requirements are done and the pilot (PM-5) has passed. After it, only fixes until the wedding.
  - Replace "any If-time items not done in v1" with an explicit list. Before invitations: only what reduces risk (link tracking, unfinished answers, copy or print for Hardingasete). Everything else ships only if finished before the ready date.
  - Move change notices to Out, or require that automated messages never contain personal links and are previewed per recipient before sending.
- **When:** PRD now.

### PM-16. Admin accounts can be created but never removed or recovered (medium)

- **Location:** FR-46; FR-47; NFR-4.
- **Stories:** S12.
- **Gap:** Helpers see every guest's phone number, allergies and questions. FR-47 creates accounts by a command on the server. Nothing removes or deactivates an account, resets a forgotten password, or lets Valdemar act without Rikke's server access.
- **Challenges a recorded decision:** memlog, "Rikke creates the admin accounts (couple + helpers) by command". Creating by command is fine; making every account change depend on one person's server access is not.
- **Fix:**
  - The couple can deactivate an admin account in the admin area, which ends its sessions at once.
  - A forgotten password can be reset without anyone touching the server: the partners reset each other's, and the couple resets the helpers'.
  - Valdemar can do every couple-level task without Rikke.
  - Admin passwords have a minimum length and are checked against common passwords, since helpers can read health data.
- **When:** v1 (small); before invitations at the latest.

### PM-17. UJ-3's fallback promise fails exactly when the site is down (medium)

- **Location:** UJ-3 step 6; FR-6; FR-52.
- **Stories:** S1.
- **Gap:** UJ-3 step 6 says that if "a page won't load", Synne still sees how to reach the couple. If the server, the certificate or the domain is down, the site can show nothing at all, and FR-5 rightly hides contact details on pages without a valid link. The only place a fallback can live is the message the guest already has.
- **Fix:** FR-52's invitation message includes the couple's names, the date, the deadline and both phone numbers, with "If the link doesn't work, call or text us". Rewrite UJ-3 step 6 to promise only what the site can actually deliver.
- **When:** Before invitations (FR-52 is [2027]).

### PM-18. The per-person price model is assumed, not confirmed (medium)

- **Location:** FR-16; FR-32; §7 Q1 and Q3.
- **Stories:** S9.
- **Gap:** Q1 was answered for capacity only, and Q3 (prices) is open. FR-16 and FR-32 assume a per-person cabin price for the whole weekend. Cabins are often priced per cabin. Then each guest's share depends on who shares the cabin, which the site deliberately does not know (cabin allocation is Out), and the couple ends up splitting costs in a spreadsheet.
- **Fix:** State the assumption in §7: every paid option has one price per person. If Hardingasete prices per cabin, the couple sets a per-person share and the form says so; the site never splits cabin costs. Make the price model part of what Q3 must answer before the architecture fixes the data model.
- **When:** Architecture.

### PM-19. SM-9 contradicts the scope, and numbers are retyped by hand (medium)

- **Location:** SM-9; SM-8; §3.4 Cabin allocation; §3.3 Print page; FR-58; UJ-4 step 5.
- **Stories:** S11, S9.
- **Gap:** SM-9 says the couple never opens Excel for guest logistics, while §3.4 puts cabin allocation outside the site, and there is no export or copy. Allergies with names, meal counts and the overnight list are typed by hand into emails and spreadsheets. Retyping is exactly where the allergy and bed mistakes that SM-8 forbids come from.
- **Challenges a recorded decision:** memlog, "Rikke types the numbers into an email; a dedicated print page stays If time."
- **Fix:** Either change SM-9 to "the couple never retypes data from the site" and add a [2027] requirement that the couple can copy as text (or print) the counts, the per-meal name lists, the allergy list with names and the overnight list with names; or keep SM-9 and bring cabin allocation into scope. Promote the print page to [2027] once Hardingasete has answered Q2.
- **When:** PRD now; built before invitations.

### PM-20. No record of what was sent to Hardingasete (medium)

- **Location:** FR-54; UJ-4 step 5; otherwise missing.
- **Stories:** S11.
- **Gap:** The counts are always live. Once the couple has sent preliminary or final numbers, nothing shows what has changed since, so late changes (illness, cancellations, consent withdrawals) are easy to forget to pass on.
- **Fix:** The couple can mark "Numbers sent to Hardingasete" with a date. The summary then shows, per count, the changes since that date and the people behind them, and "Needs attention" lists those changes until they are handled.
- **When:** Before invitations.

### PM-21. "Handled" and "seen" are anonymous and shared (medium)

- **Location:** FR-56; the addendum's "Needs attention" behaviour; FR-46.
- **Stories:** S6.
- **Gap:** One partner marking an item as seen removes it for both, with no record of who did it or when, and no way back. The PRD does not say whether helpers, who "change nothing", can mark items.
- **Fix:** Marking an item records who and when. Handled items can be reopened and stay visible in a "recently handled" list. Helpers cannot mark items. Allergy changes need an explicit "handled" by a couple member.
- **When:** v1.

### PM-22. SM-3 measures speed, not correctness (medium)

- **Location:** SM-3; SM-1; NFR-6.
- **Stories:** S7, S5.
- **Gap:** The usability test passes if the older relative finishes without help in under 10 minutes, even if the answer is wrong. The failures that hurt, a wrong "not coming" or a misread "whole weekend", are about correctness.
- **Fix:** Give the participant a scenario card with a known correct answer (who comes, which days, meals, overnight stay and allergies for both people). Success means the submitted answer matches the card, without help, in under 10 minutes. Note every misreading of the first question. Run at least one session on a phone through Messenger's built-in browser.
- **When:** v1 (the usability test in the first week of December 2026).

### PM-23. Moving a guest has undefined effects on answers and money (medium)

- **Location:** FR-50; FR-59; FR-60.
- **Stories:** S10.
- **Gap:** FR-50 lets the couple move a guest to another household, but does not say what happens to the person's answers, to both totals, or to payments already registered on the old household. One move can make one household "refund owed" and another "not paid" for money that was paid correctly.
- **Fix:** The person's answers move with them. Before confirming, the couple sees how both households' totals and payment statuses change. A registered payment can be split or moved between households. Both households are marked "Changed".
- **When:** v1.

### PM-24. Production logs leak links and personal data, and the operator relies on AI help (medium)

- **Location:** NFR-3 (only fictional data in AI tools); NFR-4; otherwise missing.
- **Stories:** S2.
- **Gap:** A personal link is full access to a household, and web logs record links [R 4.1]. Error output can include names and answers. The beginner operator's main help is an AI assistant, which NFR-3 forbids for real data. In an outage she will either break the rule or be stuck.
- **Fix:** Link codes, names, contact details and allergy information are never written to logs or shown in error output in production; codes in logged addresses are masked. Guests and admins see friendly error pages only. The runbook (PM-3) says what may be shared with AI tools when debugging production.
- **When:** Architecture.

### PM-25. Guests who will not use a link have no planned path (medium)

- **Location:** §7 Assumptions ("Guests get their link digitally and can open it"); §1 Who it is for; §3.3 English; CM-2.
- **Stories:** S4.
- **Gap:** The research found that about half of the couples used paper or phone for the oldest guests [R 2.2], and the PRD itself says a few guests do not read Norwegian. The PRD assumes everyone gets and uses a link, so anyone who does not becomes an unplanned phone call, counted against CM-2 and indistinguishable from a failure of the site.
- **Fix:** Before invitations, the couple marks in the guest list who gets an assisted RSVP (phone, paper, or a named family helper) and who needs English. Those households stay in "Needs attention" until the couple has entered their answers (FR-63), and they are kept out of SM-6 and CM-2. Decide from that list whether English (§3.3) is needed before invitations.
- **When:** Before invitations.

### PM-26. "Ask us" does not say the helpers read the questions (low)

- **Location:** FR-43; FR-46; FR-66.
- **Stories:** S12.
- **Gap:** Guests write to "us", meaning the couple, but all three helpers read every question. The privacy page says helpers can see data, but nobody reads it before asking something personal.
- **Fix:** The "Ask us" form says who reads the questions, or questions are visible to the couple only.
- **When:** v1.

## Already well covered

These failure modes came up in the pre-mortem and the PRD already handles them. Keep them as they are.

- **Link scanners and chat previews.** FR-3 (opening a link never changes anything) and FR-4 (generic titles and previews) mean that Messenger's preview fetcher and email scanners can neither answer for a guest nor leak names into a chat. C4's definition of "started" keeps any future tracking honest.
- **Strangers and dead links see nothing.** FR-5, together with NFR-4 (at least 128-bit codes, hidden from search engines, the link not passed on, wrong attempts slowed down), means a forwarded or guessed link exposes nothing. PM-4 only asks for kinder wording for guests whose link was cut off.
- **One lost or misdirected link is a small problem.** FR-51 and FR-53 let the couple copy a link again, or replace one guest's link without touching the rest of the household, and UJ-3 walks through it. When the architecture settles D14, it must keep FR-51 possible.
- **The domain and link format are frozen** before invitations (NFR-1, first bullet). That is the right rule; PM-3 adds who keeps the domain alive.
- **A failed save is never silent** for the guest, and what they typed is kept (NFR-1, third bullet).
- **A second household member does not create a duplicate answer** when the first has already sent: FR-24, FR-37, FR-38 and UJ-2 step 5 show the existing answer instead of an empty form. PM-8 covers only the simultaneous case.
- **Skimming errors are designed down.** Nothing is ticked in advance (FR-14); questions and meals follow the days a person is present (FR-15, FR-17); the cabin rule is stated before the choice (FR-16); the check page has a "Change" link per part (FR-21); errors appear at the field, with a summary (FR-22).
- **Totals cannot drift from the data.** Counts, totals and statuses are calculated, never stored (NFR-2); the total is the same on the check page and the receipt (FR-33); every count opens the people behind it (FR-55); and automated tests check the counts against a hand-made expected-results list (FR-69, SM-2).
- **Consent never blocks the RSVP** (FR-28), withdrawal works after the deadline (FR-30, FR-42), and verbal consent taken by the couple is recorded (FR-31).
- **What still works after the deadline is explicit** (FR-42), and the couple can complete or fix any household after it (FR-63).
- **Helpers cannot change data, and the server enforces it**, not just the page (FR-46, NFR-4).
- **Money as amounts, not flags.** Registered amounts with a calculated status, corrections and undo (FR-59, FR-60); what remains or is refunded after a change (FR-36); a red flag for an unmatched "I have paid" (FR-61). PM-11 and PM-12 sharpen these; the foundation is right.
- **The site sends nothing** (§3.4 Sending): there is no mass mail-out that can misfire. Keep it that way (PM-15).
- **Bed capacity is settled** (Q1: far more beds than guests), so no bed limit can lock guests out.
- **No planned downtime in the last week before the deadline, and a restore test before invitations** (NFR-1). These are the right instincts; PM-1 and PM-3 make them hold.
- **The course version is well protected.** NFR-8, UJ-6 and SM-5 make the examiner's path independent of Rikke's accounts and keys, with seeding as a separate documented step.
