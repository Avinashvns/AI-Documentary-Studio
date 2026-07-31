from app.config.constants import HEALTHY_STATUS
from app.core.enums import AgentType, Language


def test_health_constant():
    assert HEALTHY_STATUS == "healthy"


def test_agent_enum():
    assert AgentType.RESEARCH == "research"
    assert AgentType.MASTER == "master"


def test_language_enum():
    assert Language.HINDI == "Hindi"
    assert Language.ENGLISH == "English"