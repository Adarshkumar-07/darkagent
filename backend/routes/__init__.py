from __future__ import annotations

import json
from typing import Any


class ConversationStore:
    def __init__(self) -> None:
        self._sessions: dict[str, list[dict[str, str]]] = {}

    def create_session(self, session_id: str | None = None) -> str:
        key = session_id or f"session-{len(self._sessions) + 1}"
        self._sessions[key] = []
        return key

    def append(self, session_id: str, message: dict[str, str]) -> list[dict[str, str]]:
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append(message)
        return self._sessions[session_id]

    def clear(self, session_id: str) -> None:
        self._sessions[session_id] = []

    def get(self, session_id: str) -> list[dict[str, str]]:
        return list(self._sessions.get(session_id, []))

    def export_json(self, session_id: str) -> str:
        return json.dumps(self.get(session_id), indent=2)

    def delete(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
