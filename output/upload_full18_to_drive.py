# -*- coding: utf-8 -*-
import sys, io, os, json, requests
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

# Token refresh
with open(r'C:\Users\info\.claude\gdrive\.gdrive-server-credentials.json') as f:
    creds = json.load(f)

resp = requests.post(creds['token_uri'], data={
    'client_id': creds['client_id'],
    'client_secret': creds['client_secret'],
    'refresh_token': creds['refresh_token'],
    'grant_type': 'refresh_token',
})
token = resp.json().get('access_token', '')
if not token:
    print('FAIL token refresh:', resp.text[:200])
    sys.exit(1)
print('OK Token refreshed')

WIREFRAME_DIR = Path('C:/Agent/pepper/admix_wireframes')
files = [
    '01_landing_hero.png',
    '02_service_intro.png',
    '03_pricing.png',
    '04_dashboard_home.png',
    '05_campaign_step1_media.png',
    '06_campaign_step2_creative.png',
    '07_campaign_step3_size.png',
    '08_campaign_step4_budget.png',
    '09_campaign_list.png',
    '10_campaign_detail.png',
    '11_creative_library.png',
    '12_report.png',
    '13_media_onboarding.png',
    '14_media_inventory.png',
    '15_mobile_dashboard.png',
]

results = {}
for fname in files:
    fp = WIREFRAME_DIR / fname
    if not fp.exists():
        print(f'MISSING: {fname}')
        continue

    data = fp.read_bytes()
    meta = json.dumps({'name': fname, 'mimeType': 'image/png'}).encode()
    boundary = 'admixfull18bound'
    body = (
        f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode()
        + meta
        + f'\r\n--{boundary}\r\nContent-Type: image/png\r\n\r\n'.encode()
        + data
        + f'\r\n--{boundary}--'.encode()
    )
    r = requests.post(
        'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': f'multipart/related; boundary={boundary}',
        },
        data=body, timeout=60,
    )
    if r.status_code in (200, 201):
        file_id = r.json()['id']
        requests.post(
            f'https://www.googleapis.com/drive/v3/files/{file_id}/permissions',
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
            json={'role': 'reader', 'type': 'anyone'},
            timeout=15,
        )
        url = f'https://drive.google.com/uc?export=view&id={file_id}'
        results[fname] = {'id': file_id, 'url': url}
        print(f'OK {fname} -> {url}')
    else:
        print(f'FAIL {fname}: {r.status_code} {r.text[:150]}')

out_path = Path('C:/Agent/pepper/output/admix_full18_drive_urls.json')
out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'\nSaved: {out_path}')
print(f'Uploaded: {len(results)}/15')
