import os
import requests
import re
from typing import List
from dotenv import load_dotenv


load_dotenv(dotenv_path="/workspaces/polling-app/.env")

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def build_prompt(topics: List[str], n_questions: int) -> str:
    return (
        f"Generate {n_questions} multiple choice questions about {', '.join(topics)}. "
        "Each question should have 4 options labeled A, B, C, and D. Provide the correct answer after each question in the format:\n"
        "Q1: Question?\nA. ...\nB. ...\nC. ...\nD. ...\nAnswer: B"
    )

def ask_openrouter(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 512
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise Exception(f"OpenRouter API error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]

def parse_mcqs(raw: str) -> List[dict]:
    questions = []
    blocks = re.split(r"\nQ\d+:\s*", "\n" + raw.strip())

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

        answer_line = next((l for l in lines if l.lower().startswith("answer")), "")
        match = re.match(r"Answer:\s*([A-Da-d])", answer_line)

        if match and len(options) == 4:
            index = {"A": 0, "B": 1, "C": 2, "D": 3}.get(match.group(1).upper(), -1)
            if 0 <= index < 4:
                questions.append({
                    "question": question,
                    "options": options,
                    "answer_index": index
                })

    return questions
