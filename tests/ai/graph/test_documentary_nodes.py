from unittest.mock import MagicMock

import pytest

from app.ai.graph.nodes import DocumentaryNodes
from app.schemas.research import ResearchResult
from app.schemas.script import ScriptResult, ScriptSection


def create_nodes():
    return DocumentaryNodes(
        research_agent=MagicMock(),
        script_agent=MagicMock(),
        scene_planner_agent=MagicMock(),
        image_prompt_agent=MagicMock(),
    )


def create_state():
    return {
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


def test_research_node_updates_state():
    nodes = create_nodes()

    expected = ResearchResult(
        topic="Mughal Empire",
        summary="History",
        timeline=[],
        characters=[],
        sources=[],
    )

    nodes.research_agent.run.return_value = expected

    state = create_state()

    result = nodes.research_node(state)

    assert result["research"] == expected

    request = nodes.research_agent.run.call_args.args[0]

    assert request.topic == "Mughal Empire"
    assert request.language == "Hindi"
    assert request.duration == 10
    assert request.style == "historical documentary"


def test_script_node_requires_research():
    nodes = create_nodes()

    state = create_state()

    with pytest.raises(
        ValueError,
        match="Research result is required",
    ):
        nodes.script_node(state)


def test_script_node_updates_state():
    nodes = create_nodes()

    research = ResearchResult(
        topic="Mughal Empire",
        summary="History",
        timeline=[],
        characters=[],
        sources=[],
    )

    expected = ScriptResult(
        title="The Mughal Empire",
        hook="An empire that changed history.",
        introduction="The story begins.",
        sections=[
            ScriptSection(
                title="Beginning",
                narration="Babur entered India.",
            )
        ],
        ending="The legacy remains.",
        cta="Subscribe for more.",
    )

    nodes.script_agent.run.return_value = expected

    state = create_state()
    state["research"] = research

    result = nodes.script_node(state)

    assert result["script"] == expected

    nodes.script_agent.run.assert_called_once_with(
        research=research,
        language="Hindi",
    )


def test_scene_planner_node_requires_script():
    nodes = create_nodes()

    state = create_state()

    with pytest.raises(
        ValueError,
        match="Script result is required",
    ):
        nodes.scene_planner_node(state)


def test_research_node_propagates_agent_error():
    nodes = create_nodes()

    nodes.research_agent.run.side_effect = RuntimeError(
        "Research service failed"
    )

    state = create_state()

    with pytest.raises(
        RuntimeError,
        match="Research service failed",
    ):
        nodes.research_node(state)


def test_script_node_propagates_agent_error():
    nodes = create_nodes()

    research = ResearchResult(
        topic="Mughal Empire",
        summary="History",
        timeline=[],
        characters=[],
        sources=[],
    )

    nodes.script_agent.run.side_effect = RuntimeError(
        "Script service failed"
    )

    state = create_state()
    state["research"] = research

    with pytest.raises(
        RuntimeError,
        match="Script service failed",
    ):
        nodes.script_node(state)