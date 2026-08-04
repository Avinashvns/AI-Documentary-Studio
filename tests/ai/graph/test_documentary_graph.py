from unittest.mock import MagicMock

from app.ai.graph.documentary_graph import create_documentary_graph
from app.schemas.image_prompt import ImagePrompt
from app.schemas.research import ResearchResult
from app.schemas.scene import Scene
from app.schemas.script import ScriptResult, ScriptSection


def test_documentary_graph():
    research_result = ResearchResult(
        topic="Mughal Empire",
        summary="History of the Mughal Empire.",
        timeline=[],
        characters=[],
        sources=[],
    )

    script_result = ScriptResult(
        title="The Mughal Empire",
        hook="An empire that changed history.",
        introduction="The story begins in the sixteenth century.",
        sections=[
            ScriptSection(
                title="The Beginning",
                narration="Babur entered northern India.",
            )
        ],
        ending="The empire left a lasting legacy.",
        cta="Subscribe for more documentaries.",
    )

    scenes = [
        Scene(
            number=1,
            title="The Beginning",
            narration="Babur entered northern India.",
            duration=30,
        )
    ]

    image_prompts = [
        ImagePrompt(
            scene_number=1,
            prompt=(
                "Babur entering northern India, historical "
                "Mughal setting, cinematic lighting, "
                "photorealistic documentary style"
            ),
            negative_prompt=(
                "modern clothing, cars, text, watermark"
            ),
        )
    ]

    research_agent = MagicMock()
    research_agent.run.return_value = research_result

    script_agent = MagicMock()
    script_agent.run.return_value = script_result

    scene_planner_agent = MagicMock()
    scene_planner_agent.run.return_value = scenes

    image_prompt_agent = MagicMock()
    image_prompt_agent.run.return_value = image_prompts

    graph = create_documentary_graph(
        research_agent=research_agent,
        script_agent=script_agent,
        scene_planner_agent=scene_planner_agent,
        image_prompt_agent=image_prompt_agent,
    )

    initial_state = {
        "topic": "Mughal Empire",
        "language": "Hindi",
        "duration": 10,
        "style": "historical documentary",
        "research": None,
        "script": None,
        "scenes": [],
        "image_prompts": [],
        "images": [],
        "narration": "",
        "audio_path": "",
        "music_path": "",
        "subtitles_path": "",
        "output_video": "",
    }

    result = graph.invoke(initial_state)

    assert result["topic"] == "Mughal Empire"

    assert result["research"] == research_result
    assert result["script"] == script_result
    assert result["scenes"] == scenes
    assert result["image_prompts"] == image_prompts

    research_agent.run.assert_called_once()
    script_agent.run.assert_called_once_with(
        research=research_result,
        language="Hindi",
    )
    scene_planner_agent.run.assert_called_once_with(
        script=script_result,
        duration=10,
    )
    image_prompt_agent.run.assert_called_once_with(
        scenes=scenes,
        style="historical documentary",
    )


def test_documentary_graph_execution_order():
    execution_order = []

    research_result = ResearchResult(
        topic="Mughal Empire",
        summary="History",
        timeline=[],
        characters=[],
        sources=[],
    )

    script_result = ScriptResult(
        title="The Mughal Empire",
        hook="Hook",
        introduction="Introduction",
        sections=[],
        ending="Ending",
        cta="CTA",
    )

    scenes = [
        Scene(
            number=1,
            title="Beginning",
            narration="Narration",
            duration=30,
        )
    ]

    image_prompts = [
        ImagePrompt(
            scene_number=1,
            prompt="Historical cinematic documentary image",
            negative_prompt="text, watermark",
        )
    ]

    research_agent = MagicMock()
    script_agent = MagicMock()
    scene_planner_agent = MagicMock()
    image_prompt_agent = MagicMock()

    def research_run(*args, **kwargs):
        execution_order.append("research")
        return research_result

    def script_run(*args, **kwargs):
        execution_order.append("script")
        return script_result

    def scene_run(*args, **kwargs):
        execution_order.append("scene_planner")
        return scenes

    def image_prompt_run(*args, **kwargs):
        execution_order.append("image_prompt")
        return image_prompts

    research_agent.run.side_effect = research_run
    script_agent.run.side_effect = script_run
    scene_planner_agent.run.side_effect = scene_run
    image_prompt_agent.run.side_effect = image_prompt_run

    graph = create_documentary_graph(
        research_agent=research_agent,
        script_agent=script_agent,
        scene_planner_agent=scene_planner_agent,
        image_prompt_agent=image_prompt_agent,
    )

    initial_state = {
        "topic": "Mughal Empire",
        "language": "Hindi",
        "duration": 10,
        "style": "historical documentary",
        "research": None,
        "script": None,
        "scenes": [],
        "image_prompts": [],
        "images": [],
        "narration": "",
        "audio_path": "",
        "music_path": "",
        "subtitles_path": "",
        "output_video": "",
    }

    graph.invoke(initial_state)

    assert execution_order == [
        "research",
        "script",
        "scene_planner",
        "image_prompt",
    ]