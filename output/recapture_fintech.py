# -*- coding: utf-8 -*-
"""핀테크 URL 탐색 + 최종 이미지 캡처"""
import asyncio, sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 720}, user_agent=UA)
        page = await ctx.new_page()

        # Solutions 페이지에서 Financial Services 링크 URL 찾기
        print("Solutions 페이지 링크 탐색...")
        await page.goto("https://clevertap.com/solutions/", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)

        # 모든 href 링크 수집
        links = await page.evaluate("""
            () => Array.from(document.querySelectorAll('a[href]'))
                .map(a => a.href)
                .filter(h => h.includes('financial') || h.includes('fintech') || h.includes('banking') || h.includes('finance'))
        """)
        print("관련 링크:", links)

        # 모든 Solutions 섹션 링크
        sol_links = await page.evaluate("""
            () => Array.from(document.querySelectorAll('a[href]'))
                .map(a => ({text: a.textContent.trim(), href: a.href}))
                .filter(x => x.href.includes('/solutions/') && x.text.length > 0)
        """)
        print("Solutions 링크:")
        for l in sol_links:
            print(f"  {l['text']}: {l['href']}")

        # A/B Testing URL도 찾기
        print("\nA/B / Experimentation 링크:")
        ab_links = await page.evaluate("""
            () => Array.from(document.querySelectorAll('a[href]'))
                .map(a => ({text: a.textContent.trim(), href: a.href}))
                .filter(x => x.text.toLowerCase().includes('experiment') || x.text.toLowerCase().includes('a/b') || x.href.includes('experiment'))
        """)
        for l in ab_links:
            print(f"  {l['text']}: {l['href']}")

        # 홈 페이지에서 Solutions 메뉴 링크 파악
        print("\n홈에서 Solutions 메뉴...")
        await page.goto("https://clevertap.com/", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        # Solutions 메뉴 호버
        await page.hover("text=Solutions")
        await asyncio.sleep(1)
        fin_links = await page.evaluate("""
            () => Array.from(document.querySelectorAll('a[href]'))
                .map(a => ({text: a.textContent.trim(), href: a.href}))
                .filter(x => x.text.toLowerCase().includes('financial') || x.text.toLowerCase().includes('fintech') || x.text.toLowerCase().includes('banking'))
        """)
        print("Financial 관련 링크:", fin_links)

        # 직접 시도할 URL들
        test_urls = [
            "https://clevertap.com/solutions/financial-services/",
            "https://clevertap.com/solutions/fintech/",
            "https://clevertap.com/solutions/banking-and-finance/",
            "https://clevertap.com/solutions/banking/",
            "https://clevertap.com/industry/fintech/",
        ]
        print("\nURL 존재 여부 확인:")
        for url in test_urls:
            resp = await page.goto(url, wait_until="domcontentloaded", timeout=10000)
            title = await page.title()
            print(f"  {url} → {resp.status} | {title[:60]}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
