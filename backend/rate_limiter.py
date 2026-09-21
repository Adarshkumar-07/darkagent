from __future__ import annotations

import re
from typing import Any

MALICIOUS_PATTERNS = [
    r"<script",
    r"javascript:",
    r"onerror\s*=",
    r"eval\s*\(",
    r"document\.cookie",
]


def sanitize_text(value: str) -> str:
    text = value.strip()
    if len(text) > 2000:
        text = text[:2000]
    return text.replace("\x00", "")


def contains_malicious_content(value: str) -> bool:
    lowered = value.lower()
    return any(re.search(pattern, lowered) for pattern in MALICIOUS_PATTERNS)


def validate_conversation(conversation: list[Any]) -> None:
    if not isinstance(conversation, list):
        raise ValueError("conversation must be a list")
    if len(conversation) > 20:
        raise ValueError("conversation exceeds the maximum message limit")

    for item in conversation:
        if not isinstance(item, dict):
            raise ValueError("each conversation message must be an object")
        if set(item.keys()) - {"role", "content", "timestamp"}:
            raise ValueError("conversation contains unsupported fields")
        if item.get("role") not in {"user", "assistant", "system"}:
            raise ValueError("conversation role is invalid")
        content = item.get("content")
        if not isinstance(content, str):
            raise ValueError("conversation content must be a string")
        if contains_malicious_content(content):
            raise ValueError("conversation content contains unsupported content")


def validate_message_size(message: str, max_chars: int) -> None:
    if len(message) > max_chars:
        raise ValueError(f"message exceeds {max_chars} characters")
