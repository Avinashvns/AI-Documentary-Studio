from app.config.ai_settings import ai_settings


def test_provider():
    assert ai_settings.llm_provider == "ollama"


def test_temperature():
    assert ai_settings.temperature == 0.2


def test_max_tokens():
    assert ai_settings.max_tokens == 4096


def test_timeout():
    assert ai_settings.request_timeout == 120