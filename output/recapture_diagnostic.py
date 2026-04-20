# -*- coding: utf-8 -*-
"""
페이지 스캔 — 올바른 URL과 스크롤 위치 찾기
"""
import asyncio, sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

# 각 페이지/섹션 스캔
SCAN = [
    # Product 페이지 심층 스캔 (analytics/AB 섹션 찾기)
    ("scan_prod_2000",  "https://clevertap.com/product/",  2000),
    ("scan_prod_2800",  "https://clevertap.com/product/",  2800),
    ("scan_prod_3500",  "https://clevertap.com/product/",  3500),
    ("scan_prod_4200",  "https://clevertap.com/product/",  4200),
    # Solutions 페이지 스캔
    ("scan_sol_0",      "https://clevertap.com/solutions/", 0),
    ("scan_sol_600",    "https://clevertap.com/solutions/", 600),
    ("scan_sol_1200",   "https://clevertap.com/solutions/", 1200),
    # A/B Testing 페이지 (정확한 현재 URL 시도)
    ("scan_ab_hero",    "https://clevertap.com/product/experimentation-and-optimization/", 0),
    # Analytics 페이지 시도
    ("scan_cdp_hero",   "https://clevertap.com/product/customer-data-platform/", 0),
    # Pricing 페이지 (대안 - 기능 목록 있을 수 있음)
    ("scan_pricing",    "https://clevertap.com/pricing/",  400),
]

async def capture(page, name, url, scroll_y):
    print(f"  [{name}] {url} scroll={scroll_y}")
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        if scroll_y > 0:
            await page.evaluate(f"window.scrollTo(0, {scroll_y})")
            await asyncio.sleep(1.5)
        path = ASSETS / f"{name}.png"
        await page.screenshot(path=str(path),
                               clip={"x": 0, "y": 0, "width": 1280, "height": 720})
        size = path.stat().st_size // 1024
        print(f"    -> {size}KB")
        return True
    except Exception as e:
        print(f"    [오류] {e}")
        return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 720}, user_agent=UA)
        page = await ctx.new_page()
        for name, url, sy in SCAN:
            await capture(page, name, url, sy)
        await browser.close()
    print("완료")

if __name__ == "__main__":
    asyncio.run(main())
