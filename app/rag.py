import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "regulations.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    REGULATIONS = json.load(f)

def find_best_snippet(question: str) -> tuple[str | None, str | None]:
    """
    Very dumb retrieval:
    - if a keyword appears in question, return that snippet.
    """
    q_lower = question.lower()

    keyword_map = {
        "gdpr": "gdpr",
        "dora": "dora",
        "psd2": "psd2",
        "open banking": "psd2",
        "nis2": "nis2",
        "cyber": "nis2",
    }

    target = None
    for word, tag in keyword_map.items():
        if word in q_lower:
            target = tag
            break

    if not target:
        return None, None

    for item in REGULATIONS:
        if target in [t.lower() for t in item.get("tags", [])]:
            return item["id"], item["text"]

    return None, None