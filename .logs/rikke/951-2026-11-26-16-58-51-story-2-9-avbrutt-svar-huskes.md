# Story 2.9 — et avbrutt svar huskes på telefonen

## 2026-11-26 kl. 16:58 — Rikke

### Oppgave
Del av den uovervåkede goal-kjøringen. Rikkes goal-prompt står ordrett i [973-loggen](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Intensjonen for bmad-build-auto var ordrett: «Story 2.9 i .docs/planning-artifacts/epics.md». Målet (FR-78): et svar som er påbegynt, men ikke sendt, venter på gjesten når hen kommer tilbake via lenka. 2.9 er siste story i epic 2, og retrospektivet kjøres i en egen økt.

Økten ble stoppet av bruksgrensen under triagen. Rikke ba ordrett: «Fortsett der du slapp, etter instruksjonene du fikk. Agenter som ble stoppet: send dem en melding for å fortsette, eller start dem på nytt med samme prompt hvis det ikke går.» Ingen agenter var midt i arbeid, så triagen fortsatte der den slapp.

### Plan
- Spec: [spec-2-9-an-interrupted-answer-is-kept-on-the-phone.md](../../.docs/implementation-artifacts/spec-2-9-an-interrupted-answer-is-kept-on-the-phone.md), skrevet av en planleggeragent. Deretter implementering ved en egen agent.
- Fire gjennomgangsagenter (Blind Hunter, Edge Case Hunter, Verification Gap, Intent Alignment) og nettlesersjekk MT-59–64 med Playwright i Edge.

### Resultat
**Hva KI foreslo, og hva som ble godtatt, endret eller avvist**
- Planleggeren foreslo en øktkapsel `rsvp_visit` (uten svar) for å skille «kom tilbake» fra å bla mellom steg, fordi AD-8 forbyr å skrive kapsler på GET. Forslaget ble godtatt (avgjort av Claude). Prisen er at en omlasting i en fane som fortsatt er åpen, viser steget og ikke tilbudet. Det er ført i EXPERIENCE og AD-8, og MT-59 bekreftet det.
- «Ja, fortsett» går til første uferdige steg, fordi utkastet ikke husker siste side. Godtatt, og MT-59 åpnet steg 3.
- Når husstanden er endret, ryddes utkastet i stedet for å kastes: personer som ikke lenger er med, droppes, samtykket nullstilles og skjemaet åpner på steg 1. Godtatt, og MT-61 viste bare Mona etter at Geir var slettet.
- Husstander som har svart, får verken varsel eller tilbud før Story 4.1. Godtatt og ført i deferred-work.md.
- Gjennomgangen ga 24 funn: 4 ble rettet, 4 utsatt og 16 avvist med begrunnelse i spec-ens triagelogg.
  - Rettet: en test for varselet etter at en person er fjernet, sendetesten låst til nøyaktig 302 (agenten hadde løsnet den til «302 eller 303»), samme eierregel i løpende sum og en uriktig malkommentar.
  - Avvist: blant annet påstanden om falsk revisjonskonflikt. Revisjonen øker bare ved sending, se `wedding/services/answers.py`.
- Nettleser: alle radene ble bestått på første kjøring. Starttiden i tilbudet vises i Oslo-tid, og maskinen står i UTC+7.

**Verifisert:** `uv run pytest` ga 1338 beståtte tester, og ruff og djlint er rene. MT-59 til MT-64 ble kjørt i Edge etter rettingene:
- lukket nettleser simulert ved å beholde bare kapsler med `expires` > 0
- «Nei» starter tomt
- etter fristen vises ikke varselet, og kapselen er slettet
- tilbudet kan brukes med bare tastatur (fokusring `solid`)
- ingen horisontal rulling ved 360 og 180 px med 16 og 20 px tekst

**Commits:** 3f7265a (spec), 100ce48, 816195e, d1c5168, 27692d1 (rettinger), ba88f11, 480737a, 72359c5. PR: https://github.com/IBE160-2026/G26-dvergsdal/pull/47 (med gjennomgangskommentar).

### Åpne punkter
- **Rikke:** prøv på telefonen i Messenger: fyll inn to steg, lukk appen helt og åpne lenka igjen. Kommer «Vil du fortsette der du slapp?»? Hvis telefonen beholder øktkapselen, lander du på steget med svarene i stedet.
- **Story 4.1:** forklar hvorfor skjemaet starter på steg 1 etter at husstanden er endret, og bestem hva som skjer med utkastet hos husstander som har svart (deferred-work.md).
