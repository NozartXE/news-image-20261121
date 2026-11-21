"""Development build: validate the content, render the page, and
write ``entry.png`` plus a 480 px preview next to it.

The render is deterministic: the same content file always produces
the same bytes, so the script renders twice and refuses to finish
unless both renders hash identically.  Run from the repo root::

    python3 build.py
"""

import hashlib
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import gate, page


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def build(base_dir=None):
    base = base_dir or os.path.dirname(os.path.abspath(__file__))
    data = page.load_content(page.default_content_path(base))
    summary, ok = gate.report(data)
    print("gate:", summary)
    if not ok:
        return 1
    first = page.build_page(data)
    second = page.build_page(data)
    import io
    buf1, buf2 = io.BytesIO(), io.BytesIO()
    first.save(buf1, format="PNG")
    second.save(buf2, format="PNG")
    if buf1.getvalue() != buf2.getvalue():
        print("render is not deterministic", file=sys.stderr)
        return 1
    png_path = os.path.join(base, "entry.png")
    with open(png_path, "wb") as fh:
        fh.write(buf1.getvalue())
    small = first.resize((480, 480), Image.LANCZOS)
    small_path = os.path.join(base, "entry-480.png")
    small.save(small_path, format="PNG")
    print("wrote %s %d bytes sha256=%s"
          % (png_path, len(buf1.getvalue()), _sha(png_path)))
    print("wrote %s %d bytes sha256=%s"
          % (small_path, os.path.getsize(small_path), _sha(small_path)))
    return 0


if __name__ == "__main__":
    sys.exit(build())
