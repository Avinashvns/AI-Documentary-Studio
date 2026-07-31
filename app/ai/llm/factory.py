from langchain_core.language_models.chat_models import BaseChatModel

from app.ai.llm.exceptions import UnsupportedLLMProviderError
from app.ai.llm.providers import (
    create_ollama,
    create_openai,
)
from app.config.ai_settings import ai_settings


class LLMFactory:
    """
    Factory for creating chat models.
    """

    @staticmethod
    def create(model: str | None = None) -> BaseChatModel:
        provider = ai_settings.llm_provider.lower()

        providers = {
            "ollama": create_ollama,
            "openai": create_openai,
        }

        try:
            return providers[provider](model=model)
        except KeyError as exc:
            raise UnsupportedLLMProviderError(
                f"Unsupported LLM provider: {provider}"
            ) from exc