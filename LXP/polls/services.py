# polls/services.py
import os, requests

FASTAPI_URL = os.getenv("POLL_AI_URL", "http://127.0.0.1:8080/generate-poll")

def fetch_mcqs(topics: list[str], n_questions: int):
    payload = {"topics": topics, "n_questions": n_questions}
    r = requests.post(FASTAPI_URL, json=payload, timeout=30)
    r.raise_for_status()                      # raises → 4xx/5xx
    return r.json()["questions"]              # → list[dict]
