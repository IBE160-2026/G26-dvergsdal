# Story 3.4 — Oversikt over alle husstander og allergilisten

## 2026-11-27 kl. 12:00 — Rikke

### Oppgave
Del av den uovervåkede goal-kjøringen. Rikkes goal-prompt står ordrett i [973-loggen](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md). Intensjonen for bmad-build-auto var ordrett: «Story 3.4 i .docs/planning-artifacts/epics.md». Brudeparet skal kunne sjekke én husstand og gi Hardingasete navnene med allergier, og «Se hva alle har svart» manglet adresse.

### Plan
- Spec: [spec-3-4-the-overview-of-every-household-and-the-allergy-list.md](../../.docs/implementation-artifacts/spec-3-4-the-overview-of-every-household-and-the-allergy-list.md), skrevet av en planleggeragent. Implementering ved en egen agent i åtte små commits (retro-punkt 12), uten å røre `wedding/rsvp/views.py`.

### Resultat
**Hva KI foreslo, og hva som ble godtatt, endret eller avvist**
- Planleggeren oppdaget at husstandssiden A6 er story 6.3, ikke 3.4, og foreslo at husstandslenkene på tellesidene peker til raden på Gjester (`#husstand-<id>`). Godtatt; avviket er ført i epics, EXPERIENCE og deferred-work, og lenkene repekes i 6.3.
- Allergilisten bygges på én ny regel `allergy_list` rundt `allergy_state_ids`, så lengden er lik tallet på Oversikt. Godtatt.
- Implementereren fant en endring i commit 4 som pekte på en rute fra commit 5, og rettet historikken lokalt før push. Godtatt.
- Gjennomgangen ga 20 funn: 3 rettet, 4 utsatt, 13 avvist.
  - Rettet: allergilisten merket «Gjester» som åpen side (sett i Edge i MT-82), navn/kategori/merknad ble lest som én streng, duplisert testoppsett med passord skrevet ut.
  - Avvist blant annet: `answered` fra første gjest (svaret sendes per husstand), `assert` for typesnevring, to spørringer uten transaksjon (samme begrunnelse som i 3.3).
  - Avvist som falske: «MT ikke kjørt», «ingen sesjonslogg» og «status done» (alle er senere steg i løpet).
- Nettleser: MT-79 til MT-84 bestått. Skriptets «allergiord»-sjekk slo ut bare på lenken «Allergilisten»; det var en skriptfeil, ikke allergitekst i radene.

**Verifisert:** `uv run pytest` 1610 beståtte tester, ruff, ruff format og djlint rene. Nettleser: tall lik `expected.toml` (7 husstander, 14 gjester, totaler), 14 husstandslenker treffer riktig rad, utlogget avvist, hjelper, bare tastatur, 360 og 180 px ved 18 og 22,5 px uten overflyt og alle lenker minst 44 px.

**Commits:** `f16b5b1` til «Story 3.4 ferdig» på `feat/3-4-oversikt-og-allergiliste`. PR: https://github.com/IBE160-2026/G26-dvergsdal/pull/52

**Løst fra issues.md / deferred-work.md:** adressen til «Se hva alle har svart», testhjelperne i `tests/helpers.py` og den samtykkesjekkede allergilisten.

### Åpne punkter
- Husstandslenkene må repekes til A6 i story 6.3 (deferred-work).
- Markering av målrad, utskrift/eksport av allergilisten og husstander uten gjester (deferred-work).
