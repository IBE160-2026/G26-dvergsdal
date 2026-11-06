# D1 round 2 — Paid add-ons from adjacent tools, summary/confirmation UX, link previews

Scope: three questions supporting a PRD for a wedding website where guests choose paid options per person (cabin, Friday dinner, Saturday and Sunday breakfast). Payment is made offline (bank transfer or Vipps), and the couple marks households as paid by hand. Budget used: about 20 tool calls. Many primary pages returned only titles or no dates. This is noted for each claim.

## Findings

### Q1. Event-registration tools with paid add-ons and offline payment

- **Claim:** Tito lets the organiser record an offline payment (cheque, cash or bank transfer) on an unpaid order. The organiser opens the order and chooses Actions → "Mark as paid". On bank-transfer orders there is also a "Mark as paid" button next to the amount. A second page asks for confirmation. | **Source:** Task · Orders – Mark an order as paid | **Publisher:** Tito | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://go.tito.io/docs/events/mark-an-order-as-paid | **Confidence:** high | **Class:** feature
- **Claim:** In Tito, confirming "Mark as paid" issues the tickets, sends the buyer a confirmation email and closes the payment link so the buyer cannot pay twice. Tito says "You can't undo this". A paid order with no money behind it can only be cancelled, not refunded. The page shows only two states (unpaid and paid). It describes no partial payment and no payment reference. | **Source:** same as above | **Publisher:** Tito | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://go.tito.io/docs/events/mark-an-order-as-paid | **Confidence:** high | **Class:** feature
- **Claim:** In Eventbrite, the organiser creates add-ons under "Add tickets → Add-Ons". Each add-on has a price, a sales channel and a minimum and maximum per order, and can be hidden instead of deleted. (This comes from a search-result summary of the Eventbrite help article. The article itself was not opened.) | **Source:** Organizing an event (help article 624500) | **Publisher:** Eventbrite | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://www.eventbrite.com/help/en-us/articles/624500/ | **Confidence:** medium | **Class:** feature
- **Claim:** Eventbrite treats ticket add-ons as separate "Attendees", with no field that says whether an attendee is a person or an item. Eventbrite also changed checkout so that payment is taken before attendee details are collected. This is third-party integration documentation, dated 2024 and older than 12 months. | **Source:** Eventbrite integration updates | **Publisher:** Donorfy (The Access Group) | **Pub date:** 2024 (per search snippet) | **Accessed:** 2026-11-06 | **URL:** https://help-donorfy.theaccessgroup.com/en/articles/13186035-eventbrite-integration-updates | **Confidence:** medium | **Class:** feature
- **Claim:** Eventbrite's own add-ons article is marketing only ("Delight your attendees…", "increase revenue"). It says nothing about how add-ons appear at checkout, per order or per attendee, or how totals are shown. | **Source:** Sell More Than Just Tickets With Add-ons | **Publisher:** Eventbrite | **Pub date:** undated (marketing) | **Accessed:** 2026-11-06 | **URL:** https://www.eventbrite.com/blog/solutions/ticket-add-ons/ | **Confidence:** high (that the page is marketing only) | **Class:** feature
- **Claim:** Checkin (checkinevent.com, formerly checkin.no) markets forms that "adapt to participants' choices automatically" and lists card, Vipps and invoice payment with automatic payment tracking. This is a marketing page, and no help documentation about add-ons was found. | **Source:** Spar tid og skap bedre opplevelser med Checkin | **Publisher:** Checkin AS | **Pub date:** undated (marketing) | **Accessed:** 2026-11-06 | **URL:** https://www.checkinevent.com/pameldingssystem | **Confidence:** low | **Class:** feature
- **Claim:** Deltager.no's organiser terms (a template copy on Lawinsider, not the live site) let Deltager charge the organiser for invoice production (email, EHF, post) and reminder fees when participants do not pay. This shows that invoice payment with reminders exists, but nothing was found about how add-ons are presented. | **Source:** Vilkår og betingelser for bruk av deltager.no for Arrangører | **Publisher:** Lawinsider (copy of Deltager AS terms) | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://lawinsider.com/nb/contracts/bu2r2YOY1D6 | **Confidence:** low | **Class:** feature
- **Claim:** Spond Club's help centre has a "Payment request" collection. Its articles include "Payment Details for Each Recipient", "Sending Payment Reminders to Members", "After a payment has been sent out" and "instalments and flexible payments". The article text was not readable, so it is unverified whether Spond supports manual "mark as paid". | **Source:** Payment request (collection) | **Publisher:** Spond | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://help.spond.com/club/en/collections/463177-payment-request | **Confidence:** low | **Class:** feature

### Q2. Summary and confirmation UX

- **Claim:** GOV.UK's "Check answers" pattern puts one check-answers page just before the confirmation page for small and medium transactions. It gives these rules:
  - Use a page title that says what to do, for example "Check your answers before sending your application".
  - Say that the transaction is not complete until the user confirms.
  - Show only the sections that apply to the user.
  - Name the submit button after the action, for example "Send your claim form".
  - Put a "Change" link next to each item, with hidden screen-reader text that names the item.
  - Pre-fill earlier answers, and return the user to the check page after a change.
  - Show "Not provided" for optional questions the user skipped.
  
  The pattern says these pages increase users' confidence and reduce errors. | **Source:** Check answers | **Publisher:** GOV.UK Design System (GDS) | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://design-system.service.gov.uk/patterns/check-answers/ | **Confidence:** high | **Class:** ux-research
- **Claim:** GOV.UK's "Confirmation pages" pattern requires these elements:
  - a reference number, if the transaction has one
  - what happens next and when
  - contact details
  - links to what the user is likely to need next
  - a way to save a record of the transaction
  
  Research cited by the pattern found that some users bookmark the confirmation page and keep it as a receipt. Services should therefore let users return to it, or handle bookmarked links helpfully. Interactive elements inside the green confirmation panel fail accessibility unless the contrast is at least 3:1. | **Source:** Confirmation pages | **Publisher:** GOV.UK Design System (GDS) | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://design-system.service.gov.uk/patterns/confirmation-pages/ | **Confidence:** high | **Class:** ux-research
- **Claim:** Baymard's checkout testing found the following about the order-review step. This comes from free article summaries, because the full guideline (#2387) is behind a paywall.
  - Users often spot errors at the review step and want to fix them there.
  - Many sites send users backwards to edit, and Baymard recommends edit links next to each group of data.
  - Some users mistake the review page for the confirmation page and leave without ordering. The "Place order" button is the main thing that tells the two apart, and this confusion caused up to about 10 % of mobile abandonments in the worst cases.
  - An unexpected change in the total at review makes users stop recognising the order. | **Source:** Order Review & Confirmation guidelines; Office Depot order review article | **Publisher:** Baymard Institute | **Pub date:** undated / accordion article Sept 2023 (older than 12 months) | **Accessed:** 2026-11-06 | **URL:** https://baymard.com/guidelines/2387-order-review-steps-for-multistep-checkouts ; https://baymard.com/blog/office-depot-order-review-experience | **Confidence:** medium | **Class:** ux-research

### Q3. Link previews and personal or secret links

- **Claim:** Meta's crawler `facebookexternalhit/1.1` fetches any URL shared on Meta apps by copy and paste, which includes Messenger. It reads and caches the title, description and thumbnail. It sends a `Range` header, needs Open Graph tags within the first 1 MB, and "may bypass robots.txt" for security checks. Meta recommends allowlisting by user agent or IP. | **Source:** The Meta Web Crawler | **Publisher:** Meta for Developers | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://developers.facebook.com/docs/sharing/webmasters/web-crawlers/ | **Confidence:** high | **Class:** security
- **Claim:** WhatsApp crawls the URL "on behalf of the sender" with an HTTP GET while the message is being composed, before it is sent. The user agent is `WhatsApp/2.x.x.x A|I|N`. WhatsApp needs non-empty `og:title`, `og:description` and `og:url` within the first 300 KB, and `og:image` should be under 600 KB. | **Source:** Link previews (WhatsApp Business Platform) | **Publisher:** Meta for Developers | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://developers.facebook.com/documentation/business-messaging/whatsapp/link-previews/ | **Confidence:** high | **Class:** security
- **Claim:** Slackbot (`Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)`) fetches part of the page with Range headers whenever a link is posted. It reads oEmbed, Twitter Card and Open Graph tags, caches results globally for about 30 minutes and does not honour robots.txt. | **Source:** Slackbot / robots | **Publisher:** Slack | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://api.slack.com/robots | **Confidence:** high | **Class:** security
- **Claim:** iMessage/Messages previews: sources conflict about which device fetches the page.
  - A 2020 MacRumors report on the Mysk research says iMessage and WhatsApp generate the preview on the sender's device.
  - Graham Cluley (2020, citing Ross McKillop) says Messages fetches from the recipient's devices automatically, without a click.
  - Apple's TN3156 "Create rich previews for Messages" was found, but its body could not be read.
  
  **Unverified for current iOS.** | **Source:** Link Previews in Popular Messaging Apps May Lead to Security Vulnerabilities; Apple Messages could be exposing your privacy when it previews a link | **Publisher:** MacRumors; Graham Cluley | **Pub date:** 2020-10-26; 2020 (older than 12 months) | **Accessed:** 2026-11-06 | **URL:** https://www.macrumors.com/2020/10/26/link-previews-may-lead-to-security-vulnerabilities/ ; https://grahamcluley.com/apple-messages-exposing-privacy-previews-link/ | **Confidence:** low | **Class:** security
- **Claim:** iMessage link-preview requests that hit Instagram were redirected to Instagram's login page. This shows that a preview fetcher receives whatever the server returns to an unauthenticated GET. | **Source:** Instagram to fix iMessage link previews bug | **Publisher:** iMore | **Pub date:** undated (older) | **Accessed:** 2026-11-06 | **URL:** https://www.imore.com/instagram-fix-imessage-link-previews-bug | **Confidence:** low | **Class:** security
- **Claim:** In February 2026, PromptArmor reported that link-preview fetchers in messaging apps make zero-click requests to any URL in a message. This turned URLs that carry data in the query string into a data-leak channel, without anyone clicking. This is a general proof that a preview fetch is equivalent to a visit. | **Source:** AI agents spill secrets just by previewing malicious links | **Publisher:** The Register | **Pub date:** 2026-02-10 | **Accessed:** 2026-11-06 | **URL:** https://www.theregister.com/2026/02/10/ai_agents_messaging_apps_data_leak/ | **Confidence:** medium | **Class:** security
- **Claim:** Email security gateways follow embedded URLs, and load tracking pixels, to check for malicious redirects. This produces false "opens" and "clicks", often within seconds of delivery. Vendors filter these out with timing heuristics or a tracking delay, and say opens should be treated as unreliable. These are vendor help pages and the size of the effect is disputed. | **Source:** Tracking delay to avoid false opens and clicks; Bot click filtering | **Publisher:** QuickMail; Replies (Intercom help) | **Pub date:** undated | **Accessed:** 2026-11-06 | **URL:** https://help.quickmail.com/deliverability/tracking-delay-to-avoid-false-opens-and-clicks/ ; https://intercom.help/getreplies/en/articles/14884313-bot-click-filtering | **Confidence:** medium | **Class:** security

## Patterns worth borrowing (synthesis)

1. **Two payment states plus a manual "Mark as paid" action, as in Tito.** The admin marks a household as paid with a confirmation step, and the guest sees the status change. Tito makes this irreversible. For a wedding, an "undo" or "unmark" option is probably better, because the couple will make mistakes. Partial payment is not modelled in Tito, so treat "partly paid" as a deliberate PRD decision rather than an industry default.
2. **Store the household's options per person, not as separate "attendees".** Eventbrite treats each add-on as a separate attendee, which makes the attendee list ambiguous. Store each choice on the person and calculate household totals from those choices.
3. **Check-answers page before submitting, as in GOV.UK and Baymard.** List each person's options with their prices, then the household total. Put a "Change" link next to each person. Use an action-named button such as "Send booking". Say clearly that nothing is booked until the guest sends it. Keep the total stable, with no surprises at the review step.
4. **Confirmation page that works as a receipt, as in GOV.UK.** Show a payment reference, for example a household code to write in the bank-transfer or Vipps message. Show the amount, account or Vipps number, the deadline, what happens next (the couple marks it as paid) and who to contact. Guests' personal links should always reopen this status page, because users bookmark confirmation pages.
5. **Treat every preview fetch as a visit.** Messenger (via facebookexternalhit), WhatsApp and Slack fetch the URL themselves. iMessage may also fetch it, which is unverified. Therefore:
   - Put no guest or household name in `<title>` or the `og:` tags. Serve a generic Open Graph title, description and image, for example "Rikke & X – bryllup".
   - Do not count a GET from known preview user agents (`facebookexternalhit`, `WhatsApp/`, `Slackbot-LinkExpanding`) or a HEAD or Range request as "guest opened link".
   - Never let a GET change state. Opening the link must not RSVP or submit anything.
6. **Email "opened" statistics are unreliable.** If the couple wants a "has seen the invitation" indicator, base it on an action the guest takes, such as saving a choice, not on page loads.

## Leads not chased

- Tito's own "bank transfer" payment-option documentation (reference numbers, instructions shown to the buyer).
- Eventbrite's "Pay by invoice / offline payment" help article and how it shows pending orders.
- Ticketbutler (no search was spent on it).
- Spond's article "Payment Details for Each Recipient" (manual marking, reminders).
- NN/g articles on confirmation pages and order summaries (no search was spent).
- The text of Apple TN3156 (https://developer.apple.com/documentation/technotes/tn3156-create-rich-previews-for-messages), to settle which device fetches the iMessage preview and which user agent it uses.
- Microsoft Defender Safe Links documentation (whether it pre-fetches URLs in email).
- Splitwise-style cost splitting.

## Looked for but could not find

- How Deltager.no presents add-ons with prices, running totals and payment status. Only a template copy of the terms was found.
- Checkin and Hoopla help documentation about add-on products. Only Checkin's marketing page was found, and Hoopla searches returned unrelated "hoopla digital".
- A primary, current Apple statement on whether iMessage previews are fetched by the sender or the recipient.
- Any documented "partially paid" state in Tito.
- Publication dates on almost all primary help or design-system pages (all undated).
