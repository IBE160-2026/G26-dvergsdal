# Bilder

Alle bildene på nettsiden er Rikkes egne eller bilder av stedet som Rikke har fått lov til å bruke (EXPERIENCE.md › Inspiration & Anti-patterns). Ingen blomster, segl, blonder eller ikoner er tegnet i kode (UX-DR4, DESIGN.md › Shapes). Utklippene ble laget under UX-arbeidet med skriptene i `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/.working/cutout-*.py`.

Filene her er laget av [tools/prepare_images.py](../../tools/prepare_images.py) fra kildene i tabellen. Hver fil er høyst dobbelt så bred som den vises (skarp på mobilskjermer), aldri forstørret, og høyst 100 KB. Bildene forsiden bruker, er til sammen høyst 300 KB, så forsiden er brukbar på under 3 sekunder på 4G (NFR-7). Foto og illustrasjon er progressiv JPEG uten metadata, utklipp og ikoner er PNG med 256 farger og gjennomsiktighet. Ingen WebP eller AVIF, så eldre iPader viser alt.

| Fil | Kilde | Vises som | Filbredde |
|---|---|---|---|
| `segl.png` | `mockups/segl.png` (fra egne-bilder 06-Stamp.jpg) | Lakksegl over toppen av invitasjonen, 74 px | 148 px |
| `favicon-32.png` | `mockups/segl.png` | Ikon i nettleserfanen, gjennomsiktig | 32 px |
| `apple-touch-icon.png` | `mockups/segl.png` | Ikon på hjemskjermen (iOS), seglet på `page-green` fordi iOS gjør gjennomsiktig svart | 180 px |
| `brudeslor.png` | `mockups/brudeslor.png` (fra egne-bilder 07-Flowers.jpg) | Brudeslør, 224 px i toppen, 180 px i svarfeltet og på siden for ugyldige lenker | 448 px |
| `lilje-topp.png` | `mockups/lilje-topp.png` (fra egne-bilder 09-FlowersTop.jpg) | Liljekrans over «Alt om helgen», 296 px | 592 px |
| `lilje-bunn.png` | `mockups/lilje-bunn.png` (fra egne-bilder 10-FlowersBottom.jpg) | Liljekrans under «Alt om helgen», 296 px | 592 px |
| `blonde.png` | `mockups/blonde.png` (fra egne-bilder 11-Frame.jpg) | Blonderamme, 136 px på forsiden og 220 px på infosidene | 320 px (kilden er 320) |
| `illustrasjon.jpg` | `ux/egne-bilder/04-Illustration.jpg` (sjekket: ingen signatur eller tekst) | Akvarellen av tunet i toppen, 262 px | 524 px |
| `oss-strand.jpg` | `mockups/us1-utsnitt.jpg` (utsnitt av egne-bilder 12-Us1.jpg) | Brudeparet, «Vår historie» på forsiden | 400 px (kilden er 400) |
| `oss-utsikt.jpg` | `ux/egne-bilder/13-Us2.jpg` | Brudeparet på siden «Vår historie», 220 px | 440 px |
| `sted-middag.jpg` | `ux/stedet/01-Venue.jpg` | «Programmet» på forsiden | 440 px |
| `sted-tunet.jpg` | `ux/stedet/03-Venue.jpg` | «Praktisk informasjon» på forsiden og «Hardingasete og hyttene» | 440 px |
| `sted-kirka.jpg` | `ux/stedet/18-Kirka.jpg` | «Vielsen» på «Praktisk informasjon», 220 px | 440 px |
| `sted-omradet.jpg` | `ux/stedet/12-Area.jpg` | «Området rundt» på «Praktisk informasjon», 220 px | 440 px |
| `ikoner/ikon-01-fjelltur.png` … `ikoner/ikon-12-avreise.png` | `mockups/ikoner/` (fra egne-bilder 14-Icons.jpg) | Programikonene, 56 px | 112 px |

De tolv ikonene er `ikoner/ikon-01-fjelltur.png`, `ikoner/ikon-02-hytte.png`, `ikoner/ikon-03-rebus.png`, `ikoner/ikon-04-middag.png`, `ikoner/ikon-05-stamp.png`, `ikoner/ikon-06-frokost.png`, `ikoner/ikon-07-yoga.png`, `ikoner/ikon-08-bil.png`, `ikoner/ikon-09-ringer.png`, `ikoner/ikon-10-lunsj.png`, `ikoner/ikon-11-fest.png` og `ikoner/ikon-12-avreise.png`.

`mockups/` er `.docs/planning-artifacts/ux-designs/ux-aill-handle-it-2026-11-10/mockups/`, og `ux/` er `.docs/planning-artifacts/ux/`.

## Slik lages filene på nytt

Kjør fra rotmappen i repoet (Git Bash, PowerShell eller en terminal på macOS/Linux):

```bash
uvx --with pillow==13.0.0 python -I tools/prepare_images.py
```

Pillow brukes bare av dette skriptet og er ikke en avhengighet for appen. Skriptet gir de samme filene hver gang, så `git status` er ren etter en ny kjøring. Bytter Rikke ut et bilde, legges den nye kilden der tabellen viser, og kommandoen kjøres på nytt; filene her redigeres aldri for hånd.
