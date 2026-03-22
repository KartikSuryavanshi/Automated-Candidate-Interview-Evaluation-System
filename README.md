# Automated-Candidate-Interview-Evaluation-System

This repository contains the ARIES project: an Automated Candidate Interview & Evaluation System using FastAPI, WebSockets, and a free/open-source LLM API (Ollama-compatible).

## Quick Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/KartikSuryavanshi/Automated-Candidate-Interview-Evaluation-System.git
   cd Automated-Candidate-Interview-Evaluation-System
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Install and run Ollama for local LLM API:
   https://ollama.com/

5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure
- `app/` - Main application code
- `requirements.txt` - Python dependencies
- `README.md` - Project overview and setup

## License
MIT
