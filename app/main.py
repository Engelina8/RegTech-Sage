from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx

from .config import MISTRAL_API_KEY, MISTRAL_MODEL, MISTRAL_API_URL
from .models import ChatRequest, ChatResponse
from .prompts import build_prompt
from .rag import find_best_snippet

from typing import Tuple, Optional

PII_KEYWORDS = ["email", "phone", "address", "name", "passport", "client id"]
BLOCKED_OUTPUT_PHRASES = ["ignore gdpr", "bypass compliance", "illegal"]
COMPLIANCE_DISCLAIMER = (
    "\n\n⚠️ Compliance Notice: This answer is for guidance only and does not replace professional legal advice."
)

def validate_input(user_input: str) -> Tuple[bool, Optional[str]]:
    if len(user_input) > 1000:
        return False, "Input too long. Please shorten your question."
    lowered = user_input.lower()
    for keyword in PII_KEYWORDS:
        if keyword in lowered:
            return False, "Please do not include personal data (PII)."
    return True, None

def sanitize_output(text: str) -> str:
    lowered = text.lower()
    for phrase in BLOCKED_OUTPUT_PHRASES:
        if phrase in lowered:
            return (
                "I cannot provide or validate information that conflicts with compliance or legal requirements."
            )
    return text

def add_disclaimer(text: str) -> str:
    return f"{text}{COMPLIANCE_DISCLAIMER}"

def process_output(text: str) -> str:
    sanitized = sanitize_output(text)
    with_disclaimer = add_disclaimer(sanitized)
    return with_disclaimer

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
    user_input = req.question.strip()
    if not user_input:
        raise HTTPException(status_code=400, detail="Empty question")

    ok, error_message = validate_input(user_input)
    if not ok:
        raise HTTPException(status_code=400, detail=error_message)

    # mini-RAG
    snippet_id, snippet_text = find_best_snippet(user_input)
    messages = build_prompt(user_input, snippet_text)

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
        try:
            answer = data["choices"][0]["message"]["content"]
        except Exception:
            raise HTTPException(status_code=500, detail="Unexpected LLM response")

    processed_answer = process_output(answer)
    return ChatResponse(answer=processed_answer, source=snippet_id)
