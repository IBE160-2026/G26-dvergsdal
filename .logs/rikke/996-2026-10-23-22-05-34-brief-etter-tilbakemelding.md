# Brief etter tilbakemelding

## 2026-10-23 kl. 22:05 — Rikke

### Oppgave

Tilpasse briefen etter [tilbakemeldingen fra faglærer](../../.docs/planning-artifacts/briefs/brief-aill-handle-it-2026-09-23/tilbakemelding-product-brief.md) (`1477330`).

### Plan

- BMad-skill `bmad-product-brief` i oppdateringsmodus, i Claude Code. Økt-ID `fa141904-b89e-43f0-b8ea-e7496946ae81`.
- Branch `docs/brief-etter-tilbakemelding`, PR #2.
- Loggen er etterregistrert 2026-10-24 fra den lokale transkripsjonen og git-historikken.

Viktige prompts, ordrett:

> Jeg har fått tilbakemelding på prosjektet av professoren min. La oss se på det og tilpasse oss.

> er alt i tilbakemeldingen håndtert? Og hva vil In si? og hva med v2? når er de til? ønsker at sidene er tilnærmet ferdig når jeg leverer i desember

> ikke helt sikker på at vi er i mål med briefen. gå ordentlig gjennom den. først alene så i lys av tilbakemeldingene

> 1. god ide 2. kan vi droppe brukertesten? 3. okey

### Resultat

Commits: `97b70ca`, `2e4b519`, `9aa86df`, `3128bcd`, `a32fd37`, `f4d638e`, `6292a01`, merge `bee4f72`.

| Forslag fra KI | Min vurdering | Resultat |
|---|---|---|
| Bare fiktive data i repoet, egen seksjon om data og personvern | Godtatt (faglærers hovedpunkt) | `97b70ca` |
| Skille emneleveransen (desember 2026) fra det ekte bryllupet | Godtatt | `97b70ca` |
| E-post valgfri: logg til konsoll uten nøkkel | Godtatt (faglærers forslag) | `97b70ca` |
| Flytte brevanimasjonen ut av kjernen (faglærers forslag) | **Avvist først**, jeg ville beholde den. Senere samme dag flyttet jeg den selv til «hvis tid» fordi tid er en risiko | `2e4b519`, `3128bcd` |
| Taleønsker, gaveliste og lenkesporing som «andre trinn» | Endret: jeg vil at siden skal være så godt som ferdig i desember. Endte som «hvis tid og kapasitet» | `9aa86df`, `3128bcd` |
| Brukertest i slutten av november | Endret til første uke i desember | `9aa86df` |
| Overnatting per natt | Endret: hele helgen eller ingenting. Priser vises ved hvert valg, betaling per husstand | `3128bcd` |
| – | Mitt eget tillegg: PC-tilpasning og utskriftsside for admin under «hvis tid» | `a32fd37` |
| Beholde brukertesten i en enklere form | Jeg spurte om den kunne droppes. Valgte KI-ens alternativ A: testen gjøres på min telefon eller PC | `6292a01` |

Feil eller svakheter i KI-ens arbeid:

- Etter første runde mente KI at briefen var ferdig. Jeg var ikke enig og ba om en grundig gjennomgang. Den fant motsigelser (emneomfang mot ønsket om å bli ferdig i desember, «hytteneter» mot hele helgen, et utdatert antall uker) og hull (hvordan admin oppretter gjester, prismodell, hva som skjer uten samtykke, tilgjengelighet, hvor dataene lagres). Alt ble rettet i `3128bcd`.
- Først var all PC-tilpasning lagt under «hvis tid». Ved gjennomgangen ble det tydelig at sensor kjører siden på PC, så den må også fungere der med mobiloppsettet. Bare et eget PC-oppsett er nå «hvis tid» (`f4d638e`).

### Åpne punkter

- Starte en KI-logg. Løst 2026-10-24 i [ki-logg](995-2026-10-24-11-17-37-ki-logg.md).
- Lage PRD med `bmad-prd`. Ført i [issues.md](issues.md).
