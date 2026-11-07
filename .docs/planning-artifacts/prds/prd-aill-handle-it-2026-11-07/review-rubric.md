# PRD Quality Review — AI'll handle it

*Reviewed: `prd.md` and `addendum.md` (draft, 2026-11-07). Context from `.memlog.md` and the input documents. Stakes: real launch. This PRD sits at the top of the chain and feeds UX, architecture and stories.*

## Overall verdict

This is a decision-rich, honest PRD. It has a clear thesis ("it must work"), journeys whose protagonists actually drive requirements, 69 traceable FRs, measurable accessibility and runnability NFRs, and an unusually complete record of what was rejected and why. The risks are delivery and correctness at the edges:

- 65 v1 FRs with no priority order, for a solo beginner with about five weeks to delivery.
- Payment and count rules with holes exactly where SM-2 demands a 100 % match: households that owe nothing, "matching" payments, and the meal list.
- Journeys that still describe two features deferred to 2027.

A focused fix pass on those three areas would make it ready for UX and architecture.

## Decision-readiness — adequate

Decisions are written as decisions, with who made them and what was given up:

- §9 lists every deviation from the brief with a reason, including where Rikke overruled Claude ("Claude proposed storing names only (data minimisation); Rikke chose otherwise").
- The addendum's *Rejected alternatives* names the cost of each choice: no pre-ticked "everyone is coming", one link per guest rather than per household, no bed limit.
- Trade-offs are spelled out where guests will feel them: "Filippa can sleep there one night, but pays for both" (UJ-2, FR-16) and "the last save applies" (§3.4).
- D14 goes to architecture together with the conflict it creates with FR-51.
- The questions in §8 are genuinely open, and each has an owner and a point at which to revisit it.

The biggest trade-off in the project is missing from the document: how much v1 scope fits into the time left. The memlog shows the risk was raised and partly answered by deferring four FRs. The PRD itself has no risks section and no `[NOTE FOR PM]`, and nothing orders the 65 v1 FRs. Two smaller tensions are also glossed over.

### Findings

- **[high]** No priority order or cut line inside v1 (§3.1, §7 Constraints, §9 "New in v1") — §3.1 puts every FR without a [2027] or If-time mark in v1: 65 FRs plus NFR-1–NFR-9. The developer is "a solo developer, early in learning to program". The usability test is about four weeks away and delivery about five and a half, and UX, architecture and stories are not written yet. §9 shows that scope *grew* during the PRD work: Needs attention, counts that open, the "Changed" marker, admin settings with a price warning, the privacy page and verbal consent were added; a payment ledger replaced the paid/not-paid status; and "I have paid" moved from optional to v1. The PRD records neither the risk (memlog, line 72) nor a fallback. The teacher's feedback asked for exactly this: "Prioriter kjernen, så resten kan kuttes uten at appen blir halv." If time runs short, nothing tells sprint planning what to protect. *Fix:* add a short "Delivery order and cut line" to §3: (1) the features the usability test needs, with a date before the test; (2) the features the examiner needs; (3) a named list of v1 FRs that move to [2027] first if work falls behind.
- **[medium]** "Needs attention" is only designed for after the deadline (FR-56, UJ-4) — UJ-4 takes place after the deadline, so the PRD never shows the list on the day the links go out. On that day all ~35 households are "not answered", and their items bury the questions and payment mismatches. Before a household answers, the couple's only way to clear its item is "handled", and then the household leaves the list for good. The dated contact note that UJ-4 relies on (FR-62) is [2027]. *Fix:* decide when not-answered households enter the list (for example N days before the deadline, or as one line linking to FR-55's list), and whether "handled" hides them permanently.
- **[medium]** Q4's impact is understated (§7 Q4, §8) — the PRD says that a "yes" from Hardingasete on direct payment "may change FR-34". In fact it would affect about nine FRs: FR-34–FR-36, FR-56's payment items, FR-59–FR-62 and the payment details in FR-64, plus UJ-1 step 7, UJ-5 and CM-3. The research also leans towards paying the venue directly ("payment preferably goes to a third party", R 2.2). *Fix:* state the default ("v1 collects payment to the couple whatever Hardingasete answers", or the opposite) and what a "yes" would change.

## Substance over theater — strong

The personas earn their place. Each protagonist produced concrete requirements:

- **Sigmund (78):** the preset "I am Sigmund" (FR-12), "Read more" that opens in place (FR-19), 44 × 44 px targets (NFR-5) and "one obvious next step".
- **Arild's split household:** the rules in FR-14–FR-16.
- **Synne:** FR-5, FR-53 and the exceptions in FR-42 for what still works after the deadline.
- **Ingrid:** FR-68, NFR-8 and SM-5.

There is no boilerplate vision. "What matters most" states Rikke's priority in terms that can be tested ("The couple must never have to send a new invitation by hand because the site failed"). The NFRs are specific to this product: "checked for sage green on soft white", "a test link is sent through all three channels and opened on both Android and iPhone", "no planned downtime in the last week before the deadline", "Amounts are whole kroner". No differentiation section was written just to fill the template. The only padding is in the long-term metrics.

### Findings

- **[low]** Some metrics have no number (§2 SM-10, CM-1–CM-4) — SM-10's target is "Few". CM-1–CM-3 have no threshold, and CM-1 cannot be counted reliably while the change history (FR-40) is [2027]. CM-4 is a design rule that FR-26 and FR-28 already enforce, not a metric. *Fix:* give SM-10 a number or drop it, and give each CM a threshold and a data source, or label the CMs as things to watch.

## Strategic coherence — strong

The PRD has a thesis and follows it. §1 "What matters most" makes three bets: the site must work, it must be simple for guests, and the answers must be easy to trust.

- **Features serve the bets.** The link is the login and already knows who is answering. Totals and statuses are always calculated (NFR-2). Every count opens the people behind it (FR-55). FR-69's expected-results tests prove the numbers.
- **Metrics test the thesis rather than measure activity.** SM-6 measures exactly the failure Rikke fears, SM-2 and SM-8 measure trust, and SM-3 and SM-7 measure simplicity. CM-1–CM-3 guard against hitting those targets the wrong way.
- **The scope fits the problem.** The MVP replaces Messenger and Excel, and the two-delivery table keeps course v1 and production apart.

The weak points are how the scope rule and the test data are applied.

### Findings

- **[medium]** The scope rule is not in the PRD and is applied unevenly (§3.1, §3.2) — the rule behind the four [2027] tags ("v1 = what the examiner and usability test need; [2027] = what only matters with real guests") exists only in the memlog. By that rule several v1 FRs look like 2027 work: FR-53 (replacing a forwarded link), FR-31 (the couple records verbal consent), FR-65 (a warning when real prices change after real answers) and FR-4 (previews in chat apps). Some may be worth keeping because they are cheap or useful for the examiner, but the PRD doesn't say so. Neither a reader nor sprint planning can apply the rule. *Fix:* state the rule in §3, then move those FRs to [2027] or give each a one-line reason for staying in v1.
- **[medium]** SM-2 can pass while the riskiest rules go untested (FR-68, FR-69, SM-2) — SM-2 is the PRD's proof that the numbers can be trusted. But FR-68's extra test households are only "one that has paid, one that hasn't answered, and a single guest with an allergy". No test household is part paid, owes a refund, has an "I have paid" without a matching payment, has declined entirely, or is a Saturday-only guest who owes 0 kr. The pre-PRD expected-results list included "guest only Saturday", and it was dropped. *Fix:* require at least one test household for each payment status, plus one with an unmatched "I have paid", one that declined entirely, one Saturday-only guest and one withdrawn consent. Build the expected-results list from them.

## Done-ness clarity — adequate

Most FRs have a testable consequence, often a precise one:

- FR-3: "Opening a link never changes anything".
- FR-14: "Nothing is chosen in advance".
- FR-15's rule for which meals are offered.
- FR-21's "Not provided" for skipped questions, and FR-22's error summary.
- FR-29's consent record.
- FR-42's list of what locks after the deadline and what still works.
- FR-65's warning with the number of affected households.

NFR-5 and NFR-8 have real limits: 4.5:1, 200 %, 320 px, 44 × 44 px, 15–20 minutes.

The gaps cluster where SM-2 demands 100 %. The payment status, "matching" payments, the meal list and the count definitions are exactly the rules the expected-results list must encode, and they are not all defined. Several FRs also contradict each other in the guest flow, and four NFR lines still use adjectives where they need numbers.

### Findings

- **[high]** The payment status contradicts itself for households that owe nothing (addendum "Payment status (FR-60)", FR-34, FR-59, UJ-2) — the table maps "0 kr → Not paid" and "Exactly the total → Paid", and both rows match a household whose total is 0. That covers every household that declines, and every Saturday-only guest without a cabin: Saturday lunch and dinner are paid by the couple, and Saturday breakfast requires being there from Friday (FR-15, FR-32). FR-34 still offers all of them "Pay now / Pay later", right after "We're sorry you can't make it".

  The table also compares "Amount received" with the total. FR-59 and UJ-2, however, register refunds and expect "the household's balance is zero again", so after a refund the table would still say "Refund owed". These rules feed the payment overview, "Needs attention" and the SM-2 tests. *Fix:* define balance = received − refunded − total; add the statuses "nothing to pay" and "no answer yet"; skip FR-34's payment choice when the total is 0.
- **[medium]** The meal list and the count definitions are never written down (FR-15, FR-18, FR-32, FR-54) — FR-15 offers "a meal" on the days a person is there, and FR-54 counts "per meal", but the PRD never lists the meals. It mentions Saturday lunch and dinner only as paid by the couple. Nothing says whether the form asks about them or derives them from Saturday attendance, and the wedding-dinner count is the number Hardingasete needs most (UJ-4 step 5). FR-18's arrival choices are not listed either (D11 in the pre-PRD proposed four, plus "Don't know"). FR-54's "households who have answered yes" is undefined for a mixed household like Arild's. *Fix:* add a meal table (day, meal, paid by the guest or by the couple, who is offered it, asked or derived), list the arrival choices, and say for each FR-54 count whether it counts people or households.
- **[medium]** "Matching payment" is undefined (FR-56, FR-61, addendum "Needs attention" table) — a household turns red when "I have paid" has "no matching registration", and the item leaves the list when "a matching amount is registered". The PRD doesn't define "matching": equal to the total, or any amount? Open cases include a part payment registered after the report, a changed answer after the report, and a second "I have paid" after the item was marked handled. CM-3 counts these mismatches, so the definition also defines the metric. *Fix:* define "matched", for example "the registered net amount covers the total shown when the guest reported". State when each kind of "Needs attention" item comes back after it has been cleared.
- **[medium]** The thank-you page, the payment step and the returning guest's first page contradict each other (FR-7, FR-23, FR-24, FR-34, FR-37, UJ-1 steps 6–7) — the thank-you page ends with "You can now safely close the invitation", and only after that does FR-34 ask "Pay now" or "Pay later". An older guest who follows the instruction never sees how to pay. The screen also has two next steps, against UJ-1's "one obvious next step". Separately, FR-24 says that once a household has answered, the link "always opens its status", while FR-7 and FR-37 say it opens the invitation with a "See or change answer" button. *Fix:* put the payment choice before the closing line, or show the closing line only after the choice. Decide what a returning guest sees first.
- **[medium]** The leave warning cannot cover the most common way of losing a half-filled form (FR-20, NFR-1, addendum row "Saving an unfinished answer") — "A warning before leaving the form covers v1" assumes the warning appears. Phone browsers cannot reliably warn when a tab is closed, the guest switches app, or the phone discards a background tab. That is exactly what happens when an older guest switches to Messenger halfway through. *Fix:* limit FR-20 to links inside the site and the Back button. Decide whether answers survive a closed tab (for example, kept in the browser until they are sent) or accept and state the loss.
- **[medium]** It is unclear whether consent is given once per household or once per person (FR-26, FR-27, FR-29, FR-30) — "the respondent" gives consent (FR-26), and the site stores "who gave it" (FR-29). But withdrawing deletes "that person's allergy information" (FR-30). Open questions:
  - Does Arild's single yes cover all four people?
  - Can Marie withdraw a consent Arild gave for her?
  - What happens to the others' data when someone edits the answer later and answers No?

  *Fix:* store consent per person (given by whom, for whom, which text version). Say who may withdraw for whom, and how the question behaves when someone edits the answer.
- **[medium]** The privacy page link conflicts with the page for visitors without a link (FR-5, FR-66) — FR-66 links the privacy page "from the bottom of every page", and the page must say "how to contact the couple" and who the couple are. FR-5's page for visitors without a valid link may show "no names, phone numbers, date or place". A privacy link at the bottom of that page reopens what the addendum's last rejected alternative closed: "Anyone typing a random address would see both phone numbers". *Fix:* decide whether the privacy page can be reached without a valid link. If yes, say what it may show; if no, exempt the FR-5 page.
- **[medium]** No reference screen and no oldest supported phone or browser (FR-7, NFR-1, NFR-7) — "Without scrolling on a phone", "an ordinary phone on 4G" and "both Android and iPhone" name no screen size and no oldest supported version. Above the fold, FR-7 must fit the couple's names, date, place, up to four household names, the deadline and a 44 px button at a large text size. Whether that fits depends entirely on the screen, and the guests most at risk are those with older phones. *Fix:* name a reference screen size (for example 360 × 640 CSS px) and the oldest browser and OS versions to support, and test against both.
- **[medium]** NFR-4 uses adjectives where the research gave numbers, and HTTPS is missing (NFR-4) — four of the eight lines rely on adjectives: "a modern password-hashing method", "expire after a period of inactivity", and "slowed down" twice. The research the section cites (R 4.2) gives Argon2id, a 15–30 minute idle timeout and 5 login attempts per minute. Nothing requires HTTPS in production, although the link is the guests' only login. *Fix:* carry the research values into NFR-4 as defaults for architecture to confirm, and add "HTTPS only in production".
- **[medium]** Nothing would notice if the site goes down (NFR-1, SM-6) — NFR-1 is the thesis written as an NFR. But "available from the invitations until the wedding" has no target and no way to detect an outage, so the couple would hear about it from guests. That is exactly the failure SM-6 counts. Nothing covers the quiet ways links stop working in the months before the wedding either: an expired domain or TLS certificate, or an unpaid hosting bill. *Fix:* add an external uptime check that alerts the couple, and require the domain, certificate and hosting to be renewed until after 31 August 2028.
- **[low]** The deadline time is not defined (FR-41, FR-42, UJ-6 step 6) — the PRD doesn't say whether the deadline is a date or a time of day, whether guests can still answer on the deadline day, or which time zone applies. Off-by-one-day bugs are common here, and UJ-6's "move it to yesterday" test won't catch one. *Fix:* "Guests can answer until 23:59 Norwegian time on the deadline date."
- **[low]** The allergy list drops the note (FR-58 vs FR-25) — the list for the kitchen shows "names and categories" but not FR-25's short note. An "other" entry would reach Hardingasete with no content, which works against SM-8 (zero allergy mistakes). *Fix:* include the note.
- **[low]** Some requirements have no limit to test (FR-43, FR-48) — "Quick tasks work well on a phone" and "a short question" give nothing to test against. *Fix:* for FR-48, name the screen width and a maximum number of taps per task; for FR-43, set a character limit.

## Scope honesty — strong

The PRD states what is left out instead of leaving the reader to guess:

- §3.4 lists 16 exclusions, most with a reason ("it would show guests who else is coming", "the last save applies (C5)").
- §3.3 keeps the If-time items separate, and [2027] tags mark the deferred FRs.
- §9 and the addendum record every change from the brief and every rejected alternative, including a proposal Claude withdrew (showing contact details on pages without a valid link).

The number of open items is low and fits the stakes: eight questions in §8, none blocking, and two assumptions in §7, with no inline `[ASSUMPTION]` tags left. The weak spots are how §3.2 treats If-time items, and deletion.

### Findings

- **[medium]** If-time items read as both optional and required before launch (§3.2, §3.3, §1, addendum "Rejected alternatives") — §3.2 lists "any If-time items not done in v1" under *Before invitations go out*, while §3.3 is titled "If time and capacity allow". This matters for two items:
  - **English** is the only plan for the "few who don't read Norwegian" named in §1.
  - **"Change notices to guests"** (email or SMS) needs the very capability the addendum gave as the reason to reject self-service link recovery ("The site would have to send email or SMS"). It also needs an SMS provider, which appears nowhere, and guest contact details, which FR-49 makes optional.

  *Fix:* mark each If-time item as required before invitations, optional, or dropped. If English stays optional, state a fallback for guests who don't read Norwegian.
- **[low]** The deletion promise says nothing about backups or copies (NFR-1, NFR-3, FR-45, FR-67) — the PRD promises "Real data is deleted by 31 August 2028". But the daily backups, the questions emailed to the couple and the allergy list emailed to Hardingasete all fall outside the one-step delete. *Fix:* state how long backups are kept (expiring before the deletion date, or deleted together with the data), and mention the copies outside the site on the privacy page.

## Downstream usability — adequate

Traceability is strong. Almost every FR has a source tag (UJ, C/D/Q, R x.y or brief), the IDs have no gaps, and NFR-9 commits stories to cite FR IDs. The addendum gives the next steps concrete material:

- For `bmad-ux`: the payment-status table and the rules for when items leave "Needs attention".
- For `bmad-architecture`: the D14 conflict with FR-51, and the note that the data model should allow FR-40 later.

Two things weaken it as a source document. The journeys, which UX will build from, still describe deferred features, and there is no glossary to keep the domain terms consistent.

### Findings

- **[high]** The journeys still describe features deferred to 2027 (UJ-2 closing paragraph, UJ-4 step 4, UJ-5 step 4) — the four FRs were deferred after the full draft was written (memlog), and two of the deferrals never reached the journeys. UJ-2 says the couple "can open a history of who changed what and when", which is FR-40 [2027]. UJ-4 and UJ-5 have Rikke add "a dated note" that "shows in the not-answered list and the payment overview", which is FR-62 [2027]. UX builds its flows from these journeys. A plan that describes features the delivered app doesn't have matches one of the grading guide's warning signs: planning documents that describe a different app from the one delivered. *Fix:* mark those steps "(2027)" and say what Rikke does in v1 instead (mark the item as handled).
- **[medium]** There is no glossary, and the core terms drift (§1, FR-16, FR-23, FR-24, FR-32, FR-54, FR-57, FR-61) — several words are used for one thing, or one word for several things:
  - "Overnight", "cabin", "accommodation" and "beds" all name one choice.
  - "Receipt", "thank you" and "status" name the pages after sending.
  - "The overview" means both the summary (FR-54) and the full overview (FR-57), so "marked red in the overview" (FR-61, UJ-5) is ambiguous.
  - "Invitation" means the site, the front page and the message (FR-52).
  - A household is "a couple or a family" (§1), although single-guest households exist.
  - "Respondent", "link owner" and "guest" are never defined, yet FR-12, FR-29 and FR-38 depend on the difference.

  *Fix:* add a glossary of about 12 terms and use one term per concept.
- **[low]** UJ-3 combines five scenarios, and most journeys lack "Done when" (UJ-3, UJ-2–UJ-5) — "Synne has lost her link" also covers a forwarded link, the time after the deadline, the couple filling in an answer, and an error page. The protagonist switches to Rikke at step 2. Only UJ-1 and UJ-6 have a "Done when". *Fix:* split UJ-3 or label its scenarios, and add "Done when" to UJ-2 to UJ-5.

## Shape fit — strong

The PRD handles a mixed product well:

- The guest side is consumer-like and must work for older guests, and its journeys carry real weight.
- The admin side has a single operator and is written as a list of capabilities (FR-46–FR-65), without padding journeys.
- The examiner journey (UJ-6) turns grading criterion 6 into steps that can be tested.

The level of formality (69 FRs, numbered SMs and CMs, source tags) suits a real launch that is also graded on whether the process can be traced. The two-delivery table is the right structure for course v1 versus production.

### Findings

- **[medium]** No journey for the couple's setup and send-out (§4, FR-47, FR-49–FR-53, FR-64) — every guest journey starts with a link that has already been sent, and nothing covers how it got there. Rikke must create admin accounts, enter ~35 households and ~70 guests, fill in the settings, and copy and send 70 links by hand. This is the step SM-6 is about. It is also where a wrong link shows one household's answers and allergies to someone else, which is why FR-52 exists. UX gets no flow for the couple's most error-prone task. *Fix:* add UJ-7 "Rikke sets up the wedding and sends the links", ending with NFR-1's test of SMS, Messenger and email.

## Mechanical notes

- **IDs:** FR-1–FR-69, NFR-1–NFR-9, UJ-1–UJ-6, SM-1–SM-10 and CM-1–CM-4 are contiguous and unique. Every `R x.y` reference resolves to a section of `research.md` (1.7, 3.1, 3.2, 3.3, 3.5, 4.1, 4.2, 4.4, 5).
- **Source tags:**
  - FR-64 and FR-65 cite UJ-6, but UJ-6 only mentions moving the deadline. Prices and the price-change warning appear in no journey; their source is D12 and the memlog.
  - FR-47 has no source tag.
  - FR-30 cites "GDPR Art. 7(3)", a type of source the legend at the top doesn't list.
  - §3.3 settles Q9 (the Vipps QR code) but never cites it.
  - D2 (meals are chosen independently of the cabin) is neither cited nor stated as a rule.
- **Duplicates:** the third bullet of FR-56 and FR-61 specify the same red marking, which risks two stories for one rule. FR-7 and FR-41 both say where the deadline is shown.
- **Wording conflicts:**
  - NFR-4's "Only logged-in admins see guest answers" contradicts FR-2 and FR-24 as written, since guests see their own household's answers. Say "other households' answers".
  - NFR-6's "A PC shows the phone layout" conflicts with FR-48's "may be designed for a PC". Limit NFR-6 to guest pages.
- **Addendum formatting:** a stray table row ("Saving an unfinished answer to continue later | Moved to If time | …") sits after the *Test data note (FR-68)* paragraph, separated from the *Rejected alternatives* table, so it renders as broken text.
- **Assumptions Index round-trip:** no inline `[ASSUMPTION]` tags remain (the memlog says all were resolved), and §7 lists two assumptions, so there is nothing to cross-check. There are no `[NOTE FOR PM]` callouts. That is acceptable, since the decisions were closed with Rikke, but the scope/time risk deserves one.
- **Required sections:** all are present for real-launch stakes except a glossary. The schedule risk is recorded only in the memlog.
- **Frontmatter:** `status: draft`. Update it when the PRD is finalised.
