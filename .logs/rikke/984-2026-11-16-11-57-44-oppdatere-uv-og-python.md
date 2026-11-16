# Oppdatere uv og Python

## 2026-11-16 kl. 11:57 — Rikke

### Oppgave
Gjøre klar maskinen før koden starter. Arkitekturøkta fant at uv 0.12 var utdatert, og at uv 0.13 velger Python 3.15 når ingen versjon er låst. Prosjektet skal kjøre på siste Python 3.14.

### Plan
- Rikke kjørte to kommandoer selv i terminalen: `uv self update` og `uv python install 3.14`.
- KI sjekket at resultatet stemmer med arkitekturen ([ARCHITECTURE-SPINE.md](../../.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md): `.python-version` = 3.14, `requires-python` = `>=3.14,<3.15`) og med funn F2 i [review-tech-currency.md](../../.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/reviews/review-tech-currency.md).

### Resultat
- uv er oppdatert fra 0.12.18 til 0.13.8.
- Python 3.14.10 er installert som uv-styrt Python.
- KI kjørte `uv python list --only-installed` for å kontrollere. 3.14.10 ligger nå i uv sin mappe. Den gamle 3.14.0 fra python.org ligger fortsatt på PATH som `python`. uv foretrekker likevel sine egne Python-versjoner, så prosjektet vil bruke 3.14.10 når `.python-version` blir lagt inn. Den gamle installasjonen trenger ikke fjernes.
- KI sjekket også `technology.md`, som sier Python 3.12. Det er ikke en motsigelse: fila er faglærers referanse fra Pytagoras-prosjektet og beskriver ikke denne appen.
- Ingen endringer i koden. Punktet «oppdatere uv til 0.13 og Python til siste 3.14» fra [arkitekturøkta](985-2026-11-16-09-15-23-arkitektur.md) er lukket i `issues.md`.

### Åpne punkter
Ingen.
