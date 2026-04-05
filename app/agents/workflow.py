from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict

from autogen_agentchat.agents import AssistantAgent

from app.core.autogen_client import build_model_client


@dataclass
class InterviewTurn:
    question: str
    answer: str
    feedback: str


@dataclass
class InterviewSession:
    topic: str
    turns: List[InterviewTurn] = field(default_factory=list)
    last_question: str = ""


class AriesWorkflow:
    def __init__(self) -> None:
        self.model_client = build_model_client()
        self.interviewer = AssistantAgent(
            name="interviewer_agent",
            model_client=self.model_client,
            system_message=(
                "You are an interviewer agent for technical screening. "
                "Ask one concise, practical interview question at a time."
            ),
        )
        self.candidate_proxy = AssistantAgent(
            name="candidate_proxy_agent",
            model_client=self.model_client,
            system_message=(
                "You are candidate_proxy_agent. "
                "Summarize the candidate answer in one line with no judgment."
            ),
        )
        self.evaluator = AssistantAgent(
            name="evaluation_agent",
            model_client=self.model_client,
            system_message=(
                "You are an evaluation agent. "
                "Evaluate the candidate answer with score out of 10 and short justification."
            ),
        )

    async def start_interview(self, topic: str) -> InterviewSession:
        question = await self._ask_question(topic, [])
        return InterviewSession(topic=topic, last_question=question)

    async def submit_answer(self, session: InterviewSession, answer: str) -> Dict[str, str]:
        normalized_answer = await self._normalize_answer(answer)
        feedback = await self._evaluate(session.last_question, normalized_answer)
        session.turns.append(
            InterviewTurn(
                question=session.last_question,
                answer=normalized_answer,
                feedback=feedback,
            )
        )
        next_question = await self._ask_question(session.topic, session.turns)
        session.last_question = next_question
        return {
            "normalized_answer": normalized_answer,
            "feedback": feedback,
            "next_question": next_question,
        }

    async def finalize(self, session: InterviewSession) -> str:
        if not session.turns:
            return "No interview data captured. Recommendation: Insufficient data."

        transcript_lines = []
        for idx, turn in enumerate(session.turns, start=1):
            transcript_lines.append(
                f"Round {idx}\nQuestion: {turn.question}\nAnswer: {turn.answer}\nFeedback: {turn.feedback}"
            )
        transcript = "\n\n".join(transcript_lines)

        result = await self.evaluator.run(
            task=(
                "Based on this transcript, provide a final recommendation with sections: "
                "Strengths, Gaps, Final Verdict (Hire/No Hire).\n\n"
                f"{transcript}"
            )
        )
        return result.messages[-1].content.strip()

    async def close(self) -> None:
        await self.model_client.close()

    async def _ask_question(self, topic: str, turns: List[InterviewTurn]) -> str:
        context = ""
        if turns:
            latest = turns[-1]
            context = (
                "Previous round context:\n"
                f"Question: {latest.question}\n"
                f"Answer: {latest.answer}\n"
                f"Feedback: {latest.feedback}\n"
            )

        result = await self.interviewer.run(
            task=(
                f"Topic: {topic}. {context}"
                "Generate the next interview question. Return only the question text."
            )
        )
        return result.messages[-1].content.strip()

    async def _normalize_answer(self, answer: str) -> str:
        result = await self.candidate_proxy.run(
            task=(
                "Normalize this candidate answer into one clear sentence while preserving meaning: "
                f"{answer}"
            )
        )
        return result.messages[-1].content.strip()

    async def _evaluate(self, question: str, answer: str) -> str:
        result = await self.evaluator.run(
            task=(
                f"Question: {question}\n"
                f"Candidate Answer: {answer}\n"
                "Return: Score: x/10 | Feedback: <2-3 lines>."
            )
        )
        return result.messages[-1].content.strip()
