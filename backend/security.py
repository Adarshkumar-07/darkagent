from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Message(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: Annotated[Literal["user", "assistant", "system"], Field(...)]
    content: Annotated[str, Field(..., min_length=1, max_length=10000)]
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @field_validator("content")
    @classmethod
    def clean_content(cls, value: str) -> str:
        return value.strip()


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: Annotated[str, Field(..., min_length=1, max_length=2000)]
    conversation: list[Message] = Field(default_factory=list)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        sanitized = value.strip()
        if not sanitized:
            raise ValueError("message cannot be empty")
        return sanitized


class ChatResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reply: str
    conversation: list[Message] = Field(default_factory=list)
    status: Literal["ok", "error"] = "ok"


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detail: str
    code: str = "validation_error"
