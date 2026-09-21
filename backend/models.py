from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class Message(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["user", "assistant", "system"]
    content: str = Field(..., min_length=1, max_length=10_000)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    @field_validator("content")
    @classmethod
    def trim(cls, value: str) -> str:
        value = value.strip()
        if not value: raise ValueError("content cannot be empty")
        return value

class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., min_length=1, max_length=2_000)
    conversation: list[Message] = Field(default_factory=list, max_length=20)
    @field_validator("message")
    @classmethod
    def trim_message(cls, value: str) -> str:
        value = value.strip()
        if not value: raise ValueError("message cannot be empty")
        return value

class ChatResponse(BaseModel):
    reply: str = Field(..., min_length=1)
    conversation: list[Message]
    status: Literal["ok"] = "ok"

class ErrorResponse(BaseModel):
    detail: str
    code: str = "error"
