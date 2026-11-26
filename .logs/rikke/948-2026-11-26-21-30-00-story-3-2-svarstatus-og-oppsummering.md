# Story 3.2 — Svarstatus og oppsummering

## 2026-11-26 kl. 21:30 — Rikke

### Oppgave
Del av den uovervåkede goal-kjøringen. Rikkes goal-prompt står ordrett i [973-loggen](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Intensjonen for bmad-build-auto var ordrett: «Story 3.2 i .docs/planning-artifacts/epics.md». Oversikt (`/admin/`) skal vise svarstatus og oppsummeringen med tallene Hardingasete trenger (FR-48, FR-54, FR-73, FR-74, NFR-2, AD-2, AD-18, UX-DR39/40/49).

### Plan
- Spec: [spec-3-2-answer-progress-and-the-summary.md](../../.docs/implementation-artifacts/spec-3-2-answer-progress-and-the-summary.md), skrevet av en planleggeragent. Implementering ved en egen agent (stoppet av bruksgrensen og gjenopptatt), fire gjennomgangsagenter og nettleserkjøring i Edge med Playwright.
- Runner-regel fra retrospektivet for epic 2: første funksjonscommit delt opp, slik at ingen commit passerer cirka 600 endrede linjer.

### Resultat
**Hva KI foreslo, og hva som ble godtatt, endret eller avvist**
- Planleggeren foreslo at hvert tall er lengden på en id-liste fra en regel i `wedding/rules/summary.py`, at `allergy_state` og `payment_status` lages nye, og at tellinger er ren tekst til story 3.3 (ingen døde lenker). Godtatt.
- Synnes trukne samtykke lastes først i story 7.2, så tre allergitall avviker fra `expected.toml`. Planleggeren foreslo en navngitt konstant `SYNNE_UNTIL_7_2` i testene i stedet for å endre fasiten. Godtatt (avgjort av Claude).
- Implementereren la til regelene `all_households` og `answered_households` og en ekstra rad «Kommer ikke» i turpanelet. Godtatt og ført i EXPERIENCE.md.
- Gjennomgangen ga 26 funn: 8 rettet, 7 utsatt og 11 avvist med begrunnelse i spec-ens triagelogg.
  - Rettet: etikett som ga 183 px bredde ved 180 px med 20 px tekst (funnet i Edge, ikke av noen gjennomgangsagent), manglende test av samtykke-lasteren, turteksten «Kommer 3 kommer, 2 kanskje», dagrader som ikke summerte og nullrader mot spesifikasjonen, test av `household_totals`, stolpe på 0 % ved 1 av 200, død kode `admin_actor` og foreldet MT-65-resultat.
  - Avvist blant annet: tom `_attention.html` (plassen er med vilje, UX-DR39), Synnes tall (spesifikasjonsvalg), inline `style` på stolpen (prosjektet har ingen CSP) og påstanden om flere svarrader per gjest (modellen har OneToOne).
- Nettleser: MT-71 til MT-74 bestått etter rettingen. Tallene ble lest fra sidene og sammenlignet med `expected.toml`, ikke hardkodet.

**Verifisert:** `uv run pytest` 1509 beståtte tester, ruff og djlint rene. Nettleser: brudepar og hjelper, utlogget, bare tastatur, 360 og 180 px ved 16 og 20 px tekst, alle mål minst 44 px, ingen horisontal rulling.

**Commits:** små commits fra `2da0240` til «Story 3.2 ferdig» på `feat/3-2-svarstatus-og-oppsummering`. PR: https://github.com/IBE160-2026/G26-dvergsdal/pull/50

**Løst fra issues.md:** hjelperens «Du kan se alt, men ikke endre noe.»-linje.

### Åpne punkter
- Story 5.2: betalingsregelen ved negativt netto og tester med beløp.
- Story 6.1: opprydding av `frame()`; kontrast på «Se hva alle har svart» i polérstory.
- Story 7.2: Synnes trukne samtykke lastes i testdata, og `SYNNE_UNTIL_7_2` fjernes.
- Story 3.3 og 3.4: tellinger blir lenker og «Se hva alle har svart» får adresse.
