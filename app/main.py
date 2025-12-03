from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx

from .config import MISTRAL_API_KEY, MISTRAL_MODEL, MISTRAL_API_URL
from .models import ChatRequest, ChatResponse
from .prompts import build_prompt
from .rag import find_best_snippet

app = FastAPI(title="RegTech Sage")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve simple HTML UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Empty question")

    # mini input guardrail
    if len(req.question) > 1000:
        raise HTTPException(status_code=400, detail="Question too long")

    # mini-RAG
    snippet_id, snippet_text = find_best_snippet(req.question)

    messages = build_prompt(req.question, snippet_text)

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MISTRAL_MODEL,
        "messages": messages,
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(MISTRAL_API_URL, headers=headers, json=payload)
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Mistral error: {resp.text}")

        data = resp.json()
        # Adjust to actual Mistral response shape if needed
        try:
            answer = data["choices"][0]["message"]["content"]
        except Exception:
            raise HTTPException(status_code=500, detail="Unexpected LLM response")

    return ChatResponse(answer=answer, source=snippet_id)