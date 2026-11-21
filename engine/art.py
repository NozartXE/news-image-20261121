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
    """COP31 plenary: a packed hall, the big screen carrying the
    draft cut, the speaker at the podium, rows of delegates."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(30, 58, 48))
    # ceiling lights
    for i in range(9):
        lx = x + w * (0.06 + 0.11 * i)
        draw.ellipse([lx, y + h * 0.03, lx + 7, y + h * 0.03 + 7],
                     fill=(244, 196, 84))
    # banner
    bw = w * 0.16
    draw.rectangle([x + (w - bw) / 2, y + h * 0.10,
                    x + (w + bw) / 2, y + h * 0.20], fill=(20, 44, 34))
    draw.text((x + w * 0.5 - 26, y + h * 0.115), "COP31",
              font=get_font(C.SANS_BOLD, 15), fill=(244, 196, 84))
    # the screen and its message, larger so the middle of the
    # frame is not empty hall
    sx0, sy0, sx1, sy1 = x + w * 0.30, y + h * 0.22, x + w * 0.70, \
        y + h * 0.64
    draw.rectangle([sx0, sy0, sx1, sy1], fill=(20, 20, 20))
    draw.rectangle([sx0 + 3, sy0 + 3, sx1 - 3, sy1 - 3],
                   fill=(240, 238, 228))
    draw.text((x + w * 0.40, y + h * 0.30), "144→80",
              font=get_font(C.SANS_BOLD, 26), fill=C.ACCENT)
    draw.text((x + w * 0.36, y + h * 0.50), "DRAFT PARAGRAPHS",
              font=get_font(C.SANS_BOLD, 10), fill=(60, 56, 50))
    # side panels with flags
    for fx in (0.03, 0.90):
        draw.rectangle([x + w * fx, y + h * 0.22, x + w * (fx + 0.07),
                        y + h * 0.64], fill=(24, 60, 44))
        draw.ellipse([x + w * (fx + 0.02), y + h * 0.36,
                      x + w * (fx + 0.05), y + h * 0.46],
                     fill=(244, 196, 84))
    # speaker at the podium, in front of the screen's lower edge
    px = x + w * 0.5
    _person(draw, px, y + h * 0.72, h * 0.16, (34, 38, 60), (60, 56, 52))
    draw.rectangle([px - w * 0.07, y + h * 0.72, px + w * 0.07,
                    y + h * 0.82], fill=(96, 72, 46))
    draw.rectangle([px - w * 0.07, y + h * 0.72, px + w * 0.07,
                    y + h * 0.75], fill=(140, 104, 62))
    # three rows of delegates, denser towards the back
    rows = [(0.82, 0.05, 14), (0.88, 0.07, 12), (0.94, 0.09, 10)]
    hairs = [(30, 28, 26), (60, 44, 30), (200, 200, 200), (18, 18, 18),
             (120, 90, 60)]
    suits = [(52, 58, 74), (84, 60, 52), (66, 52, 76), (44, 66, 58)]
    for ry, rr, count in rows:
        for i in range(count):
            hx = x + w * (0.04 + 0.92 * i / max(count - 1, 1))
            _head(draw, hx, y + h * ry, h * rr, hairs[i % len(hairs)])
            top = y + h * ry + h * rr * 0.8
            bot = y + h - 1
            if top < bot:
                draw.rectangle([hx - h * rr * 1.6, top,
                                hx + h * rr * 1.6, bot],
                               fill=suits[i % len(suits)])


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
            draw.rectangle([tx0 + 3, y + h * (0.98 - hh + 0.08 + 0.12 * wy),
                            tx0 + 8, y + h * (0.98 - hh + 0.12 + 0.12 * wy)],
                           fill=(244, 196, 84))
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
    # three intercept bursts
    for bx, by in ((0.30, 0.42), (0.52, 0.38), (0.72, 0.40)):
        cx, cy = x + w * bx, y + h * by
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            draw.line([cx, cy, cx + 12 * math.cos(a),
                       cy + 12 * math.sin(a)], fill=(255, 240, 170),
                      width=2)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4],
                     fill=(255, 240, 170))
    # searchlight beams from the rooftops
    for bx in (0.18, 0.62):
        draw.polygon([(x + w * bx, y + h * 0.95), (x + w * (bx - 0.06),
                      y + h * 0.30), (x + w * (bx - 0.02), y + h * 0.30)],
                     fill=(240, 230, 170))


def paint_seismo(img, draw, box, story):
    """The Peru quake as a seismograph drum: a long paper strip
    carrying one thick jagged trace, mountains below, the trace
    drawn heavy enough to read at 480 px."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(240, 236, 224))
    # drum edges
    draw.rectangle([x, y, x + w, y + h * 0.10], fill=(120, 110, 96))
    draw.rectangle([x, y + h * 0.90, x + w, y + h], fill=(120, 110, 96))
    # paper grid
    for gx in range(1, 12):
        draw.line([x + w * gx / 12, y + h * 0.10, x + w * gx / 12,
                   y + h * 0.90], fill=(214, 206, 190))
    # the trace: flat, then a violent burst, then settling.
    # Mountains are drawn first so the trace stays fully visible.
    draw.polygon([(x, y + h), (x + w * 0.18, y + h * 0.72),
                  (x + w * 0.34, y + h), (x + w * 0.55, y + h * 0.66),
                  (x + w * 0.72, y + h), (x + w * 0.88, y + h * 0.76),
                  (x + w, y + h)], fill=(96, 104, 116))
    draw.line([x + w * 0.62, y + h * 0.90, x + w * 0.66, y + h * 0.78,
               x + w * 0.63, y + h * 0.70], fill=(60, 56, 50), width=2)
    pts = []
    n = 48
    for i in range(n + 1):
        fx = i / n
        if fx < 0.30:
            fy = 0.50 + 0.02 * math.sin(i * 1.7)
        elif fx < 0.62:
            fy = 0.50 + (0.34 if i % 2 else -0.30) * (
                1.0 - abs(fx - 0.46) / 0.20)
        else:
            fy = 0.50 + 0.05 * math.sin(i * 2.3) * (1 - (fx - 0.62) / 0.38)
        pts.append((x + w * fx, y + h * fy))
    draw.line(pts, fill=(158, 32, 28), width=4, joint="curve")


def paint_march(img, draw, box, story):
    """Gen Z march: three dense rows of heads, placards on sticks,
    a row of flags above the crowd."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(214, 206, 190))
    # flags along the top
    flag_cols = [(158, 32, 28), (30, 90, 160), (52, 116, 56),
                 (240, 200, 60), (158, 32, 28)]
    for i, col in enumerate(flag_cols):
        fx = x + w * (0.08 + 0.18 * i)
        draw.rectangle([fx, y + h * 0.04, fx + 2, y + h * 0.30],
                       fill=(60, 56, 50))
        draw.rectangle([fx + 2, y + h * 0.04, fx + w * 0.10,
                        y + h * 0.16], fill=col)
    # placards, kept below the label chip's top band
    for px, txt in ((0.16, "25"), (0.52, "FUTURE"), (0.80, "NOW")):
        draw.rectangle([x + w * px, y + h * 0.44, x + w * px + 2,
                        y + h * 0.62], fill=(60, 56, 50))
        draw.rectangle([x + w * (px - 0.06), y + h * 0.32,
                        x + w * (px + 0.08), y + h * 0.46],
                       fill=(248, 244, 236), outline=(24, 22, 20))
        draw.text((x + w * (px - 0.04), y + h * 0.35), txt,
                  font=get_font(C.SANS_BOLD, 9), fill=(24, 22, 20))
    # three rows of heads, back rows smaller and denser
    rows = [(0.52, 0.075, 9), (0.68, 0.095, 8), (0.86, 0.115, 7)]
    hairs = [(30, 28, 26), (60, 44, 30), (18, 18, 18), (120, 90, 60)]
    skins = [SKIN, SKIN_D, (214, 170, 130)]
    for ry, rr, count in rows:
        for i in range(count):
            hx = x + w * (0.05 + 0.90 * i / max(count - 1, 1))
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


def paint_ashes(img, draw, box, story):
    """Perth day one: the pitch, the bowler in green and gold
    mid-delivery, the stumps, a scoreboard carrying 7/58."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=GRASS)
    draw.rectangle([x, y, x + w, y + h * 0.30], fill=(120, 170, 120))
    # pitch strip
    draw.rectangle([x + w * 0.34, y + h * 0.30, x + w * 0.66, y + h],
                   fill=(214, 196, 150))
    # scoreboard panel; the figure chip on top carries 7/58
    draw.rectangle([x + w * 0.70, y + h * 0.05, x + w * 0.97,
                    y + h * 0.30], fill=(20, 20, 24))
    # stumps at the near end
    for i in range(3):
        draw.rectangle([x + w * (0.46 + 0.02 * i), y + h * 0.82,
                        x + w * (0.48 + 0.02 * i), y + h * 0.94],
                       fill=(240, 220, 140))
    # bowler in green and gold, arm high
    bx = x + w * 0.20
    _person(draw, bx, y + h * 0.80, h * 0.42, (20, 90, 50), (30, 26, 22))
    draw.line([bx + w * 0.02, y + h * 0.42, bx + w * 0.10,
               y + h * 0.28], fill=SKIN, width=3)
    draw.ellipse([bx + w * 0.10, y + h * 0.26, bx + w * 0.10 + 5,
                  y + h * 0.26 + 5], fill=(200, 40, 36))
    # batsman at the far end, small
    _person(draw, x + w * 0.50, y + h * 0.52, h * 0.20,
            (240, 240, 234), (28, 28, 30))
    # boundary rope
    draw.line([x, y + h * 0.97, x + w, y + h * 0.97],
              fill=(240, 240, 230), width=2)


def paint_bat(img, draw, box, story):
    """Wellington: the batsman from behind on the strip, the
    Basin Reserve stand behind, a scoreboard carrying 124*."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=GRASS)
    # stand: roof band and crowd dots
    draw.rectangle([x, y, x + w, y + h * 0.26], fill=(70, 74, 90))
    for i in range(14):
        cx = x + w * (0.04 + 0.065 * i)
        draw.rectangle([cx, y + h * 0.14, cx + 3, y + h * 0.17],
                       fill=((240, 200, 60), (240, 240, 230),
                             (200, 60, 50))[i % 3])
    draw.rectangle([x, y + h * 0.26, x + w, y + h * 0.30],
                   fill=(240, 240, 230))
    # pitch strip
    draw.rectangle([x + w * 0.36, y + h * 0.30, x + w * 0.64, y + h],
                   fill=(214, 196, 150))
    # scoreboard panel; the figure chip on top carries 124*
    draw.rectangle([x + w * 0.70, y + h * 0.05, x + w * 0.97,
                    y + h * 0.28], fill=(20, 20, 24))
    # batsman from behind, white, bat down
    bx = x + w * 0.50
    _person(draw, bx, y + h * 0.86, h * 0.48, (238, 238, 234),
            (28, 28, 30))
    draw.line([bx + w * 0.03, y + h * 0.55, bx + w * 0.10, y + h * 0.86],
              fill=(190, 160, 110), width=4)
    draw.ellipse([bx + w * 0.11, y + h * 0.86, bx + w * 0.11 + 5,
                  y + h * 0.86 + 5], fill=(200, 40, 36))
    # stumps
    for i in range(3):
        draw.rectangle([x + w * (0.46 + 0.02 * i), y + h * 0.88,
                        x + w * (0.48 + 0.02 * i), y + h * 0.97],
                       fill=(240, 220, 140))


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
    # flag at half-mast
    draw.rectangle([x + w * 0.86, y + h * 0.05, x + w * 0.87,
                    y + h * 0.78], fill=(60, 56, 50))
    draw.rectangle([x + w * 0.87, y + h * 0.08, x + w * 0.98,
                    y + h * 0.20], fill=(178, 40, 40))
    draw.rectangle([x + w * 0.87, y + h * 0.08, x + w * 0.90,
                    y + h * 0.20], fill=(240, 240, 230))
    # stamped document on the steps
    draw.rectangle([x + w * 0.08, y + h * 0.80, x + w * 0.34,
                    y + h * 0.96], fill=(248, 246, 240),
                   outline=(24, 22, 20))
    draw.ellipse([x + w * 0.13, y + h * 0.83, x + w * 0.29,
                  y + h * 0.93], outline=(158, 32, 28), width=2)
    draw.text((x + w * 0.16, y + h * 0.85), "VOID",
              font=get_font(C.SANS_BOLD, 8), fill=(158, 32, 28))


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
    """Texas: a cell wall, heavy bars, a small high window and a
    clock counting the 63 minutes."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], fill=(140, 132, 118))
    draw.rectangle([x, y + h * 0.78, x + w, y + h], fill=(96, 90, 80))
    # high window
    draw.rectangle([x + w * 0.68, y + h * 0.10, x + w * 0.92,
                    y + h * 0.30], fill=(30, 40, 60))
    draw.rectangle([x + w * 0.68, y + h * 0.10, x + w * 0.92,
                    y + h * 0.30], outline=(240, 240, 230), width=2)
    draw.line([x + w * 0.80, y + h * 0.10, x + w * 0.80, y + h * 0.30],
              fill=(240, 240, 230), width=2)
    # the clock
    cx, cy, r = x + w * 0.26, y + h * 0.34, h * 0.24
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=(248, 246, 240), outline=(24, 22, 20), width=2)
    draw.line([cx, cy, cx, cy - r * 0.7], fill=(24, 22, 20), width=2)
    draw.line([cx, cy, cx + r * 0.6, cy + r * 0.2],
              fill=(158, 32, 28), width=2)
    draw.text((x + w * 0.12, y + h * 0.60), "63 MIN",
              font=get_font(C.SANS_BOLD, 11), fill=(24, 22, 20))
    # bars across the whole cell
    for i in range(6):
        bx = x + w * (0.06 + 0.16 * i)
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


PAINTERS = {
    "plenary": paint_plenary,
    "missilenight": paint_missilenight,
    "seismo": paint_seismo,
    "march": paint_march,
    "runway": paint_runway,
    "ashes": paint_ashes,
    "bat": paint_bat,
    "storm": paint_storm,
    "expel": paint_expel,
    "capsize": paint_capsize,
    "cell": paint_cell,
    "tankers": paint_tankers,
}

LABELS = {
    "plenary": ("COP31 · ANTALYA", "left"),
    "missilenight": ("RIYADH", "right"),
    "seismo": ("6.7", "right"),
    "march": ("25 COUNTRIES", "left"),
    "runway": ("146 SAFE", "right"),
    "ashes": ("7/58", "right"),
    "bat": ("124*", "right"),
    "storm": ("114 KM/H", "left"),
    "expel": ("EXPELLED", "right"),
    "capsize": ("4 DEAD", "left"),
    "cell": ("63 MIN", "right"),
    "tankers": ("KHARG", "left"),
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
