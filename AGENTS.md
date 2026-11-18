# Instruksjoner for KI-agenter

Dette er et emneprosjekt i IBE160 Programmering med KI (høst 2026): en bryllupsnettside utviklet med KI og BMAD-metoden.

## Sensorveiledningen styrer arbeidet

Karakteren settes etter [docs/sensorveiledning/sensorveiledning-del1.md](docs/sensorveiledning/sensorveiledning-del1.md) (original: `sensorveiledning-del1.pdf` i samme mappe). Les den før du planlegger, skriver kode, gjennomgår kode eller rydder i repoet, og sjekk arbeidet ditt mot de sju kriteriene:

| Kriterium | Vekt |
|---|---|
| 1. Prosess og KI-styring | 30 % |
| 2. Funksjonalitet og omfang | 20 % |
| 3. Kvalitetssikring og testing | 15 % |
| 4. Design og brukeropplevelse | 10 % |
| 5. Kodekvalitet og arkitektur | 10 % |
| 6. README og kjørbarhet | 10 % |
| 7. Ryddighet i repoet | 5 % |

Sensor vurderer sporene av prosessen like mye som sluttproduktet. Det betyr i praksis:

- **Spor fra plan til kode.** Hver funksjon skal kunne spores tilbake til et krav eller en story i `.docs/planning-artifacts/` eller `.docs/implementation-artifacts/`. Når koden avviker fra planen, oppdater planleggingsdokumentet og skriv hvorfor.
- **Hold planleggingsdokumentene levende.** Product brief, PRD, arkitektur og stories skal oppdateres når beslutninger endres, ikke genereres én gang og glemmes.
- **Små commits underveis.** Én avgrenset endring per commit, med beskrivende melding. Aldri samle mye arbeid i én stor commit.
- **Dokumenter beslutninger.** Valg av teknologi, arkitektur og løsninger skrives ned med begrunnelse.
- **Gjør KI-bruken sporbar.** Prompts, KI-økter og tilfeller der gruppen har presisert, avvist eller rettet KI-forslag skal kunne kobles til konkrete endringer i repoet. Logg hver økt med `sesjonslogg`-skillen i [.logs/](.logs/) (se `CLAUDE.md`). Siter de viktigste promptene ordrett, og før under Resultat hva KI foreslo og om det ble godtatt, endret eller avvist. Nye eksempler på styring av KI legges også i lista i [.logs/rikke/README.md](.logs/rikke/README.md).
- **Test og kvalitetssikre.** Skriv automatiske tester for meningsfull logikk, dokumenter manuelle tester der automatiske ikke passer, og skriv ned feil som ble funnet i KI-generert kode og hvordan de ble rettet.
- **Design og tilgjengelighet.** Konsistent visuelt uttrykk, tydelige tilbakemeldinger og tomtilstander, god kontrast, tastaturnavigasjon, alternativtekst, skjemaetiketter og responsivt oppsett.
- **Ren kode.** Ingen død kode, duplisering eller utkommenterte rester fra forkastede KI-forsøk. Bruk linter og formatterer.
- **README er døra inn.** Hold `README.md` oppdatert med beskrivelse, forutsetninger med versjoner, eksakte kommandoer for installasjon, oppstart og tester, miljøvariabler (med `.env.example`), mappestruktur og lenker til planleggingsdokumentene.
- **Ryddig repo.** Ingen hemmeligheter, `.env`-filer, `node_modules`, byggeartefakter eller løse filer i rotmappen.

## Designskillen Impeccable

`.claude/skills/impeccable/` er [Impeccable](https://github.com/pbakaus/impeccable) v4.9.1 (Apache-2.0), kopiert uendret fra taggen `skill-v4.9.1`. Den brukes til å vurdere og pusse siden etter at en story har bygd den, for eksempel med `critique`, `audit`, `polish`, `harden`, `adapt` og `clarify`.

- **Designet står i planleggingsdokumentene.** Impeccable leter etter `PRODUCT.md` og `DESIGN.md` i rotmappen, men her ligger designet i [DESIGN.md](.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md) og [EXPERIENCE.md](.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md), og produktet i PRD-en. Les dem derfra. Ikke kjør `init` eller `document`, og ikke lag `PRODUCT.md` eller `DESIGN.md` i rotmappen: det ville gitt to versjoner av samme sannhet.
- **Briefen vinner.** Impeccable foreslår gjerne dristige valg. Farger, skrift, avstander og komponenter følger DESIGN.md. Et forslag som avviker, legges fram for Rikke, og blir det godtatt, oppdateres DESIGN.md først, med begrunnelse.
- **Endringer går gjennom en story.** Funn fra Impeccable rettes i en `bmad-build`-story eller føres i `deferred-work.md`, slik at hver endring kan spores til et krav.
- **Uten hook, live-modus og telemetri.** Hooken (som kjører ved hver redigering), `live` og `generate` er ikke satt opp. Telemetri er slått av i `.impeccable/config.json`.

Se også kapittel 5 i sensorveiledningen, *Typiske varseltegn*, og unngå alt som står der.
