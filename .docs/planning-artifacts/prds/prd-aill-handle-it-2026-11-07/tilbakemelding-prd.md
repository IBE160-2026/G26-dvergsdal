# Tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G26 – G26-dvergsdal |
| **PRD vurdert** | `.docs/planning-artifacts/prds/prd-aill-handle-it-2026-11-07/prd.md` (status final, sist endret 2026-11-08, commit 2c9b964) |
| **Dato** | 2026-11-12 |
| **Type** | Formativ tilbakemelding, ikke karakter |

## 1. Samlet inntrykk

Dette er en gjennomarbeidet PRD med egen tese («det må fungere»), konkrete brukerreiser og krav som bærer preg av at dere har tatt egne valg. Hovedrisikoen er størrelsen: ca. 78 FR og ca. 10 000 ord for et prosjekt med én utvikler og to uker til første leveranse (27. november). Det mangler også en prisregel som tester kan sjekke mot.

## 2. Dette fungerer godt

- **Testbarhet er tenkt inn fra start.** FR-69 krever en fasit regnet ut for hånd før koden skrives, FR-68 lister testhusstandene (full refusjon, delbetalt, «jeg har betalt» uten treff, trukket samtykke), og SM-2 setter kravet til 100 %. Dette svarer direkte på tilbakemeldingen på briefen.
- **Ærlig avgrensning og prioritering.** §3.1a deler v1 i tre nivåer med datoer og sier hva som kuttes først («Tier 3, cut first»). §3.4 gir begrunnelser, og §9 og addendumet viser avvik fra briefen og alternativer som ble forkastet.
- **Motmål og personvern med substans.** CM-1 til CM-4 hindrer at målene nås på feil måte («Consent is never pushed»). NFR-3 har en tabell over rettslig grunnlag per opplysningstype og en uttrykkelig akseptert risiko (C2).

## 3. Oversikt per dimensjon

| Dimensjon | Vurdering | Kort begrunnelse |
|---|---|---|
| Beslutningsklarhet | sterk | Valg, avveininger og forkastede alternativer står åpent (§9, addendum). Åpne punkter har eier og tidspunkt. |
| Substans | sterk | Ingen pynte-personas. NFR-ene har produktspesifikke terskler (18 px, 44 × 44 px, 320 px, 128 bit). |
| Strategisk sammenheng | sterk | Tesen «it must work» går igjen i NFR-1, produksjonsplanen og nivåinndelingen. |
| Testbarhet | god | Fasit og testdata er sterke, men prisregelen mangler, og enkelte krav har bare adjektiver. |
| Scope og avgrensning | god | Utelatelser er eksplisitte, men Tier 1 er for stort for to uker. |
| Brukbarhet for neste fase | god | IDer og brukerreiser med navngitte personer fungerer. Lengden, eksterne kildekoder og manglende glossar gjør uthenting tyngre. |
| Formtilpasning | god | Brukerreiser passer et produkt med gjester og admin. §3.2 og §9–10 gjør dokumentet tyngre enn nødvendig. |

## 4. Viktigste forbedringer

### 4.1 Tier 1 er for stort for to uker
- **Alvorlighet:** høy
- **Hvor:** §3.1a: «Tier 1, the usability-test build … Friday 27 November 2026»
- **Problem og hvorfor det betyr noe:** Tier 1 omfatter ca. 44 FR (FR-1–18, 21–28, 32–34, 41, 46–47, 54–55, 57–58, 68–75), pluss testdata, fasit og tester, med én utvikler som er ny i programmering og 15 dager igjen. Mister dere denne fristen, får brukertesten (SM-3) ingenting å teste. Da sliter også resten av planen.
- **Forslag:** Definer Tier 1 som en tynn gjennomgående bit, for eksempel: «Sigmund åpner lenken, svarer for to personer, ser totalen og sender. Rikke ser tallet i oppsummeringen.» Flytt allergi og samtykke (FR-25–28), ankomst (FR-18), turen (FR-17) og FR-70 til Tier 2. FR-26 lover dessuten uttak av samtykke (FR-30) og en personvernside (FR-66), som begge ligger i Tier 2. Sikte på 20–25 FR og skriv én «Done when»-setning for nivået.

### 4.2 Prisregelen mangler, og dermed fasiten
- **Alvorlighet:** høy
- **Hvor:** §5.5 FR-32/FR-33: «always calculated from the answers and the current prices»
- **Problem og hvorfor det betyr noe:** PRD-en sier ikke om hytteprisen gjelder per person, per hytte eller per husstand. Uten regelen kan ikke fasiten (FR-69) skrives, og to utviklere (eller to KI-økter) kan bygge ulike totaler.
- **Forslag:** Legg til et FR (eller utvid FR-33) med formel og regneeksempel med fiktive priser: «Totalen er summen over personer som kommer: hyttepris (X kr per person som overnatter, for hele helgen) + valgte betalte måltider. Eksempel (hytte 1 200 kr, frokost 180 kr): Filippa kommer lørdag–søndag, overnatter og spiser søndagsfrokost → 1 200 + 180 = 1 380 kr.» Dere må selv bestemme enheten. Mangler prisene (Q3), bruker dere fiktive tall.

### 4.3 Flere krav har adjektiver i stedet for grenser
- **Alvorlighet:** medium
- **Hvor:** NFR-4 «slowed down», «a period of inactivity»; FR-48 «work well on a phone»; FR-13 «one clear task per step»; NFR-6 «one obvious next step»; SM-1 «Every step works»; SM-3 (ingen antall testpersoner)
- **Problem og hvorfor det betyr noe:** Disse kan ikke bli testtilfeller uten at noen tolker dem. Det er her KI-generert kode oftest «ser riktig ut» uten å være det.
- **Forslag:** «Etter 10 ugyldige lenkeforsøk fra samme IP-adresse på 10 minutter svarer siden ikke på 15 minutter. Admin-økten utløper etter 30 minutter uten aktivitet. Å finne en gjest, kopiere lenken og se om gjesten har svart tar høyst tre trykk fra admin-forsiden på 360 px bredde.» For SM-3: skriv hvor mange testpersoner (f.eks. minst tre over 60 år) og hva som regnes som «feil svar». Tallene er forslag, men bestem dere.

### 4.4 Dokumentet er langt, og kildekodene peker utenfor det
- **Alvorlighet:** medium
- **Hvor:** Leseveiledningen i toppen (`[C4, R 4.1, review]`), §3.2, §9, §10 og addendumets FR-60-tabell
- **Problem og hvorfor det betyr noe:** Taggene peker til filer som ikke ligger i PRD-en, og «review» sier lite om hva som ble endret. §3.2 er mer driftsplan enn krav, og FR-60 og addendumet gjentar samme tabell («Where the two differ, the PRD applies»). Det gjør det tungt å hente ut stories og lett å la to versjoner glippe fra hverandre.
- **Forslag:** Behold én kilde for hver regel (FR-60). Flytt §3.2 til et eget dokument, «Produksjonsplan 2027», med bare en kort lenke og ready-date igjen i PRD-en. Bytt ut «review»-tagger med en setning i §10 der det trengs. Legg til et glossar på 10–12 ord (gjest, person, husstand, respondent, «Needs attention», «Changed»).

### 4.5 Antakelser og åpne punkter er ikke merket som antakelser
- **Alvorlighet:** medium
- **Hvor:** §7 «Assumptions» (ett punkt); §8, alle rader med «Blocks the PRD? No»; Q8
- **Problem og hvorfor det betyr noe:** Status er `final`, men viktige antakelser står som fakta, for eksempel at eldre gjester klarer skjemaet på under 10 minutter og at lenker åpnes i Messenger. Q4 sier at svaret «may change FR-34», men har ikke noe fallback. Q8 spør om faglærer godtar samtykkemodellen; det kan gruppen avgjøre selv.
- **Forslag:** Merk antakelser med `[ASSUMPTION: …]` og en indeks. Skriv for Q4: «Hvis Hardingasete tillater direkte betaling, utgår FR-34 «Pay now» og erstattes av …». Fjern eller omformuler Q8.

## 5. Mekaniske funn

- **IDer:** FR-1–78, SM-1–13, CM-1–4 og UJ-1–6 er alle til stede og unike. Rekkefølgen avviker (SM-11–13, FR-70–78), men det er forklart i leseveiledningen. Alle brukerreiser har navngitt hovedperson.
- **Glossar:** finnes ikke. «Guest / person / respondent» brukes konsekvent, men er ikke definert.
- **Krysshenvisning:** §10 (runde 3) sier «helpers see contact details (FR-66)», men FR-66 er personvernsiden. Kontaktopplysninger står i FR-49/FR-57.
- **Kodene C/D/Q/R** (f.eks. «C4», «R 4.1») løser seg bare i `pre-prd-discovery.md` og `research.md`, ikke i PRD-en.
- **Ubesvarte `[ASSUMPTION]`:** ingen merkede; se 4.5.

## 6. Før dere går videre

**Må avklares før UX, arkitektur og epics:**
- Prisregelen og hva som er innenfor Tier 1 (4.1, 4.2).
- D14/D15 (hashet lenkekode og teknologivalg). D14 er i konflikt med FR-51 («copy the guest's link») hvis kodene hashes.

**Kan vente:** Q2–Q4 og Q7 (innstillinger og tekst, ikke struktur), D12, D16 og alt merket [2027].

**Oppfølging av briefen: ja.** Fiktive testdata (NFR-3), skille mellom kursversjon og ekte bryllup (§1, §2), lokal kjøring og e-post uten nøkkel (NFR-8, FR-45), nivåinndeling (§3.1a) og fasit (FR-69) er alle fulgt opp.

## 7. Refleksjonsspørsmål

1. Addendumet viser forslag fra KI-gjennomgangene som dere avviste, for eksempel å lagre bare navn og skjule spørsmål for hjelperne. Hvordan avgjorde dere hva som skulle inn og ut, og hva sjekket dere selv i stedet for å stole på KI-vurderingen?
2. FR-14 ble omstrukturert fordi en gjennomgang mente «hele helgen? Nei» kunne virke som å takke nei. Hva gjør dere hvis brukertesten (SM-3) viser at den nye rekkefølgen også er forvirrende?

_Vurdert mot kvalitetsrubrikken i bmad-prd. Dette er veiledning, ikke sensur._
