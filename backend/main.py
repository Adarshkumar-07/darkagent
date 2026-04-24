from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent.main import DarkAgent

app = FastAPI(title="DarkAgent API", version="0.1.0")
agent = DarkAgent()


class RunRequest(BaseModel):
    goal: str = Field(..., min_length=3)
    max_steps: int = Field(default=6, ge=1, le=20)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/agent/run")
def run_agent(payload: RunRequest) -> dict:
    return agent.run(goal=payload.goal, max_steps=payload.max_steps)