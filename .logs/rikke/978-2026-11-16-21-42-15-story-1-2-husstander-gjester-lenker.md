# Story 1.2: husstander, gjester og personlige lenker

## 2026-11-16 kl. 21:42 — Rikke

### Oppgave
Rikke startet `/bmad-build` uten argument. Neste story i sprintplanen er 1.2: hver gjest skal få sin egen lenke som ikke kan gjettes, og som bare åpner gjestens egen husstand (FR-1, FR-2), og å åpne lenken skal aldri endre noe (FR-3).

### Plan
- Arbeidsflyten var `bmad-build`: avklare, planlegge (spec), implementere, gjennomgå, presentere. Spec: [spec-1-2-households-guests-and-personal-links.md](../../.docs/implementation-artifacts/spec-1-2-households-guests-and-personal-links.md).
- Rikkes valg underveis, gjennom spørsmålsdialogen:
  - **«Hva vil du jobbe med nå?»** → «Story 1.2 (Recommended)».
  - **«Får jeg bruke [hjelpeagenter] gjennom hele denne økta?»** → «Ja, bruk dem».
  - **Specen var ca. 2100 tokens, over anbefalte 1600** → «Behold hele», fordi alt hører til ett mål.
  - **Godkjenning av specen** → «Godkjenn og fortsett».
- Epic 1-konteksten ble kompilert på nytt av en hjelpeagent, fordi epics.md var endret etter forrige versjon (maks 8 personer, djLint-kommandoen).
- Claudes tekniske valg i specen, som Rikke godkjente:
  - Husstanden har ikke noe eget navnefelt; «for Sigmund og bestemor» lages av gjestenavnene i story 1.5.
  - FR-3 testes mot oppslaget i story 1.2, fordi ingen gjesteside finnes ennå. Story 1.5 fikk et nytt akseptansekrav om testen over HTTP.
  - Ny fil `wedding/actors.py`, ført inn i arkitekturen med begrunnelse.
  - Maks 8 og minst 1 person per husstand håndheves allerede i tjenesten.
  - Faste lenkekoder er bare lov for seed-kommandoen.

### Resultat
- **Gren:** `feat/1-2-husstander-gjester-lenker`, med commits fra f4d17a5 (epic-kontekst) til a77d1ae (spec done). Ikke pushet.
- **Kode** (hjelpeagent, b729bef–5aa28a7):
  - Modellene `Household` (revision 0), `Guest` (unik kode på 22 tegn) og `Settings` (én rad, sikret med en check constraint).
  - Migrasjonene `0002` og `0003`. Den siste lager Settings-raden med plassholdere: Rikke og Valdemar, priser 0, tomme telefonnumre, svarfrist 2028-01-04.
  - `wedding/actors.py`, `wedding/links.py` (`new_code`, `is_code_format`, `resolve_code`) og `wedding/rules/households.py` (maks 8).
  - Tjenesten `create_household` med `require_couple` og egne feiltyper på norsk.
  - En AST-test som sjekker at bare `wedding/services/` skriver til databasen.
- **Planendringer:**
  - epics.md: FR-3 over HTTP flyttet til story 1.5, med en rad i endringsloggen der det står at Claude bestemte.
  - ARCHITECTURE-SPINE.md: `actors.py` lagt inn.
  - README: status og mappestruktur.
- **Kontroll:**
  - Claude leste hele endringen mot specen. Hver rad i tabellen over kanttilfeller har en test som kjørte og besto.
  - Tre uavhengige gjennomgåere (Blind Hunter, Edge Case Hunter, Verification Gap) ga 25 funn, samlet i 18 rader i gjennomgangsloggen i specen. 8 ble rettet (31bcd61–26d875e):
    - telefonlengde og e-postformat blir sjekket før lagring
    - en test som faktisk viser at telefon og e-post trimmes
    - én felles `Actor`-type
    - en egen feilmelding når to personer i samme husstand har samme kode
    - riktigere FR-sporing i én test
    - «Claude bestemte» i endringsloggen i epics.md
  - De andre 10 ble avvist med begrunnelse. Blant dem:
    - **«To samtidige lagringer kan gi kræsj»:** avvist, fordi SQLite med `IMMEDIATE` tar skrivelåsen når transaksjonen starter.
    - **«En deaktivert konto kommer forbi rollesjekken»:** avvist, fordi Django nekter inaktive brukere å logge inn.
- **Sluttsjekk:** 106 tester består, og Ruff, djLint og `makemigrations --check` er rene. Sprint-status: 1.2 står på `review` til PR-en er merget.
- Lukket punktet «neste BMAD-steg: story 1.2» i issues.md.
- Rikke spurte «hva annbefaler du?». Claude anbefalte å pushe og lage en PR før story 1.3, fordi CI var det eneste som ikke var sjekket (story 1.1 feilet første gang i CI), og fordi 1.3 bygger direkte på 1.2. Rikke svarte «ja». Grenen er pushet, og [PR #19](https://github.com/IBE160-2026/G26-dvergsdal/pull/19) er laget. GitHub Actions er grønn: kjøring 43869509143 (push) og 43869558183 (PR).
- Rikke merget PR #19 selv (4e93f00). Story 1.2 er satt til `done` i sprint-status på `main` (a6c4227).

### Åpne punkter
- Neste BMAD-steg: story 1.3 (testdata og fasit) med `bmad-build`.
- **Story 1.3 og senere:** testen som reverserer Settings-migrasjonen tømmer databasen etter seg. Nye tester med `transaction=True` som trenger Settings-raden, må derfor bruke `serialized_rollback=True`.
