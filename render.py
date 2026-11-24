#!/usr/bin/env python3
"""Render page.html to entry.png at 1024x1024.

deviceScaleFactor=2, then downscale to 1024x1024 with LANCZOS. Keeps the
file under 1 MiB.
"""

import asyncio
import pathlib

from PIL import Image
from playwright.async_api import async_playwright

CHROME = "/opt/data/profiles/idea/cache/pw-browsers/chromium-1248/chrome-linux64/chrome"
ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "page.html"
OUT = ROOT / "entry.png"


async def shoot(tmp: pathlib.Path) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME)
        page = await browser.new_page(viewport={"width": 1024, "height": 1024},
                                      device_scale_factor=2)
        await page.goto(PAGE.as_uri())
        await page.wait_for_timeout(350)
        await page.screenshot(path=str(tmp), clip={"x": 0, "y": 0, "width": 1024, "height": 1024})
        await browser.close()


def downscale(tmp: pathlib.Path) -> None:
    with Image.open(tmp) as im:
        if im.size != (1024, 1024):
            im = im.resize((1024, 1024), Image.LANCZOS)
        else:
            im = im.convert("RGB")
        im = im.convert("RGB") if im.mode != "RGB" else im
        im.save(OUT, format="PNG", optimize=True)


def main() -> None:
    tmp = ROOT / ".entry-2x.png"
    asyncio.run(shoot(tmp))
    downscale(tmp)
    tmp.unlink(missing_ok=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
