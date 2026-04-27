# -*- coding: utf-8 -*-
import sys, io, os, json, requests
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

with open(r'C:\Users\info\.claude\gdrive\.gdrive-server-credentials.json') as f:
    creds = json.load(f)

resp = requests.post(creds['token_uri'], data={
    'client_id': creds['client_id'], 'client_secret': creds['client_secret'],
    'refresh_token': creds['refresh_token'], 'grant_type': 'refresh_token',
})
token = resp.json().get('access_token', '')
if not token:
    print('FAIL token'); import sys; sys.exit(1)
print('OK token refreshed')

files = [
    'admix_01_onboarding.png', 'admix_02_dashboard.png',
    'admix_03_media_select.png', 'admix_04_creative_editor.png',
    'admix_05_review.png',
]
results = {}
for fname in files:
    fp = Path('C:/Agent/pepper/admix_ui') / fname
    data = fp.read_bytes()
    meta = json.dumps({'name': fname, 'mimeType': 'image/png'}).encode()
    boundary = 'pepperplatform'
    body = (f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode()
            + meta + f'\r\n--{boundary}\r\nContent-Type: image/png\r\n\r\n'.encode()
            + data + f'\r\n--{boundary}--'.encode())
    r = requests.post(
        'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name',
        headers={'Authorization': f'Bearer {token}', 'Content-Type': f'multipart/related; boundary={boundary}'},
        data=body, timeout=60)
    if r.status_code in (200, 201):
        fid = r.json()['id']
        requests.post(f'https://www.googleapis.com/drive/v3/files/{fid}/permissions',
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
            json={'role': 'reader', 'type': 'anyone'}, timeout=15)
        url = f'https://drive.google.com/uc?export=view&id={fid}'
        results[fname] = {'id': fid, 'url': url}
        print(f'OK {fname} -> {url}')
    else:
        print(f'FAIL {fname}: {r.status_code}')

Path('C:/Agent/pepper/output/admix_platform_drive_urls.json').write_text(
    json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'\nUploaded: {len(results)}/5')
