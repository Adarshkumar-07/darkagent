from __future__ import annotations
from openai import OpenAI
from backend.config import SETTINGS

class AIService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=SETTINGS.openai_api_key) if SETTINGS.openai_api_key else None
    def generate_reply(self, message: str, conversation: list[dict[str, str]]) -> str:
        if self.client is None: raise RuntimeError("AI service is not configured")
        history = [{"role": x["role"], "content": x["content"]} for x in conversation[-12:] if x["role"] in {"user", "assistant"}]
        response = self.client.chat.completions.create(model=SETTINGS.default_model, temperature=0.7, max_tokens=500, messages=[
            {"role":"system", "content":"You are Aegis Voice, a concise, helpful voice assistant. Use plain language suitable for speech."}, *history, {"role":"user", "content": message}
        ])
        reply = response.choices[0].message.content
        if not isinstance(reply, str) or not reply.strip(): raise RuntimeError("AI service returned an empty response")
        return reply.strip()
