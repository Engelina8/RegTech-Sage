from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    source: str | None = None  # e.g. "GDPR Art. 6"