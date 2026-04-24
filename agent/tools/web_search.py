from __future__ import annotations

import requests


def web_search(query: str, limit: int = 5) -> str:
    """Simple DuckDuckGo instant answer endpoint wrapper."""
    endpoint = "https://api.duckduckgo.com/"
    response = requests.get(endpoint, params={"q": query, "format": "json", "no_html": 1}, timeout=20)
    response.raise_for_status()
    payload = response.json()

    lines = []
    if payload.get("AbstractText"):
        lines.append(f"Abstract: {payload['AbstractText']}")

    related = payload.get("RelatedTopics", [])
    for item in related[:limit]:
        text = item.get("Text") if isinstance(item, dict) else None
        if text:
            lines.append(f"- {text}")

    return "\n".join(lines) if lines else "No useful search results returned."