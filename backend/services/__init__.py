from __future__ import annotations

from collections import defaultdict, deque
from time import time


class RateLimiter:
    def __init__(self, requests_per_window: int, window_seconds: int) -> None:
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self._history: defaultdict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time()
        window = self._history[key]
        cutoff = now - self.window_seconds
        while window and window[0] <= cutoff:
            window.popleft()
        if len(window) >= self.requests_per_window:
            return False
        window.append(now)
        return True

    def reset(self, key: str | None = None) -> None:
        if key is None:
            self._history.clear()
        else:
            self._history.pop(key, None)
