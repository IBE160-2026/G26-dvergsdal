# G26 — AI'll handle it

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Dokumentasjon

- [Sensorveiledning del 1](docs/sensorveiledning/sensorveiledning-del1.md): vurderingskriteriene arbeidet styres etter
- [Instruksjoner for KI-agenter](AGENTS.md)
- [Planleggingsdokumenter](.docs/planning-artifacts/)
- [KI-logg](.docs/ki-logg/): prompts, KI-økter og beslutninger, koblet til commits

## Mappestruktur

```text
.
├── .docs/                    Det som lages underveis i prosessen
│   ├── planning-artifacts/   BMad-dokumenter: product brief, PRD, arkitektur, epics
│   └── ki-logg/              Logg over KI-økter, prompts og beslutninger
├── docs/                     Referansestoff om prosjektet
│   └── sensorveiledning/     Vurderingskriteriene (PDF-original og markdown)
├── _bmad/                    BMad-oppsett og skript
├── .claude/skills/           BMad-skills som KI-agenten bruker
├── AGENTS.md                 Instruksjoner for KI-agenter
└── CLAUDE.md                 Laster inn AGENTS.md og sensorveiledningen i Claude Code
```

`.docs/` og `docs/` har forskjellige roller: `.docs/` er det BMad-verktøyene lager (stien er satt i `_bmad/config.toml`), mens `docs/` er fast referansestoff som verktøyene leser. Applikasjonskoden får sin egen mappe når implementeringen starter.

## Medlemmer

- Rikke Dvergsdal
