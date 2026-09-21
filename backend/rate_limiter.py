from __future__ import annotations
from collections import defaultdict, deque
from time import monotonic

class RateLimiter:
    def __init__(self, requests_per_window: int, window_seconds: int) -> None:
        self.limit, self.window = requests_per_window, window_seconds
        self._history: defaultdict[str, deque[float]] = defaultdict(deque)
    def allow(self, key: str) -> bool:
        now, history = monotonic(), self._history[key]
        while history and history[0] <= now - self.window: history.popleft()
        if len(history) >= self.limit: return False
        history.append(now); return True
    def reset(self) -> None: self._history.clear()
