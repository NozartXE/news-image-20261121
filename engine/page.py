"""Page composition for the one-image front page.

The page is a stack of horizontal bands whose heights sum to the
1024 px canvas::

    kicker 20 + date 88 + figure strip 42 + hero row 285
    + cards 252 + map 74 + index 211 + date check 39 + footer 13 = 1024

The map band is funded by trimming band heights (index rows,
DATE CHECK to one line, hero/cards/kicker/strip/footer trims) —
never by dropping stories.  Stories are placed by tier: two heroes
(a wide lead and a narrower second), nine cards in two rows —
row 1 of 4 (the lead card widest), row 2 of 5 — and the rest as
numbered one-line briefs in a four-column index.  The date check
names the off-date mega-stories the page deliberately excludes.
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

KICKER_H = 20
DATE_H = 88
STRIP_H = 42
HERO_H = 285
CARDS_H = 252
MAP_H = 74
INDEX_H = 211
CHECK_H = 39
FOOTER_H = 13

# Index grid: four columns; a column holds eight briefs.  The
# grid starts INDEX_TOP px into the band and rows are INDEX_ROW_H
# apart; a brief's lines advance INDEX_LEAD px each.  The deepest
# brief (row 7, one line) bottoms at 20 + 7*25 + 14 = 209 px,
# inside the 211 px band — the gate measures this per brief.
INDEX_ROWS = 8
INDEX_ROW_H = 25
INDEX_TOP = 20
INDEX_LEAD = 14

HERO_SCENE_H = 190
HERO1_W = 655
HERO_GAP = 10
HERO2_W = CONTENT - HERO1_W - HERO_GAP

CARD_SCENE_H = 68
CARD_ROW_H = 126
CARD_GUTTER = 3
ROW1_WIDTHS = [395, 196, 196, 196]
ROW2_WIDTHS = [196, 196, 196, 196, 195]

REGION_ORDER = ["Asia", "Middle East", "Europe", "Americas", "Africa",
                "Oceania", "Global"]

STRIP = [
    ("6.7", "PERU QUAKE MAGNITUDE"),
    ("$58,983", "BITCOIN −3.9% · 02:08 UTC"),
    ("124*", "RAHUL · WELLINGTON"),
    ("114", "BRAZIL STORM GUSTS"),
    ("146", "SAFE · DAVAO LANDING"),
    ("144→80", "COP31 DRAFT CUT"),
]

CHECK_LEAD = "DATE CHECK — NOT TODAY: "
# Two lines naming all eight exclusions.  BepiColombo left this
# list in round 2: ESA + Wikipedia date the Mercury orbit insertion
# to 21 Nov 2026, so it is a story on this page, not an exclusion.
# The Shenzhen summit (Thu 19 Nov) takes its place.
# Round 4: the Poland missile is dated 20 Nov (the Kh-101 crashed
# during the 19→20 Nov barrage), and the Kryvyi Rih double-tap
# strike — late on Fri 20 Nov — joins the list as an exclusion.
# Round 5: uniform FULL dates plus one source tag per exclusion,
# split across the two lines (the full one-line version measures
# 1,158.9 px at 9 pt against an 836.5 px body budget, so it cannot
# fit on one line); CHECK_L2, already gate-checked for width, is
# now drawn as the second line.  Tags come from this edition's own
# dossiers: Daily Brief (Wall Street first report), Reuters
# (Poland), Kyiv Independent (Kryvyi Rih wire), GOV.UK (UK–EU
# deal), IMD (Akvan authority), The Hindu (Shenzhen trilateral),
# ICJ (Press Release 2026/27), Rockstar (GTA VI publisher).
CHECK_L1 = (
    "Wall Street (20 Nov · Daily Brief) · Poland missile "
    "(20 Nov · Reuters) · Kryvyi Rih (20 Nov · Kyiv Independent) · "
    "UK–EU deal (20 Nov · GOV.UK)"
)
CHECK_L2 = (
    "Akvan (20 Nov · IMD) · Shenzhen summit (19 Nov · The Hindu) · "
    "ICJ ruling (19 Nov · ICJ) · GTA VI (19 Nov · Rockstar)"
)


def space_note(data):
    """Title-line note for the illustrated story that has no map
    pin because it did not happen on Earth (the orbit story).
    Both the number and the place are derived from the content
    data, never hardcoded."""
    for story in data["stories"]:
        if story.get("scene") == "orbit":
            return "NO. %d IS IN SPACE: %s" % (
                story["num"], story["place"])
    return ""


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
        draw.text((cx + 4, y + 30), label, font=lab_face, fill=C.FAINT)
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
    # Per-story source tag on the kicker line (first cited source).
    src = (story.get("sources") or [""])[0]
    draw.text((x, ty), "%s · %s · %s" % (story["place"],
              story["kicker_date"], src.upper()), font=kick,
              fill=C.ACCENT)
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
    src = (story.get("sources") or [""])[0]
    kicker = "%s · %s · %s" % (story["place"], story["kicker_date"],
                               src.upper())
    ksize = fit_size(draw, kicker, C.SANS_BOLD, 9, 6,
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


def _map(draw, y, note=""):
    """WHERE IT HAPPENED band: title + original dotted-continent
    map with pins numbered to match the illustrated story numbers.
    The orbit story has no pin; ``note`` (from space_note, derived
    from the data) annotates it on the title line instead."""
    head = get_font(C.SANS_BOLD, 11)
    draw.text((MARGIN, y + 2), "WHERE IT HAPPENED — %d ILLUSTRATED "
              "STORIES, PINNED" % len(art.MAP_PINS),
              font=head, fill=C.INK)
    if note:
        note_face = get_font(C.SANS, 10)
        draw.text((RIGHT - text_w(draw, note, note_face), y + 3),
                  note, font=note_face, fill=C.FAINT)
    draw.line([MARGIN, y + 16, RIGHT, y + 16], fill=C.HAIRLINE)
    art.paint_map(draw, (MARGIN, y + 18, CONTENT, MAP_H - 20))


def _index(draw, briefs, y, stats):
    head = get_font(C.SANS_BOLD, 12)
    draw.text((MARGIN, y + 4), "MORE OF THE DAY — %d STORIES"
              % len(briefs), font=head, fill=C.INK)
    note = "%d ILLUSTRATED ABOVE" % stats["illustrated"]
    note_face = get_font(C.SANS, 10)
    draw.text((RIGHT - text_w(draw, note, note_face), y + 5), note,
              font=note_face, fill=C.FAINT)
    draw.line([MARGIN, y + 18, RIGHT, y + 18], fill=C.INK)
    # Four columns of eight rows (30 briefs); rows are INDEX_ROW_H
    # apart starting INDEX_TOP px into the band, so the deepest
    # brief bottoms inside the band (see the constants above).
    brief_face = get_font(C.SANS_BOLD, 12)
    col_w = CONTENT // 4
    for idx, story in enumerate(briefs):
        col, row = divmod(idx, INDEX_ROWS)
        cx = MARGIN + col * col_w
        cy = y + INDEX_TOP + row * INDEX_ROW_H
        draw.rectangle([cx, cy, cx + 26, cy + 13], fill=C.INK)
        draw.text((cx + 3, cy + 1), "%d." % story["num"],
                  font=brief_face, fill=C.PAPER)
        ly = cy
        for line in wrap_lines(draw, story["brief"], brief_face, 210)[:2]:
            draw.text((cx + 30, ly), line, font=brief_face, fill=C.INK)
            ly += INDEX_LEAD


def _date_check(draw, y):
    draw.rectangle([MARGIN, y, RIGHT, y + CHECK_H - 2],
                   outline=C.ACCENT, width=1)
    lead = get_font(C.SANS_BOLD, 9)
    body = get_font(C.SANS, 9)
    tx = MARGIN + 6
    lead_w = text_w(draw, CHECK_LEAD.rstrip(), lead)
    draw.text((tx, y + 8), CHECK_LEAD, font=lead, fill=C.INK)
    draw.text((tx + int(lead_w) + 4, y + 8), CHECK_L1, font=body,
              fill=C.INK)
    draw.text((tx + int(lead_w) + 4, y + 21), CHECK_L2, font=body,
              fill=C.INK)


def _footer(draw, data, y):
    seen = []
    for story in data["stories"]:
        for src in story.get("sources") or []:
            if src not in seen:
                seen.append(src)
    text = "SOURCES: " + " · ".join(seen) + " · Drawn in code"
    draw.text((MARGIN, y + 3), text, font=get_font(C.SANS, 7),
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
    _map(draw, y, space_note(data))
    y += MAP_H
    _index(draw, briefs, y, stats)
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
