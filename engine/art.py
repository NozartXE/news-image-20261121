"""Scene painters: one small flat-colour illustration per story.

Each painter takes the page image, a draw handle, its box
``(x, y, w, h)`` and the story dict.  All geometry is expressed as
fractions of the box width and height, so the same painter works in
a 655 px hero, a 395 px lead card and a 162 px small card.  The
shared frame, number badge and label chip are applied by
``paint_scene`` afterwards, so no painter can spill outside its box.
"""

import math

from . import colours as C
from .words import get_font

SKY_NIGHT = (28, 38, 66)
SEA = (44, 92, 128)
GRASS = (74, 140, 74)
SKIN = (232, 192, 158)
SKIN_D = (198, 150, 110)


def _head(draw, x, y, r, hair, skin=SKIN):
    """A round head with a hair cap, centred near (x, y)."""
    draw.ellipse([x - r, y - r, x + r, y + r], fill=skin)
    draw.pieslice([x - r, y - r, x + r, y + r], 180, 360, fill=hair)


def _person(draw, x, y, s, suit, hair, skin=SKIN):
    """A standing figure, ``s`` tall, feet at (x, y)."""
    r = s * 0.09
    draw.ellipse([x - r, y - s, x + r, y - s + 2 * r], fill=skin)
    draw.pieslice([x - r, y - s, x + r, y - s + 2 * r], 180, 360,
                  fill=hair)
    draw.rectangle([x - s * 0.16, y - s * 0.72, x + s * 0.16,
                    y - s * 0.06], fill=suit)
    draw.rectangle([x - s * 0.05, y - s * 0.72, x + s * 0.05,
                    y - s * 0.30], fill=(240, 238, 230))


def paint_plenary(img, draw, box, story):
    """COP31 plenary: a crowded Antalya hall — balcony delegates,
    a screen carrying a drawn draft motif (never a figure), a
    large speaker at a podium stacked with draft papers, and two
    delegate rows with flags and placards in the foreground."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(30, 58, 48))
    # back wall, slightly lighter, with arched windows
    draw.rectangle([x, y, x + w, y + h * 0.30], fill=(38, 72, 60))
    for i in range(5):
        ax = x + w * (0.06 + 0.19 * i)
        draw.rectangle([ax, y + h * 0.06, ax + w * 0.11,
                        y + h * 0.24], fill=(120, 150, 130))
        draw.ellipse([ax, y + h * 0.02, ax + w * 0.11,
                      y + h * 0.12], fill=(120, 150, 130))
    # flag bunting across the top
    flag_cols = [(178, 40, 40), (240, 200, 60), (30, 90, 160),
                 (52, 116, 56), (240, 240, 230)]
    for i, col in enumerate(flag_cols):
        fx = x + w * (0.10 + 0.17 * i)
        draw.polygon([(fx, y + h * 0.30), (fx + w * 0.05, y + h * 0.30),
                      (fx + w * 0.025, y + h * 0.37)], fill=col)
    # hanging lamps between the windows and the bunting
    for i in range(6):
        lx = x + w * (0.09 + 0.16 * i)
        draw.line([lx, y + h * 0.24, lx, y + h * 0.28],
                  fill=(200, 190, 160), width=1)
        draw.ellipse([lx - 3, y + h * 0.28, lx + 3, y + h * 0.28 + 5],
                     fill=(255, 226, 140))
    # balcony rail with the back delegate row behind it
    for i in range(16):
        hx = x + w * (0.03 + 0.062 * i)
        _head(draw, hx, y + h * 0.33, h * 0.045,
              (30, 28, 26) if i % 2 else (120, 90, 60))
    draw.rectangle([x, y + h * 0.36, x + w, y + h * 0.40],
                   fill=(96, 72, 46))
    for i in range(22):
        bx = x + w * (0.02 + 0.045 * i)
        draw.rectangle([bx, y + h * 0.36, bx + 2, y + h * 0.40],
                       fill=(140, 104, 62))
    # the screen: draft papers, gavel, thermometer — a drawn motif
    sx0, sy0, sx1, sy1 = x + w * 0.30, y + h * 0.42, x + w * 0.70, \
        y + h * 0.66
    draw.rectangle([sx0, sy0, sx1, sy1], fill=(20, 20, 20))
    draw.rectangle([sx0 + 3, sy0 + 3, sx1 - 3, sy1 - 3],
                   fill=(240, 238, 228))
    # stacked draft pages with text lines
    for k in range(3):
        px0 = sx0 + 10 + k * 7
        py0 = sy0 + 8 + k * 5
        draw.rectangle([px0, py0, px0 + w * 0.16, py0 + h * 0.14],
                       fill=(255, 255, 250), outline=(120, 114, 104))
        for ln in range(3):
            draw.line([px0 + 4, py0 + 5 + ln * 5,
                       px0 + w * 0.16 - 4, py0 + 5 + ln * 5],
                      fill=(120, 114, 104))
    draw.text((sx0 + w * 0.22, sy0 + h * 0.02), "DRAFT",
              font=get_font(C.SANS_BOLD, 10), fill=(158, 32, 28))
    # gavel on the screen's paper
    gx, gy = sx0 + w * 0.28, sy0 + h * 0.13
    draw.line([gx, gy, gx + 16, gy + 8], fill=(96, 72, 46), width=3)
    draw.rectangle([gx + 12, gy - 2, gx + 24, gy + 8],
                   fill=(60, 44, 30))
    # thermometer at the screen's right edge
    tx = sx1 - 12
    draw.rectangle([tx, sy0 + 6, tx + 6, sy1 - 6],
                   fill=(255, 255, 250), outline=(24, 22, 20))
    draw.rectangle([tx + 1, sy1 - 14, tx + 5, sy1 - 7],
                   fill=(178, 40, 40))
    draw.ellipse([tx - 2, sy1 - 10, tx + 8, sy1 - 1],
                 fill=(178, 40, 40))
    # side flag panels flanking the screen
    for fx, col in ((0.03, (178, 40, 40)), (0.90, (30, 90, 160))):
        draw.rectangle([x + w * fx, y + h * 0.42, x + w * (fx + 0.07),
                        y + h * 0.66], fill=(24, 60, 44))
        draw.rectangle([x + w * (fx + 0.01), y + h * 0.46,
                        x + w * (fx + 0.06), y + h * 0.58], fill=col)
        draw.ellipse([x + w * (fx + 0.025), y + h * 0.49,
                      x + w * (fx + 0.045), y + h * 0.55],
                     fill=(240, 240, 230))
    # tall vertical banners at the hall's edges
    for bx, col in ((0.005, (178, 40, 40)), (0.972, (240, 200, 60))):
        draw.rectangle([x + w * bx, y + h * 0.42, x + w * (bx + 0.02),
                        y + h * 0.88], fill=col)
    # mid delegate row with small flags on the desk
    for i in range(12):
        hx = x + w * (0.045 + 0.082 * i)
        _head(draw, hx, y + h * 0.70, h * 0.05,
              (60, 44, 30) if i % 3 else (18, 18, 18))
        draw.rectangle([hx + h * 0.05, y + h * 0.72,
                        hx + h * 0.05 + 8, y + h * 0.78],
                       fill=flag_cols[i % len(flag_cols)])
    # speaker at the podium, ~2x the old size, draft stacks on it
    px = x + w * 0.50
    _person(draw, px, y + h * 0.78, h * 0.30, (34, 38, 60),
            (60, 56, 52))
    for sx in (0.42, 0.545):
        draw.rectangle([x + w * sx, y + h * 0.74, x + w * (sx + 0.035),
                        y + h * 0.78], fill=(255, 255, 250))
        draw.line([x + w * sx + 2, y + h * 0.755,
                   x + w * (sx + 0.035) - 2, y + h * 0.755],
                  fill=(120, 114, 104))
    draw.rectangle([px - w * 0.08, y + h * 0.78, px + w * 0.08,
                    y + h * 0.90], fill=(96, 72, 46))
    draw.rectangle([px - w * 0.08, y + h * 0.78, px + w * 0.08,
                    y + h * 0.81], fill=(140, 104, 62))
    draw.text((px - 14, y + h * 0.83), "COP31",
              font=get_font(C.SANS_BOLD, 10), fill=(244, 196, 84))
    # front delegate row: heads, shoulders, desk flags, paper
    # stacks and white country nameplates on every desk
    for i in range(13):
        hx = x + w * (0.035 + 0.077 * i)
        if abs(hx - px) < w * 0.09:
            continue
        _head(draw, hx, y + h * 0.93, h * 0.055,
              (200, 200, 200) if i % 4 == 3 else
              (30, 28, 26) if i % 2 else (120, 90, 60))
        draw.rectangle([hx - h * 0.06, y + h * 0.955,
                        hx + h * 0.06, y + h - 1],
                       fill=((52, 58, 74), (84, 60, 52),
                             (66, 52, 76), (44, 66, 58))[i % 4])
        draw.rectangle([hx - h * 0.06, y + h * 0.90,
                        hx - h * 0.06 + 7, y + h * 0.95],
                       fill=flag_cols[i % len(flag_cols)])
        draw.rectangle([hx + h * 0.02, y + h * 0.945,
                        hx + h * 0.10, y + h * 0.975],
                       fill=(248, 246, 240))
        draw.rectangle([hx - h * 0.11, y + h * 0.955,
                        hx - h * 0.07, y + h * 0.985],
                       fill=(255, 255, 250))
    # press cameras on tripods at both front corners
    for cx in (x + w * 0.015, x + w * 0.955):
        draw.rectangle([cx, y + h * 0.80, cx + w * 0.028, y + h * 0.86],
                       fill=(16, 16, 20))
        draw.line([cx + 2, y + h * 0.86, cx - 3, y + h * 0.97],
                  fill=(16, 16, 20), width=2)
        draw.line([cx + w * 0.014, y + h * 0.86, cx + w * 0.014,
                   y + h * 0.97], fill=(16, 16, 20), width=2)
        draw.line([cx + w * 0.026, y + h * 0.86, cx + w * 0.036,
                   y + h * 0.97], fill=(16, 16, 20), width=2)


def paint_missilenight(img, draw, box, story):
    """Riyadh before dawn: skyline under a sky crossed by missile
    trails, three intercept bursts, searchlights sweeping up."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=SKY_NIGHT)
    for sx, sy in ((0.08, 0.10), (0.22, 0.06), (0.38, 0.14),
                   (0.55, 0.07), (0.71, 0.12), (0.86, 0.05),
                   (0.93, 0.18), (0.47, 0.20)):
        draw.rectangle([x + w * sx, y + h * sy, x + w * sx + 2,
                        y + h * sy + 2], fill=(220, 224, 240))
    # moon
    draw.ellipse([x + w * 0.82, y + h * 0.08, x + w * 0.90,
                  y + h * 0.20], fill=(238, 236, 222))
    # skyline: towers of varied height, one with a spire
    heights = [0.42, 0.55, 0.36, 0.62, 0.48, 0.58, 0.40, 0.52]
    for i, hh in enumerate(heights):
        tx0 = x + w * (0.02 + 0.12 * i)
        tx1 = x + w * (0.02 + 0.12 * i + 0.09)
        draw.rectangle([tx0, y + h * (0.98 - hh), tx1, y + h * 0.98],
                       fill=(16, 20, 36))
        for wy in range(3):
            for wx in range(2):
                if (i + wy + wx) % 3 == 2:
                    continue
                draw.rectangle(
                    [tx0 + 3 + wx * 8,
                     y + h * (0.98 - hh + 0.08 + 0.12 * wy),
                     tx0 + 8 + wx * 8,
                     y + h * (0.98 - hh + 0.12 + 0.12 * wy)],
                    fill=(244, 196, 84))
    # a radar dome on the second tower
    draw.pieslice([x + w * 0.155, y + h * 0.36, x + w * 0.215,
                   y + h * 0.46], 180, 360, fill=(200, 204, 216))
    # foreground rooftops: water tanks, an antenna, streetlights
    draw.rectangle([x, y + h * 0.94, x + w, y + h], fill=(10, 12, 24))
    draw.rectangle([x + w * 0.06, y + h * 0.885, x + w * 0.11,
                    y + h * 0.94], fill=(10, 12, 24))
    draw.rectangle([x + w * 0.70, y + h * 0.895, x + w * 0.76,
                    y + h * 0.94], fill=(10, 12, 24))
    draw.line([x + w * 0.86, y + h * 0.94, x + w * 0.86, y + h * 0.86],
              fill=(10, 12, 24), width=2)
    draw.line([x + w * 0.82, y + h * 0.885, x + w * 0.90, y + h * 0.885],
              fill=(10, 12, 24), width=2)
    for i in range(7):
        lx = x + w * (0.05 + 0.15 * i)
        draw.ellipse([lx - 2, y + h * 0.955, lx + 2, y + h * 0.955 + 4],
                     fill=(255, 226, 140))
    draw.polygon([(x + w * 0.50, y + h * 0.30), (x + w * 0.52,
                  y + h * 0.36), (x + w * 0.48, y + h * 0.36)],
                 fill=(16, 20, 36))
    # five missile trails arcing down from the top
    trails = [(0.10, 0.62, 0.30, 0.42), (0.30, 0.55, 0.52, 0.38),
              (0.52, 0.60, 0.72, 0.40), (0.70, 0.52, 0.86, 0.34),
              (0.88, 0.58, 0.97, 0.44)]
    for x0, y0, x1, y1 in trails:
        draw.line([x + w * x0, y + h * y0, x + w * x1, y + h * y1],
                  fill=(255, 190, 90), width=3)
        draw.ellipse([x + w * x1 - 3, y + h * y1 - 3, x + w * x1 + 3,
                      y + h * y1 + 3], fill=(255, 220, 150))
    # five intercept bursts: three large, two smaller and higher
    for bx, by, br in ((0.30, 0.42, 12), (0.52, 0.38, 12),
                       (0.72, 0.40, 12), (0.14, 0.28, 7),
                       (0.90, 0.26, 7)):
        cx, cy = x + w * bx, y + h * by
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            draw.line([cx, cy, cx + br * math.cos(a),
                       cy + br * math.sin(a)], fill=(255, 240, 170),
                      width=2)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4],
                     fill=(255, 240, 170))
    # smoke puffs drifting off the first trail
    for px, py, pr in ((0.20, 0.50, 5), (0.25, 0.46, 7),
                       (0.16, 0.55, 4)):
        draw.ellipse([x + w * px - pr, y + h * py - pr * 0.6,
                      x + w * px + pr, y + h * py + pr * 0.6],
                     fill=(150, 156, 178))
    # searchlight beams from the rooftops
    for bx in (0.18, 0.62):
        draw.polygon([(x + w * bx, y + h * 0.95), (x + w * (bx - 0.06),
                      y + h * 0.30), (x + w * (bx - 0.02), y + h * 0.30)],
                     fill=(240, 230, 170))


def paint_seismo(img, draw, box, story):
    """The Peru quake: a cracked house in the foreground, the
    seismograph drum behind it — the trace drawn heavy and the
    house large enough that both read at 480 px."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(240, 236, 224))
    # drum edges
    draw.rectangle([x, y, x + w, y + h * 0.10], fill=(120, 110, 96))
    draw.rectangle([x, y + h * 0.90, x + w, y + h], fill=(120, 110, 96))
    # paper grid
    for gx in range(1, 12):
        draw.line([x + w * gx / 12, y + h * 0.10, x + w * gx / 12,
                   y + h * 0.90], fill=(214, 206, 190))
    # mountains first so the trace stays fully visible
    draw.polygon([(x, y + h), (x + w * 0.30, y + h * 0.78),
                  (x + w * 0.45, y + h), (x + w * 0.62, y + h * 0.74),
                  (x + w * 0.78, y + h), (x + w * 0.92, y + h * 0.80),
                  (x + w, y + h)], fill=(96, 104, 116))
    # the trace: flat, then a violent burst, then settling
    pts = []
    n = 48
    for i in range(n + 1):
        fx = i / n
        if fx < 0.30:
            fy = 0.42 + 0.02 * math.sin(i * 1.7)
        elif fx < 0.62:
            fy = 0.42 + (0.30 if i % 2 else -0.26) * (
                1.0 - abs(fx - 0.46) / 0.20)
        else:
            fy = 0.42 + 0.05 * math.sin(i * 2.3) * (1 - (fx - 0.62) / 0.38)
        pts.append((x + w * fx, y + h * fy))
    draw.line(pts, fill=(158, 32, 28), width=4, joint="curve")
    # cracked house, foreground left, clear of the trace's flat run
    hx0, hx1 = x + w * 0.03, x + w * 0.24
    hy0, hy1 = y + h * 0.56, y + h * 0.94
    draw.rectangle([hx0, hy0 + h * 0.12, hx1, hy1],
                   fill=(196, 170, 130))
    # roof, split and slipped by the quake
    draw.polygon([(hx0 - 3, hy0 + h * 0.12),
                  (hx0 + (hx1 - hx0) * 0.42, hy0),
                  (hx0 + (hx1 - hx0) * 0.62, hy0 + h * 0.12)],
                 fill=(150, 60, 50))
    draw.polygon([(hx0 + (hx1 - hx0) * 0.60, hy0 + h * 0.02),
                  (hx0 + (hx1 - hx0) * 0.95, hy0 + h * 0.12),
                  (hx1 + 3, hy0 + h * 0.12)],
                 fill=(120, 48, 40))
    # the crack: a zigzag from roof to ground
    cx = hx0 + (hx1 - hx0) * 0.55
    draw.line([(cx, hy0 + h * 0.02), (cx - 4, hy0 + h * 0.16),
               (cx + 3, hy0 + h * 0.24), (cx - 3, hy0 + h * 0.32),
               (cx + 2, hy1)], fill=(24, 22, 20), width=2)
    # tilted door and a broken window
    draw.rectangle([hx0 + (hx1 - hx0) * 0.12, hy0 + h * 0.20,
                    hx0 + (hx1 - hx0) * 0.34, hy1], fill=(52, 44, 36))
    draw.rectangle([hx0 + (hx1 - hx0) * 0.62, hy0 + h * 0.16,
                    hx0 + (hx1 - hx0) * 0.84, hy0 + h * 0.28],
                   fill=(60, 70, 90))
    draw.line([hx0 + (hx1 - hx0) * 0.62, hy0 + h * 0.16,
               hx0 + (hx1 - hx0) * 0.84, hy0 + h * 0.28],
              fill=(24, 22, 20), width=2)
    # ground crack and fallen rubble
    draw.line([x + w * 0.26, y + h * 0.94, x + w * 0.34, y + h * 0.90,
               x + w * 0.40, y + h * 0.95], fill=(24, 22, 20), width=2)
    for tx, ty in ((0.27, 0.90), (0.31, 0.93), (0.36, 0.90)):
        draw.rectangle([x + w * tx, y + h * ty, x + w * (tx + 0.02),
                        y + h * (ty + 0.03)], fill=(150, 60, 50))


def paint_march(img, draw, box, story):
    """Gen Z march: three word-bearing placards (JOBS / RENT /
    CLIMATE — the living-cost demands the story reports), flags
    above, and three rows of heads for crowd depth — the words,
    not a repeated numeral, carry the scene."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(214, 206, 190))
    # flags along the top
    flag_cols = [(158, 32, 28), (30, 90, 160), (52, 116, 56),
                 (240, 200, 60), (158, 32, 28)]
    for i, col in enumerate(flag_cols):
        fx = x + w * (0.08 + 0.18 * i)
        draw.rectangle([fx, y + h * 0.04, fx + 2, y + h * 0.26],
                       fill=(60, 56, 50))
        draw.rectangle([fx + 2, y + h * 0.04, fx + w * 0.10,
                        y + h * 0.15], fill=col)
    # three placards on sticks, words large enough to read at
    # 480 px; the boxes start below the scene chip (which occupies
    # the top 21 px) so no placard slides under it, and the words
    # sit inside the boxes with clear air on every side
    for px, txt, size in ((0.03, "JOBS", 10), (0.35, "RENT", 10),
                          (0.66, "CLIMATE", 9)):
        draw.rectangle([x + w * (px + 0.13), y + h * 0.62,
                        x + w * (px + 0.13) + 2, y + h * 0.82],
                       fill=(60, 56, 50))
        draw.rectangle([x + w * px, y + h * 0.38, x + w * (px + 0.30),
                        y + h * 0.62], fill=(248, 244, 236),
                       outline=(24, 22, 20), width=2)
        draw.text((x + w * (px + 0.025), y + h * 0.395), txt,
                  font=get_font(C.SANS_BOLD, size), fill=(24, 22, 20))
    # crowd depth: a back row of smaller heads behind the placards,
    # then two rows of large heads below
    hairs = [(30, 28, 26), (60, 44, 30), (18, 18, 18), (120, 90, 60)]
    skins = [SKIN, SKIN_D, (214, 170, 130)]
    for i in range(9):
        hx = x + w * (0.05 + 0.90 * i / 8)
        _head(draw, hx, y + h * 0.70, h * 0.06,
              hairs[i % len(hairs)], skins[i % len(skins)])
    rows = [(0.78, 0.09, 7), (0.88, 0.09, 6)]
    hairs = [(30, 28, 26), (60, 44, 30), (18, 18, 18), (120, 90, 60)]
    skins = [SKIN, SKIN_D, (214, 170, 130)]
    for ry, rr, count in rows:
        for i in range(count):
            hx = x + w * (0.06 + 0.88 * i / max(count - 1, 1))
            _head(draw, hx, y + h * ry, h * rr, hairs[i % len(hairs)],
                  skins[i % len(skins)])
            draw.rectangle([hx - h * rr * 1.7, y + h * ry + h * rr,
                            hx + h * rr * 1.7, y + h * 0.98],
                           fill=((52, 58, 74), (84, 60, 52),
                                 (44, 66, 58), (120, 90, 60))[i % 4])


def paint_runway(img, draw, box, story):
    """Davao at night: the 767 on the runway, slides deployed,
    a fire truck's lights, passengers walking clear."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(20, 28, 52))
    for sx, sy in ((0.10, 0.12), (0.30, 0.07), (0.55, 0.14),
                   (0.78, 0.08), (0.92, 0.16)):
        draw.rectangle([x + w * sx, y + h * sy, x + w * sx + 2,
                        y + h * sy + 2], fill=(220, 224, 240))
    # runway with centre dashes
    draw.rectangle([x, y + h * 0.72, x + w, y + h], fill=(52, 54, 60))
    for i in range(8):
        draw.rectangle([x + w * (0.04 + 0.12 * i), y + h * 0.84,
                        x + w * (0.08 + 0.12 * i), y + h * 0.87],
                       fill=(240, 240, 230))
    # the jet: fuselage, tail, wing, engines
    fx0, fy = x + w * 0.06, y + h * 0.52
    draw.ellipse([fx0, fy - h * 0.10, fx0 + w * 0.62, fy + h * 0.10],
                 fill=(238, 238, 234))
    draw.polygon([(fx0 + w * 0.52, fy - h * 0.10),
                  (fx0 + w * 0.56, fy - h * 0.34),
                  (fx0 + w * 0.60, fy - h * 0.34),
                  (fx0 + w * 0.60, fy - h * 0.10)], fill=(200, 30, 40))
    draw.polygon([(fx0 + w * 0.30, fy + h * 0.06),
                  (fx0 + w * 0.44, fy + h * 0.30),
                  (fx0 + w * 0.50, fy + h * 0.30),
                  (fx0 + w * 0.40, fy + h * 0.06)], fill=(210, 210, 206))
    for ex in (0.24, 0.44):
        draw.rectangle([fx0 + w * ex, fy + h * 0.08, fx0 + w * (ex + 0.05),
                        fy + h * 0.16], fill=(120, 120, 116))
    for wx in range(6):
        draw.rectangle([fx0 + w * (0.10 + 0.07 * wx), fy - h * 0.04,
                        fx0 + w * (0.13 + 0.07 * wx), fy + h * 0.02],
                       fill=(40, 80, 130))
    # evacuation slides, two of them
    for sx in (0.30, 0.52):
        draw.polygon([(x + w * sx, fy + h * 0.08),
                      (x + w * (sx + 0.10), y + h * 0.72),
                      (x + w * (sx + 0.13), y + h * 0.72),
                      (x + w * (sx + 0.03), fy + h * 0.08)],
                     fill=(240, 200, 60))
    # fire truck with flashing light
    tx = x + w * 0.74
    draw.rectangle([tx, y + h * 0.52, tx + w * 0.18, y + h * 0.70],
                   fill=(178, 40, 40))
    draw.rectangle([tx + w * 0.02, y + h * 0.56, tx + w * 0.06,
                    y + h * 0.62], fill=(180, 220, 240))
    draw.ellipse([tx + w * 0.07, y + h * 0.46, tx + w * 0.10,
                  y + h * 0.52], fill=(255, 220, 90))
    # passengers walking clear, small figures
    for i in range(4):
        px = x + w * (0.70 + 0.06 * i)
        _person(draw, px, y + h * 0.94, h * 0.16,
                (52, 58, 74), (30, 28, 26))


def paint_bat(img, draw, box, story):
    """Wellington: one large batsman on the strip, stumps at both
    ends, the ball at the bat — no scoreboard panel, the chip
    carries 124*.  The batsman fills the frame so the scene reads
    as cricket without the headline."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=GRASS)
    # stand: roof band and crowd dots
    draw.rectangle([x, y, x + w, y + h * 0.24], fill=(70, 74, 90))
    for i in range(12):
        cx = x + w * (0.04 + 0.075 * i)
        draw.rectangle([cx, y + h * 0.13, cx + 3, y + h * 0.16],
                       fill=((240, 200, 60), (240, 240, 230),
                             (200, 60, 50))[i % 3])
    draw.rectangle([x, y + h * 0.24, x + w, y + h * 0.28],
                   fill=(240, 240, 230))
    # pitch strip
    draw.rectangle([x + w * 0.34, y + h * 0.28, x + w * 0.66, y + h],
                   fill=(214, 196, 150))
    # far stumps, small, at the top of the strip
    for i in range(3):
        draw.rectangle([x + w * (0.46 + 0.02 * i), y + h * 0.30,
                        x + w * (0.48 + 0.02 * i), y + h * 0.40],
                       fill=(240, 220, 140))
    # batsman from behind, large: white, bat down to the ball
    bx = x + w * 0.50
    _person(draw, bx, y + h * 0.94, h * 0.62, (238, 238, 234),
            (28, 28, 30))
    draw.line([bx + w * 0.03, y + h * 0.58, bx + w * 0.11, y + h * 0.94],
              fill=(190, 160, 110), width=5)
    draw.ellipse([bx + w * 0.11, y + h * 0.92, bx + w * 0.11 + 6,
                  y + h * 0.92 + 6], fill=(200, 40, 36))
    # near stumps, tall and wide, beside the batsman
    for i in range(3):
        draw.rectangle([x + w * (0.42 + 0.025 * i), y + h * 0.76,
                        x + w * (0.445 + 0.025 * i), y + h * 0.95],
                       fill=(240, 220, 140))
    draw.rectangle([x + w * 0.42, y + h * 0.75, x + w * 0.52,
                    y + h * 0.77], fill=(200, 180, 100))


def paint_storm(img, draw, box, story):
    """Tupanciretã: a black storm sky, slanting rain, a bent tree
    and a house with its roof torn half off."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(52, 58, 68))
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=(62, 88, 60))
    # cloud bank
    for cx, cy, r in ((0.20, 0.16, 0.14), (0.45, 0.10, 0.18),
                      (0.72, 0.16, 0.15), (0.88, 0.10, 0.10)):
        draw.ellipse([x + w * (cx - r), y + h * (cy - r * 0.5),
                      x + w * (cx + r), y + h * (cy + r * 0.5)],
                     fill=(36, 40, 50))
    # rain, slanting hard
    for i in range(14):
        rx = x + w * (0.03 + 0.07 * i)
        ry = y + h * (0.20 + 0.05 * (i % 4))
        draw.line([rx, ry, rx + 6, ry + 12], fill=(180, 200, 220),
                  width=2)
    # house with torn roof
    hx = x + w * 0.10
    draw.rectangle([hx, y + h * 0.58, hx + w * 0.42, y + h * 0.86],
                   fill=(196, 170, 130))
    draw.polygon([(hx - 4, y + h * 0.58), (hx + w * 0.21, y + h * 0.40),
                  (hx + w * 0.30, y + h * 0.58)], fill=(150, 60, 50))
    draw.rectangle([hx + w * 0.05, y + h * 0.64, hx + w * 0.12,
                    y + h * 0.74], fill=(60, 70, 90))
    # roof tiles scattered on the ground
    for tx, ty in ((0.56, 0.88), (0.62, 0.92), (0.68, 0.86),
                   (0.74, 0.92)):
        draw.rectangle([x + w * tx, y + h * ty, x + w * (tx + 0.04),
                        y + h * (ty + 0.03)], fill=(150, 60, 50))
    # bent tree
    draw.line([x + w * 0.82, y + h * 0.86, x + w * 0.72, y + h * 0.48],
              fill=(70, 52, 36), width=4)
    draw.ellipse([x + w * 0.62, y + h * 0.38, x + w * 0.82,
                  y + h * 0.52], fill=(44, 96, 52))


def paint_expel(img, draw, box, story):
    """Copenhagen: a columned facade, a flag at half-mast, the
    expelled diplomat's document stamped on the steps."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(186, 178, 164))
    # facade and columns
    draw.rectangle([x + w * 0.06, y + h * 0.18, x + w * 0.94,
                    y + h * 0.78], fill=(214, 206, 190))
    draw.rectangle([x + w * 0.06, y + h * 0.12, x + w * 0.94,
                    y + h * 0.20], fill=(150, 60, 50))
    for i in range(4):
        cx = x + w * (0.14 + 0.22 * i)
        draw.rectangle([cx, y + h * 0.20, cx + w * 0.06, y + h * 0.78],
                       fill=(240, 232, 214))
    # door
    draw.rectangle([x + w * 0.44, y + h * 0.48, x + w * 0.56,
                    y + h * 0.78], fill=(52, 44, 36))
    # flag at half-mast, lowered on the pole
    draw.rectangle([x + w * 0.86, y + h * 0.05, x + w * 0.87,
                    y + h * 0.78], fill=(60, 56, 50))
    draw.rectangle([x + w * 0.87, y + h * 0.28, x + w * 0.98,
                    y + h * 0.40], fill=(178, 40, 40))
    draw.rectangle([x + w * 0.87, y + h * 0.28, x + w * 0.90,
                    y + h * 0.40], fill=(240, 240, 230))
    # the departing envoy in the foreground, suitcase in hand
    _person(draw, x + w * 0.68, y + h * 0.96, h * 0.52,
            (34, 38, 60), (30, 28, 26))
    draw.rectangle([x + w * 0.76, y + h * 0.82, x + w * 0.88,
                    y + h * 0.96], fill=(96, 72, 46))
    draw.rectangle([x + w * 0.80, y + h * 0.78, x + w * 0.84,
                    y + h * 0.82], outline=(60, 44, 30), width=2)
    draw.line([x + w * 0.76, y + h * 0.89, x + w * 0.88,
               y + h * 0.89], fill=(60, 44, 30), width=2)
    # stamped document on the steps — sized so the stamp ring
    # and its VOID word stay inside the paper even in a short
    # (56 px) card scene
    draw.rectangle([x + w * 0.08, y + h * 0.72, x + w * 0.34,
                    y + h * 0.97], fill=(248, 246, 240),
                   outline=(24, 22, 20))
    draw.ellipse([x + w * 0.13, y + h * 0.78, x + w * 0.29,
                  y + h * 0.94], outline=(158, 32, 28), width=2)
    draw.text((x + w * 0.165, y + h * 0.815), "VOID",
              font=get_font(C.SANS_BOLD, 7), fill=(158, 32, 28))


def paint_capsize(img, draw, box, story):
    """Nigeria: a swell at dusk, the overturned hull, a life ring
    and a hand reaching from the water."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(52, 84, 120))
    draw.rectangle([x, y, x + w, y + h * 0.28], fill=(240, 190, 110))
    draw.ellipse([x + w * 0.72, y + h * 0.06, x + w * 0.84,
                  y + h * 0.22], fill=(255, 220, 140))
    # wave bands
    for wy in (0.42, 0.58, 0.76, 0.90):
        for i in range(5):
            cx = x + w * (0.08 + 0.20 * i)
            draw.arc([cx, y + h * wy, cx + w * 0.14, y + h * (wy + 0.10)],
                     180, 360, fill=(180, 205, 225), width=2)
    # overturned hull
    draw.polygon([(x + w * 0.12, y + h * 0.52), (x + w * 0.55,
                  y + h * 0.52), (x + w * 0.48, y + h * 0.40),
                  (x + w * 0.19, y + h * 0.40)], fill=(40, 44, 54))
    draw.rectangle([x + w * 0.12, y + h * 0.50, x + w * 0.55,
                    y + h * 0.54], fill=(150, 60, 50))
    # life ring
    draw.ellipse([x + w * 0.66, y + h * 0.60, x + w * 0.82,
                  y + h * 0.80], fill=(240, 120, 40))
    draw.ellipse([x + w * 0.70, y + h * 0.65, x + w * 0.78,
                  y + h * 0.75], fill=(52, 84, 120))
    # a hand above the water
    draw.line([x + w * 0.30, y + h * 0.62, x + w * 0.30, y + h * 0.44],
              fill=SKIN, width=4)
    draw.ellipse([x + w * 0.28, y + h * 0.40, x + w * 0.32,
                  y + h * 0.46], fill=SKIN)


def paint_cell(img, draw, box, story):
    """Texas: a cell wall, a small high window, and the clock fully
    clear of the bars — the bars run down the right side only, the
    clock sits alone on the left."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(140, 132, 118))
    draw.rectangle([x, y + h * 0.78, x + w, y + h], fill=(96, 90, 80))
    # the clock, alone on the left, nothing crossing it
    cx, cy, r = x + w * 0.27, y + h * 0.36, h * 0.26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=(248, 246, 240), outline=(24, 22, 20), width=2)
    draw.line([cx, cy, cx, cy - r * 0.7], fill=(24, 22, 20), width=2)
    draw.line([cx, cy, cx + r * 0.6, cy + r * 0.2],
              fill=(158, 32, 28), width=2)
    draw.text((x + w * 0.13, y + h * 0.66), "63 MIN",
              font=get_font(C.SANS_BOLD, 11), fill=(24, 22, 20))
    # high window behind the bars, top right
    draw.rectangle([x + w * 0.70, y + h * 0.08, x + w * 0.92,
                    y + h * 0.28], fill=(30, 40, 60))
    draw.rectangle([x + w * 0.70, y + h * 0.08, x + w * 0.92,
                    y + h * 0.28], outline=(240, 240, 230), width=2)
    draw.line([x + w * 0.81, y + h * 0.08, x + w * 0.81, y + h * 0.28],
              fill=(240, 240, 230), width=2)
    # bars down the right side only — clear of the clock
    for i in range(4):
        bx = x + w * (0.62 + 0.09 * i)
        draw.rectangle([bx, y, bx + w * 0.035, y + h], fill=(30, 28, 26))


def paint_tankers(img, draw, box, story):
    """Kharg Island: a dusk sea, three tankers riding at anchor,
    a low sun and a gull above the convoy."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h * 0.55], fill=(240, 170, 110))
    draw.ellipse([x + w * 0.68, y + h * 0.18, x + w * 0.80,
                  y + h * 0.38], fill=(255, 220, 140))
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=SEA)
    # wave lines
    for wy in (0.62, 0.74, 0.88):
        for i in range(4):
            cx = x + w * (0.05 + 0.25 * i)
            draw.arc([cx, y + h * wy, cx + w * 0.16, y + h * (wy + 0.08)],
                     180, 360, fill=(170, 196, 214), width=2)
    # three tankers, near to far
    for tx, ts in ((0.06, 1.0), (0.38, 0.72), (0.66, 0.52)):
        hx0 = x + w * tx
        hw = w * 0.28 * ts
        hy = y + h * (0.62 + 0.10 * (1 - ts))
        draw.rectangle([hx0, hy, hx0 + hw, hy + h * 0.10 * ts],
                       fill=(30, 34, 44))
        draw.rectangle([hx0 + hw * 0.62, hy - h * 0.12 * ts,
                        hx0 + hw * 0.80, hy], fill=(200, 200, 196))
        draw.rectangle([hx0 + hw * 0.70, hy - h * 0.20 * ts,
                        hx0 + hw * 0.74, hy - h * 0.12 * ts],
                       fill=(150, 60, 50))
        draw.rectangle([hx0, hy + h * 0.10 * ts, hx0 + hw,
                        hy + h * 0.12 * ts], fill=(178, 40, 40))
    # gull
    draw.arc([x + w * 0.44, y + h * 0.14, x + w * 0.50, y + h * 0.20],
             180, 360, fill=(24, 22, 20), width=2)
    draw.arc([x + w * 0.50, y + h * 0.14, x + w * 0.56, y + h * 0.20],
             180, 360, fill=(24, 22, 20), width=2)


def paint_hormuz(img, draw, box, story):
    """Strait of Hormuz at dusk, recomposed drone-first (round 7):
    the MQ-9 is the scene's primary subject — large, high in the
    sky at the right, circled by the dashed claim reticle — while
    the tanker is demoted to a small hull low at the left and the
    headlands sit low on the horizon.  The dashed ring, not a hit,
    is what the scene asserts: a claim, unconfirmed."""
    x, y, w, h = box
    # dusk sky, lighter at the top
    draw.rectangle([x, y, x + w, y + h * 0.62], fill=(240, 196, 130))
    draw.rectangle([x, y + h * 0.34, x + w, y + h * 0.62],
                   fill=(232, 176, 116))
    # small low sun centre-left, clear of chip and drone alike
    draw.ellipse([x + w * 0.295, y + h * 0.34, x + w * 0.365,
                  y + h * 0.50], fill=(255, 220, 140))
    # headlands low on the horizon: Iran left, Oman right
    draw.polygon([(x, y + h * 0.44), (x + w * 0.26, y + h * 0.58),
                  (x + w * 0.30, y + h * 0.62), (x, y + h * 0.62)],
                 fill=(96, 74, 58))
    draw.polygon([(x + w, y + h * 0.42), (x + w * 0.76, y + h * 0.57),
                  (x + w * 0.72, y + h * 0.62), (x + w, y + h * 0.62)],
                 fill=(84, 64, 50))
    # the sea below the horizon line
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    for wy in (0.74, 0.88):
        for i in range(4):
            cx = x + w * (0.05 + 0.25 * i)
            draw.arc([cx, y + h * wy, cx + w * 0.16, y + h * (wy + 0.08)],
                     180, 360, fill=(170, 196, 214), width=2)
    # the tanker, demoted: a small hull low at the left
    hx0, hy = x + w * 0.05, y + h * 0.70
    hw = w * 0.24
    draw.rectangle([hx0, hy, hx0 + hw, hy + h * 0.09], fill=(30, 34, 44))
    draw.rectangle([hx0, hy + h * 0.09, hx0 + hw, hy + h * 0.11],
                   fill=(178, 40, 40))
    draw.rectangle([hx0 + hw * 0.10, hy - h * 0.08, hx0 + hw * 0.24,
                    hy], fill=(200, 200, 196))
    # the MQ-9, primary: long straight wing spanning 30% of the
    # card, slender body, V-tail — centred high at the right, its
    # whole reticle clear of the label chip at the top left
    dx, dy = x + w * 0.72, y + h * 0.30
    draw.line([dx - w * 0.15, dy + h * 0.03, dx + w * 0.15,
               dy - h * 0.03], fill=(24, 22, 20), width=3)
    draw.line([dx - w * 0.08, dy - h * 0.08, dx + w * 0.08,
               dy + h * 0.08], fill=(24, 22, 20), width=2)
    draw.line([dx + w * 0.065, dy - h * 0.065, dx + w * 0.105,
               dy - h * 0.15], fill=(24, 22, 20), width=2)
    draw.line([dx + w * 0.065, dy - h * 0.065, dx + w * 0.12,
               dy - h * 0.05], fill=(24, 22, 20), width=2)
    draw.ellipse([dx - 4, dy - h * 0.08 - 4, dx + 4, dy - h * 0.08 + 4],
                 fill=(24, 22, 20))
    # dashed claim reticle around the drone (segments, not a ring)
    rx, ry = w * 0.175, h * 0.24
    for a0 in range(0, 360, 36):
        draw.arc([dx - rx, dy - h * 0.04 - ry, dx + rx,
                  dy - h * 0.04 + ry], a0, a0 + 20,
                 fill=(158, 32, 28), width=2)


def paint_forum(img, draw, box, story):
    """New Delhi: the SCO forum's colonnaded hall — rows of member
    flags on the lawn, delegates arriving at the steps, a banner
    over the door.  The story is the visit, not a summit table."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(226, 216, 196))
    # the hall: roof band, columns, door
    draw.rectangle([x + w * 0.30, y + h * 0.10, x + w * 0.94,
                    y + h * 0.66], fill=(214, 206, 190))
    draw.rectangle([x + w * 0.30, y + h * 0.06, x + w * 0.94,
                    y + h * 0.14], fill=(150, 60, 50))
    for i in range(3):
        cx = x + w * (0.38 + 0.20 * i)
        draw.rectangle([cx, y + h * 0.14, cx + w * 0.05,
                        y + h * 0.66], fill=(240, 232, 214))
    draw.rectangle([x + w * 0.55, y + h * 0.34, x + w * 0.69,
                    y + h * 0.66], fill=(52, 44, 36))
    # banner over the door
    draw.rectangle([x + w * 0.40, y + h * 0.18, x + w * 0.84,
                    y + h * 0.28], fill=(30, 90, 160))
    draw.text((x + w * 0.47, y + h * 0.195), "SCO FORUM",
              font=get_font(C.SANS_BOLD, 8), fill=(240, 240, 230))
    # steps
    draw.rectangle([x + w * 0.30, y + h * 0.66, x + w * 0.94,
                    y + h * 0.70], fill=(186, 178, 164))
    draw.rectangle([x + w * 0.30, y + h * 0.70, x + w * 0.94,
                    y + h * 0.74], fill=(200, 192, 178))
    # a row of member flags on poles along the left lawn
    flag_cols = [(52, 116, 56), (200, 40, 40), (30, 90, 160),
                 (240, 200, 60), (240, 140, 40)]
    for i, col in enumerate(flag_cols):
        fx = x + w * (0.04 + 0.055 * i)
        draw.rectangle([fx, y + h * 0.10, fx + 2, y + h * 0.62],
                       fill=(60, 56, 50))
        draw.rectangle([fx + 2, y + h * 0.10, fx + w * 0.045,
                        y + h * 0.20], fill=col)
    # delegates arriving at the steps
    _person(draw, x + w * 0.50, y + h * 0.94, h * 0.30,
            (34, 38, 60), (30, 28, 26))
    _person(draw, x + w * 0.76, y + h * 0.94, h * 0.30,
            (84, 60, 52), (60, 44, 30))
    draw.rectangle([x + w * 0.80, y + h * 0.84, x + w * 0.87,
                    y + h * 0.94], fill=(96, 72, 46))


def paint_orbit(img, draw, box, story):
    """Mercury: the cratered planet fills the frame, the stacked
    BepiColombo craft crosses it firing its thrusters — a first
    orbit after an eight-year voyage.  Drawn wide: this painter
    carries the 395 px lead card."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(10, 12, 22))
    # stars
    for sx, sy in ((0.05, 0.10), (0.16, 0.22), (0.30, 0.06),
                   (0.44, 0.16), (0.58, 0.08), (0.72, 0.20),
                   (0.84, 0.10), (0.94, 0.24), (0.24, 0.30),
                   (0.66, 0.30)):
        draw.rectangle([x + w * sx, y + h * sy, x + w * sx + 2,
                        y + h * sy + 2], fill=(220, 224, 240))
    # mercury: a big cratered disc, terminator shading on the right
    mx, my, mr = x + w * 0.22, y + h * 0.66, h * 0.44
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr],
                 fill=(168, 158, 146))
    draw.pieslice([mx - mr, my - mr, mx + mr, my + mr], -70, 70,
                  fill=(104, 96, 88))
    for cx, cy, cr in ((0.16, 0.52, 0.09), (0.30, 0.76, 0.06),
                       (0.08, 0.82, 0.05), (0.34, 0.46, 0.045),
                       (0.22, 0.62, 0.035)):
        ex, ey = x + w * cx, y + h * cy
        er = h * cr
        draw.ellipse([ex - er, ey - er, ex + er, ey + er],
                     outline=(120, 110, 98), width=2)
    # the craft: stacked orbiters, solar wing, dish, thruster plume
    cx0, cy0 = x + w * 0.56, y + h * 0.34
    draw.rectangle([cx0, cy0, cx0 + w * 0.10, cy0 + h * 0.16],
                   fill=(226, 226, 220))
    draw.rectangle([cx0 + w * 0.015, cy0 + h * 0.16,
                    cx0 + w * 0.085, cy0 + h * 0.26],
                   fill=(198, 198, 192))
    draw.rectangle([cx0 - w * 0.11, cy0 + h * 0.03,
                    cx0, cy0 + h * 0.13], fill=(44, 92, 168))
    draw.line([cx0 - w * 0.11, cy0 + h * 0.08, cx0, cy0 + h * 0.08],
              fill=(150, 180, 220), width=2)
    draw.ellipse([cx0 + w * 0.10, cy0 + h * 0.01,
                  cx0 + w * 0.16, cy0 + h * 0.15],
                 outline=(226, 226, 220), width=2)
    draw.polygon([(cx0 + w * 0.03, cy0 + h * 0.26),
                  (cx0 + w * 0.07, cy0 + h * 0.26),
                  (cx0 + w * 0.05, cy0 + h * 0.44)],
                 fill=(255, 190, 90))
    draw.polygon([(cx0 + w * 0.04, cy0 + h * 0.26),
                  (cx0 + w * 0.06, cy0 + h * 0.26),
                  (cx0 + w * 0.05, cy0 + h * 0.36)],
                 fill=(255, 240, 200))
    # the capture arc sweeping toward the planet
    draw.arc([x + w * 0.22, y + h * 0.02, x + w * 0.96,
              y + h * 0.80], 300, 60, fill=(244, 196, 84), width=2)


def paint_arson(img, draw, box, story):
    """Dhaka: a building burning at dusk — orange flames above
    the roof, smoke rising, a second block behind it."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(52, 58, 68))
    draw.rectangle([x, y + h * 0.82, x + w, y + h], fill=(40, 44, 52))
    # second block behind, dark
    draw.rectangle([x + w * 0.62, y + h * 0.42, x + w * 0.92,
                    y + h * 0.82], fill=(70, 66, 78))
    # the burning building
    bx0, bx1 = x + w * 0.08, x + w * 0.58
    draw.rectangle([bx0, y + h * 0.42, bx1, y + h * 0.82],
                   fill=(120, 100, 84))
    for wy in (0.50, 0.64):
        for wx in (0.14, 0.32):
            draw.rectangle([x + w * wx, y + h * wy,
                            x + w * (wx + 0.10), y + h * (wy + 0.09)],
                           fill=(240, 160, 60))
    # flames above the roof, shifted right so no flame tip
    # slides under the scene's label chip at the top left
    for fx, fh in ((0.22, 0.30), (0.35, 0.38), (0.47, 0.28)):
        draw.polygon([(x + w * fx, y + h * 0.44),
                      (x + w * (fx + 0.05), y + h * (0.44 - fh)),
                      (x + w * (fx + 0.10), y + h * 0.44)],
                     fill=(240, 140, 40))
        draw.polygon([(x + w * (fx + 0.02), y + h * 0.44),
                      (x + w * (fx + 0.05), y + h * (0.44 - fh * 0.6)),
                      (x + w * (fx + 0.08), y + h * 0.44)],
                     fill=(255, 210, 90))
    # smoke rising
    for sx, sy, r in ((0.36, 0.13, 0.07), (0.50, 0.09, 0.08),
                      (0.30, 0.18, 0.06)):
        draw.ellipse([x + w * (sx - r), y + h * (sy - r * 0.5),
                      x + w * (sx + r), y + h * (sy + r * 0.5)],
                     fill=(120, 116, 110))


# --- the map band -------------------------------------------------------

# Stylised continents as ellipses in map-local fractions (cx, cy, rx, ry).
# Tall enough to fill the band so the dot clusters read as land
# masses, not horizontal stripes.
MAP_LAND = [
    (0.130, 0.30, 0.105, 0.32),  # North America
    (0.185, 0.55, 0.045, 0.12),  # Central America
    (0.245, 0.72, 0.048, 0.24),  # South America
    (0.505, 0.20, 0.052, 0.16),  # Europe
    (0.525, 0.60, 0.060, 0.26),  # Africa
    (0.605, 0.44, 0.035, 0.10),  # Arabia
    (0.690, 0.30, 0.135, 0.26),  # Asia
    (0.780, 0.55, 0.042, 0.12),  # South-East Asia
    (0.855, 0.72, 0.052, 0.12),  # Australia
    (0.905, 0.85, 0.022, 0.06),  # New Zealand
]

# (story number, map-local x, map-local y) — pins for every
# illustrated story with a place on Earth; positions spread so
# no two pins collide even at the enlarged 480-px-proof size,
# including the Europe / Middle East cluster.  The orbit story
# (BepiColombo at Mercury) has no pin: a pin at the map's edge
# reads as planted on Earth, so the map's title line annotates
# it as in space instead (see page.space_note).
MAP_PINS = [
    (1, 0.565, 0.30),   # Antalya
    (2, 0.595, 0.46),   # Riyadh
    (3, 0.235, 0.62),   # Carhuamayo, Peru
    (4, 0.455, 0.22),   # Europe (Gen Z)
    (5, 0.800, 0.52),   # Davao
    (6, 0.690, 0.47),   # Strait of Hormuz
    (7, 0.905, 0.82),   # Wellington
    (8, 0.260, 0.75),   # Tupanciretã, Brazil
    (9, 0.500, 0.10),   # Copenhagen
    (10, 0.640, 0.33),  # Kharg Island
    (12, 0.500, 0.52),  # Nigeria
    (13, 0.755, 0.40),  # Dhaka
]

# Small continent labels for the map band (map-local fractions,
# top-left of the label).  Placed over the dot field or the ocean
# gaps, clear of every pin disc; set in bold at 7 pt so they read
# at native size without crowding the 480 px view.
MAP_LABELS = [
    (0.040, 0.06, "NORTH AMERICA"),
    (0.175, 0.82, "SOUTH AMERICA"),
    (0.408, 0.06, "EUROPE"),
    (0.420, 0.60, "AFRICA"),
    (0.700, 0.06, "ASIA"),
    (0.820, 0.82, "OCEANIA"),
]


def paint_map(draw, box):
    """Original dotted-continent map: land as a dense dot grid
    inside the stylised continent ellipses, numbered pins on top.

    Legibility is judged at the 480 px render, not at 1024: the
    dots are dark and large, and each pin is a 24 px disc with a
    2 px white halo and a 13 pt number, so a pin still reads as a
    numbered marker after the 0.469 downscale instead of
    collapsing into an anonymous dot."""
    x, y, w, h = box
    dot = (88, 84, 74)
    step = 4
    for cx, cy, rx, ry in MAP_LAND:
        x0 = int(x + w * (cx - rx))
        x1 = int(x + w * (cx + rx))
        y0 = int(y + h * (cy - ry))
        y1 = int(y + h * (cy + ry))
        for gx in range(x0, x1 + 1, step):
            for gy in range(y0, y1 + 1, step):
                nx = (gx - (x + w * cx)) / max(w * rx, 1)
                ny = (gy - (y + h * cy)) / max(h * ry, 1)
                if nx * nx + ny * ny <= 1.0:
                    draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2],
                                 fill=dot)
    lab_face = get_font(C.SANS_BOLD, 7)
    for fx, fy, label in MAP_LABELS:
        # Paper-coloured halo (the same device the pins use with
        # their white discs): labels that sit over the dark dot
        # field — NORTH AMERICA, ASIA — were dark-on-dark and
        # barely readable; the halo separates every label from
        # the dots without moving any label or pin.
        draw.text((x + w * fx, y + h * fy), label, font=lab_face,
                  fill=(52, 48, 44), stroke_width=2,
                  stroke_fill=C.PAPER)
    face = get_font(C.SANS_BOLD, 13)
    for num, fx, fy in MAP_PINS:
        px, py = x + w * fx, y + h * fy
        r = 12
        draw.ellipse([px - r - 2, py - r - 2, px + r + 2,
                      py + r + 2], fill=(255, 255, 255))
        draw.ellipse([px - r, py - r, px + r, py + r],
                     fill=C.ACCENT)
        label = str(num)
        bb = draw.textbbox((0, 0), label, font=face)
        draw.text((px - (bb[2] + bb[0]) / 2, py - (bb[3] + bb[1]) / 2
                   - 1), label, font=face, fill=(255, 255, 255))


PAINTERS = {
    "plenary": paint_plenary,
    "missilenight": paint_missilenight,
    "seismo": paint_seismo,
    "march": paint_march,
    "runway": paint_runway,
    "bat": paint_bat,
    "storm": paint_storm,
    "expel": paint_expel,
    "capsize": paint_capsize,
    "cell": paint_cell,
    "tankers": paint_tankers,
    "hormuz": paint_hormuz,
    "forum": paint_forum,
    "orbit": paint_orbit,
    "arson": paint_arson,
}

LABELS = {
    "plenary": ("COP31 · ANTALYA", "left"),
    "missilenight": ("RIYADH", "right"),
    "seismo": ("6.7", "right"),
    "march": ("25 COUNTRIES", "left"),
    "runway": ("146 SAFE", "right"),
    "bat": ("124*", "right"),
    "storm": ("114 KM/H", "left"),
    "expel": ("EXPELLED", "right"),
    "capsize": ("4 DEAD", "left"),
    "cell": ("63 MIN", "right"),
    "tankers": ("KHARG", "left"),
    "hormuz": ("MQ-9 CLAIM", "left"),
    "forum": ("SCO FORUM", "right"),
    "orbit": ("19:24 CET", "right"),
    "arson": ("ARSON", "left"),
}


def _chip(draw, box, label, side):
    """Black chip in the scene's top corner carrying a label."""
    x, y, w, h = box
    face = get_font(C.SANS_BOLD, 10)
    bb = draw.textbbox((0, 0), label, font=face)
    chip_w = bb[2] + 10
    if side == "right":
        cx1 = x + w - 4
        cx0 = cx1 - chip_w
    else:
        cx0 = x + 4
        cx1 = cx0 + chip_w
    draw.rectangle([cx0, y + 4, cx1, y + 21], fill=C.CHIP)
    draw.text((cx0 + 5, y + 7), label, font=face, fill=(245, 242, 235))


def _badge(draw, box, num):
    """Number badge in the top-left of a hero scene."""
    x, y, w, h = box
    face = get_font(C.SANS_BOLD, 10)
    label = str(num)
    bb = draw.textbbox((0, 0), label, font=face)
    bw = bb[2] + 10
    draw.rectangle([x + 5, y + 5, x + 5 + bw, y + 20], fill=C.INK)
    draw.text((x + 10, y + 7), label, font=face, fill=C.PAPER)


def paint_scene(img, draw, box, story):
    """Paint one illustrated story, then frame it and add furniture."""
    painter = PAINTERS[story["scene"]]
    x, y, w, h = box
    painter(img, draw, box, story)
    draw.rectangle([x, y, x + w, y + h], outline=C.RULE, width=1)
    if story.get("tier") == "hero":
        _badge(draw, box, story["num"])
    label, side = LABELS[story["scene"]]
    _chip(draw, box, label, side)
