import os
import random
import logging
import requests
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv(dotenv_path="/workspaces/polling-app/.env")

# FastAPI setup
app = FastAPI()
logger = logging.getLogger("poll_ai_service")
logging.basicConfig(level=logging.INFO)

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Request/Response models
class PollRequest(BaseModel):
    topics: List[str]
    n_questions: int = 3

class PollQuestion(BaseModel):
    question: str
    options: List[str]
    answer_index: int

class PollResponse(BaseModel):
    questions: List[PollQuestion]
    source: str

# Build prompt for LLM
def build_prompt(topics: List[str], n_questions: int) -> str:
    return (
        f"Generate {n_questions} multiple choice questions about {', '.join(topics)}. "
        "Each question should have 4 options labeled A, B, C, and D. Provide the correct answer after each question in the format:\n"
        "Q: Question?\nA. ...\nB. ...\nC. ...\nD. ...\nAnswer: B, Dont include any explanations or additional text."
        
    )

# Call OpenRouter
def ask_openrouter(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 512
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        logger.error(f"OpenRouter API error: {response.text}")
        raise HTTPException(status_code=502, detail="OpenRouter API error")

    return response.json()["choices"][0]["message"]["content"]

# Parse LLM output
import re
def parse_mcqs(raw: str) -> List[PollQuestion]:
    questions = []

    # split on either “1.”  …  or “Q1:”  …  etc.
    blocks = re.split(r"\n\s*(?:\d+\.\s*|Q\d+:)\s*", "\n" + raw.strip())

    for block in blocks:
        if not block.strip():
            continue

        lines = block.strip().split("\n")
        question = None
        options = []
        answer_index = -1

        for line in lines:
            line = line.strip()

            # first non‑option line becomes the question text
            if not question and not re.match(r"^[A-Da-d][).]\s+", line):
                question = line
            # option lines “A. …” / “B) …”
            elif re.match(r"^[A-Da-d][).]\s+", line):
                options.append(line[3:].strip())
            # answer line – pick first A‑D letter, ignore extra text
            elif line.lower().startswith("answer"):
                m = re.search(r"Answer:\s*([A-Da-d])\b", line)
                if m:
                    answer_index = "ABCD".index(m.group(1).upper())

        if question and len(options) == 4 and 0 <= answer_index < 4:
            questions.append(
                PollQuestion(
                    question=question,
                    options=options,
                    answer_index=answer_index,
                )
            )

    return questions




# Endpoint
@app.post("/generate-poll", response_model=PollResponse)
def generate_poll(req: PollRequest):
    prompt = build_prompt(req.topics, req.n_questions)
    try:
        raw = ask_openrouter(prompt)
        questions = parse_mcqs(raw)
        print("=== RAW OUTPUT ===")
        print(raw)

        if not questions:
            raise ValueError("No valid questions parsed.")
        return PollResponse(questions=questions[:req.n_questions], source="openrouter")
    except Exception as e:
        logger.exception("Poll generation failed")
        raise HTTPException(status_code=502, detail=f"Poll generation failed: {str(e)}")

# Health check
@app.get("/healthz")
def healthz():
    return {"status": "ok", "model": MODEL_NAME}

# Run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("poll_api_service:app", host="127.0.0.1", port=8080, reload=True)