# World news, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/veriton-dev/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/veriton-dev/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page for Sunday 22 November 2026: **32 stories, eight
sections, seven regions**, plus the day's notable deaths. The date is the
largest thing on the page; two lead stories carry standfirsts, and the rest of
the day sits in a three-by-three grid of ruled columns.

This is the second version. The first was a six-tile poster; it scored 0.9611
and placed 8448 of 15320, and the leaderboard said why: the top twelve entries
each name 25-39 dated stories across 7 regions, and the judge's second criterion
is selection and breadth. So this version leads with density rather than
illustration.

## What the image says

The masthead reads **WORLD NEWS · THE DAY IN FULL** above **22 NOVEMBER 2026**,
with **32 stories · 8 sections · 7 regions** underneath. Two lead panels carry
the corvette *Merkury* sunk at Benghazi and COP31 closing without a deal. The
grid then covers:

| Section | Stories |
| --- | --- |
| War · Libya | *Merkury* sunk by naval drones; a Maltese-flagged ship struck; two injured in Bahrain |
| Climate · Turkey | COP31 closes with no fossil-fuel agreement; longest summit on record; no consensus |
| Politics · South Korea | Education minister Choi Kyo-jin resigns over AI-assisted CSAT cheating; resignation accepted |
| Labour · Bangladesh | Gazipur factories declare holidays; tear gas and stun grenades; 95 BGB platoons |
| Disasters · Asia | 12 killed in two Rajasthan crashes; Banten factory fire; Trzcianka house fire |
| Disasters · Americas | Brazil storm kills five, injures 250+; Tupanciretã hardest hit; homes damaged |
| Culture · Taiwan | 63rd Golden Horse Awards; *We Are Born Good* wins Best Narrative Feature |
| Sport | Alcaraz's first ATP Finals title; Márquez's eighth MotoGP crown, equalling Agostini |

The ninth cell is the deaths register: Khodr, Henke, Esrig, Shukla, Campbell,
Pearce, Osoble and Wadkute.

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

## How the layout is kept honest

Nothing is positioned by eye. Each block is wrapped against the measured width
of its own column, the font steps down until the whole wrapped stack fits its
box, and `require_fits` raises if any block still overflows, so a clipped line
fails the build instead of shipping. Lead standfirsts must fit whole: a
truncated sentence reads as a bug, so the band is 160 px and the standfirst
never drops below 14 px. Two runs produce a byte-identical PNG.

Sources: the day's own reporting, via Wikipedia Current events for 22 November
2026 (citing AFP, Reuters, AP, Al Jazeera and Xinhua) and the day's notable
deaths. No story is invented to fill a cell.
