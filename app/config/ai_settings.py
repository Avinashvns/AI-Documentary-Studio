from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    """
    AI Configuration
    """

    llm_provider: str = Field(default="ollama")

    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="qwen3:8b")

    openai_api_key: str = Field(default="")
    openai_model: str = Field(default="gpt-5-mini")

    temperature: float = Field(
        default=0.2,
        ge=0,
        le=2
    )

    max_tokens: int = Field(
        default=4096,
        gt=0
    )

    request_timeout: int = Field(
        default=120,
        gt=0
    )

    max_retries: int = Field(
        default=2,
        ge=0
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


ai_settings = AISettings()