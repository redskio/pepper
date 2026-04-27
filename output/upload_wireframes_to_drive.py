# -*- coding: utf-8 -*-
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json, requests
from pathlib import Path

# ── 1. Refresh Google Drive token ─────────────────────────────
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
    print('FAIL Token refresh failed:', resp.text[:200])
    sys.exit(1)
print('OK Token refreshed:', token[:30])

# ── 2. Upload each PNG to Google Drive ────────────────────────
WIREFRAME_DIR = Path('C:/Agent/pepper/output/admix_wireframes')
files = sorted(WIREFRAME_DIR.glob('*.png'))
drive_urls = {}

for fp in files:
    data = fp.read_bytes()
    meta = json.dumps({'name': fp.name, 'mimeType': 'image/png'}).encode()
    boundary = 'pepperbound'
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
        data=body,
        timeout=60
    )
    if r.status_code in (200, 201):
        file_id = r.json()['id']
        # Make public
        perm = requests.post(
            f'https://www.googleapis.com/drive/v3/files/{file_id}/permissions',
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
            json={'role': 'reader', 'type': 'anyone'},
            timeout=15
        )
        url = f'https://drive.google.com/uc?export=view&id={file_id}'
        drive_urls[fp.name] = url
        print(f'OK {fp.name} -> {url}')
    else:
        print(f'FAIL {fp.name}: {r.status_code} {r.text[:200]}')

# ── 3. Save URLs to JSON for next step ───────────────────────
out = Path('C:/Agent/pepper/output/admix_drive_urls.json')
out.write_text(json.dumps(drive_urls, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'\nSaved URLs to {out}')
print('Total uploaded:', len(drive_urls))
