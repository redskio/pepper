"""
Upload modified PPTX back to Google Drive (same file ID = in-place update).
Also resolves all comments on the presentation.
"""
import json, sys
from pathlib import Path

PPTX_PATH  = "C:/Agent/pepper/output/modive_martech_v2.pptx"
FILE_ID    = "1HHZ8RfBDPpBpkOe4Nqbg1D_IMRo1wB-GZcJMyae4tXw"
CREDS_PATH = r"C:\Users\info\.claude\gdrive\.gdrive-server-credentials.json"
KEYS_PATH  = r"C:\Users\info\.claude\gdrive\gcp-oauth.keys.json"

# ── build credentials ──────────────────────────────────────────────────────
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

with open(CREDS_PATH) as f:
    c = json.load(f)

# load client_id / client_secret from keys file if not in creds
if not c.get("client_id") or not c.get("client_secret"):
    with open(KEYS_PATH) as f:
        keys = json.load(f)
    installed = keys.get("installed") or keys.get("web") or {}
    c["client_id"]     = installed.get("client_id", "")
    c["client_secret"] = installed.get("client_secret", "")
    c["token_uri"]     = installed.get("token_uri",
                         "https://oauth2.googleapis.com/token")

creds = Credentials(
    token         = c["access_token"],
    refresh_token = c["refresh_token"],
    client_id     = c["client_id"],
    client_secret = c["client_secret"],
    token_uri     = c.get("token_uri", "https://oauth2.googleapis.com/token"),
)

# refresh if expired
if creds.expired or not creds.valid:
    print("Refreshing token …")
    creds.refresh(Request())
    c["access_token"] = creds.token
    with open(CREDS_PATH, "w") as f:
        json.dump(c, f, indent=2)
    print("  ✓ Token refreshed")

# ── Drive service ──────────────────────────────────────────────────────────
drive = build("drive", "v3", credentials=creds)

# ── Step 1: update file content (keep same ID, convert to Google Slides) ───
print(f"\n[Step 1] Uploading {PPTX_PATH} → Drive file {FILE_ID} …")
media = MediaFileUpload(
    PPTX_PATH,
    mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    resumable=True,
)
result = drive.files().update(
    fileId    = FILE_ID,
    media_body= media,
    fields    = "id,name,webViewLink,modifiedTime",
).execute()
print(f"  ✓ Updated: {result.get('name')}")
print(f"  ✓ Link:    {result.get('webViewLink')}")
print(f"  ✓ Modified: {result.get('modifiedTime')}")

# ── Step 2: list and resolve all comments ──────────────────────────────────
print("\n[Step 2] Resolving comments …")
comments_resp = drive.comments().list(
    fileId = FILE_ID,
    fields = "comments(id,resolved,content)",
).execute()
comments = comments_resp.get("comments", [])
open_comments = [c for c in comments if not c.get("resolved")]
print(f"  Found {len(comments)} total, {len(open_comments)} open")

resolved = 0
for cm in open_comments:
    try:
        drive.comments().update(
            fileId    = FILE_ID,
            commentId = cm["id"],
            body      = {"resolved": True, "content": cm.get("content", "")},
            fields    = "id,resolved",
        ).execute()
        resolved += 1
        print(f"  ✓ Resolved comment {cm['id'][:8]}…")
    except Exception as e:
        print(f"  ⚠ Could not resolve {cm['id'][:8]}: {e}")

print(f"\n  Resolved {resolved}/{len(open_comments)} comments")
print("\nDone.")
print(f"\nFINAL_LINK: {result.get('webViewLink')}")
print(f"RESOLVED_COMMENTS: {resolved}")
print(f"TOTAL_COMMENTS: {len(comments)}")
