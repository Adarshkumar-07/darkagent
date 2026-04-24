from __future__ import annotations

import hashlib
from collections import deque
from datetime import datetime
from typing import Any

import chromadb


class Memory:
    """Manages short-term and long-term memory."""

    def __init__(self, max_short_term: int = 20, persist_dir: str = ".darkagent_memory") -> None:
        self.short_term: deque[dict[str, Any]] = deque(maxlen=max_short_term)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="darkagent_events")

    def add_short_term(self, role: str, content: str) -> None:
        self.short_term.append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    def get_short_term(self) -> list[dict[str, Any]]:
        return list(self.short_term)

    @staticmethod
    def _cheap_embedding(text: str, size: int = 32) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values = [b / 255.0 for b in digest[:size]]
        return values

    def add_long_term(self, text: str, metadata: dict[str, Any] | None = None) -> str:
        doc_id = hashlib.md5(f"{datetime.utcnow().isoformat()}::{text}".encode("utf-8")).hexdigest()
        self.collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[metadata or {}],
            embeddings=[self._cheap_embedding(text)],
        )
        return doc_id

    def search_long_term(self, query: str, top_k: int = 5) -> list[str]:
        result = self.collection.query(
            query_embeddings=[self._cheap_embedding(query)],
            n_results=top_k,
            include=["documents"],
        )
        docs = result.get("documents", [[]])
        return docs[0] if docs else []