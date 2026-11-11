# Source extract for bmad-ux: AI'll handle it

Extracted 2026-11-10 from:
- `prd.md` = `.docs/planning-artifacts/prds/prd-aill-handle-it-2026-11-07/prd.md` (status final; the PRD wins where documents differ)
- `prd-add.md` = same folder, `addendum.md` (section "For UX (bmad-ux)")
- `brief.md` = `.docs/planning-artifacts/briefs/brief-aill-handle-it-2026-09-23/brief.md`
- `brief-add.md` = same folder, `addendum.md`
- `research.md` = `.docs/planning-artifacts/research/user-voice-wedding-website-pre-prd-2026-11-06/research.md`

Tags: [2027] = required before invitations, not in v1. [If time] = PRD 3.3. [T1]/[T2]/[T3] = priority tier in PRD 3.1a.

## 1. Product summary and roles

A wedding website that **is** the invitation, for Rikke and Valdemar's wedding on Saturday 27 May 2028 at Hardingasete in Hardanger (weekend Fri 26 to Sun 28 May). About 70 guests each get a personal link; a household answers together (attendance, days, meals, cabin, allergies, arrival, hike), sees prices, the household total and how to pay, and can ask the couple questions. The couple and helpers get one admin overview replacing Excel. The site has no AI features. (prd.md §1; brief.md Executive Summary)

Rikke's top priority: "it must work" — never resend an invitation by hand because the site failed; simple for guests; answers easy to read and trust (prd.md §1 "What matters most").

| Role | Who | Can do | Source |
|---|---|---|---|
| Guest | ~70, all ages, many older and not used to tech, a few non-Norwegian readers; most want only practical details | Open own link (link = login), read invitation and info pages, answer for the whole household, see total, pay outside the site, report "I have paid", ask a question, withdraw allergy consent | prd.md §1, FR-1, FR-2, FR-35, FR-43, FR-30 |
| Household | Couple or family; each person has own link; any one answers for everyone | Respondent switches "I am [name]"; no "answer for myself only" | FR-12; prd.md §3.4 |
| Couple (admin) | Rikke and Valdemar | Change everything: guest list, answers (also after deadline, same form), payments, settings, consent registration | FR-46, FR-49, FR-59, FR-63, FR-64, FR-31 |
| Helpers | Toastmaster, maid of honour, best man | See everything (incl. contact details, questions, payments), change nothing; server enforces | FR-46, NFR-4; prd-add.md rejected "Hiding questions and payments from helpers" |
| Examiner | Ingrid (fictional) | Runs v1 locally via README with test links and test admin/helper | UJ-6, FR-68 |
| Hardingasete | Venue | Not a user; receives numbers by email from the couple | prd.md §3.4 |

Admin accounts created by command, no self-registration (FR-47). Guests have no accounts/passwords (prd.md §3.4).

## 2. Form factor, devices, browsers, language

Stated:
- **Phone first, for all ages.** A PC shows the phone layout; wider PC layout is [If time] (NFR-6, prd.md §3.3; brief.md Scope "Also works ... on a PC, using the phone layout").
- Works at 200 % zoom and 320 px width (NFR-5).
- Admin: quick tasks (find guest, copy link, see if answered) must work well on a phone; the full overview also works on a phone "but may be designed for a PC" (FR-48; UJ-3 step 2 Rikke on her phone). Basic responsive admin is [T3] beyond "basic responsive pages" (prd.md §3.1a).
- Examiner tests in "a narrow window, like a phone" on an ordinary PC (UJ-6 step 4).
- Production device floor [2027]: must work on older guests' actual phones/tablets **including Messenger's and Facebook's in-app browsers**, checked on a real old device; "The invitation text and the RSVP button appear even if the animation or scripts fail" (prd.md §3.2 Going live).
- Links arrive via SMS, Messenger and email; tested on Android and iPhone (NFR-1).
- Pages < 3 s on an ordinary phone on 4G (NFR-7).
- Guest pages load nothing (fonts, scripts) from other companies [2027 privacy in operation] (prd.md §3.2) — affects font choice.

Language:
- **Norwegian (bokmål)**, "plain, warm ... with a cosy tone, also in error messages" (NFR-6). Quoted UI texts in the PRD are English working labels; the UX phase sets final wording (prd.md header note; prd-add.md "Still to settle").
- English version with a language button is [If time] (prd.md §3.3). Until then non-Norwegian guests ask the couple directly (brief.md Scope; brief-add.md Later decisions).
- All times Norwegian time (FR-41). Amounts whole kroner (NFR-2).

Not stated: specific browser versions; tablet layout; dark mode; admin text size/target size (NFR-5 sizes are "on guest pages"); landscape; print styles (print page is [If time]); how the language button looks (research says no flags, see §8).

## 3. User journeys (verbatim names)

**UJ-1: Bestefar Sigmund answers for himself and bestemor** — Sigmund, 78, not used to tech, opens SMS link on phone.
1. First impression: invitation (Rikke and Valdemar, Sat 27 May 2028, Hardingasete, "he and bestemor" invited); RSVP deadline, child-free note, clear RSVP button visible without scrolling. (If time: green envelope sealed "R & V" opens on first visit.)
2. Scrolls: short cards for programme, practical info, Hardingasete and the area, about the couple; each opens its own page via "Read more"; RSVP button repeated at bottom.
3. Starts answer: "I am Sigmund" preset, changeable. Marks who is coming (both); both whole weekend; meals and overnight with prices shown before choosing; "Read more" box opens inside the step; leaving before sending warns answer not sent.
4. Allergies (optional): "No allergies or dietary needs" for himself; fills bestemor's, says yes to consent, confirms she knows and agrees.
5. Check page says at top answer not sent yet; all answers + household total; changes; presses "Send answer".
6. Thank-you matching answer (coming / not coming texts).
7. Payment: Pay now (amount, Vipps number, QR if time, account number, payment message "Bryllup" + both names; taps "I have paid", checks amount and method, sees what/when reported) or Pay later (same link always shows what he owes).
8. "You can now safely close the invitation."
Done when he knows answer is sent, what he owes, and that the link shows it again. **Biggest risk: too much at once; every screen must have one obvious next step.**

**UJ-2: Onkel Arild answers for a household where not everyone comes** — Arild for himself, tante Marie, Filippa, Leone (adult daughters).
1. "I am Arild"; Arild, Marie, Filippa coming, Leone not; nothing pre-ticked. "Whole weekend?" → "No"; Filippa Sat+Sun.
2. Form adapts: nothing more about Leone; Filippa only offered meals on her days; Sat breakfast only for Friday arrivals; Sat lunch/dinner not asked (couple pays); accommodation step says cabin is booked for whole weekend, Filippa pays both nights; total matches.
3. Checks, sends, pays as UJ-1.
4. Two weeks later: button is "See or change answer"; top of form shows what was answered, by whom, when; changes. Total up → sees what remains to pay; down → told couple notified and will refund.
5. Marie opens her link: sees Arild already answered and when, not an empty form; if she had opened first, she'd see his answer before sending hers. No silent overwrite.
6. After deadline: form locked, contact couple.
Couple sees household "Changed" (2027: full history); registers refund → balance zero.

**UJ-3: Synne has lost her link and needs a change after the deadline** — friend, new phone.
1. Messages Rikke/Valdemar. 2. Rikke finds Synne in admin on her phone, copies link, resends. 3. If link went astray: deactivate + create new (only that guest); old link shows only "private invitation, contact the couple the way you usually do", no names/phones/answers. 4. After deadline button says "See answer"; can view not change; told deadline passed + how to reach couple; can still see how to pay, "I have paid", info pages, ask a question, withdraw consent. 5. Rikke fills/changes answer in admin using the guest form; phone-reported allergy → Rikke sends consent text by message, registers consent on yes; site records who, how, when. 6. On errors Synne still sees how to reach the couple; phone numbers on every guest page.

**UJ-4: Rikke checks the numbers and sends them to Hardingasete** — after deadline.
1. Logs in → summary (FR-54): coming/not/not answered (people, households); guests per day; overnight (beds); per meal and per allergy category; coming guests with nothing registered for allergies; payment status counts; hike interest; arrivals.
2. Directly below "Needs attention" (FR-56); marks items handled/seen. (2027: invitation not marked sent, households not started, FR-77.)
3. Trusts numbers: every count opens the people ("12 for Friday dinner" → who); full overview to count herself.
4. "Not answered" with names and contact details; contacts them herself. (2027: dated note.)
5. Types numbers into email to Hardingasete (If time: print page). Cabin allocation outside site.
Helpers log in, same overview, cannot change.

**UJ-5: Rikke follows up payments** — checks Vipps/bank; payment message identifies household; registers "Received 900 kr"; site computes status (nothing to pay / not paid / part paid (X missing) / paid / refund owed (X)), only admins see it; "I have paid" with lower received amount → household **marked red** + Needs attention; reminders by message herself (2027: dated note).

**UJ-6: Ingrid, the examiner, runs the app** — clones, README, installs, seeds fictional guests (journey people + expected-results households), README lists test link per guest and test admin/helper logins; opens guest link in narrow window, full RSVP, tries wrong input, checks receipt; logs in as admin, summary matches expected-results list; moves deadline to yesterday in admin settings (guest locked, admin can still edit); sends a question (shows in admin + terminal); runs tests with one command. Done within 15–20 min without help.

## 4. Surfaces implied by requirements

### Guest side
| # | Surface | Requirement IDs |
|---|---|---|
| G1 | **No valid link page** (unknown/deactivated link, bare domain): friendly private-invitation message, no names, phones, date or place | FR-5, UJ-3 |
| G2 | **Invitation / front page**: names, date, place, invited household names, child-free, deadline (weekday, date, time), RSVP button above the fold; cards; RSVP repeated at bottom; household status block once answered; button state "RSVP" / "See or change answer" / "See answer"; contact details; "Ask us"; privacy link in footer | FR-6, FR-7, FR-8, FR-24, FR-37, FR-41, FR-42, FR-43, FR-66; prd-add.md Front page structure |
| G3 | **Info pages**: Programme (day by day, cost markers, what to bring, all activities incl. Friday hike; treasure hunt/sauna/yoga info only), Practical information (address, times, transport, parking, dress codes, house rules, what to bring), Hardingasete and the area, About us; each with obvious way back | FR-8, FR-9, FR-10, FR-11; FR-9/FR-10 full text is [T2] |
| G3b | Gifts page (simple text, links) | [If time] prd.md §3.3; prd-add.md |
| G4 | **RSVP form, stepped** with progress indicator and Back: respondent "I am …"; step 1 who is coming; step 2 whole weekend? → per-person days; then (order set by UX) meals, overnight, hike (Friday attendees only), arrival (optional fixed choices incl. "Don't know"), allergies + consent; running total; in-step "Read more"; leave warning; inline errors + error summary; contradiction blocking | FR-12–FR-20, FR-22, FR-25–FR-28, FR-32, FR-33, FR-70, FR-73, FR-75; D9 |
| G4b | **"Last updated by X at Y" header** and **conflict notice** (someone else sent after you opened: who, when, what differs) | FR-38, UJ-2 steps 4–5 |
| G5 | **Check page**: "not sent yet" at top, per-person answers, total, "Change" per part, "Not provided", button "Send answer"; allergy-without-consent warning | FR-21, FR-28, FR-33 |
| G6 | **Receipt**: coming / not coming message; then Pay now / Pay later choice (if something to pay); then "You can now safely close the invitation" | FR-23, FR-34; prd-add.md receipt wording |
| G7 | **Payment details** (Pay now): amount, Vipps number (QR [If time]), account number, payment message | FR-34, FR-71 |
| G8 | **"I have paid" report**: amount (prefilled), method Vipps/bank, who paid if someone else; afterwards shows report + time, correctable; remaining / refund notice after total change | FR-35, FR-36 |
| G9 | **Locked view** after deadline ("See answer"): read-only answers, explanation, couple contacts; payment, "I have paid", info, questions, consent withdrawal still work; also for never-answered households | FR-42, SM-11 |
| G10 | **"Ask us" form** on every guest page: short question; says Rikke, Valdemar and helpers can read it; no health info | FR-43 |
| G11 | **Consent withdrawal** via personal link (also after deadline); deletes allergy info, marks "Changed" | FR-30 (placement not specified) |
| G12 | **Privacy page**, linked from every page footer and the consent question | FR-66 |
| G13 | Envelope animation (skippable, reduce-motion, first visit only) | [If time] prd.md §3.3; prd-add.md Invitation reveal; brief-add.md |
| G14 | Speech sign-up reaching toastmaster | [If time] prd.md §3.3 |
| G15 | Language button (English) | [If time] prd.md §3.3 |
| — | Restore unsent answer on return | FR-78 [2027] |

### Admin side
| # | Surface | Requirement IDs |
|---|---|---|
| A1 | **Login** (username + password); session expiry; login rate limiting | FR-46, NFR-4 |
| A2 | **Admin home**: summary (FR-54 list) + "Needs attention" below with handled/seen actions | FR-54, FR-56; prd-add.md Needs attention table |
| A3 | **Count drill-down lists** (every count opens the people) | FR-55 |
| A4 | **Full overview**: every household/person, answers, contact (tap to call/write on phone), total, payment status, notes; unanswered stand out; mismatch red; "Changed" marker | FR-57, FR-39, FR-61 |
| A5 | **Allergy list** (names + categories, consented only) | FR-58 |
| A6 | **Guest list**: add/edit/remove households and guests (name, optional phone, email); search by name; copy link; contact details | FR-49, FR-51 |
| A6b | Move guest between households | FR-50 [T3] |
| A6c | Deactivate link + create new | FR-53 [T3] |
| A6d | Copy ready-to-send invitation message | FR-52 [2027] |
| A6e | Record invitation sent (date, channel), resends with reason | FR-76 [2027] |
| A7 | **Household edit via the guest form** (admin as author, also after deadline) | FR-63 |
| A8 | **Consent registration by couple** (who, channel, text version, when) | FR-31 [T3] |
| A9 | **Payments**: register received amounts and refunds; correct/undo; computed status | FR-59, FR-60, FR-61 |
| A10 | **Payment message edit** + duplicate warning | FR-71 |
| A11 | **Questions**: listed under Needs attention, mark answered | FR-44 |
| A12 | **Settings**: prices, deadline, contact details, Vipps and account number; couple only; deadline confirmation in words + lock-out count; price-change warning | FR-64, FR-65 [T3] |
| A13 | Household contact note (dated) | FR-62 [2027] |
| A14 | Change history | FR-40 [2027] |
| A15 | Delete all guest data with clear confirmation | FR-67 [2027] |
| A16 | Print page for Hardingasete | [If time] |
| — | Terminal: question printed when no email key; admin account command; seed command | FR-45, FR-47, FR-68 |

## 5. Behavioural requirements relevant to UX

**Access / login model**
- Link = only guest login; long random code; opens household only (FR-1, FR-2). Opening a link never changes anything; only deliberate actions save (FR-3). Page titles and previews identical for everyone, no names (FR-4). Invalid link → G1 (FR-5). Couple's contact details on every guest page incl. errors (FR-6). No self-service link recovery (prd.md §3.4).
- Admin username/password, two roles (FR-46); session idle expiry, login slowdown (NFR-4).
- Respondent identity via "I am [name]" preset to link owner, switchable; records who answered (FR-12). Don't ask for what the link knows (NFR-5).

**Form flow and states**
- One task per step, visible Back, progress indicator (FR-13). Nothing preselected for attendance (FR-14; prd-add.md rejected "Everyone is coming" ticked).
- Conditional questions (FR-15, FR-17); removed choices disappear from totals (FR-75); contradictions blocked with explanation, e.g. overnight while present only one day (FR-70). Each day shown with its date and what happens (FR-70).
- Cabin = whole weekend, both nights paid, stated clearly (FR-16). No bed limit (prd.md §7 Q1).
- Errors next to field with fix hint; error summary at top after failed continue, linking to fields (FR-22).
- Leave warning before sending (FR-20); v1 only; restoring draft is [2027] (FR-78).
- Save: succeeds and says so, or fails with clear message and keeps entered data (NFR-1).
- Conflict: show other sender's answer (who, when, what differs) before sending (FR-38).
- Success/receipt: FR-23 texts; status block on invitation afterwards (FR-24).
- Loading states: not specified beyond NFR-7 (<3 s). Empty states: not specified (see §10).

**Consent / GDPR**
- Allergies optional; per coming person either categories (gluten, lactose, nuts, shellfish, vegetarian, vegan, other) + short note, or "No allergies or dietary needs"; no diagnoses (FR-25).
- Separate Yes/No consent, starts unanswered, "I consent to …"; text covers purpose, who sees it (couple, toastmaster, maid of honour, best man), names+allergies go to Hardingasete's kitchen, withdrawable via same link (FR-26). Withdrawal info must come **before** consent (research.md §3.2, EDPB para 116).
- Confirm others know and agree when entering for others (FR-27).
- RSVP always sendable without consent; if allergies entered without consent, plain warning before sending that they won't be saved and guest can tell couple directly (FR-28). CM-4: consent is never pushed, nothing pre-ticked.
- Consent stored per person with time, giver, text version (FR-29). Withdraw anytime incl. after deadline → deletes allergy info, marks "Changed" (FR-30).
- "Ask us" warns not to write health info (FR-43). Privacy page content per FR-66.

**Prices, totals, payments (guest)**
- Price of each paid option shown before choosing: cabin (whole weekend), Friday dinner, Saturday breakfast, Sunday breakfast; friendly note why guests pay (Hardingasete's prices; couple pays Sat lunch+dinner) (FR-32).
- Household total visible along the way, identical on check page and receipt, always computed (FR-33, NFR-2).
- After sending, if something to pay: "Pay now" / "Pay later" (FR-34). Nothing to pay → closing line straight away (FR-23).
- Payment message "Bryllup" + all household names; couple can adjust; duplicate warning (FR-71). No numeric household code (prd.md §3.4).
- "I have paid": amount prefilled, method Vipps/bank, who paid if someone else; shows what/when; correctable (FR-35). After total change: remaining, or "couple told and will refund" (FR-36).
- Guests never see the couple's payment registrations/status (prd.md §3.4; FR-60).
- No online payment, no Vipps payment requests (prd.md §3.4). No tax/Vipps claims on site beyond number/QR (research.md §6 rec. 14).

**Deadline and lock**
- Deadline = a date, until 23:59 Norwegian time; shown with weekday, date and time next to the RSVP button and in household status (FR-41).
- Before deadline after answering: "See or change answer" opens prefilled form (FR-37). After: "See answer", read-only, explanation + contacts; listed functions still work; same for never-answered (FR-42). No grace period (prd.md §3.4).
- Admin can override any time with the same form (FR-63).

**Admin behaviour**
- Summary, drill-down, Needs attention leave rules (prd-add.md table): not answered → answers or handled; nothing registered for allergies → registered or handled; question → marked answered; mismatch (red) → matching amount or handled; refund owed → refund registered; "Changed" → marked seen.
- "Changed" marker rules: changed sent answer or consent withdrawn; first answer and "I have paid" don't count (FR-39).
- Payment status wording (prd-add.md): Nothing to pay / Not paid / Part paid, X kr missing / Paid / Refund owed, X kr (first matching row).
- Mismatch: received minus refunds < reported → red + Needs attention (FR-61).
- Payment registration correctable/undoable (FR-59) — the only explicit undo.
- **Confirmations specified**: deadline change (repeat new deadline in words + confirm; past or within two weeks shows number of households locked out) (FR-64); price change warning with affected household count (FR-65, T3); delete all data clear confirmation (FR-67, 2027); duplicate payment message warning (FR-71).
- Helpers: server blocks changes (NFR-4); UI treatment unspecified.

**Notifications**
- Questions always stored + Needs attention; emailed to couple if key set, else printed to terminal (FR-44, FR-45, SM-12).
- Out: site sending invitations/reminders, change emails to couple, change notices to guests, sending to Hardingasete (prd.md §3.4).

## 6. Accessibility, performance, privacy NFRs touching the UI

- NFR-5 (self-imposed WCAG 2.2 AA): contrast ≥ 4.5:1; guest body text ≥ 18 px; 200 % zoom and 320 px; full keyboard with always-visible focus; guest touch targets ≥ 44×44 px; every field labelled, errors per FR-22; don't ask what the link knows; animation respects reduce-motion and is skippable.
- Check sage green on soft white meets 4.5:1 (prd-add.md Look and feel; research.md §3.5 table).
- research.md §3.5 criteria: 1.4.3, 1.4.4/1.4.10, 2.4.7/2.4.11 (focus not obscured), 2.5.8, 3.3.1–3.3.3, 3.3.7, 3.3.8. Designsystemet error summary pattern (heading «For å gå videre må du rette opp følgende feil.», focus moves there, each error links).
- NFR-6: phone first; one obvious next step per screen; SM-3 older guest under 10 min without help, no wrong answers.
- NFR-7: < 3 s on 4G; ~70 guests, ~5 admins.
- NFR-1: links short and link-safe for SMS/Messenger/email.
- NFR-4: guest pages noindex, no referrer passing; guest answers visible only to logged-in admins and own household.
- NFR-3: only fictional data in repo, screenshots, usability test and AI tools — design mockups must use fictional names (only Rikke and Valdemar are real).
- prd.md §3.2: no third-party fonts/scripts on guest pages [2027]; static invitation + RSVP button must render without JS/animation [2027].
- Privacy page linked from every page and from consent (FR-66).

## 7. Content, voice, wording

- "Plain, warm Norwegian (bokmål) with a cosy tone, also in error messages" (NFR-6); "Warm and 'koselig' throughout, including error messages" (prd-add.md Tone).
- Look: "The couple's own look, not a template"; palette sage green, soft white, dark wood; "Elegant but cosy, not overly fancy" (prd-add.md; brief-add.md; brief.md What Makes This Different).
- Envelope: green, wax-style stamp "R & V"; unfolds into invitation that **is** the website; afterwards no folds or sheet edges, same visual style; guest should feel invited to scroll (prd-add.md Invitation reveal).
- Receipt wording, Rikke's originals (prd-add.md):
  - Coming: «Tusen takk for at du tok deg tiden til å svare, vi gleder oss til å feire den store dagen med deg/dere»
  - Not coming: «Så leit at du/dere ikke har mulighet til å delta, men dette har vi full forståelse for.»
  - End: «Du kan nå trygt lukke siden/invitasjonen»
- Why-guests-pay note: short, friendly; Hardingasete's prices; couple pays Sat lunch and dinner (FR-32). Final wording waits for Q7 (prd.md §8).
- Gift page message: "we know the wedding may be expensive to attend and we don't expect gifts, but there is a wish list for anyone who wants one" — balances asking guests to pay (prd-add.md; brief-add.md).
- Invitation message (FR-52, 2027): warmer than Claude's first example ("Hei Sigmund! Her er invitasjonen til bryllupet vårt: [lenke]"), must include first name (prd-add.md).
- Invalid link: "this is a private invitation, and the visitor should contact the couple the way they usually do" (FR-5).
- English working labels to be translated: "Send answer", "See or change answer", "See answer", "I am [name]", "Coming"/"Not coming", "No allergies or dietary needs", "Not provided", "Change", "Pay now"/"Pay later", "I have paid", "Ask us", "Read more", "Needs attention", "Changed", "Don't know" (FR-12–FR-43).
- House rules content: child-free, little phone use (FR-10; brief-add.md).
- Programme content (prd-add.md): Fri daytime mountain hike for early arrivals; evening treasure hunt (rebus), sauna and hot tub, Friday dinner (paid). Sat breakfast (paid), optional yoga, wedding, couple hosts lunch and dinner. Sun breakfast (paid). Guests encouraged to stay whole weekend but may come without staying overnight.
- Info page text lives in code in v1 (D12; prd.md §5.12 note).

## 8. Research findings relevant to UX (research.md)

- **Name search is the #1 RSVP failure** (exact match, lockout, strangers) → personal link avoids it (§1.1, §2.1).
- Store per person, answer per household; tri-state attendance gives "not answered" list (§1.2).
- Joy: deadline shown next to RSVP button; after deadline button replaced with custom message (§1.3). No product says whether guests lock while couple can edit — designed by us.
- Admin dashboards: meal totals, not-answered list, missing meal choice (§1.4).
- **No wedding product shows guests what they owe**; borrow from GOV.UK check answers (title says what to do, "nothing complete until confirmed", "Change" per item with hidden SR text, button named after action, "Not provided"), Baymard (users fix errors at review; confuse review with confirmation; **unexpected total change at review breaks trust**), GOV.UK confirmation (reference, what happens next, contacts, keep a record; users bookmark it), Tito "Mark as paid" (§1.5, §1.7).
- Couples: chasing replies is the core pain; Norwegian norm: friendly phone call to non-responders (§2.1).
- Joy praised for easy RSVP and less stressful lists; Zola 1.2/5 for fees/support (§2.1).
- Guest payment: accommodation broadly accepted if optional and disclosed up front; paying for meals often called "tacky", "nickel and dimed"; "nobody wants to feel like they have to purchase their spot" (§2.1, §2.2). Klikk.no: "guests must pay in the bar" annoys guests (§1.6). Norwegian meal norms unknown.
- Helpers: platforms give every user full edit; couples shared logins → limited roles is a gap (§2.1).
- **Guests ask anyway** even when info is on site; many never open it; digital link helps; guests lose the card (§2.2).
- **Two kinds of guests:** half want only logistics (times, dress code, RSVP, gifts — "Just the important info I need"), half read everything incl. couple's story (§2.2).
- **Older guests:** most manage, some can't; half of couples used a hybrid (paper/phone) (§2.2). NN/g 65+: more mistakes, blame themselves, miss vague errors; small text/buttons and strict formats (date pickers, hyphenated numbers) cause errors; use forgiving input, errors at field, larger targets (§2.2).
- GOV.UK: one question per page, visible Back link, "Continue" button (§2.2).
- Language switcher: prominent is found faster; no flags (§2.2).
- Invitations "clear for the most senior generation"; **no evidence on older guests and animated envelopes** — prototype test suggested (§2.2, §7).
- JTBD (§2.3): guest wants to see immediately who in household is invited and what to do by when; avoid name search, tick each person, know it got through; know cost before committing; older guest wants large text, clear way back, a person to call; near the date: times, address, parking, dress code, what to bring, quickly.
- Link previews cached by Messenger/WhatsApp → no names in title/og tags; scanners open links → "opened" ≠ started (§4.1).
- Insight 4 (§5): structured choices (fixed arrival/allergy options, check page, receipt) lower guest errors and give countable admin data.
- Caveat: user voice mostly US and partly old (§Executive summary, §9 staleness: NN/g 2019, etiquette 2021–23 "use with caution").

## 9. Open decisions explicitly deferred to UX

1. Final Norwegian wording of every interface text; PRD labels are English working labels (prd.md header; prd-add.md "Still to settle").
2. Order of form steps after the first two (FR-13, FR-14; prd-add.md).
3. Wording explaining why guests pay, after Q7 is answered (FR-32; prd.md §8 Q7 "Before the UX text is written").
4. Exact invitation message for sending links, warmer, with first name (FR-52 [2027]; prd-add.md).
5. Number of weeks before a not-started household appears in Needs attention, and when the two FR-77 items leave the list (FR-77 [2027]; prd-add.md).
6. Final receipt texts, starting from Rikke's wording (prd-add.md FR-23 section).
7. Carry the full look and programme from the brief: palette, contrast check of sage green on soft white, envelope reveal spec (prd-add.md "the UX work must carry them in full").
Not UX (architecture): D12 info pages editable in admin, D14 link codes hashed vs plain (affects whether admin can copy an existing link, FR-51), D15 stack; D16 email provider (Rikke, 2027) (prd.md §8; prd-add.md For architecture).
Implicitly left open (not assigned to anyone, UX should settle): see §10 gaps marked (UX).

## 10. Contradictions and gaps

Superseded brief/research positions (PRD wins; make sure UX follows the PRD):
- Link per household (research.md §5, rec. 3; brief-add.md "opened their link") vs one link per guest (FR-1, FR-12; prd.md §9).
- Consent required to send (brief-add.md struck-through) vs always sendable (FR-28).
- Last save wins (brief.md Scope, brief-add.md C5) vs later sender sees other answer first (FR-38).
- Payment "paid/undo, paid X now owes Y" (brief.md) vs amount-based five statuses (FR-59, FR-60).
- All admins full access (brief.md, brief-add.md) vs helpers read-only (FR-46).
- Link tracking "opened" (brief-add.md) vs "started" [2027] (FR-77, C4). Change notifications to guests: If time in brief → Out in PRD.
- Brief: deadline shown "on the receipt page"; PRD: next to RSVP button and in household status (FR-41). Brief: "receipt page that the personal link always opens"; PRD instead puts a status block on the invitation (FR-24). (UX) decide whether the receipt is a persistent page or only the status block.

Gaps (UX should decide or flag):
- (UX) «deg/dere», «du/dere», «siden/invitasjonen» in Rikke's wording need a rule (household size? number coming? single-person household?).
- (UX) Where consent withdrawal lives on the guest side (FR-30 has no surface).
- (UX) Empty states not specified: empty Needs attention, no questions, no payments, household with nothing to pay, zero counts in drill-downs.
- (UX) Loading/saving states not specified beyond NFR-1 and NFR-7; double-submit handling on "Send answer" / "I have paid".
- (UX) Destructive admin actions without stated confirmation: remove guest/household (FR-49), deactivate link (FR-53), mark Needs attention items handled (undo?), withdraw consent (deletes data, FR-30). Only FR-59 has explicit undo.
- (UX) "Marked red" (FR-61, UJ-5) must not rely on colour alone (WCAG 1.4.1 not cited in NFR-5).
- (UX) Helper read-only UI: hide vs disable edit controls; whether helpers see the Settings page.
- (UX) Admin text and target sizes: NFR-5 sizes apply only to guest pages; FR-48 says admin may be PC-designed but used on phone.
- (UX) Session-expiry experience for admins mid-edit (NFR-4) and saving (NFR-1).
- (UX) FR-20 leave warning: browser "beforeunload" is unreliable in in-app browsers (Messenger/Facebook, prd.md §3.2) — needs an in-page fallback.
- (UX) "I am [name]" switch: what happens to answers already filled if respondent changes mid-form; whether it affects "Ask us" sender.
- (UX) After-deadline view for a household that never answered (FR-42 "same message") — what content, any payment?
- (UX) Hike question for "maybe": how counted in summary (FR-54 "interest").
- (UX) Arrival fixed choices not listed anywhere (FR-18 only says fixed + "Don't know").
- (UX) Programme times/dates per day and dress codes not given in any source; content placeholders needed.
- (UX) Where unanswered questions are read in full (FR-44 only says listed in Needs attention); no dedicated questions list surface.
- (UX) Non-Norwegian guests in v1: no English; only "ask the couple directly" (brief.md) — maybe a one-line English hint? not decided.
- Tension: FR-78 [2027] keeps unsent answers (possibly allergies = health data) on the guest's device; not discussed against NFR-3.
- Tension: FR-6 contact details on every guest page vs FR-5 none on no-link page — consistent by design (prd-add.md rejected alternative), but UJ-3 step 6 "every guest page" must be read as valid-link pages only.
- Tension: UJ-1 step 3 lists "meals and whether they stay overnight" together; FR-13 leaves order open; FR-73 says meals do not depend on overnight stay.
- Tension: gift card in front page structure (prd-add.md) is If time; FR-8 lists four cards only.
- Research is mostly US and old; Norwegian norms on paying for meals unknown (research.md §2.2, §7; Q7 open).
