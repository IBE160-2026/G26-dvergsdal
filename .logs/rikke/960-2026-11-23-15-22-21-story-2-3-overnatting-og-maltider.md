# Story 2.3: Overnatting, måltider og løpende sum

## 2026-11-23 kl. 15:22 — Rikke

### Oppgave
Del av den autonome goal-kjøringen. Rikkes goal-prompt er sitert ordrett i [973-…-story-1-4b-papir-bilder-g1.md](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Story-runneren ga denne intensjonen til bmad-build-auto ordrett:

> STORY: 2.3 — Overnight stay, meals and the running total. Sprint-status key: 2-3-overnight-stay-meals-and-the-running-total. […] The running total must work without JavaScript (server-rendered) and update with JS if the spec chooses it; if JS is used, the live region must exist in the page from the start.

### Plan
- En planleggeragent skrev [spec-2-3](../../.docs/implementation-artifacts/spec-2-3-overnight-stay-meals-and-the-running-total.md). Den bygger på 2.1 og 2.2 og lukker tre utsatte funn: kroner-visningen, FR-75 og malvalget i `step.html`.
- En implementeringsagent fulgte spec-en. Den ble stoppet av bruksgrensen og fortsatte etterpå.
- Fire KI-agenter gikk gjennom koden, og Claude kjørte nettlesersjekker i Edge.
- Funnene ble sortert og rettet, og til slutt ble det PR og merge.

### Resultat
**Kode:**
- `wedding/rules/money.py` (`household_total`) og `answer.py` (`Answer`, utvidet `normalise_answer`).
- Kroner-filteret, steg 3 og steg 4.
- `POST /<kode>/svar/sum/` og `static/js/rsvp-total.js`.

**Hva KI foreslo, og hva som ble godtatt, endret eller avvist:**
- **Planleggeren, godtatt.** Disse valgene ble godtatt og er avgjort av Claude etter goal-regelen:
  - Et lite skript med server-fragment for summen, slik at serveren alltid er fasit.
  - En person som bare kommer én dag får likevel Ja/Nei, men en avvist «Ja» lagres ikke, og feilmeldingen forklarer hvorfor.
  - Kladdecookien går til format 3.
  - Spørsmålene «Hvem skal overnatte på Hardingasete?» og «Hvilke måltider skal vi bestille?» unngår du/dere, fordi noen svarer alene.
- **Gjennomgangen ga 21 funn, og 3 ble rettet:**
  - Feiloppsummeringen gikk ut over arket ved 180px. Det fant Claude selv i et skjermbilde fra Edge.
  - Samme sum ble lest opp på nytt i statusfeltet.
  - En test sjekket ingenting.
- **Utsatt:** 1 funn, teksten ved pris 0, til story 4.5.
- **Avvist:** 17 funn. Eksempler:
  - «Steg 4 kan bli tomt» er feil, fordi `form_steps` hopper over steget.
  - «JS-oppførselen er ikke verifisert» er feil, fordi den ble kjørt i Edge.
  - Vakter mot input som ikke er tall i `kroner` ble avvist, fordi alle kallere sender heltall.
- **Nettlesersjekkene:** Claudes første skript feilet på Arilds steg 2 og på en navigasjonsrase. Det var feil i skriptet, ikke i appen, og skriptet ble rettet.

**Verifisert:**
- `uv run pytest`: 1021 bestått. ruff og djlint er rene.
- MT-1 (2.3), MT-30, MT-31 og MT-32 ble kjørt med Playwright mot Edge:
  - summen går 0 → 1 500 → 3 000 → 4 120 kr, med og uten JavaScript
  - skjemaet kan brukes med bare tastatur
  - ingen horisontal rulling ved 360 og 180 px eller med 20px tekst

**Commits:** 895b2be (spec), 9b30149, e2ec359, 44927d5, 69adfe1, f11006c, a3fd56c, c39cac2.
**PR:** https://github.com/IBE160-2026/G26-dvergsdal/pull/38

Det utsatte funnet om malvalg og FR-75 fra story 2.2 er lukket i `issues.md`.

### Åpne punkter
- **Story 4.5:** teksten «hver gjest betaler selv» står fortsatt på steg 3–4 når en pris er 0.
