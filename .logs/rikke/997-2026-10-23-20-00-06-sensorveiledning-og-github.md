# Sensorveiledning og GitHub-arbeidsflyt

## 2026-10-23 kl. 20:00 — Rikke

### Oppgave

Sørge for at sensorveiledningen styrer alt arbeidet med KI, og lære arbeidsflyten med branch og pull request.

### Plan

- Claude Code uten BMad-skill. Økt-ID `07d2fd81-0973-41ac-8637-2e32c2fa5f79` og `f8a14b73-5c49-4ecb-b102-5f0bd00ee8f6`.
- Branch `docs/sensorveiledning`, PR #1.
- Loggen er etterregistrert 2026-10-24 fra de lokale transkripsjonene og git-historikken.

Viktige prompts, ordrett:

> I mappen vi jobber i ser du at jeg har lagt inn en sensorveiledning. Denne er veldig viktig at vi forholder oss til gjennom hele prosessen. Gjør slik at/plasser den et sted hvor du vet at den vil bli tatt ordentlig med i prosessen med å utvikle bryllupsnettsiden. Karakteren i faget benytter denne.

KI lagde en markdown-versjon av PDF-en, la begge i `docs/sensorveiledning/`, og skrev `AGENTS.md` med instruksjoner til KI-agenter. `CLAUDE.md` importerer begge, slik at de leses i hver økt.

> er det best sånn det er nå, eller å slette PDFen og kun ha markdown?

> er dette nødvendig for meg som jobber alene på prosjektet?

> jeg er helt ny i dette og trenger den veiledningen jeg kan få slik som dette. kan du sørge for at jeg får det?

### Resultat

Commits: `ba3dbaf` Legg til sensorveiledning del 1 som styrende dokument, `e2459f5` merge av PR #1.

| Forslag fra KI | Min vurdering | Resultat |
|---|---|---|
| Legge sensorveiledningen inn som styrende dokument via `AGENTS.md` og `CLAUDE.md` | Godtatt | `ba3dbaf` |
| Beholde både PDF (original) og markdown (det KI leser) | Godtatt etter at jeg spurte om PDF-en burde slettes | `ba3dbaf` |
| Bruke branch og pull request i stedet for å committe rett på `main` | Spurte om det var nødvendig når jeg jobber alene. Godtatt fordi sensor ser etter det under kriterium 1. Små rettelser kan gå rett på `main` | PR #1 |
| Lagre at jeg trenger enkel veiledning på norsk | Mitt ønske. KI lagret det i sitt minne for senere økter | – |

Feil eller svakheter i KI-ens arbeid: Markdown-versjonen er KI-ens avskrift av PDF-en, og nummereringen i kapittel 3 er endret. Derfor beholdes PDF-en som originalen ved tvil.

### Åpne punkter

- Gå gjennom tilbakemeldingen fra faglærer på briefen. Løst samme dag i [brief-etter-tilbakemelding](996-2026-10-23-22-05-34-brief-etter-tilbakemelding.md).
