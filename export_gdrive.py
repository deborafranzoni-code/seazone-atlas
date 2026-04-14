"""
Export Google Docs from a Drive folder into ./docs/ as markdown with metadata
headers, matching the format ingest.py expects.

Setup (one-time):
  1. Create an OAuth client in Google Cloud Console (type: Desktop app).
  2. Download credentials.json to this folder.
  3. pip install google-api-python-client google-auth google-auth-oauthlib

Env vars (in .env):
  GDRIVE_FOLDER_ID  the folder whose Google Docs should be exported
  GDRIVE_AREA       label written into the metadata header (e.g. "Financeiro")

Run: python export_gdrive.py
The first run opens a browser for consent and writes token.json.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", "")
AREA = os.environ.get("GDRIVE_AREA", "Geral")
OUT = Path(__file__).parent / "docs"
CREDS = Path(__file__).parent / "credentials.json"
TOKEN = Path(__file__).parent / "token.json"

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[-\s]+", "-", s)
    return s[:80] or "doc"


def get_services():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS.exists():
                raise SystemExit(f"Missing {CREDS}. See file header for setup.")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN.write_text(creds.to_json())

    return build("drive", "v3", credentials=creds)


def list_docs(drive, folder_id: str):
    page_token = None
    q = (
        f"'{folder_id}' in parents "
        "and mimeType='application/vnd.google-apps.document' "
        "and trashed=false"
    )
    while True:
        resp = drive.files().list(
            q=q,
            fields="nextPageToken, files(id, name, webViewLink)",
            pageSize=100,
            pageToken=page_token,
        ).execute()
        for f in resp.get("files", []):
            yield f
        page_token = resp.get("nextPageToken")
        if not page_token:
            return


def export_markdown(drive, file_id: str) -> str:
    # Drive supports direct Markdown export for Google Docs.
    data = drive.files().export(fileId=file_id, mimeType="text/markdown").execute()
    return data.decode("utf-8") if isinstance(data, bytes) else data


def main() -> int:
    if not FOLDER_ID:
        print("Set GDRIVE_FOLDER_ID in .env first.", file=sys.stderr)
        return 1

    OUT.mkdir(exist_ok=True)
    drive = get_services()
    count = 0

    for f in list_docs(drive, FOLDER_ID):
        title = f["name"]
        url = f.get("webViewLink") or f"https://docs.google.com/document/d/{f['id']}"
        try:
            body = export_markdown(drive, f["id"])
        except Exception as e:
            print(f"  skip {title!r}: {e}", file=sys.stderr)
            continue

        safe_title = title.replace("|", "-")
        header = f"<!-- title: {safe_title} | url: {url} | area: {AREA} -->\n\n"
        out_path = OUT / f"{slugify(title)}-{f['id'][:8]}.md"
        out_path.write_text(header + body, encoding="utf-8")
        count += 1
        print(f"  {count:>3}  {title[:70]}")

    print(f"\nExported {count} docs to {OUT}")
    print("Next: python ingest.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
