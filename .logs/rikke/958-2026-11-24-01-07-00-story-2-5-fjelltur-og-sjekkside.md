# Story 2.5: fjelltur fredag og sjekksiden

## 2026-11-24 kl. 01:07 — Rikke

### Oppgave
Denne økten er en del av den autonome goal-kjøringen. Rikkes goal-prompt er sitert ordrett i [973-…-story-1-4b-papir-bilder-g1.md](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Story-runneren ga denne intensjonen ordrett:

> STORY: 2.5 — The Friday hike and the check page. Sprint-status key: 2-5-the-friday-hike-and-the-check-page […] The check page summarises every step; nothing is written to the database yet (sending is Story 2.6a). Browser checks: a real form submission in Edge through all steps to the check page (validation errors, Back, edit links from the check page), keyboard-only, 360 and 180px, 20px default text. Breakpoints in em.

### Plan
- En planleggeragent skrev [spec-2-5](../../.docs/implementation-artifacts/spec-2-5-the-friday-hike-and-the-check-page.md). Spec-en ble committet alene (6e58b06).
- En implementeringsagent bygde den. Arbeidet ble committet i fire små steg: svarregler, utkastcookie, steg 6 og sjekksiden.
- Fire gjennomgangsagenter gikk gjennom koden, og Claude kjørte nettleserkontrollene med Playwright i Edge.
- Funnene ble sortert, rettinger ble sendt tilbake til implementeringsagenten, og kontrollene ble kjørt på nytt.

### Resultat
- **Steg 6 «Fjelltur fredag»:** de som kommer fredag svarer «Ja», «Nei» eller «Kanskje». Steget hoppes over når ingen kommer fredag. Utkastcookien er nå format 5.
- **Sjekksiden «Se over svaret før du sender»:**
  - Den har én del per steg som gjelder, hver med «Endre».
  - Den viser FR-28-advarselen. Det løser deferred-punktet fra 2.4.
  - Nederst står totalen for husstanden, og så «Send svaret» over «Tilbake».
  - «Endre» bruker `?fra=se-over`.
- **Hva KI foreslo, og hva som ble godtatt, endret eller avvist:**
  - **Planleggerens forslag, godtatt (avgjort av Claude):**
    - Fjellturen er påkrevd for alle som kommer fredag.
    - Det vises ingen priser per linje, bare totalen (AD-12, avvik fra mockupen, notert i DESIGN.md).
    - Bare stegene som gjelder får en del på sjekksiden.
    - «Send svaret» skriver ingenting før story 2.6a.
  - **Implementeringsagentens avvik:** den skrev «Endre hvem som kommer» i stedet for «Endre hvem kommer», fordi spec-ens egen tabell sa det. Godtatt.
  - **Gjennomgangen ga 25 funn:** 10 rettet, 1 utsatt og 14 avvist. Dette ble rettet (commit f99e2b6):
    - en sirkulær import mellom `forms` og `summary`, som Blind Hunter og Edge Case Hunter fant
    - `?fra` forsvant ved omdirigering
    - en tom, valgfri merknad ga linjen «Ikke oppgitt» for alle
    - fredagsregelen er samlet i `joins_hike`
    - nye tester og opprydding i dokumentene
  - **Avvist, med begrunnelse i Review Triage Log:**
    - Å gjøre om `HikeForm`, fordi den følger samme mønster som de andre stegene.
    - En respondentlinje på sjekksiden.
    - At «Send svaret» ikke sender, fordi sendingen er lagt til 2.6a.
  - **Fra nettleseren:**
    - MT-36 a) ventet fokus på feillenken, men mønsteret er at feiloppsummeringen får fokus. Testplanen er rettet.
    - FR-28-advarselen for «Ingen allergier» + «Nei» følger regelen fra 2.4 og er ikke en feil.
- **Verifisert:**
  - `uv run pytest` ga 1158 tester bestått, og ruff og djlint er rene.
  - MT-1 (2.5) og MT-36–38 ble kjørt med Playwright i Edge etter rettingene, med 360/180px og 16/20px tekst. Det var ingen vannrett rulling, «Endre» er 44px høy og knappene står 12px fra hverandre.
- **Commits og PR:** grenen `feat/2-5-fottur-og-sjekkside`, [PR #40](https://github.com/IBE160-2026/G26-dvergsdal/pull/40), med kommentaren fra gjennomgangen.

### Åpne punkter
- **Claude, story 2.6a:** selve sendingen og statusen «Sender …». I tillegg skal totalen som vises på sjekksiden lagres i utkastet (AD-8), og et CSRF-avvik på sjekksiden skal gi en vennlig side (deferred-work.md).
