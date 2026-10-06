# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G26 – G26-dvergsdal |
| **Product brief** | `.docs/planning-artifacts/briefs/brief-aill-handle-it-2026-09-23/brief.md` (commit `ee25e52`) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

Briefen er skrevet på engelsk; tilbakemeldingen er på norsk. Jeg har også lest `addendum.md` i samme mappe.

## Samlet vurdering

- **Godt utgangspunkt med justeringer.** Gruppen kan gå videre og innarbeide punktene under.

**Det som er bra:**

1. Problemet er ekte og konkret: invitasjon som bilde på Messenger, svar i fritekst og et Excel-ark som mister allergier og sengeplasser. Det er lett å se for seg både gjestene og brudeparet, og løsningen svarer direkte på hvert punkt i problemlisten.
2. Kjerneflyten er tydelig og testbar: personlig lenke → brevanimasjon → RSVP for hele husstanden → pris og betalingsinformasjon, og på admin-siden tellinger for oppmøte, måltider, senger, allergier og betaling. Suksesskriteriene for emneleveransen beskriver nettopp dette.
3. Avgrensningen er klok: ingen nettbetaling, ingen utsending fra siden, ingen gjestekontoer, og KI-funksjonene i appen er bevisst fjernet med en begrunnelse (kostnad og ikke krav). Det gjør prosjektet mer gjennomførbart for én person.

**De viktigste endringene:**

1. Repoet er offentlig. Ekte gjesteliste, navn, allergier og betalingsinformasjon må aldri havne i repoet eller i testdata. Skriv inn i briefen at all utvikling og testing skjer med fiktive gjester, og at ekte data bare ligger i produksjonsdatabasen.
2. Skill mellom emneleveransen (desember 2026) og det ekte bryllupet (2027–2028). Suksesskriteriene for det ekte bryllupet (90 % svar uten purring, null allergifeil) kan ikke måles i emnet, og «production-ready» med drift til 2028 er ikke noe sensor vurderer. Gjør det tydelig hva som er v1 for emnet.
3. Planlegg hvordan sensor kan kjøre appen lokalt: med ferdige testgjester og husstander, en test-adminbruker og e-postvideresending som virker uten deres e-postkonto (f.eks. logging til konsoll i utviklingsmodus).

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Middels**

**Sammenlignbart med:** Mellom 6) To-do-liste med smarte etiketter (enkel) og 2) AI CV- og søknadsassistent (middels). Appen har ingen KI-funksjon, men to brukerroller (gjest via personlig lenke og admin med innlogging), husstander, prisberegning, svarfrist med låsing og helseopplysninger løfter den over et rent CRUD-prosjekt. Jeg plasserer den i nedre del av middels.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Middels | Pris per gjest ut fra valgte måltider og hyttenatt, tellinger per måltid, sengebehov, låsing ved svarfrist og overstyring etter frist. Reglene er enkle hver for seg, men mange, og tallene må stemme mot Hardingasete. |
| Datamodell – antall entiteter og relasjoner mellom dem | Middels | Gjest, husstand, RSVP-svar per gjest, måltid, pris, betaling, spørsmål, taleønske og admin-bruker. Husstand–gjest og flytting mellom husstander krever nøye modellering. |
| Brukere, roller og innlogging | Middels | Gjester logger inn med personlig lenke (token), admin med passord. Personlige lenker må være vanskelige å gjette. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Lav | Ingen KI i appen. Det er et bevisst og godt begrunnet valg. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Middels | E-postvideresending av gjestespørsmål er «must-have». Det krever en e-posttjeneste og nøkler. Vipps er bare betalingsinformasjon, ikke integrasjon. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav | Flere i samme husstand kan i prinsippet svare samtidig; avklar at siste lagring gjelder, eller vis hvem som har svart. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Lav | Ikke i v1. En utskrift- eller eksportvisning til Hardingasete kan være nyttig, men er ikke nødvendig. |
| Sikkerhet og personvern | Middels | Allergier er helseopplysninger. Samtykke via avkrysning er nevnt, men tilgang, sletting etter bryllupet og hvor dataene lagres bør beskrives. |

**Hva vanskelighetsgraden betyr for dere:**

- _Middels:_ Et godt balansert valg. Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer. For deg som jobber alene betyr det: få gjesteflyten og admin-tellingene helt riktige og godt testet før brevanimasjon, gaveliste, taleønsker og engelsk versjon får mye tid.

### Gjennomførbarhet med BMAD og Claude Code

Dere skal planlegge med BMAD (product brief → PRD → arkitektur → epics og stories) og implementere med Claude Code. Vurderingen under tar hensyn til at det må være tid til hele denne flyten, og til testing, retting og README til slutt.

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | Risiko | Én utvikler, ca. 12 uker, og ingen PRD ennå. «In»-listen har seks informasjonssider, full RSVP, admin med overstyring, e-post og taleønsker. Realistisk hvis animasjon og innholdssider holdes enkle og PRD kommer raskt. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | OK | Briefen og addendumet er detaljerte (RSVP-felter, adminoversikt, regler for svarfrist). Gavelisten og e-postkostnad er åpne, men små spørsmål. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | OK | En vanlig fullstack-webapp med database, skjemaer og innlogging passer godt. Brevanimasjonen kan gjøres med CSS. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | OK | Du kjenner domenet godt og kan regne ut riktig pris og antall for en testgjesteliste for hånd. Lag en fast testliste med fasit. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | OK | Pris, tellinger, låsing ved frist og husstandssvar er tydelige regler. Kriteriet om at admin viser riktige tall for en testgjesteliste er en god automatisk test. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | Risiko | Briefen fokuserer på hosting og drift for brudeparet, ikke lokal kjøring. Planlegg seed-data med fiktive gjester og testlenker, en test-admin, og en e-postløsning som virker uten nøkkel i utviklingsmodus. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | OK | Ingen språkmodell. E-posttjeneste og hosting er åpne kostnader, men de gjelder produksjon. Sørg for at emneversjonen ikke er avhengig av dem. |

**Konklusjon om gjennomførbarhet:**

- **Gjennomførbart med justert omfang.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. Del «In» i en kjerne for emnet (personlig lenke, husstands-RSVP med pris, låsing ved frist, admin-oversikt med tellinger og overstyring) og et andre trinn (brevanimasjon, taleønsker, gaveliste, lenkesporing). Da er det tydelig hva som må være ferdig i desember.
2. Gjør e-postvideresending valgfri i lokal kjøring: spørsmål lagres alltid i databasen og vises i admin, og e-post sendes bare når en nøkkel er satt.
3. Flytt «production-ready» og drift til 2028 ut av emnets suksesskriterier og inn i visjonen. Hosting er ikke nødvendig for emnet.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Tydelig: en bryllupsnettside som også er invitasjonen, med personlig lenke, husstands-RSVP og en adminoversikt som erstatter Excel. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | OK | Svært konkret, med fire tydelige feilmønstre (tapt informasjon, purring, forvirring, endringer som ikke når fram). |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | OK | Beskriver opplevelsen for både gjester og brudepar, uten teknologi. |
| What Makes This Different – er vurderingen ærlig og realistisk? | OK | Ærlig: fordelen er tilpasning (husstander, tredagers helg med tillegg, Vipps, norsk), ikke teknologi, og Joy, Zola og The Knot er nevnt. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | OK | Gjester i alle aldre, brudeparet og hjelpere, med konkrete suksessmål. Eldre gjester og gjester uten norsk er gode designhensyn. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Juster | Kriteriene for emneleveransen er gode og testbare. Kriteriene for det ekte bryllupet kan ikke måles i emnet; merk dem som langsiktige mål. «Under 10 minutter for en eldre slektning» er en god brukertest – planlegg når den skal gjøres. |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Juster | «In», «Stretch» og «Out» er tydelige, men «In» er stor for én person, og alt står som like viktig. Prioriter innenfor «In». |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | OK | Kort og nøktern (minneside etter bryllupet). |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Juster | Briefen og addendumet er detaljerte nok for PRD, og beslutningen om å fjerne KI fra appen er dokumentert i commit-historikken. Repoet har ellers lite aktivitet; kom i gang med PRD og prompt-logg nå. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | Juster | Nok innhold til å vise reell funksjonalitet. Prioriter kjernen, så resten kan kuttes uten at appen blir halv. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | OK | Pris, tellinger og låsing kan testes automatisk mot en fiktiv gjesteliste med fasit. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | OK | Fargepalett, brevanimasjon, mobilbruk og eldre gjester gir et tydelig designgrunnlag. Husk tilgjengelighet (kontrast, skriftstørrelse, tastaturnavigasjon). |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | Juster | Teknologistakk er ikke valgt ennå. Velg en enkel fullstack-løsning med én database, og begrunn valget i arkitekturen. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | Juster | Planlegg lokal kjøring med seed-data, testlenker og test-admin, og en e-postløsning som virker uten nøkkel. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Endre | Fordi repoet er offentlig, må briefen eller arkitekturen si eksplisitt at ekte gjestedata og allergier aldri committes, at nøkler ligger i `.env` utenfor Git, og at testdata er fiktive. |

## 3. Neste steg for gruppen

1. Legg til en kort seksjon om data og personvern: kun fiktive testdata i repoet, ekte data bare i produksjon, samtykke, hvem som har tilgang, og når data slettes etter bryllupet.
2. Prioriter innenfor «In» og skill emnets suksesskriterier fra bryllupets, og lag en fiktiv gjesteliste med forventede tall som kan brukes i tester og i README.
3. Gå videre til PRD og arkitektur, og ta med lokal kjøring og e-post i utviklingsmodus som eksplisitte krav.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
