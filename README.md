# G26 — AI'll handle it

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

**AI'll handle it** er bryllupsnettsiden til Rikke og Valdemar. Hver gjest får en personlig lenke som er den eneste innloggingen: der ser gjesten invitasjonen, programmet og praktisk informasjon, og svarer for husstanden sin. Brudeparet og hjelperne får en oversikt over svar, allergier og betalinger. Nettsiden er laget for gjester i alle aldre på mobil, og den er utviklet med KI og BMAD-metoden.

Repoet inneholder applikasjonen og dokumentasjonen av utvikling, testing og kvalitetssikring med KI.

> **Status:** Prosjektgrunnmuren er på plass (story 1.1): Django-prosjektet, innstillinger, brukermodellen, tester og sjekker. Det finnes ingen sider ennå. Siden for ugyldige lenker kommer i story 1.4b og invitasjonens forside i story 1.5, så foreløpig viser `http://127.0.0.1:8000/` Djangos egen startside.

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

Ruff sjekker og formaterer Python-koden, djLint sjekker Django-malene. Det finnes ingen maler før story 1.4a, så djLint melder foreløpig at den ikke fant noe å sjekke, og avslutter uten feil.

Sjekker som ikke kan automatiseres, for eksempel hvordan sidene ser ut på en smal mobilskjerm, står i [docs/manual-test-plan.md](docs/manual-test-plan.md).

## Innstillinger

Appen trenger ingen innstillinger for å kjøre lokalt: alt har trygge standardverdier, og det trengs ingen `.env`-fil. Innstillingene leses fra miljøvariabler, og alle står med eksempelverdier i [.env.example](.env.example).

| Variabel | Lokal standard | Forklaring |
|---|---|---|
| `APP_ENV` | `local` | `local` eller `production`, skrevet nøyaktig slik. Alt annet (for eksempel `prod`) gjør at appen nekter å starte. |
| `DEBUG` | `true` lokalt, `false` i produksjon | Djangos feilsøkingssider. |
| `SECRET_KEY` | en fast nøkkel bare for lokal bruk | Signeringsnøkkel. Produksjon må ha sin egen lange, tilfeldige nøkkel. |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` | Kommaseparerte domenenavn nettsiden svarer på. |

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
│   ├── links.py              Gjør en personlig lenkekode om til en gjest
│   ├── management/commands/  Kommandoer, for eksempel testdata
│   ├── fixtures/             Testdata og fasit (TOML)
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

Hvorfor koden er delt slik, står i arkitekturen under. Mappene `rules/`, `services/`, `rsvp/` og `fixtures/` er tomme til historiene som trenger dem.

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
