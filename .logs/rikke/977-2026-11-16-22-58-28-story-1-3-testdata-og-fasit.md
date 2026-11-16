# Story 1.3: testdata og fasit

## 2026-11-16 kl. 22:58 — Rikke

### Oppgave
Rikke startet `/bmad-build` uten mer tekst og valgte story 1.3 (*Fictional test data and the hand-made expected-results list*) da Claude spurte hva som skulle bygges. Hun ga også lov til å bruke underagenter i hele kjøringen. Målet er at sensor får fiktive gjester å prøve med én kommando, og at senere stories har en fasit regnet ut for hånd å sjekke tallene sine mot (FR-47, FR-68, FR-69, FR-72, NFR-3, AD-14, AD-16).

### Plan
- Spesifikasjon: [spec-1-3-fictional-test-data-and-the-hand-made-expected-results-list.md](../../.docs/implementation-artifacts/spec-1-3-fictional-test-data-and-the-hand-made-expected-results-list.md). Epic 1-konteksten var utdatert (epics og arkitektur var endret etter at den ble laget), så en underagent laget den på nytt først.
- Claude foreslo 7 fiktive husstander med 14 gjester som til sammen dekker hvert tilfelle i FR-68. Prisene er på 2026-nivå, men fiktive (hytte 1500, middag fredag 340, frokost 260), som svaret fra Hardingasete anbefalte.
- Rikke fikk to spørsmål før godkjenning:
  - *Hvem skal regne ut fasiten?* Svar: «KI + kontroll + deg». Claude regner, en uavhengig underagent regner på nytt uten å se tallene, og Rikke stikkprøver.
  - *Specen er på ca. 2500 tokens (anbefalt maks 1600). Dele den?* Svar: «Behold hele».
- Rikke godkjente specen med «Godkjenn og fortsett».
- Arbeidet ble gjort på grenen `feat/1-3-testdata-og-fasit` i denne rekkefølgen: `seed.toml` → `expected.toml` i egen commit → kode (underagent) → tre uavhengige gjennomganger → rettelser.

### Resultat
**Data og fasit (Claude, med Rikkes kontroll):**
- `wedding/fixtures/seed.toml` (67bad24): innstillinger, to testbrukere og de 7 husstandene. Svar, allergier, samtykker og betalinger står som data for story 2.6d, 5.2 og 7.2.
- Den uavhengige underagenten fikk nøyaktig de samme tallene som Claude for alle verdiene. Den pekte på at FR-60 ikke sier hvilken betalingsstatus en husstand som ikke har svart, skal ha.
- Rikkes stikkprøve, ordrett: «1: a) 4120, b) 1560, c) 4340, 2: A».
  - b) Stemte: 1560 kr er 6 lørdagsfrokoster × 260 kr.
  - a) Arilds sum: 4120 er Arild + Filippa, så Marie var utelatt. Fasiten sier 6480.
  - c) Evas tilgode: 4340 er alle beløpene lagt sammen. Fasiten sier 260.
  - Claude viste utregningen, og Rikke svarte «ja» til 6480 og 260.
- **Rikke avviste KIs tolkning av FR-60:** For Mona og Geir, som ikke har svart, hadde både Claude og underagenten satt «Ingenting å betale». Rikke valgte A, «Ikke svart». FR-60 i PRD-en ble oppdatert (9360654).
- `wedding/fixtures/expected.toml` (55a38e0): fasiten, i egen commit før koden. Commit-meldingen beskriver alle fire stegene.

**Kode (underagent, 10 commits 184753f..e3ba5da):**
- `is_test_data` på `Household` og `User`, med migrasjon `0004`. Husstander og brukere som systemaktøren lager, er testdata.
- Tjenestene `create_admin_user`, `update_settings` og `reset_test_data`, og selectoren `seed_conflicts`.
- Kommandoen `uv run manage.py seed_testdata`. Den nekter å kjøre uten `APP_ENV` lik `local` og stopper uten å skrive hvis ekte data bruker en kode eller et brukernavn fra `seed.toml`. Den skriver alt i én transaksjon og skriver ut en testlenke per gjest.
- Nye tester, oppdatert README (Testdata-delen med lenker og innlogginger) og AD-4/AD-16 i arkitekturen.

**Gjennomgang:**
- Blind Hunter, Edge Case Hunter og Verification Gap ga 22 funn.
- 9 ble rettet (8e7b669..13b73ba):
  - En test som beviser at gamle testdata blir stående når en tjeneste feiler etter at slettingen har kjørt.
  - Beslutningen om «Ikke svart» ført inn i epics (story 3.5 og 5.3).
  - Et nytt krav i story 3.1 om at ekte admin-brukere aldri lages med systemaktøren, ellers ville de blitt slettet av neste `seed_testdata`.
  - En test som sjekker at tallene i fasiten stemmer med hverandre.
  - Selectoren fikk nytt navn, og feilmeldingen om `APP_ENV` ble rettet.
- 13 ble avvist med begrunnelse i specens triage-logg, blant annet en påstått race condition som `transaction_mode: IMMEDIATE` allerede hindrer.
- Spec og sprint-status: c2d650f og 8d9381f. Sprint-status er `review`.

**Verifisert av Claude etter rettelsene:**
- 204 tester passerer, og Ruff, djLint og `makemigrations --check` er grønne.
- `seed_testdata` kjørt to ganger ga samme utskrift.

**Push og PR:** Rikke ba om «push og pr». Grenen er pushet, og [PR #20](https://github.com/IBE160-2026/G26-dvergsdal/pull/20) er laget. GitHub Actions er grønn (kjøring 43882272063). Rikke merget PR #20 («gjort»), og sprint-status ble satt til `done` på `main` (eef8f6b).

### Åpne punkter
- **Story 3.1:** `create_admin` må lage ekte kontoer med `is_test_data=False` gjennom sin egen vei, ikke med systemaktøren (krav lagt inn i epics).
- **Story 5.3:** `payment_status` må få vite om husstanden har svart, så den kan gi «Ikke svart» (krav lagt inn i epics).
- Neste BMAD-steg: story 1.4a (fargene, skrifttypene, knappene og meldingene i invitasjonen) med `bmad-build`.
