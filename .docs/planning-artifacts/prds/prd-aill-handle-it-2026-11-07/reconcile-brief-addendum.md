# Reconciliation: brief addendum → PRD

**Date:** 2026-11-07
**Input:** `../../briefs/brief-aill-handle-it-2026-09-23/addendum.md`, cited as **A Lnn** (line numbers in that file)
**Compared against:** `prd.md` (**PRD Lnn**), `addendum.md` in this folder (**PRD-add Lnn**), `.memlog.md` (**memlog Lnn**)
**Also checked for provenance:** `extract-brief.md` in this folder, `../../research/user-voice-wedding-website-pre-prd-2026-11-06/pre-prd-discovery.md`

**In brief.** There are no high-severity gaps: every v1 Must in the input (A L73) is in the PRD. The losses are mostly qualitative ideas and content: the look and feel, the programme details, the whole-weekend intent, the gift message and how prominent the important notes are. One change has no record anywhere: speech sign-ups are now visible to the toastmaster only. Most losses happened while the PRD was drafted, not during extraction. `extract-brief.md` captured them (L19, L21, L35, L38–39, L72, L74, L138, L176), but `prd.md` and the PRD addendum don't carry them.

| | High | Medium | Low |
|---|---|---|---|
| Gaps (section 1) | 0 | 5 | 5 |
| Contradictions without a record (section 2) | 0 | 1 | 0 |
| UX items to preserve in the PRD addendum (section 4) | 0 | 2 | 0 |

## 1. Gaps

### G1. Programme and venue details are missing (medium)

- **Input:** A L24–28 and L18. On Friday there is a mountain hike during the day for early arrivals. In the evening there is a treasure hunt (rebus), then sauna and hot tub. On Saturday there is optional yoga, then the wedding, and the couple hosts lunch and dinner. Hardingasete provides the venue, all meals and the cabins, which are on the farmyard.
- **PRD:** FR-9 (PRD L246) names the activities and says the programme is shown day by day. Neither the PRD nor the PRD addendum contains the programme itself. Times of day, the order of events, "for early arrivals", the rebus and the farmyard cabins are all missing. The "Hardingasete and the area" card in FR-8 has no content source either. The text of the information pages lives in the code (D12, PRD L358), so a story for FR-9 has nothing in the PRD to build from.
- **Fix:** Add a "Programme and venue content (source for FR-8, FR-9)" block under "For UX" in the PRD addendum. Copy it from A L18 and L24–28, and mark the times "to be confirmed with Hardingasete (Q2)". The programme should also say the hike is during the day. FR-17 asks everyone present on Friday (memlog L81), so without that, guests arriving Friday evening may answer "yes".

### G2. "Guests are encouraged to stay the whole weekend" is lost (medium)

- **Input:** A L27.
- **PRD:** The PRD never states this. FR-14's first question ("is everyone coming the whole weekend?") fits the intent, but the intent itself is written down nowhere. UX and the content have nothing telling them to present the whole weekend as what guests are invited to.
- **Fix:** Add one sentence to "What we are building" in PRD §1, for example: "Guests are invited to the whole weekend and encouraged to stay all three days; coming for fewer days is fine." Add a matching line under "For UX" in the PRD addendum, so the invitation and programme texts invite guests to the weekend, not only to the Saturday.

### G3. The gift message is lost (medium)

- **Input:** A L34: "we know the wedding may be expensive to attend and we don't expect gifts, but there is a wish list for anyone who wants one."
- **PRD:** §3.3 (PRD L118) and §9 (PRD L497) keep only the form of the gift list ("simple text page, possibly with links"). The message itself is gone. The gift page is If time, so v1 may end up saying nothing about gifts at all. Yet the message is what balances asking guests to pay for meals and the cabin (C3, and the "why guests pay" note in FR-32).
- **Fix:** Put the wording under "For UX" in the PRD addendum as Rikke's own copy, as was done for the receipt. Consider a one-line "we don't expect gifts" note in v1, either on the Practical information page or next to the FR-32 note, regardless of whether the gift page is built.

### G4. The important notes have become a sub-item (medium)

- **Input:** A L32: "Important notes: child-free wedding; keep phone use to a minimum." The input lists this as a content page of its own.
- **PRD:** FR-10 (PRD L247) folds the notes into Practical information as "house rules (child-free, little phone use)", behind a "Read more" card. FR-7, FR-8 and the front-page structure (PRD-add L16–25) have no place for them. A guest can therefore send the RSVP without ever seeing that the wedding is child-free. That matters for parents, who need to arrange childcare for a whole weekend. The renaming already happened in `extract-brief.md` L46.
- **Fix:** Add to FR-7 or FR-8 that the child-free and phone notes are visible without opening a "Read more" page. They could go on the invitation, on the first card or in the first RSVP step; UX decides where. Keep the friendlier framing "Important" rather than "house rules".

### G5. The post-wedding keepsake was dropped without a record (medium)

- **Input:** A L68: "Possible post-wedding keepsake (photo sharing, thank-you message) if time allows." The same idea is in the brief's vision (brief.md L141) and was captured in `extract-brief.md` L19.
- **PRD:** It appears nowhere: not in §3.3 If time, §3.4 Out of scope, §9, the rejected alternatives or the memlog. The product impact is low. But the grading guide asks that anything left out of or changed from the plan is described and justified (criterion 2).
- **Fix:** Add a line to §3.4 with the reason, or a note that it may come later, plus a row in §9. If the idea is ever kept, note that photos are personal data. They must be covered by the deletion date of 31 August 2028 (NFR-3) and by the privacy page (FR-66).

### G6. Answered guest questions can't be seen anywhere (low)

- **Input:** A L63: "Guest questions are stored and shown in admin (must-have for V1)."
- **PRD:** FR-44 (PRD L307) shows questions only under "Needs attention". A question leaves that list once the couple marks it as answered (PRD-add L48), and no other view shows it afterwards. The couple can't look back at what guests asked. SM-10 ("guests asking about something the site already answers", PRD L84) can't be checked either.
- **Fix:** Extend FR-44 so that answered questions stay visible, marked as answered, in a question list or on the household.

### G7. The interim plan for guests who don't read Norwegian is lost (low)

- **Input:** A L66: an English version "switched with a language button at the top" is a stretch goal. "Until then, non-Norwegian guests ask the couple directly." See also A L48.
- **PRD:** §1 (PRD L40) names these guests, and §3.3 (PRD L120) has "an English version with a language button". The interim plan is gone, and so is the placement "at the top". `extract-brief.md` L131 had already left out the interim plan.
- **Fix:** Add to §3.3 or §1: "Until then, guests who don't read Norwegian contact the couple directly (their contact details are on every page, FR-6)." Put "language button at the top" under "For UX" in the PRD addendum.

### G8. The open question about email cost is lost (low)

- **Input:** A L63: "Open question: whether sending email costs anything in production."
- **PRD:** §3.2 (PRD L106) and D16 (PRD L484) cover only that the provider must store data in the EU.
- **Fix:** Extend D16 to cover both EU storage and cost.

### G9. Course process requirements are missing from §7 (low)

- **Input:** A L39–41. The reflection report is 3,000–5,000 words and requires that all prompts are saved. The planning artifacts are evidence for section 2.4 of the report. AI use is documented through the development process (prompt log, BMad).
- **PRD:** §7 lists the solo team, BMAD, full-stack with one database and no AI in the site, but not the prompt log. NFR-9 covers tracing stories to requirements, not tracing prompts. The project's `AGENTS.md` and `.logs/` already make logging happen in practice, so the risk is small.
- **Fix:** Add a constraint to §7: "Process evidence: all prompts and AI sessions are saved in `.logs/`; the reflection report requires them."

### G10. "Later visits skip the letter" has no workable definition (low, If time)

- **Input:** A L8.
- **PRD:** §3.3 (PRD L113) and UJ-1 (PRD L149) say "the first time a guest visits" but not how the site knows it is the first time. Recording a visit when the page loads would break FR-3 (PRD L237). Link previews in Messenger, SMS and email would also count as the first visit (C4), so the guest would never see the envelope.
- **Fix:** Note under "For UX" (or the architecture notes) in the PRD addendum how a first visit is detected: per device, or until the guest's own action such as tapping the envelope open. A page load must never count.

## 2. Contradictions without a record

### X1. Speech sign-ups: "only the toastmaster sees" them (medium)

- **Input:** A L51 lists speech sign-ups in the admin overview for "the couple and helpers". A L55 says: "Speech sign-ups should reach the toastmaster." The brief says the same (brief.md L100).
- **PRD:** §3.3 (PRD L117) says: "Only the toastmaster sees the sign-ups." That shuts out the couple, the maid of honour and the best man. It also contradicts the PRD itself. §1 (PRD L43) and FR-46 (PRD L312) define two roles, and helpers "see everything". A view only the toastmaster can see would need a third access level that the role model doesn't have.
- **Record:** There is none in the memlog, §9 or the rejected alternatives. The rule comes from a research idea (pre-prd-discovery §5, L145, "Swedish example [R 1.6]"). That idea was listed for discussion, and Rikke never decided on it. An AI-proposed change has gone into the PRD without a recorded decision, which matters for criterion 1 (Prosess og KI-styring).
- **Fix:** Ask Rikke.
  - If she keeps the rule, log it in the memlog, add a row to §9 and add a toastmaster-only permission to FR-46. Update the consent and privacy texts if needed.
  - If not, change §3.3 to "Speech sign-ups are shown in the admin overview and reach the toastmaster."
  - Either way, say where guests sign up: per guest in the RSVP form (A L16, L22), or separately.

I found no other contradiction without a record. The change from a consent checkbox to a Yes/No choice is traced by the input itself: A L86 points to C1, which specifies "Yes/No, unticked".

## 3. Deliberate changes (accounted for)

- Letter/envelope animation (A L7–8): moved to If time, while the static invitation look is Must. A L74; PRD §3.3; memlog L15.
- Speech sign-up (A L22): moved to If time. A L74; PRD §3.3. Who sees the sign-ups is covered in X1.
- Full access for all helpers (A L55–56, L64): helpers are now read-only, and only the couple changes data. PRD §9; FR-46; memlog L51.
- "Possibly" toastmaster, maid of honour and best man (A L55): they are definite helper accounts, created with a command. FR-46–47; memlog L83.
- The couple marks who has paid (A L45): replaced by registering amounts, with the status calculated (not paid, part paid, paid, refund owed). PRD §9; FR-59–60; memlog L55; rejected alternatives in the PRD addendum.
- Link tracking by "opened their link" (A L52): changed to "started" (pressed Start or saved an answer) and moved to If time. A L74, L92 (C4); PRD §3.3; FR-3.
- A consent checkbox that blocked sending (A L56, L64, L85): the RSVP can now always be sent, with a separate Yes/No allergy consent that starts unanswered. A L86 (C1); FR-26–28; CM-4.
- The consent names who can see the data (A L64): it now also names Hardingasete's kitchen. PRD §9 "Allergy recipients"; memlog L53, L58.
- "Real data only in the production database" (A L76): the couple also emails names and allergies to Hardingasete, and guest questions are emailed to the couple. PRD §9; FR-26, FR-45; NFR-3 (data processing agreements).
- The respondent chooses who they are (A L89, C6): the choice is now set to the link's owner and can be switched. PRD §9 "Links"; memlog L38.
- One link per guest (A L6): kept, against the research's assumption of one link per household. PRD §9; rejected alternatives in the PRD addendum; memlog L36, L38.
- Expected arrival time (A L51, L60): optional fixed choices, including "Don't know", with no time pickers. Memlog L60; FR-18 [D11].
- Friday hike yes/no/maybe (A L60): asked only of guests present on Friday, while the programme shows the hike to everyone. Memlog L81; FR-9, FR-17.
- Accommodation all or nothing (A L18, L79): a guest who sleeps only one night still pays for both. Memlog L26; FR-16.
- Meals per person (A L19, L79): offered only on days the person is there, and Saturday breakfast only to those there from Friday. Memlog L28; FR-15.
- Treasure hunt, sauna and hot tub, yoga (A L25–26): information only, with no sign-up. PRD §3.4 (Q6); FR-9.
- AI removed, including cabin and bed placement (A L65): no AI in the site, and the couple allocates cabins outside it. PRD §3.4; memlog L59; rejected alternatives in the PRD addendum.
- "Beds needed" (A L51): beds are only counted, with no bed limit. Memlog L79; rejected alternatives in the PRD addendum.
- Gift list form undecided (A L67): a simple text page with links, If time. PRD §9; memlog L70. The lost message is covered in G3.
- English version (A L66, L74): If time. PRD §3.3. The lost interim plan is covered in G7.
- "Change notifications" (A L74): notices to guests stay If time (memlog L78), and email to the couple when an answer changes is dropped (PRD §9; memlog L29; rejected alternatives in the PRD addendum).
- PC layout (A L74): If time, and a PC shows the phone layout. PRD §3.3; NFR-6.
- Printer-friendly page for Hardingasete (A L74): If time, and the couple emails the numbers. PRD §3.3, §3.4; memlog L46.
- Override after the lock (A L54): only the couple can do it, since helpers are read-only. FR-63; memlog L51.
- Allergies after the deadline: guests can no longer change them, but withdrawing consent still works. Memlog L39, L82; FR-30, FR-42.
- Guests pay the couple, who pays Hardingasete (A L44): kept, but it may change if Hardingasete allows guests to pay directly. PRD §7 Q4 and §8 (open question).

## 4. Qualitative ideas at risk

| # | Idea in the input | Status in the PRD | Action |
|---|---|---|---|
| Q1 | **Elegant but cosy; fits a wedding without being overly fancy** (A L12) | Lost. Only "cosy" survives, and only for the language (NFR-6, PRD L431: "plain, warm … cosy tone"; Tone in PRD-add L39–41). "Elegant" and "not overly fancy" appear nowhere. "Plain, warm" could be read as a casual visual style. | **Medium.** Belongs in UX; preserve in PRD addendum. Add a "Look and feel" item under "For UX" with A L12 word for word. |
| Q2 | **Palette: sage green, soft white, dark wood** (A L13) | Weakened. It survives only as a contrast warning (NFR-5, PRD L419: "sage green on soft white") and as a "green envelope" (PRD L113; PRD-add L9). Dark wood is gone. The teacher's feedback named the palette as part of a clear basis for the design (tilbakemelding L103, criterion 4). | **Medium.** Belongs in UX; preserve in PRD addendum, and say that the envelope is sage green. Also adjust NFR-5 in the PRD to check every text and background colour pair, not only sage green on soft white. Dark wood is the likely text colour, and white text on sage green buttons needs checking too. |
| Q3 | A physical invitation (letter/envelope) as the way in (A L7) | Kept and enriched: a wax seal reading "R & V" that unfolds into the site (PRD-add L7–14). | No change needed. Check it against Q1 so it doesn't become "overly fancy". |
| Q4 | The invitation is to the whole weekend, and guests are encouraged to stay for all of it (A L27) | Lost. | See G2. |
| Q5 | Care about what attending costs guests: the wedding "may be expensive to attend", and the couple doesn't expect gifts (A L34) | Lost. | See G3. Write it together with the copy explaining why guests pay (C3). |
| Q6 | Child-free and little phone use as *important* notes (A L32) | Weakened to "house rules" behind "Read more". | See G4. Keep the tone friendly, not like a set of rules. |
| Q7 | An active, social weekend in Hardanger: day hike, rebus treasure hunt, sauna and hot tub, yoga (A L25–26) | Reduced to a list of activity names. | See G1. |
| Q8 | Easy for guests of all ages (A L14) | Kept and strengthened (NFR-5, NFR-6, SM-3, UJ-1). | No change needed. |
| Q9 | Guests who don't speak Norwegian are looked after (A L48, L66) | These guests are named (PRD L40), but the interim plan is lost. | See G7. |
| Q10 | Speech sign-ups reach the toastmaster (A L55) | The intent is kept, but who can see the sign-ups changed without a record. | See X1. |

## 5. Other findings (not from this input)

- PRD-add L88: a row from the rejected-alternatives table ("Saving an unfinished answer …") ended up below "Test data note". It renders as a stray table row.
- PRD §3.3 (PRD L119) defines link tracking as "pressed Start", but the PRD elsewhere calls this the RSVP button (FR-7). Use one name.
- UJ-2 (PRD L178), UJ-4 (PRD L202) and UJ-5 (PRD L214) describe the change history and the dated contact notes as if they were in v1. FR-40 and FR-62 are marked [2027].
