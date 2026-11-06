---
title: "Pre-PRD research: wedding website (AI'll handle it)"
type: "user-voice + competitive + domain + technical"
topic: "What similar products, users, rules and technical practice tell us before writing the PRD for AI'll handle it"
decision: "What the PRD must contain: requirements, scope, priorities, and which questions to settle first"
source: "native run (parallel web research, 2 rounds)"
status: complete
preset: "deep"
validation: "normal"
claims_verified: 18
claims_unverified: 2
claims_disputed: 1
created: "2026-11-06"
updated: "2026-11-06"
---

# Pre-PRD research: wedding website (AI'll handle it)

**Decision this research serves:** what the PRD must contain (requirements, scope, priorities) and which questions must be settled first.

## Executive summary

**The brief holds up, with two important adjustments.** The research supports the core of the brief: a personal link per household, one person answering for everyone, and an admin overview that replaces Excel. Two points in the brief should be changed before the PRD, and several decisions must be made explicitly. The analysis and the list of decisions are in [pre-prd-discovery.md](pre-prd-discovery.md).

**Three findings carry the recommendation:**

1. **The personal link is the right choice, and the research strongly supports it.** Name search is the most common source of RSVP errors in established products (exact match, lockout, strangers answering) [6][13][28][39]. Products and open-source projects that work well let one person answer for the household but store attendance and choices **per person per event** [1][2][14][15]. The link must be handled as a secret: at least 128 bits of randomness, no names in the page title (Messenger and WhatsApp fetch and cache the preview), and nothing should happen just because the link is opened [48][87][88].
2. **Consent must be separated from the RSVP.** The brief says the answer can't be sent without consent. GDPR Art. 7(4) and EDPB say consent tied to a service is presumed not freely given, and the burden of proof is on the couple [73][93]. In addition, no source supports one adult consenting for another adult's health data [92][93]. The allergy field should therefore be optional, with its own consent, and the solution for answering on behalf of others must be chosen and justified (see recommendations 1–2).
3. **Showing guests what they owe has no direct model.** No wedding product found shows guests what they owe for their own meals or accommodation [10][11][15]. Guests paying for accommodation is common in Scandinavia [19][20], while paying for meals is seen as awkward in US sources [44][45]; Norwegian norms for meals were not found. The best patterns come from other domains: show prices before the choices, a check page with a stable total, a receipt page with a payment reference, and "Mark as paid" in admin [82][85][86][43].

**Biggest caveat:** the user voice is mostly American and partly old (WeddingWire 2017–2023), because Reddit and datatilsynet.no could not be reached by the research tools. Norwegian norms (paying for meals, reply deadlines) and what Datatilsynet thinks about closed event sites remain open. They should be closed by talking to Hardingasete and a few guests, and if needed by asking Datatilsynet. All recommendations are in section 6, and open questions in section 7.

## 1. Similar solutions: what established products and open-source projects do

### 1.1 Households: the household answers, each person is stored

All the products examined let one person answer for a group but store the answers per person. Joy has "parties", where one member can "step up to respond for the entire group" [1]; Zola lets one household member answer for everyone by typing their own name [6]; WedSites calls them "households" and records members who answer separately individually [16]. The two best-documented open-source projects use the same model: czue/django-wedding-website has `Party` 1–N `Guest` with a random `invitation_id` on the party [14], and fredbenenson/git-hitched has `Invite` (household) 1–N `Guest` [15].

**Identification is where the products fail.** Zola requires the name to match the guest list exactly and locks the guest out for a few hours after repeated failed attempts [6]. "Name not found" is the most common complaint in WeddingWire threads about RSVP [13][38], and a vendor help centre lists it as a known issue [39]. A personal link avoids name search: per recipient in Greenvelope [9] (low confidence, marketing) and per household in czue [14]. That this removes the problem is our analysis. *Confidence: medium (forum + vendor docs).*

### 1.2 Multi-day events: one schedule, attendance per event

Joy's model is the most mature: one master schedule, each event visible only to "Specific guests" (chosen by tags), its own questions per event, and conditional follow-up questions, so meal choice is asked only of guests who say yes [2][5]. Joy also has "Ask Once Per: Household" for questions that apply to the whole group [5]. Zola [7] and The Knot [104] let the couple choose which events each guest is invited to.

In the data model, git-hitched shows how to do this without flags: `Event`, `EventInvite` (which household is invited to what) and `RSVP(guest, event)` with nullable `attending` (null = not answered) [15]. czue models an extra event as a single boolean (`rehearsal_dinner`) [14], which doesn't scale to three days. Both use **tri-state attendance** (yes / no / not answered), which gives the admin a "not answered" list for free [14][15].

### 1.3 Deadline and locking

Joy has the most complete deadline handling (help docs from Aug and Oct 2026): the form closes automatically at midnight in the event's time zone, the deadline is shown next to the RSVP button, an optional grace period runs from 12 hours to 7 days, and after the deadline the button is replaced by a custom message [3][4]. Joy also sends event reminders to attending guests 6, 3 and 1 month before the event, and RSVP summary emails to the couple [4]. **No product clearly says whether guests are locked out while the couple can still edit.** That rule must be designed by us. *Confidence: high (Joy's own docs).*

### 1.4 Admin view

Zola shows meal totals and adult/child breakdowns, and the couple can edit answers [8]. czue has a separate dashboard with RSVP counts, a list of guests who haven't answered, and guests missing a meal choice [14]. git-hitched has a dashboard with response rate, attendance per event, meal counts, CSV import and Excel export [15]. Greenvelope (low confidence) and git-hitched offer CSV/Excel export [9][15]. *Confidence: medium–high.*

### 1.5 Money from guests: no wedding product shows what guests owe

Website and RSVP are free on the big platforms [12], and every wedding product examined handles money only as **gifts** (cash funds): Zola charges 2.5% on credit-card payments [10] and Joy 3.5% (Joy's "zero-fee" marketing contradicts its own help centre) [11]. **No wedding product found shows guests what they owe for their own meals or rooms.** git-hitched is the only project that charges for hotel rooms, using Stripe, and it stores amounts as integer cents with a status lifecycle (pending/confirmed/refunded) [15]. The "what you owe" part of the PRD has no direct model to copy (see 1.7 for adjacent categories). *Confidence: high (absence confirmed by two researchers).*

### 1.6 Norwegian and Nordic solutions

No Norwegian wedding service with households, meal choices and payment information was found. What came up were the multilingual planning.wedding (marketing a personal link per guest) [17], Wix/Canva templates, and Google Forms as an RSVP tool [105]. Norwegian couples most likely use international tools, generic page builders, or Google Forms/Excel, but **no data on how common each is was found**. *Confidence: low (thin data, and the absence is itself a finding).*

Norwegian conventions that affect the site:
- **Deadlines:** invitations about 3 months before and reply deadline about 1 month before, per a 2024 Norwegian-language vendor guide [18]. This is not an authoritative source. *Medium/low.*
- **Guests paying for accommodation** is common in Scandinavia: guests book and pay for their own stay, often at a rate the couple negotiated [19], and Thon Hotels publishes per-wedding pages with special guest room rates [20]. **No Norwegian source on guests paying for meals was found.** *Medium.*
- Costs that fall on guests are a sensitive topic: Klikk.no lists "guests must pay in the bar" among the blunders that annoy guests [21]. *Medium.*
- **Speeches:** the usual Norwegian speech order and the toastmaster's running schedule are described [22]. A Swedish 2026 example shows speech sign-up to the toastmasters in a form the couple doesn't see, with name, relation, type, duration (~5 min), technical needs, and a deadline 2 weeks before the wedding [23]. *High for that wedding, low as a general convention.*
- **Wish list:** Ønskeskyen is used in Norway and prevents duplicate gifts, but has no wedding-specific features [24].

### 1.7 Adjacent categories: paid add-ons and confirmation

Because no wedding product handles guest-paid options, the second round looked at event-registration tools and design systems.

- **Offline payment marked by hand:** Tito lets the organiser open an unpaid order and choose "Mark as paid" (with a confirmation step). This sends the buyer a confirmation email and closes the payment link, and Tito says "You can't undo this". Tito has only two states, unpaid and paid, with no "partly paid" [82]. *High.* For a wedding, "undo" is probably better, since the couple will make mistakes, and partial payment must be a deliberate PRD decision.
- **Options per person, not as separate rows:** Eventbrite stores each add-on as a separate "attendee", without distinguishing people from items [83], which makes the attendee list ambiguous. Store the options on the person and calculate household totals from them. *Medium.*
- **Norwegian registration tools** (Checkin, Deltager.no, Hoopla): only marketing pages and terms were found, not how they present options and payment status [84]. *Low.*
- **Summary before submit:** GOV.UK "Check answers": a page title that says what to do, a statement that nothing is complete until the user confirms, a "Change" link per item (with hidden screen-reader text), a button named after the action, and "Not provided" for skipped optional questions [85]. Baymard: users find errors at the review step and want to fix them there, some confuse the review page with the confirmation page, and **an unexpected change in the total at review makes users stop recognising the order** [86]. *High (GOV.UK) / medium (Baymard, paywalled).*
- **Confirmation as a receipt:** GOV.UK requires a reference, what happens next and when, contact details, and a way to save a record; users bookmark the confirmation page as a receipt [43]. For this site: the personal link should always open the household's status page, with amount, payment reference, account/Vipps number and status.

## 2. What users say

Method note: Reddit was not reachable for the research tools (blocked). User voices therefore come mostly from WeddingWire forums (often 2017–2023), Trustpilot (2026), and editorial etiquette sources. Prevalence claims are only made where two independent communities agree.

### 2.1 The couple

**Chasing replies is the core problem.** A couple with 50 invited guests got almost no replies, and email and text reminders didn't help ("no one has been responding") [25]. Reddit threads, available only as search snippets, describe the same thing. Norwegian etiquette advice assumes it: "make a friendly phone call" to anyone who hasn't answered [26]. Workarounds: set the deadline well before the venue/caterer deadline and call people [25]; some mark non-responders as "no" (Reddit story retold in the press, low) [106]. *Medium (two communities plus a Norwegian editorial source).*

**Household and plus-one errors break the headcount.** Zola could not handle "The Smith Family" as one invitation ("You have to populate it exactly as it wants you to") [27]; strangers RSVP'd with meal choices on an open site [28]; guests add extra people [107]. One couple gave up and went back to paper cards [27]. *Medium.*

**Praise (2026):** Joy is praised for easy RSVP collection and "less stressful" guest lists, and criticised for charging to email guest groups [29]. Zola has a score of 1.2/5 on Trustpilot, with complaints about fees, support and missing export of the gift list [30].

**Guests paying.** Couples who host cabin or camp weekends do collect money for accommodation and meals themselves (Venmo/PayPal/cheque) [108] (low–medium), and a couple whose venue required prepayment had no way to track who had paid [31]. **None describes a method for tracking payments.** Etiquette is split: guests paying for **accommodation** is broadly accepted if it is optional and disclosed up front; asking guests to pay for **meals** is often called "tacky", and guests feel "nickel and dimed" [32][44][45]. *Medium (WeddingWire + A Practical Wedding, US norms).* Norwegian norms for paid meals were not found (see 1.6).

**The numbers the venue needs:** caterers typically want the final headcount 1–4 weeks before and dietary details about 1–2 weeks before; the advice is to set the RSVP deadline about 2 weeks before the caterer's deadline [33]. *Medium (several independent sources agree on the range).*

**Helpers:** on WeddingWire, every added user could edit everything, so a couple shared their login with the bride's mother instead [34]. At least one vendor sells limited roles [35]. Limited helper roles are a known gap in the market. *Medium.*

### 2.2 The guests

**Guests ask anyway.** In one WeddingWire thread, about 12 of 21 voices said guests asked about times, place, hotel and food even though it was on the site, and many never opened the site [36]. Traffic rose when the link was sent by email instead of only printed on the card; guests lose the card and need the link again [36]. *Medium (one community, 2017).*

**Two kinds of guests.** About half want only logistics: times for all events, dress code, RSVP, gifts ("Just the important info I need"); the rest read everything, including the couple's story [37]. *Medium.*

**Older guests: most manage, not all.** In a thread with about 13 couples, results went both ways: a 91-year-old managed fine, while two great-aunts in their 80s could not and sent a note instead. About half of the couples used a hybrid approach (paper or phone for the oldest guests) [40]. *Medium.*

**Usability research on older users** (NN/g, 123 people aged 65+, 2019): they make more mistakes than younger users and blame themselves, they miss or misunderstand vague error messages, and small text and buttons and strict input formats (date pickers, phone numbers with hyphens) cause errors. Recommendations: forgiving input, clear error messages placed at the field, larger targets [41]. *High (but 2019).* GOV.UK recommends one question per page, a visible Back link, a "Continue" button, and a **confirmation page** that says what was received, what happens next and when, and gives the user a way to keep a record [42][43]. *High.*

**Costs must be clear before guests answer.** Paid accommodation is acceptable if it is optional, priced per unit and known up front; adding costs later or charging for meals the hosts "provide" is seen as improper [44][45]. A Practical Wedding: "nobody wants to feel like they have to purchase their spot at the wedding", and payment preferably goes to a third party [45]. *Medium (two independent sources, US).*

**Language:** Wikimedia's user tests found that a prominent language switcher is found faster, and practitioners advise against flags (language ≠ country) [46]. *Low–medium.*

**Invitation experience:** Lizzie Post (2017) says invitations should be on paper and "clear for the most senior generation" [47]. **No evidence was found on how older guests react to animated envelopes.** *Medium (expert opinion, old).*

### 2.3 Jobs-to-be-done (synthesis of 2.1–2.2)

| Who | When … | I want … | So that … |
|---|---|---|---|
| Couple | the venue's deadline approaches | reliable counts per meal and day, with dietary needs | I can send final numbers without guessing |
| Couple | someone hasn't answered | to see exactly who is missing, with contact details | I don't spend a week chasing |
| Couple | guests pay for accommodation and meals | to see who owes what and who has paid | I don't need a separate spreadsheet or awkward chasing |
| Couple | helpers need to help | to give them access without sharing my password | helpers can help without me |
| Guest | I get the link | to see right away who in my household is invited and what I must do by when | I don't have to ask |
| Guest | I answer | to avoid searching for my name, tick each person, and know it got through | I'm sure it worked |
| Guest | before I commit to the weekend | to know what it costs, what is optional, and who I pay | there are no surprises |
| Older guest | I'm unsure | large text, a clear way back, and a person to call | I'm not afraid of doing it wrong |
| Guest | close to the date | times, address, parking, dress code, what to bring, quickly | I find it without asking |

## 3. Rules: privacy, payment and accessibility

Not legal advice. datatilsynet.no refused connections in both rounds, so Datatilsynet points rest on search excerpts (medium confidence). The GDPR text, the EDPB guidelines and the Vipps terms were read in full.

### 3.1 Does GDPR apply to a private wedding site?

GDPR does not apply to "purely personal or household activity", but it does apply to those who provide the means, such as hosting and email providers (Recital 18) [68]. The CJEU reads the exception narrowly: Lindqvist (2003) excluded internet publication to an indefinite audience, and Ryneš (2014) narrowed it further [69] (secondary commentary; primary text not retrievable). Datatilsynet calls the exception "a narrow exception" and points out that online publication about others may be covered [97]. **No source was found on whether a closed, link-protected event site falls inside or outside the exception.** The safe and assessable choice is to **assume GDPR applies**, and to document that as a decision. *Medium (the conclusion is analysis; the sources are high/medium).*

### 3.2 Allergies, consent, and answering on behalf of others

- **Health data:** Art. 9 prohibits processing "data concerning health" unless an exception applies, for example explicit consent (Art. 9(2)(a)) [70]. Datatilsynet reads health data broadly, including indirect information [71]. That allergies are health data is an inference; no source specifically on food allergies was found. Religious dietary needs may reveal religious belief, which is also Art. 9 data. *Medium.*
- **Consent must not be a condition for the RSVP.** Art. 7(4) and EDPB 05/2020 say consent tied to a service for data that isn't necessary for it is "presumed to be not freely given", and **the controller has the burden of proof** (paras 26, 32, 36) [73][93]. The brief's rule "the answer can't be sent without consent" therefore conflicts with the guidelines. *High.*
- **Explicit consent online:** separate Yes/No boxes with wording like "I hereby consent to …" are enough (para 96); "It is clear to me that …" is not [93]. Inform about withdrawal **before** consent is given (para 116) [93]. *High.*
- **Record:** store how and when consent was given and which text was shown (para 108), without collecting more than needed (para 106) [93]. *High.*
- **Withdrawal in the same interface** (the personal link), as easy as giving consent, after which the data is deleted (paras 113–117) [93][73]. *High.*
- **One person answering for others:** consent is by definition the data subject's **own** statement (EDPB para 93), and EDPB discusses third-party consent only for **parents of children** [93]. Helsedirektoratet (2025) says "relatives cannot consent to processing of personal data on behalf of an adult" (health-care context) [92]. **No source supports a household member validly consenting for another adult.** A confirmation box ("I confirm that the people I am answering for are informed and have consented") is a practical mitigation **without** any source behind it. A Norwegian sports club writes that it collects allergy information for events where food is served [109], and NIF's guide says that, for registration in general, consent should be obtained "from the person" [103] (both low–medium, from search excerpts). *Medium.*
- **Data minimisation:** "adequate, relevant and limited to what is necessary" (Art. 5(1)(c)), and storage limited in time (Art. 5(1)(e)) [96]. *High.*

### 3.3 Privacy notice and processors

Art. 13 lists what guests must be told: who is responsible and how to contact them, purpose and legal basis, recipients (helpers, the venue kitchen), any transfer outside the EEA, retention period, rights (access, rectification, erasure, and so on), the right to withdraw consent, the right to complain to Datatilsynet, and whether providing the data is voluntary and what happens if they don't [94]. Hosting and email providers that store data are **processors** and need a data processing agreement (Art. 28) [95][98]. *High.*

### 3.4 Vipps and bank transfer

- **Vipps between private persons** is free up to 5,000 NOK to the same recipient within 24 hours, then 1% [74]. Private users can receive money "for private purposes", and payers can pay by phone number or by scanning "their personal QR code"; payment requests are allowed only when agreed with the payer in advance; business purposes and public collections are not allowed (terms v1.5, 2026-10-20) [75][76]. **The terms neither allow nor forbid showing the number or QR code on a website.** The fee from 1 March 2027 (2 NOK) applies **only to scheduled payments**, not to one-off transfers [75]. "Vipps boks" costs 19 NOK per 1,000 NOK [77]. *High.*
- **Bank transfer:** 11-digit account number [100]; KID is a structured reference that requires an incoming-payment agreement with the bank (business service), while private persons use free-text "melding" [101]. *Medium/low (the business-only point is inferred).*
- **Tax:** Skatteetaten says it's the purpose of the money, not how it's paid, that decides whether it is taxable; income from work or business is taxable [102]. No source covers cost-sharing between private persons directly, so the PRD should make no tax claims. *Medium/low (2013).*

### 3.5 Accessibility (universal design)

The Norwegian Equality and Anti-Discrimination Act (likestillings- og diskrimineringsloven) § 18 places the ICT duty on "public and private undertakings" [78], and Uutilsynet names businesses, clubs and organisations [79]. A private couple is **probably** not covered, but no source says so outright (inference). WCAG 2.2 (W3C, 12 Dec 2024) is still a good self-imposed target, and it is assessed under criterion 4 anyway [80]. Most relevant for this site:

| Criterion | What it means here |
|---|---|
| 1.4.3 Contrast (AA) | 4.5:1 for text: sage green on soft white must be checked |
| 1.4.4 / 1.4.10 Resize text / Reflow | Works at 200% zoom and at 320 px width |
| 2.4.7 / 2.4.11 Focus visible / not obscured | Visible focus for keyboard navigation |
| 2.5.8 Target size (AA) | At least 24×24 px (larger for older guests) |
| 3.3.1–3.3.3 Errors and labels | Error described in text at the field, with a suggested fix, and labels on all fields |
| 3.3.7 Redundant entry | Don't ask for what the link already knows (names) |
| 3.3.8 Accessible authentication | No password for guests, which the personal link already fulfils |

Designsystemet.no (Digdir) describes the error-summary pattern: shown above the submit button only after an attempt to submit, focus moves there, each error links to its field, and the heading "For å gå videre må du rette opp følgende feil." [81]. *High.*

## 4. Technical practice (input to non-functional requirements; stack choice belongs in the architecture document)

### 4.1 Personal links

OWASP: tokens that are not generated by the framework should come from a cryptographically secure random number generator (CSPRNG) and have **at least 128 bits of entropy**, preferably 160+, and should not contain personal data [48]. Identifiers in URLs leak through logs, history, bookmarks, the Referer header and search engines [48]. URL tokens should be stored "in a secure manner", pages carrying them should send `Referrer-Policy: no-referrer`, and attempts should be rate-limited [49]. **OWASP does not explicitly say that tokens must be stored hashed.** That is a trade-off for the PRD/architecture: hashed storage is safer, but then the admin can't show the link again and must regenerate it (our analysis). *High.*

**Link scanners.** Email security scanners (SafeLinks, Proofpoint, Barracuda) send GET requests to links before the person clicks, and projects have fixed this by keeping GET side-effect-free and putting every change behind a POST [51]; OWASP also requires that GET has no side effects [50]. For link tracking ("opened link"), this means a bot visit can register as an "open". *Medium–high.*

**Link previews in Messenger, WhatsApp and Slack.** Meta's crawler `facebookexternalhit` fetches every URL shared in Meta apps (including Messenger), caches title, description and image, and "may bypass robots.txt" [87]. WhatsApp fetches the URL "on behalf of the sender" while the message is being written [88]. Slackbot does the same and ignores robots.txt [89]. Whether iMessage fetches from the sender's or the recipient's phone is **unverified** (2020 sources conflict) [90]. Email gateways create false "opens" and "clicks" within seconds of delivery [91]. *High (Meta/Slack docs) / low (iMessage).*

Consequences: (1) the personal link's `<title>` and `og:` tags must not contain guest names, because the preview is shown in the chat and cached by Meta; (2) "link opened" cannot be based on page loads, and should instead be based on an action by the guest (e.g. first save) or filter known bots; (3) opening the link must never change anything.

### 4.2 Admin login

OWASP's baseline: **Argon2id** for passwords (minimum m=19 MiB, t=2, p=1; bcrypt only for legacy systems, cost ≥10) [52]; server-side sessions in `HttpOnly` + `Secure` + `SameSite` cookies, a new session ID at login, idle timeout 15–30 min, and logout that invalidates the session on the server [48]; the framework's built-in CSRF protection on all forms [50]. Laravel's docs show login rate limiting of 5 attempts per minute per email+IP as an example [62]. No primary source on sessions vs JWT was found (unverified). *High.*

### 4.3 Email without a key

Django has a console backend (writes emails to stdout) and a file backend for development [53]; Mailpit is a local SMTP server with a web UI and an API for tests [54]. Production (2027): Resend's free tier is 3,000 a month / 100 a day [55], but **account data and logs stay in the US** even when sending from Ireland [56]; Postmark is free for 100 a month [57]; Brevo is free for 300 a day (help centre only, medium) [58]. *High except Brevo.*

### 4.4 Database and "clone and run"

SQLite: suitable for sites with fewer than ~100,000 hits a day, no setup, one file, one writer at a time [59], which is more than enough for 70 guests and 4 admins. PostgreSQL requires the examiner to install a server or Docker. Relevant version facts: Django 6.1 is current (5.2 LTS still supported, 6.2 LTS planned for April 2027) [67]; the Django admin is meant as an *internal* tool, not as the whole front end [60]; Prisma v7 no longer seeds automatically, so seeding must be a separate documented step [61]; Laravel 13 is current and requires PHP + Composer + npm [62]. *High (medium for the Django version).*

### 4.5 "Last save wins"

The standard pattern is a `version` column and `UPDATE … WHERE id = ? AND version = ?`; 0 affected rows means a conflict, and the screen shows "updated by X at Y" [63]. `updated_at` alone is a weaker signal (clock precision) [63]. *Medium (vendor blog, but an established pattern).*

### 4.6 EU hosting (2027, briefly)

Hetzner Cloud costs from about €6 a month (Germany/Finland) [64]; Fly.io has no free tier (Frankfurt ~$7.73 a month for 1 GB) [65]; Render's free Postgres expires after 30 days, and its free web services sleep after 15 minutes [66]. *High (pricing pages, Nov 2026).*

## 5. Cross-dimension insights

1. **The personal link solves three problems at once, but creates two new ones.** It removes the most common RSVP error (name search) (section 1.1), meets WCAG 3.3.8 without a password [80], and stops strangers from answering [28]. But the link is fetched and cached by chat apps [87][88], and it identifies the *household*, not the person. That makes both "who answered" and "who consented" unclear (section 3.2).
2. **Answering on behalf of the household and consenting to allergies pull in opposite directions.** Products and users want one person to answer for everyone [1][27], while GDPR treats consent as the person's own act [93][92]. This is the most important design conflict before the PRD. A model that resolves it: the respondent fills in everything, allergies are optional per person, and the consent is formulated and stored per person, with an easy way to withdraw it through the same link. The residual risk must be described honestly.
3. **Money is where there are no models, and where the social risk is highest.** No wedding product shows what guests owe (section 1.5), Scandinavian practice is that guests pay for accommodation themselves [19][20], and US guests react to paying for meals [44][45]. Norwegian norms for meals are unknown. The good patterns therefore come from other domains (Tito's "Mark as paid", GOV.UK check answers/receipt, Baymard's "no surprises in the total") [82][85][86][43].
4. **Older guests and the couple's need for numbers point to the same solution.** Older guests make mistakes and blame themselves [41]; the couple needs correct numbers [33]. Structured choices (fixed options for arrival and allergies, check page, receipt) lower the error rate for guests *and* give countable data for the admin view, which also makes the automated tests against a fasit list easier to write.
5. **Clone-and-run, GDPR and cost point to the same technical choices.** SQLite needs no setup [59]; an email backend that writes to the console needs no key [53]; and for production (2027) the requirement is EU *storage*, not just EU sending, which rules out Resend as-is [56].

## 6. Recommendations (input to the PRD)

Each recommendation names its confidence basis. "PRD" = functional requirement, "NFR" = non-functional requirement, "Brief" = the brief should be updated.

1. **Brief + PRD: separate consent from the RSVP.** Attendance, options and arrival can always be sent; the allergy field is optional with its own unticked Yes/No consent per person, informing about withdrawal before consent is given, stored with time and text version, and withdrawable through the same link. *High basis (GDPR text + EDPB).*
2. **PRD: decide how allergies for other adults are handled.** Options: (a) the respondent confirms that the others are informed and agree (practical, but not source-backed as valid consent), (b) each adult confirms their own entry, (c) collect only categories + short text. Recommendation: (a) + (c), with the residual risk documented, because (b) breaks the "one person answers" flow. *Medium (an analytical trade-off).*
3. **PRD: personal link per household, attendance and options per person per day/event, and tri-state status.** *High (products + OSS + user voice).*
4. **PRD: a check page before sending and a receipt/status page that the link always opens**, with amount, payment reference, account number/Vipps number, payment status and deadline. *High (GOV.UK) / medium (Baymard).*
5. **PRD: prices visible before the choices, stable total, friendly explanation of why guests pay.** *Medium (US etiquette + Klikk.no; Norwegian norms for meals unknown).*
6. **PRD: payment status as "not paid / paid" with undo, plus a decision on what happens when the total changes after payment.** *Medium (Tito + analysis).*
7. **PRD: admin with a "not answered" list with contact details, counts per meal/day/bed/allergy category, and the ability to answer on behalf of a household.** *Medium–high.*
8. **PRD: RSVP deadline configurable, set about 2 weeks before Hardingasete's deadline for final numbers.** *Medium (caterer sources, not Norwegian).*
9. **NFR (security):** token ≥128 bits from a CSPRNG, no personal data in the URL or in `<title>`/`og:` tags, `Referrer-Policy: no-referrer`, noindex, rate limiting, no state change on GET, a regenerable link; admin with Argon2id, secure session cookies, CSRF, login rate limiting. *High (OWASP, Meta docs).*
10. **NFR (accessibility):** WCAG 2.2 AA as a self-imposed target, with larger targets than 24 px, an error summary following Designsystemet, and no time pickers or strict formats. *High (W3C, NN/g, Digdir).*
11. **NFR (privacy):** privacy page covering the Art. 13 points, deletion date (31 Aug 2028 per the brief), processor agreement with hosting/email, EU storage. *High.*
12. **NFR (runnability):** no external database server, email to the console without a key, seeding as an explicit documented step. *High.*
13. **Brief: redefine or drop "link tracking"** (bots create false opens). *High (Meta/Slack docs + vendor docs).*
14. **Do not claim anything about tax or Vipps on the site beyond showing the number/QR**; avoid "payment requests" without prior agreement. *High (Vipps terms) / medium (tax).*

## 7. Open questions

| Question | Why it's open | What would answer it |
|---|---|---|
| Does the household exemption cover a closed, link-protected wedding site? | No source found; datatilsynet.no could not be read | Ask Datatilsynet's advice line, or keep the conservative assumption (recommended) |
| Is a respondent's confirmation enough for others' allergy information? | No source on adults in a non-health context | Ask Datatilsynet, or design to minimise (recommendation 2) |
| Norwegian norms for guests paying for meals at a wedding weekend | Not found online | Ask a few guests; Kvinneguiden forum |
| How older guests react to the letter animation | No evidence | Prototype test with one older relative |
| Does iMessage fetch the preview on the sender's or recipient's phone? | Conflicting 2020 sources | Send the link to yourself and check the server log |
| How do Norwegian registration tools (Checkin, Deltager) show options and payment status? | Only marketing pages available | Create a free test event and try it |
| Hardingasete's numbers, deadlines and price model | Not public | Ask the venue |
| Brevo/Postmark data storage in the EU | Not verified from primary pages | Check before choosing a provider in 2027 |

## 8. Sources

Accessed 2026-11-06 unless otherwise stated. Digests with full details and quotes are in [digests/](digests/).

| # | Supports | Publisher | Pub. date | Confidence |
|---|---|---|---|---|
| 1 | Joy parties, one answers for the group | [Joy help](https://withjoy.com/help/en/articles/8343360-adding-plus-ones-and-parties) | 2025-08-08 | high |
| 2 | Joy multi-event, specific guests | [Joy help](https://withjoy.com/help/en/articles/11085588-how-can-i-use-joy-to-manage-rsvps-and-schedules-for-multiple-events-when-not-everyone-is-invited-to-every-event) | 2025-08-08 | high |
| 3 | Joy RSVP deadline | [Joy help](https://withjoy.com/help/en/articles/15219057-set-an-rsvp-deadline) | 2026-08-07 | high |
| 4 | Joy RSVP settings, grace period, reminders | [Joy help](https://withjoy.com/help/en/articles/16241371-event-settings-rsvp) | 2026-10-02 | high |
| 5 | Joy custom/follow-up questions, Ask Once Per Household | [Joy help](https://withjoy.com/help/en/articles/8293305-customize-your-rsvp-questions) | undated | medium |
| 6 | Zola exact name match, lockout | [Zola help](https://help.zola.com/hc/en-us/articles/115002214951) | undated | medium |
| 7 | Zola events per guest | [Zola FAQ](https://www.zola.com/faq/360002575731-How-do-I-control-who-s-invited-to-what-And-how-can-I-control-who-RSVPs-to-what-) | undated (2024 screenshots) | high |
| 8 | Zola meal/adult-child totals | [Zola FAQ](https://www.zola.com/faq/115000345711-guest-list/115000790951-rsvp) | undated | medium |
| 9 | Greenvelope personal link, CSV export | [Greenvelope FAQ](https://card.greenvelope.com/faq) | undated | low |
| 10 | Zola cash funds 2.5% | [Zola FAQ](https://www.zola.com/faq/115002838152) | undated | medium |
| 11 | Joy card fee 3.5% | [Joy help](https://withjoy.com/help/en/articles/9794151) | undated | medium |
| 12 | Free website/RSVP, RSVPify | [Zola Expert Advice](https://www.zola.com/expert-advice/best-online-wedding-rsvp-tools) | 2026-04-17 | medium |
| 13 | "Name not found" in forums | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/rsvping-but-names-not-found/af78784e1277356a.html) | undated | medium |
| 14 | czue Party/Guest model, dashboard | [GitHub czue](https://github.com/czue/django-wedding-website) | undated | high |
| 15 | git-hitched Invite/Guest/Event/RSVP, cents | [GitHub fredbenenson](https://github.com/fredbenenson/git-hitched) | undated | high |
| 16 | WedSites households | [WedSites docs](https://docs.wedsites.com/rsvp/rsvp-faqs/how-do-households-rsvp-together) | undated | medium |
| 17 | planning.wedding Norwegian | [planning.wedding](https://planning.wedding/nb/guest-list/application) | undated | low |
| 18 | Norwegian deadline ~1 month | [Amelia Wedding (NO)](https://amelia-wedding.pl/no/blog/post/hvordan-sende-ut-bryllupsinvitasjoner) | 2024-03-14 | medium/low |
| 19 | Guests pay for accommodation (Scandinavia) | [Amelia Wedding (DA)](https://amelia-wedding.pl/da/blog/post/transport-og-overnatning-for-bryllupsgaester-2026-hvad-i-boer-arrangere-og-hvad-i-kan-droppe) | 2026 | medium |
| 20 | Wedding rates at Norwegian hotels | [Thon Hotels](https://www.thonhotels.com/event/pab-ina-folkedal-bryllup) | undated | medium |
| 21 | Blunders that annoy guests | [Klikk.no](https://www.klikk.no/kvinneguiden/bryllup/ti-tabber-som-irriterer-vettet-av-gjestene-2567894) | undated | medium |
| 22 | Speech order, toastmaster | [Klikk.no](https://www.klikk.no/mote/bryllup/slik-lykkes-du-som-toastmaster-2567311) | undated | medium |
| 23 | Swedish speech sign-up form | [Google Forms (private)](https://docs.google.com/forms/d/e/1FAIpQLSeUbJ-TTozKtwkJWf05o6Sy-DQybaEReYZL1VrSWLI_cTWF4Q/viewform) | 2026 | high/low |
| 24 | Ønskeskyen in Norway | [Ritzau](https://via.ritzau.dk/nyhedsrum/13562281/onskeskyen-norge/r) | undated | medium |
| 25 | Nobody answers, chasing | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/why-isnt-anyone-responding/236f7bc761f2effc.html) | 2019-11-08 | medium |
| 26 | Norwegian etiquette: phone non-responders | [Klikk.no](https://www.klikk.no/kvinneguiden/bryllupsetikette-2575330) | undated | medium |
| 27 | Zola can't handle families | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/zola-issues-advice-appreciated/275e8fe3908db9e7.html) | 2020-01-13 | medium |
| 28 | Strangers RSVPing | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/rsvp-on-zola-gone-wrong/f9f596dafccae34b.html) | 2020-03-03 | medium |
| 29 | Joy reviews 2026 | [Trustpilot](https://uk.trustpilot.com/review/withjoy.com?page=5) | 2026 | medium |
| 30 | Zola reviews 2026 | [Trustpilot](https://www.trustpilot.com/review/zola.com) | 2026 | medium |
| 31 | Collecting payment from guests | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/destination-wedding-guest-payment-collection-question/bd986b3a24e719bd.html) | 2023-01-26 | medium |
| 32 | Accommodation: tacky or not | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/lodging-accomodations-tacky-or-not/0d1f3247b044d96b.html) | undated | medium |
| 33 | Caterer deadlines | [Easy Weddings](https://www.easyweddings.com.au/WeddingCaterers/advice/caterers-dietary-requirements) + [WeddingWire](https://www.weddingwire.com/wedding-forums/final-count-1-month-prior-wth/782ccca5af0b20de.html) | undated | medium |
| 34 | Helpers share login | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/wedding-wire-website-control-users/e225c83cdaeb0a04.html) | 2018-07-09 | medium |
| 35 | Limited roles (WedSites) | [WedSites help](https://help.wedsites.com/en/articles/14456319-adding-user-to-wedding) | undated | low |
| 36 | Guests ask anyway; link sent digitally | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/no-one-using-wedding-website/5f85cb409fc69258.html) | 2017-06-01 | medium |
| 37 | Two kinds of guests | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/how-much-do-you-look-into-a-couples-wedding-website/383c5003fa077e69.html) | 2021-06 | medium |
| 38 | Can't find my name | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/rsvp-troubles-for-guests/e222c7b964152b27.html) | 2021-07 | medium |
| 39 | "I can't find my name" (vendor) | [WedSites docs](https://docs.wedsites.com/rsvp/rsvp-faqs/why-is-my-rsvp-not-working) | undated | medium |
| 40 | Older guests online / hybrid | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/online-rsvp/227c668762244223.html) | 2020-01 | medium |
| 41 | Usability for 65+ | [Nielsen Norman Group](https://www.nngroup.com/articles/usability-for-senior-citizens/) | 2019-09-08 | high |
| 42 | One question per page, Back link | [GOV.UK Design System](https://design-system.service.gov.uk/patterns/question-pages) | undated | high |
| 43 | Confirmation page | [GOV.UK Design System](https://design-system.service.gov.uk/patterns/confirmation-pages/) | undated | high |
| 44 | Paying when accommodation/food is "included" | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/asking-guests-to-pay-when-lodging-and-food-is-included/bb7ffd0022521b15.html) | 2023-03 | medium |
| 45 | Ask guests to pay accommodation thoughtfully | [A Practical Wedding](https://apracticalwedding.com/how-do-we-thoughtfully-ask-guests-to-pay-for-their-accommodations/) | 2021-03-31 | medium |
| 46 | Language switcher tests | [MediaWiki](https://www.mediawiki.org/wiki/Reading/Web/Desktop_Improvements/Repository/Language_Switching_User_Tests) | ~2021–22 | low/medium |
| 47 | Paper invitation, oldest generation | [Refinery29](https://www.refinery29.com/digital-wedding-invitations) | 2017-12-19 | medium |
| 48 | Token entropy, URL leakage, sessions | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | living | high |
| 49 | URL tokens, no-referrer, rate limiting | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html) | living | high |
| 50 | CSRF, GET without side effects | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) | living | high |
| 51 | Email scanners consume links | [GitHub supabase/auth #1214](https://www.github.com/supabase/auth/issues/1214) | 2025–26 | medium |
| 52 | Argon2id | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | living | high |
| 53 | Django console email | [Django docs](https://docs.djangoproject.com/en/5.2/topics/email/) | 5.2 docs | high |
| 54 | Mailpit | [Mailpit](https://mailpit.axllent.org/) | undated | high |
| 55 | Resend free tier | [Resend](https://resend.com/pricing) | current | high |
| 56 | Resend data stored in the US | [Resend docs](https://www.resend.com/docs/dashboard/domains/regions.md) | current | high |
| 57 | Postmark free tier | [Postmark](https://postmarkapp.com/pricing) | current | high |
| 58 | Brevo free tier | [Brevo help](https://help.brevo.com/hc/en-us/articles/208580669) | undated | medium |
| 59 | SQLite suitability | [SQLite](https://www.sqlite.org/whentouse.html) | undated | high |
| 60 | Django admin internal tool | [Django docs](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/) | 6.1 docs | high |
| 61 | Prisma v7 seeding | [Prisma docs](https://www.prisma.io/docs/orm/prisma-migrate/workflows/seeding) | v7 docs | high |
| 62 | Laravel prerequisites, login rate limiting | [Laravel docs](https://laravel.com/docs/12.x/starter-kits) | 12.x docs | high |
| 63 | Optimistic locking pattern | [AppMaster](https://appmaster.io/blog/optimistic-locking-busy-admin-tools) | 2025-06-11 | medium |
| 64 | Hetzner prices | [Hetzner](https://www.hetzner.com/cloud/) | current | high |
| 65 | Fly.io prices | [Fly.io](https://docs.fly.io/about/pricing) | current | high |
| 66 | Render free tier | [Render](https://render.com/docs/free) | current | high |
| 67 | Django versions | [Django](https://www.djangoproject.com/download/) | 2026 | medium |
| 68 | Household exemption, Recital 18 | [gdpr-info.eu](https://gdpr-info.eu/recitals/no-18/) | 2016 | high |
| 69 | Lindqvist, Ryneš | [EU Law Analysis](https://eulawanalysis.blogspot.com/2014/12/bringing-data-protection-home-cjeu.html) | 2014-12 | medium |
| 70 | Art. 9 health data | [gdpr-info.eu](https://gdpr-info.eu/art-9-gdpr/) | 2016 | high |
| 71 | Datatilsynet special categories | [Datatilsynet](https://www.datatilsynet.no/rettigheter-og-plikter/virksomhetenes-plikter/om-behandlingsgrunnlag/spesielt-om-sarlige-kategorier-av-personopplysninger/) | undated | medium |
| 73 | Art. 7 conditions for consent | [gdpr-info.eu](https://gdpr-info.eu/art-7-gdpr/) | 2016 | high |
| 74 | Vipps fees between private persons | [Vipps MobilePay help](https://help.vippsmobilepay.com/nb-NO/articles/does-it-cost-anything-to-send-money) | © 2026 | high |
| 75 | Vipps private terms v1.5 (QR, requests, 2027 fee) | [Vipps MobilePay](https://vippsmobilepay.com/terms-and-conditions/no/private-user) | 2026-10-20 | high |
| 76 | Vipps private use only | [Vipps](https://vipps.no/privat-betalinger) | © 2026 | high |
| 77 | Vipps boks fee | [Vipps](https://vipps.no/kasse) | undated | high |
| 78 | Likestillings- og diskrimineringsloven §§ 17–18 | [Lovdata](https://lovdata.no/dokument/NL/lov/2017-06-16-51/KAPITTEL_3) | 2017 (amended) | high |
| 79 | Who must comply with UU rules | [Uutilsynet](https://www.uutilsynet.no/regelverk/regelverk/266) | undated | high/medium |
| 80 | WCAG 2.2 | [W3C](https://www.w3.org/TR/WCAG22/) | 2024-12-12 | high |
| 81 | Error summary | [Designsystemet](https://designsystemet.no/no/components/docs/error-summary/overview) | undated | high |
| 82 | Tito "Mark as paid" | [Tito docs](https://go.tito.io/docs/events/mark-an-order-as-paid) | undated | high |
| 83 | Eventbrite add-ons as attendees | [Donorfy help](https://help-donorfy.theaccessgroup.com/en/articles/13186035-eventbrite-integration-updates) | 2024 | medium |
| 84 | Checkin (Norwegian registration tool) | [Checkin](https://www.checkinevent.com/pameldingssystem) | undated | low |
| 85 | Check answers | [GOV.UK Design System](https://design-system.service.gov.uk/patterns/check-answers/) | undated | high |
| 86 | Order review, stable total | [Baymard Institute](https://baymard.com/guidelines/2387-order-review-steps-for-multistep-checkouts) | undated/2023 | medium |
| 87 | Meta crawler for shared links | [Meta for Developers](https://developers.facebook.com/docs/sharing/webmasters/web-crawlers/) | undated | high |
| 88 | WhatsApp link previews | [Meta for Developers](https://developers.facebook.com/documentation/business-messaging/whatsapp/link-previews/) | undated | high |
| 89 | Slackbot link expanding | [Slack](https://api.slack.com/robots) | undated | high |
| 90 | iMessage preview (disputed) | [MacRumors](https://www.macrumors.com/2020/10/26/link-previews-may-lead-to-security-vulnerabilities/) vs [Graham Cluley](https://grahamcluley.com/apple-messages-exposing-privacy-previews-link/) | 2020 | low |
| 91 | False opens from scanners | [QuickMail help](https://help.quickmail.com/deliverability/tracking-delay-to-avoid-false-opens-and-clicks/) | undated | medium |
| 92 | Relatives cannot consent for adults | [Helsedirektoratet](https://www.helsedirektoratet.no/rundskriv/bilder-film-og-lydopptak-i-helse-og-omsorgstjenesten/rettslige-rammer/samtykke-og-innhenting-av-samtykke) | 2025-02-03 | medium |
| 93 | EDPB Guidelines 05/2020 on consent | [EDPB](https://www.edpb.europa.eu/system/files/documents/files/file1/edpb_guidelines_202005_consent_en.pdf) | 2020-05-04 (v1.1) | high |
| 94 | Art. 13 duty to inform | [gdpr-info.eu](https://gdpr-info.eu/art-13-gdpr/) | 2016 | high |
| 95 | Art. 28 processor | [gdpr-info.eu](https://gdpr-info.eu/art-28-gdpr/) | 2016 | high |
| 96 | Art. 5 minimisation, storage limitation | [gdpr-info.eu](https://gdpr-info.eu/art-5-gdpr/) | 2016 | high |
| 97 | Datatilsynet: household exemption is narrow | [Datatilsynet](https://www.datatilsynet.no/regelverk-og-verktoy/lover-og-regler/om-personopplysningsloven-og-nar-den-gjelder/) | undated | medium |
| 98 | Datatilsynet: processor agreement | [Datatilsynet](https://www.datatilsynet.no/rettigheter-og-plikter/virksomhetenes-plikter/behandlingsansvarlig-og-databehandler/) | undated | medium |
| 100 | Account number 11 digits | [DNB Eufemia](https://unpkg.com/@dnb/eufemia@11.0.0/docs/uilib/extensions/forms/Value/BankAccountNumber.md) | v11 | medium |
| 101 | KID | [Store norske leksikon](https://snl.no/KID-nummer) | undated | medium/low |
| 102 | Tax depends on purpose | [Skatteetaten](https://www.skatteetaten.no/contentassets/0ba2ca32044049818117080b319868fb/skatteregler-ved-crowdfunding-pdf.pdf) | 2013-12-04 | medium |
| 104 | The Knot events per guest | [The Knot Help Center](https://helpcenter.theknot.com/hc/en-us/articles/9718161760148) | undated | medium |
| 105 | Google Forms used as an RSVP form (Sweden) | [Google Forms (private)](https://docs.google.com/forms/d/17mDGDlUNZizMWAPHsFO1-Od2QumWa2LWbHIPKo4yDo8/viewform) | undated | medium |
| 106 | Marking non-responders as "no" | [AOL (People)](https://www.aol.com/bride-says-couple-cant-attend-090000012.html) | undated | low |
| 107 | Guests add extra people | [WeddingWire forums](https://www.weddingwire.com/wedding-forums/help-guests-rsvp-for-more-than-invited/2e693a5e4c22b900.html) | undated | low/medium |
| 108 | Collecting payment for a cabin weekend | [The Knot Community](https://forums.theknot.com/discussion/1040578/collecting-money-from-guests-for-weekend-wedding-accomodations) + [couple's Zola FAQ](https://zola.com/wedding/joinusinthewoods/faq) | undated | low/medium |
| 109 | Sports club collects allergies for events | [Orkanger IF](https://www.orkanger-if.no/assets/Uploads/Personvernerklaering-OIF.pdf) | undated | low/medium |
| 103 | NIF: consent from the person for registration | [Norges idrettsforbund](https://www.idrettsforbundet.no/contentassets/3baa66d1574c4465a31e5c3a179f5d28/veileder-for-informasjonssikkerhet-i-idretten20.12.2017_s.pdf) | 2017-12-20 | low/medium |

## 9. Staleness map

Computed with `recon_kit.py staleness` (windows: features/prices/payment 3 months, versions 6, security 12, sentiment 18, conventions/UX research/accessibility 36, regulatory: check at every use).

| Claim | Class | Pub. | Re-check |
|---|---|---|---|
| Joy deadline features [4] | feature | 2026-10 | 2027-01 |
| Vipps fees and terms [74][75] | payment | 2026-10 | 2027-01 |
| No product shows what guests owe [10]; name-search problems [6] | feature | 2026-11 | 2027-02 |
| Email and hosting prices [55][56][57][58][64][65][66] | pricing | 2026-11 | 2027-02 |
| Framework versions [61][62][67] | version | 2026-11 | 2027-05 |
| OWASP baseline [48][52], preview crawlers [87][88][89] | security | 2026-11 | 2027-11 |
| WCAG 2.2 [80] | accessibility | 2024-12 | 2027-12 |
| **Already stale:** US etiquette on paying [44][45] (2021–23), NN/g 65+ [41] (2019) | sentiment / UX | — | use with caution |
| **Regulatory:** consent and household exemption [73][92][93][97] | regulatory | — | check again before production in 2027 |

Earliest re-check: **January 2027** (Joy features and Vipps). Before production in 2027, prices, Vipps terms and the regulatory points must be checked again (Refresh).

