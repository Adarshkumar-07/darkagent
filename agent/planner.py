from __future__ import annotations

from typing import Any

from agent.brain import Brain


class Planner:
    def __init__(self, brain: Brain) -> None:
        self.brain = brain

    def build_plan(self, goal: str, context: list[str]) -> list[dict[str, Any]]:
        prompt = f"""
        Goal: {goal}
        Context:\n- """ + "\n- ".join(context[:8]) + """

        Return JSON with shape:
        {
          "tasks": [
            {"id": 1, "title": "...", "type": "research|create|analyze|execute", "tool_hint": "web_search|filesystem|code_exec|none"}
          ]
        }
        Keep tasks practical and execution-ready.
        """
        raw = self.brain.reason(
            system_prompt="You are a senior autonomous agent planner.",
            user_prompt=prompt,
            as_json=True,
        )
        parsed = self.brain.safe_json(raw)
        tasks = parsed.get("tasks") if isinstance(parsed, dict) else None
        if not tasks:
            tasks = [
                {"id": 1, "title": "Research goal landscape", "type": "research", "tool_hint": "web_search"},
                {"id": 2, "title": "Create first draft deliverable", "type": "create", "tool_hint": "none"},
                {"id": 3, "title": "Refine deliverable", "type": "analyze", "tool_hint": "none"},
            ]
        return tasks