"""
CleverTap 홈페이지 이미지 캡처 스크립트
Playwright를 사용해 주요 페이지 스크린샷 캡처
"""
import asyncio
import os
import sys
import requests
from pathlib import Path
from playwright.async_api import async_playwright

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

OUTPUT_DIR = Path("C:/Agent/pepper/output/clevertap_assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES = [
    ("main", "https://clevertap.com"),
    ("product", "https://clevertap.com/product/"),
    ("analytics", "https://clevertap.com/product/analytics/"),
    ("engagement", "https://clevertap.com/product/engagement/"),
    ("segmentation", "https://clevertap.com/product/segmentation/"),
    ("customers", "https://clevertap.com/customers/"),
    ("ai_ml", "https://clevertap.com/product/ai/"),
    ("ab_testing", "https://clevertap.com/product/ab-testing/"),
]

async def capture_page(page, name, url):
    print(f"[캡처] {name}: {url}")
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)

        # 풀페이지 스크린샷
        screenshot_path = OUTPUT_DIR / f"screenshot_{name}.png"
        await page.screenshot(path=str(screenshot_path), full_page=False)
        print(f"  ✅ 스크린샷 저장: {screenshot_path}")

        # 뷰포트 상단 캡처 (슬라이드용)
        viewport_path = OUTPUT_DIR / f"viewport_{name}.png"
        await page.screenshot(path=str(viewport_path), clip={"x": 0, "y": 0, "width": 1280, "height": 720})
        print(f"  ✅ 뷰포트 저장: {viewport_path}")

        # 이미지 URL 수집 및 다운로드
        images = await page.evaluate("""
            () => {
                const imgs = Array.from(document.querySelectorAll('img'));
                return imgs
                    .map(img => img.src || img.dataset.src)
                    .filter(src => src && (src.startsWith('http') || src.startsWith('//')))
                    .filter(src => !src.includes('icon') && !src.includes('favicon'))
                    .slice(0, 10);
            }
        """)

        downloaded = 0
        for i, img_url in enumerate(images):
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            try:
                resp = requests.get(img_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code == 200 and len(resp.content) > 5000:
                    ext = img_url.split('?')[0].split('.')[-1][:4].lower()
                    if ext not in ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg']:
                        ext = 'png'
                    img_path = OUTPUT_DIR / f"img_{name}_{i}.{ext}"
                    with open(img_path, 'wb') as f:
                        f.write(resp.content)
                    downloaded += 1
                    print(f"  📥 이미지 다운로드: {img_path.name} ({len(resp.content)//1024}KB)")
            except Exception as e:
                pass

        print(f"  📊 {name}: 이미지 {downloaded}개 다운로드 완료")
        return True

    except Exception as e:
        print(f"  ❌ {name} 캡처 실패: {e}")
        return False

async def main():
    print("🚀 CleverTap 이미지 캡처 시작")
    print(f"📁 저장 경로: {OUTPUT_DIR}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        success_count = 0
        for name, url in PAGES:
            result = await capture_page(page, name, url)
            if result:
                success_count += 1

        await browser.close()

    # 결과 확인
    files = list(OUTPUT_DIR.iterdir())
    print(f"\n✅ 캡처 완료: {success_count}/{len(PAGES)} 페이지")
    print(f"📁 총 파일 수: {len(files)}개")
    for f in sorted(files):
        size = f.stat().st_size // 1024
        print(f"  - {f.name} ({size}KB)")

if __name__ == "__main__":
    asyncio.run(main())
