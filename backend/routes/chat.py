from __future__ import annotations
from fastapi import APIRouter, HTTPException, Request
from backend.config import SETTINGS
from backend.models import ChatRequest, ChatResponse, ErrorResponse
from backend.security import sanitize_text, validate_conversation, validate_message_size
from backend.services.ai_service import AIService

router = APIRouter(prefix="/api")
service = AIService()

@router.post("/chat", response_model=ChatResponse, responses={400:{"model":ErrorResponse}, 503:{"model":ErrorResponse}})
async def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    message = sanitize_text(payload.message)
    try:
        validate_message_size(message, SETTINGS.max_message_chars)
        history = [item.model_dump() for item in payload.conversation]
        validate_conversation(history)
        reply = service.generate_reply(message, history)
    except ValueError as exc: raise HTTPException(400, str(exc)) from exc
    except RuntimeError as exc: raise HTTPException(503, str(exc)) from exc
    except Exception as exc: raise HTTPException(502, "The AI service is temporarily unavailable") from exc
    return ChatResponse(reply=reply, conversation=[*history, {"role":"user","content":message}, {"role":"assistant","content":reply}])
