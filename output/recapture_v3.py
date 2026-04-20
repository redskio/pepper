# -*- coding: utf-8 -*-
"""
CleverTap 스크린샷 재캡처 v3
전략: 페이지 전체 스크롤로 lazy loading 트리거 → 핵심 섹션으로 복귀 → 캡처
"""
import sys, io, asyncio, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")
ASSETS.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"


async def lazy_scroll(page):
    """전체 페이지를 천천히 스크롤하여 lazy load 트리거"""
    height = await page.evaluate("document.body.scrollHeight")
    step = 400
    pos = 0
    while pos < height:
        await page.evaluate(f"window.scrollTo(0, {pos})")
        await page.wait_for_timeout(300)
        pos += step
    # 잠시 대기 후 높이 재체크 (동적 콘텐츠)
    await page.wait_for_timeout(1000)


async def dismiss_overlays(page):
    """쿠키 배너, 팝업, 채팅 위젯 제거"""
    for sel in [
        'button:has-text("Accept")',
        'button:has-text("Accept All")',
        'button:has-text("Reject All")',
        '#onetrust-accept-btn-handler',
        '[class*="cookie"] button',
    ]:
        try:
            el = page.locator(sel).first
            if await el.is_visible():
                await el.click()
                await page.wait_for_timeout(500)
                break
        except:
            pass
    # 채팅 위젯, 배너 DOM 숨기기
    await page.evaluate("""
        () => {
            const hide = [
                '[class*="chat"]', '[class*="intercom"]', '[class*="widget"]',
                '[class*="cookie"]', '[id*="cookie"]', '[class*="banner"]',
                '[class*="announcement"]', '[class*="notification-bar"]',
                '[id*="onetrust"]', '[class*="gdpr"]',
                'iframe[src*="intercom"]', 'iframe[src*="chat"]',
            ];
            hide.forEach(sel => {
                document.querySelectorAll(sel).forEach(el => el.style.display = 'none');
            });
        }
    """)


async def capture_at(page, name: str, url: str, target_scroll: int):
    """
    URL 로드 → lazy load 트리거 → target_scroll 위치에서 캡처
    target_scroll: 실제 캡처할 Y 위치 (뷰포트 상단 기준)
    """
    print(f"[{name}] {url} (target_scroll={target_scroll}px)")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)  # 초기 JS 실행 대기

        await dismiss_overlays(page)
        await lazy_scroll(page)  # lazy load 트리거

        # 타겟 위치로 이동
        await page.evaluate(f"window.scrollTo(0, {target_scroll})")
        await page.wait_for_timeout(2000)

        # 오버레이 재제거 (스크롤 후 다시 나타날 수 있음)
        await dismiss_overlays(page)

        out_path = ASSETS / f"screenshot_{name}.png"
        await page.screenshot(
            path=str(out_path),
            clip={"x": 0, "y": 0, "width": 1280, "height": 720}
        )
        size = out_path.stat().st_size // 1024
        print(f"  -> {out_path.name} ({size}KB)")
        return str(out_path)
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
        return None


async def capture_full_page(page, name: str, url: str):
    """전체 페이지 스크린샷 (레이아웃 파악용)"""
    print(f"[FULL] {name}")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        await dismiss_overlays(page)
        await lazy_scroll(page)
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(1000)

        out_path = ASSETS / f"full_{name}.png"
        await page.screenshot(path=str(out_path), full_page=True)
        size = out_path.stat().st_size // 1024
        height = await page.evaluate("document.body.scrollHeight")
        print(f"  -> full_{name}.png ({size}KB, page_height={height}px)")
        return height
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
        return 0


async def capture_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=UA
        )
        page = await ctx.new_page()

        # ── 먼저 전체 페이지 높이 파악 ──
        print("=== 페이지 높이 파악 (full-page) ===")
        h_analytics = await capture_full_page(page, "analytics_full", "https://clevertap.com/product/analytics/")
        h_seg = await capture_full_page(page, "segmentation_full", "https://clevertap.com/product/segmentation/")
        h_ab = await capture_full_page(page, "ab_testing_full", "https://clevertap.com/product/ab-testing/")

        print(f"\n페이지 높이: analytics={h_analytics}px, segmentation={h_seg}px, ab_testing={h_ab}px")

        # ── 제품 섹션 캡처 (페이지 중반부 — 1/3 지점) ──
        print("\n=== 제품 섹션 캡처 ===")

        # Analytics: 페이지 1/3 지점
        t_analytics = max(300, h_analytics // 4) if h_analytics > 0 else 800
        await capture_at(page, "analytics_v4", "https://clevertap.com/product/analytics/", t_analytics)

        # Segmentation: 페이지 1/3 지점
        t_seg = max(300, h_seg // 4) if h_seg > 0 else 800
        await capture_at(page, "segmentation_v4", "https://clevertap.com/product/segmentation/", t_seg)

        # A/B Testing: 페이지 1/3 지점
        t_ab = max(300, h_ab // 4) if h_ab > 0 else 800
        await capture_at(page, "ab_testing_v4", "https://clevertap.com/product/ab-testing/", t_ab)

        # ── 추가: 주요 섹션 다중 캡처 ──
        # Analytics 여러 지점
        for frac, label in [(3, "mid"), (2, "half")]:
            t = h_analytics // frac if h_analytics > 0 else 1200
            await capture_at(page, f"analytics_v4_{label}", "https://clevertap.com/product/analytics/", t)

        # Segmentation 여러 지점
        for frac, label in [(3, "mid"), (2, "half")]:
            t = h_seg // frac if h_seg > 0 else 1200
            await capture_at(page, f"segmentation_v4_{label}", "https://clevertap.com/product/segmentation/", t)

        # A/B Testing 여러 지점
        for frac, label in [(3, "mid"), (2, "half")]:
            t = h_ab // frac if h_ab > 0 else 1200
            await capture_at(page, f"ab_testing_v4_{label}", "https://clevertap.com/product/ab-testing/", t)

        await browser.close()

    print("\n=== 완료 ===")
    for f in sorted(ASSETS.glob("*_v4*.png")) + sorted(ASSETS.glob("full_*.png")):
        print(f"  {f.name}: {f.stat().st_size//1024}KB")


if __name__ == "__main__":
    asyncio.run(capture_all())
