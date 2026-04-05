from app.llm_api import query_ollama

class InterviewerAgent:
    """AI Interviewer Agent: Asks questions and evaluates answers."""
    def __init__(self):
        self.role = "Interviewer"

    async def ask_question(self, topic: str) -> str:
        prompt = f"You are an expert technical interviewer. Ask a challenging interview question about {topic}."
        return await query_ollama(prompt)

    async def evaluate_answer(self, question: str, answer: str) -> str:
        prompt = (
            f"You are an expert interviewer. Here is the question: '{question}'. "
            f"Here is the candidate's answer: '{answer}'. Give a brief, objective evaluation."
        )
        return await query_ollama(prompt)
