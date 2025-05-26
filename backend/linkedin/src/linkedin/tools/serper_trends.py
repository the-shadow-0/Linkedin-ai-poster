import os
import requests

def serper_trends() -> str:
    """Return today’s top trending topics via Serper.dev."""
    api_key = os.getenv("461dacfe42a399654a3a4f6a8f3a1be54c2fffba")
    resp = requests.get(
        "https://google.serper.dev/trends",
        headers={"X-API-KEY": api_key}
    )
    topics = resp.json().get("trends", [])[:3]
    return "\n".join(f"{i+1}. {t['title']}" for i, t in enumerate(topics))
