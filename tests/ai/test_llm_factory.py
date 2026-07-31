from langchain_ollama import ChatOllama

from app.ai.llm.factory import LLMFactory
from app.config.ai_settings import ai_settings


def test_create_default_ollama():
    ai_settings.llm_provider = "ollama"

    llm = LLMFactory.create()

    assert isinstance(llm, ChatOllama)


def test_override_model():
    ai_settings.llm_provider = "ollama"

    llm = LLMFactory.create(model="qwen3:4b")

    assert isinstance(llm, ChatOllama)