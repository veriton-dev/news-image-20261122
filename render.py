#!/usr/bin/env python3
"""Render the 22 November 2026 world-news poster to entry.png.

One day, six stories, six countries. The poster is drawn at 2x and
downsampled with LANCZOS so shapes and type stay clean at judge scale.
"""

from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
SS = 2
W = SIZE * SS

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (12, 15, 20)
PANEL = (24, 29, 37)
EDGE = (40, 48, 59)
INK = (240, 243, 247)
MUTED = (148, 159, 173)

LABEL_SIZE = 46
TAG_SIZE = 24
KICKER_SIZE = 26
DATE_SIZE = 72
SUB_SIZE = 28

MARGIN = 28
GAP_X = 16
GAP_Y = 16
PAD = 18
TOP = 228
TILE_W = (SIZE - 2 * MARGIN - GAP_X) // 2
TILE_H = 245
INNER_W = TILE_W - 2 * PAD
PILL_H = 36
ICON = 58
ICON_GAP = 8

STORIES = [
    {
        "tag": "WAR · LIBYA",
        "lines": ("Corvette sunk", "at Benghazi"),
        "accent": (232, 93, 93),
        "icon": "ship",
    },
    {
        "tag": "CLIMATE · TURKEY",
        "lines": ("COP31 ends", "with no deal"),
        "accent": (74, 196, 143),
        "icon": "globe",
    },
    {
        "tag": "LABOUR · BANGLADESH",
        "lines": ("Wage protests", "shut factories"),
        "accent": (242, 168, 58),
        "icon": "crowd",
    },
    {
        "tag": "DISASTER · BRAZIL",
        "lines": ("Storm kills five", "250+ injured"),
        "accent": (86, 168, 232),
        "icon": "storm",
    },
    {
        "tag": "POLITICS · SOUTH KOREA",
        "lines": ("Minister resigns", "over AI cheating"),
        "accent": (198, 124, 226),
        "icon": "screen",
    },
    {
        "tag": "SPORT · PORTUGAL",
        "lines": ("Márquez seals", "8th MotoGP title"),
        "accent": (232, 196, 74),
        "icon": "helmet",
    },
]


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size * SS)


def width(text: str, size: int, bold: bool = True) -> float:
    return font(size, bold).getlength(text) / SS


def draw_text(d: ImageDraw.ImageDraw, x: float, y: float, text: str,
              size: int, fill, bold: bool = True, anchor: str = "ls") -> None:
    d.text((x * SS, y * SS), text, font=font(size, bold), fill=fill, anchor=anchor)


class Frame:
    """Maps a 100x100 icon design space onto a box of the poster."""

    def __init__(self, d: ImageDraw.ImageDraw, x: float, y: float, s: float):
        self.d = d
        self.x = x
        self.y = y
        self.k = s / 100.0

    def _pt(self, px: float, py: float) -> tuple[float, float]:
        return ((self.x + px * self.k) * SS, (self.y + py * self.k) * SS)

    def _box(self, x0, y0, x1, y1):
        ax, ay = self._pt(x0, y0)
        bx, by = self._pt(x1, y1)
        return [ax, ay, bx, by]

    def rect(self, x0, y0, x1, y1, fill):
        self.d.rectangle(self._box(x0, y0, x1, y1), fill=fill)

    def round_rect(self, x0, y0, x1, y1, r, fill=None, outline=None, w=0):
        self.d.rounded_rectangle(
            self._box(x0, y0, x1, y1),
            radius=r * self.k * SS, fill=fill, outline=outline,
            width=int(w * self.k * SS),
        )

    def ellipse(self, x0, y0, x1, y1, fill=None, outline=None, w=0):
        self.d.ellipse(self._box(x0, y0, x1, y1), fill=fill, outline=outline,
                       width=int(w * self.k * SS))

    def poly(self, pts, fill):
        self.d.polygon([self._pt(px, py) for px, py in pts], fill=fill)

    def line(self, pts, fill, w=3):
        self.d.line([self._pt(px, py) for px, py in pts], fill=fill,
                    width=max(1, int(w * self.k * SS)))

    def arc(self, x0, y0, x1, y1, start, end, fill, w=3):
        self.d.arc(self._box(x0, y0, x1, y1), start=start, end=end, fill=fill,
                   width=int(w * self.k * SS))


def icon_ship(f: Frame, a):
    f.rect(24, 18, 31, 46, a)
    f.rect(10, 30, 42, 58, a)
    f.rect(48, 42, 88, 58, a)
    f.poly([(2, 58), (98, 58), (84, 80), (16, 80)], a)
    f.line([(4, 90), (28, 84), (52, 90), (76, 84), (96, 90)], a, 3)


def icon_globe(f: Frame, a):
    f.ellipse(16, 10, 84, 78, outline=a, w=4)
    f.ellipse(40, 10, 60, 78, outline=a, w=4)
    f.line([(16, 44), (84, 44)], a, 4)
    f.line([(24, 27), (76, 27)], a, 4)
    f.line([(24, 61), (76, 61)], a, 4)
    f.line([(50, 10), (50, 78)], a, 4)


def icon_crowd(f: Frame, a):
    for cx, cy in ((24, 34), (76, 34), (50, 20)):
        f.ellipse(cx - 8, cy - 8, cx + 8, cy + 8, fill=a)
    for cx, cy in ((24, 44), (76, 44), (50, 30)):
        f.round_rect(cx - 14, cy, cx + 14, cy + 32, 8, fill=a)
    for cx, cy in ((12, 62), (88, 62), (50, 68)):
        f.ellipse(cx - 8, cy - 8, cx + 8, cy + 8, fill=a)
    for cx, cy in ((12, 72), (88, 72), (50, 78)):
        f.round_rect(cx - 14, cy, cx + 14, cy + 26, 8, fill=a)


def icon_storm(f: Frame, a):
    f.ellipse(4, 22, 46, 58, fill=a)
    f.ellipse(30, 10, 76, 50, fill=a)
    f.ellipse(54, 22, 98, 62, fill=a)
    f.rect(14, 40, 88, 60, a)
    f.poly([(55, 58), (36, 88), (50, 88), (42, 106), (66, 72), (51, 72), (61, 58)], a)
    f.line([(2, 74), (11, 86)], a, 3)
    f.line([(90, 70), (99, 82)], a, 3)


def icon_screen(f: Frame, a):
    f.round_rect(6, 8, 94, 72, 6, outline=a, w=4)
    f.rect(38, 72, 62, 82, a)
    f.round_rect(24, 82, 76, 90, 4, fill=a)
    f.line([(32, 24), (68, 56)], a, 6)
    f.line([(68, 24), (32, 56)], a, 6)


def icon_helmet(f: Frame, a):
    f.ellipse(8, 4, 92, 88, fill=a)
    f.rect(2, 52, 98, 76, a)
    f.round_rect(32, 42, 92, 62, 9, fill=BG)
    f.round_rect(42, 70, 74, 78, 4, fill=BG)
    f.rect(2, 76, 98, 88, BG)
    f.rect(8, 76, 92, 86, a)


ICONS = {
    "ship": icon_ship,
    "globe": icon_globe,
    "crowd": icon_crowd,
    "storm": icon_storm,
    "screen": icon_screen,
    "helmet": icon_helmet,
}


def check_fit() -> None:
    worst_label = (0.0, "")
    for s in STORIES:
        for label in s["lines"]:
            w = width(label, LABEL_SIZE)
            if w > worst_label[0]:
                worst_label = (w, label)
            if w > INNER_W:
                raise SystemExit(f"label overflows tile: {label!r} {w:.1f} > {INNER_W}")
        pill_w = width(s["tag"], TAG_SIZE) + 24
        if pill_w + ICON_GAP + ICON > INNER_W:
            raise SystemExit(f"tag row overflows tile: {s['tag']!r} {pill_w + ICON_GAP + ICON} > {INNER_W}")
    tag = max(((width(s["tag"], TAG_SIZE), s["tag"]) for s in STORIES))
    print(f"labels {LABEL_SIZE}px: widest {worst_label[0]:.1f}px ({worst_label[1]}) of {INNER_W}px")
    print(f"tags {TAG_SIZE}px: widest {tag[0]:.1f}px ({tag[1]})")


def render() -> Image.Image:
    check_fit()
    img = Image.new("RGB", (W, W), BG)
    d = ImageDraw.Draw(img)

    draw_text(d, MARGIN, 44, "SUNDAY · WORLD NEWS", KICKER_SIZE, MUTED)
    draw_text(d, SIZE - MARGIN, 44, "6 STORIES · 6 COUNTRIES", KICKER_SIZE, MUTED, anchor="rs")

    draw_text(d, MARGIN, 139, "22 NOVEMBER 2026", DATE_SIZE, INK)

    d.rectangle([MARGIN * SS, 162 * SS, (SIZE - MARGIN) * SS, 165 * SS], fill=EDGE)
    for i, s in enumerate(STORIES):
        x0 = MARGIN + i * 6
        d.rectangle([x0 * SS, 161 * SS, (x0 + 4) * SS, 166 * SS], fill=s["accent"])

    draw_text(d, MARGIN, 198, "Six stories from six regions, in one day", SUB_SIZE, MUTED, bold=False)

    for i, s in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = MARGIN + col * (TILE_W + GAP_X)
        y = TOP + row * (TILE_H + GAP_Y)
        a = s["accent"]

        d.rounded_rectangle([x * SS, y * SS, (x + TILE_W) * SS, (y + TILE_H) * SS],
                            radius=16 * SS, fill=PANEL, outline=EDGE, width=2 * SS)

        pill_w = width(s["tag"], TAG_SIZE) + 24
        pill_top = y + 15
        d.rounded_rectangle([(x + PAD) * SS, pill_top * SS,
                             (x + PAD + pill_w) * SS, (pill_top + PILL_H) * SS],
                            radius=(PILL_H // 2) * SS, fill=a)
        draw_text(d, x + PAD + 12, pill_top + 25, s["tag"], TAG_SIZE, BG)

        ICONS[s["icon"]](Frame(d, x + TILE_W - PAD - ICON, y + 12, ICON), a)

        b2 = y + TILE_H - 49
        b1 = b2 - 55
        draw_text(d, x + PAD, b1, s["lines"][0], LABEL_SIZE, INK)
        draw_text(d, x + PAD, b2, s["lines"][1], LABEL_SIZE, INK)

    return img.resize((SIZE, SIZE), Image.LANCZOS)


def main() -> int:
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render().save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes, {SIZE}x{SIZE})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
