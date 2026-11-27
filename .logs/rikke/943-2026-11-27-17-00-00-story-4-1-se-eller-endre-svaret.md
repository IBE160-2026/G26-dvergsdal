# Story 4.1 — Se eller endre svaret før fristen

## 2026-11-27 kl. 17:00 — Rikke

### Oppgave
Del av den uovervåkede goal-kjøringen. Rikkes goal-prompt står ordrett i [973-loggen](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Intensjonen for bmad-build-auto var ordrett: «Story 4.1 i .docs/planning-artifacts/epics.md». Første story i epic 4: onkel Arild skal kunne åpne det sendte svaret, se hvem som svarte sist og endre det før fristen.

### Plan
- Spec: [spec-4-1-see-or-change-the-answer-before-the-deadline.md](../../.docs/implementation-artifacts/spec-4-1-see-or-change-the-answer-before-the-deadline.md), skrevet av en planleggeragent (ny epic-4-kontekst). `wedding/rsvp/views.py` skulle ikke vokse; ny kode i egne moduler (`change.py`, `rules/changes.py`, `services/changes.py`).
- Implementering i fire commits, så gjennomgang med fire agenter, nettleserkontroll MT-91 til MT-96 i Edge, rettinger.

### Resultat
**Hva KI foreslo, og hva som ble godtatt, endret eller avvist**
- Planleggeren bygger utkastet fra det sendte svaret i minnet (ikke i informasjonskapselen) og lar en `send` kreve et ekte utkast. Godtatt: det lukker det utsatte funnet fra 2.8 om gamle faner.
- «Sist endret av <navn>» navngir siste avsender (`sent_by_name`), ikke en endrer; `changed_at` er bare parets markør. Godtatt og ført som datert notat i ARCHITECTURE-SPINE og EXPERIENCE.
- Bekreftelser («Jeg bekrefter …») bæres aldri over i utkastet; samtykke bare for gjeldende tekstversjon. Godtatt.
- Implementereren avvek fra spesifikasjonen i to punkter (signaturen til `seeded_draft` for å unngå sirkulær import, og 303 for alle `send` uten utkast). Godtatt, ført i resultatet.
- Gjennomgangen ga 20 funn: 3 rettet (test av siste samtykkehendelse, test av `?sending=` på andre steg, MT-91-ordlyd), 1 utsatt til story 4.2 (første POST uten utkast seedes ved nyeste revisjon), 16 avvist (blant annet at send fra andre steg blir seedet og at et ødelagt utkast blir liggende: begge feil ved lesing av koden).
- Nettleser: først feilet skriptet fordi attributtnavn har dynamiske id-er; rettet i skriptet. Summen 4 980 kr vises etter «Fortsett», ikke ved avkrysning (testplanen rettet). Ellers MT-91 til MT-96 bestått.

**Verifisert:** `uv run pytest` 1662 beståtte tester, ruff, ruff format og djlint rene. Edge: 4 980 kr på Se over svaret, kvittering og forside, `changed_at` satt, `send` uten utkast gir 303, etter fristen verken linje eller knapp, tastatur gjennom alle steg, 360 og 180 px ved 16 og 20 px uten overflyt (knapp 52–88 px).

**Commits:** `7633fdc`, `73dec10`, `36aa987`, `61303a5`, `589d05c`, `8cf09c9`, `1f36a8f` på `feat/4-1-se-eller-endre-svaret`. PR: https://github.com/IBE160-2026/G26-dvergsdal/pull/55

**Løst fra issues.md / deferred-work.md:** 2.8 (gammel fane kan sende på nytt), 2.9 (utkast for besvart husstand), 2.9 (forklaring ved «Ja, fortsett»).

### Åpne punkter
- Story 4.2: første POST uten utkast seedes ved nyeste revisjon, så et skjema åpnet før en annen sendte kan overskrive uten varsel (deferred-work).
