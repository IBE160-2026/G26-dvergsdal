# 2026-09-23 – Product brief

| | |
|---|---|
| **Verktøy** | Claude Code, BMad-skill: `bmad-product-brief` (coaching-modus) |
| **Økt-ID** | `b5788704-cd46-4042-8935-be97853983b0` |
| **Branch / PR** | `main` (før branch-arbeidsflyten var på plass) |
| **Commits** | `e61935e` Initial commit, `157b9ba` merge med startcommit, `c840dfb` Fjern personlige BMad-filer |

## Mål

Lage en product brief for bryllupsnettsiden, og få prosjektet opp på gruppens GitHub-repo.

## Viktige prompts

> CB

Startet `bmad-product-brief`. Deretter limte jeg inn en lang beskrivelse på norsk av ideen, bakgrunnen min og bryllupet. KI stilte nummererte spørsmål som jeg svarte på i flere runder.

> the deadline is in the midle of desember. About 70 guests. Might invite a few guests who doesent speak norwegian. Payment will be simply by paying through the bank or with Vipps to us. [...] I'm building this alone. Coach path.

> I forgot to mention that the course need a AI feature. SO I-m thinking a possibility for the guest to ask questions in the website ang get answers. I'm also thinking about an AI feature that helps us [...] to place where the guest are to sleep.

> For the older realtive you can say 10 minutes. I'd like to move guest questions forwarded to my e-mail to the green part. [...] I'd really like to have the letter animation.

> undo and unconnect what you did since my last message

> kan du nå se i min github om jeg har lastet opp for mye. kanskje ikke professoren min trenger alt det?

## Hva KI foreslo, og hva jeg gjorde

| Forslag fra KI | Min vurdering | Resultat |
|---|---|---|
| Suksesskriterier med plassholder for svarprosent | Godtatt, satte 90 % og la til et eget kriterium om at siden skal være lett å bruke | `brief.md` |
| Brukertest med eldre slektning innen 5 minutter | Endret til 10 minutter | `.memlog.md` |
| Videresending av gjestespørsmål på e-post som «stretch» | Endret til «must» | `brief.md` |
| Brevanimasjon | Holdt fast på den som ønske | `brief.md` |
| KI-assistent for gjester og KI-hjelp til sengeplassering | Mitt eget forslag, basert på at jeg trodde emnet krevde en KI-funksjon. Rettet 2026-09-26 | Se [neste logg](2026-09-26-fjern-ki-funksjoner.md) |
| `git init` i prosjektmappen | **Avvist.** KI gjorde det uten at jeg hadde bedt om det, og repoet skulle kobles til gruppens repo. KI slettet `.git`-mappen igjen | – |
| Vurdering av hva som lå på GitHub | Godtatt: BMad skal ligge i repoet, men to personlige BMad-filer som står i `.gitignore`, ble fjernet | `c840dfb` |

## Feil eller svakheter i KI-ens arbeid

- KI opprettet et git-repo uten å spørre. Jeg avviste det og fikk det angret.
- Pushen feilet først fordi PC-en var logget inn med feil GitHub-konto. KI forklarte feilen (403) og ga meg kommandoene for å logge inn på nytt.

## Neste steg

Gå gjennom om emnet faktisk krever en KI-funksjon i appen.
