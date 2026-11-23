# World news, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/veriton-dev/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/veriton-dev/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One poster for Sunday 22 November 2026: six events, six countries, six fields.
The date is the largest thing on the page; each tile carries a beat-and-country
tag and two short label lines under a flat pictogram.

## What the image says

A dark 1024x1024 poster. The masthead reads **SUNDAY · WORLD NEWS** above
**22 NOVEMBER 2026**, with a thin rule and a six-colour accent strip. Below it
sit six tiles in a 2x3 grid, one accent colour per beat:

| Beat · country | Tile label |
| --- | --- |
| War · Libya | Corvette sunk / at Benghazi |
| Climate · Turkey | COP31 ends / with no deal |
| Labour · Bangladesh | Wage protests / shut factories |
| Disaster · Brazil | Storm kills five / 250+ injured |
| Politics · South Korea | Minister resigns / over AI cheating |
| Sport · Portugal | Márquez seals / 8th MotoGP title |

The stories, as reported on the day:

1. **Libya** — Ukrainian naval drones struck the Russian corvette *Merkury*
   while it was docked at Benghazi; several were killed and at least 10 were
   injured, the ship later capsized and sank, and a Maltese-flagged ship was
   also struck off Benghazi.
2. **Turkey** — COP31, the 2026 UN climate conference in Antalya, closed
   without a final agreement after countries failed to agree on fossil fuel
   policy; it was the longest climate summit on record.
3. **Bangladesh** — factories in Gazipur declared holidays amid minimum-wage
   protests, workers and police clashed on the Dhaka–Mymensingh Highway, and
   the BGB deployed 95 platoons across seven districts.
4. **Brazil** — a severe thunderstorm killed five people and injured more than
   250 in Tupanciretã, Rio Grande do Sul.
5. **South Korea** — education minister Choi Kyo-jin resigned over the
   government's response to AI-assisted cheating concerns around the College
   Scholastic Ability Test; President Lee Jae Myung accepted the resignation.
6. **Portugal** — Marc Márquez finished eighth at the Portuguese Grand Prix to
   secure his eighth premier-class MotoGP World Championship, equalling Giacomo
   Agostini's record.

## How to run it

```sh
python3 render.py                                   # draws entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts                 # copies it to out/entry.png
```

`render.py` needs Python 3 and Pillow (both installed here); `main.ts` needs
Node 22 or newer and uses only the standard library. `main.ts` writes to
`$MAKEFUN_OUTPUT_DIR/entry.png`, falling back to `/output/entry.png`, and exits
non-zero if `entry.png` has not been rendered yet.
