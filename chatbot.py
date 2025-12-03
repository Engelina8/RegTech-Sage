import logging
import re
from typing import Tuple, Optional
from mistral_client import MistralClient

PII_KEYWORDS = ["email", "phone", "address", "name", "passport", "client id"]
MALICIOUS_PROMPTS = [
    "ignore previous instructions",
    "bypass compliance",
    "ignore gdpr"
]
BLOCKED_OUTPUT_PHRASES = ["ignore gdpr", "bypass compliance", "illegal"]
COMPLIANCE_DISCLAIMER = (
    "\n\n⚠️ Compliance Notice: This answer is for guidance only and does not replace professional legal advice."
)
SENSITIVE_PATTERNS = [r"sk-\w{32,}", r"api[_-]?key\s*=\s*\w+", r"token\s*=\s*\w+"]

logger = logging.getLogger(__name__)

def safe_log(message: str) -> None:
    """Redact sensitive keys from log messages."""
    redacted = message
    for pattern in SENSITIVE_PATTERNS:
        redacted = re.sub(pattern, "[REDACTED]", redacted, flags=re.IGNORECASE)
    logger.info(redacted)

def validate_input(user_input: str) -> Tuple[bool, Optional[str]]:
    """Check for length, PII, and adversarial instructions."""
    if len(user_input) > 1000:
        return False, "Input too long. Please shorten your question."
    lowered = user_input.lower()
    for keyword in PII_KEYWORDS:
        if keyword in lowered:
            return False, "Please do not include personal data (PII)."
    for bad in MALICIOUS_PROMPTS:
        if bad in lowered:
            return False, "I cannot comply with this request because it conflicts with compliance and security requirements."
    return True, None

def sanitize_output(text: str) -> str:
    """Block dangerous output."""
    lowered = text.lower()
    for phrase in BLOCKED_OUTPUT_PHRASES:
        if phrase in lowered:
            return "I cannot provide or validate information that conflicts with compliance or legal requirements."
    return text

def add_disclaimer(text: str) -> str:
    """Add compliance disclaimer."""
    return f"{text}{COMPLIANCE_DISCLAIMER}"

def process_output(text: str) -> str:
    """Sanitize and append disclaimer."""
    sanitized = sanitize_output(text)
    with_disclaimer = add_disclaimer(sanitized)
    return with_disclaimer

class RegTechSageChatbot:
    SYSTEM_PROMPT = (
        "You are RegTech Sage, an expert advisor on regulatory compliance for regulated industries. "
        "Explain PSD2, DORA, GDPR, NIS2, and digital sovereignty in clear, business-friendly language. "
        "Provide high-level guidance on secure data sharing, governance, and compliance best practices. "
        "Do not provide legal advice or implementation-level security exploits. Maintain a professional, concise tone. "
        "Always follow compliance rules, rely on provided legal text or snippets, say 'I don't know' if not sure, and never repeat documents verbatim."
    )

    def __init__(self):
        self.client = MistralClient()

    def ask(self, user_input: str) -> str:
        """Main chat entry point with all guardrails."""
        valid, error_message = validate_input(user_input)
        if not valid:
            safe_log(f"Rejected user input: {error_message}")
            return error_message

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        response = self.client.send_message(messages)
        answer = response["choices"][0]["message"]["content"]
        return process_output(answer)
