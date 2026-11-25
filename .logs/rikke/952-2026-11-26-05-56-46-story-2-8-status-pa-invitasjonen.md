# Story 2.8 — husstandens status på invitasjonen

## 2026-11-26 kl. 05:56 — Rikke

### Oppgave
Del av den uovervåkede goal-kjøringen. Rikkes goal-prompt står ordrett i [973-loggen](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Intensjonen for bmad-build-auto var ordrett: «Story 2.8 i .docs/planning-artifacts/epics.md». Målet: når en husstand har svart, viser invitasjonen at svaret er sendt og når, slik at ingen svarer på nytt eller lurer.

Planleggeren ble stoppet av bruksgrensen første gang. Rikke ba ordrett: «Fortsett der du slapp, etter instruksjonene du fikk. Agenter som ble stoppet: send dem en melding for å fortsette, eller start dem på nytt med samme prompt hvis det ikke går.» Planleggeren ble startet på nytt med samme prompt.

### Plan
- Spec: [spec-2-8-the-household-s-status-on-the-invitation.md](../../.docs/implementation-artifacts/spec-2-8-the-household-s-status-on-the-invitation.md), skrevet av planleggeragent, så implementering ved egen agent.
- Fire gjennomgangsagenter (Blind Hunter, Edge Case Hunter, Verification Gap, Intent Alignment) og nettlesersjekk MT-55–58 med Playwright i Edge.

### Resultat
**Hva KI foreslo, og hva som ble godtatt, endret eller avvist**
- Planleggeren foreslo `id="status"` på overskriften i stedet for på arket (som i mockupen), slik at fokus lander på overskriften. Dette ble godtatt, og MT-57 bekreftet `H2#status` etter begge hoppene.
- Planleggeren foreslo at `/svar/` også sendes til statusen etter fristen, i stedet for at siden viser «Svarfristen har gått ut». Dette ble godtatt og ført som «avgjort av Claude» i EXPERIENCE.md.
- Implementereren oppdaget at spesifikasjonen ville ødelagt konflikthåndteringen fra 2.6c (GET med `?sending=` etter en avvist sending). Derfor la den inn et unntak. Gjennomgangen fant at unntaket var for vidt: hvem som helst kunne åpne alle skjemasteg igjen med `?sending=x`. Unntaket ble snevret inn til bare sjekksiden før fristen.
- Gjennomgangen ga 28 funn: 9 ble rettet, 1 ble utsatt og 18 ble avvist med begrunnelse i spec-ens triagelogg. Blant de avviste: en ekstra SELECT per side, det at den skjulte fokusringen er designmønsteret fra 1.6, og at 0 kr-blokken for Synne allerede er bestemt.
- Nettleserfunn: MT-56 satte fristen til «i går», men maskinen står i UTC+7, så fristen hadde ennå ikke gått ut i Oslo. Steget bruker nå to dager tilbake (ført i Spec Change Log).

**Verifisert:** `uv run pytest` ga 1315 beståtte tester, og ruff og djlint er rene. MT-55 til MT-58 ble kjørt i Edge etter rettingene: Marie har 6 480 kr og «Slik betaler du», Synne har 0 kr og ingen knapp, og etter fristen får Marie statusen mens Mona får «Svarfristen har gått ut». Fokus lander på `H2#status`. Det er ingen horisontal rulling ved 360 og 180 px med 16 og 20 px tekst.

**Commits:** 4686955 (spec), c51be93, 09f2a40, 629a50e, 059ad49 (rettinger), 718ac28, 2029b66, dd24a7c. PR: https://github.com/IBE160-2026/G26-dvergsdal/pull/46 (med gjennomgangskommentar).

### Åpne punkter
- **Story 4.1:** en husstand som har svart kan fortsatt sende (POST) fra et gammelt utkast i en annen fane (deferred-work.md).
