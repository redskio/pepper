# -*- coding: utf-8 -*-
import sys, io, json, requests
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

# Load drive URLs
urls_path = Path('C:/Agent/pepper/output/admix_full18_drive_urls.json')
drive_urls = json.loads(urls_path.read_text(encoding='utf-8'))

# Notion config
import yaml
with open(r'C:\Agent\mcp_registry.yaml', encoding='utf-8') as f:
    reg = yaml.safe_load(f)

NOTION_TOKEN = reg['notion']['api_token']
PAGE_ID = reg['notion']['pages']['pepper']

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

# Build children blocks: heading + images
screen_labels = {
    '01_landing_hero.png':         '01. Landing Hero — 랜딩 히어로',
    '02_service_intro.png':        '02. Service Intro — 서비스 소개',
    '03_pricing.png':              '03. Pricing — 요금제',
    '04_dashboard_home.png':       '04. Dashboard Home — 대시보드',
    '05_campaign_step1_media.png': '05. Campaign Step 1 — 미디어 선택',
    '06_campaign_step2_creative.png': '06. Campaign Step 2 — 크리에이티브',
    '07_campaign_step3_size.png':  '07. Campaign Step 3 — 사이즈/포맷',
    '08_campaign_step4_budget.png':'08. Campaign Step 4 — 예산/기간',
    '09_campaign_list.png':        '09. Campaign List — 캠페인 목록',
    '10_campaign_detail.png':      '10. Campaign Detail — 캠페인 상세',
    '11_creative_library.png':     '11. Creative Library — 크리에이티브 라이브러리',
    '12_report.png':               '12. Report — 리포트',
    '13_media_onboarding.png':     '13. Media Onboarding — 미디어사 온보딩',
    '14_media_inventory.png':      '14. Media Inventory — 인벤토리 관리',
    '15_mobile_dashboard.png':     '15. Mobile Dashboard — 모바일 대시보드',
}

# Top-level heading
children = [
    {
        'object': 'block',
        'type': 'heading_2',
        'heading_2': {
            'rich_text': [{'type': 'text', 'text': {'content': 'AdMix 전체 화면 와이어프레임 (Deep Blue + Lime Green, 15 screens)'}}]
        }
    },
    {
        'object': 'block',
        'type': 'paragraph',
        'paragraph': {
            'rich_text': [{'type': 'text', 'text': {'content': 'Web: 1440x900 / Mobile: 390x844 | Color: #1A1F5E + #4ADE80'}}]
        }
    },
]

for fname, label in screen_labels.items():
    if fname not in drive_urls:
        print(f'SKIP (no URL): {fname}')
        continue
    url = drive_urls[fname]['url']
    children.append({
        'object': 'block',
        'type': 'paragraph',
        'paragraph': {
            'rich_text': [{'type': 'text', 'text': {'content': label}, 'annotations': {'bold': True}}]
        }
    })
    children.append({
        'object': 'block',
        'type': 'image',
        'image': {'type': 'external', 'external': {'url': url}}
    })

# Notion API has 100-block limit per request — send in batches of 20
BATCH = 20
total = 0
for i in range(0, len(children), BATCH):
    batch = children[i:i+BATCH]
    r = requests.patch(
        f'https://api.notion.com/v1/blocks/{PAGE_ID}/children',
        headers=HEADERS,
        json={'children': batch},
        timeout=30,
    )
    if r.status_code == 200:
        total += len(batch)
        print(f'OK batch {i//BATCH+1}: {len(batch)} blocks appended')
    else:
        print(f'FAIL batch {i//BATCH+1}: {r.status_code} {r.text[:200]}')

print(f'\nTotal blocks appended: {total}/{len(children)}')
notion_url = f'https://www.notion.so/{PAGE_ID.replace("-","")}'
print(f'Notion page: {notion_url}')
