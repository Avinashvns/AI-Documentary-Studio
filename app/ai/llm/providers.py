from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from app.config.ai_settings import ai_settings


def create_ollama(model: str | None = None):
    """
    Create an Ollama chat model.
    """
    return ChatOllama(
        model=model or ai_settings.ollama_model,
        base_url=ai_settings.ollama_base_url,
        temperature=ai_settings.temperature,
    )


def create_openai(model: str | None = None):
    """
    Create an OpenAI chat model.
    """
    return ChatOpenAI(
        model=model or ai_settings.openai_model,
        api_key=ai_settings.openai_api_key,
        temperature=ai_settings.temperature,
        max_retries=ai_settings.max_retries,
        timeout=ai_settings.request_timeout,
    )