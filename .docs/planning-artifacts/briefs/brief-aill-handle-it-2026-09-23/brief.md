---
title: "Product Brief: AI'll handle it"
status: final
created: 2026-09-23
updated: 2026-09-26
---

# Product Brief: AI'll handle it

## Executive Summary

AI'll handle it is a wedding website that is also the invitation, for Rikke's wedding weekend at Hardingasete in Hardanger on 27 May 2028. Each of about 70 guests gets a personal link. The first time they open it, a letter unfolds like a paper invitation and leads into a site with everything about the weekend: the programme from Friday's mountain hike to Sunday breakfast, practical details, and house rules. Households answer together in one simple form covering attendance, meals, cabin beds, allergies and arrival. Guests see exactly what their choices cost and how to pay, and can send any remaining question straight to the couple.

It replaces the usual approach: a photo invitation sent over Messenger, free-text replies, and an Excel sheet. That approach loses allergies and bed counts, costs the couple hours of chasing and checking, and can't keep 70 people up to date when plans change. Here, the couple gets one admin overview to take to the venue, with attendance, meal counts, beds, allergies, payments and who hasn't opened their invitation yet.

The project is also Rikke's solo full-stack project for IBE160 Programmering med KI at Høgskolen i Molde, due mid-December 2026. The name refers to how it is built, with AI as a development partner. The site itself has no AI features. The course version is meant to be the real product, with a year of testing before invitations go out in about December 2027.

## The Problem

A three-day wedding weekend with about 70 guests means many details per guest: whether they are coming, which meals they want across three days (Friday dinner, Saturday and Sunday breakfast), whether they need a cabin bed, allergies and dietary needs, and what they owe. Guests belong to households and couples, and one person often answers for several people.

The default way to handle this is a photo of an invitation sent by Messenger, email and text, with guests replying in free text and the couple copying answers into Excel. This breaks down in predictable ways:

- **Information gets lost or garbled.** Replies are scattered across channels and written differently by everyone. Missing an allergy means a guest gets food they cannot eat. Missing a bed count means a guest has nowhere to sleep.
- **The couple spends hours chasing, checking and re-typing.** Every answer has to be found, read, interpreted and entered by hand, then double-checked against the numbers sent to the venue.
- **Guests get confused.** The programme, prices, dress codes and practical details live in a single image or a long message that is hard to look up later.
- **Changes don't reach everyone.** When a time, price or plan changes, the couple has to message every guest again and hope they read it.

## The Solution

Each guest gets a personal link. The first visit opens with the letter animation, and later visits go straight to the site. Guests are grouped into households, so one person can answer for the whole family.

**For guests**, the site is the one place for everything about the weekend: the programme from Friday's hike to Sunday breakfast, practical information, house rules (child-free, as little phone use as possible), an introduction to the couple, and a no-pressure gift list. Guests answer in one simple form: whether they're coming, meals, cabin bed, allergies, expected arrival and the Friday hike. They see exactly what their choices cost and how to pay by bank transfer or Vipps. If something isn't clear, they can send a question to the couple from the site.

**For the couple**, an admin area replaces the Excel sheet. It shows who is coming and who hasn't answered or even opened their link, meal counts for every meal, beds needed, allergies by name, who owes what and who has paid, guest questions, and speech sign-ups for the toastmaster. Answers lock at the RSVP deadline so the numbers stay fixed. The couple can always override: edit answers, move people between households, or remove a guest.

## Who This Serves

- **Guests (about 70, all ages).** Some are confident on their phones, some are not. A few may not speak Norwegian. They need to understand the weekend, answer once, and know what they owe. Success means they never have to ask the couple something the site already answers.
- **The couple (Rikke and partner).** They need numbers they can trust when talking to Hardingasete, and to stop chasing replies. Success means one screen replaces Excel, the message threads and the double-checking.
- **Helpers (toastmaster, maid of honour, best man).** They share the admin view, so they can follow what concerns them, such as speech sign-ups for the toastmaster, without going through the couple.

## What Makes This Different

Free services like Joy, Zola and The Knot already handle a basic RSVP. Their shape doesn't fit this wedding:

- **Households answer together.** Each guest has a personal link, but a family or couple can answer as one.
- **A three-day weekend with paid add-ons.** Guests pick individual meals and cabin nights, see the exact price, and pay the couple by bank transfer or Vipps, which is common in Norway.
- **An invitation that feels like one.** A letter unfolds the first time a guest opens their link.
- **Norwegian first, with the couple's own look.** Sage green, soft white and dark wood, not a template.

The honest advantage isn't technology. It's fit. This is built for exactly one wedding, by someone who knows every guest. It avoids paying for, or compromising with, a generic product. It's also a learning project that ends in something that will actually be used.

## Success Criteria

**Course delivery (mid-December 2026)**
- The full guest flow works end to end on a phone: open personal link, see the letter, RSVP for the household, see the price and how to pay.
- The admin overview shows correct counts (attendance, meals, beds, allergies, payments) for a test guest list.
- A guest question sent from the site shows up in the admin view and in the couple's email.
- A complete prompt log backs the reflection report.

**Easy to use for everyone**
- An older relative who is not comfortable with technology completes the RSVP for their household on their own phone without help, in under 10 minutes.
- The couple can find any number Hardingasete asks for in under a minute.

**The real wedding (invitations about December 2027, wedding 27 May 2028)**
- 90% of households answer through the site before the RSVP deadline, without being chased.
- Zero allergy or bed mistakes at Hardingasete.
- The couple never opens Excel for guest logistics.
- Few guests message the couple with questions the site already answers.

## Scope

**In: delivered mid-December 2026 as the real, production-ready product**
- Personal link per guest; households and couples, with one person answering for all.
- Letter-opening invitation on the first visit; straight to the site on later visits.
- Information pages: weekend programme, practical info (address, times, dress codes, transport), about the couple, house rules, gifts.
- RSVP for each guest in the household, filled in by any one member: attendance, meals, cabin bed, allergies, expected arrival, Friday hike, and consent to share with the admin team. Shows price and bank/Vipps payment details. Locks at the RSVP deadline.
- Admin for the couple and helpers (full access for all): login; overview of attendance, meal counts, beds, allergies, payments and opened links; editing and overrides; guest questions, also forwarded to the couple's email; speech sign-ups.

**Stretch: if time allows, or during 2027 before invitations go out**
- Email or SMS notifications to guests when information changes.
- An English version of the site, switched with a language button at the top. Until then, guests who don't read Norwegian ask the couple directly.

**Out**
- Online payment. Guests pay the couple by bank transfer or Vipps outside the site.
- The site sending invitations. The couple sends each link by Messenger, SMS or email.
- Guest accounts and passwords. The personal link is the login.

**Constraints and open questions**
- Solo developer, early in learning to code, about 12 weeks to the deadline.
- Must be full-stack with a database (course requirement). An AI feature in the site is not required. AI is used in the development process and documented in the prompt log.
- Allergies are health data under GDPR. Handled by explicit guest consent.
- The site must stay online and maintained until mid-2028. The couple owns hosting and cost.
- Open: the form of the gift list (static list, external link, or gifts guests can reserve).
- Open: whether sending email costs anything. If it does, decide later how to handle it.

## Vision

The goal is a great weekend and a stress-free run-up to it. Guests arrive knowing what to expect, having answered once. The couple spends the last months planning the celebration, not chasing replies.

If time allows after the wedding, the site could become a keepsake: guests share photos and the couple posts a thank-you.
