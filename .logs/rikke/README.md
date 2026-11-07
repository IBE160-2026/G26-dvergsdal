# Sesjonslogg – Rikke

Denne mappen dokumenterer hvordan KI er brukt i prosjektet. Hver fil beskriver én arbeidsøkt med KI, delt i Oppgave, Plan, Resultat og Åpne punkter, med prompts sitert ordrett og lenker til commits.

Loggen føres med `sesjonslogg`-skillen fra faglærer ([.claude/skills/sesjonslogg/SKILL.md](../../.claude/skills/sesjonslogg/SKILL.md)). Filene har et nedtellende nummer, så den nyeste ligger øverst. Det som gjenstår, står i [issues.md](issues.md).

Loggen gjør KI-bruken sporbar for sensor (kriterium 1 i [sensorveiledningen](../../docs/sensorveiledning/sensorveiledning-del1.md)) og er grunnlaget for refleksjonsrapporten i del 2. Fullstendige transkripsjoner ligger lokalt hos Claude Code og er ikke lagt i repoet; øktenes ID står i hver logg. Ingen ekte gjestedata eller hemmeligheter, for repoet er offentlig.

## Eksempler på styring av KI

En samlet liste over tilfeller der jeg har presisert, avvist eller rettet KI. Detaljene står i hver logg.

- **Avviste `git init`** (2026-09-23): KI opprettet et git-repo på eget initiativ. Jeg ba den angre, fordi repoet skulle kobles til gruppens repo på GitHub. [Logg](999-2026-09-23-18-41-07-product-brief.md)
- **Fjernet KI-funksjonene** (2026-09-26): Briefen sa at emnet krevde en KI-funksjon. Jeg rettet det, og fjernet KI-assistenten fordi den koster penger å drifte. [Logg](998-2026-09-26-12-49-07-fjern-ki-funksjoner.md)
- **Krevde ny gjennomgang** (2026-10-23): KI mente briefen var ferdig. Jeg ba om en grundig gjennomgang, som fant motsigelser og hull. [Logg](996-2026-10-23-22-05-34-brief-etter-tilbakemelding.md)
- **Gikk imot faglæreren, og snudde selv** (2026-10-23): Jeg beholdt brevanimasjonen i kjernen, men flyttet den senere til «hvis tid» fordi tiden er en risiko. [Logg](996-2026-10-23-22-05-34-brief-etter-tilbakemelding.md)
- **Vurderte KI-ens anbefaling om brukertesten** (2026-10-23): Jeg ville droppe den, KI anbefalte å beholde en enklere variant, og jeg valgte det. [Logg](996-2026-10-23-22-05-34-brief-etter-tilbakemelding.md)
- **Pekte KI til riktig sted** (2026-11-06): KI lette etter faglærers loggopplegg i alle repoene i kursorganisasjonen. Jeg rettet den til mitt eget repo, der opplegget lå. [Logg](994-2026-11-06-18-09-28-sesjonslogg.md)
- **Utvidet researchen og valgte blant alternativene** (2026-11-06): Jeg ba KI bruke så mye innsats som trengs før PRD-en. Researchen viste at samtykkeregelen i briefen bryter med GDPR. Jeg godtok forslaget om å skille samtykke fra svaret, og valgte selv alternativ (a) for samtidige svar. [Logg](993-2026-11-06-19-10-08-research-for-prd.md)
- **Avviste betalingskode og presiserte svarskjemaet** (2026-11-06): KI foreslo en egen husstandskode i Vipps-meldingen. Jeg avviste den, fordi det kommer få betalinger. Jeg presiserte også spørsmålene om overnatting ut fra svaret fra Hardingasete, og la til «Vet ikke» for ankomsttid. [Logg](993-2026-11-06-19-10-08-research-for-prd.md)
- **Rettet en antagelse i researchen** (2026-11-07): Researchen antok én lenke per husstand, mens briefen sa én per gjest. KI fant motsigelsen, og jeg valgte én lenke per gjest. [Logg](992-2026-11-07-20-56-52-prd.md)
- **Endret roller og betaling** (2026-11-07): Jeg bestemte at hjelperne bare skal kunne se, ikke endre, og at en husstand skal kunne være «delvis betalt». KI foreslo å registrere beløp og regne ut statusen, og det godtok jeg. [Logg](992-2026-11-07-20-56-52-prd.md)
- **Avviste dataminimering** (2026-11-07): KI anbefalte å bare lagre gjestenes navn. Jeg avviste det, fordi telefon og e-post gjør oppfølgingen lettere for oss. Personvernsiden forklarer hva som lagres og hvorfor. [Logg](992-2026-11-07-20-56-52-prd.md)
- **Valgte blant forslagene fra fem KI-anmeldere** (2026-11-07): Jeg godtok blant annet prioritetsnivåer i v1 og en ny rekkefølge i skjemaet. Jeg avviste valget «svarer selv», at gjester ser vår bekreftelse av betalingen, og å lagre gamle priser per husstand. Oppfølgingen av husstander som ikke har begynt, endret jeg fra «noen dager» til «noen uker». [Logg](992-2026-11-07-20-56-52-prd.md)
