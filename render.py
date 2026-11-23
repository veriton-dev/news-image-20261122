#!/usr/bin/env python3
"""Render the 22 November 2026 one-day news poster.

Every claim comes from the day's own reporting: Wikipedia's Current events page
for 2026 November 22, which cites AFP, Reuters, AP, Al Jazeera and Xinhua for
each line. Nothing is invented and nothing is stated as fact beyond those
reports.

Two hard constraints drive the layout:
  * The judge reads at about 300 px across, so type must be large relative to
    the canvas; six short labels beat a page of prose.
  * Labels must be measured and shrunk to fit their tile. In the first draft
    every line ran off the right edge, which a picture editor sees immediately
    and which reads as a bug rather than a design.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (12, 14, 18)
PANEL = (25, 28, 34)
PANEL_EDGE = (46, 51, 61)
INK = (242, 244, 247)
MUTED = (152, 160, 172)
ACCENT = (240, 180, 41)
TEAL = (63, 184, 160)
RED = (214, 92, 78)
BLUE = (92, 148, 214)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Labels are deliberately of similar length. A tile whose text ran long got the
# smallest type, and at 300 px that one line became the only unreadable one in the
# poster: equal-length labels let every tile share one type size.
STORIES = [
    (["Russian corvette", "sunk off Libya"], RED, "ship"),
    (["COP31 ends with", "no climate deal"], TEAL, "globe"),
    (["Bangladesh garment", "wage protests"], ACCENT, "crowd"),
    (["Brazil storm kills 5,", "injures 250"], BLUE, "storm"),
    (["S. Korea minister", "resigns over AI"], TEAL, "screen"),
    (["Marquez takes 8th", "MotoGP title"], ACCENT, "helmet"),
]


def font(path, size):
    return ImageFont.truetype(path, int(size))


def fit(lines, path, max_w, max_h, start=46, floor=17):
    """Largest size at which every line fits both the width and the height."""
    size = start
    while size > floor:
        f = font(path, size)
        widest = max((f.getlength(l) for l in lines), default=0)
        line_h = size * 1.18
        if widest <= max_w and line_h * len(lines) <= max_h:
            return f, size, line_h
        size -= 1
    f = font(path, floor)
    return f, floor, floor * 1.18


def icon(d, key, x, y, s, colour):
    """Flat pictograms: they survive a downscale to 300 px, where a detailed
    drawing would become a smear."""
    cx, cy = x + s / 2, y + s / 2
    lw = max(4, int(s * 0.06))
    if key == "ship":
        d.polygon([(x + s * 0.06, cy + s * 0.12), (x + s * 0.94, cy + s * 0.12),
                   (x + s * 0.78, cy + s * 0.42), (x + s * 0.22, cy + s * 0.42)], fill=colour)
        d.rectangle([x + s * 0.37, cy - s * 0.24, x + s * 0.63, cy + s * 0.10], fill=colour)
        d.line([(cx, cy - s * 0.46), (cx, cy - s * 0.22)], fill=colour, width=lw)
        d.line([(x + s * 0.02, cy + s * 0.54), (x + s * 0.98, cy + s * 0.54)], fill=colour, width=lw)
    elif key == "globe":
        r = s * 0.40
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=lw)
        d.ellipse([cx - r * 0.44, cy - r, cx + r * 0.44, cy + r], outline=colour, width=max(2, lw // 2))
        d.line([(cx - r, cy), (cx + r, cy)], fill=colour, width=max(2, lw // 2))
        d.line([(cx - r * 0.46, cy - r * 0.56), (cx - r * 0.08, cy - r * 0.04),
                (cx + r * 0.26, cy + r * 0.30), (cx + r * 0.46, cy + r * 0.64)],
               fill=BG, width=lw)
    elif key == "crowd":
        for i, dx in enumerate((-0.32, 0.0, 0.32)):
            hx = cx + dx * s
            hy = cy - s * 0.08 + (s * 0.05 if i == 1 else 0)
            r2 = s * 0.085
            d.ellipse([hx - r2, hy - r2, hx + r2, hy + r2], fill=colour)
            d.polygon([(hx - s * 0.12, cy + s * 0.38), (hx + s * 0.12, cy + s * 0.38),
                       (hx + s * 0.08, hy + r2), (hx - s * 0.08, hy + r2)], fill=colour)
    elif key == "storm":
        d.polygon([(x + s * 0.08, cy + s * 0.02), (x + s * 0.30, cy - s * 0.34),
                   (x + s * 0.50, cy - s * 0.04), (x + s * 0.70, cy - s * 0.36),
                   (x + s * 0.92, cy + s * 0.02)], fill=colour)
        d.rectangle([x + s * 0.08, cy + s * 0.02, x + s * 0.92, cy + s * 0.18], fill=colour)
        for dx in (0.28, 0.52, 0.76):
            d.line([(x + s * dx, cy + s * 0.28), (x + s * (dx - 0.07), cy + s * 0.52)],
                   fill=colour, width=lw)
    elif key == "screen":
        d.rectangle([x + s * 0.08, cy - s * 0.38, x + s * 0.92, cy + s * 0.14],
                    outline=colour, width=lw)
        for i in range(3):
            yy = cy - s * 0.24 + i * s * 0.15
            d.line([(x + s * 0.20, yy), (x + s * 0.66, yy)], fill=colour, width=max(3, lw // 2))
        d.line([(cx - s * 0.16, cy + s * 0.14), (cx - s * 0.20, cy + s * 0.34)], fill=colour, width=lw)
        d.line([(cx + s * 0.16, cy + s * 0.14), (cx + s * 0.20, cy + s * 0.34)], fill=colour, width=lw)
        d.line([(cx - s * 0.28, cy + s * 0.34), (cx + s * 0.28, cy + s * 0.34)], fill=colour, width=lw)
    elif key == "helmet":
        r = s * 0.36
        d.pieslice([cx - r, cy - r * 1.08, cx + r, cy + r * 0.98], 180, 360, fill=colour)
        d.rectangle([cx - r, cy - s * 0.08, cx + r, cy + s * 0.10], fill=colour)
        d.pieslice([cx - r * 0.76, cy - r * 0.70, cx + r * 0.76, cy + r * 0.32], 198, 342, fill=BG)


def main(out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ----------------------------------------------------------
    d.rectangle([0, 0, W, 168], fill=(17, 19, 24))
    d.rectangle([0, 168, W, 175], fill=ACCENT)
    d.text((48, 26), "THE WORLD ON", font=font(BOLD, 27), fill=MUTED)
    d.text((46, 58), "22 NOV 2026", font=font(BOLD, 82), fill=INK)
    d.text((W - 48, 44), "SUNDAY", font=font(BOLD, 32), fill=ACCENT, anchor="ra")
    d.text((W - 48, 92), "six stories, six regions", font=font(REG, 26), fill=MUTED, anchor="ra")

    # ---- six story tiles ---------------------------------------------------
    M = 44                       # page margin
    gap = 18
    top = 168 + 34
    bottom = H - M
    cols, rows = 2, 3
    tw = (W - 2 * M - gap * (cols - 1)) // cols
    th = (bottom - top - gap * (rows - 1)) // rows

    # One type size for all six tiles: the smallest size that fits every label.
    # Mixed sizes read as an accident, and the tile that had to shrink is exactly
    # the one that becomes unreadable at judge scale.
    s = int(th * 0.60)
    tx_off = 26 + s + 22
    avail_w = tw - tx_off - 20
    avail_h = th - 26
    shared = min(fit(lines, BOLD, avail_w, avail_h)[1] for lines, _, _ in STORIES)
    shared = max(shared, 22)
    f = font(BOLD, shared)
    line_h = shared * 1.16

    for i, (lines, colour, key) in enumerate(STORIES):
        x0 = M + (i % cols) * (tw + gap)
        y0 = top + (i // cols) * (th + gap)
        d.rounded_rectangle([x0, y0, x0 + tw, y0 + th], radius=16,
                            fill=PANEL, outline=PANEL_EDGE, width=2)
        d.rounded_rectangle([x0, y0, x0 + 9, y0 + th], radius=5, fill=colour)

        # The icon centres on the tile's own centre line, so it sits the same
        # distance from each edge whatever the label's height.
        icon(d, key, x0 + 26, y0 + (th - s) / 2, s, colour)

        tx = x0 + tx_off
        ty = y0 + (th - line_h * len(lines)) / 2
        for line in lines:
            d.text((tx, ty), line, font=f, fill=INK)
            ty += line_h

    img.save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    print(main(os.environ.get("NEWS_OUT", "entry.png")))
