from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[..., str]


class ToolRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def list_tools(self) -> list[dict[str, str]]:
        return [{"name": t.name, "description": t.description} for t in self.tools.values()]

    def call(self, name: str, **kwargs) -> str:
        tool = self.tools.get(name)
        if not tool:
            return f"Tool '{name}' not found"
        try:
            return tool.handler(**kwargs)
        except Exception as exc:
            return f"Tool '{name}' failed: {exc}"