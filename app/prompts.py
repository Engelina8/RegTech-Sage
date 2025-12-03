# RegTech Sage prompt template and builder

SYSTEM_PROMPT = (
	"You are RegTech Sage, an expert AI assistant for explaining EU regulations (GDPR, DORA, PSD2, NIS2) in simple, business-friendly language. "
	"You are not a lawyer. Always end your answers with: 'This is general information, not legal advice.'"
)

DISCLAIMER = "This is general information, not legal advice."

def build_prompt(user_question: str, context_snippet: str = None):
	messages = [
		{"role": "system", "content": SYSTEM_PROMPT}
	]
	if context_snippet:
		messages.append({"role": "assistant", "content": context_snippet})
	messages.append({"role": "user", "content": user_question})
	return messages
