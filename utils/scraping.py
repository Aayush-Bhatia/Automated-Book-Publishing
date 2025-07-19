

import os
import asyncio
from playwright.async_api import async_playwright

#folders exist
os.makedirs("assets/screenshots", exist_ok=True)
os.makedirs("assets/raw_text", exist_ok=True)

async def scrape_chapter(url: str, screenshot_path: str, text_path: str) -> str | None:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            print(f"🌐 Navigating to: {url}")
            await page.goto(url, timeout=60000)

            await page.wait_for_selector("div#bodyContent")

            # Screenshot
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"-- Screenshot saved → {screenshot_path}")

            # Get text
            chapter_text = await page.inner_text("div#bodyContent")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(chapter_text)
            print(f"-- Text saved → {text_path}")

            await browser.close()
            return chapter_text

    except Exception as e:
        print(f"-- Scraping Error: {e}")
        return None
