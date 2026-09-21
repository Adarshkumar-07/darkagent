from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    app_name: str = "Aegis Voice"
    environment: str = "development"
    openai_api_key: str | None = None
    default_model: str = "gpt-4o-mini"
    max_request_size: int = 1024 * 1024
    max_conversation_messages: int = 20
    max_message_chars: int = 2000
    max_history_chars: int = 20000
    allowed_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"])
    rate_limit_requests: int = 20
    rate_limit_window_seconds: int = 60


@dataclass
class RuntimeSettings:
    app_name: str = "Aegis Voice"
    environment: str = "development"
    openai_api_key: str | None = None
    default_model: str = "gpt-4o-mini"
    max_request_size: int = 1024 * 1024
    max_conversation_messages: int = 20
    max_message_chars: int = 2000
    max_history_chars: int = 20000
    allowed_origins: list[str] = field(default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"])
    rate_limit_requests: int = 20
    rate_limit_window_seconds: int = 60


def get_settings() -> RuntimeSettings:
    import os

    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    return RuntimeSettings(
        app_name=os.getenv("APP_NAME", "Aegis Voice"),
        environment=os.getenv("ENVIRONMENT", "development"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        default_model=os.getenv("AI_MODEL", "gpt-4o-mini"),
        max_request_size=int(os.getenv("MAX_REQUEST_SIZE", str(1024 * 1024))),
        max_conversation_messages=int(os.getenv("MAX_CONVERSATION_MESSAGES", "20")),
        max_message_chars=int(os.getenv("MAX_MESSAGE_CHARS", "2000")),
        max_history_chars=int(os.getenv("MAX_HISTORY_CHARS", "20000")),
        allowed_origins=[origin.strip() for origin in allowed_origins.split(",") if origin.strip()],
        rate_limit_requests=int(os.getenv("RATE_LIMIT_REQUESTS", "20")),
        rate_limit_window_seconds=int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60")),
    )


SETTINGS = get_settings()
