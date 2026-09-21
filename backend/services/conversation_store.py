from __future__ import annotations
import json

class ConversationStore:
    def __init__(self) -> None: self._sessions: dict[str, list[dict[str, str]]] = {}
    def get(self, session_id: str) -> list[dict[str, str]]: return list(self._sessions.get(session_id, []))
    def append(self, session_id: str, message: dict[str, str]) -> list[dict[str, str]]:
        self._sessions.setdefault(session_id, []).append(message); return self.get(session_id)
    def clear(self, session_id: str) -> None: self._sessions[session_id] = []
    def export_json(self, session_id: str) -> str: return json.dumps(self.get(session_id), indent=2)
