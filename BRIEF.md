# BUILD BRIEF — "The World Daily", front page for Tuesday 24 November 2026

Write two files in this repository: `page.html` and `main.py`. Then render `page.html` to
`entry.png`.

## Why this version exists

A previous version of this page failed an objective test. An AI judge looks at the finished
image at roughly **300 pixels across**, not 1024. Every element must therefore survive a
3.41x shrink. The old page measured, in pixels of the 1024-wide render:

| element | px @1024 | px @300 | outcome |
|---|---|---|---|
| masthead | 94 | 27.5 | fine |
| date | 34 | 10.0 | fine |
| lead headline | 66 | 19.3 | fine |
| deck | 26 | 7.6 | marginal |
| lead body | 19.5 | 5.7 | grey mush |
| chart caption | 13 | 3.8 | grey mush |
| section kicker | 15 | 4.4 | grey mush |
| secondary headline | 41 | 12.0 | fine |
| secondary body | 18 | 5.3 | grey mush |
| briefs | 17 | 5.0 | grey mush |
| footer | 15 | 4.4 | grey mush |

The fix is not to shrink copy — it is to **cut words and grow type**. At 300px this page must
read as: one enormous name, one enormous headline, a strong picture, two clear secondary
headlines, two clear one-line briefs.

## Hard type floors — every one is checked, none may be waived

At the 1024-wide render, measured with `getComputedStyle().fontSize`:

- masthead: **>= 100px**
- date line: **>= 34px**
- lead headline: **>= 78px**
- deck (one line only): **>= 30px**
- any lead body copy you keep: **>= 26px**, and at most two sentences total
- chart axis / legend / caption text: **>= 20px**
- kicker labels above the secondary stories: **>= 26px**
- secondary headlines: **>= 44px**
- brief lines: **>= 30px**
- footer: **>= 24px**

If a line will not fit at these sizes, **delete words** until it does. Do not reduce type to
make words fit. A headline of four words at 80px beats a headline of nine words at 55px.

## Content (real events of 23-24 November 2026, use exactly these)

- Lead — Markets: **"Chips Lead a Broad Rally"**. Nvidia reinstated Jensen Huang, driving a
  broad semiconductor rally. Show S&P 500 +1.8% and Nasdaq +2.6% as a hand-written inline SVG
  chart (no external images), and make the chart large: a clear block roughly 420px wide and
  300px tall, not a small inset.
- Secondary 1 — Africa: the corvette **Merkury**, a Russian warship, sank at Benghazi, Libya.
- Secondary 2 — Asia: the **ICJ** delivered its ruling on the Rohingya genocide case.
- Brief 1 — Climate: the annual UN climate summit closed without an agreed final text; Pacific
  nations said the failure left them without promised finance.
- Brief 2 — Middle East: Trump said he may resume strikes on Iran after the new year if talks
  fail; in Israel Gadi Eisenkot said Iran poses no immediate threat before a government forms.

Each brief is **one line**. If the full sentence will not fit at 30px across 944px of measure,
shorten the wording until it does — keep the facts, drop the clauses.

## Layout

- Masthead "The World Daily" at the top, centred, white-space nowrap.
- Date line beneath it: "Tuesday 24 November 2026", dark red, bold serif.
- A thin double rule under the date line (a thick top border and a thin bottom border on a
  short empty div).
- Lead block filling the upper half: big headline, one-line deck, then a two-column split of
  (a) at most two sentences of body copy with a drop cap and (b) the large SVG chart.
- Below that, a rule, then two secondary stories side by side, equal widths, separated by a
  thin vertical hairline. Each has a red kicker (AFRICA / ASIA), a big headline, and at most
  one short sentence.
- Below those, a rule, then the two briefs as single lines, each led by a red tag
  (CLIMATE / MIDDLE EAST) and an em dash.
- Footer at the very bottom: "The World Daily · Tuesday 24 November 2026 · page one".

Palette: near-black ink `#15130f`, warm off-white paper `#f5f0e3`, one dark-red accent
`#8c1a11`. Serif (Georgia) for display type, clean sans (Helvetica/Arial) for body.

## Hard constraints

- The whole page must fit in exactly 1024x1024 CSS pixels with **no scrolling** and **no text
  below y=1014**. Measure this; do not guess.
- All graphics must be inline SVG you author. No external fonts, no network requests, no raster
  images anywhere in the HTML.
- Self-contained single HTML file.
- `entry.png` must be a PNG, exactly 1024x1024, under 1048576 bytes.

## main.py

A Python program that copies `entry.png` from the repository root into the directory named by
the `MAKEFUN_OUTPUT_DIR` environment variable (default `/output`). Deterministic: two runs
produce byte-identical results. With `--check` it verifies the PNG is at most 1048576 bytes and
at most 1024x1024 pixels, prints the byte count, the dimensions and a short sha256, and exits 1
on failure. Standard library plus Pillow only.

## Rendering

Render `page.html` to `entry.png` at 1024x1024 with Playwright, using the Chromium at
`/opt/data/profiles/idea/cache/pw-browsers/chromium-1248/chrome-linux64/chrome`. Render at
`deviceScaleFactor=2` and downscale to 1024x1024 (LANCZOS). Keep the file under 1 MiB.

## Steps you must actually perform

1. Write `page.html`.
2. Write `measure.py` that loads the page in Chromium at 1024x1024 and prints, for each of the
   selectors `.masthead`, `.dateline`, `.lead-head`, `.deck`, `.lead-copy p`, any chart `text`,
   `.kicker`, `.sub-head`, `.story p`, `.brief`, `footer`: its computed fontSize, that size
   times 300/1024, and its bounding box. Also print `document.documentElement.scrollWidth` and
   `scrollHeight` and the lowest text baseline.
3. Run it. Every type floor in this brief must pass, and nothing may sit below y=1014. If any
   floor fails, **edit the page and re-run** until all pass. Do not report success before the
   numbers are pasted from a real run.
4. Write `main.py`, render `entry.png`, and run
   `MAKEFUN_OUTPUT_DIR=/tmp/mfout python3 main.py --check` until it prints OK.
5. Report the final measured table (element, px@1024, px@300), the lowest text y, and the PNG
   byte count — copied from the actual runs, not from memory.

Do not stop until `entry.png` exists, `main.py --check` passes, and the measurement table shows
every floor met.
