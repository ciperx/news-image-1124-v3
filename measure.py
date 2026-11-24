#!/usr/bin/env python3
"""Measure page.html in Chromium at 1024x1024 and print the type table.

Prints computed fontSize, that size at 300px wide (x300/1024), and the
bounding box for every element named in the build brief, plus the document
scroll size and the lowest text baseline.
"""

import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

CHROME = "/opt/data/profiles/idea/cache/pw-browsers/chromium-1248/chrome-linux64/chrome"
PAGE = pathlib.Path(__file__).resolve().parent / "page.html"

SELECTORS = [
    ".masthead",
    ".dateline",
    ".lead-head",
    ".deck",
    ".lead-copy p",
    ".chart text",
    ".kicker",
    ".sub-head",
    ".story p",
    ".brief",
    "footer",
]

JS = """
(selectors) => {
  const out = {rows: [], scrollWidth: 0, scrollHeight: 0, lowestText: null};
  for (const sel of selectors) {
    const els = Array.from(document.querySelectorAll(sel));
    if (!els.length) { out.rows.push({sel, missing: true}); continue; }
    let size = 0, text = "";
    for (const el of els) {
      size = Math.max(size, parseFloat(getComputedStyle(el).fontSize));
    }
    const r = els[0].getBoundingClientRect();
    const rl = els[els.length - 1].getBoundingClientRect();
    out.rows.push({
      sel,
      count: els.length,
      size,
      text: els[0].textContent.trim().slice(0, 48),
      x: Math.round(r.x * 10) / 10,
      y: Math.round(r.y * 10) / 10,
      w: Math.round(r.width * 10) / 10,
      h: Math.round(r.height * 10) / 10,
      right: Math.round(rl.right * 10) / 10,
      bottom: Math.round(Math.max(...els.map(e => e.getBoundingClientRect().bottom)) * 10) / 10,
    });
  }
  out.scrollWidth = document.documentElement.scrollWidth;
  out.scrollHeight = document.documentElement.scrollHeight;

  // Lowest text baseline: walk all text nodes, use a Range for each line box.
  let lowest = 0, lowestText = "";
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    if (!node.textContent.trim()) continue;
    const range = document.createRange();
    range.selectNodeContents(node);
    for (const rect of range.getClientRects()) {
      if (rect.bottom > lowest) { lowest = rect.bottom; lowestText = node.textContent.trim().slice(0, 40); }
    }
  }
  out.lowestText = {bottom: Math.round(lowest * 10) / 10, text: lowestText};
  return out;
}
"""


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME)
        page = await browser.new_page(viewport={"width": 1024, "height": 1024})
        await page.goto(PAGE.as_uri())
        await page.wait_for_timeout(200)
        data = await page.evaluate(JS, SELECTORS)
        await browser.close()

    print(f"{'selector':<14} {'px@1024':>8} {'px@300':>7} {'x':>7} {'y':>7} "
          f"{'w':>7} {'h':>7} {'right':>7} {'bottom':>7}  text")
    print("-" * 110)
    for row in data["rows"]:
        if row.get("missing"):
            print(f"{row['sel']:<14} {'MISSING':>8}")
            continue
        n = row["count"]
        label = row["sel"] + (f" (x{n})" if n > 1 else "")
        print(f"{label:<14} {row['size']:>8.1f} {row['size'] * 300 / 1024:>7.1f} "
              f"{row['x']:>7.1f} {row['y']:>7.1f} {row['w']:>7.1f} {row['h']:>7.1f} "
              f"{row['right']:>7.1f} {row['bottom']:>7.1f}  {row['text']}")

    print("-" * 110)
    print(f"scrollWidth  = {data['scrollWidth']}")
    print(f"scrollHeight = {data['scrollHeight']}")
    lt = data["lowestText"]
    print(f"lowest text bottom = {lt['bottom']}  ({lt['text']!r})")
    print(f"lowest text below y=1014? {'YES -- FAIL' if lt['bottom'] > 1014 else 'no'}")

    floors = {
        ".masthead": 100, ".dateline": 34, ".lead-head": 78, ".deck": 30,
        ".lead-copy p": 26, ".chart text": 20, ".kicker": 26,
        ".sub-head": 44, ".story p": 26, ".brief": 30, "footer": 24,
    }
    print()
    ok = True
    for row in data["rows"]:
        if row.get("missing"):
            print(f"FLOOR {row['sel']}: MISSING -> FAIL")
            ok = False
            continue
        need = floors.get(row["sel"])
        if need is None:
            continue
        good = row["size"] >= need
        ok = ok and good
        print(f"FLOOR {row['sel']:<14} {row['size']:>6.1f} >= {need:<3} "
              f"{'PASS' if good else 'FAIL'}")
    if data["scrollWidth"] > 1024 or data["scrollHeight"] > 1024:
        print("SCROLL: FAIL")
        ok = False
    else:
        print(f"SCROLL: PASS ({data['scrollWidth']}x{data['scrollHeight']})")
    if lt["bottom"] > 1014:
        ok = False
    print("RESULT:", "ALL FLOORS PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
