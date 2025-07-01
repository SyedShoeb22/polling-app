# 🗳️ Poll AI Generator API

This is a FastAPI-based microservice that generates multiple-choice questions (MCQs) from any topic using **LLMs via OpenRouter**.

### ✨ Features

- ✅ Accepts a list of topics, generates MCQs
- 🧠 Uses a free/open-source LLM (via OpenRouter API)
- 💡 Smart fallback to built-in questions when model fails
- 🚀 Built with FastAPI and ready for deployment

---

## 🚀 How to Run

### 1. Clone this Repo

```bash
git clone https://github.com/your-username/poll-ai-service.git
cd poll-ai-service
2. Set up the Environment
Create a .env file:
```
```bash

cp .env.example .env
Inside .env, add your OpenRouter API key:
```
```bash
OPENROUTER_API_KEY=your-openrouter-key-here
```
3. Install Requirements
```bash

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
4. Start the Server
```bash

uvicorn poll_ai_service:app --host 0.0.0.0 --port 8080 --reload
```
🧪 Example API Request
POST /generate-poll
```bash

curl -X POST http://localhost:8080/generate-poll \
  -H "Content-Type: application/json" \
  -d '{
    "topics": ["Java Collections"],
    "n_questions": 2
}'
```
Sample Response:
```bash
{
  "questions": [
    {
      "question": "Which collection maintains insertion order?",
      "options": ["HashSet", "TreeSet", "LinkedHashSet", "ConcurrentSkipListSet"],
      "answer_index": 2
    },
    {
      "question": "Which collection is thread-safe?",
      "options": ["ArrayList", "HashSet", "Vector", "LinkedList"],
      "answer_index": 2
    }
  ],
  "source": "openrouter"
}
```
