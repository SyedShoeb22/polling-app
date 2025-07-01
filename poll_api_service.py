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
        "Q: Question?\nA. ...\nB. ...\nC. ...\nD. ...\nAnswer: B"
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
    blocks = re.split(r"\nQ\d+:\s*", "\n" + raw.strip())  # Split on Q1:, Q2:, etc.

    for block in blocks:
        if not block.strip():
            continue

        lines = block.strip().split("\n")
        if len(lines) < 6:
            continue

        question = lines[0].strip()
        options = []
        for line in lines[1:5]:
            if ". " in line:
                options.append(line.split(". ", 1)[1].strip())

        # Find answer line
        answer_line = next((l for l in lines if l.lower().startswith("answer")), "")
        answer_match = re.match(r"Answer:\s*([A-Da-d])", answer_line)

        if answer_match and len(options) == 4:
            answer_letter = answer_match.group(1).upper()
            answer_index = {"A": 0, "B": 1, "C": 2, "D": 3}.get(answer_letter, -1)

            if 0 <= answer_index < 4:
                questions.append(PollQuestion(
                    question=question,
                    options=options,
                    answer_index=answer_index
                ))

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
    uvicorn.run("poll_ai_service:app", host="0.0.0.0", port=8080, reload=True)
