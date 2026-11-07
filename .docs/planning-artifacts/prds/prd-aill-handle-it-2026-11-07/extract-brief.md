# Extract from Product Brief (for PRD)

Sources (all in `.docs/planning-artifacts/briefs/brief-aill-handle-it-2026-09-23/`):
- `brief.md` (status: final, created 2026-09-23, updated 2026-11-06) — abbreviated **B**
- `addendum.md` — abbreviated **A**
- `tilbakemelding-product-brief.md` (teacher feedback, 2026-10-06, on brief commit `ee25e52`, Norwegian) — abbreviated **T**

## 1. Product summary & vision

- Name: **AI'll handle it**. A wedding website that is also the invitation (B: Executive Summary).
- Wedding: Rikke's wedding weekend at **Hardingasete, Hardanger**; wedding day **Saturday 27 May 2028** (B: Exec Summary; A: Weekend programme).
- ~**70 guests**, each with a **personal link**; households answer together in one form (attendance, meals, cabin beds, allergies, arrival); guests see cost per option, tick options, see household total and how to pay, can send questions to the couple (B: Exec Summary).
- Replaces: photo invitation over Messenger, free-text replies, Excel sheet (B: Exec Summary, The Problem).
- Couple gets one admin overview: attendance, meal counts, beds, allergies, payments, guest questions (B: Exec Summary).
- Course project: Rikke's **solo full-stack** project for **IBE160 Programmering med KI, Høgskolen i Molde**, due **mid-December 2026**. Name refers to building with AI as development partner; **the site has no AI features** (B: Exec Summary).
- Goal: finished site at course delivery Dec 2026. Scope split: Must (by Dec 2026) vs If time and capacity allow (by Dec 2026 if possible, else before invitations go out ~**December 2027**). Course version runs **locally with fictional test guests**; hosting and real data in **2027** (B: Exec Summary).
- Vision: great weekend, stress-free run-up; guests arrive knowing what to expect, having answered once; couple plans the celebration instead of chasing replies (B: Vision).
- After course: production during 2027, online until wedding May 2028; **couple owns hosting and its cost** (B: Vision).
- Possible post-wedding keepsake: guests share photos, couple posts thank-you, if time allows (B: Vision; A: Later decisions).
- Differentiator vs Joy, Zola, The Knot: fit, not technology — households answer together; three-day weekend with paid add-ons paid by bank transfer/Vipps; invitation that feels like one (letter unfold, if time); Norwegian first with own look (B: What Makes This Different).
- Look and feel: elegant but cosy, not overly fancy; palette **sage green, soft white, dark wood**, not a template (A: Look and feel; B: What Makes This Different).

## 2. Users / roles

- **Guests**: about **70**, all ages; some confident on phones, some not; many older and not used to technology; a few may not speak Norwegian. Need to understand the weekend, answer once, know what they owe. Success: never ask the couple something the site already answers (B: Who This Serves; A: Guests).
- **Households**: a couple or a family; each guest has a personal link; one member (e.g. father of a family) answers for all; person answering first chooses who they are from household names (B: The Solution, Scope; A: Invitation experience).
- **The couple (Rikke and partner)**: need trustworthy numbers for Hardingasete; stop chasing replies; one screen replaces Excel, message threads, double-checking. Pass numbers on to Hardingasete themselves (B: Who This Serves, The Solution).
- **Helpers: toastmaster, maid of honour, best man**: share the admin view; **all admin users get full access** (B: Who This Serves, Scope; A: Admin).
- **Toastmaster**: receives speech sign-ups (if-time feature) (B: Scope; A: Admin).
- **Venue Hardingasete**: provides venue, all meals and cabin accommodation; receives numbers from the couple (not from the site) (A: Weekend programme; B: Scope Out).
- **Examiner (sensor)**: runs app locally on a PC via README with seed data, test links, test admin (B: Change Log 2026-10-23 review; T: section 2).
- **Usability test participant**: older relative not comfortable with technology (B: Success Criteria).

Event facts (A: Weekend programme; B: Solution):
- **Friday**: mountain hike during the day for early arrivals; evening treasure hunt (rebus), then sauna and hot tub; Friday dinner (paid).
- **Saturday 27 May 2028**: optional yoga, then the wedding; couple hosts lunch and dinner (free for guests); Saturday breakfast (paid).
- **Sunday**: Sunday breakfast (paid).
- Accommodation: cabins on the farmyard at Hardingasete, whole weekend or nothing.
- Guests encouraged to stay the whole weekend; can come without staying overnight (e.g. only the wedding day).

## 3. Capabilities / features

Must (by mid-December 2026):
- Admin creates guests and households and gets each guest's personal link (B: Scope Must; A: Admin).
- Personal link per guest; link is the login; long random hard-to-guess token; shows only that guest's household (B: Scope Must, Scope Out, Data and Privacy).
- Information pages: weekend programme, practical info (address, times, dress codes, transport), about the couple, house rules (child-free, minimal phone use). Kept simple (B: Scope Must, The Solution; A: Content pages).
- RSVP per guest in household, filled by any one member who first chooses who they are (B: Scope Must; C6 in A: Decisions after research).
- RSVP field: attendance and which days per person (Friday, Saturday, Sunday) (B: Scope Must; Change Log D1–D11).
- RSVP field: paid options per person — accommodation whole weekend, Friday dinner, Saturday breakfast, Sunday breakfast — price shown next to each before choosing, with short note why guests pay (B: Scope Must, The Solution; A: Paid options).
- Meals chosen independently of accommodation (B: Scope Must).
- RSVP field: allergies — optional categories plus short note, consent-gated (B: Scope Must, Data and Privacy).
- RSVP field: expected arrival — optional fixed choices including "Don't know" (B: Scope Must).
- RSVP field: Friday hike (yes/no/maybe) (B: Scope Must; A: RSVP rules).
- Step-by-step form, check-answers page before sending, receipt page afterwards that the personal link always opens (B: Scope Must).
- Household total and bank/Vipps payment details; total does not change unexpectedly between form and summary (B: Scope Must).
- Payment message shows only that payment is for the wedding (no household code) (B: Solution; Change Log D1–D11).
- Lock at RSVP deadline; deadline shown next to the button and on receipt page; after deadline guests see message with couple's contact details (B: Scope Must; A: RSVP rules).
- Concurrent household edits: last save wins; form shows who last updated and when before anyone starts editing (B: Scope Must; C5).
- Consent flow for allergies (see Business rules) incl. withdrawal through same link, deleting allergy info (B: Scope Must, Data and Privacy).
- Admin login (B: Scope Must).
- Admin overview: who is coming and who hasn't answered, meal counts per meal, beds needed, allergies by name, what each household owes and whether paid, guest questions (B: The Solution, Scope Must).
- Admin overview also (A only): expected arrival time per guest, Friday hike interest, speech sign-ups (A: Admin).
- Mark households paid, with undo; show "paid X, now owes Y" if total changes afterwards (B: Scope Must; D1–D11).
- Admin editing and overrides: edit answers (also after lock), move people between households, remove a guest (B: The Solution, Scope Must; A: Admin).
- Guest questions ("ask us" form): always stored and shown in admin; email forwarding optional — sent only when email key is set, otherwise written to the console (B: Scope Must, Success Criteria; A: Later decisions).
- Easy to use on phone for all ages; also works and is easy to read on PC using the phone layout (B: Scope Must).
- Local setup: seed data with fictional guests and households, test links, test admin user (B: Scope Must).

If time and capacity allow (by Dec 2026 if possible, else before invitations ~Dec 2027) (B: Scope):
- Letter-opening invitation animation on first visit (letter/envelope); later visits straight to site (B: Scope; A: Invitation experience; T: CSS suggested).
- Speech sign-ups that reach the toastmaster.
- Gift list page (copy: "we know the wedding may be expensive to attend and we don't expect gifts, but there is a wish list for anyone who wants one") (A: Content pages).
- Link tracking: which households have started (e.g. clicked "Start" or saved an answer); page load does not count (C4).
- English version, language button at top.
- Email or SMS notifications to guests when information changes.
- Layout using the larger PC screen.
- Printer-friendly admin page with numbers for Hardingasete.

## 4. Business rules

Prices / payment:
- Paid options per person: cabin accommodation for whole weekend (all or nothing, confirmed by Hardingasete), Friday dinner, Saturday breakfast, Sunday breakfast (B: Solution; A: Paid options).
- Saturday lunch and dinner paid by the couple (B: Solution; A).
- Guests pay Hardingasete's prices (rationale note shown) (B: Solution).
- Payment per household: form sums household total (A: Paid options).
- Payment outside app: bank transfer or Vipps to the couple; couple pays Hardingasete (A: Payments; B: Scope Out).
- Prices from Hardingasete not yet known → must be easy to change (B: Constraints; A).
- Price per guest = selected meals + accommodation; counts per meal; bed need (T: Domenelogikk).

Attendance / meals / cabins:
- Per person: which days (Fri, Sat, Sun); can attend without overnight stay (B: Solution).
- Meals independent of accommodation (B: Scope Must).
- Accommodation: whole weekend or nothing (B; A).

Deadlines:
- RSVP deadline locks answers; set about **two weeks before Hardingasete's deadline** for final numbers (B: Constraints).
- Admin can override after lock (B; A).
- Post-deadline: guest sees message with couple's contact details (B; A).
- Course delivery mid-December 2026; usability test first week of December 2026; invitations ~December 2027; wedding 27 May 2028; deletion by 31 August 2028 (B).

Consent (B: Scope Must, Data and Privacy; A: Consent, Decisions after research):
- RSVP can always be sent; consent is not a condition (GDPR Art. 7(4)).
- Allergies/dietary needs optional; saved only with separate, **unticked** consent ("I consent to …") naming purpose (passing on to Hardingasete's kitchen) and who can see it (couple, toastmaster, maid of honour, best man).
- Guests told before consenting that they can withdraw via the same link; withdrawal deletes allergy information.
- Site stores when consent was given and which text was shown.
- Without consent, guests can tell the couple directly.
- Person answering enters allergies for each person and confirms others in household know and agree; only categories + short note, no diagnoses; remaining risk accepted and documented.
- Superseded rule (2026-10-23): consent box required to send the answer — replaced 2026-11-06.

Households:
- Couple or family; one member answers for all; responder chooses identity from household names (C6) (B).
- Last save wins; "last updated by X at Y" shown before editing (C5).
- Admin can move people between households (B; A).

Links:
- One personal link per guest; long random token; shows only own household; is the login (B).
- Couple sends links manually via Messenger, SMS or email; site does not send invitations (B: Scope Out; A: Admin).
- Page titles and link previews contain no names (C7) (B: Data and Privacy).
- Link tracking counts a household only once started, not on page load (C4).

## 5. Non-functional constraints

- Privacy/GDPR: repo is public; allergies are health data; GDPR assumed to apply (online, outside hosting, private-use exemption narrow) (B: Data and Privacy).
- Only fictional data in repo (dev, tests, seed, screenshots, usability test); real names, guest lists, allergies, payment details never committed and never pasted into AI tools (B; A; T).
- Real data only in production DB, set up 2027, hosted in **EU/EEA** (B).
- Secrets in `.env` ignored by Git; `.env.example` without real values; test admin fictional, only in local seed data, login documented in README (B).
- Access: only logged-in admin users see guest answers (B).
- Deletion: real guest data deleted no later than three months after wedding, by **31 August 2028** (B).
- Devices: phone-first; must work on PC with phone layout (examiner runs on PC) (B: Scope Must, Change Log).
- Accessibility: large readable text, good contrast, clear labels on every form field, clear messages when something is missing or wrong, full keyboard navigation (B: Who This Serves).
- Languages: Norwegian UI in V1; English is stretch (A: Later decisions).
- Hosting: none for course delivery (runs locally); production 2027, couple owns hosting and cost (B).
- Cost: no AI features (cost); course version must not depend on email service or hosting; email production cost open (B; T).
- Runnable: someone unfamiliar runs locally via README without Rikke's accounts or keys (B: Success Criteria).
- Reliability/correctness: admin counts must match hand-computed expected numbers for fictional test guest list, checked by automated tests (B: Success Criteria; T).
- Tech: full-stack with a database (course requirement); simple solution, one database, chosen and justified in architecture document (B: Constraints; T).
- Solo developer early in learning to code (B: Constraints).
- Process: all prompts saved; reflection report 3000–5000 words; planning artifacts are evidence for report section 2.4 (A: Course context).

## 6. Out of scope / explicitly excluded

- Online payment (B: Scope Out).
- Site sending invitations (B).
- Site sending answers or numbers to Hardingasete (B).
- Guest accounts and passwords (B).
- Hosting for course delivery (B).
- AI features in the site — guest Q&A assistant and AI cabin/bed placement dropped 2026-09-26 (B: Change Log; A: Later decisions).
- Household code in payment message (D1–D11) (B: Change Log).
- Diagnoses in allergy data (B: Data and Privacy).
- File handling/export not in v1 (T: Filhåndtering) — printer-friendly admin page is if-time.

## 7. Success metrics

Course delivery (mid-December 2026) (B: Success Criteria):
- Full guest flow works end to end on a phone: open link, RSVP for household, tick paid options, see total and how to pay.
- Admin overview shows correct counts (attendance, meals, beds, allergies, payments) for fictional test guest list with hand-computed expected numbers, verified by automated tests.
- Answers lock at deadline; admin can still override.
- Guest question appears in admin; emailed when key set, else console.
- Unfamiliar person runs app locally via README with seeded guests/households, test links, test admin, no Rikke accounts/keys.
- Complete prompt log backs reflection report.

Usability (test first week of December 2026):
- Older relative not comfortable with technology completes household RSVP on Rikke's phone or PC without help in **under 10 minutes** (fictional data).
- Couple finds any number Hardingasete asks for in **under a minute**.

Long-term (real wedding, not measured in course):
- **90%** of households answer through the site before deadline without being chased.
- **Zero** allergy or bed mistakes at Hardingasete.
- Couple never opens Excel for guest logistics.
- Few guest messages asking what the site already answers.

## 8. Open questions (unresolved)

- Prices from Hardingasete unknown (must be easy to change) (B: Constraints).
- Gift list form: static list, external link, or reservable gifts (B; A).
- Whether sending email costs anything in production (B; A).
- Hardingasete's answers on beds and cabins, prices, deadline for final numbers, whether guests can pay venue directly (asked 2026-11-06) (B: Constraints).
- Exact RSVP deadline date (depends on Hardingasete's deadline; ~2 weeks before) (B).
- Technology stack not yet chosen (to be justified in architecture) (B; T).

## 9. Change-log items (later decisions)

- **2026-09-26**: AI features removed from site (cost, not course requirement); confirmed AI-in-app not required (B; A).
- **2026-10-06**: Teacher feedback (T): difficulty "Middels" (lower middle); feasibility "Gjennomførbart med justert omfang"; key changes: fictional data only in public repo, separate course v1 from real wedding, plan local run with seed data/test admin/email without key; split "In" into core and second step; make email optional; move production/hosting to vision; risks: time/scope, runnable for examiner.
- **2026-10-23**: After teacher feedback — course delivery separated from wedding; real-wedding criteria → long-term goals; production/hosting → vision; email forwarding optional with console logging; local setup with seed data and test admin; Data and Privacy section; last-save-wins with "last updated"; usability test first week of December.
- **2026-10-23 (review)**: Must vs If-time split; letter animation, speech sign-ups, gift list, link tracking, English, change notifications → if-time; added admin creates guests/households, per-guest paid options with prices, whole-weekend accommodation, couple pays Sat lunch/dinner, payment per household, prices unknown, consent required to send (later replaced), usability requirements, EU/EEA storage, fictional test admin, sending to Hardingasete out; added PC layout and printer-friendly admin page to if-time; site must work on PC with phone layout; usability test on Rikke's phone or PC.
- **2026-11-06 (research, C1–C7)**: consent separated from RSVP (GDPR Art. 7(4), EDPB) — always sendable, consent only for optional allergies, withdrawable, recorded; responder confirms others agree, minimal data; prices shown before choosing with explanation, stable total (C3); link tracking = household started (C4); last updated shown before editing (C5); responder chooses identity (C6); no names in titles/previews (C7); GDPR assumed; Hardingasete answers open. Sources: `../../research/user-voice-wedding-website-pre-prd-2026-11-06/research.md`, `pre-prd-discovery.md`.
- **2026-11-06 (D1–D11)**: per-person days (Fri/Sat/Sun), attend without overnight; meals independent of accommodation; accommodation whole weekend or nothing (confirmed by Hardingasete); step-by-step form with check page and receipt page; deadline shown next to button and on receipt; payment message only shows it's for the wedding (no household code); payment status undo and "paid X, now owes Y"; allergies = categories + short note; arrival = optional fixed choices with "Don't know". Source: `pre-prd-discovery.md` section 2.
