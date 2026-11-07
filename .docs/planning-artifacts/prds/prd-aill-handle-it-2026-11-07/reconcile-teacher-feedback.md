# Reconciliation: teacher feedback on the brief vs the PRD

| | |
|---|---|
| **Input** | `../../briefs/brief-aill-handle-it-2026-09-23/tilbakemelding-product-brief.md` (course teacher, 2026-10-06, on brief commit `ee25e52`, in Norwegian) |
| **Checked against** | `prd.md` (draft, 2026-11-07), `addendum.md`, `.memlog.md` |
| **Context** | `docs/sensorveiledning/sensorveiledning-del1.md`, plus the brief, the brief addendum and the brief memlog, which record how the feedback was first handled on 2026-10-23 |
| **Date** | 2026-11-07 |

**Location keys.** `T L n` is line n of the feedback file. `memlog L n` is line n of this workspace's `.memlog.md`. `brief memlog L n` is line n of the brief's `.memlog.md`. PRD locations are given as section numbers and requirement IDs.

**Result.** There are 15 gaps (1 high, 4 medium, 10 low) and 2 contradictions without a record.

The PRD carries every main change the teacher asked for:
- fictional data only;
- the course v1 kept separate from the real wedding;
- a local run with seed data, a test admin and email that works without a key;
- optional email;
- production work kept out of the course success criteria.

Two things are weak:
- **Scope and time.** This was the teacher's first risk. It has grown since the feedback, but the PRD text no longer mentions it.
- **The local test setup.** A few details there decide whether the examiner can follow the README without problems.

## Gaps

### G1 (high) The time and scope risk is not in the PRD, and v1 has no priority order

- **Feedback:**
  - "Tid og omfang" is rated **Risiko**: one developer, and the plan is realistic only "hvis animasjon og innholdssider holdes enkle" (T L59).
  - "«In» er stor for én person, og alt står som like viktig. Prioriter innenfor «In»" (T L91).
  - "Prioriter kjernen, så resten kan kuttes uten at appen blir halv" (T L101; also T L111).
  - Get the guest flow and admin counts right and tested before the envelope animation, gift list, speeches and English get much time (T L51).
  - The suggested core is the personal link, household RSVP with price, lock at the deadline, and the admin overview with counts and override (T L73).
- **PRD:**
  - **v1 is flat.** §3.1 puts every FR in v1 except those marked [2027] or listed under If time. That is 65 FRs plus NFR-1 to NFR-9 (memlog L72), all with the same weight.
  - **The risk and the principle are only in the memlog.** Memlog L72 and L75 record that the time risk was raised and accept a principle: "v1 = what the examiner and usability test need". Neither the risk nor the principle is in the PRD text.
  - **The principle cut almost nothing.** It deferred only FR-40, FR-52, FR-62 and FR-67, and all four were added during the PRD session itself. Nothing from the brief's Must list was cut.
  - **v1 grew after the warning:**
    - §9 "New in v1" lists six new feature groups;
    - the amount-based payment model (FR-59, FR-60);
    - "I have paid" (FR-35, FR-61);
    - a second admin role that the server must enforce (FR-46, NFR-4);
    - link deactivation (FR-53).
  - **Two safeguards from the brief are gone:**
    - the brief's "Kept simple" for information pages, which was the teacher's condition for the plan to be realistic;
    - the rule that If-time work is "built after the core and cut first" (brief memlog L58).
  - **Little time is left.** There are about 3.5 weeks to the usability test and 5.5 weeks to delivery. No UX, architecture or story documents exist yet.
- **Suggested fix:** Add a short "Delivery order" subsection to §3. It needs no time plan; brief memlog L69 deliberately left one out.
  1. State the teacher's risk and the principle from memlog L75.
  2. Mark a **core** inside v1 that matches T L73 and T L19 plus what the examiner needs. A candidate:
     - links: FR-1 to FR-6;
     - household RSVP with price and payment details: FR-12 to FR-18, FR-21, FR-23, FR-24, FR-32 to FR-34;
     - changing answers, the lock and admin override: FR-37, FR-38, FR-41, FR-42, FR-63;
     - allergies with consent: FR-25 to FR-30;
     - admin login, guest list and overview with counts: FR-46, FR-47, FR-49, FR-54, FR-57;
     - basic payment tracking: FR-59, FR-60;
     - questions: FR-43 to FR-45;
     - seed data, expected results and local run: FR-68, FR-69, NFR-2, NFR-8.
  3. Name the v1 items to **cut first** if the core is not built and tested by a checkpoint, for example the usability test. Candidates:
     - FR-31;
     - the tailored messages in FR-36;
     - FR-48, FR-53, FR-55;
     - FR-56, reduced to a not-answered list;
     - FR-61, FR-65.
  4. Say that If-time work starts only after the core passes its tests, and that information pages stay static text (D12).
  5. Record any cut in §9. Sensorveiledning criterion 2 asks for what was left out to be described and explained.

### G2 (medium) No rules for moving or removing a guest

- **Feedback:** "Husstand–gjest og flytting mellom husstander krever nøye modellering" (T L41).
- **PRD:** FR-50 is one sentence: "The couple can move a guest to another household". FR-49 lets the couple remove guests. Nothing says what happens to:
  - the guest's answers, allergy consent and link;
  - the totals and payment statuses of the two households (FR-60 works per household);
  - the "Changed" marker;
  - "last updated by".

  The addendum's notes for architecture do not mention it either.
- **Suggested fix:**
  - Add the rules to FR-50, and add removal to FR-49. For example:
    - the guest's answers, consent and link follow the guest;
    - both households' totals are recalculated;
    - registered payments stay with the household that paid, so the old household may show "refund owed" and the new one "part paid";
    - both households are marked "Changed".
  - Add a moved guest to the seed data and the expected results (FR-68, FR-69).
  - Note the data-model need in the addendum's architecture section.

### G3 (medium) Seed data and expected results leave out settings and payments

- **Feedback:**
  - Ready-made test guests and households (T L26).
  - "Lag en fast testliste med fasit" (T L62).
  - Price, counts and lock can be tested against a fictional list with expected results (T L102, T L111).
  - The admin counts include payment: "tellinger for oppmøte, måltider, senger, allergier og betaling" (T L19).
  - Payment information must never be in the repo or in test data (T L24).
- **PRD:**
  - **Settings are not seeded.** FR-68 seeds guests, households, guest contact details, test links and two test users. It does not seed the settings that the totals and the payment page depend on: prices, the deadline, the couple's contact details, and the Vipps and account numbers (FR-64). Without fixed fictional prices, the totals in FR-69 cannot be worked out by hand in advance.
  - **A decision was lost.** Memlog L41 decided that the course version and seed data use fictional numbers for the couple's contact details. That decision is not in the PRD.
  - **Payments are not counted.** FR-54's summary has no payment count, although the brief's course success criterion counted payments.
  - **Payment cases are not seeded.** The seed has "one that has paid". It has no part-paid household, no refund owed, no "I have paid" without a matching payment, no "Changed" household and no open question. So the examiner sees an empty "Needs attention" list (FR-56), and the tests cannot check the payment statuses (FR-60, FR-61).
- **Suggested fix:**
  - Extend FR-68 with fixed settings that are clearly fictional, in the style of the addendum's Test data note: prices, a deadline in the future, the couple's contact details, and Vipps and account numbers.
  - Also seed one case for each payment status, the mismatch, a "Changed" household and an open question.
  - Extend FR-69 so the expected results include each household's payment status and the "Needs attention" items.
  - Add a payment line (paid, part paid, not paid, refund owed) to FR-54's summary, or say why it is left out.

### G4 (medium) The README cannot list test links that are random

- **Feedback:** Seed data "med fiktive gjester og testlenker" (T L64, T L105).
- **PRD:**
  - UJ-6 step 3 says "The README lists a test link per guest", and FR-68 gives each guest a test link.
  - FR-1 and NFR-4 require a long random code with at least 128 bits of randomness.
  - D14 (whether codes are stored hashed or plain) is still open.
  - So two things can break the README:
    - if the seed makes new random codes on every run, the README cannot list them in advance;
    - if codes are stored hashed, the admin area cannot show them either (addendum, D14).
- **Suggested fix:**
  - State in FR-68 how the examiner gets the links. Either the seed uses fixed, documented codes for the fictional guests (local only; see G5), or the seed command prints every link.
  - Pass this on to D14 as a constraint in the addendum.

### G5 (medium) Nothing stops the test accounts from reaching production

- **Feedback:** The repo is public (T L24, T L106), and the examiner needs a test admin (T L26).
- **PRD:**
  - The brief's answer to this feedback said the test admin "is fictional, exists only in local seed data" (brief, Data and Privacy).
  - FR-68 keeps the test couple admin and the test helper but drops "exists only in local seed data".
  - No NFR stops the seed command from running against the production database.
  - Their logins, and possibly fixed test links (G4), will be in a public README. In production, that would give anyone couple access to allergy data.
- **Suggested fix:** Add to FR-68 or NFR-4:
  - test users and test links exist only in local seed data;
  - the seed command refuses to run with production settings;
  - production admin accounts are made only with FR-47's command.

### G6 (low) The named automated tests leave out the lock and household answers

- **Feedback:** "Pris, tellinger, låsing ved frist og husstandssvar er tydelige regler" (T L63). "Pris, tellinger og låsing kan testes automatisk" (T L102).
- **PRD:** The only automated tests the PRD names check counts and totals against the expected results (NFR-2, FR-69, UJ-6 step 8). Three rules are tested only by hand in UJ-6, or not at all:
  - the lock: the guest is blocked after the deadline and the admin is not (FR-42, FR-63);
  - household answers: the last save applies, and who answered is recorded (FR-38, FR-12);
  - the server stops helpers from changing data (NFR-4).

  SM-1's "automated tests" have no stated scope.
- **Suggested fix:** Add one line to NFR-9 or §2 that names these rules as targets for automated tests.

### G7 (low) NFR-5 has no font-size target

- **Feedback:** "Husk tilgjengelighet (kontrast, skriftstørrelse, tastaturnavigasjon)" (T L103).
- **PRD:** NFR-5 covers contrast, keyboard, focus, zoom, screen width and touch targets, but not text size. The brief's "large, readable text" was dropped.
- **Suggested fix:** Add a minimum body text size for guest pages to NFR-5. The exact value can be set in bmad-ux.

### G8 (low) The expected results are not linked to the README, and Q8 is half answered

- **Feedback:** Make a fictional guest list with expected numbers "som kan brukes i tester og i README" (T L111).
- **PRD:**
  - FR-69 says the list is "documented"; UJ-6 step 5 says "in the documentation".
  - Q8 (§8) asks the teacher whether the list must be in the PRD or only in the tests. The feedback has already answered that: in the tests and the README.
- **Suggested fix:**
  - Change FR-69 to "documented in, or linked from, the README".
  - Narrow Q8 to "Must it also be in the PRD?"

### G9 (low) The NFRs do not say whether they apply to v1 or to production

- **Feedback:** "Gjør det tydelig hva som er v1 for emnet" (T L25).
- **PRD:** FRs carry a [2027] tag, but NFRs do not. Some NFR-1 bullets say "In production" and others do not. These can only be checked in production:
  - NFR-1: the link format is fixed, and a link is test-sent by SMS, Messenger and email on Android and iPhone;
  - NFR-3 bullets 4–5: EU/EEA hosting, data processing agreements and the deletion date;
  - NFR-7: pages load in 3 seconds on 4G.
- **Suggested fix:** Tag the production-only NFR bullets [2027], as the FRs are.

### G10 (low) Deletion does not cover backups or email copies

- **Feedback:** Describe how data is deleted after the wedding (T L47, T L110).
- **PRD:** NFR-3 sets 31 August 2028, and FR-67 (delete all, deliberately deferred to [2027]) gives the tool. Nothing covers:
  - the daily backups (NFR-1);
  - guest questions emailed to the couple (FR-45);
  - the allergy list the couple emails to Hardingasete (UJ-4).
- **Suggested fix:** Add one NFR-3 bullet: backups expire and these emails are deleted by the same date. The privacy page (FR-66) says so.

### G11 (low) Nothing says the local database file stays out of Git

- **Feedback:** The repo row is rated **Endre**: plan where secrets, test data and documentation live, and never commit real guest data (T L106).
- **PRD:**
  - Keys and fictional data are covered (NFR-3, NFR-4, NFR-9).
  - With SQLite recommended (addendum, D15), the database file will sit in the project folder.
  - Nothing says the database file, its backups or exports stay out of Git. In the course this would be a stray file under criterion 7. In 2027 it would be real health data in a public repo.
- **Suggested fix:** Add to the addendum's architecture notes that database files, backups and exports are ignored by Git.

### G12 (low) Text kept in the code can put real names in the public repo

- **Feedback:** Real guest lists and names must never be in the repo (T L24).
- **PRD:** D12 keeps the information-page text in the code (the note after FR-65). From 2027 the real texts will be in the public repo. Nothing says they must leave out the names of guests or helpers (such as the toastmaster) or private phone numbers.
- **Suggested fix:** Add to NFR-3: information texts in the code name no guests or helpers and contain no contact details; contact details come from settings (FR-64).

### G13 (low) The usability test does not say how a phone reaches the local app

- **Feedback:** Plan when the usability test is done (T L90). The course version runs locally (T L64).
- **PRD:**
  - SM-3 sets the time (first week of December 2026) and requires fictional data.
  - It drops the brief's "on Rikke's phone or PC" (brief, Success Criteria; brief memlog L72), while SM-1 says "on a phone".
  - A phone can only reach a locally running app if the app accepts connections from the home network. Nothing in the PRD or addendum asks for that.
- **Suggested fix:** State the device in SM-3. If a phone is used, note in the addendum's architecture section that the local server must be reachable on the home network.

### G14 (low) The brief's change log does not yet show the PRD changes

- **Feedback:** Update the brief in the repo when things change, "slik at historikken viser hvordan planen utviklet seg" (T L114).
- **PRD:** §9 lists the changes, and memlog L54 has a to-do to update the brief's change log at Finalize. It has not been done yet; the brief was last updated 2026-11-06.
- **Suggested fix:** Do it at Finalize. Include:
  - helpers are read-only;
  - payments are registered as amounts, with four statuses;
  - "I have paid" is in v1;
  - guests' phone and email are stored;
  - email to the couple on change is dropped;
  - the gift list is decided.

### G15 (low) Some requirements have no source, or the wrong one

- **Feedback:** Requirements must be traceable from the brief to the code (T L100).
- **PRD:** FR-47, FR-52 and FR-67 have no source. FR-65 cites UJ-6, which contains no price change; the decision is in memlog L63.
- **Suggested fix:** Add the sources, for example the memlog decision or "Rikke, 2026-11-07".

## Contradictions without a record

### X1 Course success criteria the teacher praised were cut, with no note in §9

- **Feedback:** "Kriteriene for emneleveransen er gode og testbare" (T L90). "Kom i gang med PRD og prompt-logg nå" (T L100).
- **PRD:** Three of the brief's six course success criteria are no longer in §2:
  - answers lock at the deadline, and the admin can still override them;
  - a guest question shows up in admin, is emailed when a key is set, and is otherwise written to the console;
  - "A complete prompt log backs the reflection report".

  The first two survive as FR-42, FR-63, FR-44 and FR-45 and as UJ-6 steps 6–7 (see G6 for testing them). The prompt log has disappeared from the PRD altogether, although the sensorveiledning gives process 30 %. Neither §9 nor the memlog records the change.
- **Suggested record:** Either:
  - restore them as SM rows; or
  - add a §9 row saying that UJ-6 and the FR tests cover the first two, and that the prompt log and session logs (`.logs/`, sesjonslogg) are kept outside the PRD as process evidence.

### X2 FR-5 hides the date and place, but the public repo shows them

- **Feedback link:** The repo is public (T L24, T L106).
- **PRD:**
  - FR-5 shows visitors without a valid link no names, phone numbers, date or place (memlog L85).
  - The date, the venue and the whole programme are already in the public repo (PRD §1, the brief).
  - D12 puts all information-page text in the code.
  - Nothing records whether this is acceptable.
- **Suggested record:** Either:
  - note that event details are not secret, because FR-5 protects people rather than the event; or
  - plan to keep the real 2027 texts out of Git.

## Addressed / deliberate (accounted for)

### Addressed in the PRD

- **Fictional data only** (T L24, L106, L110): only fictional data in the repo, tests, test data, screenshots, the usability test and AI tools; real data only in production → NFR-3; §1 "Two deliveries"; addendum Test data note (`example.com`, phone numbers that can't be real).
- **Course v1 separate from the real wedding** (T L25) → §1 "Two deliveries"; §2 split; §3.1 and §3.2; [2027] tags.
- **Real-wedding criteria as long-term goals** (T L25, L90) → §2 SM-6 to SM-10, "not measured in the course".
- **Production out of the course criteria** (T L75): "production-ready", running until 2028 and hosting → no course metric needs them; §3.2 lists the production work; §3.4 puts "Hosting for the course" out of scope.
- **Local run** (T L26, L64, L105, L112): test guests and households, a test admin and email without a key → UJ-6; FR-68 (plus a test helper); FR-45; NFR-8.
- **Optional email** (T L44, L74): questions always stored and shown in admin, emailed only with a key → FR-44, FR-45, NFR-8, UJ-6 step 7.
- **Course version needs no email service or hosting** (T L65) → NFR-8 (no accounts, keys or separate database server); §3.4.
- **Examiner runs the app in reasonable time** (T L64; sensorveiledning §3) → SM-5: 15–20 minutes, with a trial run on a clean machine (memlog L78).
- **A fixed fictional test list with expected results, checked by tests** (T L62, L63, L102) → FR-69, SM-2, NFR-2. Coverage gaps: G3, G8.
- **Links that are hard to guess** (T L42) → FR-1; NFR-4 (at least 128 bits; repeated wrong-link attempts slowed down).
- **Two household members answering at once** (T L45): "last save applies, or show who answered" → FR-38 does both; UJ-2 step 5.
- **Health data: access, deletion and storage** (T L47, L110) → access in FR-26, FR-46 and NFR-4; deletion date and EU/EEA storage in NFR-3; privacy page in FR-66. Gap: G10.
- **Consent** (T L110) → FR-25 to FR-31.
- **Keys in `.env` outside Git, with an example file without real values** (T L106) → NFR-4, NFR-9, UJ-6 step 2.
- **A simple full-stack app with one database, justified in the architecture** (T L104) → §7 "Course requirement"; D15; addendum (SQLite for clone-and-run).
- **Domain rules** (T L40): price per guest, counts, beds, lock and override → FR-32, FR-33, FR-54, FR-16, FR-42, FR-63, NFR-2.
- **Accessibility: contrast and keyboard** (T L103) → NFR-5. Font size: G7.
- **Older guests as a design concern** (T L89, L103) → UJ-1, NFR-5, NFR-6, SM-3.
- **Guests who don't read Norwegian** (T L89) → §1 "Who it is for"; an English version is If time (§3.3). The brief's fallback ("ask the couple directly") is not restated, but FR-43 covers it in practice.
- **When the usability test happens** (T L90) → SM-3 and §7: first week of December 2026, with fictional data. Device: G13.
- **PRD and architecture next, with local run and dev-mode email as explicit requirements** (T L100, L112) → this PRD (2026-11-07); NFR-8, FR-45, FR-68; architecture questions handed on in the addendum.
- **The exclusions the teacher praised are kept** (T L20, L43): no online payment, no sending from the site, no guest accounts, no AI → §3.4; §7 "No AI in the site".
- **Vipps is payment information, not an integration** (T L44) → FR-34; §3.4 (no Vipps payment requests).

### Deliberate, accounted for

- **Core and second step renamed** (T L73): they are now v1 and If time, and all four second-step items (envelope animation, speech sign-ups, gift list, link tracking) are If time → brief memlog L62; PRD §3.3.
- **Envelope animation out of the core** (T L51, L59, L61): only the static invitation look is Must → §3.3; addendum "Invitation reveal"; memlog L15; brief memlog L63.
- **No time plan** → brief memlog L69 (the user doesn't know exactly when she will work). G1's fix asks for an order, not a time plan.
- **Scope principle** "v1 = what the examiner and usability test need", with FR-40, FR-52, FR-62 and FR-67 deferred to 2027 → memlog L72 and L75; §3.2. The principle itself is not in the PRD text (G1).
- **Print or export view for Hardingasete** (T L46) → a print page is If time (§3.3; memlog L46). There is no CSV export, which the teacher called unnecessary.
- **Last save wins, with no conflict detection** (T L45) → §3.4 "Conflicts" (C5).
- **Whole-weekend cabin instead of cabin nights** (T L40): both nights are paid → FR-16; D1.
- **Consent model differs from the checkbox the teacher read** (T L47) → C1; Q8 asks the teacher about it.
- **Gift list and email cost were open** (T L60) → the gift list is decided (§9; memlog L70); the production email provider and its cost are §3.2 and D16 (2027).
- **Helpers read-only** (T L42 assessed two roles; this adds a third) → §9; memlog L51. Adds v1 work: G1.
- **Payments as amounts with four statuses, and "I have paid" in v1** → §9; addendum Rejected alternatives; memlog L19 and L55. Adds v1 work: G1.
- **New v1 features** ("Needs attention", counts that open the people behind them, the "Changed" marker, admin settings with a price warning, the privacy page, consent the couple records by phone) → §9 "New in v1". Adds v1 work: G1.
- **Guests' phone and email are stored** (privacy, T L47): Rikke rejected Claude's proposal to store names only → §9; addendum Rejected alternatives; memlog L84; the privacy page explains it (FR-66).
- **The couple's own names appear in the PRD and on the site** (T L24 is about guest names) → memlog L21.
- **Information text lives in the code, not editable in admin** → D12; the note after FR-65; memlog L69. Consequences: G12, X2.
- **The delete-all tool is deferred to 2027** → FR-67 [2027]; memlog L75.
- **Usability test in the first week of December, accepting less time to fix what it finds** → brief memlog L60.
- **Less to build:**
  - email to the couple when an answer changes is dropped;
  - there is no self-service link recovery;
  - there is no Excel import;
  - there is no "who's coming" list for guests.

  → §9; §3.4; addendum Rejected alternatives; memlog L29, L43, L64, L78.
- **Saving an unfinished answer is If time** → §3.3; memlog L17. *Note:* the addendum row that records this (line 88) sits after the Test data note instead of inside the Rejected alternatives table. With no blank line before it, it displays as part of the Test data paragraph.

## Risks the teacher raised and how the PRD now stands on them

| Risk (teacher's rating, location) | Where the PRD stands | Status |
|---|---|---|
| Time and scope: **Risiko** (T L59, L91, L101) | The teacher rated it with about 12 weeks left and no PRD. Now there are about 3.5 weeks to the usability test and 5.5 to delivery, and UX, architecture and stories do not exist yet. v1 has 65 FRs and grew after the warning. The risk and the scope principle are only in the memlog. | **Higher than when raised** (G1) |
| Examiner can run the app: **Risiko** (T L64, L105) | UJ-6, FR-68, FR-69, FR-45, NFR-8 and the SM-5 trial run cover it. Still open: how test links get into the README (G4), seeded settings (G3), and the technology stack (D15). | Mostly mitigated |
| Public repo and real data (T L24; repo row rated **Endre**, T L106) | NFR-3, NFR-4, the addendum's Test data note and memlog L41 cover it. Still open: test accounts reaching production (G5), the database file in Git (G11), names in information text (G12). | Mostly mitigated |
| Data model, moving guests between households: Middels (T L41) | FR-50 is one sentence with no rules. | **Open** (G2) |
| Many domain rules, numbers must match Hardingasete: Middels (T L40) | FR-32, FR-33, FR-54, NFR-2 and the FR-69 expected results cover it. Payments are in neither the summary nor the expected results (G3). | Partly mitigated |
| Email service and keys: Middels (T L44) | FR-45 and NFR-8 write to the console without a key. The production provider comes in 2027 (D16). | Mitigated |
| Two household members answering at once: Lav (T L45) | FR-38 and C5: the last save applies, and "last updated by" is shown before editing. | Resolved by decision |
| Health data: access, deletion, storage: Middels (T L47) | FR-25 to FR-31, FR-46, FR-66, NFR-3 and NFR-4 cover it. Backups and email copies are not covered (G10), and the delete-all tool waits until 2027. | Mostly mitigated |
| Links and roles: Middels (T L42) | FR-1, NFR-4 (at least 128 bits) and FR-46 cover it. A third role (read-only helpers, enforced on the server) adds work. | Mitigated, but adds to the time risk |
| Process: little activity, start the PRD and prompt log (T L100) | The PRD exists, a month after the feedback, with a memlog, sources on requirements and NFR-9 traceability. The prompt log is not mentioned (X1), and the brief's change log is not updated yet (G14). | Partly mitigated |
| Costs and dependencies: OK (T L65) | NFR-8 covers it. There is no AI; hosting and email are 2027 costs. | Mitigated |
| Checking the AI's work: OK (T L62) | FR-69's expected results are checked by tests. | Mitigated (coverage: G3, G6) |
| When the usability test happens (T L90) | First week of December, with little time to fix findings (accepted in brief memlog L60). The device and network are not stated (G13). | Planned, risk accepted |
