# Automated Candidate Interview & Evaluation System

An agentic AI solution for top-of-funnel recruitment that conducts technical interview rounds, evaluates candidate responses in real time, and produces a final recommendation using Microsoft AutoGen multi-agent orchestration.

<img width="1432" height="774" alt="Screenshot 2026-04-03 at 9 26 21 AM" src="https://github.com/user-attachments/assets/55195758-1f42-485e-aded-3a1ca7ecc006" />

https://github.com/user-attachments/assets/1dd3f1eb-c6b5-41a7-881c-10de8cdfd6a3

## System Architecture

The system consists of three agents communicating in a structured loop:

- **Interviewer Agent** — generates context-aware interview questions
- **Candidate Bridge** — captures and normalises candidate input
- **Evaluation Agent** — scores answers and provides constructive feedback
- **FastAPI + WebSocket** — streams the conversation in real time
- **Microsoft AutoGen (AgentChat)** — multi-agent orchestration framework

Flow per round:

1. Interviewer Agent asks a question
2. Candidate submits an answer via the browser
3. Evaluation Agent scores and provides feedback
4. Interviewer Agent generates the next question using prior context

On stop, the system produces a final recommendation report covering Strengths, Gaps, and a Hire / No-Hire verdict.

## Section-Wise Build Path

**Section 1 — Foundations & Configuration**
1. Project setup (virtual environment, dependencies)
2. AutoGen + model configuration
3. Environment variables

**Section 2 — Agent Implementation**
1. Interviewer Agent
2. Candidate Bridge
3. Evaluation Agent

**Section 3 — Integration & Testing**
1. WebSocket integration of all agents
2. Multi-round interview testing

**Section 4 — Interface & Deployment**
1. Interactive browser interview console
2. Render deployment-ready structure

## Quick Start

**1. Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
pip install tiktoken openai
```

**3. Configure environment:**
```bash
cp .env.example .env
```

**4. Start Ollama (free local model API):**
```bash
ollama serve
ollama pull llama3.2:3b
```

**5. Run server:**
```bash
uvicorn app.main:app --reload
```

**6. Open in browser:**
```
http://127.0.0.1:8000
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Interview UI |
| GET | `/health` | Service health check |
| WS | `/ws/interview` | Real-time interview channel |

**WebSocket actions:**

| Action | Payload | Description |
|--------|---------|-------------|
| `start` | `{ topic }` | Begin interview on a given topic |
| `answer` | `{ answer }` | Submit candidate answer |
| `stop` | — | End interview and receive final report |

## Project Structure

```
app/
├── core/
│   ├── config.py          # Environment settings
│   └── autogen_client.py  # Ollama OpenAI-compatible model client
├── agents/
│   └── workflow.py        # Interviewer / Evaluator orchestration
├── schemas/
│   └── interview.py       # Request/response models
├── static/
│   └── index.html         # Frontend interview console
└── main.py                # FastAPI routes + WebSocket handling
```

## Notes

- Runs on free local models via [Ollama](https://ollama.com/).
- Swap `OLLAMA_BASE_URL` and `OLLAMA_MODEL` in `.env` to use any OpenAI-compatible endpoint.
