# -*- coding: utf-8 -*-
import sys, io, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json, requests
from pathlib import Path

# ── Refresh token ──────────────────────────────────────────────
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

# ── Upload files ───────────────────────────────────────────────
WIREFRAME_DIR = Path('C:/Agent/pepper/output/admix_wireframes')
files = [
    '01_dashboard.png',
    '02_new_campaign.png',
    '03_media_selection.png',
    '04_creative_editor.png',
    '05_contract_flow.png',
]

results = {}
for fname in files:
    fp = WIREFRAME_DIR / fname
    if not fp.exists():
        print(f'MISSING: {fname}')
        continue

    data = fp.read_bytes()
    meta = json.dumps({'name': fname, 'mimeType': 'image/png'}).encode()
    boundary = 'pepperv2bound'
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

# ── Save results ───────────────────────────────────────────────
out_path = Path('C:/Agent/pepper/output/admix_v2_drive_urls.json')
out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'\nSaved: {out_path}')
print(f'Uploaded: {len(results)}/5')
