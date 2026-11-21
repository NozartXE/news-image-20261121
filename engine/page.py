"""Page composition for the one-image front page.

The page is a stack of horizontal bands whose heights sum to the
1024 px canvas::

    kicker 24 + date 90 + figure strip 48 + hero row 300
    + cards 260 + index 240 + date check 42 + footer 20 = 1024

Stories are placed by tier: two heroes (a wide lead and a narrower
second), ten cards in two rows — the lead card spans two columns so
the quake seismograph reads at any size — and the rest as numbered
one-line briefs in a four-column index.  The date check names the
off-date mega-stories the page deliberately excludes.
"""

import json
import os

from PIL import Image, ImageDraw

from . import art, colours as C
from .words import fit_size, get_font, text_w, wrap_lines

MARGIN = 16
PAGE = 1024
CONTENT = 992
RIGHT = MARGIN + CONTENT

KICKER_H = 24
DATE_H = 90
STRIP_H = 48
HERO_H = 300
CARDS_H = 260
INDEX_H = 240
CHECK_H = 42
FOOTER_H = 20

HERO_SCENE_H = 190
HERO1_W = 655
HERO_GAP = 10
HERO2_W = CONTENT - HERO1_W - HERO_GAP

CARD_SCENE_H = 72
CARD_ROW_H = 130
CARD_GUTTER = 3
ROW1_WIDTHS = [395, 196, 196, 196]
ROW2_WIDTHS = [163, 163, 163, 163, 163, 162]

REGION_ORDER = ["Asia", "Middle East", "Europe", "Americas", "Africa",
                "Oceania", "Global"]

STRIP = [
    ("6.7", "PERU QUAKE MAGNITUDE"),
    ("$58,983", "BITCOIN −3.9% · 02:08 UTC"),
    ("124*", "RAHUL · WELLINGTON"),
    ("7/58", "STARC · PERTH"),
    ("146", "SAFE · DAVAO LANDING"),
    ("144→80", "COP31 DRAFT CUT"),
]

CHECK_LEAD = "DATE CHECK — NOT TODAY: "
CHECK_L1 = (
    "Wall Street correction (20 Nov) · Poland missile "
    "(overnight 20→21 Nov) · UK–EU deal (20 Nov) · Akvan "
    "landfall (20 Nov)"
)
CHECK_L2 = (
    "BepiColombo at Mercury (20 Nov) · ICJ Myanmar ruling "
    "(19 Nov) · GTA VI launch (19 Nov)"
)


def region_counts(stories):
    """Counts per region in REGION_ORDER, skipping empty regions."""
    counts = {r: 0 for r in REGION_ORDER}
    for s in stories:
        counts[s["region"]] += 1
    return [(r, counts[r]) for r in REGION_ORDER if counts[r]]


def compute_stats(data):
    """Counts the content file derives every printed number from."""
    stories = data["stories"]
    by_tier = lambda t: [s for s in stories if s.get("tier") == t]
    counts = region_counts(stories)
    return {
        "stories": len(stories),
        "illustrated": len([s for s in stories if s.get("scene")]),
        "heroes": len(by_tier("hero")),
        "cards": len(by_tier("card")),
        "index": len(by_tier("index")),
        "regions": len(counts),
        "region_counts": counts,
    }


def _kicker(draw, stats):
    face = get_font(C.SANS_BOLD, 12)
    draw.text((MARGIN, 6), "ONE DAY OF WORLD NEWS, ONE PICTURE",
              font=face, fill=C.INK)
    scope = "%d STORIES · %d REGIONS · %d ILLUSTRATED" % (
        stats["stories"], stats["regions"], stats["illustrated"])
    draw.text((RIGHT - text_w(draw, scope, face), 6), scope,
              font=face, fill=C.ACCENT)


def _masthead(draw, data):
    size = fit_size(draw, data["date_line"], C.SERIF_BOLD, 64, 40,
                    CONTENT)
    face = get_font(C.SERIF_BOLD, size)
    draw.text((MARGIN, KICKER_H + 12), data["date_line"], font=face,
              fill=C.INK)
    draw.rectangle([MARGIN, KICKER_H + DATE_H - 8, RIGHT,
                    KICKER_H + DATE_H - 5], fill=C.INK)


def _strip(draw, y):
    fig_face = get_font(C.SERIF_BOLD, 24)
    lab_face = get_font(C.SANS_BOLD, 9)
    cell = CONTENT / len(STRIP)
    for i, (figure, label) in enumerate(STRIP):
        cx = MARGIN + int(i * cell)
        if i:
            draw.line([cx - 1, y + 5, cx - 1, y + 41], fill=C.HAIRLINE)
        draw.text((cx + 4, y + 3), figure, font=fig_face, fill=C.ACCENT)
        draw.text((cx + 4, y + 32), label, font=lab_face, fill=C.FAINT)
    draw.line([MARGIN, y + STRIP_H - 1, RIGHT, y + STRIP_H - 1],
              fill=C.HAIRLINE)


def _chips(draw, x, y, counts):
    """Region chips: REGIONS: followed by one boxed count per region."""
    lead = get_font(C.SANS_BOLD, 8)
    chip = get_font(C.SANS_BOLD, 8)
    draw.text((x, y + 2), "REGIONS:", font=lead, fill=C.ACCENT)
    cx = x + int(text_w(draw, "REGIONS:", lead)) + 7
    for region, count in counts:
        label = "%s %d" % (region.upper(), count)
        bb = draw.textbbox((0, 0), label, font=chip)
        cw = bb[2] + 10
        draw.rectangle([cx, y, cx + cw, y + 13], outline=C.FAINT, width=1)
        draw.text((cx + 5, y + 2), label, font=chip, fill=C.FAINT)
        cx += cw + 5
    return cx


def _hero_text(draw, story, x, w, y_top, counts=None):
    kick = get_font(C.SANS_BOLD, 10)
    head = get_font(C.SERIF_BOLD, 19)
    dek = get_font(C.SANS, 13)
    ty = y_top
    draw.text((x, ty), "%s · %s" % (story["place"],
              story["kicker_date"]), font=kick, fill=C.ACCENT)
    ty += 14
    for line in wrap_lines(draw, story["headline"], head, w):
        draw.text((x, ty), line, font=head, fill=C.INK)
        ty += 21
    for line in wrap_lines(draw, story["dek"], dek, w):
        draw.text((x, ty), line, font=dek, fill=C.SOFT)
        ty += 15
    if counts:
        _chips(draw, x, ty + 4, counts)
        ty += 17
    return ty


def _heroes(draw, img, heroes, counts, y):
    first, second = heroes
    box1 = (MARGIN, y, HERO1_W, HERO_SCENE_H)
    box2 = (MARGIN + HERO1_W + HERO_GAP, y, HERO2_W, HERO_SCENE_H)
    art.paint_scene(img, draw, box1, first)
    art.paint_scene(img, draw, box2, second)
    text_y = y + HERO_SCENE_H + 2
    _hero_text(draw, first, MARGIN, HERO1_W, text_y, counts=counts)
    _hero_text(draw, second, MARGIN + HERO1_W + HERO_GAP, HERO2_W,
               text_y)


def _num_box(draw, x, y, num):
    """Black box sized to the numeral, story number in white bold."""
    face = get_font(C.SANS_BOLD, 8)
    label = str(num)
    bb = draw.textbbox((0, 0), label, font=face)
    w = bb[2] + 6 + (3 if len(label) == 1 else 0)
    draw.rectangle([x, y, x + w, y + 11], fill=C.INK)
    draw.text((x + (w - bb[2]) // 2 - bb[0], y + 2), label, font=face,
              fill=C.PAPER)
    return w + 1


def _card(draw, img, story, x, y, w):
    box = (x, y, w, CARD_SCENE_H)
    art.paint_scene(img, draw, box, story)
    ty = y + CARD_SCENE_H + 3
    box_w = _num_box(draw, x, ty, story["num"])
    kicker = "%s · %s" % (story["place"], story["kicker_date"])
    ksize = fit_size(draw, kicker, C.SANS_BOLD, 9, 7,
                     w - box_w - 3)
    draw.text((x + box_w + 3, ty), kicker,
              font=get_font(C.SANS_BOLD, ksize), fill=C.ACCENT)
    ty += 13
    head = get_font(C.SANS_BOLD, 13)
    for line in wrap_lines(draw, story["headline"], head, w):
        draw.text((x, ty), line, font=head, fill=C.INK)
        ty += 14
    dsize = fit_size(draw, story["dek"], C.SANS, 11, 8, w)
    draw.text((x, ty), story["dek"], font=get_font(C.SANS, dsize),
              fill=C.SOFT)


def _cards(draw, img, cards, y):
    row1, row2 = cards[:4], cards[4:]
    cx = MARGIN
    for story, w in zip(row1, ROW1_WIDTHS):
        _card(draw, img, story, cx, y, w)
        cx += w + CARD_GUTTER
    cx = MARGIN
    for story, w in zip(row2, ROW2_WIDTHS):
        _card(draw, img, story, cx, y + CARD_ROW_H, w)
        cx += w + CARD_GUTTER


def _index(draw, briefs, y):
    head = get_font(C.SANS_BOLD, 12)
    draw.text((MARGIN, y + 4), "MORE OF THE DAY — %d STORIES"
              % len(briefs), font=head, fill=C.INK)
    note = "12 ILLUSTRATED ABOVE"
    note_face = get_font(C.SANS, 10)
    draw.text((RIGHT - text_w(draw, note, note_face), y + 5), note,
              font=note_face, fill=C.FAINT)
    draw.line([MARGIN, y + 18, RIGHT, y + 18], fill=C.INK)
    brief_face = get_font(C.SANS_BOLD, 12)
    col_w = CONTENT // 4
    row_h = 31
    for idx, story in enumerate(briefs):
        col, row = divmod(idx, 7)
        cx = MARGIN + col * col_w
        cy = y + 22 + row * row_h
        draw.rectangle([cx, cy, cx + 26, cy + 13], fill=C.INK)
        draw.text((cx + 3, cy + 1), "%d." % story["num"],
                  font=brief_face, fill=C.PAPER)
        ly = cy
        for line in wrap_lines(draw, story["brief"], brief_face, 210)[:2]:
            draw.text((cx + 30, ly), line, font=brief_face, fill=C.INK)
            ly += 14


def _date_check(draw, y):
    draw.rectangle([MARGIN, y, RIGHT, y + CHECK_H - 2],
                   outline=C.ACCENT, width=1)
    lead = get_font(C.SANS_BOLD, 9)
    body = get_font(C.SANS, 9)
    tx = MARGIN + 6
    lead_w = text_w(draw, CHECK_LEAD.rstrip(), lead)
    draw.text((tx, y + 7), CHECK_LEAD, font=lead, fill=C.INK)
    draw.text((tx + int(lead_w) + 4, y + 7), CHECK_L1, font=body,
              fill=C.INK)
    draw.text((tx, y + 19), CHECK_L2, font=body, fill=C.INK)


def _footer(draw, data, y):
    seen = []
    for story in data["stories"]:
        for src in story.get("sources") or []:
            if src not in seen:
                seen.append(src)
    text = "SOURCES: " + " · ".join(seen) + " · Drawn in code"
    draw.text((MARGIN, y + 4), text, font=get_font(C.SANS, 7),
              fill=C.FAINT)


def build_page(data):
    """Render the full front page from the content dict."""
    img = Image.new("RGB", (PAGE, PAGE), C.PAPER)
    draw = ImageDraw.Draw(img)
    stats = compute_stats(data)
    stories = sorted(data["stories"], key=lambda s: s["num"])
    heroes = [s for s in stories if s["tier"] == "hero"]
    cards = [s for s in stories if s["tier"] == "card"]
    briefs = [s for s in stories if s["tier"] == "index"]

    y = 0
    _kicker(draw, stats)
    y += KICKER_H
    _masthead(draw, data)
    y += DATE_H
    _strip(draw, y)
    y += STRIP_H
    _heroes(draw, img, heroes, stats["region_counts"], y)
    y += HERO_H
    _cards(draw, img, cards, y)
    y += CARDS_H
    _index(draw, briefs, y)
    y += INDEX_H
    _date_check(draw, y)
    y += CHECK_H
    _footer(draw, data, y)
    y += FOOTER_H
    assert y == PAGE, y
    return img


def load_content(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def default_content_path(base_dir):
    return os.path.join(base_dir, "content", "content-20261121.json")
