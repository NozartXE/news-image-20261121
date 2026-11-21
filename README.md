# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/NozartXE/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/NozartXE/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image that sums up the world news of Saturday 21 November 2026: a
date-as-masthead front page with one dominant hero (COP31 running into
overtime), a second hero (five Houthi missiles downed over Riyadh and
Jizan), a figure strip of the day's key numbers — each figure appearing
exactly once in the story text — ten more stories as drawn scene-cards
(led by the Peru quake, its seismograph trace drawn heavy enough to
read at 480 px), and the rest of the day as one-line briefs. 40 stories,
every illustrated story pure 21-November news; a DATE CHECK panel lists
the 19–20 November items that were deliberately excluded, and the
validator fails the build if any excluded story is printed anywhere on
the page.

The picture is drawn by a deterministic engine (`engine/`, Pillow): a
validated content file goes in, a byte-identical 1024×1024 PNG comes
out. The validator refuses to draw a page whose accounting breaks —
story counts, scene counts, region counts, or a figure repeated outside
its one allowed place.

## Run it

```sh
python3 build.py                # validates, draws entry.png + entry-480.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png — a whole PNG, 1024x1024, under the 1 MiB gate
```

## Sources

Reuters · Al Jazeera · Dawn · AFP · Dunya News · USGS/IGP · AP · CAAP ·
RTL · The Economic Times · CoinGecko (Bitcoin 02:08 UTC).
