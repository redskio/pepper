# -*- coding: utf-8 -*-
"""
CleverTap 이미지 재캡처 — product 메인 페이지 섹션 캡처
clevertap.com/product/ 가 정상 로드됨 (7265px)
전체 페이지를 캡처한 후 섹션별로 클립
"""
import sys, io, asyncio
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")
ASSETS.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# (name, url, scroll_y_list) — scroll_y_list: 캡처할 Y 위치들
CAPTURES = [
    # Product 메인 (7265px) — 여러 섹션
    ("product_s1",   "https://clevertap.com/product/",   [300, 800, 1300, 1800, 2400, 3000, 3600, 4200]),
    # 솔루션/고객 페이지들도 시도
    ("solutions_fintech", "https://clevertap.com/solutions/fintech/",      [300, 800, 1400]),
    ("solutions_ecomm",   "https://clevertap.com/solutions/e-commerce/",   [300, 800, 1400]),
    ("customers_page",    "https://clevertap.com/customers/",              [300, 800]),
    ("pricing_page",      "https://clevertap.com/pricing/",                [300, 600, 1000]),
    ("blog_analytics",    "https://clevertap.com/blog/mobile-app-analytics/", [400, 1000]),
]


async def dismiss_overlays(page):
    for sel in ['button:has-text("Accept")', 'button:has-text("Accept All")', '#onetrust-accept-btn-handler']:
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


async def load_page_fully(page, url: str):
    """페이지 로드 + 전체 스크롤로 lazy loading 트리거"""
    await page.goto(url, wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(3000)
    await dismiss_overlays(page)

    # 천천히 전체 스크롤
    total_h = await page.evaluate("document.body.scrollHeight")
    pos = 0
    while pos < total_h:
        await page.evaluate(f"window.scrollTo(0, {pos})")
        await page.wait_for_timeout(150)
        pos += 400

    await page.wait_for_timeout(2000)
    total_h = await page.evaluate("document.body.scrollHeight")
    print(f"  page_height={total_h}px")
    return total_h


async def capture_at_y(page, name: str, y: int):
    """지정 Y 위치에서 뷰포트 캡처"""
    await page.evaluate(f"window.scrollTo(0, {y})")
    await page.wait_for_timeout(800)
    await dismiss_overlays(page)
    out_path = ASSETS / f"screenshot_{name}_y{y}.png"
    await page.screenshot(path=str(out_path), clip={"x": 0, "y": 0, "width": 1280, "height": 720})
    size = out_path.stat().st_size // 1024
    print(f"  [{y}px] -> {out_path.name} ({size}KB)")
    return str(out_path)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=UA,
            locale="en-US",
        )
        await ctx.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)
        page = await ctx.new_page()

        for name, url, y_list in CAPTURES:
            print(f"\n=== {name} :: {url} ===")
            try:
                h = await load_page_fully(page, url)
                for y in y_list:
                    if y < h:
                        await capture_at_y(page, name, y)
                    else:
                        print(f"  [{y}px] 건너뜀 (page_height={h}px)")
            except Exception as e:
                print(f"  [ERROR] {e}")

        await browser.close()

    print("\n=== 완료 ===")
    files = sorted(ASSETS.glob("screenshot_*_y*.png"))
    for f in files:
        print(f"  {f.name}: {f.stat().st_size//1024}KB")
    print(f"총 {len(files)}개 캡처")


if __name__ == "__main__":
    asyncio.run(main())
