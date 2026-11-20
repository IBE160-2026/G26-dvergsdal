# Story 1.5: invitasjonens forside

## 2026-11-20 kl. 18:32 — Rikke

### Oppgave
Tredje story i den autonome goal-kjøringen (prompten er sitert i [story-1-4b-papir-bilder-g1](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md)). Intensjonen til `bmad-build-auto` var «Story 1.5 i .docs/planning-artifacts/epics.md»: en gyldig lenke skal åpne en invitasjon der bestefar Sigmund straks ser hvem som gifter seg, når, hvor, at han og bestemor er invitert, og fristen for å svare.

### Plan
- Gren `feat/1-5-invitasjonens-forside`.
- Planleggings-sub-agent: [spec-1-5](../../.docs/implementation-artifacts/spec-1-5-the-invitation-front-page.md). Implementerings-sub-agent. Fire gjennomgangs-sub-agenter. Claude triagerte funnene og sendte rettingene tilbake.
- MT-1, MT-9 og MT-11 til MT-15 med Playwright mot Edge: toppfelt på første skjerm, hopp til `#svar`, menyen og trykkflater, og lastetid på 4G.

### Resultat
**Bygd:** forsiden under `/<kode>/` (meny, toppfelt, innledning, «Alt om helgen», svarfeltet, bunnfeltet) og rammen for `/program/`, `/praktisk/` og `/historie/`. Rene regler for husstandsnavn, «deg»/«dere» og `tel:`-numre, og ingen GET skriver til databasen (testet over HTTP).

**Hva KI foreslo, og hva som ble godtatt, endret eller avvist:**
- **Godtatt fra planleggeren:**
  - Adressene `/program/`, `/praktisk/` og `/historie/`, ført inn i AD-6.
  - Menyen er sticky bare når skjermen også er bred nok.
  - Bunnfeltet utelates helt når ingen kontakt har et nummer.
  - Testkravet for 4G er «Fast 4G» med `loadEventEnd` og LCP under 3 s.
- **Funnet av Claude i nettleseren:** toppfeltet sluttet på 578 px ved 360 × 560, så det sto ikke på første skjerm slik akseptkriteriet krever. Implementeringsagenten fant årsaken: «Hardingasete · Hardanger» i kapitéler blir 307 px bred og brytes på to linjer. Mockupen skjulte det med hardt mellomrom. Rettet med 30 px mindre luft i toppfeltet (DESIGN.md, datert notat), og ny måling ga 548 px.
- **Endret etter gjennomgangen (15 rettinger):**
  - Menyen kunne dekke svarfeltet når brukeren forstørrer teksten, fordi bruddpunktet var i px. Det er nå `20em`.
  - DESIGN.md og EXPERIENCE.md sa fortsatt `scroll-margin-top` og sticky bare etter høyde. Begge er oppdatert.
  - Bunnfeltets kontakter er flyttet til `wedding/selectors.py`, så feilsidene i story 1.8 kan bruke dem.
  - «+47 (0) …» ringte feil nummer.
  - Testhjelpere var kopiert i fem filer.
  - MT-14 hadde dobbel id.
- **Avvist (12):** blant annet at infosidene er tomme, fordi 1.6 og 1.7 fyller dem i samme kjøring. En gjest som slettes mellom to databaseoppslag ble også avvist, sammen med en manglende innstillingsrad (migrasjonen lager alltid én).
- **Utsatt:** et ukjent andre ledd (`/<kode>/svar/`) viser Djangos 404, til story 1.8.

**Verifisert:** `uv run pytest` 578 bestått (fra 492), ruff og djlint rene. MT-1, MT-9 og MT-11 til MT-15 bestått i Edge etter rettingene; 4G («Fast 4G») median 0,5 s, LCP 0,6 s. Sjekkene for 1.4b og 1.4c består fortsatt.

**Commits:** `b91cc01` … `31f85f4` (7 commits). [PR #27](https://github.com/IBE160-2026/G26-dvergsdal/pull/27).

### Åpne punkter
- Godkjenne at luften i toppfeltet er strammet inn 30 px (DESIGN.md), og at stedet brytes som «HARDINGASETE · / HARDANGER». Alternativet er mindre bokstavavstand på stedslinja, så den får plass på én linje.
