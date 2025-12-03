# Minimal keyword-based retrieval for regulations
import json
import os

REGULATIONS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'regulations.json')

try:
	with open(REGULATIONS_PATH, encoding='utf-8') as f:
		REGULATIONS = json.load(f)
except Exception:
	REGULATIONS = []

KEYWORDS = [
	("gdpr", ["gdpr", "general data protection regulation"]),
	("dora", ["dora", "digital operational resilience act"]),
	("psd2", ["psd2", "payment services directive"]),
	("nis2", ["nis2", "network and information security"]),
	("cyber", ["cyber", "cybersecurity"]),
	("open_banking", ["open banking"])
]

def retrieve_snippet(user_question: str):
	q = user_question.lower()
	for key, variants in KEYWORDS:
		if any(word in q for word in variants):
			for snippet in REGULATIONS:
				if snippet.get("id", "").lower() == key:
					return snippet.get("id"), snippet.get("text")
	return None, None
