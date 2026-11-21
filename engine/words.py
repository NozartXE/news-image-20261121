"""Font cache and greedy line breaking for the front page.

Every measurement on the page goes through these two helpers so a
headline, a brief and a validator probe all agree on how wide a
string is at a given size.
"""

from PIL import ImageFont

_loaded = {}


def get_font(path, size):
    """Return the cached TrueType font for (path, size)."""
    key = (path, size)
    if key not in _loaded:
        _loaded[key] = ImageFont.truetype(path, size)
    return _loaded[key]


def text_w(draw, text, face):
    """Advance width of ``text`` in ``face`` on ``draw``."""
    return draw.textlength(text, font=face)


def wrap_lines(draw, text, face, max_w):
    """Greedy word wrap of ``text`` to lines no wider than ``max_w``."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if text_w(draw, trial, face) <= max_w or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_size(draw, text, path, top_size, min_size, max_w):
    """Largest size in [min_size, top_size] at which ``text`` fits."""
    size = top_size
    while size > min_size and text_w(draw, text,
                                     get_font(path, size)) > max_w:
        size -= 1
    return size
