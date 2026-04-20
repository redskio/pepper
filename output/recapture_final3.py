# -*- coding: utf-8 -*-
"""올바른 URL로 3개 이미지 최종 캡처"""
import asyncio, sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

TARGETS = [
    # Analytics — /product/ scroll=2800 (Customer Data and Analytics 섹션)
    ("ctx_analytics",  "https://clevertap.com/product/",              2800, "Analytics UI"),
    # A/B Testing — 올바른 URL
    ("ctx_ab",         "https://clevertap.com/experiment-optimization/", 500, "A/B Testing 히어로"),
    ("ctx_ab_mid",     "https://clevertap.com/experiment-optimization/", 1000, "A/B Testing mid"),
    # Fintech — 올바른 URL
    ("ctx_fintech",    "https://clevertap.com/financial-services/",    0,   "Fintech 히어로"),
    ("ctx_fintech_mid","https://clevertap.com/financial-services/",    600, "Fintech mid"),
]

async def capture(page, name, url, scroll_y, desc):
    print(f"  [{name}] {desc}: scroll={scroll_y}")
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2.5)
        if scroll_y > 0:
            await page.evaluate(f"window.scrollTo(0, {scroll_y})")
            await asyncio.sleep(1.5)
        path = ASSETS / f"{name}.png"
        await page.screenshot(path=str(path),
                               clip={"x": 0, "y": 0, "width": 1280, "height": 720})
        size = path.stat().st_size // 1024
        print(f"    -> {path.name} ({size}KB)")
        return True
    except Exception as e:
        print(f"    [오류] {e}")
        return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 720}, user_agent=UA)
        page = await ctx.new_page()
        for name, url, sy, desc in TARGETS:
            await capture(page, name, url, sy, desc)
        await browser.close()
    print("완료")

if __name__ == "__main__":
    asyncio.run(main())
