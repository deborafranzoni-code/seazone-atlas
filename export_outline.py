"""
Export all documents from an Outline workspace into ./docs/ with metadata headers
already in the format that ingest.py expects.

Env vars (in .env):
  OUTLINE_URL      e.g. https://outline.seazone.dev
  OUTLINE_API_KEY  Bearer token — get at <your-outline>/settings/api-tokens

Optional:
  OUTLINE_COLLECTIONS  comma-separated collection IDs to include (default: all)

Run: python export_outline.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE = os.environ.get("OUTLINE_URL", "").rstrip("/")
TOKEN = os.environ.get("OUTLINE_API_KEY", "")
ALLOWED = {c.strip() for c in os.environ.get("OUTLINE_COLLECTIONS", "").split(",") if c.strip()}
OUT = Path(__file__).parent / "docs"


def _post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Outline da Seazone fica atrás do Cloudflare, que bane o UA
            # padrão do urllib (Python-urllib/x.y) com erro 1010.
            "User-Agent": "Mozilla/5.0 (rag-seazone-export)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code} on {path}: {body}") from e


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[-\s]+", "-", s)
    return s[:80] or "doc"


def list_documents():
    offset, limit = 0, 100
    while True:
        data = _post("/api/documents.list", {"offset": offset, "limit": limit, "sort": "updatedAt"})
        docs = data.get("data", []) or []
        for d in docs:
            yield d
        if len(docs) < limit:
            return
        offset += limit


def collection_name(cache: dict, coll_id: str) -> str:
    if coll_id in cache:
        return cache[coll_id]
    try:
        data = _post("/api/collections.info", {"id": coll_id})
        name = (data.get("data") or {}).get("name") or "Geral"
    except SystemExit:
        name = "Geral"
    cache[coll_id] = name
    return name


def main() -> int:
    if not BASE or not TOKEN:
        print("Set OUTLINE_URL and OUTLINE_API_KEY in .env first.", file=sys.stderr)
        return 1

    OUT.mkdir(exist_ok=True)
    cache: dict = {}
    count, skipped = 0, 0

    for doc in list_documents():
        coll_id = doc.get("collectionId") or ""
        if ALLOWED and coll_id not in ALLOWED:
            skipped += 1
            continue

        title = doc.get("title") or "Untitled"
        url = f"{BASE}{doc.get('url', '/')}"
        area = collection_name(cache, coll_id)
        body = _post("/api/documents.export", {"id": doc["id"]}).get("data", "")

        # Sanitize metadata values (pipes would confuse the header parser).
        safe_title = title.replace("|", "-")
        safe_area = area.replace("|", "-")
        header = f"<!-- title: {safe_title} | url: {url} | area: {safe_area} -->\n\n"

        out_path = OUT / f"{slugify(title)}-{doc['id'][:8]}.md"
        out_path.write_text(header + body, encoding="utf-8")
        count += 1
        print(f"  {count:>3}  [{area[:18]:<18}]  {title[:70]}")
        time.sleep(0.1)  # be polite to the API

    print(f"\nExported {count} docs to {OUT}" + (f" (skipped {skipped})" if skipped else ""))
    print("Next: python ingest.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
