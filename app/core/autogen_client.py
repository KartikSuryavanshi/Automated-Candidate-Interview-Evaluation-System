from autogen_ext.models.openai import OpenAIChatCompletionClient

from app.core.config import settings


def build_model_client() -> OpenAIChatCompletionClient:
    # Ollama exposes an OpenAI-compatible endpoint at /v1.
    return OpenAIChatCompletionClient(
        model=settings.ollama_model,
        api_key="ollama",
        base_url=settings.ollama_base_url,
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "ollama",
        },
        temperature=0.4,
    )
