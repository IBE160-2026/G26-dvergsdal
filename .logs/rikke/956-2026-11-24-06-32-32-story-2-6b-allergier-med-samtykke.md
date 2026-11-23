# Story 2.6b: Allergier lagres bare med samtykke

## 2026-11-24 kl. 06:32 — Rikke

### Oppgave
Denne økten er en del av den autonome goal-kjøringen. Rikkes goal-prompt er sitert ordrett i [973-…-story-1-4b-papir-bilder-g1.md](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Story-runneren ga denne intensjonen ordrett:

> «Read …\scratchpad\story-runner.md fully and follow it. STORY: 2.6b — Allergies are stored only with consent … Allergy data is health data: follow PRD/architecture consent and storage rules exactly (no consent → nothing stored, not even in logs). Keep 2.6c/2.6d boundaries. Browser checks: a real send in Edge with consent «Ja» for one person and «Nei» for another, then verify the database rows …; keyboard-only; 360 and 180px; 20px text.»

### Plan
- En planleggeragent skrev [spec-2-6b](../../.docs/implementation-artifacts/spec-2-6b-allergies-are-stored-only-with-consent.md). En implementeringsagent bygde den.
- Fire gjennomgangsagenter (Blind Hunter, Edge Case Hunter, Verification Gap, Intent Alignment) gikk gjennom koden.
- Claude kjørte nettleserkontrollene MT-42 til MT-44 med Playwright mot Edge, triagerte funnene og rettet dem.

### Resultat
- **Kode:**
  - Migrering 0006 lager tabellene `Allergy` og `Consent`.
  - Den nye regelen `consent_outcomes` avgjør for hver gjest om allergiopplysningene skal lagres, slettes eller beholdes.
  - `send_answer` bruker regelen i samme transaksjon og fører én samtykkehendelse per person som svarte. Den avviser ugyldige allergisvar før noe skrives.
- **Hva KI foreslo, og hva som ble godtatt, endret eller avvist:**
  - **Planleggerens valg** (godtatt, avgjort av Claude):
    - Å registrere hvilken versjon av samtykketeksten gjesten så, flyttes til 2.6c, som uansett trenger et nytt kakeformat.
    - En gjest som slutter å komme, får lagrede opplysninger slettet (FR-75, NFR-3).
    - «Ja» uten noe utfylt sletter lagrede opplysninger.
    - Det kom ingen ny tekst på sjekksiden. Advarselen etter FR-28 dekker AC3.
  - **Gjennomgangen ga 22 funn: 2 rettet, 2 utsatt og 18 avvist.**
    - Rettet: Blind Hunter fant at testplanen forventet fire samtykkerader, mens det riktige er tre. Kjøringen i Edge bekreftet tre.
    - Rettet: Edge Case Hunter fant at testhjelperen `_with` mistet de valgte dagene.
    - Utsatt: samtidige første sendinger kan gi IntegrityError (går til 2.6c).
    - Utsatt: en test av hva sletting av en gjest gjør med samtykke og allergier (går til historien som innfører sletting).
    - Avvist, blant annet: påstanden om at notatlengden ikke sjekkes. Både skjemaet og draft-dekoderen avviser for lange notater.
    - Avvist: at `given_by_name` er for kort. Feltet har samme lengde som gjestenavnet.
    - Avvist: at gjentatte like samtykkehendelser er en feil. Tabellen er en hendelseslogg, så gjentakelser er ment.
  - **Funn fra nettleserkontrollene:**
    - Den første kjøringen ga 500, fordi den lokale databasen ikke var migrert. Det var et oppsettsavvik og ikke en kodefeil. README sier allerede at `migrate` skal kjøres.
    - Skriptet fant den skjulte kopien av «Fortsett»-knappen først. Det ble rettet i skriptet.
- **Verifisert:**
  - 1218 tester bestått; ruff, ruff format og djlint er rene.
  - MT-42 (ekte sending, databaseradene lest med `manage.py shell`), MT-43 (bare tastatur) og MT-44 (360 og 180px, med og uten 20px tekst) bestod i Edge 158.
- **Commits og PR:**
  - Commits: de851de ea1a746 86c434e 1b0c3e6 31b047b 653b355 e36f4f1 
  - PR: [#42](https://github.com/IBE160-2026/G26-dvergsdal/pull/42)

### Åpne punkter
- **Claude, story 2.6c:** sørge for at samtidige første sendinger ikke gir IntegrityError, og registrere hvilken versjon av samtykketeksten gjesten så (deferred-work.md).
- **Claude, historien som innfører sletting av gjester:** test av at `Consent.given_by` blir null og at allergier og samtykke slettes sammen med gjesten (deferred-work.md).
