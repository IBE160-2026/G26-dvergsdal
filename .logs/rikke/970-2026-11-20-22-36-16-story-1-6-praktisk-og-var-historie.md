# Story 1.6: Praktisk informasjon og Vår historie

## 2026-11-20 kl. 22:36 — Rikke

### Oppgave
Fjerde story i den autonome goal-kjøringen (prompten er sitert i [story-1-4b-papir-bilder-g1](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md)). Intensjonen til `bmad-build-auto` var «Story 1.6 i .docs/planning-artifacts/epics.md»: gjesten skal kunne lese hvordan man kommer seg dit, hvor man sover, husreglene og parets egen historie.

Midt i økten skrev Rikke, ordrett:

> kjør compact etter hver merget PR

Claude svarte at `/compact` er en innebygd kommando som bare brukeren kan skrive. Claude kan ikke starte den selv. Claude melder derfor tydelig fra etter hver merget PR, så Rikke kan kjøre den. Ellers komprimerer Claude Code automatisk.

### Plan
- Gren `feat/1-6-praktisk-og-var-historie`. Planleggings-sub-agenten skrev [spec-1-6](../../.docs/implementation-artifacts/spec-1-6-practical-information-and-our-story-pages.md). Deretter fulgte en implementerings-sub-agent og fire gjennomgangs-sub-agenter.
- MT-1 (1.6) og MT-16 til MT-18 med Playwright mot Edge. Claude kjørte også en egen måling av hopp til-lenkene fra 260 til 480 px.

### Resultat
**Bygd:** Praktisk informasjon med «Hopp til» og sju ark i fast rekkefølge (plassholdertekst fra mockupen, i malene), og Vår historie med ett ark, ni kapitler og signaturen i Imperial Script.

**Hva KI foreslo, og hva som ble godtatt, endret eller avvist:**
- **Godtatt fra planleggeren:**
  - Kartknappen «Åpne veibeskrivelse i kart» bygges ikke ennå. Mockupen lenker til `#`, adressen er en plassholder og kartjenesten er ikke valgt. Den er flyttet til story 7.4.
  - Prikkene er skjulte `span`-er i HTML i stedet for CSS-tekst, fordi noen skjermlesere leser opp CSS-tekst.
  - Teksten i Vår historie er hentet fra den godkjente mockupen.
- **Funnet i gjennomgangen og bekreftet av Claude i Edge:** Blind Hunter og Edge Case Hunter påsto at en prikk kunne starte en linje. Målingen viste at «· Antrekk» sto alene på en egen linje fra 260 helt opp til 360 px. Årsaken er at den selvhostede EB Garamond er bredere enn Google Fonts-versjonen mockupen ble godkjent med. Det ble rettet med 5 px prikkmarg (før 7 px), uten sidemarg på nav, og med et em-basert brytningspunkt på 22.5em. Ny måling: tre linjer fra 360 px, én lenke per linje uten prikker under, og ingen prikk starter en linje.
- **Andre rettinger (15 rader totalt):**
  - Story 7.4 fikk kriterier for kartknappen og for en test som feiler når gjestesidene fortsatt har «[…]».
  - EXPERIENCE.md sa fortsatt `scroll-margin-top` for svarfeltet.
  - Testene ble ryddet for duplikater og for en påstand om du/dere som ingen test sjekket.
  - Hårlinjen bruker nå fargetokenet i stedet for en hardkodet farge.
- **Avvist (9):** blant annet at MT-radene ikke var kjørt (de var kjørt) og at skjermleserskjulingen bare var sjekket i markup (MT-18 leste tilgjengelighetstreet).
- **Brukergrense:** implementeringsagenten stoppet midt i rettingene da 5-timersgrensen ble nådd. Den fortsatte fra der den slapp etter nullstillingen. Utviklingsserveren ble stoppet av systemet på grunn av lite minne, så nettlesersjekkene kjører nå med en server som startes og stoppes i samme kommando.

**Verifisert:** `uv run pytest` 604 bestått, ruff og djlint rene. MT-1 (1.6), MT-16 (klikk, tastatur og touch), MT-17 og MT-18 bestått i Edge.

**Commits:** spec `d24e212`, deretter fire commits for sidene, design/epics, dokumentasjon og ferdigstilling. [PR #28](https://github.com/IBE160-2026/G26-dvergsdal/pull/28).

### Åpne punkter
Ingen nye. Plassholderne i Praktisk informasjon og «[stilling]» i Vår historie står allerede som åpne punkter til story 7.4.
