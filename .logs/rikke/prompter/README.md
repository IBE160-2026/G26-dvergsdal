# Prompter for den autonome story-kjøringen

Fra story 1.7 kjøres hver story i en egen, ny Claude Code-økt (`claude -p`), slik at konteksten er tom for hver story. Rikke valgte det 2026-11-20 fordi Claude ikke kan kjøre `/compact` selv (se [story 1.6-loggen](../970-2026-11-20-22-36-16-story-1-6-praktisk-og-var-historie.md)). Goal-prompten står ordrett i [story 1.4b-loggen](../973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md).

- [story-runner.md](story-runner.md): instruksen hver story-økt får: plan, port, implementering, fire gjennomgangsagenter, nettlesersjekker, triage, rettinger, logg, PR og merge.
- [planner-instructions.md](planner-instructions.md): instruksen til planleggingsagenten som skriver specen.
- [run-story.sh](run-story.sh): starter en økt og fortsetter den automatisk etter 5-timersgrensen.

`<scratchpad>` er en midlertidig mappe på Rikkes maskin (Playwright-skript, diff-filer og triage-utkast). Instruksen endres når en retrospektiv ber om det: punkt 7 fra [retrospektiven for epic 1](../967-2026-11-21-13-45-51-retrospektiv-epic-1.md) ga mindre commits, Spec Change Log, triage som PR-kommentar og arbeidsflytkontekst til to av gjennomgangsagentene.
