# Extract: pre-PRD discovery + research (input to PRD)

Sources: `../../research/user-voice-wedding-website-pre-prd-2026-11-06/pre-prd-discovery.md` (PD), `.../research.md` (R). [R x.y] = research.md section; [n] = research source no.

## 1. Decided items

### C-items (decided 2026-11-06, Rikke; brief updated same day)

| ID | Decision (exact) | Implied requirement |
|---|---|---|
| C1 | "Accepted. The consent is separated from the RSVP: the answer can always be sent; the allergy field is optional with its own consent." | RSVP submittable without consent. Allergy field optional, own consent box: Yes/No, unticked, "I consent to …" wording; inform about withdrawal **before** consent; store timestamp + text version of consent; withdrawal via same personal link, then data deleted; guests who don't consent can tell couple directly. [R 3.2] |
| C2 | "Accepted. The respondent fills in allergies per person and confirms that the others know about it and agree. Categories + short text. The residual risk is documented in the brief." | Allergies per person; confirmation checkbox "I confirm that the people I am answering for know about this and agree"; data minimisation (categories + short text). Children not relevant (child-free). [R 3.2, 5] |
| C3 | "Accepted. Prices are shown before the choices, with a short explanation and a total that doesn't change unexpectedly." | Prices visible before form asks; explain why (Hardingasete prices; couple pays Saturday lunch + dinner); friendly tone; stable total through check step. [R 1.6, 2.1, 2.2] |
| C4 | "Accepted. \"Opened\" means that the guest has done something on the site, not that the page was loaded." | Link tracking based on guest action (e.g. clicked "Start" / saved), not GET page load. [R 4.1] |
| C5 | "Option (a): last save wins, and \"last updated by X at Y\" is shown before anyone starts editing." | No optimistic locking required; show "last updated by X at Y" before editing begins. [R 4.5] |
| C6 | "Accepted. The respondent chooses \"I am …\" from the household's names at the start." | Respondent identity selection from household member list at start of flow; used for "updated by". |
| C7 | "Accepted. Page title and preview are generic, with no names." | `<title>` and `og:` tags generic, no guest names. [R 4.1] |

### D-items (decided 2026-11-06, Rikke)

| ID | Decision (exact) | Implied requirement |
|---|---|---|
| D1 | "Per person, the form asks: are they coming, which days (Fri/Sat/Sun), which meals, and are they staying overnight. Hardingasete confirmed that accommodation is the whole weekend or nothing, so overnight is a single yes/no." | Data per person: attending, days (Fri/Sat/Sun), meals, overnight (single yes/no). Counts per day/meal/bed. |
| D2 | "Yes. A guest can come without accommodation, for example only for the wedding day, and chooses meals independently of accommodation." | Meals independent of accommodation; day-only attendance supported. |
| D3 | "Decided as C1 and C2." | See C1, C2. |
| D4 | "Accepted. The RSVP deadline is configurable and set about two weeks before Hardingasete's deadline, and it's shown next to the button and on the receipt page." | Configurable deadline setting; displayed next to RSVP button and on receipt page. Actual date pending Q2. |
| D5 | "Accepted. Locked for guests after the deadline, with a clear message and contact info. No grace period; the admin can override." | Post-deadline guest lock + message with contact info; admin can still edit. |
| D6 | "Accepted. Paid / not paid with undo. Amounts are stored as whole numbers, and totals are always calculated. The \"I have paid\" self-report remains optional." | Two-state payment status, reversible; integer amounts; totals derived, never stored. Self-report = optional feature. |
| D7 | "Accepted. If the total changes after payment, the admin sees \"paid X, now owes Y\"." | Store paid amount; admin shows difference when total changes after payment. |
| D8 | "**Changed.** No household code. The payment message only needs to show that it's for the wedding (for example \"Bryllup\" + name), because the couple won't receive many Vipps payments." | No household payment code; receipt instructs message e.g. "Bryllup" + name. (Deviation from PD proposal.) |
| D9 | "Accepted. Step by step with a check page before sending and a receipt page after." | Multi-step form (e.g. attendance → options → allergies → arrival → check), check-answers page, receipt page. Keep steps few. |
| D10 | "Accepted. Predefined allergy categories + short free text." | Categories: gluten, lactose, nuts, shellfish, vegetarian, vegan, other + short free text. Label proposed: "Allergies or dietary needs the kitchen must know about". Counts per category in admin. |
| D11 | "Accepted with an addition. Fixed choices for arrival time, but optional and with a \"Don't know\" option." | Arrival choices: Friday morning, Friday afternoon, Friday evening, Saturday morning, Don't know; optional; optional comment. No time pickers. |

### Q-items with answers

| ID | Question | Answer |
|---|---|---|
| Q5 | Can someone come only Saturday? Only Friday? | "answered 2026-11-06: yes, guests choose days and meals independently of accommodation" |
| Q6 | Should Friday activities (treasure hunt, sauna) and Saturday yoga have sign-up, or just be information? | "answered 2026-11-07: information only, no sign-up. The activities are shown on the programme page and are not part of the RSVP form" |

## 2. Still-open questions

| ID | Question | Recommendation | Blocks PRD? |
|---|---|---|---|
| D12 | Content management: info pages in code / editable by admin | In code for v1; prices and deadline as settings in admin or config (prices unknown yet) | No — "Taken into the PRD" |
| D13 | Helper roles: everyone full access (brief) / limited roles | Keep full access for 4 trusted people; note as conscious choice | No — "Taken into the PRD" (confirm) |
| D14 | Hashed or plain tokens | Plain + regenerate option in v1, or hashed + "generate new link" | No — Architecture |
| D15 | Database and stack (SQLite/Postgres; Django/Laravel/JS) | SQLite for clone-and-run | No — Architecture |
| D16 | Email provider in production (2027) | Check data **storage** location (Resend stores in US) | No — Later (2027) |
| Q1 | Hardingasete: number of beds/cabins, allocation (per person/cabin)? | — | No (sent 2026-11-06, awaiting reply); affects bed limit, price model, cabin allocation |
| Q2 | Hardingasete: when are final numbers for meals/beds/allergies needed, what format? | — | No (deadline configurable); sets D4 date and admin overview/print format |
| Q3 | Hardingasete: prices per meal and accommodation? | — | No (prices configurable) |
| Q4 | Hardingasete: pay couple or Hardingasete directly? | Paying third party feels better [R 2.2] | No; affects payment flow |
| Q7 | 2–3 guests (incl. older): how does "pay for meals" come across? What would you look for? | — | No; informs C3 wording, IA |
| Q8 | Course teacher: OK that consent model differs from brief if justified? Must "fasit" test list be in PRD or only tests? | — | No |
| Q9 | Own Vipps app: show phone number only, or QR as well? | Avoid "payment request" without prior agreement (terms forbid) | No; affects receipt page |
| Open research | Norwegian norms for guests paying for meals | Ask guests (Q7); Kvinneguiden | No |
| Open research | Norwegian user voice on wedding sites | Usability test in December + guest conversations | No |
| Open research | Older guests' reaction to animated envelope | Prototype test with one older relative | No |
| Open research | iMessage preview: which device fetches? | Send link to self, check server log | No |
| Open research | Is confirmation enough for one person entering another adult's allergies? | Ask Datatilsynet, or use C2 minimisation | No (C2 decided) |
| Open research | Does household exemption cover closed wedding site? | Keep conservative assumption (GDPR applies); document as decision | No |
| Open research | Norwegian registration tools (Checkin, Deltager) options/payment display | Create free test event | No |
| Open research | Brevo/Postmark EU data storage | Check before choosing 2027 | No |

Checklist status (PD §8): all items ticked except "Start `bmad-prd` with the brief, the addendum, research.md and this note as input".

## 3. Ideas / topics flagged for PRD

| Idea | Basis | Proposed scope |
|---|---|---|
| Check-your-answers page before sending, "Change" per person | GOV.UK, Baymard [R 1.7] | Must |
| Receipt/status page the link always opens (amount, reference, account/Vipps, status, deadline) | [R 1.7] | Must |
| "Not answered" list with contact details | [R 2.1] | Must (admin) |
| Admin can answer on behalf of a household | [R 2.2] | Must (part of "editing and overrides") |
| Attendance per day | [R 1.2] | Must (D1 decided per day) |
| Contact info (phone) on every page | [R 2.2] | Must (cheap) |
| Generic link preview (no names in title/og) | [R 4.1] | Must |
| Admin can regenerate a household's link | [R 4.1, 2.2] | Must (small) |
| Predefined allergy options + counts | [R 3, 2.1] | Must |
| CSV export / print page for Hardingasete | [R 1.4] | If time (in brief) |
| "I have paid" self-report from guest | [R 1.7] | Discuss (D6: optional) |
| Reminders (manual list) | [R 1.3, 2.1] | Out; admin list is enough |
| QR code with personal link on paper card | [R 2.2] | Outside site; possible later |
| Language preset per household (English) | [R 2.2] | If time (with English version) |
| Speech sign-up only toastmaster sees | [R 1.6] | If time (in brief) |
| "Who's coming" list visible to guests | Not researched; privacy risk | Discuss, probably no |
| Letter animation | No evidence; respect reduce-motion | If time (in brief); must be skippable |

User-need summaries (PD §4):
- Guest landing page after link: household names, deadline, "Start" button.
- Guest: receipt page + link always opens household status.
- Guest: prices visible before form, total shown along the way, unchanged at check step.
- Older guests: large text, large buttons, Back link, errors at the field, error summary, couple's phone number on every page.
- "Practical" page ordered by day: time, address, parking, transport, dress code, what to bring, weather.
- Couple: admin overview with counts per meal, day, bed, allergy + printable page/CSV; "not answered" list with phone/email; payment overview per household; admin fills form on behalf of household.
- Helpers: shared admin; speech sign-up to toastmaster (if time).

Brainstorming topics (PD §7): first 10 seconds after link; the money talk wording; RSVP flow for family of four (one not coming); admin overview designed from Hardingasete's questions; weekend programme page by day (optional/costed items, what to bring: hiking boots, swimwear for hot tub); tone ("dere"/"du", humour in errors); edge cases (change of mind after paying, household splits, lost link, simultaneous answers, Saturday-only); fasit test list households (couple both coming, family with one not coming, single with allergy, Saturday-only guest, household paid, household not answered).

## 4. Research findings implying requirements

### Guest UX
- Personal link per household removes name-search errors (most common RSVP failure: exact match, lockout, strangers answering). [R 1.1] [6][13][28][39]
- One person answers for household; store answers **per person per event**; options stored on the person, household totals calculated (not add-ons as separate rows). [R 1.1, 1.2, 1.7] [1][14][15][83]
- Tri-state attendance (yes / no / not answered, null = not answered) gives "not answered" list for free. [R 1.2] [14][15]
- Conditional follow-ups: meal choice asked only of attending guests. [R 1.2] [2][5]
- Check answers page: title saying what to do, statement that nothing is complete until confirmed, "Change" link per item (hidden screen-reader text), button named after action, "Not provided" for skipped optional questions. Unexpected total change at review breaks recognition. [R 1.7] [85][86]
- Confirmation/receipt: reference, what happens next and when, contact details, way to save a record; users bookmark it. [R 1.7] [43]
- Guests ask anyway; many never open site; send link digitally; guests lose cards and need link again. [R 2.2] [36]
- Two guest types: ~half want only logistics (times, dress code, RSVP, gifts). [R 2.2] [37]
- Older guests: most manage, some don't; ~half of couples used hybrid (paper/phone). [R 2.2] [40]
- Older users (65+): more mistakes, blame themselves; miss vague errors; small text/buttons and strict formats (date pickers, hyphenated phones) cause errors → forgiving input, errors at the field, larger targets. [R 2.2] [41]
- GOV.UK: one question per page, visible Back link, "Continue" button, confirmation page. [R 2.2] [42][43]
- Costs must be clear before answering; adding costs later is improper; paying a third party preferred. [R 2.2] [44][45]
- Language switcher: prominent, no flags. [R 2.2] [46]
- Invitations "clear for the most senior generation"; no evidence on animated envelopes. [R 2.2] [47]
- Costs on guests sensitive in Norway ("guests must pay in the bar" listed as blunder). [R 1.6] [21]

### Couple / admin dashboard
- Chasing replies is core problem; set deadline well before venue deadline; phone non-responders. [R 2.1] [25][26]
- Admin counts: meal totals, attendance per event, response rate, "not answered" list, missing meal choice; CSV/Excel export standard. [R 1.4] [8][14][15]
- Couple can edit answers. [R 1.4] [8]
- No product shows what guests owe; payment tracking absent everywhere; couples collecting money had no way to track who paid. [R 1.5, 2.1] [10][11][15][31][108]
- "Mark as paid" pattern (Tito: two states, confirmation step); for wedding use undo. [R 1.7] [82]
- Integer amounts (cents) with status lifecycle. [R 1.5] [15]
- Caterers want final headcount 1–4 weeks before, dietary details ~1–2 weeks before; RSVP deadline ~2 weeks before caterer deadline. [R 2.1] [33]
- Helpers: every added user could edit everything → couples shared login; limited roles is market gap. [R 2.1] [34][35]
- No product says whether guests are locked while couple can still edit — must design. [R 1.3]
- Joy: deadline shown next to RSVP button; form closes at midnight event time zone; after deadline button replaced by custom message. [R 1.3] [3][4]
- Norwegian convention: invitations ~3 months before, reply deadline ~1 month before (weak source). [R 1.6] [18]
- Speech sign-up example: name, relation, type, duration (~5 min), technical needs, deadline 2 weeks before; couple doesn't see. [R 1.6] [23]

### Privacy / GDPR
- Assume GDPR applies (household exemption narrow; no source on closed sites); document as decision. [R 3.1] [68][69][97]
- Allergies likely health data (Art. 9); religious dietary needs may be Art. 9. [R 3.2] [70][71]
- Consent must not be condition for RSVP (Art. 7(4), EDPB; burden of proof on controller). [R 3.2] [73][93]
- Explicit consent: separate Yes/No with "I hereby consent to …"; inform about withdrawal before consent. [R 3.2] [93]
- Record how/when consent given and text shown, without collecting more than needed. [R 3.2] [93]
- Withdrawal in same interface, as easy as giving; data then deleted. [R 3.2] [73][93]
- No source supports one adult consenting for another; confirmation box is unsourced mitigation. [R 3.2] [92][93]
- Data minimisation and storage limitation (Art. 5). [R 3.2] [96]
- Privacy notice per Art. 13: controller + contact, purpose + legal basis, recipients (helpers, venue kitchen), transfer outside EEA, retention, rights, right to withdraw, right to complain to Datatilsynet, whether voluntary and consequences. [R 3.3] [94]
- Hosting/email providers storing data = processors → data processing agreement (Art. 28). [R 3.3] [95][98]
- Deletion date 31 Aug 2028 (per brief). [R 6 rec. 11]

### Payment (Vipps / bank)
- Vipps private: free to 5,000 NOK per recipient/24h then 1%; "for private purposes"; pay by phone number or personal QR; payment requests only if agreed in advance; no business/public collections; terms silent on showing number/QR on website. [R 3.4] [74][75][76]
- 2 NOK fee from 1 Mar 2027 only for scheduled payments. [R 3.4] [75]
- Bank: 11-digit account number; private persons use free-text "melding" (KID needs business agreement). [R 3.4] [100][101]
- Make no tax claims; no claims about Vipps beyond showing number/QR. [R 3.4, 6 rec. 14] [102]

### Accessibility (WCAG 2.2 AA as self-imposed target) [R 3.5] [80][81]
- 1.4.3 contrast 4.5:1 (check sage green on soft white).
- 1.4.4/1.4.10 works at 200% zoom and 320 px width.
- 2.4.7/2.4.11 visible, unobscured focus.
- 2.5.8 targets ≥24×24 px (larger for older guests).
- 3.3.1–3.3.3 error text at the field with suggested fix; labels on all fields.
- 3.3.7 don't ask for what the link already knows (names).
- 3.3.8 no password for guests.
- Error summary (Designsystemet): above submit, only after submit attempt, focus moves there, each error links to field, heading "For å gå videre må du rette opp følgende feil."
- Legal duty probably doesn't cover private couple (inference); assessed under criterion 4 anyway. [78][79]

### Link security / link previews [R 4.1]
- Token from CSPRNG, ≥128 bits (prefer 160+), no personal data in URL. [48]
- URLs leak via logs, history, bookmarks, Referer, search engines → `Referrer-Policy: no-referrer`, noindex, rate-limit attempts, store tokens securely. [48][49]
- Hashed storage not explicitly required by OWASP; trade-off (hashed → admin must regenerate). [48]
- GET must have no side effects; all changes via POST (email scanners pre-fetch links). [50][51]
- Meta `facebookexternalhit` fetches/caches title, description, image for links in Messenger, may bypass robots.txt; WhatsApp fetches on sender's behalf while typing; Slackbot ignores robots.txt; iMessage unverified. [87][88][89][90]
- Email gateways create false opens/clicks within seconds. [91]
- Consequences: no names in `<title>`/`og:`; "opened" based on guest action or bot filter; opening link never changes anything.

### Admin login [R 4.2]
- Argon2id (m=19 MiB, t=2, p=1; bcrypt only legacy, cost ≥10). [52]
- Server-side sessions; `HttpOnly` + `Secure` + `SameSite` cookies; new session ID at login; idle timeout 15–30 min; logout invalidates server session. [48]
- Framework CSRF protection on all forms. [50]
- Login rate limiting (e.g. 5/min per email+IP). [62]

### Reliability / concurrency / runnability
- Last-save-wins: standard safer pattern is `version` column + conditional UPDATE; `updated_at` weaker. (C5 chose (a).) [R 4.5] [63]
- SQLite: no setup, one file, one writer, ample for 70 guests + 4 admins; Postgres needs server/Docker. [R 4.4] [59]
- Django admin intended as internal tool, not whole front end. [R 4.4] [60]
- Prisma v7 no auto-seed → seeding explicit documented step. [R 4.4] [61]
- Email in dev: console/file backend or Mailpit (no key). [R 4.3] [53][54]
- NFR runnability: no external DB server, email to console without key, seeding explicit documented step. [R 6 rec. 12]
- Production email (2027): require EU **storage**; Resend stores account data/logs in US → ruled out as-is; Postmark 100/mo free; Brevo 300/day (unverified). [R 4.3] [55][56][57][58]
- EU hosting 2027: Hetzner ~€6/mo; Fly.io no free tier; Render free Postgres expires 30 days, web sleeps 15 min. [R 4.6] [64][65][66]
- Re-check: Joy features + Vipps Jan 2027; prices, Vipps terms, regulatory points before production 2027. [R 9]

### Cross-dimension [R 5]
- Personal link identifies household, not person → "who answered" and "who consented" unclear (resolved by C6, C2).
- Structured choices (arrival, allergies, check, receipt) lower guest errors and give countable admin data and easier fasit tests.

## 5. Explicitly out of scope / excluded

- Sign-up for Friday activities (treasure hunt, sauna) and Saturday yoga — information only on programme page, not part of RSVP form (Q6).
- Household payment code (D8 changed: no household code).
- Grace period after deadline (D5).
- Optimistic locking / conflict message (C5 chose last-save-wins).
- "Opened" based on page load (C4).
- Consent as precondition for sending RSVP (C1).
- Reminders sent from the system — "Out (the couple sends them themselves); the list in admin is enough".
- QR code on paper card — "Outside the site (couple's choice); possible later".
- "Who's coming" list for guests — "Discuss, probably no".
- "Partly paid" payment state (D6: two states only).
- Children/child pricing — child-free wedding.
- Tax claims; Vipps "payment requests" without prior agreement.
- Time pickers / strict input formats.
