# Story 2.7: kvitteringen og hvordan man betaler

## 2026-11-26 kl. 00:54 — Rikke

### Oppgave
Del av den uovervåkede goal-kjøringen. Rikkes goal-prompt står ordrett i [973-loggen](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Intensjonen for bmad-build-auto var ordrett: «Story 2.7 i .docs/planning-artifacts/epics.md». Målet: «Svaret er sendt» blir en full kvittering, og gjestene får se hvordan de betaler.

Økten ble avbrutt av bruksgrensen to ganger. Etter siste avbrudd så det ut som en annen økt hadde laget commits på grenen, og jeg stoppet. Rikke presiserte da ordrett: «Det finnes ingen annen økt. Du er den eneste. Grenen er pushet, men det finnes ingen PR og ingen sesjonslogg. Gjør nå selv steg 13–16 i story-runner.md». Commitene var altså fra denne økten før avbruddet. Jeg tok kjøringen videre fra PR-steget.

### Plan
- Planleggeragent skrev [specen](../../.docs/implementation-artifacts/spec-2-7-the-receipt-and-how-to-pay.md). Den fikk punktet om live region fra deferred-work og issues.md.
- Implementeringsagent, så commits i små steg: regler, selector og oppsummering, og til slutt views, maler, CSS og JS.
- Fire gjennomgangsagenter og MT-51 til MT-54 med Playwright i Edge. Deretter triage, rettinger og ny kjøring.

### Resultat
**Hva KI foreslo, og hva som ble godtatt, endret eller avvist**

Godtatt fra planleggeren (avgjort av Claude):
- «Betal nå» åpner en egen side `/svar/betal/` («Slik betaler du»). Den virker uten JavaScript, og 2.8 kan lenke dit.
- «Betal senere» er en lenke til `sendt/?betal=senere` med en melding som får fokus.
- Kvitteringen leser det lagrede svaret (`sent_answer`), aldri utkastet.
- Beløp og kontonummer kopieres som bare sifre.
- «Betal nå» får ikke autofokus, i motsetning til notatet i mockupen. Da hopper ikke skjermleseren over overskriften om at svaret er sendt.

Endret etter gjennomgangen. Fire agenter ga 28 funn: 1 middels, 14 små, 12 falske og 1 uavklart. Av dem ble 6 rettet:
- Delvise dager i `sent_answer` manglet test (middels). Det er nå en rundtur-test med delvise dager og et måltid.
- `Answer` ble bygd med ni posisjonsargumenter. Nå brukes nøkkelargumenter.
- Kontonummer med bare sifre er flyttet fra viewet til en ny regel, `digits_only` (AD-12).
- Nye tester for trukket samtykke, for husstander der ingen kommer, og for tomt kontonummer.
- README-treet nevner nå `pay.html` og `pay-row.html`.

Utsatt: hvis både Vipps-nummer og kontonummer er tomme, viser betalingssiden ingen betalingsmåte. Punktet står i deferred-work.md.

Avvist: 21 funn, med begrunnelse i specens triagelogg. Blant dem:
- Null-sjekker i `rsvp-copy.js` for markup som alltid finnes.
- Tilstander som `send_answer` aldri lagrer.
- «Trykk og hold» på PC. Ordlyden er avgjort, og verdien markeres uansett.

Nettlesertesten: første kjøring stoppet på steg 6. Feilen lå i testskriptet mitt, ikke i appen. «Fortsett» ventet ikke på navigasjonen, så skriptet sjekket URL-en for tidlig. Skriptet venter nå på navigasjonen. Etter det besto alle radene, også etter rettingene.

**Verifisert:**
- `uv run pytest`: 1296 bestått. Ruff og djlint er rene.
- MT-51: Mona 3 000 kr. Sigmund 4 720 kr. Synne 0 kr og ingen betalingsknapper, og `betal/` sender henne tilbake til kvitteringen.
- MT-52: alle fire `role="status"` er tomme når siden lastes. Utklippstavlen får `12345678900`, og «Kopiert» kommer bare i riktig felt. Når kopieringen feiler, markeres verdien. Uten JavaScript vises ingen knapper.
- MT-53: bare tastatur fungerer, og fokusmarkeringen er `solid`.
- MT-54: ingen horisontal rulling ved 360 og 180px, verken med 16 eller 20px tekst. Knappene er 46–54px høye.

**Commits:** 68e9523 (spec), 3c2cc32, 7bcde2a, 7cb8717, 5fa9483 og 5484ff5 (rettinger), d0c4d88, cc59306, fe3ff56 og 8fcc361. PR: https://github.com/IBE160-2026/G26-dvergsdal/pull/45

### Åpne punkter
- [ ] Rikke lytter til «Kopiert» med NVDA eller VoiceOver. Punktet står allerede i issues.md, og koden er på plass.
