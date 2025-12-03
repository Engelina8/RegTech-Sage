BASE_SYSTEM_PROMPT = """
You are RegTech Sage, a helpful compliance assistant for EU regulations
(GDPR, DORA, PSD2, NIS2). You are NOT a lawyer and do not give formal
legal advice.

Rules:
- Explain in simple, clear language.
- If you reference a regulation, mention the name and article when possible.
- If you are unsure, say so and suggest consulting a compliance officer or lawyer.
- Always end with this disclaimer:
  "This is general information, not legal advice."
"""

def build_prompt(user_question: str, context_snippet: str | None = None) -> list[dict]:
    messages = [{"role": "system", "content": BASE_SYSTEM_PROMPT.strip()}]
    if context_snippet:
        messages.append({
            "role": "system",
            "content": f"Relevant regulatory context:\n{context_snippet}"
        })
    messages.append({"role": "user", "content": user_question})
    return messages