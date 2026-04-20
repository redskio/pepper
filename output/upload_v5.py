# -*- coding: utf-8 -*-
"""v5 PPTX → Google Slides 업로드"""
import sys, io, json, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_FILE = r"C:\Users\info\.claude\gdrive\.gdrive-server-credentials.json"
PPTX_PATH  = r"C:\Agent\pepper\output\clevertap_proposal_kr_v5.pptx"
FILE_NAME  = "CleverTap 제안서 KR v5 (이미지 컨텍스트 교정)"

with open(TOKEN_FILE) as f:
    t = json.load(f)

creds = Credentials(
    token=t["access_token"],
    refresh_token=t["refresh_token"],
    client_id=t["client_id"],
    client_secret=t["client_secret"],
    token_uri=t.get("token_uri", "https://oauth2.googleapis.com/token"),
)

svc = build("drive", "v3", credentials=creds)

print(f"업로드: {FILE_NAME}")
meta = {
    "name": FILE_NAME,
    "mimeType": "application/vnd.google-apps.presentation"
}
media = MediaFileUpload(
    PPTX_PATH,
    mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    resumable=True
)
f = svc.files().create(body=meta, media_body=media, fields="id,webViewLink").execute()
fid = f["id"]

# 링크 공개
svc.permissions().create(fileId=fid, body={"type": "anyone", "role": "reader"}).execute()

link = f.get("webViewLink", f"https://docs.google.com/presentation/d/{fid}/edit")
print(f"완료!")
print(f"Google Slides: {link}")
print(f"File ID: {fid}")
