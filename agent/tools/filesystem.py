from __future__ import annotations

from pathlib import Path


def read_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return f"File not found: {path}"
    return p.read_text(encoding="utf-8")[:12000]


def write_file(path: str, content: str) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} chars to {path}"