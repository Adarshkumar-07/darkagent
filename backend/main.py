from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from backend.config import SETTINGS
from backend.models import ChatRequest, ChatResponse, ErrorResponse
from backend.security import sanitize_text, validate_conversation, validate_message_size
from backend.services.ai_service import AIService

router = APIRouter(prefix="/api")
service = AIService()


@router.post("/chat", response_model=ChatResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    client_ip = request.client.host if request.client else "unknown"
    # Rate limiting handled by app middleware before route execution.
    message = sanitize_text(payload.message)
    validate_message_size(message, SETTINGS.max_message_chars)
    validate_conversation([item.model_dump() for item in payload.conversation])

    normalized_history = [item.model_dump() for item in payload.conversation]
    try:
        reply = service.generate_reply(message, normalized_history)
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive catch for runtime provider failures
        raise HTTPException(status_code=502, detail="The AI service is currently unavailable. Please try again later.") from exc

    updated_conversation = [
        *normalized_history,
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    return ChatResponse(reply=reply, conversation=updated_conversation, status="ok")
