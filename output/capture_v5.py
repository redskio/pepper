# -*- coding: utf-8 -*-
"""
CleverTap 슬라이드별 컨텍스트 이미지 정밀 캡처 v5
- 각 페이지를 스크롤하며 제품 UI 섹션 탐색
- 슬라이드 주제에 맞는 최적 섹션 캡처
"""
import sys, io, asyncio, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path("C:/Agent/pepper/output/clevertap_assets")
OUT.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

# 슬라이드별 캡처 스펙
# (파일명, URL, 스크롤_y, 캡처_높이, 설명)
CAPTURES = [
    # 표지 — 홈페이지 히어로 (쿠키 배너 제거 후)
    ("ctx_cover.png",
     "https://clevertap.com",
     0, 720,
     "cover_hero"),

    # 소개 — product 개요 (전체 플랫폼 다이어그램)
    ("ctx_intro.png",
     "https://clevertap.com/product/",
     800, 720,
     "product_platform"),

    # 고객사 — customers 페이지 로고 섹션
    ("ctx_customers.png",
     "https://clevertap.com/customers/",
     600, 720,
     "customer_logos"),

    # 아키텍처 — product all-in-one 섹션
    ("ctx_architecture.png",
     "https://clevertap.com/product/",
     2000, 720,
     "product_architecture"),

    # Analytics — 데이터 분석 대시보드
    ("ctx_analytics.png",
     "https://clevertap.com/customer-data-and-analytics/",
     700, 720,
     "analytics_dashboard"),

    # Analytics 2 — 더 아래 섹션
    ("ctx_analytics2.png",
     "https://clevertap.com/customer-data-and-analytics/",
     1600, 720,
     "analytics_funnel"),

    # 세그멘테이션 — 세그먼트 빌더
    ("ctx_segmentation.png",
     "https://clevertap.com/segmentation/",
     700, 720,
     "segment_builder"),

    # 세그멘테이션 2
    ("ctx_segmentation2.png",
     "https://clevertap.com/segmentation/",
     1500, 720,
     "segment_filter"),

    # 인게이지먼트 — 멀티채널 메시징
    ("ctx_engagement.png",
     "https://clevertap.com/omnichannel-engagement/",
     700, 720,
     "engagement_channels"),

    # 인게이지먼트 2
    ("ctx_engagement2.png",
     "https://clevertap.com/omnichannel-engagement/",
     1600, 720,
     "engagement_campaign"),

    # AI/ML — CleverAI 엔진
    ("ctx_ai.png",
     "https://clevertap.com/ai/",
     700, 720,
     "ai_engine"),

    # AI/ML 2
    ("ctx_ai2.png",
     "https://clevertap.com/ai/",
     1600, 720,
     "ai_prediction"),

    # A/B 테스트 — 실험 설정
    ("ctx_ab.png",
     "https://clevertap.com/ab-testing/",
     700, 720,
     "ab_test_setup"),

    # A/B 테스트 2
    ("ctx_ab2.png",
     "https://clevertap.com/ab-testing/",
     1600, 720,
     "ab_results"),

    # 핀테크 — fintech solutions
    ("ctx_fintech.png",
     "https://clevertap.com/solutions/fintech/",
     600, 720,
     "fintech_hero"),

    # 핀테크 2
    ("ctx_fintech2.png",
     "https://clevertap.com/solutions/fintech/",
     1400, 720,
     "fintech_use_cases"),

    # 캠페인 빌더 (인게이지먼트용 추가)
    ("ctx_campaign.png",
     "https://clevertap.com/campaign-orchestration/",
     700, 720,
     "campaign_builder"),

    # 개인화
    ("ctx_personalization.png",
     "https://clevertap.com/personalization/",
     700, 720,
     "personalization"),
]


async def capture(name, url, scroll_y, height, label):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": height},
            user_agent=UA,
        )
        page = await ctx.new_page()

        # 쿠키 배너 자동 닫기
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(2)

            # 쿠키/팝업 닫기 시도
            for sel in ['button[data-testid*="accept"]', 'button:text("Accept")',
                        'button:text("Reject All")', '.onetrust-close-btn-handler',
                        '[aria-label*="close" i]', 'button:text("×")',
                        'button.cookie-close']:
                try:
                    btn = page.locator(sel).first
                    if await btn.count() > 0:
                        await btn.click()
                        await asyncio.sleep(0.5)
                        break
                except:
                    pass

            # 스크롤
            if scroll_y > 0:
                await page.evaluate(f"window.scrollTo(0, {scroll_y})")
                await asyncio.sleep(1.5)

            # 캡처
            out_path = str(OUT / name)
            await page.screenshot(
                path=out_path,
                clip={"x": 0, "y": 0, "width": 1280, "height": height}
            )

            size = os.path.getsize(out_path) // 1024
            print(f"  OK  {name} ({label}) — {size}KB")

        except Exception as e:
            print(f"  ERR {name}: {e}")
        finally:
            await browser.close()


async def main():
    print(f"총 {len(CAPTURES)}개 캡처 시작")
    for name, url, scroll_y, h, label in CAPTURES:
        await capture(name, url, scroll_y, h, label)
    print("캡처 완료")


if __name__ == "__main__":
    asyncio.run(main())
