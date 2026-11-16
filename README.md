# G26 — AI'll handle it

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

**AI'll handle it** er bryllupsnettsiden til Rikke og Valdemar. Hver gjest får en personlig lenke som er den eneste innloggingen: der ser gjesten invitasjonen, programmet og praktisk informasjon, og svarer for husstanden sin. Brudeparet og hjelperne får en oversikt over svar, allergier og betalinger. Nettsiden er laget for gjester i alle aldre på mobil, og den er utviklet med KI og BMAD-metoden.

Repoet inneholder applikasjonen og dokumentasjonen av utvikling, testing og kvalitetssikring med KI.

> **Status:** Prosjektgrunnmuren er på plass (story 1.1): Django-prosjektet, innstillinger, brukermodellen, tester og sjekker. Husstander, gjester, personlige lenkekoder og innstillingene finnes i databasen (story 1.2), og `seed_testdata` fyller dem med fiktive testdata (story 1.3), men det finnes ingen sider ennå. Siden for ugyldige lenker kommer i story 1.4b og invitasjonens forside i story 1.5, så foreløpig viser `http://127.0.0.1:8000/` Djangos egen startside.

## Forutsetninger

| Verktøy | Versjon | Merknad |
|---|---|---|
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | 0.13 (0.12 virker også) | Installerer riktig Python og alle avhengigheter |
| Python | 3.14 | Trenger ikke installeres selv: uv henter versjonen i `.python-version` |
| Git | hvilken som helst nyere | For å klone repoet |

Appen bruker SQLite, som følger med Python. Den trenger ingen database-server, ingen kontoer og ingen nøkler, og kjører på Windows, macOS og Linux.

## Installere og starte

```bash
git clone https://github.com/IBE160-2026/G26-dvergsdal.git
cd G26-dvergsdal
uv sync
uv run manage.py migrate
uv run manage.py runserver
```

Åpne <http://127.0.0.1:8000/> i nettleseren. Stopp serveren med `Ctrl+C`.

`uv sync` installerer Python 3.14 og de låste versjonene i `uv.lock`. `migrate` lager den lokale databasen `db.sqlite3`, som git ignorerer.

## Testdata

Én kommando fyller databasen med fiktive husstander, gjester, innstillinger og to testbrukere fra [wedding/fixtures/seed.toml](wedding/fixtures/seed.toml). Kjør den etter `migrate`:

```bash
uv run manage.py seed_testdata
```

Kommandoen skriver ut en testlenke per gjest og innloggingene under. Den kan kjøres så ofte du vil: den sletter først testdataene fra forrige kjøring, men aldri husstander eller brukere den ikke har laget selv. Er en lenkekode eller et brukernavn fra `seed.toml` allerede i bruk av slike data, stopper den uten å endre noe. Den kjører bare når `APP_ENV` ikke er satt eller er `local`, så testdata aldri havner på den ekte nettsiden.

Alle personene er oppdiktet, bortsett fra Rikke og Valdemar: e-postene er på `example.com`, telefonnumrene begynner med `+47 000`, og kontonummeret har feil kontrollsiffer. Svarfristen settes til 30 dager etter dagen kommandoen kjøres, så svarskjemaet er åpent.

| Gjest | Husstand | Testlenke |
|---|---|---|
| Sigmund | Sigmund og bestemor | <http://127.0.0.1:8000/test-sigmund0000000000/> |
| bestemor | Sigmund og bestemor | <http://127.0.0.1:8000/test-bestemor000000000/> |
| Arild | Arild, Marie, Filippa og Leone | <http://127.0.0.1:8000/test-arild000000000000/> |
| Marie | Arild, Marie, Filippa og Leone | <http://127.0.0.1:8000/test-marie000000000000/> |
| Filippa | Arild, Marie, Filippa og Leone | <http://127.0.0.1:8000/test-filippa0000000000/> |
| Leone | Arild, Marie, Filippa og Leone | <http://127.0.0.1:8000/test-leone000000000000/> |
| Synne | Synne | <http://127.0.0.1:8000/test-synne000000000000/> |
| Tor | Tor og Hilde | <http://127.0.0.1:8000/test-tor00000000000000/> |
| Hilde | Tor og Hilde | <http://127.0.0.1:8000/test-hilde000000000000/> |
| Eva | Eva | <http://127.0.0.1:8000/test-eva00000000000000/> |
| Jonas | Jonas og Ida | <http://127.0.0.1:8000/test-jonas000000000000/> |
| Ida | Jonas og Ida | <http://127.0.0.1:8000/test-ida00000000000000/> |
| Mona | Mona og Geir | <http://127.0.0.1:8000/test-mona0000000000000/> |
| Geir | Mona og Geir | <http://127.0.0.1:8000/test-geir0000000000000/> |

Åpne lenkene mens `uv run manage.py runserver` kjører. Invitasjonen de åpner, kommer i story 1.5; til da viser de Djangos egen startside, akkurat som `/`.

| Brukernavn | Passord | Rolle |
|---|---|---|
| `testpar` | `bryllup-test-2028` | Brudeparet |
| `testhjelper` | `bryllup-test-2028` | Hjelper |

Innloggingen for brudeparet og hjelperne under `/admin/` kommer i story 3.1.

`seed.toml` inneholder også de planlagte svarene, allergiene, samtykkene og betalingene. De lastes inn i senere stories (2.6d, 5.2 og 7.2). Fasiten for disse dataene, regnet ut for hånd før koden som regner dem ut, ligger i [wedding/fixtures/expected.toml](wedding/fixtures/expected.toml); commit-meldingen til fila forklarer hvordan tallene ble kontrollert.

## Tester og sjekker

Alle testene kjøres med én kommando:

```bash
uv run pytest
```

Kodesjekkene (de samme som GitHub Actions kjører på hver push og pull request, se [.github/workflows/checks.yml](.github/workflows/checks.yml)):

```bash
uv run ruff check
uv run ruff format --check
uv run djlint --check .
```

Feiler en sjekk, retter disse kommandoene det meste automatisk:

```bash
uv run ruff check --fix
uv run ruff format
uv run djlint --reformat .
```

Ruff sjekker og formaterer Python-koden, djLint sjekker Django-malene. Det finnes ingen maler før story 1.4a, så djLint melder foreløpig at den ikke fant noe å sjekke, og avslutter uten feil.

Sjekker som ikke kan automatiseres, for eksempel hvordan sidene ser ut på en smal mobilskjerm, står i [docs/manual-test-plan.md](docs/manual-test-plan.md).

## Innstillinger

Appen trenger ingen innstillinger for å kjøre lokalt: alt har trygge standardverdier, og det trengs ingen `.env`-fil. Innstillingene leses fra miljøvariabler, og alle står med eksempelverdier i [.env.example](.env.example).

| Variabel | Standard lokalt | Standard i produksjon | Forklaring |
|---|---|---|---|
| `APP_ENV` | `local` | (settes til `production`) | `local` eller `production`, skrevet nøyaktig slik. Alt annet (for eksempel `prod`) gjør at appen nekter å starte. |
| `DEBUG` | `true` | `false` | Djangos feilsøkingssider. |
| `SECRET_KEY` | en fast nøkkel bare for lokal bruk | ingen brukbar: den lokale nøkkelen godtas ikke | Signeringsnøkkel. Produksjon må ha sin egen lange, tilfeldige nøkkel. |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` | tom: må settes | Kommaseparerte domenenavn nettsiden svarer på. |

Med `APP_ENV=production` nekter appen å starte hvis `DEBUG` er på, `SECRET_KEY` mangler eller er den lokale nøkkelen, eller `ALLOWED_HOSTS` er tom. Meldingen sier hva som må rettes.

Slik bruker du en egen innstillingsfil (valgfritt):

```bash
cp .env.example .env
uv run --env-file .env manage.py runserver
```

`.env` holdes ute av git og skal aldri committes.

## Mappestruktur

```text
.
├── config/                   Django-innstillinger, rot-URL-er, WSGI/ASGI
│   └── env.py                Leser miljøvariabler og vakten for produksjon
├── wedding/                  Dataeieren: modeller (også brukermodellen) og forretningslogikk
│   ├── rules/                Rene regelfunksjoner uten Django (summer, tellinger, frist)
│   ├── services/             Den eneste koden som skriver til databasen
│   ├── rsvp/                 Svarskjemaet, brukt av både gjester og brudeparet
│   ├── selectors.py          Lesespørringer for visningene
│   ├── actors.py             Hvem som handler: gjest, admin eller system
│   ├── links.py              Gjør en personlig lenkekode om til en gjest
│   ├── management/commands/  Kommandoer: seed_testdata fyller inn testdata
│   ├── fixtures/             Testdata (seed.toml) og fasit (expected.toml)
│   └── migrations/           Databasemigrasjoner
├── guests/                   Gjestesidene under /<kode>/
├── dashboard/                Sidene for brudeparet og hjelperne under /admin/
├── static/                   CSS, JavaScript, fonter og bilder, alt fra egen server
├── tests/                    pytest-testene
├── docs/                     Referansestoff: sensorveiledningen og manuell testplan
├── .docs/                    Det som lages underveis: planlegging og implementering (BMAD)
├── .logs/rikke/              Logg over KI-økter og issues.md med åpne punkter
├── .github/workflows/        GitHub Actions: tester og kodesjekker
├── _bmad/                    BMad-oppsett og skript
├── .claude/skills/           BMad-skills og sesjonslogg-skillen som KI-agenten bruker
├── manage.py                 Djangos kommandolinjeverktøy
├── pyproject.toml, uv.lock   Avhengigheter og verktøyoppsett, låst med uv
├── .python-version           Python 3.14
├── .env.example              Alle innstillingene med eksempelverdier
├── AGENTS.md                 Instruksjoner for KI-agenter
└── CLAUDE.md                 Laster inn AGENTS.md og sensorveiledningen, og krever sesjonslogg
```

Hvorfor koden er delt slik, står i arkitekturen under. Mappen `rsvp/` er tom til historiene som trenger den.

`.docs/` og `docs/` har forskjellige roller: `.docs/` er det BMad-verktøyene lager (stien er satt i `_bmad/config.toml`), mens `docs/` er fast referansestoff.

## Dokumentasjon

- [Sensorveiledning del 1](docs/sensorveiledning/sensorveiledning-del1.md): vurderingskriteriene arbeidet styres etter
- [Instruksjoner for KI-agenter](AGENTS.md)
- Planleggingsdokumenter i [.docs/planning-artifacts/](.docs/planning-artifacts/):
  - [Product brief](.docs/planning-artifacts/briefs/brief-aill-handle-it-2026-09-23/brief.md)
  - [PRD](.docs/planning-artifacts/prds/prd-aill-handle-it-2026-11-07/prd.md)
  - [UX: utseende (DESIGN.md)](.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md) og [oppførsel (EXPERIENCE.md)](.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md)
  - Arkitektur: [forklart på norsk](.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/oversikt.md), [reglene koden følger (ARCHITECTURE-SPINE.md)](.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md) og [begrunnelsen for hvert valg](.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/.memlog.md)
  - [Epics og stories](.docs/planning-artifacts/epics.md)
- Implementering i [.docs/implementation-artifacts/](.docs/implementation-artifacts/): spesifikasjon per story og [sprintstatus](.docs/implementation-artifacts/sprint-status.yaml)
- [Manuell testplan](docs/manual-test-plan.md)
- [Sesjonslogg](.logs/rikke/): prompts, KI-økter og beslutninger, koblet til commits, og [åpne punkter](.logs/rikke/issues.md)

## Medlemmer

- Rikke Dvergsdal
