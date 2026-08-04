from unittest.mock import patch

from app.agents.scene_planner import ScenePlannerAgent
from app.schemas.scene import Scene, ScenePlan
from app.schemas.script import ScriptResult, ScriptSection
from tests.fakes.fake_llm import FakeLLM


@patch("app.agents.scene_planner.ScenePrompt.build")
def test_scene_planner_agent(mock_prompt):
    expected = ScenePlan(
        scenes=[
            Scene(
                number=1,
                title="The Beginning",
                narration="An empire was about to rise.",
                duration=30,
            ),
            Scene(
                number=2,
                title="Rise of the Empire",
                narration="The Mughal Empire began expanding.",
                duration=45,
            ),
        ]
    )

    fake_llm = FakeLLM(expected)

    fake_prompt = mock_prompt.return_value

    fake_prompt.__or__.return_value = (
        fake_llm.with_structured_output(ScenePlan)
    )

    script = ScriptResult(
        title="The Mughal Empire",
        hook="An empire that changed history.",
        introduction="This is the story of the Mughal Empire.",
        sections=[
            ScriptSection(
                title="The Beginning",
                narration="The empire began in the sixteenth century.",
            )
        ],
        ending="Its legacy can still be seen today.",
        cta="Subscribe for more historical documentaries.",
    )

    agent = ScenePlannerAgent(llm=fake_llm)

    result = agent.run(
        script=script,
        duration=10,
    )

    assert len(result) == 2

    assert result[0].number == 1
    assert result[0].title == "The Beginning"
    assert result[0].duration == 30

    assert result[1].number == 2