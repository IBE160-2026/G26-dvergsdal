# Story 2.4: Allergier og samtykke

## 2026-11-23 kl. 20:11 — Rikke

### Oppgave
Dette er en del av den autonome goal-kjøringen. Rikkes goal-prompt er sitert ordrett i [973-…-story-1-4b-papir-bilder-g1.md](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Story-runneren ga denne intensjonen ordrett:

> STORY: 2.4 — Allergies and consent. Sprint-status key: 2-4-allergies-and-consent […] Allergy data is sensitive (health data): follow the PRD/architecture rules on consent and storage exactly; Story 2.6b stores allergies only with consent, so keep the boundary the epics set.

### Plan
- En planleggeragent skrev [spec-2-4](../../.docs/implementation-artifacts/spec-2-4-allergies-and-consent.md).
- En implementeringsagent fulgte spec-en. Den ble stoppet av bruksgrensen og fortsatte etterpå.
- Fire KI-agenter gikk gjennom koden: Blind, Edge Case, Verification Gap og Intent. Gjennomgangen ble også stoppet av bruksgrensen og fortsatte etterpå.
- Claude kjørte MT-1 (2.4), MT-33, MT-34 og MT-35 i Edge.
- Funnene ble sortert, rettet og målt på nytt. Til slutt kom PR og merge.

### Resultat
**Kode:**
- Reglene: `wedding/rules/allergies.py`.
- Samtykkeversjonen: `wedding/services/consent.py` med `CONSENT_TEXT_VERSION`.
- Steg 5 i `wedding/rsvp/`, malene `allergy_fields.html` og `consent_text.html`, og skriptet `static/js/rsvp-allergies.js`.
- Kladdecookien er nå format 4.
- Ingenting skrives til databasen.

**Hva KI foreslo, og hva som ble godtatt, endret eller avvist:**
- **Planleggeren, godtatt.** Disse valgene er avgjort av Claude etter goal-regelen:
  - Samtykket gis per person, ikke per husstand. Det følger epics-AC og FR-29, mens mockupen hadde ett samtykke for husstanden. Teksten bruker «dere» i stedet for «du».
  - Et «Nei» sletter ikke det gjesten har skrevet i kladden (AD-8). I stedet sier et «Obs»-varsel at opplysningene ikke blir lagret.
  - «Ingen allergier eller matbehov» regnes som allergiopplysning og trenger samtykke.
  - Samtykketeksten er versjonert, og en test kobler versjonen til en hash av teksten.
- **Gjennomgangen ga 24 funn, og 4 ble rettet:**
  - Hash-testen ville feilet ved CRLF-utsjekk på Windows.
  - En forfalsket bekreftelse for den som svarer, ble godtatt.
  - Varselet gikk 47px ut over skjermen ved 180px. Det fant Claude selv i den første målingen i Edge (`.notice__text` manglet `min-width: 0`).
  - README sa det samme om lagring to ganger.
- **Utsatt:** 2 funn. Personvernteksten om kladden går til story 7.1, og lagring av samtykketekstens versjon til 2.6b/2.6c.
- **Avvist:** 18 funn. Eksempler:
  - «Cookien blir over 4 KB med åtte merknader med æøå» er feil. Claude målte verste tilfelle til 1 836 tegn, fordi cookien er komprimert.
  - Forskjellen mellom `maxlength` og `len` ble avvist, fordi nettleseren er den strengeste av de to.
  - Varselet for «Ingen …» ble avvist, fordi det er et bevisst valg i spec-en.

**Verifisert:**
- `uv run pytest`: 1106 bestått. ruff og djlint er rene.
- MT-1 (2.4) og MT-33–35 er bestått i Edge etter rettingene: 0px overflyt ved 360, 180 og 320px og ved 20px tekst, og valgflater på minst 44px.

**Commits:** 301d1eb (spec), 7cf7732, d5bab6f, db1856b, 5155829, 5fc242f, 90153ec og a256956 (rettinger), 3562cd4, 18d6c21. PR: https://github.com/IBE160-2026/G26-dvergsdal/pull/39

### Åpne punkter
Ingen nye punkter for Rikke. De to utsatte funnene ligger i `deferred-work.md` under navngitte stories.
