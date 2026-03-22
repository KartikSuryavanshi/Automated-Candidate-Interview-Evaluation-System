from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from app.interviewer_agent import InterviewerAgent
from app.candidate_proxy import CandidateProxy
from app.evaluator_agent import EvaluatorAgent
import asyncio
import os

app = FastAPI()

interviewer = InterviewerAgent()
candidate = CandidateProxy()
evaluator = EvaluatorAgent()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/static")

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/demo")
def serve_demo():
    return FileResponse("app/static/index.html")

@app.websocket("/ws/interview")
async def interview_websocket(websocket: WebSocket):
    await websocket.accept()
    transcript = []
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("action") == "stop":
                break
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
        pass
    finally:
        transcript_str = "\n".join([f"{role}: {msg}" for role, msg in transcript])
        recommendation = await evaluator.final_recommendation(transcript_str)
        try:
            await websocket.send_json({"role": "evaluator", "message": recommendation, "final": True})
        except:
            pass
        await websocket.close()
