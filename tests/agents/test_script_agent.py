from unittest.mock import patch

from app.agents.script import ScriptAgent
from app.schemas.research import ResearchResult
from app.schemas.script import (
    ScriptResult,
    ScriptSection,
)
from tests.fakes.fake_llm import FakeLLM


@patch("app.agents.script.ScriptPrompt.build")
def test_script_agent(mock_prompt):

    expected = ScriptResult(
        title="The Mughal Empire",
        hook="A powerful empire changed history.",
        introduction="Introduction",
        sections=[
            ScriptSection(
                title="Rise",
                narration="The empire began..."
            )
        ],
        ending="The legacy lives on.",
        cta="Subscribe for more."
    )

    fake_llm = FakeLLM(expected)

    fake_prompt = mock_prompt.return_value

    fake_prompt.__or__.return_value = (
        fake_llm.with_structured_output(
            ScriptResult
        )
    )

    research = ResearchResult(
        topic="Mughal Empire",
        summary="History",
        timeline=[],
        characters=[],
        sources=[],
    )

    agent = ScriptAgent(
        llm=fake_llm
    )

    result = agent.run(research)

    assert result.title == "The Mughal Empire"

    assert len(result.sections) == 1