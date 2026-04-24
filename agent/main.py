from __future__ import annotations

from collections import deque
from typing import Any

from agent.brain import Brain
from agent.executor import Executor
from agent.memory import Memory
from agent.planner import Planner
from agent.reflection import Reflection
from agent.tools.base import Tool, ToolRegistry
from agent.tools.code_exec import run_python
from agent.tools.filesystem import read_file, write_file
from agent.tools.web_search import web_search


class DarkAgent:
    """Autonomous agent implementing observe → think → plan → act → reflect."""

    def __init__(self) -> None:
        self.brain = Brain()
        self.memory = Memory()
        self.tools = self._build_tools()
        self.planner = Planner(self.brain)
        self.executor = Executor(self.brain, self.tools)
        self.reflection = Reflection(self.brain)

    def _build_tools(self) -> ToolRegistry:
        registry = ToolRegistry()
        registry.register(Tool("read_file", "Read file from disk", read_file))
        registry.register(Tool("write_file", "Write file to disk", write_file))
        registry.register(Tool("web_search", "Search web information", web_search))
        registry.register(Tool("run_python", "Execute short Python code", run_python))
        return registry

    def run(self, goal: str, max_steps: int = 6) -> dict[str, Any]:
        self.memory.add_short_term("user", goal)

        # Observe
        recalled = self.memory.search_long_term(goal, top_k=5)

        # Think/Plan
        plan = self.planner.build_plan(goal=goal, context=recalled)
        queue = deque(plan)

        execution_log: list[dict[str, Any]] = []

        # Act
        steps = 0
        while queue and steps < max_steps:
            task = queue.popleft()
            result = self.executor.execute_task(goal=goal, task=task)
            execution_log.append(result)
            self.memory.add_short_term("assistant", str(result))
            self.memory.add_long_term(str(result), metadata={"goal": goal, "task": task.get("title", "")})
            steps += 1

        # Reflect
        improved = self.reflection.improve(goal=goal, execution_log=execution_log)
        self.memory.add_short_term("assistant", improved)
        self.memory.add_long_term(improved, metadata={"goal": goal, "phase": "reflection"})

        return {
            "goal": goal,
            "plan": plan,
            "execution_log": execution_log,
            "reflection": improved,
            "short_term_memory": self.memory.get_short_term(),
            "tools": self.tools.list_tools(),
        }