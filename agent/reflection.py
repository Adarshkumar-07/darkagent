from __future__ import annotations

from agent.brain import Brain


class Reflection:
    def __init__(self, brain: Brain) -> None:
        self.brain = brain

    def improve(self, goal: str, execution_log: list[dict]) -> str:
        prompt = (
            f"Goal: {goal}\n"
            f"Execution log: {execution_log}\n"
            "Provide: (1) what worked, (2) what is weak, (3) improved final output, (4) next actions."
        )
        return self.brain.reason(
            system_prompt="You are a self-critic module that improves agent outputs.",
            user_prompt=prompt,
        )