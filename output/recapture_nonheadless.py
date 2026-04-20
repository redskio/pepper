# -*- coding: utf-8 -*-
"""
CleverTap 스크린샷 재캡처 — non-headless + stealth 모드
headless=False로 실제 브라우저 환경 사용
"""
import sys, io, asyncio
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")
ASSETS.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

TARGETS = [
    ("analytics_v5",      "https://clevertap.com/product/analytics/",    1200),
    ("segmentation_v5",   "https://clevertap.com/product/segmentation/",  1000),
    ("ab_testing_v5",     "https://clevertap.com/product/ab-testing/",    1000),
    ("orchestration_v5",  "https://clevertap.com/product/journeys/",       800),
    ("product_overview_v5","https://clevertap.com/product/",               600),
]


async def dismiss_overlays(page):
    for sel in [
        'button:has-text("Accept")',
        'button:has-text("Accept All")',
        '#onetrust-accept-btn-handler',
    ]:
        try:
            el = page.locator(sel).first
            if await el.is_visible():
                await el.click()
                await page.wait_for_timeout(500)
                break
        except:
            pass
    await page.evaluate("""
        () => {
            ['[class*="cookie"]','[id*="cookie"]','[id*="onetrust"]',
             'iframe[src*="chat"]','[class*="intercom"]'].forEach(sel => {
                document.querySelectorAll(sel).forEach(el => el.style.display = 'none');
            });
        }
    """)


async def slow_scroll_and_back(page, target_y: int):
    """천천히 스크롤해서 lazy load 트리거 후 target_y 위치로 복귀"""
    # 전체 높이 파악
    total_h = await page.evaluate("document.body.scrollHeight")
    print(f"  page_height={total_h}px, target={target_y}px")

    # 천천히 아래로
    pos = 0
    while pos < min(target_y + 1440, total_h):
        await page.evaluate(f"window.scrollTo(0, {pos})")
        await page.wait_for_timeout(200)
        pos += 300

    await page.wait_for_timeout(1500)

    # target_y 위치로
    await page.evaluate(f"window.scrollTo(0, {target_y})")
    await page.wait_for_timeout(2000)


async def capture(page, name: str, url: str, target_y: int):
    print(f"\n[{name}] {url}")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(2000)
        await dismiss_overlays(page)
        await slow_scroll_and_back(page, target_y)
        await dismiss_overlays(page)

        # 전체 높이 다시 체크
        total_h = await page.evaluate("document.body.scrollHeight")
        print(f"  final page_height={total_h}px")

        out_path = ASSETS / f"screenshot_{name}.png"
        await page.screenshot(
            path=str(out_path),
            clip={"x": 0, "y": 0, "width": 1280, "height": 720}
        )
        size = out_path.stat().st_size // 1024
        print(f"  -> {out_path.name} ({size}KB)")
        return str(out_path)
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-web-security",
            ]
        )
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=UA,
            locale="en-US",
            timezone_id="America/New_York",
        )
        # stealth: navigator.webdriver 숨기기
        await ctx.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        """)
        page = await ctx.new_page()

        for name, url, target_y in TARGETS:
            await capture(page, name, url, target_y)

        await browser.close()

    print("\n=== 완료 ===")
    for f in sorted(ASSETS.glob("*_v5.png")):
        print(f"  {f.name}: {f.stat().st_size//1024}KB")


if __name__ == "__main__":
    asyncio.run(main())
