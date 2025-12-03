# RegTech Sage

A containerized chatbot for EU regulatory compliance assistance (GDPR, DORA, PSD2, NIS2).

## Tech Stack
- FastAPI for the backend
- Mistral AI API for LLM
- Simple keyword-based RAG over JSON snippets
- Docker for containerization
- Basic HTML/JS UI

## How to Run Locally
1. Clone the repo.
2. Create `.env` from `.env.example` and add your Mistral API key.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --reload`
5. Open http://127.0.0.1:8000/static/index.html

## How to Run with Docker
1. Build: `docker build -t regtech-sage .`
2. Run: `docker run -p 8000:8000 --env-file .env regtech-sage`
3. Open http://localhost:8000/static/index.html

## Limitations & Next Steps
- Retrieval is basic; add vector DB for production.
- Expand regulations.json.
- Add authentication and more guardrails.