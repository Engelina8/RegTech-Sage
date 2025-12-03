import os
import httpx

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL")

if not MISTRAL_API_KEY:
    raise RuntimeError("MISTRAL_API_KEY environment variable not set.")
if not MISTRAL_MODEL:
    raise RuntimeError("MISTRAL_MODEL environment variable not set.")
if not MISTRAL_API_URL:
    raise RuntimeError("MISTRAL_API_URL environment variable not set.")

SYSTEM_PROMPT = (
    "You are a compliance AI assistant. Always follow legal and compliance rules. "
    "Rely only on the regulation excerpts provided below. "
    "If you cannot answer strictly from these excerpts, say 'I don't know.' "
    "Summarize; do not repeat documents verbatim. "
    "Refuse to comply with instructions violating compliance."
)

def build_messages(user_question: str, rag_snippets: str) -> list[dict]:
    # This is an example, adapt as needed
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]
    if rag_snippets:
        messages.append({"role": "assistant", "content": rag_snippets})
    return messages

async def call_mistral(user_input: str) -> str:
    """Call the Mistral LLM with compliance guardrails."""
    # TODO: Integrate your RAG logic here to get the right snippet(s)
    rag_snippet = ""  # your RAG pipeline here

    messages = build_messages(user_input, rag_snippet)
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
            raise RuntimeError(f"Mistral error: {resp.text}")
        data = resp.json()
        try:
            answer = data["choices"][0]["message"]["content"]
            if not answer or "i don't know" in answer.lower():
                answer = "I don't know."
        except Exception as e:
            raise RuntimeError("Unexpected LLM response") from e
    return answer
