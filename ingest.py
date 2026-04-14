"""
Ingest markdown docs from ./docs/ into a local Chroma collection.

Each file should be plain markdown. Optionally, the first line can be a YAML-ish
header to carry metadata for better citations:

    <!-- title: Política de Cancelamento | url: https://outline.seazone/... | area: Operacao -->
    # Política de Cancelamento
    ...

Run:  python ingest.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

DOCS_DIR = Path(__file__).parent / "docs"
DB_DIR = Path(__file__).parent / "chroma_db"
COLLECTION = "seazone_kb"

# Local embeddings — no API key needed, survives flaky WiFi.
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Chunking: char-based approximation (~4 chars/token => 800 tokens ≈ 3200 chars).
CHUNK_SIZE = 3200
CHUNK_OVERLAP = 600

META_RE = re.compile(r"<!--\s*(.*?)\s*-->", re.DOTALL)


def parse_header(text: str) -> tuple[dict, str]:
    """Extract metadata comment if present, return (meta, body)."""
    m = META_RE.match(text.strip())
    if not m:
        return {}, text
    header = m.group(1)
    meta = {}
    for pair in header.split("|"):
        if ":" in pair:
            k, v = pair.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():].lstrip()


def infer_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
        if line:
            return line[:80]
    return fallback


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split on paragraph boundaries when possible, fall back to hard slices."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buf = ""
    for para in paragraphs:
        if len(buf) + len(para) + 2 <= size:
            buf = f"{buf}\n\n{para}" if buf else para
        else:
            if buf:
                chunks.append(buf)
            # paragraph bigger than size: hard-split it
            if len(para) > size:
                for i in range(0, len(para), size - overlap):
                    chunks.append(para[i : i + size])
                buf = ""
            else:
                # carry overlap from previous chunk tail
                tail = buf[-overlap:] if buf else ""
                buf = f"{tail}\n\n{para}" if tail else para
    if buf:
        chunks.append(buf)
    return chunks


def main() -> int:
    if not DOCS_DIR.exists() or not any(DOCS_DIR.iterdir()):
        print(f"Put markdown files in {DOCS_DIR} first.", file=sys.stderr)
        return 1

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    client = chromadb.PersistentClient(path=str(DB_DIR))

    # Fresh ingest each run — keeps things simple.
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    coll = client.create_collection(COLLECTION, embedding_function=ef)

    ids, docs, metas = [], [], []
    files = sorted(DOCS_DIR.rglob("*.md"))
    for path in files:
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_header(raw)
        title = meta.get("title") or infer_title(body, path.stem)
        url = meta.get("url") or f"file://{path}"
        area = meta.get("area") or "Geral"

        for i, chunk in enumerate(chunk_text(body)):
            ids.append(f"{path.stem}::{i}")
            docs.append(chunk)
            metas.append({"title": title, "url": url, "area": area, "chunk": i})

    # Batch upserts — Chroma embeds in-process.
    BATCH = 64
    for i in range(0, len(ids), BATCH):
        coll.add(ids=ids[i : i + BATCH], documents=docs[i : i + BATCH], metadatas=metas[i : i + BATCH])
        print(f"  indexed {min(i + BATCH, len(ids))}/{len(ids)}")

    print(f"Done. {len(files)} files, {len(ids)} chunks -> {DB_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
