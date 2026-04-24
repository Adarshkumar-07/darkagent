# DarkAgent

DarkAgent is an autonomous AI agent platform (AutoGPT/BabyAGI style), built around a true multi-step loop:

`observe → think → plan → act → reflect`

## Step-by-step roadmap

1. **Foundation (done)**
   - Build modular agent components: Brain, Memory, Planner, Executor, Reflection.
   - Expose orchestration through FastAPI backend.
2. **Tool expansion (next)**
   - Add richer tool routing and structured tool arguments.
   - Add authenticated provider adapters for external APIs.
3. **Memory upgrades**
   - Swap cheap embeddings with OpenAI/SBERT embeddings.
   - Add episodic memory summarization and retention policies.
4. **Agent safety and governance**
   - Add policy checks per tool/action.
   - Add run budgets and user approval gates for risky actions.
5. **Frontend + observability**
   - Build run dashboard (task queue, token usage, error traces).
   - Add traces, metrics, and replay for agent runs.
6. **Deployment hardening**
   - Containerize services and deploy to cloud with persistent volumes.

## Architecture diagram (text)

```
[User Goal]
    |
    v
[FastAPI /agent/run]
    |
    v
[DarkAgent Orchestrator]
    |
    +--> Observe: retrieve context from Long-Term Memory (Chroma)
    +--> Think/Plan: Brain + Planner -> Task Queue
    +--> Act: Executor -> Tool Registry -> {filesystem, web_search, code_exec}
    +--> Reflect: Reflection module improves final output
    +--> Persist: Short-Term Memory + Long-Term Memory
    |
    v
[Final Structured Response]
```

## Project structure

```
agent/
  brain.py
  memory.py
  planner.py
  executor.py
  reflection.py
  main.py
  tools/
    base.py
    filesystem.py
    web_search.py
    code_exec.py

backend/
  main.py

frontend/
  README.md
```

## Example flow: "Help me earn money on Fiverr"

DarkAgent run behavior:
1. Analyze goal intent and recall relevant memory.
2. Create a task queue (niche research, gig creation, description generation).
3. Execute tasks with tools and LLM reasoning.
4. Reflect over outputs and improve quality.
5. Store artifacts/results to long-term memory for future reuse.

## Core implementation highlights

- **Goal-based loop** with explicit planner + executor separation.
- **Task queue system** (`deque`) for multi-step execution.
- **Retry & error handling** in executor task runs.
- **Tool-calling subsystem** via `ToolRegistry` abstraction.
- **Memory system**:
  - short-term chat trace (rolling deque)
  - long-term persistent vector memory via ChromaDB
- **Reflection loop** to critique and improve final output.

## Libraries required

- FastAPI
- Uvicorn
- Pydantic
- OpenAI Python SDK
- ChromaDB
- requests
- python-dotenv

Install:

```bash
pip install -r requirements.txt
```

## Running locally

```bash
uvicorn backend.main:app --reload
```

Then call:

```bash
curl -X POST http://127.0.0.1:8000/agent/run \
  -H 'Content-Type: application/json' \
  -d '{"goal": "Help me earn money on Fiverr", "max_steps": 6}'
```

## Deployment guide

1. Create Docker image with `python:3.11-slim`.
2. Copy project, `pip install -r requirements.txt`.
3. Mount persistent volume for `.darkagent_memory`.
4. Set environment variables:
   - `OPENAI_API_KEY` (optional but recommended)
   - `DARKAGENT_MODEL` (default `gpt-4o-mini`)
5. Run with `uvicorn backend.main:app --host 0.0.0.0 --port 8000`.
6. Put behind reverse proxy (Nginx/Caddy) and HTTPS.

## Differentiation

### DarkAgent vs ChatGPT

- ChatGPT typically responds in a single conversational turn.
- DarkAgent converts goal -> actionable task queue -> tool execution -> self-reflection.
- DarkAgent persists memory across runs to improve future actions.

### DarkAgent vs normal AI SaaS tools

- Typical SaaS wrappers are one-shot prompts with templates.
- DarkAgent is autonomous and stateful:
  - dynamic planning
  - multi-step execution
  - real tool use
  - iterative self-improvement
  
  # Frontend (placeholder)

This folder is reserved for a future React/Next.js interface that will:
- submit goals to `POST /agent/run`
- stream intermediate task execution states
- visualize memory and reflection traces