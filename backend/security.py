from __future__ import annotations

import re

PATTERNS = (r"<script", r"javascript:", r"onerror\s*=", r"eval\s*\(", r"document\.cookie")

def sanitize_text(value: str) -> str:
    return value.replace("\x00", "").strip()[:2_000]

def contains_malicious_content(value: str) -> bool:
    return any(re.search(pattern, value.lower()) for pattern in PATTERNS)

def validate_conversation(conversation: list[dict]) -> None:
    if len(conversation) > 20: raise ValueError("conversation exceeds the maximum message limit")
    for item in conversation:
        if item.get("role") not in {"user", "assistant", "system"}: raise ValueError("conversation role is invalid")
        if not isinstance(item.get("content"), str) or contains_malicious_content(item["content"]):
            raise ValueError("conversation content is invalid")

def validate_message_size(message: str, max_chars: int) -> None:
    if len(message) > max_chars: raise ValueError(f"message exceeds {max_chars} characters")
