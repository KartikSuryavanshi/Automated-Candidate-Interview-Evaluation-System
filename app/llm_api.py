import httpx
import os

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

async def query_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
