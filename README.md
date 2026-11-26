# G26 — AI'll handle it

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

**AI'll handle it** er bryllupsnettsiden til Rikke og Valdemar. Hver gjest får en personlig lenke som er den eneste innloggingen: der ser gjesten invitasjonen, programmet og praktisk informasjon, og svarer for husstanden sin. Brudeparet og hjelperne får en oversikt over svar, allergier og betalinger. Nettsiden er laget for gjester i alle aldre på mobil, og den er utviklet med KI og BMAD-metoden.

Repoet inneholder applikasjonen og dokumentasjonen av utvikling, testing og kvalitetssikring med KI.

> **Status:** Epic 1 til 3 er bygd. Gjester åpner den personlige lenken og ser invitasjonen, programmet og praktisk informasjon, og svarer for husstanden sin i svarskjemaet med kvittering og betalingsinformasjon (se [Svarskjemaet](#svarskjemaet)). Brudeparet og hjelperne logger inn under `/admin/logg-inn/` og ser Oversikt over svar, overnatting, måltider, allergier og fjelltur, tellesidene bak hvert tall, Gjester med en rad per husstand og allergilisten (se [Admin](#admin)). Testene sjekker at hvert tall stemmer med fasitlisten som er regnet ut for hånd (story 3.5, se [Fasit-testene](#fasit-testene)). Betalinger, endring av svar og innstillinger kommer i epic 4 til 8.

## Forutsetninger

| Verktøy | Versjon | Merknad |
|---|---|---|
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | 0.13 (0.12 virker også) | Installerer riktig Python og alle avhengigheter |
| Python | 3.14 | Trenger ikke installeres selv: uv henter versjonen i `.python-version` |
| Git | hvilken som helst nyere | For å klone repoet |

Appen bruker SQLite, som følger med Python. Den trenger ingen database-server, ingen kontoer og ingen nøkler, og kjører på Windows, macOS og Linux.

## Installere og starte

```bash
git clone https://github.com/IBE160-2026/G26-dvergsdal.git
cd G26-dvergsdal
uv sync
uv run manage.py migrate
uv run manage.py runserver
```

Åpne <http://127.0.0.1:8000/> i nettleseren. Den viser siden for ugyldige lenker, «Dette er en privat invitasjon», fordi invitasjonen bare åpnes med en personlig lenke; fyll inn testdata (se [Testdata](#testdata)) og åpne en testlenke for å se den. Stilprøven ligger på <http://127.0.0.1:8000/stil/>. Stopp serveren med `Ctrl+C`.

`uv sync` installerer Python 3.14 og de låste versjonene i `uv.lock`. `migrate` lager den lokale databasen `db.sqlite3`, som git ignorerer.

## Testdata

Én kommando fyller databasen med fiktive husstander, gjester, innstillinger og to testbrukere fra [wedding/fixtures/seed.toml](wedding/fixtures/seed.toml). Kjør den etter `migrate`:

```bash
uv run manage.py seed_testdata
```

Kommandoen skriver ut en testlenke per gjest og innloggingene under. Den kan kjøres så ofte du vil: den sletter først testhusstandene fra forrige kjøring med alt som er i dem (også en gjest som er lagt til i en testhusstand senere) og testbrukerne, men aldri husstander eller brukere den ikke har laget selv, og den fjerner innsendingene (`Submission`) som hørte til testhusstandenes svar. Innstillingene (priser, kontaktpersoner, kontonummer og svarfrist) erstattes med testverdiene fra `seed.toml` hver gang, og kommandoen skriver det ut, fordi svarfristen må være 30 dager fra dagen den kjøres. Er en lenkekode eller et brukernavn fra `seed.toml` allerede i bruk av husstander eller brukere den ikke har laget, stopper den uten å endre noe. Den kjører bare når `APP_ENV` ikke er satt eller er `local`, så testdata aldri havner på den ekte nettsiden.

Alle personene er oppdiktet, bortsett fra Rikke og Valdemar: e-postene er på `example.com`, telefonnumrene begynner med `+47 000`, og kontonummeret har feil kontrollsiffer. Svarfristen settes til 30 dager etter dagen kommandoen kjøres, så svarskjemaet er åpent.

| Gjest | Husstand | Testlenke |
|---|---|---|
| Sigmund | Sigmund og bestemor | <http://127.0.0.1:8000/test-sigmund0000000000/> |
| bestemor | Sigmund og bestemor | <http://127.0.0.1:8000/test-bestemor000000000/> |
| Arild | Arild, Marie, Filippa og Leone | <http://127.0.0.1:8000/test-arild000000000000/> |
| Marie | Arild, Marie, Filippa og Leone | <http://127.0.0.1:8000/test-marie000000000000/> |
| Filippa | Arild, Marie, Filippa og Leone | <http://127.0.0.1:8000/test-filippa0000000000/> |
| Leone | Arild, Marie, Filippa og Leone | <http://127.0.0.1:8000/test-leone000000000000/> |
| Synne | Synne | <http://127.0.0.1:8000/test-synne000000000000/> |
| Tor | Tor og Hilde | <http://127.0.0.1:8000/test-tor00000000000000/> |
| Hilde | Tor og Hilde | <http://127.0.0.1:8000/test-hilde000000000000/> |
| Eva | Eva | <http://127.0.0.1:8000/test-eva00000000000000/> |
| Jonas | Jonas og Ida | <http://127.0.0.1:8000/test-jonas000000000000/> |
| Ida | Jonas og Ida | <http://127.0.0.1:8000/test-ida00000000000000/> |
| Mona | Mona og Geir | <http://127.0.0.1:8000/test-mona0000000000000/> |
| Geir | Mona og Geir | <http://127.0.0.1:8000/test-geir0000000000000/> |

Åpne lenkene mens `uv run manage.py runserver` kjører. Hver lenke åpner invitasjonen til husstanden sin, for eksempel «for Sigmund og bestemor»; menyen øverst går til de tre infosidene. `/` og en ukjent lenke viser siden for ugyldige lenker. Andre gale adresser viser også siden for ugyldige lenker, eller, når adressen begynner med en gyldig lenke, en feilside med brudeparets telefonnumre (se [Feilsider](#feilsider)).

Terminalen der serveren kjører, viser `/[code]/` i stedet for lenkekoden, for eksempel `"GET /[code]/ HTTP/1.1" 200` for en testlenke og `"GET /[code]/ HTTP/1.1" 404` og `Not Found: /[code]/` for en ukjent lenke. En lenkekode er gjestens eneste innlogging, så den skal ikke havne i en logg (story 1.4c).

| Brukernavn | Passord | Rolle |
|---|---|---|
| `testpar` | `bryllup-test-2028` | Brudeparet |
| `testhjelper` | `bryllup-test-2028` | Hjelper |

Logg inn med dem på <http://127.0.0.1:8000/admin/logg-inn/> (se [Admin](#admin)).

`seed.toml` inneholder også de planlagte svarene, allergiene, samtykkene og betalingene. Svarene, allergiene og samtykkene sendes gjennom sendetjenesten som om gjesten svarte selv (story 2.6d). Betalingene og Synnes tilbaketrukne samtykke lastes inn i senere stories (5.2 og 7.2). Fasiten for disse dataene, regnet ut for hånd før koden som regner dem ut, ligger i [wedding/fixtures/expected.toml](wedding/fixtures/expected.toml); commit-meldingen til fila forklarer hvordan tallene ble kontrollert.

## Admin

Brudeparet og hjelperne logger inn på <http://127.0.0.1:8000/admin/logg-inn/> med brukernavn og passord. Etter innloggingen kommer de til Oversikt på `/admin/`, med menyen Oversikt · Gjester · Betalinger · Innstillinger · Logg ut. Foreløpig er bare Oversikt en side, og den viser bare hvem som er logget inn; Gjester, Betalinger og Innstillinger står som ren tekst til sidene deres er bygd. Uten innlogging sender alle adresser under `/admin/` deg til innloggingssiden. Økten varer i 20 timer etter siste bruk og slutter å gjelde da; innloggingssiden sier da «Du ble logget ut fordi du var borte en stund.» Kjør `seed_testdata` først og logg inn med `testpar` eller `testhjelper` (se [Testdata](#testdata)).

Det finnes ingen selvregistrering, ingen «glemt passord» og ikke Djangos egen admin-side, og `createsuperuser` brukes ikke. Ekte kontoer lages bare på maskinen der appen kjører, med:

```bash
uv run manage.py create_admin <brukernavn> --role couple
uv run manage.py create_admin <brukernavn> --role helper
```

`couple` er brudeparet (full tilgang) og `helper` en hjelper (ser alt, endrer ingenting). Kommandoen spør om passordet to ganger og sjekker at det er godt nok; passordet kan ikke gis som argument. Et brukernavn som finnes fra før, eller en annen rolle, blir avvist med en melding og ingenting lagres. Ekte kontoer er ikke testdata, så `seed_testdata` lar dem stå.

## Svarskjemaet

Fyll inn testdata og start serveren (se [Testdata](#testdata)), åpne en testlenke, for eksempel <http://127.0.0.1:8000/test-sigmund0000000000/>, og trykk «Svar på invitasjonen» nederst i svarfeltet. Skjemaet åpnes på `/<kode>/svar/` med steg 1, «Hvem kommer?», der hver person i husstanden får «Kommer» eller «Kommer ikke». «Bytt» (i husstander med flere enn én person) endrer hvem som svarer.

Steg 1 til 6 og «Se over svaret» er bygd. Steg 2, «Er alle som kommer, med hele helgen?», viser de tre dagene med dato og hva som skjer. «Ja» går videre; «Nei» viser på samme side en gruppe med dagene for hver person som kommer. Dagene må komme etter hverandre, så fredag og søndag uten lørdag gir en feilmelding. Steg 3, «Hvem skal overnatte på Hardingasete?», viser prisen for hytte hele helgen per person og gir «Ja» eller «Nei» for hver som kommer; den som bare er med én dag, kan ikke velge «Ja» og får forklaringen. Steg 4, «Hvilke måltider skal vi bestille?», viser bare måltidene hver person kan få ut fra dagene sine, med pris. Begge stegene viser «Totalt for husstanden» under valgene. Summen regnes alltid ut på serveren; med JavaScript oppdateres den også mens gjesten velger, ved at skjemaet sendes til `POST /<kode>/svar/sum/?steg=<steg>`, som bare svarer med summen og ikke lagrer noe. Endres dagene eller hvem som kommer, fjernes valg som ikke lenger gjelder, og stegene etter steg 2 må gås gjennom igjen. Steg 5, «Allergier og matbehov», er valgfritt: for hver person som kommer, «Ingen allergier eller matbehov» eller faste kategorier og en kort merknad (høyst 200 tegn), og «Ja»/«Nei» til at opplysningene lagres, uten at noe er valgt på forhånd. Den som svarer for andre, må bekrefte at de vet om det og er enige. Uten «Ja» kan gjesten gå videre, men skjemaet sier at opplysningene ikke blir lagret. Allergiene lagres når svaret sendes, og bare med «Ja» (story 2.6b): «Nei» sletter lagrede opplysninger, et nytt svar uten samtykkesvar lar dem stå, og den som ikke lenger kommer, får dem slettet. Hvert «Ja» og «Nei» lagres som en samtykkehendelse med hvem som svarte, når og versjonen av samtykketeksten. Med JavaScript fjerner «Ingen …» krysset i kategoriene og omvendt; uten JavaScript gir begge kryss en feilmelding. Steg 6, «Hvem blir med på fjellturen fredag?», gir «Ja», «Nei» eller «Kanskje» for hver som er med fredag; er ingen med fredag, hoppes steget over. «Se over svaret» (`/<kode>/svar/se-over/`) sier først at svaret ikke er sendt ennå, og viser så én del per steg med svaret for hver person, «Ikke oppgitt» for det som er hoppet over, en advarsel når allergier ikke blir lagret uten samtykke, og «Totalt for husstanden». «Endre» åpner steget med `?fra=se-over`, og «Fortsett» eller «Tilbake» fører da tilbake til «Se over svaret»; har endringen lagt til en person eller en dag, kommer stegene med nye spørsmål først. «Send svaret» lagrer svaret (story 2.6a): knappen viser «Sender …» mens svaret sendes, informasjonskapselen med utkastet slettes, og gjesten kommer til «Svaret er sendt» (`/<kode>/svar/sendt/`) med «Sendt av <navn> <dag og dato> kl. <tid>.» og deretter kvitteringen (story 2.7): brudeparets takk («Tusen takk …» når noen kommer, «Så leit …» når ingen kommer), «Dette har dere svart» med de samme linjene som på «Se over svaret» uten «Endre», «Totalt for husstanden» og lenken «Til invitasjonen». Skal husstanden betale noe, kommer «Betal nå» og «Betal senere» over «Du kan nå trygt lukke invitasjonen.». «Betal nå» åpner «Slik betaler du» (`/<kode>/svar/betal/`) med beløpet, Vipps-nummeret og kontonummeret fra innstillingene og betalingsmeldingen «Bryllup <navnene>» som tekst som kan markeres; med JavaScript i en sikker sammenheng (https eller localhost) får hver rad en «Kopier»-knapp. «Betal senere» viser at den samme lenken alltid viser hva som er igjen å betale. Sendingen er trygg ved feil og gjentak (story 2.6c): skjemaet på «Se over svaret» har en engangs innsendings-ID og summen siden viste som skjulte felt. Trykkes «Send svaret» to ganger, eller sendes samme side på nytt, lagres svaret én gang og gjesten kommer til «Svaret er sendt». Har noen andre i husstanden sendt et svar etter at gjesten begynte, lagres ingenting, og «Se over svaret» sier hvem som sendte og når; samtykket til allergier må da gis på nytt. Har summen endret seg (ny pris eller en endring i en annen fane), eller teksten om samtykke, lagres ingenting, og siden sier hva som skjedde. Feiler lagringen eller forbindelsen, står alt igjen, knappen blir «Send svaret» igjen, og meldingen sier «Prøv igjen» og gir brudeparets telefonnumre. Har svarfristen gått ut når svaret sendes, lagres ingenting, og gjesten ser «Svarfristen har gått ut». Et senere steg sender gjesten tilbake til det første steget som ikke er besvart. Kommer ingen, går «Fortsett» rett til «Se over svaret». Ingenting lagres i databasen før svaret sendes: til da ligger svaret i informasjonskapselen `rsvp_draft` i nettleseren. En øktkapsel, `rsvp_visit` (verdien «1», ingen svar), settes ved hvert innsendte steg og forsvinner når nettleseren lukkes; uten den, og med et utkast, viser hver adresse under `/<kode>/svar/` først «Vil du fortsette der du slapp?» (story 2.9). Etter fristen sletter forsiden og «Svarfristen har gått ut» utkastet. Svarfristen er 30 dager etter at `seed_testdata` ble kjørt; etter fristen viser alle adressene under `/<kode>/svar/` «Svarfristen har gått ut». Har husstanden svart (story 2.8), viser forsiden statusfeltet «Svaret er sendt» der svarfeltet sto, med «Sendt av …», «Totalt for husstanden» og, når noe skal betales, «Slik betaler du»; «Svar» i menyen og «Se svaret» i toppfeltet fører dit, og åpner husstanden `/<kode>/svar/` eller et annet steg, kommer den til statusfeltet (`/<kode>/#status`), også etter fristen. Det gjelder ikke siden et avvist svar kommer tilbake til (`?sending=…`).

## Tester og sjekker

Alle testene kjøres med én kommando:

```bash
uv run pytest
```

Kodesjekkene (de samme som GitHub Actions kjører på hver push og pull request, se [.github/workflows/checks.yml](.github/workflows/checks.yml)):

```bash
uv run ruff check
uv run ruff format --check
uv run djlint --check .
```

Feiler en sjekk, retter disse kommandoene det meste automatisk:

```bash
uv run ruff check --fix
uv run ruff format
uv run djlint --reformat .
```

Ruff sjekker og formaterer Python-koden, djLint sjekker Django-malene.

### Fasit-testene

Tallene brudeparet ser, skal stemme med en liste som er regnet ut for hånd: [wedding/fixtures/expected.toml](wedding/fixtures/expected.toml). Listen er talt opp fra testdataene i `seed.toml` og reglene i kravene, ikke regnet ut av appen: Claude talte, en annen agent talte på nytt uten å se tallene, og Rikke kontrollerte et utvalg for hånd. [tests/test_expected_results.py](tests/test_expected_results.py) er beviset på at appen og listen er enige:

- Hver telling på Oversikt (husstander og personer som kommer, dager, overnatting, måltider, allergier og fjelltur) er sammenlignet med listen, på reglene, på tellingsregisteret og på de ferdige sidene (Oversikt, tellesidene, Gjester og allergilisten). Betaling-panelet er ikke med, det kommer i story 5.3.
- Hver husstands totalsum og hver gjests status og allergitilstand er sammenlignet med listen.
- Vakttester sørger for at listen selv henger sammen med `seed.toml` og med seg selv, og at en ny del av listen ikke blir stående uten en test.

Kjør dem med:

```bash
uv run pytest tests/test_expected_results.py
```

En endring i listen er alltid en egen commit med begrunnelsen i meldingen, aldri en endring for å få en test til å gå grønn: viser en test en forskjell, er appen feil, med mindre tellingen for hånd viser noe annet. Testdataene lagrer Synnes nøtteallergi til story 7.2 laster inn at hun trakk samtykket; testene legger inn tilbaketrekkingen selv, så alle tall stemmer uten avvik, og én egen test viser hva testdataene alene gir.

Sjekker som ikke kan automatiseres, for eksempel hvordan sidene ser ut på en smal mobilskjerm, står i [docs/manual-test-plan.md](docs/manual-test-plan.md).

## Feilsider

Feilsidene vises bare når `DEBUG` er av; med `DEBUG` på (standard lokalt) viser Django sine egne feilsøkingssider. Med `DEBUG=false` serveres stilarket og bildene fra `staticfiles/`, så kjør `collectstatic` først. I PowerShell:

```powershell
uv run manage.py seed_testdata
uv run manage.py collectstatic --noinput
$env:DEBUG='false'; $env:ALLOWED_HOSTS='localhost'; uv run manage.py runserver
```

I bash, zsh eller Git Bash er siste linje `DEBUG=false ALLOWED_HOSTS=localhost uv run manage.py runserver`. Med `ALLOWED_HOSTS=localhost` svarer serveren bare på `localhost`, ikke på `127.0.0.1`. I PowerShell gjelder variablene til de fjernes; for å kjøre serveren vanlig igjen etterpå, kjør `Remove-Item Env:DEBUG, Env:ALLOWED_HOSTS`. Åpne så:

- <http://localhost:8000/hei/x/>: siden for ugyldige lenker, «Dette er en privat invitasjon», med status 404.
- <http://localhost:8000/test-sigmund0000000000/finnes-ikke/>: «Vi finner ikke denne siden», med knappen «Tilbake til invitasjonen» og brudeparets telefonnumre nederst.

`staticfiles/` holdes ute av git. Feilsidene for 500 (noe gikk galt hos oss), 400 (for eksempel en adresse serveren ikke svarer på) og et skjema som ble avvist av CSRF-sjekken dekkes av de automatiske testene i [tests/test_error_pages.py](tests/test_error_pages.py), og alle feilsidene sjekkes i en nettleser i MT-22 i [docs/manual-test-plan.md](docs/manual-test-plan.md).

## Stilprøve

<http://127.0.0.1:8000/stil/> viser invitasjonens farger, de to skriftene, de fire knappene, papirarket og de fire varslene, slik de er beskrevet i [DESIGN.md](.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md). Siden er laget for å se designet og gjøre de manuelle testene MT-2 til MT-4 (høykontrast, redusert bevegelse og fonter) i [docs/manual-test-plan.md](docs/manual-test-plan.md). Den inneholder ingen personopplysninger, leser ingenting fra databasen og finnes bare når `APP_ENV` er `local`; med `APP_ENV=production` gir `/stil/` siden for ugyldige lenker med status 404.

## Innstillinger

Appen trenger ingen innstillinger for å kjøre lokalt: alt har trygge standardverdier, og det trengs ingen `.env`-fil. Innstillingene leses fra miljøvariabler, og alle står med eksempelverdier i [.env.example](.env.example).

| Variabel | Standard lokalt | Standard i produksjon | Forklaring |
|---|---|---|---|
| `APP_ENV` | `local` | (settes til `production`) | `local` eller `production`, skrevet nøyaktig slik. Alt annet (for eksempel `prod`) gjør at appen nekter å starte. |
| `DEBUG` | `true` | `false` | Djangos feilsøkingssider. |
| `SECRET_KEY` | en fast nøkkel bare for lokal bruk | ingen brukbar: den lokale nøkkelen godtas ikke | Signeringsnøkkel. Produksjon må ha sin egen lange, tilfeldige nøkkel. |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` | tom: må settes | Kommaseparerte domenenavn nettsiden svarer på. |

Med `APP_ENV=production` nekter appen å starte hvis `DEBUG` er på, `SECRET_KEY` mangler eller er den lokale nøkkelen, eller `ALLOWED_HOSTS` er tom. Meldingen sier hva som må rettes.

Slik bruker du en egen innstillingsfil (valgfritt):

```bash
cp .env.example .env
uv run --env-file .env manage.py runserver
```

`.env` holdes ute av git og skal aldri committes.

## Mappestruktur

```text
.
├── config/                   Django-innstillinger, rot-URL-er, WSGI/ASGI, mellomvare og loggfilter
│   ├── env.py                Leser miljøvariabler og vakten for produksjon
│   ├── middleware.py         Mellomvare: X-Robots-Tag: noindex på hvert svar
│   ├── error_handlers.py     Feilsidene for hele nettstedet: brudeparets egne under /admin/, gjestenes ellers
│   └── logging_filters.py    Loggfilter som bytter lenkekoder ut med [code]
├── wedding/                  Dataeieren: modeller (også brukermodellen) og forretningslogikk
│   ├── rules/                Rene regelfunksjoner uten Django (summer, tellinger, frist; summary.py gir id-listene bak tallene i Oversikt)
│   ├── services/             Den eneste koden som skriver til databasen (answers.py: send_answer, som lagrer svaret; consent.py: samtykketekstens versjon; exceptions.py: avvisningene, blant annet endret svar, endret sum og endret samtykketekst)
│   ├── rsvp/                 Svarskjemaet, brukt av både gjester og brudeparet: stegene, skjemaene, utkastet i informasjonskapselen, visningene og oppsummeringen på «Se over svaret» (summary.py)
│   │   └── templates/rsvp/   Malene for et steg, «Se over svaret», kvitteringen «Svaret er sendt» (sent.html), «Slik betaler du» (pay.html) og delene (hvem som svarer, feiloppsummeringen, includes/pay-row.html med én betalingsrad)
│   ├── templatetags/         Malfilteret `kroner`, som skriver alle beløp likt (1 450 kr)
│   ├── selectors.py          Lesespørringer for visningene
│   ├── actors.py             Hvem som handler: gjest, admin, system eller operatøren som kjører create_admin
│   ├── links.py              Gjør en personlig lenkekode om til en gjest
│   ├── management/commands/  Kommandoer: seed_testdata fyller inn testdata, create_admin lager en ekte konto
│   ├── fixtures/             Testdata (seed.toml) og fasit (expected.toml)
│   ├── templates/wedding/    Grunnmalen (base.html), felles deler som varselet, lenkeforhåndsvisningen og bunnfeltet, og robots.txt
│   └── migrations/           Databasemigrasjoner
├── guests/                   Gjestesidene: forsiden og infosidene under /<kode>/, siden for ugyldige lenker og stilprøven /stil/
│   └── templates/guests/errors/  Feilsidene for 404, 500, 400 og CSRF, med rammen error_page.html ved siden av (story 1.8); siden for utløpt svarfrist, rsvp_closed.html, ligger ved siden av errors/ (story 2.1)
├── dashboard/                Sidene for brudeparet og hjelperne under /admin/: innlogging, utlogging, adminrammen med menyen, Oversikt og brudeparets egne feilsider (story 3.1); selectors.py laster gjestenes fakta og overview.py gjør reglene om til tallene i Oversikt (story 3.2); counts.py er registeret som navngir hvert tall én gang, og count.html er tellesiden bak hvert tall (story 3.3); guest_list.py bygger radene på Gjester og allergilisten, og guests.html og allergies.html er de to sidene (story 3.4)
├── static/                   CSS, JavaScript, fonter og bilder, alt fra egen server
│   ├── css/site.css          Stilarket: alle fargene, avstandene og skriftstørrelsene fra DESIGN.md
│   ├── css/style-sample.css  Oppsettet for stilprøven /stil/, lastes bare der
│   ├── js/rsvp-total.js      Oppdaterer totalsummen på svarskjemaets steg 3 og 4 mens gjesten velger
│   ├── js/rsvp-allergies.js  Gjør «Ingen allergier eller matbehov» eksklusivt på steg 5
│   ├── js/rsvp-send.js       Viser «Sender …» på «Send svaret» og stopper et dobbelttrykk
│   ├── js/rsvp-copy.js       «Kopier»-knappene på «Slik betaler du» (story 2.7)
│   ├── fonts/                Imperial Script og EB Garamond som WOFF2, med lisens og README
│   └── img/                  Rikkes bilder (segl, blomster, blonderamme, illustrasjon, foto, ikoner), med README
├── tests/                    pytest-testene (test_admin_login, test_admin_errors, test_admin_routing, test_create_admin og test_architecture_imports hører til story 3.1; test_summary_rules, test_overview og test_admin_overview til story 3.2; test_counts og test_admin_count_page til story 3.3; test_guest_list, test_admin_guests_page og test_admin_allergy_page til story 3.4; test_expected_results, fasit-testene mot `expected.toml`, til story 3.5)
├── tools/                    Hjelpeskript for utviklere: prepare_images.py lager bildene i static/img/
├── docs/                     Referansestoff: sensorveiledningen og manuell testplan
├── .docs/                    Det som lages underveis: planlegging og implementering (BMAD)
├── .logs/rikke/              Logg over KI-økter og issues.md med åpne punkter
├── .github/workflows/        GitHub Actions: tester og kodesjekker
├── _bmad/                    BMad-oppsett og skript
├── .claude/skills/           BMad-skills, sesjonslogg-skillen og designskillen Impeccable som KI-agenten bruker
├── .impeccable/config.json   Innstilling for Impeccable: telemetri av
├── manage.py                 Djangos kommandolinjeverktøy
├── pyproject.toml, uv.lock   Avhengigheter og verktøyoppsett, låst med uv
├── .python-version           Python 3.14
├── .env.example              Alle innstillingene med eksempelverdier
├── .gitattributes            Linjeskift for Impeccable-skriptet og robots.txt (alltid LF)
├── AGENTS.md                 Instruksjoner for KI-agenter
└── CLAUDE.md                 Laster inn AGENTS.md og sensorveiledningen, og krever sesjonslogg
```

Hvorfor koden er delt slik, står i arkitekturen under.

`.docs/` og `docs/` har forskjellige roller: `.docs/` er det BMad-verktøyene lager (stien er satt i `_bmad/config.toml`), mens `docs/` er fast referansestoff.

## Dokumentasjon

- [Sensorveiledning del 1](docs/sensorveiledning/sensorveiledning-del1.md): vurderingskriteriene arbeidet styres etter
- [Instruksjoner for KI-agenter](AGENTS.md)
- Planleggingsdokumenter i [.docs/planning-artifacts/](.docs/planning-artifacts/):
  - [Product brief](.docs/planning-artifacts/briefs/brief-aill-handle-it-2026-09-23/brief.md)
  - [PRD](.docs/planning-artifacts/prds/prd-aill-handle-it-2026-11-07/prd.md)
  - [UX: utseende (DESIGN.md)](.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/DESIGN.md) og [oppførsel (EXPERIENCE.md)](.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/EXPERIENCE.md)
  - Arkitektur: [forklart på norsk](.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/oversikt.md), [reglene koden følger (ARCHITECTURE-SPINE.md)](.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/ARCHITECTURE-SPINE.md) og [begrunnelsen for hvert valg](.docs/planning-artifacts/architecture/architecture-aill-handle-it-2026-11-16/.memlog.md)
  - [Epics og stories](.docs/planning-artifacts/epics.md)
- Implementering i [.docs/implementation-artifacts/](.docs/implementation-artifacts/): spesifikasjon per story og [sprintstatus](.docs/implementation-artifacts/sprint-status.yaml)
- [Manuell testplan](docs/manual-test-plan.md)
- [Sesjonslogg](.logs/rikke/): prompts, KI-økter og beslutninger, koblet til commits, og [åpne punkter](.logs/rikke/issues.md)

## Bilder

Alle bildene i [static/img/](static/img/) er Rikkes egne eller bilder av stedet som Rikke har lov til å bruke. [static/img/README.md](static/img/README.md) viser kilden til hver fil, og filene lages på nytt med `uvx --with pillow==13.0.0 python -I tools/prepare_images.py` fra rotmappen. Pillow trengs bare til dette skriptet og er ikke en avhengighet for appen.

## Fonter og lisenser

Skriftene Imperial Script og EB Garamond ligger i [static/fonts/](static/fonts/) og er lisensiert under SIL Open Font License 1.1. Lisensene ligger ved siden av fontfilene, og [static/fonts/README.md](static/fonts/README.md) viser hvor filene er hentet fra og kommandoene som laget dem.

Designskillen [Impeccable](https://github.com/pbakaus/impeccable) i [.claude/skills/impeccable/](.claude/skills/impeccable/) er lisensiert under Apache-2.0. Lisensen og NOTICE.md ligger i mappen, og [AGENTS.md](AGENTS.md) beskriver hvordan den brukes i prosjektet.

## Medlemmer

- Rikke Dvergsdal
