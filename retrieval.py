"""
Query the Chroma collection built by ingest.py.

Returns (context_string, sources) where context_string is formatted for the
LLM prompt and sources is a list of dicts usable for UI citations.
"""

from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

DB_DIR = Path(__file__).parent / "chroma_db"
COLLECTION = "seazone_kb"
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)


def _get_collection():
    client = chromadb.PersistentClient(path=str(DB_DIR))
    return client.get_collection(COLLECTION, embedding_function=_ef)


def retrieve(query: str, area: str | list | None = None, top_k: int = 5) -> tuple[str, list[dict]]:
    coll = _get_collection()

    if isinstance(area, list) and len(area) > 1:
        where = {"area": {"$in": area}}
    elif isinstance(area, list) and len(area) == 1:
        where = {"area": area[0]}
    elif area and area != "Todas":
        where = {"area": area}
    else:
        where = None
    res = coll.query(query_texts=[query], n_results=top_k, where=where)

    docs = res["documents"][0]
    metas = res["metadatas"][0]
    distances = res.get("distances", [[None] * len(docs)])[0]

    # Dedup sources by url while preserving order.
    seen_urls = set()
    sources = []
    blocks = []
    for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances), start=1):
        blocks.append(
            f"[{i}] Título: {meta['title']}\nURL: {meta['url']}\nÁrea: {meta['area']}\n\n{doc}"
        )
        if meta["url"] not in seen_urls:
            seen_urls.add(meta["url"])
            url = meta["url"]
            # Derive source label from URL
            if "slack.com" in url:
                source = "Slack"
            elif "outline.seazone" in url:
                source = "Outline"
            elif url.startswith("file://"):
                source = "Local"
            else:
                source = "Outro"
            sources.append(
                {
                    "title": meta["title"],
                    "url": url,
                    "area": meta["area"],
                    "source": source,
                    "distance": dist,
                }
            )

    context = "\n\n---\n\n".join(blocks) if blocks else "(nenhum trecho encontrado)"
    return context, sources
