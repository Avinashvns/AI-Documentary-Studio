from unittest.mock import patch

from app.agents.research import ResearchAgent
from app.schemas.research import ResearchResult
from tests.fakes.fake_llm import FakeLLM


@patch("app.agents.research.ResearchPrompt.build")
def test_research_agent(mock_prompt):
    expected = ResearchResult(
        topic="Mughal Empire",
        summary="History",
        timeline=[],
        characters=[],
        sources=[],
    )

    fake_llm = FakeLLM(expected)

    fake_prompt = mock_prompt.return_value

    fake_prompt.__or__.return_value = fake_llm.with_structured_output(
        ResearchResult
    )

    agent = ResearchAgent(llm=fake_llm)

    result = agent.run("Mughal Empire")

    assert result.topic == "Mughal Empire"