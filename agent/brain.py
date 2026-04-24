from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI


class Brain:
    """LLM reasoning engine for planning, tool selection, and reflection."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("DARKAGENT_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None

    def reason(self, system_prompt: str, user_prompt: str, as_json: bool = False) -> str:
        """Runs an LLM reasoning step; falls back to deterministic output when no API key exists."""
        if not self.client:
            if as_json:
                return json.dumps(
                    {
                        "summary": "Local fallback mode (no OPENAI_API_KEY).",
                        "tasks": [
                            "Research demand and competitor landscape",
                            "Generate first draft output",
                            "Refine output using reflection",
                        ],
                    }
                )
            return f"[Fallback Reasoning] {user_prompt[:400]}"

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            response_format={"type": "json_object"} if as_json else None,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""

    def safe_json(self, text: str) -> dict[str, Any]:
        """Best-effort JSON parsing."""
        try:
            return json.loads(text)
        except Exception:
            return {"raw": text}