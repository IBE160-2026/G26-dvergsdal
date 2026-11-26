# Story 3.3 — Hvert tall åpner menneskene bak

## 2026-11-27 kl. 09:00 — Rikke

### Oppgave
Del av den uovervåkede goal-kjøringen. Rikkes goal-prompt står ordrett i [973-loggen](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Intensjonen for bmad-build-auto var ordrett: «Story 3.3 i .docs/planning-artifacts/epics.md». Hvert tall over 0 på Oversikt skal åpne listen over menneskene bak tallet (FR-55, UX-DR41, AD-2, NFR-2).

### Plan
- Spec: [spec-3-3-every-count-opens-the-people-behind-it.md](../../.docs/implementation-artifacts/spec-3-3-every-count-opens-the-people-behind-it.md), skrevet av en planleggeragent. Implementering ved en egen agent i åtte små commits (retro-punkt 12 fra epic 2), fire gjennomgangsagenter og nettleserkjøring i Edge med Playwright.

### Resultat
**Hva KI foreslo, og hva som ble godtatt, endret eller avvist**
- Planleggeren foreslo et register `dashboard/counts.py` (slug, tittel, type, regelkall) som eneste kilde for Oversikt, lenkene og tellesiden A3 på `/admin/tall/<slug>/`, slik at radene er lik tallet per konstruksjon. Godtatt.
- A3 viser bare navn, ikke allergidetaljer, fordi den samtykkesjekkede listen er story 3.4; «Se hva alle har svart» er fortsatt vanlig tekst. Godtatt (avgjort av Claude).
- Implementereren bygde ruten og A3 før lenkene og delte malen per rad (`_cells.html`) i stedet for per celle, fordi et mellomrom ga «3 ja , 2 kanskje». Godtatt og ført i Spec Change Log.
- Gjennomgangen ga 22 funn: 4 rettet, 4 utsatt, 14 avvist.
  - Rettet: testen godtok et tall som manglet på Oversikt, de gjengitte lenkene ble aldri fulgt i en test, skjermleseren leste navn og husstand som én streng, utdatert tekst i DESIGN/EXPERIENCE/README.
  - Avvist blant annet: manglende id mellom to spørringer (ikke vist at det kan skje), gjentatt regelberegning (lite data), at allergilistene viser kategori til hjelperen (reglene følger samtykke, den samtykkesjekkede listen er 3.4) og at manuelle tester ikke var kjørt (kjøres etter gjennomgangen).
- Nettleser: MT-75 til MT-78 bestått. Mitt første skript viste «FEIL» for ni lenker fordi skriptet antok at `h1` starter med radetiketten; det var en skriptfeil, ikke en feil i siden. 404-siden ble sjekket med `DEBUG=False`, siden `DEBUG=True` viser Djangos tekniske 404. Alt+Left leveres ikke av Playwright, så tilbake ble målt med `goBack()`.

**Verifisert:** `uv run pytest` 1573 beståtte tester, ruff, ruff format og djlint rene. Nettleser: 30 lenker som hver åpner en liste med `li` = `h1`-tall = lenketall, 6 nuller uten lenke, utlogget avvist, hjelper, bare tastatur, 360 og 180 px ved 18 og 22,5 px uten overflyt og med mål på minst 44 px.

**Commits:** `da8e88d` til «Story 3.3 ferdig» på `feat/3-3-tall-apner-personene`. PR: https://github.com/IBE160-2026/G26-dvergsdal/pull/51

**Løst fra issues.md / deferred-work.md:** 3.3-halvdelen av «tallene blir lenker».

### Åpne punkter
- Story 3.4: adressen til «Se hva alle har svart», allergilisten med samtykke og lenke fra husstandsrader til A6.
- Polishstory: dobbel kolon i overskrifter som «Betaling: Delbetalt: 0 husstander».
- Delte testhjelpere bør flyttes til `tests/helpers.py`.
