# Story 2.6d: testdata med svar og ekte sending i nettleser

## 2026-11-25 kl. 20:36 — Rikke

### Oppgave
Del av den uovervåkede goal-kjøringen. Rikkes goal-prompt står ordrett i [973-loggen](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Intensjonen for bmad-build-auto var ordrett: «Story 2.6d i .docs/planning-artifacts/epics.md». Målet: `seed_testdata` skal legge inn svarene fra `seed.toml` gjennom den ekte tjenesten, og én ekte sending i nettleseren skal være kjørt og ført.

### Plan
- Planleggeragent skrev [specen](../../.docs/implementation-artifacts/spec-2-6d-test-data-with-answers-and-a-real-browser-send.md). Den fikk de utsatte punktene fra epic 1-retroen (innstillinger, feilstier, rollemerker) og fra 2.6c (gamle `Submission`-rader).
- Implementeringsagent, så commits i små steg: tjeneste, tester og kommando.
- Fire gjennomgangsagenter og MT-50 med Playwright i Edge. Deretter triage, rettinger og ny kjøring.

### Resultat
**Hva KI foreslo, og hva som ble godtatt, endret eller avvist**

Godtatt fra planleggeren (avgjort av Claude):
- Seeden erstatter fortsatt innstillingene hver gang, i stedet for retroens «bare over plassholderne». Grunnen: en frosset svarfrist ville etter hvert stengt skjemaet (epics 1.3). Det står nå i hjelpeteksten, utskriften, README og en AD-16-merknad.
- Svarene sendes med `send_answer` som systemaktør.
- Fixturen `seeded` beholder en ubesvart husstand for de rundt 20 eldre skjematestene. Den nye `seeded_with_answers` har hele seeden.
- Synnes tilbaketrukne samtykke venter til 7.2. Det er ført som utsatt punkt for 3.5.

Funnet av nettlesertesten og rettet: første kjøring av MT-50 talte 25 og 26 `Submission`-rader, ikke 7 og 6. Foreldreløse rader fra seeder før 2.6d lå igjen i utviklingsbasen. `reset_test_data` fjerner dem nå. Endringen har en egen test, og MT-50 ble kjørt på nytt med 6, 7 og 6 rader.

Andre rettinger etter gjennomgangen:
- `snapshot()` teller nå også `PersonAnswer` og `Allergy`.
- Notatet i `expected.toml` er flyttet.

Utsatt: 5.2 og 7.2 må utvide oppryddingen til `Submission`-typene de legger til.

Avvist: 23 funn, med begrunnelse i specens triagelogg. Blant dem:
- `KeyError` ved feilformet `seed.toml`. Fila er en utviklerfil, og transaksjonen rulles tilbake.
- Fixturen skriver forbi tjenestene. Det er testoppsett.
- Admin-tall mot `expected.toml`. Det hører til 3.5.

**Verifisert:**
- `uv run pytest`: 1268 bestått. Ruff og djlint er rene.
- MT-50 i Edge: «Totalt for husstanden: 3 000 kr», «Sendt av Mona», revision 1, 7 innsendinger, og 6 etter ny seed.

**Commits:** 9812ae1 (spec), 853fb80, 1d01c0d, 8bb612e, dbed2ea (rettinger), 60b698e, cf9fc62, c9a7c22. PR: https://github.com/IBE160-2026/G26-dvergsdal/pull/44

Punktet i issues.md om gamle `Submission`-rader er lukket.

### Åpne punkter
Ingen nye for Rikke. De utsatte punktene for 3.5, 5.2 og 7.2 står i deferred-work.md.
