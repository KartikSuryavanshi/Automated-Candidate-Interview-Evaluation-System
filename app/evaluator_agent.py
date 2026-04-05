from app.llm_api import query_ollama

class EvaluatorAgent:
    """Evaluator Agent: Provides real-time feedback and final recommendation."""
    def __init__(self):
        self.role = "Evaluator"

    async def give_feedback(self, question: str, answer: str) -> str:
        prompt = (
            f"You are an expert technical evaluator. Here is the question: '{question}'. "
            f"Here is the candidate's answer: '{answer}'. Give constructive feedback and a score out of 10."
        )
        return await query_ollama(prompt)

    async def final_recommendation(self, transcript: str) -> str:
        prompt = (
            f"You are an evaluator. Here is the full interview transcript: {transcript}. "
            f"Summarize the candidate's performance and give a final hire/no-hire recommendation."
        )
        return await query_ollama(prompt)
