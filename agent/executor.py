from __future__ import annotations

from typing import Any

from agent.brain import Brain
from agent.tools.base import ToolRegistry


class Executor:
    def __init__(self, brain: Brain, tools: ToolRegistry) -> None:
        self.brain = brain
        self.tools = tools

    def execute_task(self, goal: str, task: dict[str, Any], retries: int = 2) -> dict[str, Any]:
        title = task.get("title", "untitled")
        task_type = task.get("type", "analyze")
        tool_hint = task.get("tool_hint", "none")

        for attempt in range(retries + 1):
            try:
                if tool_hint in {"web_search", "filesystem", "code_exec"}:
                    result = self._execute_with_tool(goal, title, tool_hint)
                else:
                    result = self.brain.reason(
                        system_prompt="You execute practical tasks toward a goal.",
                        user_prompt=f"Goal: {goal}\nTask: {title}\nTask type: {task_type}\nProduce concise output.",
                    )
                return {"status": "ok", "task": title, "attempt": attempt + 1, "result": result}
            except Exception as exc:
                err = str(exc)
                if attempt == retries:
                    return {"status": "error", "task": title, "attempt": attempt + 1, "result": err}

        return {"status": "error", "task": title, "attempt": retries + 1, "result": "unknown"}

    def _execute_with_tool(self, goal: str, title: str, tool_hint: str) -> str:
        if tool_hint == "web_search":
            query = f"{goal} {title}"
            return self.tools.call("web_search", query=query)

        if tool_hint == "filesystem":
            filename = "outputs/agent_notes.md"
            content = f"# Goal\n{goal}\n\n# Task\n{title}\n"
            return self.tools.call("write_file", path=filename, content=content)

        if tool_hint == "code_exec":
            code = "print('quick check: task execution path working')"
            return self.tools.call("run_python", code=code)

        return "No compatible tool selected."