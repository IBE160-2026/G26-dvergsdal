# 2026-09-26 – Fjerne KI-funksjoner fra briefen

| | |
|---|---|
| **Verktøy** | Claude Code, BMad-skill: `bmad-product-brief` (oppdatering) |
| **Økt-ID** | `b52d3c82-6f9f-4c63-bfe5-26bf219690cc` |
| **Branch / PR** | `main` |
| **Commits** | `ee25e52` Fjern AI-funksjoner fra produktbriefen |

## Mål

Fjerne KI-funksjonene fra nettsiden, fordi de koster penger å drifte og ikke er et krav i emnet.

## Viktige prompts

> ønsker å endre briefen min. viser seg at å ha AI implementert i nettsiden min koster penger og ikke er et krav i faget. ønsker derfor å fjerne det fra mitt prosjekt

KI pekte på at `.memlog.md` og briefen sa at emnet *krevde* en KI-funksjon, og spurte om jeg hadde sjekket dette med faglærer eller oppgaveteksten før vi låste det.

> ja, bekrefter at AI feature ikke må inngå i applikasjonen. 1. fjern 2. kan være en mulighet å lage en funksjon som gjør siden på engelsk. eks en knapp øverst som kan bytte til engelsk. ikke et must, men fint om jeg har tid og mulighet. 3. ja 4. behold 5. korrekt

## Hva KI foreslo, og hva jeg gjorde

| Forslag fra KI | Min vurdering | Resultat |
|---|---|---|
| Fjerne KI-assistenten for gjester | Godtatt | `ee25e52` |
| Fjerne KI-hjelp til sengeplassering | Godtatt | `ee25e52` |
| Hva gjør vi med gjester som ikke snakker norsk? | Mitt forslag: en språkknapp øverst som «hvis tid» | `ee25e52` |
| Beholde navnet «AI'll handle it»? | Beholdt. Navnet viser til at siden bygges med KI | `ee25e52` |
| Erstatte suksesskriteriet for KI-assistenten | Godtatt: et gjestespørsmål skal vises i admin og komme fram på e-post | `ee25e52` |

## Feil eller svakheter i KI-ens arbeid

Briefen fra 2026-09-23 sa at emnet krevde en KI-funksjon. Det kom fra min egen misforståelse, og KI skrev det inn som et krav uten å stille spørsmål ved det. Da jeg ville rette det, sjekket KI motsigelsen mot loggen før den endret noe. I `.memlog.md` står det som en `(override)` som opphever den gamle beslutningen.

## Neste steg

Vente på tilbakemelding fra faglærer på briefen. Den kom 2026-10-06 (`1477330`).
