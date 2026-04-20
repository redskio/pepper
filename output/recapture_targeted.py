# -*- coding: utf-8 -*-
"""
CleverTap 슬라이드별 컨텍스트 맞춤 이미지 재캡처
문제 슬라이드: analytics, segmentation, ab_testing
전략: 각 페이지에서 스크롤하여 실제 제품 기능 컨텐츠 캡처
"""
import sys, io, asyncio, os, requests
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")
ASSETS.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"

async def capture_section(page, name: str, url: str, scroll_y: int = 0,
                           wait_sel: str = None, extra_wait: float = 3.0):
    """페이지 특정 스크롤 위치에서 뷰포트 캡처"""
    print(f"[{name}] {url} (scroll={scroll_y}px)")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2500)

        # 쿠키 배너 닫기
        for sel in ['button:has-text("Accept")', 'button:has-text("Reject All")',
                    '[class*="cookie"] button', '#onetrust-accept-btn-handler']:
            try:
                el = page.locator(sel).first
                if await el.is_visible():
                    await el.click()
                    await page.wait_for_timeout(500)
                    break
            except:
                pass

        # 광고 배너 숨기기
        await page.evaluate("""
            () => {
                const banners = document.querySelectorAll('[class*="announcement"], [class*="banner"], [class*="cookie"], [id*="cookie"]');
                banners.forEach(b => b.style.display = 'none');
            }
        """)

        if wait_sel:
            try:
                await page.wait_for_selector(wait_sel, timeout=8000)
            except:
                pass

        # 스크롤
        if scroll_y > 0:
            await page.evaluate(f"window.scrollTo(0, {scroll_y})")
            await page.wait_for_timeout(int(extra_wait * 1000))

        # 캡처
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


async def capture_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=UA
        )
        page = await ctx.new_page()

        # ── Analytics: 스크롤 내려서 대시보드/차트 섹션 캡처 ──
        await capture_section(
            page, "analytics_v2",
            "https://clevertap.com/product/analytics/",
            scroll_y=600,
            extra_wait=3.0
        )

        # ── Segmentation: 세그먼트 필터 섹션 ──
        await capture_section(
            page, "segmentation_v2",
            "https://clevertap.com/product/segmentation/",
            scroll_y=700,
            extra_wait=3.0
        )

        # ── A/B Testing ──
        await capture_section(
            page, "ab_testing_v2",
            "https://clevertap.com/product/ab-testing/",
            scroll_y=600,
            extra_wait=3.0
        )

        # ── Product Overview (소개 슬라이드용) ──
        await capture_section(
            page, "product_overview_v2",
            "https://clevertap.com/product/",
            scroll_y=500,
            extra_wait=3.0
        )

        # ── Orchestration/Journeys (아키텍처 슬라이드용) ──
        await capture_section(
            page, "orchestration_v2",
            "https://clevertap.com/product/journeys/",
            scroll_y=500,
            extra_wait=3.0
        )

        # ── Personalization (세그멘테이션 대체) ──
        await capture_section(
            page, "personalization_v2",
            "https://clevertap.com/product/personalization/",
            scroll_y=600,
            extra_wait=3.0
        )

        # ── Fintech 솔루션 ──
        await capture_section(
            page, "fintech_v2",
            "https://clevertap.com/solutions/fintech/",
            scroll_y=500,
            extra_wait=3.0
        )

        # ── 추가 스크롤 캡처: Analytics 더 아래 ──
        await capture_section(
            page, "analytics_v3",
            "https://clevertap.com/product/analytics/",
            scroll_y=1200,
            extra_wait=3.0
        )

        # ── 추가: Engagement 더 아래 ──
        await capture_section(
            page, "engagement_v2",
            "https://clevertap.com/product/engagement/",
            scroll_y=800,
            extra_wait=3.0
        )

        await browser.close()

    print("\n=== 재캡처 완료 ===")
    for f in sorted(ASSETS.glob("*_v2.png")) | set(ASSETS.glob("*_v3.png")):
        print(f"  {f.name}: {f.stat().st_size//1024}KB")


if __name__ == "__main__":
    asyncio.run(capture_all())
