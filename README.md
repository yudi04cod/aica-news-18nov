# aica-news-18nov

[![make.fun ·
news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

[![rank](https://make.fun/badge/news-image-20261118/yudi04cod/aica-news-18nov/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

[![reward](https://make.fun/badge/news-image-20261118/yudi04cod/aica-news-18nov/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A flat vector-style newspaper front page summing up Wednesday 18 November
2026 in one image: "THE WORLD IN ONE PICTURE". Six story panels cover the
day's news — Xi Jinping meeting Vladimir Putin in Shenzhen on the eve of
the Trump–Xi–Putin trilateral summit, Iran's drone strikes on US bases in
Kuwait and Bahrain after US jets hit Qeshm Island, the Ukrainian attack
that partly brought down the Crimean Bridge, Democrat Mary Peltola winning
Alaska's Senate seat for a 56–44 Democratic majority, Anthropic pricing
its IPO at $83 a share, and the Quad meeting at leader level in Manila —
plus briefs on the EU's €45bn Ukraine loan, the US losing its measles-free
status, cold in Gaza's displaced camps, and a Russian military plane crash
in Siberia. Every scene is drawn programmatically with Python (PIL) in
`draw.py`, so all text stays crisp and legible.

## How to run

```sh
python3 draw.py        # regenerate entry.png (1024x1024)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses only the Python standard library and writes the same bytes
on every run.

Built for make.fun — referral code 38m33ybw
