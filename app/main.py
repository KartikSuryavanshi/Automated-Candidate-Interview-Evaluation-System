from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.agents.workflow import AriesWorkflow, InterviewSession

app = FastAPI(title="ARIES - Automated Candidate Interview & Evaluation System")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

workflow = AriesWorkflow()
sessions: dict[str, InterviewSession] = {}


@app.get("/")
def index() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aries"}


@app.websocket("/ws/interview")
async def interview_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    session_id: Optional[str] = None

    try:
        while True:
            payload = await websocket.receive_json()
            action = payload.get("action")

            if action == "start":
                topic = payload.get("topic", "Machine Learning")
                session_id = str(uuid4())
                session = await workflow.start_interview(topic)
                sessions[session_id] = session
                await websocket.send_json(
                    {
                        "type": "started",
                        "session_id": session_id,
                        "topic": topic,
                        "question": session.last_question,
                    }
                )

            elif action == "answer":
                if not session_id or session_id not in sessions:
                    await websocket.send_json(
                        {
                            "type": "error",
                            "message": "No active interview session. Start first.",
                        }
                    )
                    continue

                answer = payload.get("answer", "")
                if not answer.strip():
                    await websocket.send_json(
                        {"type": "error", "message": "Answer cannot be empty."}
                    )
                    continue

                result = await workflow.submit_answer(sessions[session_id], answer)
                await websocket.send_json(
                    {
                        "type": "round_result",
                        "normalized_answer": result["normalized_answer"],
                        "feedback": result["feedback"],
                        "next_question": result["next_question"],
                    }
                )

            elif action == "stop":
                if not session_id or session_id not in sessions:
                    await websocket.send_json(
                        {
                            "type": "error",
                            "message": "No active interview session to stop.",
                        }
                    )
                    continue

                final_report = await workflow.finalize(sessions[session_id])
                await websocket.send_json(
                    {"type": "final_report", "report": final_report}
                )
                del sessions[session_id]
                session_id = None

            else:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Invalid action. Use start, answer, or stop.",
                    }
                )

    except WebSocketDisconnect:
        if session_id and session_id in sessions:
            del sessions[session_id]
