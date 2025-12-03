from mistral_client import MistralClient

class RegTechSageChatbot:
    SYSTEM_PROMPT = (
        "You are RegTech Sage, an expert advisor on regulatory compliance for regulated industries. "
        "Explain PSD2, DORA, GDPR, NIS2, and digital sovereignty in clear, business-friendly language. "
        "Provide high-level guidance on secure data sharing, governance, and compliance best practices. "
        "Do not provide legal advice or implementation-level security exploits. Maintain a professional, concise tone."
    )

    def __init__(self):
        self.client = MistralClient()

    def ask(self, user_input):
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        response = self.client.send_message(messages)
        return response["choices"][0]["message"]["content"]
