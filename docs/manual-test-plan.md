# Manuell testplan

Sjekker som ikke lar seg automatisere med pytest, for eksempel at appen starter på en ren maskin, hvordan sidene ser ut på en smal mobilskjerm, og ting som krever en ekte nettleser. Hver story legger til radene den trenger. De automatiske testene kjøres med `uv run pytest` (se [README](../README.md#tester-og-sjekker)).

**Slik brukes tabellen:** Gjør stegene, sammenlign med forventet resultat, og fyll inn dato og resultat (`Bestått` eller `Feilet: <hva som skjedde>`). Ved ny kjøring legges en ny linje til under samme id, så historikken blir stående. Skriv hvem som testet, og på hvilken maskin.

| Id | Story | Steg | Forventet resultat | Dato | Resultat |
|---|---|---|---|---|---|
| MT-1 | 1.1 | På en maskin med uv og uten `.env`: klon repoet til en ny mappe og kjør kommandoene under «Installere og starte» i README (`uv sync`, `uv run manage.py migrate`, `uv run manage.py runserver`). Åpne <http://127.0.0.1:8000/>, stopp serveren med `Ctrl+C` og kjør `git status`. | Serveren starter uten feil og uten nøkler eller kontoer, siden viser Djangos startside («Installasjonen var vellykket!», til forsiden kommer i story 1.5), og `git status` viser ingen endringer (verken `db.sqlite3` eller `staticfiles/`). | 2026-11-16 | Bestått. Kjørt av Claude (KI-agent) på Windows 11 med uv 0.13.8, i en fersk klone av den lokale grenen `feat/1-1-kjorbart-prosjekt`; serveren ble startet på port 8765 og siden hentet med `curl`. Bør gjentas av Rikke i en nettleser fra GitHub-klonen. |
