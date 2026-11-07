---
title: "Review of the PRD against the grading guide (sensorveiledning del 1)"
reviewed: "prd.md and addendum.md at commit 7384511 (status: draft)"
lens: "Course examiner: the seven criteria and the warning signs in chapter 5"
created: 2026-11-07
---

# Review: the PRD through the examiner's eyes

This is one of the five reviews in the PRD reviewer gate (see the last entry in `.memlog.md`). It reads [prd.md](prd.md) and [addendum.md](addendum.md) the way the examiner will: against the seven criteria in the [grading guide](../../../../docs/sensorveiledning/sensorveiledning-del1.md) and its chapter 5, *Typiske varseltegn*. It also uses the teacher's [feedback on the brief](../../briefs/brief-aill-handle-it-2026-09-23/tilbakemelding-product-brief.md), because the examiner will compare the PRD with what the brief and the feedback promised.

Context: solo beginner; today is 7 November 2026; usability test in the first week of December (around 30 Nov–4 Dec); delivery mid-December; no UX, architecture, stories or code yet.

## Verdict

**A strong process document that promises too much product.** The PRD gives criterion 1 an unusually good start. Almost every requirement names its source, decisions and AI corrections are written down, course v1 is kept apart from production, and the examiner's own journey (UJ-6) turns the README and runnability into requirements.

The risk is in criteria 2 and 3. v1 holds 65 functional requirements, all equally important, for a beginner with about 3.5 weeks to the usability test and 5.5 weeks to delivery. Some of the rules the tests must check are not defined, such as which meals are counted, what a 0 kr total means, what a "matching" payment is, and what happens to answers left over after an edit. If time runs out, the gaps will look unplanned, and the PRD will describe a bigger app than the one delivered.

**Recommendation:** fix SV-1 to SV-4 before UX and architecture start. They are PRD edits plus one new file, roughly half a day. Take the medium findings in before stories are written. Nothing here calls for rethinking the product.

## Findings at a glance

| Severity | Count |
|---|---|
| Critical | 1 |
| High | 3 |
| Medium | 12 |
| Low | 7 |

| ID | Severity | Criterion | Location | Finding |
|---|---|---|---|---|
| SV-1 | Critical | 2 | §3.1, §7 | No priority or cut line inside v1; nothing says what must work by the usability test |
| SV-2 | High | 3 | FR-15, FR-23, FR-32–34, FR-39, FR-54, FR-56, FR-60–61 | Rules behind counts, totals and payment status have gaps |
| SV-3 | High | 3 | FR-68, FR-69, Q8 | Expected-results list not written; seed data too thin to exercise the rules; no seeded settings |
| SV-4 | High | 7 | UJ-1 to UJ-3, FR-68 | Personas may be real relatives, and they become seed data |
| SV-5 | Medium | 1, 2 | UJ-2, UJ-4, UJ-5 | Journeys promise [2027] features (change history, dated notes) |
| SV-6 | Medium | 2 | §3.1, §6 | Scope principle and [2027] reasons missing; production-only NFRs unmarked |
| SV-7 | Medium | 1 | frontmatter, §8, §9, brief | No PRD change log; the brief contradicts the PRD; Hardingasete's answers could reshape v1 |
| SV-8 | Medium | 1 | NFR-9 | Traceability stops at the stories |
| SV-9 | Medium | 3 | §2, §6 | No QA approach beyond the expected-results test |
| SV-10 | Medium | 3 | FR-41, FR-42 | Deadline moment, server enforcement and test clock undefined |
| SV-11 | Medium | 3 | FR-22, FR-26–28, FR-43, FR-59 | Validation rules and input limits undefined |
| SV-12 | Medium | 4 | SM-3, SM-4 | The usability test has no protocol |
| SV-13 | Medium | 4 | FR-51, FR-54–58 | Empty states and admin confirmations missing |
| SV-14 | Medium | 6 | FR-68, NFR-8, UJ-6 | Test links not fixed, no reset, tests may share the database |
| SV-15 | Medium | 1 | header, `.memlog.md` | This session's prompts and AI corrections are not in the session log yet |
| SV-16 | Medium | 5, 2 | FR-63, FR-31 | The couple's override could become a second RSVP form |
| SV-17 | Low | 3 | FR-7, FR-20, SM-1, NFR-4, NFR-7 | Some measures are too vague to test |
| SV-18 | Low | 4 | FR-24, NFR-6 | Two UX contradictions |
| SV-19 | Low | 4 | interface labels | No Norwegian glossary for the interface |
| SV-20 | Low | 1 | FR-47, FR-52, FR-67 | Three requirements have no source |
| SV-21 | Low | 7 | end of `addendum.md` | A stray table row |
| SV-22 | Low | 7 | this folder | The extract files are unexplained |
| SV-23 | Low | 1, 2 | `inputs`, §2 | Proposal not referenced; two brief success criteria dropped from §2 |

## What already works

Keep these. They are what the examiner looks for.

- **Sources on requirements.** 66 of 69 FRs name a journey, decision or research section. This is exactly the *sammenheng plan–kode* that criterion 1 asks for.
- **Visible AI steering.** §9 and the addendum's *Rejected alternatives* say where Claude proposed something and Rikke chose otherwise: name-only storage, contact details on unknown-link pages, the research's one-link-per-household assumption, and the wording of the invitation message. The round 2 commit message (`a9b95e8`) says the same.
- **Course v1 separated from production.** The *Two deliveries* table, §3.2 and SM-6 to SM-10 act on the teacher's second change request.
- **The examiner as a user.** UJ-6, NFR-8 and SM-5 promise no keys, a working `.env.example`, seed data with test links and logins, email to the console, one test command, and 15–20 minutes. That is the same limit the guide gives the examiner.
- **A meaningful automated test target.** SM-2, FR-69 and NFR-2 ("calculated, never stored") make the core numbers testable against a hand-made list, as the teacher asked.
- **Concrete accessibility targets.** NFR-5 gives numbers that can be checked: 4.5:1 contrast, 320 px, 200 % zoom, 44 px targets, keyboard use and the error summary.
- **Clear scope edges.** §3.4 says what is out and mostly why, and If-time items are marked in the journeys.
- **Iteration in git.** The first draft and the two review rounds are separate commits with descriptive messages on their own branch.

## Criterion by criterion

| Criterion (weight) | How well the PRD sets it up | Main risk | Findings |
|---|---|---|---|
| 1. Process and AI steering (30 %) | Strong | The chain stops at stories; the PRD drifts away from the app if it isn't updated | SV-5, SV-7, SV-8, SV-15, SV-20, SV-23 |
| 2. Functionality and scope (20 %) | Good content, too much of it | Unplanned gaps at delivery | SV-1, SV-5, SV-6, SV-16 |
| 3. QA and testing (15 %) | Good starting points | Undefined rules lead to tests that copy the code; thin seed data | SV-2, SV-3, SV-9, SV-10, SV-11, SV-17 |
| 4. Design and UX (10 %) | Strong expectations | Empty states, a usability test without a protocol, inconsistent labels | SV-12, SV-13, SV-18, SV-19 |
| 5. Code quality and architecture (10 %) | Adequate: linter and formatter required, stack left to the architecture | Two copies of the RSVP logic | SV-16 |
| 6. README and runnability (10 %) | Strong | Test links that change every time the seed runs | SV-14 |
| 7. Repo hygiene (5 %) | Good rules | Personas that may be real; small leftovers | SV-4, SV-21, SV-22 |

## Findings

Each finding gives the location, what is wrong, why it matters for the grade, and a fix at PRD level.

### Critical

#### SV-1 · No priority or cut line inside v1

- **Criterion:** 2 (also 3 and 6)
- **Location:** §3.1; §7 *Dates*; SM-3 and SM-4; the scope/time-risk and scope-principle entries in `.memlog.md`
- **Finding:** §3.1 puts every FR not marked [2027] or If time in v1. That is 65 requirements, many with several parts, and nothing says which matter most. The memlog shows that Claude raised the time risk: about 3.5 weeks to the usability test and 5.5 to delivery, before UX, architecture and stories exist. The response was to defer four FRs. The PRD still has no build order, no set of features that must work by the usability test, and no agreed list of what to cut first. The teacher said the same about the brief: «alt står som like viktig. Prioriter innenfor «In»» and «Prioriter kjernen, så resten kan kuttes uten at appen blir halv».
- **Why it matters:** Criterion 2 is judged against the plan. At D–E, «omfanget er klart mindre enn proposal tilsier uten god begrunnelse». A cut that was planned and justified in advance reads very differently from features that are simply missing. Time pressure also squeezes the tests (criterion 3) and the README trial (criterion 6), which come last. Finally, SM-3 and SM-4 need a working guest flow and admin summary by the end of November, and the PRD does not make sure those come first.
- **Suggested fix:**
  - Add §3.1a *Priority within v1* with three tiers. Tier 1 is the usability-test build, Tier 2 completes the course version, and Tier 3 is what gets cut first. Appendix A has a proposal.
  - Add dates to §7. Proposal: plan and expected-results list by 13 Nov, Tier 1 by 27 Nov, usability test in the first week of December, feature freeze on 10 Dec.
  - Add the rule: "Tier 3 items not done by feature freeze move to [2027], and the change log records why."
  - Add a short *Risks* subsection listing the riskiest parts (Appendix B).

### High

#### SV-2 · The rules behind counts, totals and payment status have gaps

- **Criterion:** 3 (also 2 and 5)
- **Location:** FR-15, FR-16, FR-23, FR-26, FR-29, FR-30, FR-32 to FR-34, FR-39, FR-54, FR-56, FR-59 to FR-61; the addendum tables *"Needs attention" behaviour* and *Payment status*
- **Finding:** SM-2 and the expected-results list depend on rules that are not settled yet:

  | # | Where | Gap | Proposal for Rikke to confirm |
  |---|---|---|---|
  | 1 | FR-54, FR-32 | Which meals are counted? Saturday lunch and dinner are not choices, but Hardingasete needs those numbers too. | Count five meals. Saturday lunch and dinner are counted as everyone present on Saturday. |
  | 2 | FR-15, FR-37 | What happens to old answers after an edit, for example if someone drops Friday or stops coming? NFR-2 counts from stored answers, so leftovers give wrong numbers. | Answers for days or people no longer coming are removed on save. Allergy data and consent for someone not coming are deleted. |
  | 3 | FR-34, FR-60, addendum | With a 0 kr total, both "Not paid" and "Paid" match in the addendum table, and FR-34 still offers "Pay now / Pay later". | Status "Nothing to pay" and no payment step. A household that hasn't answered has no payment status. |
  | 4 | FR-61, addendum | What is a "matching payment"? The guest's report has no amount (FR-35). | Red while the latest "I have paid" is newer than the latest registered payment and the status is not "Paid". |
  | 5 | FR-59, FR-60 | How do refunds count toward the status? | Amount received = payments minus refunds. |
  | 6 | FR-23 | Which receipt message does a household get when some people come and some don't? | The "coming" message if at least one person comes. |
  | 7 | FR-39, FR-63 | What marks a household "Changed"? FR-30 says consent withdrawal does. Does an admin edit, a payment report or a question? | A guest saving different answers, and a consent withdrawal. Not admin edits, payment reports or questions. |
  | 8 | FR-56 | Does a household marked "seen" come back if it changes again? Are all unanswered households listed from day one? | It comes back when it changes again. Decide whether unanswered households are listed from the start or only near the deadline. |
  | 9 | FR-16, FR-32 | Is the cabin priced per person or per cabin? UJ-2 implies per person ("pays for both"), but the PRD never says so. | Per person for the whole weekend, as an assumption until Q3 is answered. |
  | 10 | FR-26, FR-29, FR-30 | Is consent one choice per answer or one per person? FR-30 deletes "that person's" data. | Stored per person, with who gave it. |

- **Why it matters:** Where the PRD is silent, AI-generated code picks a behaviour, and tests written afterwards tend to copy it. The examiner then sees tests that pass but prove little («tester bare trivielle ting»). Settling the rules first gives meaningful unit tests, and it is itself a clear example of the student steering the AI (criterion 1).
- **Suggested fix:** Add §5.15 *Calculation rules*, with one line per row above, or extend the addendum tables. Add the 0 kr row to the payment-status table. The proposals are suggestions, not decisions: confirm or change each one.

#### SV-3 · The expected-results list is not written, and the seed data can't exercise the rules

- **Criterion:** 3 (also 6)
- **Location:** FR-68, FR-69, SM-2, §8 Q8, UJ-6 step 3
- **Finding:**
  1. **The list doesn't exist yet.** The expected-results list ("fasit") is the strongest test idea in the PRD. Q8 waits for the next supervision to decide where it lives, but the teacher has already answered: «lag en fiktiv gjesteliste med forventede tall som kan brukes i tester og i README».
  2. **The seed covers too few cases.** Beyond the journey people, FR-68 adds only three households: one that has paid, one that hasn't answered, and one guest with an allergy. These cases are not covered:
     - part paid, refund owed, and a red "I have paid";
     - a household marked "Changed";
     - a 0 kr total, and a whole household saying no;
     - allergies without consent, withdrawn consent, and consent registered by the couple;
     - an unanswered question, and a deactivated link.

     "Needs attention" would be almost empty when the examiner logs in.
  3. **No settings are seeded.** FR-68 seeds people but not prices, the deadline, the Vipps and account numbers or the couple's contact details. Without prices there are no totals to check.
  4. **The order isn't stated.** Nothing says the list is worked out before the code it checks.
- **Why it matters:** For A–B in criterion 3, the tests must «dekker sentral logikk» and the QA must be systematic. A list worked out by hand and committed before the code proves that the tests did not come from the AI's own output. UJ-6 also sends the examiner to compare the admin summary with this list.
- **Suggested fix:**
  - Close Q8.
  - Create `expected-results.md` next to the PRD (or in the test folder), and link it from FR-69 and later from the README.
  - Extend FR-68: "at least one household for each rule in §5.15 and each 'Needs attention' item type; fictional settings: prices, a deadline in the future, Vipps and account numbers, contact details".
  - Extend FR-69: "worked out by hand from the seed, committed before the code it checks, and each value names the test that checks it."

#### SV-4 · The journey personas may be real people

- **Criterion:** 7 (also 3: awareness of security and privacy)
- **Location:** UJ-1 to UJ-3; FR-68 ("the people from UJ-1 to UJ-3"); NFR-3
- **Finding:** Rikke told the journeys with family roles and personal details: bestefar Sigmund, 78; onkel Arild, tante Marie and their adult daughters Filippa and Leone; and the friend Synne. The PRD never says these people are invented. FR-68 turns them into seed data with allergies, consent and payment status, in a public repo.
- **Why it matters:** The teacher's first change request was that real names, guest lists and allergies never go into the repo or the test data. If a persona is a real relative, the seed would attach invented allergies and debts to a real name. The examiner would notice that under criterion 7 and in the security check in criterion 3. If they are invented, saying so removes the doubt at no cost.
- **Suggested fix:** Confirm whether the names are real. If any is, replace it with an obviously invented one before the seed data is written, and ask the teacher whether the existing commits need cleaning. Add to NFR-3: "All personas and seed people are fictional; no name belongs to a real guest."

### Medium

#### SV-5 · Journeys promise [2027] features as if they were in v1

- **Criterion:** 1, 2
- **Location:** UJ-2, last paragraph ("can open a history of who changed what and when"); UJ-4 step 4 and UJ-5 step 4 (dated notes); compare FR-40 and FR-62, both [2027]
- **Finding:** The journeys were not updated when FR-40 and FR-62 were deferred. If-time items are marked in the journeys, but [2027] items are not.
- **Why it matters:** In step 7 of the guide, the examiner checks «at dokumentene henger sammen med koden». A journey step that the app can't do looks like a plan that describes another app (warning sign 2), even though the deferral is written down elsewhere.
- **Suggested fix:** Mark these steps the way the If-time ones are marked, for example "*(2027: change history, FR-40)*", or rewrite them to describe v1 (UJ-2: "sees 'last updated by Arild at …'"). Add to §3.1: "Journey steps that depend on [2027] or If-time items are marked."

#### SV-6 · The scope principle, the reasons for [2027], and the scope of the NFRs are missing

- **Criterion:** 2
- **Location:** §3.1, §3.2; NFR-1, NFR-3, NFR-7
- **Finding:**
  1. The principle that decided the [2027] items appears only in the memlog: "v1 = what the examiner and the usability test need; [2027] = what only matters with real guests". The four [2027] FRs have no reason in the PRD.
  2. [2027] is defined for FRs only. Several NFR bullets apply only in production, but they are not marked:
     - NFR-1: the link format is fixed before invitations go out, and a test link is sent through three channels;
     - NFR-3: data processing agreements, and deletion by 31 August 2028;
     - NFR-7: pages load in 3 seconds on 4G.

     A reader can't tell which NFRs v1 must meet.
- **Why it matters:** The examiner looks for «at det som er utelatt eller endret fra proposal, er beskrevet og begrunnet», and reads the PRD, not the memlog. Unmarked production NFRs can be read as unmet promises for v1.
- **Suggested fix:** Open §3.1 with the principle. Put a short reason after each [2027] tag, for example for FR-67: "course data is fictional; deletion matters only for real data". Tag the production-only NFR bullets [2027], or split §6 into v1 and production.

#### SV-7 · The PRD has no way to stay up to date yet

- **Criterion:** 1
- **Location:** frontmatter (`status: draft`); §8; §9; the brief (`status: final`)
- **Finding:**
  1. The PRD has no change log of its own. §9 covers only the changes from the brief.
  2. The brief still says helpers have full access and that payment status has two states (D6). Updating it is a to-do in the memlog but hasn't been done.
  3. §8 says Hardingasete's answers don't block the PRD, but not what they do to v1. Q4 (guests paying Hardingasete directly) could remove the whole payment area in the middle of implementation.
- **Why it matters:** Planning documents that «fremstår som generert én gang og ikke brukt videre» are a D–E sign in criterion 1. The examiner will open the brief, see `final`, and find that it contradicts the PRD.
- **Suggested fix:**
  - Add §10 *Change log* with dated entries. Start with rounds 2 and 3 and the reviewer gate.
  - Before merging `docs/prd`, add a pointer to PRD §9 in the brief's change log.
  - Add to §8: "v1 is built on the current assumptions: guests pay the couple, the cabin is priced per person, and prices and the deadline are fictional. Hardingasete's answers change settings or the 2027 scope, not v1, unless the change log says so."
  - After the gate, set `status: final` and keep `updated:` current.

#### SV-8 · Traceability stops at the stories

- **Criterion:** 1 (also 3)
- **Location:** NFR-9
- **Finding:** NFR-9 makes stories cite FR IDs. Nothing links requirements to commits, pull requests or tests, so the chain the examiner wants to follow (requirement → story → commit → test) breaks after the story.
- **Why it matters:** For A–B in criterion 1, «prosessen kan følges tydelig fra plan til ferdig app», and decisions are «koblet til konkrete endringer». IDs in commit messages and test names let anyone follow the chain with `git log` and a text search.
- **Suggested fix:** Extend NFR-9: "Each story is built on its own branch and merged by pull request. Commit messages and PR titles name the story ID, and each test names the FR it checks. The epics document keeps a table of FR → story → test, updated at the end." Optionally, use one GitHub issue per story, closed by its pull request.

#### SV-9 · No QA approach beyond the expected-results test

- **Criterion:** 3
- **Location:** §2 (SM-1, SM-2); §6 (NFR-4, NFR-5, NFR-9)
- **Finding:** The PRD says what will be measured, but not how quality is checked during the build. It doesn't say:
  - which rules get unit tests and which flows get end-to-end tests;
  - which negative and security tests are needed;
  - how accessibility is checked;
  - whether each pull request is reviewed;
  - where errors found in AI-generated code are written down.

  Some must-have tests already follow from the PRD:
  - opening a link changes nothing (FR-3);
  - the server rejects a helper's attempt to change data (NFR-4);
  - the server rejects a guest's change after the deadline (FR-42);
  - a deactivated link shows only the private message (FR-5);
  - "No" to consent stores no allergy data (FR-28).
- **Why it matters:** The examiner looks for «spor av kodegjennomgang» and «beskrivelser av feil som ble funnet i KI-generert kode og hvordan de ble rettet». That evidence is cheap to plan now and hard to reconstruct in December.
- **Suggested fix:** Add NFR-10 *Quality assurance*, covering:
  - the test levels and the must-have tests above;
  - a manual test plan made from the steps in UJ-1 to UJ-6, with dated results;
  - an accessibility check: an automated scan plus a keyboard walk-through at 320 px;
  - a review of each pull request, with bugs in AI-generated code recorded in the pull request and the session log.

#### SV-10 · The deadline's exact moment, enforcement and testing are undefined

- **Criterion:** 3
- **Location:** FR-41, FR-42, FR-64; UJ-6 step 6
- **Finding:** "After the deadline" doesn't say exactly when that is, for example the end of the day in Norwegian time. FR-42 doesn't say that the server enforces the lock; NFR-4 says that only for helpers. And nothing lets automated tests check behaviour before and after the deadline without editing data.
- **Why it matters:** Locking at the deadline is one of the brief's success criteria for the course, and the examiner is likely to test it (UJ-6 step 6). Being off by a day, and locks that only hide buttons, are typical bugs in AI-generated code.
- **Suggested fix:** FR-41: "The deadline is a date; answers can be changed until 23:59 Norwegian time that day." FR-42: "The server rejects locked changes; hiding the buttons is not enough." Add to NFR-9 or NFR-10: "Tests can set the current time."

#### SV-11 · Validation rules and input limits are not defined

- **Criterion:** 3 (also 4)
- **Location:** FR-22, FR-26 to FR-28, FR-43, FR-49, FR-59
- **Finding:** FR-22 says how errors look, but not what counts as an error. These are not defined:
  - which answers are required in each step;
  - what happens when allergies are entered but consent is "No" or left unanswered: an error, or the allergies are dropped with a message;
  - the maximum length of the allergy note, questions and names;
  - which amounts the couple may register: whole positive kroner only? Can a refund be larger than what was received?
  - what removing a household with registered payments does.
- **Why it matters:** The examiner will «prøve feil input og uventet bruk». Without rules, AI-generated code handles each form differently, and there is nothing to test against.
- **Suggested fix:** Add a short validation table to §5.3 and §5.11 (field, required or not, limit, error message). Add one line: "Text from guests is always shown as plain text, never as HTML."

#### SV-12 · The usability test has no protocol

- **Criterion:** 4 (also 3)
- **Location:** SM-3, SM-4; §7 *Dates*
- **Finding:** SM-3 and SM-4 say what is measured, but not:
  - who takes part, which tasks they get, and on which device;
  - how the results are recorded, and when the fixes happen.

  In SM-4, "the couple" includes Rikke, who built the admin area. Testing on a phone also needs the phone to reach the app running on the PC; otherwise the test runs in a narrow PC window.
- **Why it matters:** A documented usability test, with findings and fixes, is the strongest «spor av designarbeid» and shows quality assurance beyond the code. Without a protocol, the result is an anecdote.
- **Suggested fix:** Add a short protocol to §2 or the addendum:
  - participants: at least one older relative for SM-3, and Valdemar or a helper for SM-4;
  - 3–5 written tasks, for example "How many Sunday breakfasts?" and "Who needs gluten-free food?";
  - the device and how it reaches the app;
  - what is recorded: time, where they hesitate, and errors;
  - where the results go: a dated test report in the repo;
  - time for fixes before feature freeze.

#### SV-13 · Empty states and admin confirmations are missing

- **Criterion:** 4
- **Location:** FR-44, FR-51, FR-54 to FR-58; NFR-6
- **Finding:** Errors and the guest receipt are well covered, but empty states are not:
  - a summary with no answers;
  - an empty "Needs attention" and no questions;
  - an empty allergy list;
  - a search with no match.

  There is also no feedback after admin actions, such as registering a payment or marking an item as handled.
- **Why it matters:** The guide lists «forståelige tilbakemeldinger, feilmeldinger og tomtilstander», and AGENTS.md repeats it. Some admin lists may be empty when the examiner runs the app.
- **Suggested fix:** Add FR-70: "Every list and count has a friendly empty state that says what will appear there. Every save in the admin area shows a short confirmation."

#### SV-14 · Details the README will depend on

- **Criterion:** 6
- **Location:** FR-68; NFR-8; UJ-6 steps 2 and 3; SM-5
- **Finding:**
  1. UJ-6 promises a test link per guest in the README, but links are random (NFR-4) and may be stored hashed (D14). Nothing says the seeded links stay the same, so running the seed again could break every link in the README.
  2. There is no reset. After the examiner tries wrong input, the data no longer matches the expected-results list.
  3. The tests and manual use could share one database.
  4. Nothing requires exact versions in the README, a screenshot, or commands that work in both PowerShell and bash (for example copying `.env.example`).
  5. The command that creates admin accounts (FR-47) must be in the README, next to the seeded logins.
- **Why it matters:** For A–B in criterion 6, «sensor får appen til å kjøre ved å følge README uten avvik». Test links that don't work is the most likely way for this app to fail that check.
- **Suggested fix:**
  - Extend FR-68: "Seeded test links are fixed, fictional values that are the same on every run. Running the seed command again resets the database to the seed state."
  - Extend NFR-8: "Tests use their own database. The app starts with the defaults in `.env.example`, or the README gives the copy command for both shells. The README names exact versions and shows a screenshot made with fictional data."
  - In SM-5, have someone other than Rikke do the trial run, on another operating system if possible, and log the result.

#### SV-15 · This session's prompts and AI corrections are not in the session log yet

- **Criterion:** 1
- **Location:** PRD header ("Every decision … is logged in `.memlog.md`"); the last entries in `.memlog.md`; `.logs/rikke/`
- **Finding:** The memlog records decisions as short paraphrases in English, without Rikke's own words or links to commits. The session log for this session isn't in `.logs/rikke/` yet. It should quote the prompts word for word and include the six examples of steering the AI that the memlog lists. The PRD doesn't link to it either.
- **Why it matters:** Criterion 1 asks for «lagrede prompts», and for corrections that are «koblet til konkrete endringer». This session has some of the project's best examples:
  - Rikke rejected Claude's proposal to store names only;
  - the one-link-per-household assumption was corrected;
  - D6 was replaced;
  - helpers were made read-only;
  - Claude revised its own proposal for UJ-3.
- **Suggested fix:** Before merging `docs/prd`, write the session log. Quote the key prompts, for example Rikke's telling of UJ-1 and her rejection of name-only storage, and link `ae1b330`, `a9b95e8` and `7384511`. Add the examples to `.logs/rikke/README.md`, and link the log from the PRD header next to `.memlog.md`.

#### SV-16 · The couple's override could become a second RSVP form

- **Criterion:** 5 (also 2)
- **Location:** FR-63, FR-31; UJ-3 step 5
- **Finding:** FR-63 lets the couple fill in or change any answer, also after the deadline, and FR-31 adds consent given by phone. The PRD doesn't say that this goes through the same form and rules as the guest flow. An AI building an admin page from its own story is likely to build a second form with its own copy of the rules.
- **Why it matters:** Two copies of the riskiest logic double the work (criterion 2) and create the duplication that criterion 5 marks down («lite duplisering»). The copies will drift apart and give different totals.
- **Suggested fix:** FR-63: "The couple uses the same step-by-step form and rules as guests, opened from the admin area, with two differences: it works after the deadline, and allergy consent can be registered as given by phone or message (FR-31)."

### Low

#### SV-17 · Some measures are too vague to test

- **Criterion:** 3
- **Location:** FR-7, FR-20, SM-1, NFR-4, NFR-7
- **Finding and fix:**
  - **FR-7** "without scrolling on a phone": name a screen size, for example 360 × 740.
  - **SM-1** "on a phone": say whether this means a real phone reaching the PC over the local network, or the browser's phone view.
  - **NFR-4**: give numbers for the session timeout and for slowing down repeated attempts. The research suggests 15–30 minutes and about 5 attempts a minute.
  - **NFR-7**: this can't be measured on a local app. Mark it [2027], or use a mobile performance audit in the browser instead.
  - **FR-20**: browsers on iPhones don't reliably warn when a tab is closed. Say "leaving through the site's own links asks for confirmation; closing the browser is best effort".

#### SV-18 · Two UX contradictions

- **Criterion:** 4
- **Location:** FR-7, FR-24, FR-37; NFR-6 compared with FR-48
- **Finding:**
  - After a household has answered, does the link open the invitation with "See or change answer" (FR-37), or a status page (FR-24: "always opens its status")?
  - NFR-6 says a PC shows the phone layout, but FR-48 lets the admin overview be designed for a PC.
- **Suggested fix:**
  - FR-24: "After answering, the invitation page shows a status panel (answers, total, payment, deadline) above the cards."
  - NFR-6: "Applies to guest pages; admin pages may use a wider layout."

#### SV-19 · No Norwegian glossary for the interface

- **Criterion:** 4 (also 3)
- **Location:** FR-12, FR-23, FR-35, FR-37, FR-43, FR-56; NFR-6
- **Finding:** The site is in Norwegian, but its labels exist only as English translations: "I am", "See or change answer", "Ask us", "I have paid", "Needs attention" and "Changed". Different stories will translate them differently.
- **Suggested fix:** Add a glossary to the addendum that maps each English term to Rikke's Norwegian label, for use in UX, stories and tests. Tests that find buttons by their label then stay stable.

#### SV-20 · Three requirements have no source

- **Criterion:** 1
- **Location:** FR-47, FR-52, FR-67
- **Finding:** All three came from decisions in this session (see the memlog), but have no source tag.
- **Suggested fix:** Add a source, for example [PRD round 2] for FR-47. Better still, number the decisions from this session in the memlog (P-1, P-2, …) so FRs can cite them the same way they cite the C and D decisions.

#### SV-21 · A stray table row in the addendum

- **Criterion:** 7
- **Location:** last line of `addendum.md`, under *Test data note*
- **Finding:** The row "Saving an unfinished answer to continue later | Moved to If time …" sits outside the *Rejected alternatives* table and shows as loose text.
- **Suggested fix:** Move it into the *Rejected alternatives* table.

#### SV-22 · The extract files are unexplained

- **Criterion:** 7
- **Location:** `extract-brief.md` and `extract-pre-prd.md` in this folder
- **Finding:** About 400 lines of AI summaries sit next to the PRD with no note on what they are. Only the commit message of `ae1b330` explains them.
- **Suggested fix:** Add one line to the PRD header listing the files in this folder and what each is for, for example "extract-*.md: AI summaries of the inputs, kept as process evidence". Or remove them if they add nothing.

#### SV-23 · The proposal isn't referenced, and two of the brief's success criteria were dropped from §2

- **Criterion:** 1, 2
- **Location:** `inputs` in the frontmatter; §2
- **Finding:** The examiner starts from «gruppens godkjente proposal». The PRD's inputs list the brief, the feedback and the research, but not the proposal, if it is a separate document. In addition, two of the brief's success criteria for the course are missing from §2 and appear only in UJ-6:
  - answers lock at the deadline while the couple can still override them;
  - a guest question reaches the admin area, by email or in the console.
- **Suggested fix:** Add the proposal to `inputs`, or state that the brief serves as the proposal. Add SM rows for the lock and override and for questions, checked by automated tests.

## Appendix A: Suggested priority within v1

This is a proposal for Rikke to accept or change. It follows the teacher's core, «personlig lenke, husstands-RSVP med pris, låsing ved frist, admin-oversikt med tellinger og overstyring», and puts what the usability test needs first.

**Tier 1: the usability-test build.** Works end to end by Friday 27 November, ready for the test in the first week of December.

- **Start:**
  - FR-68 and FR-69, with the expected-results list written first;
  - the seed creates the test accounts (FR-47);
  - one command to run the app and one to run the tests (NFR-8, NFR-9);
  - a first draft of the README steps.
- **Guest pages:**
  - FR-1 to FR-18, with short draft text on the information pages;
  - FR-21 to FR-28, FR-32 to FR-34 and FR-41.
- **Admin area:** FR-46 (the couple's login), FR-54, FR-55, FR-57 (a simple table) and FR-58.

**Tier 2: the complete course version.** Done by feature freeze on Thursday 10 December, in this order:

1. The rest of the teacher's core: FR-37 to FR-39, FR-42, FR-63 (the same form, see SV-16) and FR-64.
2. Questions to the couple: FR-43 to FR-45.
3. Payments: FR-35, FR-36 and FR-59 to FR-61.
4. Admin tasks: FR-56, FR-49, FR-51, and the helper role in FR-46.
5. Privacy and polish: FR-19, FR-20, FR-29, FR-30, FR-66, and the full text for FR-9 and FR-10.

**Tier 3: cut first.** Anything here that isn't done by 10 December moves to [2027], with the reason in the change log:

- **FR-50, moving a guest to another household.** Removing and re-adding the guest works, and moving answers and payments has many edge cases.
- **FR-53, giving a guest a new link.** This only matters when a real link is lost. If it is cut, mark UJ-3 step 3.
- **FR-31, consent the couple registers after a phone call.** This only matters with real guests. If it is cut, mark UJ-3 step 5.
- **FR-65, the warning when prices change.** v1 uses fixed test prices.
- **FR-48, beyond basic responsive admin pages.**
- **Slowing down wrong guest links (NFR-4),** if the chosen stack doesn't provide it.

Build Tier 1 in this order:

1. The rules and their unit tests, from the expected-results list.
2. The guest flow when everyone comes all weekend.
3. The exceptions: someone not coming, or coming only some days.
4. Allergies and consent.
5. The check page, the receipt and the payment information.
6. The admin summary, where each count opens the people behind it.
7. A dry run of the usability test.

## Appendix B: Riskiest parts for a solo beginner

| Rank | Part | Requirements | Why it is risky | How the PRD can lower the risk |
|---|---|---|---|---|
| 1 | The household RSVP form | FR-12 to FR-24, FR-37, FR-38, FR-63 | The most state and branching: per person, per day and per meal, plus editing, a check page with "Change" links, an error summary, and use by the couple | Settle the rules (SV-2), use one form for guests and the couple (SV-16), and build the "everyone, all weekend" path first |
| 2 | Money | FR-32 to FR-36, FR-59 to FR-61 | Edge cases (0 kr, refunds, "matching" reports) decide which households the couple sees in red | Define the rules (SV-2), and keep totals and statuses as small calculations with unit tests (NFR-2) |
| 3 | "Needs attention" | FR-56, addendum table | Five item types, each with its own way of leaving the list and perhaps coming back | Define when items come back (SV-2), and build the list after the data it reads from |
| 4 | Consent | FR-26 to FR-31 | Consent per person, text versions, withdrawal after the deadline, and consent the couple registers | Tier 1: the consent question and storing it. Tier 2: the record and withdrawal. Tier 3: consent given by phone |
| 5 | Admin security | FR-46, NFR-4 | Password hashing, sessions that expire, protection against forged forms, slowing down repeated attempts, and role checks on the server | Ask the architecture for a stack with these built in, and test helper and deadline enforcement (SV-9) |
| 6 | Changing the guest list | FR-49, FR-50, FR-53 | Moving or removing people who have answers and payments | Define what happens, or cut FR-50 and FR-53 (Tier 3) |
| 7 | Accessibility | NFR-5 | Own colour palette, a step-by-step form, and moving focus to the error summary | Check contrast when choosing colours, and put an automated scan and a keyboard walk-through in the test plan |

## Appendix C: Warning signs in chapter 5

| Warning sign | Risk from this PRD | Covered by |
|---|---|---|
| Almost all code in one or a few commits right before the deadline | Medium: a large v1 and a late usability test push work into the last week | SV-1, SV-8 |
| Planning documents describe another app, or were written afterwards | Medium to high: the PRD promises more than is likely to be delivered, the journeys include [2027] features, and the brief contradicts the PRD | SV-1, SV-5, SV-7 |
| README is an unchanged template, or its commands don't work | Low: UJ-6 and NFR-8 are strong. The risk is test links that change | SV-14 |
| API keys, passwords or `.env` files committed | Low: NFR-4, NFR-8 and `.gitignore` cover it | – |
| `node_modules`, `venv`, build folders or large binaries in the repo | Low: `.gitignore` covers it | – |
| Tests fail or only test trivial things | Medium: the expected-results test is meaningful, but undefined rules invite tests that copy the code | SV-2, SV-3, SV-9 |
| Dead code, duplicate files, or leftovers from discarded AI attempts | Low to medium: a second RSVP form for the couple | SV-16 |
| Documentation of AI use is general and not linked to changes | Low to medium: the memlog is good, and the session log is still to come | SV-8, SV-15 |
