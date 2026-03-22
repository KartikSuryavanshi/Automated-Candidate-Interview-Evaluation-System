from app.llm_api import query_ollama

class CandidateProxy:
    """Candidate Proxy: Simulates or relays candidate responses."""
    def __init__(self):
        self.role = "Candidate"

    async def answer_question(self, question: str) -> str:
        prompt = f"You are a job candidate. Here is the interview question: '{question}'. Give your best answer."
        return await query_ollama(prompt)
