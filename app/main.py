from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from app.interviewer_agent import InterviewerAgent
from app.candidate_proxy import CandidateProxy
from app.evaluator_agent import EvaluatorAgent
import asyncio
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

interviewer = InterviewerAgent()
candidate = CandidateProxy()
evaluator = EvaluatorAgent()

@app.get("/")
def read_root():
    return {"message": "ARIES Automated Candidate Interview & Evaluation System is running."}

@app.websocket("/ws/interview")
async def interview_websocket(websocket: WebSocket):
    await websocket.accept()
    transcript = []
    try:
        while True:
            data = await websocket.receive_json()
            topic = data.get("topic", "Python")
            # 1. Interviewer asks a question
            question = await interviewer.ask_question(topic)
            await websocket.send_json({"role": "interviewer", "message": question})
            transcript.append(("interviewer", question))
            # 2. Candidate answers
            answer = await candidate.answer_question(question)
            await websocket.send_json({"role": "candidate", "message": answer})
            transcript.append(("candidate", answer))
            # 3. Evaluator gives feedback
            feedback = await evaluator.give_feedback(question, answer)
            await websocket.send_json({"role": "evaluator", "message": feedback})
            transcript.append(("evaluator", feedback))
    except WebSocketDisconnect:
        # On disconnect, send final recommendation
        transcript_str = "\n".join([f"{role}: {msg}" for role, msg in transcript])
        recommendation = await evaluator.final_recommendation(transcript_str)
        await websocket.close()
        # Optionally, log or store the recommendation

@app.get("/demo")
def serve_demo():
    return FileResponse("app/static/index.html")
