# -*- coding: utf-8 -*-
"""
CleverTap 슬라이드별 컨텍스트 최적화 이미지 재캡처
- 각 페이지에서 스크롤해서 실제 제품 UI 이미지가 보이는 구간 캡처
- 로딩 대기 시간 충분히 확보
"""
import asyncio, sys, io, os, requests
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")
ASSETS.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

# (파일명, URL, 스크롤_Y, 설명)
TARGETS = [
    # 표지/소개: 메인 히어로 섹션
    ("ctx_main",        "https://clevertap.com",                         0,    "메인 홈 히어로"),
    # 소개: 제품 개요 페이지 - 스크롤해서 제품 다이어그램 보이게
    ("ctx_product_overview","https://clevertap.com/product/",            800,  "제품 개요"),
    # 고객사: Customers 페이지
    ("ctx_customers",   "https://clevertap.com/customers/",              400,  "고객사"),
    # 아키텍처: Product 페이지 스크롤 (플랫폼 다이어그램)
    ("ctx_architecture","https://clevertap.com/product/",                1600, "플랫폼 아키텍처"),
    # Analytics: Customer Data & Analytics 페이지
    ("ctx_analytics",   "https://clevertap.com/product/customer-data-platform/", 600, "분석"),
    # Segmentation: Segmentation 페이지
    ("ctx_segmentation","https://clevertap.com/product/segments/",       500,  "세그멘테이션"),
    # Engagement: Omnichannel Engagement
    ("ctx_engagement",  "https://clevertap.com/product/omnichannel-engagement/", 500, "인게이지먼트"),
    # AI/ML: CleverAI 페이지 - 스크롤해서 기능 다이어그램
    ("ctx_ai",          "https://clevertap.com/clevertap-ai/",           600,  "AI 기능"),
    # A/B Testing: Experiment & Optimization
    ("ctx_ab",          "https://clevertap.com/product/experiments/",    500,  "A/B 테스트"),
    # Fintech: Fintech Solutions 페이지
    ("ctx_fintech",     "https://clevertap.com/solutions/fintech/",      600,  "핀테크"),
]

async def capture(page, name, url, scroll_y, desc):
    print(f"  [{name}] {desc}: {url}")
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
        print(f"    -> {path.name} ({size}KB)")

        # 이미지가 너무 작으면 (blank page) 다른 스크롤 위치 시도
        if size < 20:
            for alt_y in [200, 1200, 2000]:
                await page.evaluate(f"window.scrollTo(0, {alt_y})")
                await asyncio.sleep(1.0)
                await page.screenshot(path=str(path),
                                       clip={"x": 0, "y": 0, "width": 1280, "height": 720})
                size2 = path.stat().st_size // 1024
                if size2 > 50:
                    print(f"    -> 재캡처 성공 at scroll={alt_y}: {size2}KB")
                    break
        return True
    except Exception as e:
        print(f"    [오류] {e}")
        return False

async def main():
    print("CleverTap 슬라이드별 이미지 재캡처 시작")
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

    files = list(ASSETS.glob("ctx_*.png"))
    print(f"\n완료: {ok}/{len(TARGETS)} 캡처, {len(files)}개 ctx 파일")
    for f in sorted(files):
        print(f"  {f.name}: {f.stat().st_size//1024}KB")

if __name__ == "__main__":
    asyncio.run(main())
