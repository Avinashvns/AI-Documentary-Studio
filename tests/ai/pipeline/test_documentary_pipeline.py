from unittest.mock import MagicMock

import pytest

from app.ai.pipeline.documentary_pipeline import DocumentaryPipeline
from app.ai.pipeline.exceptions import DocumentaryPipelineError
from app.schemas.image_prompt import ImagePrompt
from app.schemas.render import RenderConfig
from app.schemas.request import DocumentaryRequest
from app.schemas.research import ResearchResult
from app.schemas.scene import Scene
from app.schemas.script import ScriptResult, ScriptSection


def create_graph_result():
    research = ResearchResult(
        topic="Mughal Empire",
        summary="History of the Mughal Empire.",
        timeline=[],
        characters=[],
        sources=[],
    )

    script = ScriptResult(
        title="The Mughal Empire",
        hook="An empire that changed history.",
        introduction="The story begins.",
        sections=[
            ScriptSection(
                title="The Beginning",
                narration="Babur entered northern India.",
            )
        ],
        ending="The legacy remains.",
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
                "Mughal environment, cinematic lighting, "
                "photorealistic documentary style"
            ),
            negative_prompt=(
                "modern clothing, cars, text, watermark"
            ),
        )
    ]

    return {
        "research": research,
        "script": script,
        "scenes": scenes,
        "image_prompts": image_prompts,
    }


def test_documentary_pipeline():
    graph = MagicMock()

    graph_result = create_graph_result()

    graph.invoke.return_value = graph_result

    pipeline = DocumentaryPipeline(
        graph=graph
    )

    request = DocumentaryRequest(
        topic="Mughal Empire",
        language="Hindi",
        duration=10,
        style="historical documentary",
    )

    documentary = pipeline.run(request)

    assert documentary.request == request

    assert documentary.research == graph_result["research"]

    assert documentary.script == graph_result["script"]

    assert documentary.scenes == graph_result["scenes"]

    assert (
        documentary.image_prompts
        == graph_result["image_prompts"]
    )

    assert documentary.render.resolution == "2K"
    assert documentary.render.fps == 30
    assert documentary.render.format == "mp4"

    graph.invoke.assert_called_once()



def test_pipeline_builds_correct_initial_state():
    graph = MagicMock()

    graph.invoke.return_value = create_graph_result()

    pipeline = DocumentaryPipeline(
        graph=graph
    )

    request = DocumentaryRequest(
        topic="Battle of Plassey",
        language="Hindi",
        duration=15,
        style="cinematic historical",
    )

    pipeline.run(request)

    initial_state = graph.invoke.call_args.args[0]

    assert initial_state["topic"] == "Battle of Plassey"
    assert initial_state["language"] == "Hindi"
    assert initial_state["duration"] == 15
    assert initial_state["style"] == "cinematic historical"

    assert initial_state["research"] is None
    assert initial_state["script"] is None

    assert initial_state["scenes"] == []
    assert initial_state["image_prompts"] == []
    assert initial_state["images"] == []



def test_pipeline_accepts_custom_render_config():
    graph = MagicMock()

    graph.invoke.return_value = create_graph_result()

    pipeline = DocumentaryPipeline(
        graph=graph
    )

    request = DocumentaryRequest(
        topic="Mughal Empire",
    )

    render = RenderConfig(
        resolution="1080p",
        fps=60,
        format="mp4",
    )

    documentary = pipeline.run(
        request=request,
        render=render,
    )

    assert documentary.render == render

    assert documentary.render.resolution == "1080p"
    assert documentary.render.fps == 60



def test_pipeline_wraps_graph_error():
    graph = MagicMock()

    graph.invoke.side_effect = RuntimeError(
        "Research model unavailable"
    )

    pipeline = DocumentaryPipeline(
        graph=graph
    )

    request = DocumentaryRequest(
        topic="Mughal Empire"
    )

    with pytest.raises(
        DocumentaryPipelineError,
        match="Documentary pipeline failed",
    ):
        pipeline.run(request)