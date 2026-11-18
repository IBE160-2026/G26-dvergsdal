# Fonter

Nettsiden henter skriftene fra egen server, aldri fra Google Fonts eller andre (PRD 3.2, AD-15, UX-DR2). Begge familiene er lisensiert under SIL Open Font License 1.1, og lisensen ligger ved siden av filene.

| Fil | Familie | Kilde | Lisens |
|---|---|---|---|
| `imperial-script-400.woff2` | Imperial Script, regular (bare navnene «Rikke & Valdemar») | [ImperialScript-Regular.ttf](https://github.com/google/fonts/blob/7af0d90b4d532ffa4b041937b560c6df4e7b1e95/ofl/imperialscript/ImperialScript-Regular.ttf) | [imperial-script-OFL.txt](imperial-script-OFL.txt) |
| `eb-garamond-roman.woff2` | EB Garamond, rett, variabel vekt 400–800 | [EBGaramond[wght].ttf](https://github.com/google/fonts/blob/7af0d90b4d532ffa4b041937b560c6df4e7b1e95/ofl/ebgaramond/EBGaramond%5Bwght%5D.ttf) | [eb-garamond-OFL.txt](eb-garamond-OFL.txt) |
| `eb-garamond-italic.woff2` | EB Garamond, kursiv, variabel vekt 400–800 | [EBGaramond-Italic[wght].ttf](https://github.com/google/fonts/blob/7af0d90b4d532ffa4b041937b560c6df4e7b1e95/ofl/ebgaramond/EBGaramond-Italic%5Bwght%5D.ttf) | [eb-garamond-OFL.txt](eb-garamond-OFL.txt) |

Kildene er hentet fra [google/fonts](https://github.com/google/fonts) på commit `7af0d90b4d532ffa4b041937b560c6df4e7b1e95` (18. november 2026). EB Garamond er variable fonter, så én fil per stil dekker både 400 (brødtekst) og 600 (etiketter og uthevinger).

## Slik ble filene laget

Kommandoene under er for bash. På Windows kjøres de i Git Bash, som følger med Git for Windows. Kjør dem i en tom mappe utenfor repoet.

Hent kildefilene fra den låste commiten:

```bash
SRC=https://raw.githubusercontent.com/google/fonts/7af0d90b4d532ffa4b041937b560c6df4e7b1e95/ofl
curl -fL -o ImperialScript-Regular.ttf "$SRC/imperialscript/ImperialScript-Regular.ttf"
curl -fL -o "EBGaramond[wght].ttf" "$SRC/ebgaramond/EBGaramond%5Bwght%5D.ttf"
curl -fL -o "EBGaramond-Italic[wght].ttf" "$SRC/ebgaramond/EBGaramond-Italic%5Bwght%5D.ttf"
sha256sum ImperialScript-Regular.ttf "EBGaramond[wght].ttf" "EBGaramond-Italic[wght].ttf"
```

`sha256sum` skal gi disse verdiene:

| Kildefil | SHA-256 |
|---|---|
| `ImperialScript-Regular.ttf` | `fa040ae596cde82559c3bcf056ac216a94efa904b848382ab85740d38df4bab7` |
| `EBGaramond[wght].ttf` | `ef9512f92f6d579e5dc75af59a5a4b1b8b47d2eda89e00b954d44520e5369027` |
| `EBGaramond-Italic[wght].ttf` | `bba2c4499c93c9612b90b9825d32b07da52fce2fe57562a1eb6b833553f93c4e` |

Filene er så kuttet ned til latinske tegn (med æ, ø og å, «», ·, –, … og pilen ←) og lagret som WOFF2. Alle OpenType-funksjonene er beholdt, så linjetall (`lnum`), tabelltall (`tnum`) og kapitéler (`smcp`, `c2sc`) virker. Kommandoene kjøres i samme mappe:

```bash
UNICODES="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD"
uvx --from "fonttools[woff]" pyftsubset ImperialScript-Regular.ttf --unicodes="$UNICODES" --layout-features='*' --flavor=woff2 --output-file=imperial-script-400.woff2
uvx --from "fonttools[woff]" pyftsubset "EBGaramond[wght].ttf" --unicodes="$UNICODES" --layout-features='*' --flavor=woff2 --output-file=eb-garamond-roman.woff2
uvx --from "fonttools[woff]" pyftsubset "EBGaramond-Italic[wght].ttf" --unicodes="$UNICODES" --layout-features='*' --flavor=woff2 --output-file=eb-garamond-italic.woff2
```

Med fonttools 4.68.0 og brotli 1.2.1 (det `uvx` hentet 18. november 2026) ga dette filene som ligger her:

| Fil | SHA-256 |
|---|---|
| `imperial-script-400.woff2` | `000f14b10faa5a8e7cb82e6a3b0b1cf77f1fceaa64e9db1f49e4473e26535b0b` |
| `eb-garamond-roman.woff2` | `7fc9f183f1ff5767f891a9c40b0322b80241fc72313f872458b1b128942c610e` |
| `eb-garamond-italic.woff2` | `b984f0ebc13b29bd7256c178c22a41e6e97fb584e3d9203d118a12537b9a96c8` |

En annen versjon av fonttools eller brotli kan gi andre byte, selv om fontene er like. Tegnområdet er det samme som Google Fonts bruker for «latin», pluss pilene U+2190–2193 (for «← Tilbake til invitasjonen»). Imperial Script har ingen pil, men den brukes bare til navnene.
