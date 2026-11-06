# KI-logg

Denne mappen dokumenterer hvordan KI er brukt i prosjektet. Hver fil beskriver én arbeidsøkt med KI: hva jeg ba om, hva KI foreslo, hva jeg godtok, endret eller avviste, og hvilke commits endringene havnet i.

Loggen gjør KI-bruken sporbar for sensor (kriterium 1 i [sensorveiledningen](../../docs/sensorveiledning/sensorveiledning-del1.md)) og er grunnlaget for refleksjonsrapporten i del 2.

## Slik føres loggen

- Én fil per økt, navngitt `ÅÅÅÅ-MM-DD-kort-tema.md`. Kopier [mal.md](mal.md).
- Skriv loggen i samme økt eller rett etter, og commit den sammen med endringene eller like etter.
- Siter de viktigste promptene ordrett. Korte svar som «ja» eller «commit» trengs ikke.
- Lenk alltid til commit-hasher, slik at hver beslutning kan kobles til en konkret endring.
- Ingen ekte gjestedata, navn på gjester eller hemmeligheter. Repoet er offentlig.

Verktøy: [Claude Code](https://claude.com/claude-code) med BMad-metoden (skills i `.claude/skills/`). Fullstendige transkripsjoner ligger lokalt hos Claude Code og er ikke lagt i repoet; øktenes ID står i hver logg.

## Oversikt

| Dato | Økt | Fase | Commits |
|---|---|---|---|
| 2026-09-23 | [Product brief](2026-09-23-product-brief.md) | Planlegging | `e61935e`, `c840dfb` |
| 2026-09-26 | [Fjerne KI-funksjoner fra briefen](2026-09-26-fjern-ki-funksjoner.md) | Planlegging | `ee25e52` |
| 2026-10-23 | [Sensorveiledning og GitHub-arbeidsflyt](2026-10-23-sensorveiledning-og-github.md) | Oppsett | `ba3dbaf`, PR #1 |
| 2026-10-23 | [Brief etter tilbakemelding](2026-10-23-brief-etter-tilbakemelding.md) | Planlegging | `97b70ca`–`6292a01`, PR #2 |
| 2026-10-24 | [Oppsett av KI-loggen](2026-10-24-ki-logg.md) | Prosess | denne branchen |

## Eksempler på styring av KI

En samlet liste over tilfeller der jeg har presisert, avvist eller rettet KI. Detaljene står i hver logg.

- **Avviste `git init`** (2026-09-23): KI opprettet et git-repo på eget initiativ. Jeg ba den angre, fordi repoet skulle kobles til gruppens repo på GitHub.
- **Fjernet KI-funksjonene** (2026-09-26): Briefen sa at emnet krevde en KI-funksjon. Jeg rettet det, og fjernet KI-assistenten fordi den koster penger å drifte.
- **Krevde ny gjennomgang** (2026-10-23): KI mente briefen var ferdig. Jeg ba om en grundig gjennomgang, som fant motsigelser og hull.
- **Gikk imot faglæreren, og snudde selv** (2026-10-23): Jeg beholdt brevanimasjonen i kjernen, men flyttet den senere til «hvis tid» fordi tiden er en risiko.
- **Vurderte KI-ens anbefaling om brukertesten** (2026-10-23): Jeg ville droppe den, KI anbefalte å beholde en enklere variant, og jeg valgte det.
