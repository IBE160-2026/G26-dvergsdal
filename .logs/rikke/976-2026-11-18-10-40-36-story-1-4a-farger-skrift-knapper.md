# Story 1.4a: farger, skrift, knapper og varsler

## 2026-11-18 kl. 10:40 — Rikke

### Oppgave
Bygge story 1.4a med `bmad-build`: invitasjonens farger, skrift, knapper og varsler som et felles designsystem. Story 1.4b–1.8 skal bygge på det.

Prompts, ordrett:
- `/bmad-build` → valg: «Story 1.4a (Recommended)»
- Eksempelside: «Ja, lag /stil/ (Recommended)»
- Lengde på spec-en: «Behold hele (Recommended)»
- «hvordan sjekker/tester jeg den?»
- «1» (godkjenn spec-en og fortsett)

### Plan
- Epic 1-konteksten var utdatert (epics, AD-16 og FR-60 var endret etter at den ble laget), så Claude lagde den på nytt med en underagent før planleggingen.
- Spec: [spec-1-4a-the-invitation-s-colours-type-buttons-and-notices.md](../../.docs/implementation-artifacts/spec-1-4a-the-invitation-s-colours-type-buttons-and-notices.md), med Rikkes to beslutninger (eksempelsiden `/stil/`, spec-en samlet selv om den er ca. 2 000 tokens).
- Rikkes spørsmål om hvordan hun kan teste viste et hull: eksempelsiden manglet en hopp-lenke for å teste redusert bevegelse (MT-3). Den ble lagt inn i spec-en før godkjenning.
- En underagent implementerte fra spec-en. Tre uavhengige gjennomganger (Blind Hunter, Edge Case Hunter og Verification Gap) gikk gjennom koden, og Claude vurderte hvert funn mot koden.

### Resultat
- **Grenen `feat/1-4a-farger-skrift-knapper`, åtte commits:** bc8399e (spec og epic-kontekst), fe9a83b (fonter), 76e6b6f (stilark), 826419f (grunnmal og varsel), 7c05f3b (stilprøven `/stil/`), f807c16 (tester), 99f83ba (README, testplan og arkitektur) og 794c481 (gjennomgang, spec ferdig og sprint-status `review`).
- **Det som ble laget:**
  - `static/css/site.css` med alle DESIGN.md-tokens som CSS-variabler.
  - Imperial Script og EB Garamond som egne WOFF2-filer, med OFL-lisens, SHA-256 og kommandoene i `static/fonts/README.md`.
  - `wedding/templates/wedding/base.html` og varsel-includen.
  - Stilprøven `/stil/`, som bare finnes når `APP_ENV` er `local`.
  - 116 nye tester i `tests/test_design_system.py`.
  - MT-2 til MT-4 og en ny MT-1-rad i den manuelle testplanen.
- **Verifisert:** 320 tester består. Ruff, djLint og `makemigrations --check` er grønne. Hver rad i spec-ens testtabell har en test som kjører og består.
- **Etter økten:** Rikke åpnet `/stil/` og fikk bare Djangos «Installasjonen var vellykket!». Årsaken var at serveren på port 8000 kjørte fra en annen klone (`C:\Test\G26-dvergsdal`, på `main`). Fra riktig mappe virket siden, og Rikke godkjente utseendet («alt ser bra ut, gå videre»). Grenen ble pushet og [PR #21](https://github.com/IBE160-2026/G26-dvergsdal/pull/21) laget. GitHub Actions er grønn.
- **Merget:** Rikke merget PR #21 (`478ee18`). Story 1.4a er satt til `done` i sprint-status (`aa111ce`).
- **Manuelle tester:** Rikke kjørte MT-1 (1.4a), MT-2, MT-3 og MT-4 i nettleser, og alle besto. Hun skrev resultatet for MT-2 som «Alt ble sort med lyse kanter og lys tekst». Claude spurte om resten av det testen krever, altså kant på alle knappene, strek og ikon på varslene og fokusring ved `Tab`, før det ble ført som «Bestått». Editoren hennes formaterte også tabellen på nytt, og det ble beholdt.
- **Bivirkning:** URL-oppsettet er ikke lenger tomt, så `/` og testlenkene viser Djangos «Page not found (404)» til story 1.4b. README og MT-1 er oppdatert.
- **KI-styring og retting av KI-kode:**
  - Implementeringsagenten oppdaget selv at `:active` på alle elementer ville tegnet fokusringen rundt hele siden ved hvert trykk, og begrenset den til lenker, knapper og skjemafelt.
  - De tre gjennomgangene ga 26 funn. 15 ble rettet, 10 avvist med begrunnelse og 1 utsatt.
  - Blant de rettede funnene:
    - Knappetesten var triviell: `.button` matchet også `.button--secondary`, og ingen deklarasjoner ble sjekket.
    - `outline: 0px` slapp gjennom testen for fjernet fokusring.
    - Den smale `:active`-rettingen hadde ingen test.
    - Omriss-knappen ble usynlig (krem på krem) på kremfarget ark.
    - Fontkildene kunne ikke etterprøves.
  - Agenten ødela koden med vilje for å sjekke at de nye testene fanger feilene: en bar `:active`, `outline-width: 0px`, feil bakgrunn på hovedknappen og en omdøpt `head`-blokk. Alle fire ble fanget.
  - Det utsatte funnet (skjermlesere og varsler som legges inn med JavaScript) står i [deferred-work.md](../../.docs/implementation-artifacts/deferred-work.md).
  - Hele vurderingen står i Review Triage Log i spec-en.

### Åpne punkter
- **Story 2.7 eller 4.2:** det første varselet som legges inn med JavaScript må ha en tom live region i siden fra start, og testes med skjermleser (deferred-work.md).
- Neste BMAD-steg: story 1.4b (papir, Rikkes bilder og siden for ugyldige lenker) med `bmad-build`.
