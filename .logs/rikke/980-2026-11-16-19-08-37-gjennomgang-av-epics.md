# Gjennomgang av epics

## 2026-11-16 kl. 19:08 — Rikke

### Oppgave
Rikke kjørte `/bmad-help` for å se hva som var neste steg. Claude anbefalte Story 1.1 med `bmad-build`, med en valgfri `bmad-review` av `epics.md` først (et åpent punkt fra [epics-og-stories](982-2026-11-16-12-45-37-epics-og-stories.md)). Rikke kjørte `/bmad-review`, og etter funnene svarte hun **«2»**, altså «rette alt nå, også struktur og språk», før koden starter.

### Plan
- Gjennomgå `epics.md` med fire vinkler fra `bmad-review`: adversarial, edge-case-hunter og structure parallelt, og prose oppå structure. Verification-gap hoppes over fordi den bare gjelder kode.
- Lagre rapporten i repoet ved siden av de andre gjennomgangene: [review-epics-2026-11-16.md](../../.docs/planning-artifacts/reviews/review-epics-2026-11-16.md) og en `.json` med de samme funnene.
- Ny branch `docs/epics-review`. Rette i små commits: først arkitekturen og PRD-en der funnene når dit, så epic 1, epic 2, epic 3–8, strukturen og til slutt sprint-status.
- Spørre Rikke bare om ekte produktbeslutninger, én om gangen, og ta tekniske valg selv med begrunnelse (jf. tidligere tilbakemelding).

### Resultat
**Funn:** adversarial 30, edge-case-hunter 46, structure 11 + 2 og prose 18 + 4. Femten problemer ble funnet av flere vinkler uavhengig av hverandre. Det alvorligste: utkast-cookien gjaldt bare `/<kode>/svar/`, så forsida `/<kode>/` kunne aldri vise «Du har et svar som ikke er sendt ennå» (A1/E1). Feilen lå både i arkitekturen og i epics, som Claude skrev tidligere i dag. Claude kontrollerte den selv i filene før rettingen.

**Rikkes beslutning:** På spørsmålet om fredag og søndag uten lørdag valgte Rikke **«Ikke tillatt (anbefalt)»**: dagene må henge sammen. Ført inn i PRD FR-14, FR-15 og FR-70 med endringslogg.

**Rettinger (commits på `docs/epics-review`):**

| Commit | Hva |
|---|---|
| `63d9b03` | Rapporten fra gjennomgangen |
| `639ebdb` | Arkitektur: cookie-sti `/<kode>/`, ødelagte utkast slettes, notat maks 200 tegn og husstand maks 8, revisjon på `Household`, avvist sending lagrer ingen `Submission`, seed bare med `APP_ENV=local`. Begrunnelser i `.memlog.md` |
| `dafbbfe` | PRD: dagene må henge sammen, og lørdagsfrokost krever fredag og lørdag |
| `fb703c2` | Arkitektur: retting av Claudes egen feil i `639ebdb` (se under) |
| `dcc2556` | Epics: AD-linjene i takt med arkitekturen |
| `094e812` | Epic 1: Settings-rad via datamigrering, trygg ny seed-kjøring, låsetilfeller som avstand fra fristen, og 1.4 delt i 1.4a–1.4c med egne kriterier for varsler, høykontrast, redusert bevegelse og lenkeforhåndsvisning |
| `82c15a4` | Epic 2: fristen stopper svar allerede i nivå 1, samtykke per person med bekreftelse for andre, regler for dager og overnatting, «Endre» som legger til en person, ødelagte utkast og CSRF, og 2.6 delt i 2.6a–2.6d |
| `e207b21` | Epic 3–8: blant annet overstyring med skrivebeskyttet samtykke, beløpsregler, søk med æøå, avsender som beholdes ved sletting, tall for sperrer, README med `createcachetable` og gamle lenkekoder som aldri gjenbrukes |
| `6f10bcc` | Struktur: Epic List først, inventaret kortet ned og flyttet bakerst, hver FR viser storyene som bygger den, «Not in this story»-linjer, forklaring av ID-er og personer, «Not in v1» samlet, stående krav for skrivetjenester og endringslogg |
| `8101833` | Sprint-status generert på nytt: 53 stories, alle backlog |
| `ecd3c0b` | Utfallet for hvert funn i rapporten |

**Hva KI foreslo, og hva som ble godtatt eller endret:**
- Gjennomgangen foreslo at gyldige lenkekoder alltid skulle slippe gjennom en sperre. Claude avviste det mens rettingen ble skrevet, fordi sperren da ikke stopper gjetting. Story 8.6 *forsinker* i stedet alle forespørsler fra en adresse som har nådd grensen, slik NFR-4 sier («slowed»). En familie på felles Wi-Fi kommer fortsatt inn.
- For CSRF-feil foreslo gjennomgangen å si at det siste steget må fylles ut på nytt. Claude valgte i stedet å vise steget igjen med det gjesten skrev, slik EXPERIENCE.md lover.
- Ved endrede allergier uten svar på samtykke foreslo gjennomgangen en feltfeil. Claude valgte en advarsel på kontrollsida, fordi FR-28 sier at man alltid kan sende uten samtykke.

**Feil i Claudes egne rettinger, fanget underveis:**
- Første ordlyd for seed sa at en manglende `APP_ENV` skulle stoppe kommandoen. Det ville stoppet sensors testdata, fordi AD-14 krever at appen kjører uten `.env`. Rettet i `fb703c2`.
- Første kjøring av sporingen fra FR til story fanget «NFR-1» som «FR-1» og ga feil storyer. Fila ble tilbakestilt, og skriptet ble rettet før noe ble committet.
- Mens kriteriene ble skrevet, flyttet Claude CSRF-kriteriet fra story 1.8 til 2.1, fordi skjemaet ikke finnes før story 2.1.

**Tekniske valg Claude tok** (står i endringsloggen i epics.md): maks 8 personer per husstand, 2 punkter i «Trenger oppfølging» før «Vis alle» (fra EXPERIENCE.md-skissa, kan endres etter måling), innloggingssperre ved 5 feil per brukernavn eller 20 per adresse på 15 minutter, og forsinkelse ved 20 ukjente lenkekoder på 15 minutter.

Rikke ba om **«push og lag PR»**: `docs/epics-review` er pushet, og [PR #17](https://github.com/IBE160-2026/G26-dvergsdal/pull/17) er laget mot `main` med en tabell over commits, beslutninger og hva som bør sjekkes.

Rikke merget PR #17 på GitHub. Lokal `main` er oppdatert med `git pull` og står likt med `origin/main` (merge-commit `501c560`), og den lokale branchen `docs/epics-review` er slettet.

Lukket punkt i `issues.md`: «vurdere en `bmad-review` av epics.md før koden starter».

### Åpne punkter
- Se over Claudes tekniske valg fra gjennomgangen: maks 8 personer per husstand, 2 punkter i «Trenger oppfølging» og tallene for innloggings- og lenkesperrer (endringsloggen i `epics.md`).
- **2027:** sørge for at `APP_ENV=production` er satt på serveren. Mangler den, gjelder lokale standarder, og da slår verken produksjonssjekkene i AD-14 eller seed-sperren inn.
