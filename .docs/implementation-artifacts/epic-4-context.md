# Epic 4 Context: Guests change their answer until the deadline locks it

<!-- Generated from planning artifacts. Regenerate with compile-epic-context if planning docs change. -->

## Goal

A household that has answered can open its sent answer, change it and send again until 23:59 Norwegian time on the deadline day, and sees who answered last. A member never overwrites another member's newer answer without seeing it first. After the deadline guests can only look at their answer, while the couple can still fill in or change any household's answer with the same form. The couple change the deadline, prices and contact details in Settings, with a confirmation step. The numbers the couple give Hardingasete stay fixed once the deadline has passed.

## Stories

- Story 4.1: See or change the answer before the deadline
- Story 4.2: No answer is overwritten without anyone seeing it
- Story 4.3: The answer locks at the deadline
- Story 4.4: The couple fills in or changes any household's answer
- Story 4.5: The couple changes the deadline, prices and contact details

## Requirements & Constraints

- Before the deadline the status block offers «Se eller endre svar», which opens the one form with the sent answers filled in; the form's top shows who last changed the answer and when.
- «Changed» is a household marker set only when a sent answer's content really changes (after normalisation), by a guest or the couple, or on consent withdrawal; the first answer, payment reports and an identical re-send never set it.
- No silent overwrite: a draft older than the household's revision is refused and the guest sees the newer answer (who, when, what differs) before sending again; consent «Ja» never carries across a revision change.
- The deadline is a date; guests may send until 23:59:59 Oslo time that day. It locks only guest sends that change answer content; consent withdrawal, «Jeg har betalt» and every couple service are never locked.
- A double tap on a send, also a re-send, shows the receipt and never a conflict with oneself; the revision rises once.
- The couple's override keeps the guests' own answer rules but records the admin as author and shows «Rikke og Valdemar», never a username.

## Technical Decisions

- One form in `wedding/rsvp/`, mounted for guests in `guests/views.py` and later for the couple in `dashboard/`; step handlers are shared, so mount-specific behaviour is passed in, not copied.
- Only services in `wedding/services/` write; each service takes an explicit actor and is one transaction. `Household.changed_at` is set by one helper called from those services (AD-19).
- The deadline check is the one function `is_past_deadline(deadline, now)` in `wedding/rules/`; tests cover both sides of the boundary (AD-11).
- Submission ids make repeats safe: the repeat check runs before the revision check (AD-20); a refused write records none.
- Revision (`Household.revision`) goes up on every send; the draft carries the revision it started from (AD-9).
- Counts, totals and status are computed by rules, never stored (AD-2, AD-4). Expected numbers live in `wedding/fixtures/expected.toml`; lock cases are added there in Story 4.3.
- `wedding/rsvp/views.py` is 1,528 lines; Story 4.4 splits it before the second mount. Keep earlier Epic 4 stories from growing it.

## UX & Interaction Patterns

- Status block (G2): «Dere kan endre svaret fram til <weekday date> kl. 23:59.» (du/dere rule) and the primary button «Se eller endre svar»; after the deadline the button becomes «Se hele svaret» (Story 4.3).
- Top of the form when answered: info notice «Sist endret av <name>, <date> kl. <time>»; a conflict is a warning notice with who, when and what differs (Story 4.2).
- Confirmation before risky admin writes: a first POST that writes nothing, then a dialog or confirm page (Story 4.5).
- Touch targets at least 44px, em breakpoints, usable at 20px text and 180px width.

## Cross-Story Dependencies

- 4.2 builds on 4.1's change flow and replaces the simple conflict text from Story 2.6c.
- 4.3 needs the status block and the reopened form from 4.1; 4.4 mounts the same form for the couple and uses 4.1's `changed_at` helper and 4.2's conflict notice.
- Epic 5 (payment reports) must not set `changed_at`; Story 7.2 (consent withdrawal) does.
