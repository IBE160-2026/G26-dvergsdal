---
title: "GDPR review: PRD for AI'll handle it"
type: review
reviewer: "Claude (GDPR reviewer in the PRD reviewer gate)"
reviewed:
  - prd.md (draft, 2026-11-07)
  - addendum.md (2026-11-07)
background:
  - ../../research/user-voice-wedding-website-pre-prd-2026-11-06/research.md (section 3)
created: 2026-11-07
status: for triage
---

# GDPR review: PRD for AI'll handle it

> This review is part of the reviewer gate (see `.memlog.md`). It checks `prd.md` and `addendum.md` against the GDPR, with section 3 of the [pre-PRD research](../../research/user-voice-wedding-website-pre-prd-2026-11-06/research.md) as background.
>
> It respects the decisions recorded in `.memlog.md`, the [brief](../../briefs/brief-aill-handle-it-2026-09-23/brief.md) and [pre-prd-discovery.md](../../research/user-voice-wedding-website-pre-prd-2026-11-06/pre-prd-discovery.md). Where a decision creates a real risk, the finding is labelled **Challenges a recorded decision**.
>
> This is not legal advice. The regulatory points should be checked again before production in 2027 [R 9].

**Severity levels**

| Level | Meaning |
|---|---|
| Critical | Unlawful or harmful as specified. Must be fixed before any real data is collected. |
| High | A significant legal gap or a likely problem at the real wedding. Fix it in the PRD before architecture and stories. |
| Medium | Smaller impact, or easy to work around. Fix it in the PRD or before invitations go out. |
| Low | Polish and good practice. |

## Verdict

**Approve with changes. There are no critical findings.**

The privacy foundation is strong for a project of this size:

- Consent is separate from the RSVP, and nothing is ticked in advance.
- Withdrawal works through the same link, even after the deadline.
- Allergy data is minimised.
- Real data stays out of the repo and out of AI tools.
- Production is planned in the EU/EEA, with data processing agreements and a deletion date.

Four high findings should be fixed in the PRD before architecture, because they shape the consent flow and the data model:

1. **G-1:** For other adults, the allergy "consent" is the respondent's statement, not the person's own consent. Now that every guest has their own link, a light fix is cheap. *Challenges a recorded decision (C2).*
2. **G-2:** The planned change history and the daily backups would keep allergy data after consent is withdrawn.
3. **G-3:** The PRD gives no legal basis for any data except the allergies, and that basis is only implied. FR-66 asks for "the legal basis", in the singular.
4. **G-4:** Verbal consent registered by the couple (FR-31) is neither informed nor provable, and it can override a guest's "No" in the form.

Most medium findings need only a sentence or two added to existing requirements.

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 4 |
| Medium | 11 |
| Low | 3 |
| **Total** | **18** |

## Findings at a glance

| ID | Severity | Location | Finding | Fix by |
|---|---|---|---|---|
| G-1 | High | FR-27, FR-29, FR-12 | Consent for another adult's allergies comes from the respondent, not from that person | PRD now |
| G-2 | High | FR-30, FR-40, NFR-1 | The change history and backups keep allergy data after withdrawal | PRD now |
| G-3 | High | NFR-3, FR-66 | No legal basis is stated, except an implied consent for allergies, and the controllers are not named | PRD now |
| G-4 | High | FR-31, FR-28 | Verbal consent registered by the couple is neither informed nor provable | PRD now |
| G-5 | Medium | FR-46, FR-54–57 | Helpers see everything, including questions written to the couple | PRD now |
| G-6 | Medium | FR-30, FR-56, FR-58 | Withdrawal after the allergy list is sent, and withdrawal by mistake | v1 |
| G-7 | Medium | NFR-3, FR-45, FR-67 | Copies outside the database are never deleted, and allergy data is kept after the wedding | 2027 (FR-45 in v1) |
| G-8 | Medium | FR-66, FR-5, FR-52 | The privacy page misses points from Art. 13 and 14, and it is unclear when and where it appears | v1 |
| G-9 | Medium | FR-26, FR-66, 3.3 | The consent and privacy texts are only in Norwegian | 2027 |
| G-10 | Medium | FR-25, FR-43, FR-62 | Free-text fields invite health data and other sensitive data | v1 |
| G-11 | Medium | FR-2, FR-4, FR-24 | Link previews and forwarded links expose the household's answers | v1 |
| G-12 | Medium | NFR-4, NFR-1, FR-47 | Production security lacks HTTPS, backup rules, account removal, log rules and a breach plan | 2027 (logging rule in v1) |
| G-13 | Medium | NFR-3, 3.2 | The list of processors and transfers is incomplete, and guest pages may load content from third parties | 2027 (no third-party requests from v1) |
| G-14 | Medium | NFR-3, 3.2 | There is no record of processing, no joint-controller note and no instructions for helpers | 2027 |
| G-15 | Medium | UJ-1–UJ-3, FR-68, SM-3 | The public repo may hold real people's names, and the usability test may be recorded there | Now |
| G-16 | Low | FR-49, FR-63, FR-66 | Rights other than withdrawal need only small changes | v1 |
| G-17 | Low | FR-26, FR-29, FR-30 | Small gaps in the consent text and the consent record | v1 |
| G-18 | Low | 3.3 | If-time features change what data is collected and who sees it | When built |

## Consent at a glance

| Condition | Status | See |
|---|---|---|
| Freely given (Art. 7(4)) | **Met.** The RSVP works without consent, and nothing is ticked in advance. | FR-26, FR-28, CM-4 |
| Specific | **Mostly met.** There is one clear purpose (safe food), but the text names neither the controllers nor the exact data. | G-17 |
| Informed | **Partly met.** Not for guests who don't read Norwegian, and not for consent registered by the couple. | G-9, G-4 |
| Explicit and unambiguous (Art. 9(2)(a)) | **Met online:** "I consent to …", as a Yes/No choice that starts unanswered. **Not met** for verbal consent as specified. | FR-26, G-4 |
| Withdrawable as easily as given (Art. 7(3)) | **Met, with gaps.** The history and backups keep the data. A withdrawal by mistake is easy, and after the deadline it can't be undone. | FR-30, G-2, G-6 |
| Given by the data subject | **Not met** when one adult answers for another. | G-1 |
| Provable (Art. 7(1)) | **Partly met.** Not for adults whose answers were entered by others or by the couple, and the couple can't see the consent records. | FR-29, G-1, G-4, G-17 |

## Findings

### High

#### G-1 · High · Consent for another adult's allergies comes from the respondent, not from that person

**Location:** FR-27, FR-29, FR-12, FR-58; UJ-1 step 4; UJ-2 step 1
**Fix by:** PRD now (consent flow and data model)
**Challenges a recorded decision:** decision C2 in `pre-prd-discovery.md` and "Answering for others" in the brief. Both accepted the remaining risk on 2026-11-06.

**Finding.** Usually one person answers for the whole household: Sigmund for bestemor (UJ-1), Arild for Marie and the daughters (UJ-2). For the others, the stored "consent" is only the respondent confirming that they "know about it and agree" (FR-27). FR-29 then records "who gave it". Anyone can pick "I am …" (FR-12), so the record may even name the wrong person.

**Why it matters.** Art. 9(2)(a) requires explicit consent from the data subject, and Art. 4(11) defines consent as the data subject's own indication of their wishes. The research found no source that lets one adult consent for another (EDPB 05/2020 para 93; Helsedirektoratet) [R 3.2]. The couple has to prove consent (Art. 7(1)), and for most allergy entries they can't.

The risk was accepted while the research still assumed one link per household. The PRD has since given every guest their own link (FR-1). That removes most of the reason for accepting the risk: the other person can now confirm through their own link, without anyone answering again.

**Suggested fix.** Keep "one person answers for everyone", and add a light confirmation through each guest's own link:

1. Reword FR-27: "[Name] has asked me to give this information and agrees to the consent text above." The respondent then passes on the other person's decision instead of making it for them.
2. FR-29 records the following for each person whose allergy data is stored:
   - how consent was given: through their own link, through a household member, or registered by the couple (FR-31);
   - whose link was used, and which "I am" was chosen;
   - the time and the version of the consent text.
3. When that person opens their own link, the page shows: "Arild registered allergy information for you on 12.01. It is shared with … [Yes, I consent] [Remove it]."
   - Both buttons look equally important, and the question is shown only once (CM-4).
   - Choosing "Yes" turns the entry into the person's own consent.
   - The message also gives the person the information Art. 14 requires when data comes from someone else.
4. The allergy list (FR-58) marks entries that the person has not confirmed, so the couple can check them by phone before sending the list. These entries still go to the kitchen, because food safety comes first.
5. Update the note on remaining risk in the brief and the PRD. What remains is the people who never open their link. If Rikke wants certainty, she can ask Datatilsynet's guidance service, as the research suggests [R 7].

#### G-2 · High · The change history and backups keep allergy data after withdrawal

**Location:** FR-30, FR-40 [2027], FR-67; addendum, "Change marker and history"; NFR-1 (daily backups)
**Fix by:** PRD now. FR-40 is [2027], but the data model is decided during architecture.

**Finding.** FR-30 promises that withdrawing consent deletes the person's allergy information. Two parts of the plan would keep it anyway, and the PRD says nothing about either:

- **Change history.** FR-40 keeps "who changed what, and when" for every change, and the addendum asks for a data model that allows a full history from the start. A typical history table stores the old and new values. The allergy categories and notes would therefore survive a withdrawal or a correction.
- **Backups.** The daily backups (NFR-1) keep the same data, and restoring one would bring withdrawn data back.

**Why it matters.** Once consent is withdrawn, there is no legal ground left, so the data must be erased (Art. 7(3), Art. 17(1)(b)). A privacy page that promises deletion that doesn't happen also breaks the transparency principle (Art. 5(1)(a)). Getting the data model right now is cheap; fixing it after the site is live is not.

**Suggested fix.** Add these rules to FR-30, FR-40 and NFR-3:

1. The history records *that* allergy information or consent was added, changed or withdrawn, for whom, by whom and when. It never stores the allergy information itself.
2. Consent and withdrawal events are kept as proof (Art. 7(1)), without the allergy information.
3. Backups are encrypted, stored in the EU/EEA and deleted after a fixed number of days, for example 30. The privacy page says that deleted data disappears from the backups within that time.
4. After a restore, any withdrawals and deletions made since the backup are carried out again. A small log of the IDs involved, without content, is enough for this.
5. An automated test checks that after a withdrawal, no table, including the history, still holds that person's allergy information. This also counts towards criterion 3.

#### G-3 · High · No legal basis is stated, except an implied consent for allergies

**Location:** NFR-3; FR-66 ("the legal basis"); section 1 (who the site is for)
**Fix by:** PRD now

**Finding.** The PRD implies that consent is the legal basis for allergies (FR-26). For all other data it states no legal basis at all:

- names and households;
- the phone numbers and email addresses the couple enters;
- RSVP answers, payments and "I have paid" reports;
- questions, notes and the change history;
- consent records and admin accounts;
- technical logs, including the IP addresses used to slow down repeated attempts (NFR-4).

FR-66 asks the privacy page to state "the legal basis", in the singular. That suggests one basis for everything, and the likely wrong guess is "consent". Guests are never asked to consent to the couple storing their names or numbers, and the PRD rightly makes the RSVP independent of consent (FR-28, CM-4). The PRD also never says who the controllers are.

**Why it matters.** Every purpose needs a legal basis under Art. 6(1), and the privacy page must state the basis for each purpose (Art. 13(1)(c)). Where the basis is legitimate interest, the page must also say what that interest is (Art. 13(1)(d)). If RSVP data were based on consent, withdrawing consent would delete the RSVP itself, which works against the reliability goal.

**Suggested fix.**

1. Add a short list of the data to NFR-3, giving for each kind of data its source, purpose, legal basis, who sees it and when it is deleted. Appendix A is a starting point:
   - legitimate interest (Art. 6(1)(f)) for all data except allergies;
   - explicit consent (Art. 6(1)(a) together with Art. 9(2)(a)) for allergies and dietary needs.
2. Write down a short balancing test for legitimate interest, covering three points:
   - guests expect the couple to keep track of answers and money (Recital 47);
   - the data is limited, and so is access to it;
   - everything is deleted by 31 August 2028.
3. Name the roles in NFR-3:
   - Rikke and Valdemar are joint controllers (Art. 26);
   - the helpers act on their behalf (Art. 29);
   - Hardingasete receives allergy data as a controller in its own right;
   - the hosting, backup and email providers are processors (Art. 28).
4. Change FR-66 to "the legal basis for each purpose".

#### G-4 · High · Verbal consent registered by the couple is neither informed nor provable

**Location:** FR-31, FR-28, FR-42; UJ-3 step 5
**Fix by:** PRD now (FR-31 is in v1)
**Challenges a recorded decision:** the memlog entry "When an admin enters allergies on a guest's behalf, the admin ticks 'The guest consented verbally or by message'". The fix builds on this decision rather than replacing it.

**Finding.** FR-31 lets the couple tick that a guest consented "by phone or message". The site then records who registered it and when. Three things are missing:

- **Information.** Nothing makes sure the guest is told what FR-26 tells guests in the form: that the helpers can see it, that the name goes to Hardingasete's kitchen, and that consent can be withdrawn.
- **Proof.** The record doesn't say how consent was given or which version of the consent text applied.
- **Respect for a "No".** FR-28 tells a guest who answers "No" in the form that they "can tell the couple directly". If the couple then registers the allergy through FR-31, it ends up exactly where the guest just declined to put it.

After the deadline, FR-31 is the only way to add allergies (FR-42).

**Why it matters.** "By the way, I'm allergic to nuts" said on the phone is not explicit, informed consent to sharing with the helpers and the kitchen (Art. 4(11), Art. 9(2)(a)). The EDPB accepts spoken consent only when the person was given the same clear information and confirmed specifically, and it warns that such consent is hard to prove (EDPB 05/2020, paras 94–95). This route matters most for older guests and for guests who don't read Norwegian. Overriding a guest's "No" is a real way to lose their trust.

**Suggested fix.** Change FR-31 and FR-28:

1. Before ticking, the couple gives the guest the same consent text as FR-26. The best way is to send a ready-made message with the text and a link to the privacy page, and ask the guest to reply "Yes". The reply is written proof. Reading the text aloud is the fallback.
2. The record stores:
   - how consent was given (phone or message) and which version of the text applied;
   - who consented, which must be the person the data is about (G-1);
   - who registered it, and when.
3. Make FR-28 honest. Either tell the guest "If you tell us directly, we register it with your consent, and it is shared in the same way", or offer a genuinely more private option, for example that the couple tells the kitchen without storing it on the site.
4. Before the deadline, the couple asks guests who can use their link to give consent there themselves.

### Medium

#### G-5 · Medium · Helpers see everything, including questions written to the couple

**Location:** FR-46, FR-54–FR-57, FR-62, FR-40; NFR-4; the list of who can see allergies in FR-26
**Fix by:** PRD now (the roles are in v1)
**Challenges a recorded decision:** the memlog entries "Helper roles changed from brief: … READ-ONLY admin access" and "Helpers (read-only) also see guests' phone numbers and emails".

**Finding.** The helpers can change nothing, but they "see everything":

- contact details and allergies;
- payment status, "I have paid" reports that don't match a payment, and refunds;
- guest questions;
- the couple's notes and the change history.

None of the helpers' tasks in the PRD needs payments, questions, notes or the history. The clearest example is "Ask us" (FR-43). The guest writes to the couple, but the question also shows up for the toastmaster, maid of honour and best man under "Needs attention" (FR-56). Questions can be personal: money trouble, seating, a family conflict or health.

**Why it matters.** By default, only the data needed for each purpose may be processed, and Art. 25(2) says explicitly that this also covers *who can access it* (see also Art. 5(1)(c)). Guests who believe they are writing privately to the couple are misled, which breaks fairness and transparency (Art. 5(1)(a)). At a family wedding, this is the most likely way for the site to cause real social harm.

**Suggested fix.** Describe what helpers see in FR-46:

- **Helpers see:**
  - the summary counts (FR-54);
  - the people behind the counts for attendance, days, meals, overnight stays, the hike and arrivals;
  - allergies, but only if a helper has a named task that needs them, for example the toastmaster talking to the kitchen on the day;
  - contact details, but only where a task needs them, for example the toastmaster organising speeches.
- **Helpers don't see:** payments, questions, notes or the history.
- **The server enforces it:** the server limits what helpers can see, not only what they can change (NFR-4).

If Rikke wants to keep "helpers see everything", two things are needed as a minimum:

- the "Ask us" form says that the helpers can read questions too;
- the privacy page and the consent text list everything the helpers can see.

#### G-6 · Medium · Withdrawal after the allergy list is sent, and withdrawal by mistake

**Location:** FR-30, FR-42, FR-56, FR-58; UJ-4 step 5
**Fix by:** v1

**Finding.** Withdrawing consent deletes the data, and the household is only marked "Changed" (FR-30). Two cases are not covered:

- **The list has already been sent.** If the couple has already emailed the allergy list to Hardingasete, the kitchen still has the withdrawn data.
- **Withdrawal by mistake.** Anyone with a link to the household can withdraw consent for any member in one step, even someone who was forwarded the link (G-11). After the deadline, guests can't add allergies again (FR-42). A mistaken withdrawal therefore removes a real allergy from the kitchen list without anyone noticing.

**Why it matters.** The couple must tell everyone who received the data when it is erased (Art. 19). A privacy feature also must not put food safety at risk (SM-8: zero allergy mistakes).

**Suggested fix.**

1. Before withdrawing, the site asks for confirmation and names the person and the consequence: "The kitchen will no longer be told about bestemor's allergies."
2. The site records who withdrew, through which link, and when (G-17).
3. A withdrawal gets its own item under "Needs attention", not just the "Changed" marker: "Allergy consent withdrawn for [name] by [name]. If the list has been sent, tell Hardingasete."
4. The couple can register the allergy again, with consent, through FR-31 (G-4).

#### G-7 · Medium · Copies outside the database are never deleted, and allergy data is kept after the wedding

**Location:** NFR-3, NFR-1 ("until the data is deleted"), FR-45, FR-58, FR-67; UJ-4 step 5; the print page in 3.3
**Fix by:** before invitations (2027). The content of the FR-45 email can be fixed in v1.
**Challenges a recorded decision (in part):** that each question is emailed to the couple (FR-45, from the brief).

**Finding.** NFR-3 says that real data lives only in the production database and is deleted by 31 August 2028. But the PRD itself creates copies outside the database:

- emails with the text of each question (FR-45), kept in the couple's mailbox and in the email provider's logs;
- the allergy list with names (UJ-4), kept in the couple's sent mail and in Hardingasete's inbox;
- printed lists, if the print page is built.

FR-67 deletes only the guest data on the site. In addition, all data has the same deletion date, although allergy data is of no use after the wedding. Until August, the guest links keep showing the household's answers, including allergies (NFR-1).

**Why it matters.** Data may be kept only as long as it is needed (Art. 5(1)(e)). The privacy page would promise a deletion date that these copies don't follow. A personal mailbox may also be hosted by a provider outside the EEA.

**Suggested fix.**

1. FR-45: the email only says "There is a new question on the site", with no question text and no names. The question itself stays in the database, which is hosted in the EU.
2. For Hardingasete:
   - send only what the kitchen needs, and agree on the format through Q2;
   - send it to an address confirmed in advance;
   - ask the venue to delete the list after the wedding.
3. Delete data in stages (NFR-3):
   - allergy data within two weeks after the wedding;
   - after the wedding, guest links show only the payment status and a thank-you message, not the answers;
   - everything else by 31 August 2028.
4. Turn FR-67 into a deletion checklist:
   - the database and the backups;
   - the processors' accounts and logs;
   - email copies, both sent emails and notifications;
   - printouts and admin accounts;
   - finally, the hosting itself.
5. Reword NFR-3 so it names the few copies allowed outside the database and says that they follow the same deletion dates.

#### G-8 · Medium · The privacy page misses required points, and when and where it appears is unclear

**Location:** FR-66, FR-5, FR-21, FR-52
**Fix by:** v1

**Finding.** Compared with Art. 13 and Art. 14 (see Appendix B), FR-66 lacks:

- the names of the controllers, both of them;
- the legal basis for each purpose, and the legitimate interests (G-3);
- processors as recipients: hosting, email and backups;
- transfers outside the EEA, or a statement that there are none;
- whether answering is voluntary, and what happens if a guest doesn't give allergy information;
- the full list of rights (access, rectification, erasure, restriction, objection and portability), and that the couple answers within one month;
- where the data came from, both for data the couple enters and for answers given by household members (Art. 14(2)(f)).

It is also unclear when and where the page appears:

- **Where.** FR-66 links the page "from every page". But FR-5 forbids names on pages without a valid link, and the privacy page must name the controllers.
- **When.** For contact details the couple enters, guests must get the information no later than the first message the couple sends them (Art. 14(3)(b)). FR-52 doesn't mention this.

**Why it matters.** Guests have a right to this information (Art. 12–14), and their explicit consent is only informed if they can find it.

**Suggested fix.**

1. Add the missing points from Appendix B to FR-66.
2. Show the privacy page only with a valid guest link or after admin login. The page in FR-5 gets one general line saying that only technical logs are kept.
3. On the check page (FR-21), add a short note near "Send", for example: "We store your answers to plan the wedding and delete them by 31 August 2028. Read more."
4. The invitation message (FR-52) says that the link also explains how the guest's information is handled.

#### G-9 · Medium · The consent and privacy texts are only in Norwegian

**Location:** FR-26, FR-27, FR-66; NFR-6; section 1 ("a few who don't read Norwegian"); the English version, which is If time (3.3)
**Fix by:** before invitations (2027)

**Finding.** The PRD knows that some guests don't read Norwegian, but the English version is only an If-time item. These guests would give explicit consent to a text they can't read, and would get privacy information they can't understand.

**Why it matters.** Consent must be informed (Art. 4(11)), and the information must be easy to understand (Art. 12(1)). The transparency guidelines that the EDPB has endorsed (WP260 rev.01) say a translation should be provided when the controller addresses people who speak other languages.

**Suggested fix.** Before invitations go out, these texts exist in English, even if the rest of the English version stays If time:

- the consent text;
- the confirmation for others;
- the confirmation of withdrawal;
- the privacy page.

If the translation isn't ready, the couple uses FR-31 for these guests and sends them the consent text in English.

#### G-10 · Medium · Free-text fields invite health data and other sensitive data

**Location:** FR-25 (short note), FR-43 and FR-44 (questions), FR-62 (contact note)
**Fix by:** v1 (help texts and length limits)

**Finding.** FR-25 says "No diagnoses", but nothing in the form enforces it. Realistic notes include:

- a diagnosis, such as "coeliac disease";
- "pregnant, no raw fish", which may not have been announced yet;
- "no alcohol", which can reveal a pregnancy, a religion or recovery from addiction.

Other free-text fields carry the same risk:

- **Questions.** They will contain health information that the form has no place for, such as mobility on the hike or the need for a ground-floor cabin for an older guest. No consent covers these questions, the helpers can see them (G-5), and they are emailed (G-7).
- **Notes.** The couple's notes about guests can drift into opinions.

Some data is sensitive only indirectly:

- **Dietary categories.** Vegetarian, vegan and "other" (for example halal or kosher) can reveal a person's beliefs. That is acceptable, because these categories are covered by the consent.
- **Households.** Who lives in a household can reveal sexual orientation (CJEU C-184/20, *OT*). This is one more reason to keep households hidden from other guests, as section 3.4 already does.

**Why it matters.** No Art. 9 exception covers health data outside the consent, and collecting more than needed breaks data minimisation (Art. 5(1)(c)).

**Suggested fix.**

1. FR-25: limit the length of the note and add a help text: "Write what the kitchen must avoid, not why. Please don't write diagnoses or other health details."
2. FR-43: add a help text: "Please don't write health information here. Use the allergy step, or call us." The couple can delete a question once it is answered.
3. FR-62: notes are short and factual. Guests can see them if they ask (G-16).
4. If accessibility or mobility needs are wanted later, collect them with consent, like allergies, or decide to handle them by phone.

#### G-11 · Medium · Link previews and forwarded links expose the household's answers

**Location:** FR-2, FR-4, FR-7, FR-24, FR-52, FR-53; UJ-3; NFR-4
**Fix by:** v1

**Finding.** FR-4 keeps names out of page titles and link previews, but the services that make previews still download the whole page:

- according to the research, Meta's crawler downloads links sent in Messenger [R 4.1];
- email security scanners download links in emails.

The page a link opens shows the names in the household (FR-7) and, once they have answered, "the answers" (FR-24). If the couple resends a link after the guest has answered (UJ-3), the downloaded page can include the household's allergies.

A forwarded link is worse, for example one sent with "look at our invitation!". Whoever gets it sees the answers and allergies of everyone in the household. By choosing "I am …", they can also change answers or withdraw consent.

**Why it matters.** Health data must not reach third parties that the privacy page doesn't name (Art. 5(1)(f), Art. 32). The personal link works like a key: whoever has it gets in. The PRD should therefore limit what each link shows.

**Suggested fix.**

1. The page a link opens shows attendance, the total, payment and the deadline. Allergy details appear only after the guest taps to see or change the answer.
2. Known link-preview bots get the general page from FR-5. This also supports FR-3 and link tracking (C4).
3. The invitation (FR-7) and the message in FR-52 say that the link is personal and should not be forwarded.
4. If a link is forwarded anyway, FR-53 lets the couple replace it.

#### G-12 · Medium · Production security lacks HTTPS, backup rules, account removal, log rules and a breach plan

**Location:** NFR-4, NFR-1, FR-45, FR-47; D14
**Fix by:** before invitations (2027). The rule for logs applies from v1.

**Finding.** NFR-4 covers links, passwords, sessions, forged submissions and roles well, but five things are missing:

- **HTTPS on every page, with HSTS.** The link is the login, so it must never be sent without encryption.
- **Backups.**
  - Backups need encryption, storage in the EEA and a time limit (G-2).
  - If link codes are stored as plain text (D14), a copy of a backup can open every household's page.
  - The restore test (NFR-1) copies real data. It must also run in the EEA, and the copy must be deleted afterwards.
- **Admin accounts.**
  - FR-47 can create accounts but not deactivate them. A helper may need to be removed before the wedding, and all helper accounts after it.
  - Passwords need a minimum length.
  - Two-step login for the couple's accounts is worth considering.
- **Logs.**
  - The web server logs contain full addresses with link codes, and slowing down repeated attempts means storing IP addresses.
  - Application logs and error reports contain no answers, allergy data or link codes.
  - Access logs are kept for a short time, for example 14 to 30 days.
  - In production, FR-45 never falls back to writing questions to the console, so question text doesn't end up in the hosting provider's logs.
- **A plan for data breaches.** One paragraph is enough:
  - deactivate the links or accounts involved, and assess the risk;
  - notify Datatilsynet within 72 hours, unless the breach is unlikely to put guests at risk (Art. 33);
  - tell the guests if the risk is high (Art. 34). Leaked allergy data probably counts as high risk;
  - record every breach (Art. 33(5)).

  The most likely breach is sending the Hardingasete list to a mistyped email address.

**Why it matters.** Security must match the risk (Art. 32). The site holds health data about around 70 people, protected only by personal links.

**Suggested fix.** Add the points above to NFR-4. Add "deactivate an admin account" to FR-47. Put the plan for data breaches under "Before invitations go out" (3.2).

#### G-13 · Medium · The list of processors and transfers is incomplete, and guest pages may load content from third parties

**Location:** NFR-3; 3.2 "Agreements"; D16
**Fix by:** the rule against third-party requests from v1; agreements and transfers in 2027

**Finding.** Data processing agreements are planned only with the hosting and email providers. But guest data or guest traffic can also reach other services:

- backup storage;
- a DNS or CDN proxy, which sees every address, including the link codes;
- error tracking and uptime monitoring;
- later, an SMS provider (If time).

Hosting "in the EU/EEA" is not the whole story either. Data can still leave the EEA if the provider is American-owned, or if it uses subcontractors outside the EEA, for example for support or logs.

Front ends written by AI also often load fonts, icons, maps or videos from other companies' servers, which sends every guest's IP address to them. A German court awarded damages for exactly this when a site loaded Google Fonts (LG München I, 3 O 17493/20, 2022).

Finally, the PRD doesn't cover data stored on the guest's phone. The If-time envelope animation needs a "first visit" flag, and a language choice would also be stored.

**Why it matters.**

- Every processor needs a data processing agreement (Art. 28).
- Transfers outside the EEA need a legal basis for the transfer (Chapter V).
- The privacy page must list recipients and transfers (Art. 13(1)(e)–(f)).
- Norway's cookie rule (ekomloven) requires consent for storing anything on the device that isn't strictly necessary.

**Suggested fix.**

1. NFR-3 lists every service that stores or sees guest data or traffic. Each one needs a data processing agreement, and either storage in the EEA or a valid basis for transfers, such as the EU–US Data Privacy Framework or standard contractual clauses. Prefer providers based in the EEA.
2. A new NFR: guest pages load nothing from other companies' servers.
   - Fonts, icons, scripts and images are hosted on the site itself.
   - Maps and wish lists are plain links.
3. Use only cookies that are strictly necessary: the admin session, protection against forged submissions, and the guest session. The envelope flag either stores nothing on the phone, or is described on the privacy page and asks for the consent the cookie rule requires.

#### G-14 · Medium · There is no record of processing, no joint-controller note and no instructions for helpers

**Location:** NFR-3; 3.2 "Before invitations go out"
**Fix by:** before invitations (2027). The record can be written now.

**Finding.** Three required documents are missing, and one conclusion is not written down:

- **Record of processing.** Small organisations are normally exempt from keeping one. Because the site processes health data, the exemption doesn't apply (Art. 30(5)).
- **Joint-controller note.** Rikke and Valdemar decide together, so they are joint controllers. This requires a short agreement between them and one contact point that guests are told about (Art. 26).
- **Instructions for helpers.** The helpers act under the couple's authority, and should get short written instructions (Art. 29).
- **Why no impact assessment.** A full data protection impact assessment (DPIA) is probably not required at this size, for three reasons:
  - health data meets one of the nine WP248 criteria, and two are usually needed;
  - older guests are not "vulnerable" in the WP248 sense, because they are not in a weaker position than the couple;
  - the scale is small.

**Why it matters.** The couple must be able to show that they follow the rules (Art. 5(2), Art. 24). These documents are also evidence of the process for the course (criterion 1).

**Suggested fix.** Add to 3.2:

1. A one-page record of processing, built from Appendix A plus the processors and the security measures.
2. Two lines on joint control: who answers requests from guests, and who handles data breaches.
3. A short note to the helpers:
   - use the data only for the wedding;
   - take no screenshots and share nothing;
   - log out on shared devices;
   - report a lost phone.
4. A half-page risk assessment that explains why a full DPIA isn't needed.

#### G-15 · Medium · The public repo may hold real people's names, and the usability test may be recorded there

**Location:** UJ-1–UJ-3, UJ-6, FR-68 (the test data reuses the people from the journeys), SM-3, NFR-3
**Fix by:** now

**Finding.**

- **Names in the journeys.** The journeys name Bestefar Sigmund (78), bestemor, Onkel Arild, Tante Marie, Filippa, Leone and Synne. They appear alongside the couple's real names, the date and the venue. The test data, tests, screenshots and the README's test links will reuse these people, with invented allergies, absences and unpaid amounts. If they are real relatives and friends, the public repo would link invented health and payment details to people others can recognise.
- **The usability test.** SM-3 uses fictional data, but the test person is a real older relative. Notes, quotes, screenshots or recordings of them may end up in the repo as test documentation.

**Why it matters.** Invented details about a real person who can be recognised are still personal data about that person. Publishing on the open internet is not covered by the household exemption (*Lindqvist*) [R 3.1]. NFR-3 promises fictional data only.

**Suggested fix.**

1. Confirm that the names in the journeys are invented. If they are real, rename them before they spread into test data, tests and screenshots.
2. Document the usability test without names, for example as "Participant 1, 75+":
   - no names, faces or voices in the repo;
   - ask the participant before using the notes;
   - delete any recordings after the analysis.

### Low

#### G-16 · Low · Rights other than withdrawal need only small changes

**Location:** FR-49, FR-57, FR-63, FR-66; FR-40
**Fix by:** v1 for deleting a guest completely; the rest in 2027

**Finding.** The PRD handles withdrawal well, but leaves gaps for the other rights:

- **Access.** A guest can see their household's answers, but not their contact details, notes, history, questions or consent records. An access request (Art. 15) must cover all of it.
- **Rectification and objection.** In practice, FR-49 and FR-63 already cover these.
- **Erasure.** FR-49 doesn't say whether "removes" also deletes the history, questions, notes and consent records.

**Why it matters.** At this scale, handling requests by hand is enough. But the couple must answer within one month (Art. 12(3)), and a deletion that leaves traces in the history is not a real erasure (Art. 17).

**Suggested fix.**

1. FR-49: removing a guest deletes their data everywhere, including the history, questions, notes and consent records.
2. The couple can see everything stored about one guest in one place, which is enough to answer a request by hand.
3. FR-66 tells guests to contact the couple to use their rights, and says they get an answer within one month.
4. No export feature is needed, because guests already see their own allergy data through their link.

#### G-17 · Low · Small gaps in the consent text and the consent record

**Location:** FR-26, FR-29, FR-30, FR-57
**Fix by:** v1

**Finding.** The EDPB lists the minimum a consent text must contain (EDPB 05/2020, para 64). Several small points are missing:

- **Who and what.** The text names neither the controllers (Rikke and Valdemar) nor the exact data (the categories and the note).
- **New versions of the text.** Nothing says what happens to existing consents when a new version adds a recipient or a purpose.
- **Withdrawals.** A withdrawal is not recorded as an event, and the couple has no way to register a withdrawal made by phone.
- **Order in the form.** FR-26 doesn't say whether the allergy fields appear before or after the consent question.
- **The couple's view.** No requirement lets the couple see the consent records. They need them to prove consent and to act on G-1.

**Why it matters.** Consent covers only what the person was told, and the couple must be able to prove both the consent and any withdrawal (Art. 7(1), Art. 7(3)).

**Suggested fix.**

1. Name the controllers and the data in the FR-26 text.
2. Ask the consent question first, and show the allergy fields only after "Yes". After "No", nothing is sent or logged.
3. Record withdrawals: who withdrew, when, and through which link. The couple can register a withdrawal made by phone.
4. A new version of the text with new recipients or purposes needs new consent.
5. The overview (FR-57) shows each person's consent record.

#### G-18 · Low · If-time features change what data is collected and who sees it

**Location:** 3.3; the vision in the brief (a keepsake site with guests' photos)
**Fix by:** when each feature is built

**Finding.** Several If-time features change what data the site handles, or who receives it:

- **Speech sign-up** adds new data, which only the toastmaster sees.
- **Link tracking** records what guests do on the site.
- **Change notices by email or SMS** add a processor and use contact details for a new purpose.
- **The envelope animation** stores data on the guest's device.
- **The print page** creates paper copies.
- **The English version** affects consent (see G-9).

The keepsake idea in the brief, where guests share photos after the wedding, also conflicts with deleting everything by 31 August 2028.

**Why it matters.** Each of these features changes the privacy page (Art. 13) and the record of processing (Art. 30).

**Suggested fix.** Add a rule: if an If-time feature adds data, recipients, processors or storage on the guest's device, FR-66 and the record of processing are updated before the feature ships. Leave the photo keepsake out of this PRD, because it needs its own design for consent and deletion.

## What the PRD already gets right

- Consent is separate from the RSVP, which can always be sent without it (FR-28, CM-4; Art. 7(4)).
- The consent question is explicit: a Yes/No choice that starts unanswered and says "I consent to …" (FR-26).
- Guests are told how to withdraw before they consent (FR-26).
- The site records when consent was given, by whom, and which version of the text was shown (FR-29).
- Consent can be withdrawn through the same link, also after the deadline (FR-30, FR-42; Art. 7(3)).
- Allergies are limited to categories and a short note, with no diagnoses (FR-25).
- The consent text names the helpers and Hardingasete's kitchen as recipients (FR-26).
- The links are well protected (FR-1–FR-5, NFR-4):
  - link codes have at least 128 bits of randomness;
  - opening a link never changes anything;
  - page titles and previews contain no names;
  - nothing is shown without a valid link;
  - search engines are kept out, the link is not passed on to other sites, and repeated attempts with wrong links are slowed down.
- The server, not just the page, stops helpers from changing data (NFR-4).
- Only fictional data is used in the repo, the tests, screenshots, the usability test and AI tools (NFR-3).
- Production runs in the EU/EEA, with data processing agreements and a fixed deletion date (NFR-3, 3.2).

## Recorded decisions checked

| Decision | Source | Verdict |
|---|---|---|
| GDPR is assumed to apply; the household exemption is not relied on | brief, NFR-3 | The right call. Keep it documented. |
| Optional phone and email per guest, entered by the couple (Claude's proposal to store names only was rejected) | memlog | Respected. Legitimate interest covers it, because guests expect the couple to have their number. G-3 and G-8 must be done, and G-5 for what helpers see. |
| Helpers can see but not change, enforced by the server | memlog, FR-46 | Respected. G-5 questions only *what* they can see. |
| Allergies are locked after the deadline; withdrawal still works | memlog, FR-42 | Respected. G-6 adds a confirmation and a follow-up item. |
| One link per guest | memlog, FR-1 | Good for privacy (FR-53), and it makes the fix in G-1 cheap. |
| No "who's coming" list for guests | memlog, 3.4 | Right. It also avoids revealing relationships (G-10). |
| No self-service link recovery | memlog, 3.4 | Fine. It avoids sending links to addresses nobody has checked. |
| Nothing is shown without a valid link | memlog, FR-5 | Right. G-8 places the privacy page to match. |
| Deletion by 31 August 2028 | brief, NFR-3 | Fine as the final date. G-7 deletes allergy data earlier. |
| Full change history [2027] | memlog, FR-40 | Respected. G-2 limits what the history may contain. |
| Answering for others with a confirmation (C2) | pre-PRD discovery, brief | **Challenged** in G-1. |
| Verbal consent ticked by the couple | memlog, FR-31 | **Challenged and extended** in G-4. |
| Helpers see everything | memlog, FR-46 | **Challenged** in G-5. |
| Each question is emailed to the couple | brief, FR-45 | **Challenged in part** in G-7: keep the email, but leave out the question. |

## Appendix A: Suggested list of data for NFR-3

A starting point for G-3, and for the record of processing in G-14. "Legitimate interest" means Art. 6(1)(f).

| Data | Comes from | Purpose | Legal basis | Who sees it | Deleted |
|---|---|---|---|---|---|
| Name, household | The couple | Invite guests and plan the wedding | Legitimate interest | Couple; helpers (G-5) | By 31 Aug 2028 |
| Phone, email (optional) | The couple | Follow up answers and payments | Legitimate interest | Couple; helpers only if a task needs it | By 31 Aug 2028 |
| Attendance, days, meals, overnight stay, hike, arrival, who answered | Guest, household member or couple (FR-63) | Plan meals, beds and the programme; give Hardingasete the numbers | Legitimate interest | Couple, helpers; Hardingasete gets only the numbers | By 31 Aug 2028 |
| Allergies and dietary needs (categories and note) | Guest, household member (G-1) or couple (G-4) | Safe food from Hardingasete's kitchen | Explicit consent: Art. 6(1)(a) and Art. 9(2)(a) | Couple; helpers (G-5); Hardingasete's kitchen gets the name and category | When consent is withdrawn; otherwise within two weeks after the wedding (G-7) |
| Consent and withdrawal records (without the allergy information) | System | Prove consent and withdrawal (Art. 7(1)) | Legitimate interest | Couple | By 31 Aug 2028 |
| Payments, refunds, "I have paid" | Couple, guest | Settle shared costs | Legitimate interest. Contract (Art. 6(1)(b)) could also be argued; pick one. | Couple | By 31 Aug 2028, after refunds |
| Guest questions | Guest | Answer the guest | Legitimate interest | Couple | When no longer needed, at the latest by 31 Aug 2028 |
| Contact notes, change history (without the allergy information) | Couple, system | Follow up; keep answers correct and traceable | Legitimate interest | Couple | By 31 Aug 2028 |
| Admin accounts | Rikke | Control who has access | Legitimate interest | Rikke | Helper accounts after the wedding; all by 31 Aug 2028 |
| Technical logs, IP addresses used to slow down repeated attempts | System | Security (Recital 49) | Legitimate interest | Couple, hosting provider | After 14–30 days |

## Appendix B: Art. 13 and 14 checklist for FR-66

| The privacy page must state | GDPR | In FR-66 today? |
|---|---|---|
| Who the controllers are (Rikke and Valdemar, jointly) and how to contact them | 13(1)(a), 26(2) | Partly ("how to contact the couple") |
| Each purpose and its legal basis | 13(1)(c) | Partly (only one "legal basis") |
| The legitimate interests, where Art. 6(1)(f) is used | 13(1)(d) | No |
| Recipients: helpers, Hardingasete's kitchen and processors (hosting, email, backups) | 13(1)(e) | Partly (no processors) |
| Transfers outside the EEA, or a statement that there are none | 13(1)(f) | No |
| How long data is kept | 13(2)(a) | Yes |
| The rights to access, rectification, erasure, restriction, objection and portability; how to use them; an answer within one month | 13(2)(b), 12(3) | Partly ("the guest's rights") |
| The right to withdraw consent at any time | 13(2)(c) | Yes |
| The right to complain to Datatilsynet | 13(2)(d) | Yes |
| Whether giving the data is required, and what happens if not. The RSVP is voluntary; without allergy information, the kitchen won't know. | 13(2)(e) | No |
| Automated decisions (there are none) | 13(2)(f) | No (saying "none" is optional) |
| What the couple entered about the guest (name, phone, email) | 14(1)(d) | Yes |
| Where the data came from: the couple's own contacts, and household members answering for each other | 14(2)(f) | No |
| When: at the latest with the first message to the guest | 14(3)(b) | Not stated (G-8) |
