from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from backend.config import SETTINGS


class AIService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=SETTINGS.openai_api_key) if SETTINGS.openai_api_key else None

    def generate_reply(self, message: str, conversation: list[dict[str, str]]) -> str:
        if not self.client or not SETTINGS.openai_api_key:
            raise ValueError("AI API key is not configured. Set OPENAI_API_KEY in your environment before using the assistant.")

        history = []
        for item in conversation[-12:]:
            role = item.get("role")
            content = item.get("content")
            if role in {"user", "assistant"} and isinstance(content, str):
                history.append({"role": role, "content": content})

        payload = [
            {
                "role": "system",
                "content": (
                    "You are Aegis Voice, a helpful AI voice assistant. "
                    "Be concise, natural, and useful. Reply in plain language, and keep answers easy to speak aloud."
                ),
            },
            *history,
            {"role": "user", "content": message},
        ]

        response = self.client.chat.completions.create(
            model=SETTINGS.default_model,
            messages=payload,
            temperature=0.7,
            max_tokens=500,
        )
        reply = response.choices[0].message.content
        if not isinstance(reply, str) or not reply.strip():
            raise ValueError("AI service returned an empty or invalid response.")
        return reply.strip()
