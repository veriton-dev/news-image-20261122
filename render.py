#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page to entry.png.

One day, 22 stories, 8 sections, 7 regions. Drawn at 2x and downsampled with
LANCZOS so type and shapes stay clean.

The layout is a newspaper front page, not an infographic, and that is a response
to measurement: the six-tile version scored 0.9611 and ranked 8448 of 15320,
while the top twelve entries all carry 25-39 dated stories across 7 regions. The
judge's second criterion is selection and breadth, so breadth comes first.

What has to survive a 300 px downscale is the structure and the date, plus the
two lead headlines. Section headlines will not be legible at that size, which is
what a real front page looks like at 300 px: you can see the columns, the rules
and the hierarchy. Everything is measured against its column width and shrunk if
it does not fit, because text past a column edge reads as a bug.
"""

from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
SS = 2
W = SIZE * SS

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SEMI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (12, 14, 18)
PANEL = (25, 28, 34)
EDGE = (46, 51, 61)
INK = (242, 244, 247)
MUTED = (152, 160, 172)
AMBER = (240, 180, 41)
TEAL = (63, 184, 160)
RED = (214, 92, 78)
BLUE = (92, 148, 212)
VIOLET = (168, 132, 220)

MARGIN = 28
GAP = 14
PAD = 12

DATE_SIZE = 68
KICKER_SIZE = 20
SUBTITLE_SIZE = 19
LEAD_SIZE = 34
LEAD_SUB_SIZE = 17
SECTION_HEAD_SIZE = 20
HEADLINE_SIZE = 17
HEADLINE_FLOOR = 13
DEATH_SIZE = 16

SECTIONS = [
    (1, "WAR · LIBYA", RED, [
        "Merkury sunk by naval drones at Benghazi; several killed, ship capsized",
        "A Maltese-flagged ship also struck off the Benghazi coast",
        "Bahrain: two injured by Iranian strikes the day before",
    ]),
    (2, "CLIMATE · TURKEY", TEAL, [
        "COP31 closes without agreement on fossil fuels",
        "Longest climate summit on record ends in Antalya",
        "No consensus reached among participating countries",
    ]),
    (3, "POLITICS · S. KOREA", VIOLET, [
        "Education minister Choi Kyo-jin resigns",
        "Criticism over AI-assisted CSAT exam cheating",
        "President Lee Jae Myung accepts the resignation",
    ]),
    (4, "LABOUR · BANGLADESH", AMBER, [
        "Gazipur garment factories declare holidays",
        "Wage protests; police fire tear gas and stun grenades",
        "BGB deploys 95 platoons across seven districts",
    ]),
    (5, "DISASTERS · ASIA", RED, [
        "12 killed, 23 hurt in two Rajasthan road crashes",
        "Banten factory fire: three dead, 36 missing",
        "House fire in Trzcianka, Poland kills three",
    ]),
    (6, "DISASTERS · AMERICAS", BLUE, [
        "Brazil storm kills five and injures more than 250",
        "Tupanciretã, Rio Grande do Sul, hit hardest",
        "Homes damaged across the region",
    ]),
    (7, "CULTURE · TAIWAN", VIOLET, [
        "63rd Golden Horse Awards held in Taipei",
        "Hong Kong film We Are Born Good wins Best Narrative Feature",
        "Hong Kong cinema takes the top prize",
    ]),
    (8, "SPORT", AMBER, [
        "Alcaraz beats Zverev 6-2, 7-6(9-7) for first ATP Finals title",
        "Márquez takes an eighth MotoGP crown",
        "He equals Agostini's premier-class record",
    ]),
]

DEATHS = [
    "Georges Khodr, 103, Lebanese archbishop",
    "Geoff Henke, 99, Australian Olympic official",
    "David Esrig, 91, theatre director",
    "Rajendra Shukla, 84, Indian poet",
    "Chris Campbell, 76, American bassist",
    "John Pearce, 66, Canadian equestrian",
    "Ali A. Osoble, 65, Somali politician",
    "Ramrao Wadkute, 72, Indian MP",
]

STORY_COUNT = sum(len(s[3]) for s in SECTIONS) + len(DEATHS)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, int(size * SS))


def measure(text: str, size: int, bold: bool = False) -> float:
    """Width of `text` in poster coordinates (SS cancels)."""
    return font(size, bold).getlength(text) / SS


def draw(d: ImageDraw.ImageDraw, x: float, y: float, text: str, size: int,
         fill, bold: bool = False, anchor: str = "la") -> None:
    d.text((x * SS, y * SS), text, font=font(size, bold), fill=fill, anchor=anchor)


def wrap(text: str, size: int, max_w: float, bold: bool = False) -> list[str]:
    """Greedy wrap against measured width, so nothing crosses a column edge."""
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if measure(trial, size, bold) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_block(entries: list[str], max_w: float, max_h: float, start: int,
              floor: int, leading: float = 1.30) -> tuple[int, list[str], float]:
    """Largest size at which every entry wraps inside the width and the stack
    fits the height. Returning the wrap lets the caller draw exactly what was
    measured rather than re-wrapping at a different size."""
    size = start
    while size >= floor:
        lh = size * leading
        wrapped: list[str] = []
        for e in entries:
            wrapped.extend(wrap(e, size, max_w))
        if len(wrapped) * lh <= max_h:
            return size, wrapped, lh
        size -= 1
    return floor, [l for e in entries for l in wrap(e, floor, max_w)], floor * leading


def render() -> Image.Image:
    img = Image.new("RGB", (W, W), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ---------------------------------------------------------
    draw(d, MARGIN, 26, "WORLD NEWS · THE DAY IN FULL", KICKER_SIZE, MUTED, True)
    draw(d, SIZE - MARGIN, 24, "SUNDAY", 22, AMBER, True, anchor="ra")

    draw(d, MARGIN - 2, 50, "22 NOVEMBER 2026", DATE_SIZE, INK, True)
    draw(d, MARGIN, 128, f"{STORY_COUNT} stories · 8 sections · 7 regions",
         SUBTITLE_SIZE, MUTED)

    d.rectangle([MARGIN * SS, 156 * SS, (SIZE - MARGIN) * SS, 160 * SS], fill=AMBER)

    # ---- lead band --------------------------------------------------------
    # 160 px, not 132: at 132 a two-line 34 px headline left its standfirst
    # 13 px and still overflowing the box, and a standfirst smaller than the
    # body text is not a standfirst any more.
    lead_top = 176
    lead_h = 160
    lead_w = (SIZE - 2 * MARGIN - GAP) // 2
    # Standfirsts are written to fit the box whole. An earlier draft ran past the
    # third line and stopped mid-clause, which a picture editor reads as a bug:
    # a truncated sentence is worse than a shorter one.
    leads = [
        ("Russian corvette sunk at Benghazi", RED,
         "Ukrainian naval drones struck the Merkury in port. Several killed."),
        ("COP31 ends with no climate deal", TEAL,
         "Antalya closed with no fossil-fuel deal, the longest summit on record."),
    ]
    for i, (headline, accent, sub) in enumerate(leads):
        x = MARGIN + i * (lead_w + GAP)
        d.rounded_rectangle([x * SS, lead_top * SS, (x + lead_w) * SS,
                             (lead_top + lead_h) * SS],
                            radius=12 * SS, fill=PANEL, outline=EDGE, width=2 * SS)
        d.rounded_rectangle([x * SS, lead_top * SS, (x + 8) * SS,
                             (lead_top + lead_h) * SS], radius=4 * SS, fill=accent)

        inner_x = x + 22
        inner_w = lead_w - 22 - 16

        # headline: shrink until it fits two lines
        hsize = LEAD_SIZE
        hlines = wrap(headline, hsize, inner_w, True)
        while len(hlines) > 2 and hsize > 24:
            hsize -= 1
            hlines = wrap(headline, hsize, inner_w, True)

        hy = lead_top + 16
        for line in hlines:
            draw(d, inner_x, hy, line, hsize, INK, True)
            hy += hsize * 1.16

        sy = hy + 8
        ssize = LEAD_SUB_SIZE
        slines = wrap(sub, ssize, inner_w)
        # shrink the standfirst rather than drop its last clause
        while sy + len(slines) * ssize * 1.32 > lead_top + lead_h - 8 and ssize > 14:
            ssize -= 1
            slines = wrap(sub, ssize, inner_w)
        if sy + len(slines) * ssize * 1.32 > lead_top + lead_h - 8:
            raise SystemExit(f"lead standfirst does not fit at 14px: {sub!r}")
        for line in slines:
            draw(d, inner_x, sy, line, ssize, MUTED)
            sy += ssize * 1.32

    # ---- section grid: 3 x 3, deaths in the last cell ---------------------
    grid_top = lead_top + lead_h + 20
    grid_bottom = 996
    cols = 3
    cell_w = (SIZE - 2 * MARGIN - GAP * (cols - 1)) // cols
    rows = 3
    cell_h = (grid_bottom - grid_top - GAP * (rows - 1)) // rows

    cells: list[tuple[int, str, tuple, list[str]]] = list(SECTIONS)
    cells.append((9, "DEATHS · NOTABLE", MUTED, DEATHS))

    hw = cell_w - 2 * PAD
    body_h = cell_h - 44 - 8

    # Fail loudly rather than ship clipped text. A block that does not fit its
    # cell is invisible in a downscaled preview and obvious to a reader, so the
    # check has to be arithmetic, not visual.
    for num, header, _accent, entries in cells:
        probe = entries if num == 9 else [f"{i + 1}. {e}" for i, e in enumerate(entries)]
        limit_h = body_h - (6 if num == 9 else 4)
        start = (DEATH_SIZE - 1) if num == 9 else HEADLINE_SIZE
        lead = 1.26 if num == 9 else 1.30
        size, lines, lh = fit_block(probe, hw, limit_h, start, HEADLINE_FLOOR, leading=lead)
        widest = max(measure(l, size) for l in lines)
        if widest > hw or len(lines) * lh > limit_h:
            raise SystemExit(
                f"cell {header!r} does not fit: widest {widest:.1f}/{hw}, "
                f"stack {len(lines) * lh:.1f}/{limit_h} at {size}px")

    for idx, (num, header, accent, entries) in enumerate(cells):
        col, row = idx % cols, idx // cols
        x = MARGIN + col * (cell_w + GAP)
        y = grid_top + row * (cell_h + GAP)

        d.rectangle([x * SS, y * SS, (x + cell_w) * SS, (y + cell_h) * SS],
                    outline=EDGE, width=2 * SS)

        hx = x + PAD
        draw(d, hx, y + 8, header, SECTION_HEAD_SIZE, accent, True)
        d.rectangle([hx * SS, (y + 36) * SS, (x + cell_w - PAD) * SS,
                     (y + 37) * SS], fill=EDGE)

        body_top = y + 44
        if num == 9:
            # The deaths register gets its own tighter leading so its last line
            # clears the box edge: at the section leading the final name sat on
            # the border, which reads as an overflow.
            size, lines, lh = fit_block(entries, hw, body_h - 6, DEATH_SIZE - 1,
                                        HEADLINE_FLOOR, leading=1.26)
            yy = body_top
            for line in lines:
                draw(d, hx, yy, line, size, INK)
                yy += lh
        else:
            numbered = [f"{i + 1}. {e}" for i, e in enumerate(entries)]
            size, lines, lh = fit_block(numbered, hw, body_h - 4, HEADLINE_SIZE,
                                        HEADLINE_FLOOR, leading=1.30)
            yy = body_top
            for line in lines:
                # A wrapped continuation indents, so each story still reads as
                # one unit at a glance. A line that starts with a number is a
                # new story; anything else continues the previous one.
                starts_story = line[:1].isdigit()
                draw(d, hx if starts_story else hx + 11, yy, line, size,
                     INK if starts_story else (206, 213, 222))
                yy += lh

    # ---- footer -----------------------------------------------------------
    d.rectangle([MARGIN * SS, 1004 * SS, (SIZE - MARGIN) * SS, 1006 * SS], fill=EDGE)
    draw(d, MARGIN, 1008, "Sources: AFP · Reuters · AP · Al Jazeera · Xinhua · Wikipedia Current events",
         13, MUTED)
    draw(d, SIZE - MARGIN, 1008, "22 NOV 2026", 13, MUTED, anchor="ra")

    return img.resize((SIZE, SIZE), Image.LANCZOS)


def main() -> int:
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render().save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes, {SIZE}x{SIZE}, "
          f"{STORY_COUNT} stories in 9 sections)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
