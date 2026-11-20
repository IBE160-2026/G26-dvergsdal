# Story 1.4c: personvern i hoder, lenkeforhåndsvisning og logger

## 2026-11-20 kl. 17:39 — Rikke

### Oppgave
Andre story i den autonome goal-kjøringen (prompten er sitert i [story-1-4b-papir-bilder-g1](973-2026-11-20-17-07-22-story-1-4b-papir-bilder-g1.md)). Intensjonen til `bmad-build-auto` var «Story 1.4c i .docs/planning-artifacts/epics.md»: lenken og navnet til en gjest skal holdes unna søkemotorer, forhåndsvisninger og serverloggen (FR-4, NFR-4, AD-15).

### Plan
- Gren `feat/1-4c-personvern-hoder-og-logger`.
- Én planleggings-sub-agent sjekket epic-konteksten (gyldig, ikke kompilert på nytt) og skrev [spec-1-4c](../../.docs/implementation-artifacts/spec-1-4c-guest-pages-stay-private-headers-link-previews-and-logs.md). Claude sjekket den mot «Ready for Development».
- En implementerings-sub-agent bygde og committet i små steg. Claude leste diffen og kjørte testene.
- Fire gjennomgangs-sub-agenter. Claude triagerte funnene og sendte rettingene tilbake til implementeringsagenten.
- MT-8 og MT-9 med Playwright mot Edge.

### Resultat
**Bygd:** `X-Robots-Tag: noindex` på alle svar, `Referrer-Policy: same-origin`, noindex-meta og én fast Open Graph-forhåndsvisning i `base.html` utenfor alle blokker (bilde: utsnitt av Rikkes akvarell), `/robots.txt` over oppsamlingsruten, og et loggfilter som maskerer lenkekoden som `/[code]/`.

**Hva KI foreslo, og hva som ble godtatt, endret eller avvist:**
- **Godtatt fra planleggeren:** `robots.txt` blokkerer ingenting, fordi en søkemotor som ikke får hente siden aldri ser `noindex`. Tekstene i forhåndsvisningen er «Invitasjon» og «En personlig invitasjon. Åpne lenken for å se den.» (Rikke kan ønske andre ord). Forhåndsvisningsbildet er 1000×525, ikke 1200×630, for å holde seg under 100 KB. Filteret maskerer alle første ledd, ikke bare koder på 22 tegn, fordi en feilskrevet kode nesten er en ekte.
- **Funnet av Claude i nettleseren:** første kjøring av MT-8 viste at bildet i `og:image` manglet `X-Robots-Tag` under `runserver`. Django serverer statiske filer utenom mellomvaren. Rettet med `whitenoise.runserver_nostatic`. Blind Hunter fant det samme.
- **Endret etter gjennomgangen (18 rettinger):**
  - Loggfilteret slapp gjennom koder i hele URL-er (Djangos CSRF-melding tar med hele Referer), etter `=`, med dobbel skråstrek og i tracebacks.
  - Filterrekkefølgen gjorde at en avvist post ble sendt videre umaskert.
  - Med `DEBUG` av ble ingenting logget i det hele tatt. Ny feilhandler for WARNING og over, og en rot-logger.
  - `og:image` ble `:///…` uten request.
  - Testen for Referrer-Policy kunne aldri feile.
  - `NOT_LINK_CODES` sjekkes nå mot URL-oppsettet, så story 3.1 sin `admin/` feiler testen til filteret kjenner den.
- **Avvist (5):** blant annet at sammenligningen av forhåndsvisninger for to koder er triviell nå. Testen bruker ekte seed-koder og blir reell i story 1.5.
- **Utsatt:** produksjonens tilgangslogg, `SECURE_PROXY_SSL_HEADER`, `SECURE_SSL_REDIRECT` og MT-10 (ekte Messenger/SMS) venter på hosting. En 400-side for DisallowedHost hører til story 1.8.

**Verifisert:** `uv run pytest` 492 bestått (fra 427), ruff og djlint rene. MT-8 og MT-9 bestått i Edge med Playwright, før og etter rettingene, og MT-5/MT-6 fra 1.4b består fortsatt.

**Commits:** `1e6cbcc` … `47ef777` (13 commits). [PR #26](https://github.com/IBE160-2026/G26-dvergsdal/pull/26).

### Åpne punkter
- MT-10: lim inn en testlenke i Messenger og en SMS når nettsiden ligger på en offentlig adresse.
- Rikke kan vurdere ordlyden i forhåndsvisningen («Invitasjon» / «En personlig invitasjon. Åpne lenken for å se den.»).
