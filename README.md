# Aegis Voice

Aegis Voice is a responsive browser voice assistant built on the existing DarkAgent FastAPI foundation. It combines Web Speech API input, a secure server-side OpenAI integration, short-term conversation context, local commands, and browser speech synthesis.

## Architecture

- `frontend/`: React + TypeScript + Vite UI. `api.ts` is the typed API boundary; hooks isolate recognition and synthesis; `commands.ts` contains local commands; `state.ts` documents valid assistant transitions.
- `backend/`: FastAPI API, strict Pydantic models, request-size/CORS/rate-limit middleware, input validation, and server-only OpenAI client.
- Conversation history is kept in the current browser session and sent as bounded context with each request. Export is a client-side JSON download.

## Features

Voice input with interim transcript, typed fallback, IDLE/LISTENING/PROCESSING/SPEAKING/ERROR states, automatic speech toggle, pause/resume/stop, voice selection, themes, settings, timestamps, local commands, clear/new/export actions, defensive API errors, and responsive layouts.

## Setup

### Backend

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
# Set OPENAI_API_KEY in .env
uvicorn backend.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Set `VITE_API_BASE_URL` to the backend origin when it is not `http://localhost:8000`.

## Commands

Say or type `clear conversation`, `new conversation`, `stop speaking`, `start listening`, `open settings`, or `close settings`. `what time is it` is handled locally.

## Validation commands

```bash
pytest -q
cd frontend && npm test && npm run build
```

## Deployment

Build the frontend with `npm run build` and serve `frontend/dist` over HTTPS. Run FastAPI behind a TLS reverse proxy with a production `ALLOWED_ORIGINS` value and a secret `OPENAI_API_KEY`. Never put provider keys in Vite variables.

## Security

The API uses strict schemas, bounded message/history sizes, explicit CORS origins, request-size protection, in-memory IP rate limiting, server-side secrets, and text-only React rendering. Production deployments should add a durable distributed rate limiter, authentication, HTTPS, structured logging, and secret rotation.

## Browser limitations

SpeechRecognition is not available in every browser and can require a secure context and microphone permission. SpeechSynthesis voices are browser/OS supplied and may load asynchronously. Typed chat remains available when voice features are unsupported.
