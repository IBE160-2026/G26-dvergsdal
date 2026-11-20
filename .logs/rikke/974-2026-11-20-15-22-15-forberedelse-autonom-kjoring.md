# Forberedelse til autonom kjøring av epics og stories

## 2026-11-20 kl. 15:22 — Rikke

### Oppgave
Rikke vil kjøre goal-kommandoen slik at Claude gjennomfører alle gjenværende epics og stories uten menneske i løkka, med én sub-agent per story. Før det ba hun om en liste over hva hun må gjøre i forkant. Prompten, ordrett:

> Jeg ønsker å kjøre goal kommandoen for å gjennomføre alle epics og stories autonomisk uten human in the loops. Før vi gjør det må vi klargjøre hva jeg må gjøre i forkant, blandt annet sørge for at nødvendige API nøkler er på plass, samt sørge for at nødvendige CLI er på plass. Lag en liste over hva jeg må gjøre, slik at du kan gjennomføre alle stories og epics automatisk. Du skal da bruke sub-agenter hver story.

### Plan
- Lese `sprint-status.yaml`, `epics.md`, arkitekturen, `.env.example` og README for å finne eksterne avhengigheter og innhold bare Rikke kan levere.
- Sjekke installerte verktøy, GitHub-innlogging, grenbeskyttelse og testene.
- Lese `bmad-build-auto` for å se når den autonome løkka stopper (HALT).

### Resultat
Ingen kode endret. Funnene:

- **Gjenstår:** 50 stories (6 i epic 1, 13 i epic 2, 5 i epic 3, 5 i epic 4, 5 i epic 5, 6 i epic 6, 4 i epic 7, 6 i epic 8).
- **API-nøkler:** appen trenger ingen (NFR-8, `.env.example` har bare `APP_ENV`, `DEBUG`, `SECRET_KEY` og `ALLOWED_HOSTS`). Hosting, backup og overvåking er utsatt til 2027.
- **Verktøy:** git 2.55, gh 2.101, uv 0.13.8, Python 3.14.10, Node 26.7, Claude Code 2.1.329 er installert. `gh` er logget inn med scopene `gist`, `read:org` og `repo`, men mangler `workflow`. `main` har ingen grenbeskyttelse. `uv run pytest`: 320 bestått.
- **Innhold bare paret kan levere:** story 7.4 krever endelige tekster og tider for programmet og praktisk informasjon «before this story starts». Bildene (`.docs/planning-artifacts/ux/egne-bilder/`) og `Vår historie.docx` finnes.
- **`bmad-build-auto`:** stopper ved skitten arbeidskopi, uklar intensjon og «intent gap», committer lokalt men pusher aldri. Løkka må derfor selv lage gren, PR og merge.
- **Risiko mot sensorveiledningen:** én lang kjøring uten Rikke gir historikk samlet i få perioder og få spor av at gruppen har styrt KI (kriterium 1, kapittel 5). Claude anbefalte å kjøre ett epic om gangen, med Rikkes gjennomgang og retrospektiv mellom epicene.

Claude leverte en liste med det Rikke må gjøre selv (kvote, `workflow`-scope, innhold, fire beslutninger, PC-en våken) og det Claude gjør selv (Playwright-nettleser til skjermsjekker, tillatelser, gren og PR per story, sesjonslogg).

**Rikkes svar (samme økt), ordrett:**

> Profesoren som anbefaler goal på alt på en gang. Du kan merge PR-ene ja. Ta med epic 8 ja. Om en story blir blokkert gjør du det som er ebst for prosjektet. […] for punkt 4 bekrefter jeg alt

Claudes anbefaling om ett epic om gangen ble altså avvist, etter råd fra faglæreren. Alle 50 stories kjøres i én goal-kjøring. Claude merger PR-ene selv, epic 8 er med, og bildene og `Vår historie.docx` er bekreftet endelige.

**Gjort etter svaret:**
- **Test av sub-agenter i flere ledd:** en sub-agent kunne starte en egen sub-agent, men den kjørte i bakgrunnen og svaret kom aldri tilbake. Beslutning: hovedøkten styrer hver story og starter sub-agentene til implementering og gjennomgang selv.
- **`_bmad/custom/bmad-build-auto.toml`:** ny overstyring som sier at løkka venter på varslene fra sub-agentene i stedet for å stoppe med «no subagents», og som laster `AGENTS.md`. Sjekket at den kommer med i den ferdige arbeidsflyten. [PR #23](https://github.com/IBE160-2026/G26-dvergsdal/pull/23): CI grønn, merget av Claude (commit `79b47f7`).
- **Playwright:** nedlastingen av Playwrights egen Chromium hang seg opp to ganger under utpakkingen (`chrome.dll` ble skrevet, `chrome.exe` aldri), trolig fordi antivirusprogrammet låste fila. Beslutning: Playwright 1.55.0 styrer i stedet Edge, som følger med Windows 11 (`channel: 'msedge'`, Edge 157). Testet med et vindu på 360 × 560: virker. Pakken ligger i øktens scratchpad, ikke i prosjektet.
- **Tillatelser:** Claude ville skrive `.claude/settings.local.json` med tillatelser til `git push` og `gh pr merge`, men auto mode avviste skrivingen. Merge av PR #23 gikk likevel gjennom i auto mode, så fila trengs trolig ikke.
- **`gh auth refresh -s workflow`:** ble ikke kjørt første gang, fordi `!` bare virker først i en melding. Rikke kjørte den så som egen melding og godkjente i nettleseren. Tokenet har nå `workflow`.

### Åpne punkter
- Levere endelige tekster og tider for programmet og praktisk informasjon før story 7.4. Er de ikke levert, bygger Claude på det som står i planleggingsdokumentene, og fører opp i story-spesifikasjonen hva som fortsatt er plassholdere.
