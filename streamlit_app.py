

# --- Begin Refactored Streamlit App ---
import streamlit as st
import os
import httpx
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-medium")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai/v1/chat/completions")

# Prompt template
SYSTEM_PROMPT = (
    "You are RegTech Sage, an expert AI assistant for explaining EU regulations (GDPR, DORA, PSD2, NIS2) in simple, business-friendly language. "
    "You are not a lawyer. Always end your answers with: 'This is general information, not legal advice.'"
)
DISCLAIMER = "This is general information, not legal advice."

# Load regulations for RAG
DATA_PATH = Path(__file__).resolve().parent / "data" / "regulations.json"
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        REGULATIONS = json.load(f)
except Exception:
    REGULATIONS = []

def find_best_snippet(question: str):
    q_lower = question.lower()
    keyword_map = {
        "gdpr": "gdpr",
        "dora": "dora",
        "psd2": "psd2",
        "open banking": "psd2",
        "nis2": "nis2",
        "cyber": "nis2",
    }
    target = None
    for word, tag in keyword_map.items():
        if word in q_lower:
            target = tag
            break
    if not target:
        return None, None
    for k, v in REGULATIONS.items() if isinstance(REGULATIONS, dict) else []:
        if target in k.lower():
            return k, v
    return None, None

def build_prompt(user_question: str, context_snippet: str = None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    if context_snippet:
        messages.append({"role": "assistant", "content": context_snippet})
    messages.append({"role": "user", "content": user_question})
    return messages

def call_mistral(messages):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MISTRAL_MODEL,
        "messages": messages,
        "temperature": 0.2,
    }
    try:
        resp = httpx.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error contacting Mistral API: {e}"

def add_disclaimer(text: str) -> str:
    if DISCLAIMER not in text:
        return f"{text}\n\n{DISCLAIMER}"
    return text

st.set_page_config(page_title="RegTech Sage Chatbot", page_icon="🤖")
st.title("RegTech Sage: EU Compliance Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []


user_input = st.text_input("Ask a compliance question:", "")
if st.button("Send") and user_input.strip():
    st.session_state["messages"].append(("user", user_input))
    snippet_id, snippet_text = find_best_snippet(user_input)
    # Only call LLM if question is in scope
    if snippet_id is not None:
        messages = build_prompt(user_input, snippet_text)
        answer = call_mistral(messages)
        answer = add_disclaimer(answer)
        st.session_state["messages"].append(("bot", answer))
    else:
        st.session_state["messages"].append(("bot", "Outside of scope. This assistant only answers questions about EU regulations and compliance.\n\nThis is general information, not legal advice."))

for role, msg in st.session_state["messages"]:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**RegTech Sage:** {msg}")
