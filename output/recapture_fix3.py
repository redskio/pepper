# -*- coding: utf-8 -*-
"""
Analytics, A/B Testing, Fintech 3개 재캡처 — 올바른 URL + 낮은 스크롤
"""
import asyncio, sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

# (파일명, URL, 스크롤_Y, 설명)
TARGETS = [
    # Analytics: 낮은 스크롤로 hero/product UI 잡기
    ("ctx_analytics",  "https://clevertap.com/product/customer-data-analytics/", 300, "Analytics 히어로"),
    ("ctx_analytics_b","https://clevertap.com/product/customer-data-analytics/", 700, "Analytics mid"),
    # A/B Testing: 올바른 URL
    ("ctx_ab",         "https://clevertap.com/product/experimentation-and-optimization/", 400, "A/B 테스트"),
    ("ctx_ab_b",       "https://clevertap.com/product/experimentation-and-optimization/", 900, "A/B 테스트 mid"),
    # Fintech: 올바른 URL (financial-services)
    ("ctx_fintech",    "https://clevertap.com/solutions/financial-services/",     300, "핀테크 히어로"),
    ("ctx_fintech_b",  "https://clevertap.com/solutions/financial-services/",     800, "핀테크 mid"),
]

async def capture(page, name, url, scroll_y, desc):
    print(f"  [{name}] {desc}: {url} scroll={scroll_y}")
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
    print("3개 이미지 재캡처")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=UA
        )
        page = await ctx.new_page()

        ok = 0
        for name, url, scroll_y, desc in TARGETS:
            if await capture(page, name, url, scroll_y, desc):
                ok += 1

        await browser.close()

    print(f"\n완료: {ok}/{len(TARGETS)}")

if __name__ == "__main__":
    asyncio.run(main())
