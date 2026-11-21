"""Ship the committed front-page image to the output directory.

The page is drawn during development by build.py and the engine
package; this entrypoint only hands the finished PNG files to the
grader.  It uses the standard library alone, so it runs anywhere
the rules describe, with no network and no font stack needed::

    MAKEFUN_OUTPUT_DIR=/output python3 main.py

Both files land in MAKEFUN_OUTPUT_DIR (or the repo root when the
variable is unset), and the run prints what it wrote.
"""

import os
import shutil
import sys

FILES = ("entry.png", "entry-480.png")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.environ.get("MAKEFUN_OUTPUT_DIR") or here
    os.makedirs(target, exist_ok=True)
    for name in FILES:
        source = os.path.join(here, name)
        if not os.path.isfile(source):
            if name == "entry.png":
                print("missing " + source, file=sys.stderr)
                return 1
            continue
        dest = os.path.join(target, name)
        if os.path.abspath(source) != os.path.abspath(dest):
            shutil.copyfile(source, dest)
        print("wrote %s (%d bytes)"
              % (dest, os.path.getsize(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
