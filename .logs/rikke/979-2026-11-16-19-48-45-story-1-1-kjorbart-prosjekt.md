# Story 1.1: kjørbart prosjekt

## 2026-11-16 kl. 19:48 — Rikke

### Oppgave
Rikke startet `/bmad-build` uten mer tekst. Claude fant ingen påbegynte specs og foreslo neste punkt fra `issues.md`. Rikke valgte **«Story 1.1 (Anbefalt)»** (kjørbart prosjekt med én kommando for tester og sjekker) og svarte **«Ja, bruk dem (Anbefalt)»** på om Claude kunne bruke hjelpeagenter i hele kjøringen. Målet er grunnmuren som resten av koden bygger på, og at sensor kan installere, starte og teste appen etter README.

Økt-ID i Claude Code: `6b5d34a7-954b-4d48-8532-fb270fc47c61`.

### Plan
- `bmad-build` i fem steg: avklare, planlegge (spec), bygge, gjennomgå, presentere. Arbeidet ligger på branchen `feat/1-1-kjorbart-prosjekt`.
- En hjelpeagent samlet kravene for epic 1 i [epic-1-context.md](../../.docs/implementation-artifacts/epic-1-context.md).
- Claude skrev spec-en: [spec-1-1-runnable-project-with-one-command-for-tests-and-checks.md](../../.docs/implementation-artifacts/spec-1-1-runnable-project-with-one-command-for-tests-and-checks.md). Den var på omtrent 2100 tokens, mot anbefalt 1600. Rikke valgte **«Behold hele (Anbefalt)»** og deretter **«Godkjenn og fortsett»**.
- En ny hjelpeagent bygde storyen med spec-en som eneste kilde. Etterpå leste Claude hele endringen selv og kjørte alle sjekkene.
- Tre uavhengige gjennomgangsagenter så på endringen: Blind Hunter, Edge Case Hunter og Verification Gap. Funnene ble vurdert ett for ett, og smårettingene ble sendt tilbake til den samme hjelpeagenten.

### Resultat
**Bygd:**
- Django 6.1.3 på Python 3.14 med uv. Alle avhengighetene er låst i `uv.lock`.
- Mappestrukturen fra arkitekturen.
- `wedding.User` med rollen `couple`/`helper` fra første migrasjon.
- Innstillinger fra miljøvariabler, med en produksjonsvakt (AD-14).
- 44 tester, Ruff, djLint og GitHub Actions.
- `.env.example`, `docs/manual-test-plan.md` (MT-1) og en ny README på norsk.

**Commits på `feat/1-1-kjorbart-prosjekt`:**

| Commit | Hva |
|---|---|
| `0d0f106` | Spec og samlet kontekst for epic 1, committet før koden |
| `5e787cb` | Python 3.14, uv og låste avhengigheter; `.gitignore` for Django i stedet for Next.js |
| `1d7ec9a` | Innstillinger fra miljøvariabler og produksjonsvakt |
| `36a9b87` | Mappestruktur og egen User-modell |
| `093a0b8` | Test som holder `wedding/rules/` fri for Django og prosjektkode |
| `764b085` | GitHub Actions |
| `6ec1f7f` | README og manuell testplan |
| `475a2b6` | Epics: djLint-kommandoen trenger en sti |
| `6517882` | README lenker til arkitekturforklaringen, ikke faglærerens referanse |
| `d5c5ba9`–`d2cc723` | Fem smårettinger etter gjennomgangen |
| `ea13e26` | Spec satt til done, story 1.1 til `review` i sprint-status |

**Verifisert:** `uv sync --locked`, `migrate` og `check` gir ingen feil. `uv run pytest` ga 44 bestått. `ruff check`, `ruff format --check` og `djlint --check .` avslutter med kode 0. Hjelpeagenten kjørte MT-1 i en fersk klone: serveren svarte med Djangos startside, og `git status` var ren etterpå.

**Avvik fra planen:** Storyen sa `uv run djlint --check`, men djLint 1.50 krever en sti og stopper ellers med kode 2. Claude fant dette under planleggingen ved å kjøre verktøyet. Kommandoen er nå `uv run djlint --check .`, og avviket er begrunnet i endringsloggen i `epics.md`.

**Tekniske valg Claude tok** (står i spec-en):
- En ukjent `APP_ENV` (for eksempel `prod`) får appen til å nekte å starte.
- Nye brukere får rollen `helper` som standard.
- Djangos innebygde admin er ikke installert, fordi `/admin/` hører til `dashboard`.
- Forsida viser Djangos startside til story 1.4b og 1.5.

**Hva KI foreslo, og hva som ble godtatt, endret eller avvist:**
- **Claude fanget en feil fra hjelpeagenten:** README lenket til `technology.md` som «teknologivalg». Fila er faglærerens referanse for et annet prosjekt (Pytagoras: FastAPI, Next.js, Supabase) og kunne fått sensor til å tro at appen bruker den stakken. Rettet i `6517882`.
- **Claude rettet sin egen spec før godkjenning:** den første versjonen ville fått djLint til å feile når det ikke finnes maler. Claude testet og la til `allow_empty_input` før spec-en ble vist til Rikke.
- **De tre gjennomgangene ga 20 funn.** Hvert funn ble vurdert mot koden og står i triage-loggen i spec-en.
  - *Godtatt og rettet:* tester for WhiteNoise og for `.env.example`, ærlig tekst om hva produksjonsvakten sjekker, at renhetstesten tåler BOM og navngir importer riktig, og README med standardverdier for produksjon og kommandoene som retter feil.
  - *Avvist med begrunnelse:* sikre cookies og HTTPS (utsatt til 2027), sesjonstid (epic 3), dynamiske importer og at alle produksjonsfeil skal vises samtidig (sjeldent, og rettingen gir mer kode), og at loggen manglet (den skrives nå).

Rikke svarte **«ja»** til å pushe og lage PR. Branchen er pushet, og [PR #18](https://github.com/IBE160-2026/G26-dvergsdal/pull/18) er laget mot `main`. Den første kjøringen i GitHub Actions feilet i oppsettet: `astral-sh/setup-uv@v10` finnes ikke, fordi den bare publiserer fullstendige versjonsnumre. Claude hadde slått opp siste utgivelse under planleggingen uten å sjekke at tagen fantes. Versjonen er låst til `v10.3.3` i `feb0972`, og begge kjøringene på PR-en er grønne.

Rikke spurte om hun skulle bruke Vercel for å se nettsiden. Claude frarådet det: SQLite-fila forsvinner på Vercel, hosting skal velges i 2027 (EU/EØS), og sensor kjører appen lokalt etter README. Rikke kjørte så MT-1 selv i en fersk klone fra GitHub: **«det gikk bra, alt funket»**. Resultatet står i `docs/manual-test-plan.md`.

Rikke leste Claudes tre tekniske valg og svarte **«ser bra ut. har merget»**. PR #18 er merget (merge-commit `0c27541`), lokal `main` er oppdatert, branchen er slettet, og story 1.1 står som `done` i sprint-status.

Rikke spurte om hun skulle svare ut de åpne punktene nå. Claude svarte at punktene fra story 1.1 hører til story 3.1 og 2027, men pekte på et eldre punkt som story 1.2 trenger: maks 8 personer per husstand. Rikke svarte **«ingen er flere enn 8 nei»**. Bekreftelsen står i endringsloggen i `epics.md`.

Lukket punkt i `issues.md`: «neste BMAD-steg: Story 1.1 med `bmad-build`».

### Åpne punkter
- Neste BMAD-steg: story 1.2 (husstander, gjester og personlige lenker) med `bmad-build`.
- **Story 3.1:** `manage.py createsuperuser` gir en superbruker med rollen `helper`. Kommandoen for adminkontoer (FR-47) må sette rollen bevisst.
- **2027:** gjøre produksjonsvakten strengere når hosting velges (minimumslengde på `SECRET_KEY`, avvise `ALLOWED_HOSTS=*`) og legge til sikre cookies, HTTPS-innstillinger og `CSRF_TRUSTED_ORIGINS`.
