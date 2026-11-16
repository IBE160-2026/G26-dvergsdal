# Lukke Q8 (samtykkemodellen)

## 2026-11-16 kl. 12:06 — Rikke

### Oppgave
Rikke kjørte `/bmad-help` for å finne ut hva som er neste steg etter arkitekturen. Svaret nevnte det åpne punktet om å spørre faglærer om samtykkemodellen (Q8). Rikke spurte ordrett: «hva mener du med samtykkemodellen?»

### Plan
- KI leste PRD-en (FR-25 til FR-31, §8 Q8), briefens addendum og de to PRD-gjennomgangene som omtaler Q8.
- KI forklarte forskjellen mellom den gamle modellen i briefen (svaret kan ikke sendes uten avkrysning) og den nye (svaret kan alltid sendes, og samtykket gjelder bare allergiene, jf. GDPR art. 7(4)).
- KI anbefalte å lukke Q8 selv i stedet for å spørre faglærer. Rikke svarte ordrett: «lukke selv».

### Resultat
- **`bmad-help`:** planleggingen er ferdig til og med arkitekturen. Neste påkrevde steg er `bmad-create-epics-and-stories` i et nytt kontekstvindu, deretter `bmad-sprint-planning` og `bmad-build`.
- **KI-forslag godtatt:** å lukke Q8 uten å spørre faglærer. Begrunnelsen:
  - Endringen gjør modellen strengere mot personvernreglene, ikke slappere.
  - Begrunnelsen står allerede i briefens addendum og i FR-26 til FR-31.
  - To PRD-gjennomganger hadde foreslått det samme: `tilbakemelding-prd.md` og `review-sensorveiledning.md` (SV-3).
  - Den andre delen av Q8 (hvor fasitlista skal ligge) var allerede besvart av faglærer: i testene og README.
- **Endringer, commit `52cdd9a` på branch `docs/lukke-q8`:**
  - [prd.md](../../.docs/planning-artifacts/prds/prd-aill-handle-it-2026-11-07/prd.md): Q8 i §8 er strøket og merket «Closed 2026-11-16», og endringsloggen har fått en ny rad.
  - [pre-prd-discovery.md](../../.docs/planning-artifacts/research/user-voice-wedding-website-pre-prd-2026-11-06/pre-prd-discovery.md): Q8 er merket som lukket, med henvisning til PRD §8.
- Punktet «spørre faglærer om samtykkemodellen er i orden (Q8)» er lukket i `issues.md`.
- Rikke ba om push (`git push -u origin docs/lukke-q8`). Branchen ligger nå på GitHub og er klar for pull request.

### Åpne punkter
Ingen nye. Neste BMAD-steg (epics og stories) står allerede i `issues.md`.
