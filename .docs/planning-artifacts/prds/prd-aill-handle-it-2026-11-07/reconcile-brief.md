# Reconciliation: product brief → PRD

- **Input:** `.docs/planning-artifacts/briefs/brief-aill-handle-it-2026-09-23/brief.md` (status final, updated 2026-11-06)
- **Compared with:** `prd.md`, `addendum.md` and the decision log `.memlog.md` in this workspace, as of 2026-11-07
- **References:** "l." line numbers point into `brief.md`. "§9" is PRD section 9, *Changes from the product brief*. "memlog l." points into `.memlog.md`.

## Summary

| | Count |
|---|---|
| Gaps, high | 1 |
| Gaps, medium | 7 |
| Gaps, low | 11 |
| Contradictions without a record | 2 (one is high if confirmed) |
| Deliberate changes, accounted for | 17 |

The PRD keeps the brief's requirements, business rules, numbers and dates well. All numbers and dates survive unchanged:

- 27 May 2028
- about 70 guests
- mid-December 2026
- first week of December 2026
- about December 2027
- 31 August 2028
- under 10 minutes
- under 1 minute
- 90 %
- zero mistakes
- deadline two weeks before Hardingasete's

The losses fall into three areas:

- **Process.** The prompt log commitment is gone.
- **Look and feel.** The palette and "the couple's own look" are gone, and so is large text.
- **Definitions the expected-results tests depend on.** These are meal counts, meals versus accommodation, and payment counts.

## Gaps

### G-1 Prompt log and documented AI use (high)

- **Brief:**
  - Success criteria, course delivery (l. 73): "A complete prompt log backs the reflection report."
  - Constraints (l. 117): "AI is used in the development process and documented in the prompt log."
- **PRD:** Missing.
  - The course-version metrics (SM-1 to SM-5) have no process metric.
  - Section 7 only says Rikke "builds with AI assistance, using the BMAD method".
  - NFR-9 traces stories to requirement IDs, but not to AI sessions.
  - No memlog or §9 entry drops it.
- **Why high:** It is the brief's only process success criterion. It maps directly to grading criterion 1 (30 %), which asks for saved prompts and AI sessions linked to concrete changes.
- **Fix:**
  - Add a course-version metric: every AI session that changes the repo is logged in `.logs/`, with key prompts quoted and each AI proposal marked accepted, changed or rejected, and the log backs the reflection report.
  - Add the prompt log to the constraints in section 7.
  - Extend NFR-9's traceability to the session logs.

### G-2 The couple's own look (medium)

- **Brief:** What makes this different (l. 61): "Norwegian first, with the couple's own look. Sage green, soft white and dark wood, not a template."
- **PRD:** Two traces survive: NFR-5's contrast check of "sage green on soft white", and the addendum's "green envelope".
  - "Dark wood", "the couple's own look" and "not a template" appear nowhere.
  - The addendum's invitation reveal says the content keeps "the same visual style", but never says what that style is.
- **Fix:**
  - Add a "Look and feel" entry to the addendum's *For UX* section: sage green, soft white and dark wood; the couple's own look, not a template; Norwegian first.
  - Add one line to NFR-6 or section 1, so that bmad-ux picks it up.

### G-3 Large, readable text (medium)

- **Brief:** Who this serves (l. 52): many guests are older, so the site needs "large, readable text, good contrast, clear labels on every form field…".
- **PRD:** NFR-5 sets contrast, 200 % zoom, 320 px width, visible focus and 44 px touch targets, but no default text size. Zoom leaves the work to the guest, and the older guest in UJ-1 (Sigmund, 78) is the least likely to zoom.
- **Fix:** Add to NFR-5 or NFR-6: guest pages use large body text by default, without zooming. The UX phase sets the exact size, for example at least 18 px.

### G-4 Accepted residual risk of answering for others (medium)

- **Brief:** Data and privacy (l. 131): no source supports one adult consenting for another. The brief chooses a confirmation plus data minimisation, and says "This remaining risk is accepted and documented."
- **PRD:** FR-27 implements the confirmation. The PRD records neither the legal uncertainty nor the fact that the risk was accepted.
  - The PRD has no risk section.
  - Q8 asks the teacher about the consent model in general, not about this risk.
- **Fix:** Add an accepted-risk line under NFR-3 or the assumptions in section 7:
  - The risk: one person's confirmation is not consent from another adult.
  - The mitigations: FR-25 (minimal data), FR-27 (confirmation) and FR-30 (withdrawal).
  - The acceptance: accepted by Rikke [brief, C2, R 3.2].

### G-5 Test accounts exist only locally, and the repo is public (medium)

- **Brief:** Data and privacy:
  - l. 129: "The test admin user is fictional, exists only in local seed data, and its login is documented in the README."
  - l. 125: "The repository is public."
- **PRD:**
  - FR-68 seeds a test couple admin and a test helper, and in UJ-6 the README publishes their logins.
  - Nothing says that seed data and test accounts must never reach production, and the 2027 list in 3.2 doesn't include it.
  - The PRD never says the repo is public, which is the reason for NFR-3's fictional-data rule and NFR-4's no-secrets rule.
- **Why medium:** If the README's admin password worked in production, it would expose real guest data, including allergies, which are health data.
- **Fix:**
  - NFR-4: test accounts and fictional data exist only in local seed data. The seed command refuses to run against the production database, and production has no test accounts.
  - Add this check to 3.2.
  - State in NFR-3 that the repository is public.

### G-6 Prices before any choice (medium)

- **Brief:** The solution (l. 35): "Before guests choose anything, they see the paid options with the price next to each one and a short note on why guests pay for these."
  - The brief is not consistent here: its Must list (l. 91) uses the weaker "before guests choose".
  - C3 in `pre-prd-discovery.md` says "before the form asks".
- **PRD:** FR-32 says "The price of each paid option is shown before the guest chooses."
  - A price next to each checkbox satisfies this, even after the guest has already chosen which days to come.
  - FR-9 only marks "what costs money", with no amounts.
  - So a guest can decide to come on Friday before seeing that Friday means a paid dinner and a cabin paid for the whole weekend.
- **Fix:** Extend FR-32 and link it to Q7:
  - Before the first question (on the form's first screen or on the programme page), show an overview of all paid options with prices and the short note on why guests pay.
  - Then show each price again next to its option.

### G-7 Counts for every meal, including those the couple pays for (medium)

- **Brief:**
  - The solution (l. 44): the admin area shows "meal counts for every meal".
  - l. 42: Saturday lunch and dinner are paid by the couple.
- **PRD:** FR-54 says "the count per meal", but the form only offers the paid meals (FR-15, FR-32).
  - Nothing defines how Saturday lunch and dinner are counted, yet they are the main meals Hardingasete must cater (UJ-4 step 5).
  - The expected-results list (FR-69) therefore has no defined number for them.
- **Fix:**
  - In FR-54, name all five meals: Friday dinner; Saturday breakfast, lunch and dinner; Sunday breakfast.
  - State the counting rule, for example "everyone coming on Saturday counts for Saturday lunch and dinner".
  - Include both meals in FR-69.

### G-8 Meals don't depend on accommodation, and the wedding-day-only guest (medium)

- **Brief:**
  - Must (l. 91): "Meals are chosen independently of accommodation."
  - The solution (l. 35): "Guests can come without staying overnight, for example only for the wedding day." This is decision D2.
- **PRD:** The rule is only implied, by keeping FR-15 and FR-16 separate.
  - It is never stated, and D2 is not cited anywhere.
  - FR-15's "Saturday breakfast only to those present from Friday" makes it easy to wrongly tie breakfast to the cabin.
  - FR-68's seed households have no wedding-day-only guest without a cabin. So the case the brief names is not in the expected-results list or the tests.
- **Fix:**
  - Add one sentence to FR-15 or FR-16: meals don't depend on staying overnight [D2].
  - Add a Saturday-only guest without a cabin to FR-68.

### G-9 Payment counts in the admin summary (low)

- **Brief:** Success criteria (l. 69): the admin overview shows correct counts for "attendance, meals, beds, allergies, payments", checked by automated tests.
- **PRD:** The FR-54 summary has no payment line.
  - Payment status is shown per household (FR-57) and as exceptions (FR-56).
  - NFR-2 tests "counts and totals" without naming payment statuses.
- **Fix:**
  - Add to FR-54: the number of households in each payment status, and the total still owed.
  - Name payment statuses in FR-69 and NFR-2.

### G-10 Two of the four problems are gone (low)

- **Brief:**
  - The problem (l. 28–29) names "Guests get confused" (the details live in one image or a long message) and "Changes don't reach everyone".
  - The executive summary (l. 14) says the old way "can't keep 70 people up to date when plans change".
- **PRD:** "The problem it replaces" keeps chasing and miscounting, adds payments, and drops both of these.
  - V1 does answer them: the information pages, the link that always shows the current state (FR-24), and change notices as If time.
  - But the reason for these features is no longer written down.
- **Fix:** Add both problems to section 1, one sentence each, and say how v1 meets them.

### G-11 Guests who don't read Norwegian (low)

- **Brief:** If time (l. 103): an English version with "a language button at the top. Until then, guests who don't read Norwegian ask the couple directly."
- **PRD:** Section 3.3 keeps the English version but drops where the button goes. "Who it is for" names these guests, but nothing says what they do in v1.
- **Fix:** Add the v1 fallback to 3.3 or NFR-6: they contact the couple, whose contact details are on every guest page (FR-6).

### G-12 Usability test participant and device (low)

- **Brief:**
  - Success criteria (l. 76): "An older relative who is not comfortable with technology … on Rikke's phone or PC".
  - The change log (l. 147) explains the device: the course version only runs locally.
- **PRD:** SM-3 says only "An older relative", with no device. Being "not comfortable with technology" is what makes the test meaningful.
- **Fix:**
  - Restore both parts in SM-3.
  - If the test uses the phone, the local app must be reachable from the phone on the home network. Note this for the architecture and the README.

### G-13 Two course success criteria are not metrics (low)

- **Brief:** Success criteria:
  - l. 70: answers lock at the deadline, and the admin can still override them.
  - l. 71: a guest question shows up in admin; it is emailed when a key is set, and written to the console otherwise.
- **PRD:** FR-42, FR-63, FR-44 and FR-45 cover these, and UJ-6 steps 6–7 walk through them. But they are missing from the metrics table, so they aren't stated as acceptance checks for the course.
- **Fix:** Add them to the course metrics, or name UJ-6 as the acceptance script for SM-1 and SM-5.

### G-14 Answered questions stay visible (low)

- **Brief:** Must (l. 94): "Guest questions are always stored and shown in admin."
- **PRD:** FR-44 lists questions under "Needs attention", and the addendum's table removes them from the list once they are marked answered.
  - FR-57's full overview doesn't show questions, so answered questions are stored but not shown anywhere.
  - The read-only helpers lose the record.
- **Fix:** In FR-44 or FR-57, keep all questions viewable, answered or not, for example per household.

### G-15 The consent text should say that withdrawing deletes the data (low)

- **Brief:** Must (l. 92): before they consent, guests are told they can withdraw through the same link, "which deletes the allergy information".
- **PRD:** The consent text in FR-26 says consent "can be withdrawn through the same link", but not that the data is then deleted. FR-30 has the behaviour, but not the wording guests see.
- **Fix:** Add "and that withdrawing deletes the information" to the last bullet of FR-26.

### G-16 What email costs in production (low)

- **Brief:** Open questions (l. 120): "whether sending email costs anything in production."
- **PRD:** D16 in section 8 covers the provider and EU storage, but not cost.
- **Fix:** Add cost to D16.

### G-17 "Finished, stable and tested", and a simple, justified stack (low)

- **Brief:**
  - Scope (l. 87): "Must: finished, stable and tested by mid-December 2026".
  - Constraints (l. 117): "A simple full-stack solution with one database, chosen and justified in the architecture document".
  - Information pages (l. 90): "Kept simple".
- **PRD:**
  - Section 3.1 says what is in v1, but not the standard it must meet.
  - Section 7 says the technology "is chosen", not that the choice is justified, and drops "simple".
  - V1 has grown well beyond the brief's Must (§9 "New in v1", memlog l. 72), so keeping things simple matters more now, not less.
- **Fix:**
  - 3.1: "Every v1 requirement is finished, stable and tested."
  - Section 7: "A simple solution with one database, chosen and justified in the architecture document."

### G-18 Keepsake after the wedding (low)

- **Brief:** Vision (l. 141): if time allows after the wedding, guests share photos and the couple posts a thank-you.
- **PRD:** It is not in If time, Out of scope, Rejected alternatives or the memlog.
- **Fix:** Record it as outside this PRD. Note that guest photos are personal data, so the keepsake would conflict with two existing requirements:
  - deleting all data by 31 August 2028 (NFR-3);
  - NFR-1's availability "until the wedding".

### G-19 The examiner uses an ordinary PC (low)

- **Brief:** Must (l. 95) and the change log (l. 147): the site "also works and is easy to read on a PC, using the phone layout", "since the examiner runs it on a PC".
- **PRD:** In UJ-6 step 4, Ingrid opens the guest link "in a narrow window, like a phone". This suggests the examiner has to resize the window, but NFR-6 already says a PC shows the phone layout.
- **Fix:** Rewrite UJ-6 step 4: she opens the link in an ordinary browser window, and the guest pages show the phone layout, readable on a PC. A narrow window becomes optional.

## Contradictions without a record

### X-1 The journey personas may be real guests (high if confirmed; verify)

- **Brief:** Data and privacy (l. 127): "Real names, guest lists, allergies and payment details are never committed and never pasted into AI tools."
- **PRD:** UJ-1 to UJ-3 name Bestefar Sigmund (78) and bestemor, Onkel Arild, tante Marie, Filippa, Leone and Synne, with ages and household details.
  - FR-68 and memlog l. 62 reuse them as seed data.
  - The memlog says Rikke narrated these journeys (l. 12, l. 22), using family-role names.
  - UJ-6 calls them "fictional", but no memlog entry records Rikke confirming that they are made up. Only the partner's name has an explicit decision (l. 21).
- **Risk:** If any of them are real, the PRD already breaks the brief's rule, and the seed data would put real names into a public repo.
  - The names are in three local commits on `docs/prd` (ae1b330, a9b95e8, 7384511).
  - That branch is not yet among the remote-tracking branches, so it can still be fixed before pushing.
- **Fix:** Ask Rikke. If any names are real, replace them with clearly made-up names in `prd.md`, `addendum.md` and `.memlog.md` before pushing, and log her answer in the memlog.

### X-2 Speech sign-ups visible only to the toastmaster (low)

- **Brief:** If time (l. 100): "Speech sign-ups that reach the toastmaster". In the brief, every admin user had full access (l. 93).
- **PRD:** Section 3.3 says "Only the toastmaster sees the sign-ups", which hides them from the couple.
  - The rule comes from the idea list in `pre-prd-discovery.md`, not from a memlog or §9 entry.
  - FR-46's two roles can't express it: the couple has full access, and helpers see everything.
- **Fix:** Either record the decision in §9 and the memlog and flag the extra visibility rule for the architecture, or go back to the brief's wording.

## Deliberate changes (accounted for)

- **Helpers.** Full access → read-only (§9; memlog l. 51; FR-46).
- **Payment status.** Paid/not paid with undo → amounts are registered and the status is calculated: not paid, part paid, paid or refund owed. This absorbs "paid X, now owes Y" (§9; memlog l. 52, 55; addendum *Rejected alternatives*; FR-59, FR-60).
- **"I have paid".** Optional → in v1 (§9; memlog l. 19; FR-35).
- **Who is answering.** "First chooses who they are" → "I am …" is preset to the link's owner and can be changed (§9 *Links*; memlog l. 38; *Rejected alternatives*; FR-12).
- **Consent text.** It also says that names and allergies go to Hardingasete's kitchen (§9; memlog l. 58; FR-26).
- **Gift list.** The format was open in the brief → a simple text page with links, If time (§9; memlog l. 70).
- **Guest contact details.** The couple stores an optional phone and email per guest. Rikke rejected Claude's names-only proposal (§9; memlog l. 84; *Rejected alternatives*; FR-49).
- **Friday hike.** Asked only of those present on Friday; the programme still shows it to everyone (memlog l. 81; FR-9, FR-17).
- **Saturday breakfast.** Offered only to those present from Friday (memlog l. 28; FR-15).
- **Deadline lock.** The brief locks answers "so the numbers stay fixed". The PRD keeps the lock, but allergy consent can still be withdrawn after the deadline. That deletes the allergy data and marks the household "Changed". Adding or changing allergies is locked (memlog l. 37, 39, 82; FR-30, FR-42).
- **The couple's names.** "Rikke and partner" → the partner is named, Valdemar (memlog l. 21).
- **Information pages.** House rules are folded into *Practical information*, and a *Hardingasete and the area* card is added (memlog l. 16; FR-8, FR-10; addendum *Front page structure*).
- **Prices.** "Easy to change" → prices, the deadline, contact details and payment details are admin settings, with a warning when prices change. Page text stays in the code (D12; memlog l. 63, 69; FR-64, FR-65).
- **Admin on a PC.** The full admin overview may be designed for a PC in v1, while a PC layout for guests stays If time (memlog l. 42; FR-48; NFR-6).
- **Letter animation.** → A green envelope with an "R & V" seal, If time. The static invitation look is Must (memlog l. 15; 3.3; addendum *Invitation reveal*).
- **Beds and cabins.** The open question about beds is partly closed: no bed limit, and cabins are allocated outside the site (memlog l. 59, 79; section 7 Q1; 3.4; *Rejected alternatives*).
- **V1 scope.** V1 has grown beyond the brief's Must: "Needs attention", counts that open the people behind them, "Changed", settings, the privacy page, and consent recorded by the couple. The scope risk is handled by moving FR-40, FR-52, FR-62 and FR-67 to [2027] (§9 "New in v1"; memlog l. 72, 75).

## Qualitative ideas at risk

| Idea in the brief | Where | State in the PRD | Suggested home |
|---|---|---|---|
| The couple's own look: sage green, soft white and dark wood, "not a template" | l. 61 | Only a contrast check survives (NFR-5) | Addendum *For UX* (G-2) |
| Large, readable text for older guests | l. 52 | Missing; zoom only | NFR-5 or NFR-6 (G-3) |
| "The honest advantage isn't technology. It's fit": built for exactly one wedding, by someone who knows every guest, without paying for or settling for a generic product such as Joy, Zola or The Knot | l. 56, 63 | Gone. Only NFR-7 ("no further scaling") and D12 echo it | One sentence in section 1 as a design principle: prefer simple, single-wedding solutions over general features |
| The vision: "a great weekend and a stress-free run-up"; guests "arrive knowing what to expect, having answered once"; the couple plans the celebration instead of chasing replies | l. 137 | Gone. "What matters most" covers reliability, simplicity and readable answers, but not the experience the site exists for | One line of purpose in section 1 |
| "The one place for everything about the weekend", still right when plans change | l. 14, 29, 35 | The pages exist, but neither the problem nor this promise is written down | Section 1 (G-10) |
| Simplicity as a way of building: "one simple form", "Kept simple", "a simple full-stack solution" for a beginner | l. 12, 90, 117 | "Simple for guests" is kept. Simplicity as a build constraint is dropped, while v1 has grown | Section 7 (G-17) |
| No surprises about money: guests see the prices and the reason before any choice | l. 35 | Partly kept: the friendly note (FR-32) and the stable total (FR-33). The up-front overview is weakened | FR-32 (G-6) |
| Why the site is called "AI'll handle it": it is built with AI as a development partner | l. 16 | Gone. Next to "The site itself has no AI features", the name now reads oddly | One sentence in section 1 |
| A learning project that ends in something that will actually be used | l. 63 | Partly kept, through the "Two deliveries" table | — |
| A keepsake after the wedding | l. 141 | Gone | An out-of-scope note (G-18) |

**Preserved well:**

- The invitation that "feels like one": FR-7 and the addendum's reveal, with the static look as Must.
- Households answering together.
- Norwegian first (NFR-6).
- Numbers the couple can trust (UJ-4, FR-55).
- The warm tone, which the addendum states more strongly than the brief does.

## Noticed in passing (not from the brief)

- **Stray row in the addendum.** The row "Saving an unfinished answer to continue later | Moved to If time" sits under the *Test data note* heading, cut off from the *Rejected alternatives* table.
- **Journeys ahead of the FRs.** Two journeys describe as v1 behaviour what FR-40 and FR-62 defer to [2027]:
  - UJ-2: the couple opens a change history.
  - UJ-4 and UJ-5: dated contact notes.
