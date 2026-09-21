from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.config import SETTINGS
from backend.rate_limiter import RateLimiter
from backend.routes.chat import router

app = FastAPI(title=SETTINGS.app_name, version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=SETTINGS.allowed_origins, allow_credentials=False, allow_methods=["POST","GET"], allow_headers=["Content-Type"])
limiter = RateLimiter(SETTINGS.rate_limit_requests, SETTINGS.rate_limit_window_seconds)
@app.middleware("http")
async def protections(request: Request, call_next):
    if request.headers.get("content-length") and int(request.headers["content-length"]) > SETTINGS.max_request_size:
        return JSONResponse({"detail":"request is too large","code":"request_too_large"}, status_code=413)
    if request.url.path == "/api/chat" and request.method == "POST":
        ip = request.client.host if request.client else "unknown"
        if not limiter.allow(ip): return JSONResponse({"detail":"rate limit exceeded","code":"rate_limited"}, status_code=429)
    return await call_next(request)
@app.get("/health")
def health() -> dict[str, str]: return {"status":"ok"}
app.include_router(router)
