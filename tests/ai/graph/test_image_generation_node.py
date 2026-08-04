from unittest.mock import MagicMock

from app.ai.graph.nodes import DocumentaryNodes
from app.image_generation.models import GeneratedImage
from app.schemas.image_prompt import ImagePrompt


def test_image_generation_node():
    service = MagicMock()

    service.generate_images.return_value = [
        GeneratedImage(
            path="scene_1.png",
            width=768,
            height=432,
            format="png",
            provider="local",
        ),
        GeneratedImage(
            path="scene_2.png",
            width=768,
            height=432,
            format="png",
            provider="local",
        ),
    ]

    nodes = DocumentaryNodes(
        research_agent=MagicMock(),
        script_agent=MagicMock(),
        scene_planner_agent=MagicMock(),
        image_prompt_agent=MagicMock(),
        image_generation_service=service,
    )

    state = {
        "image_prompts": [
            ImagePrompt(
                scene_number=1,
                prompt="ancient Indian palace",
                negative_prompt="blurry",
            ),
            ImagePrompt(
                scene_number=2,
                prompt="historical battlefield",
                negative_prompt="cartoon",
            ),
        ]
    }

    result = nodes.image_generation_node(state)

    assert result == {
        "images": [
            "scene_1.png",
            "scene_2.png",
        ]
    }

    service.generate_images.assert_called_once_with(
        image_prompts=state["image_prompts"],
    )


def test_image_generation_node_empty_prompts():
    service = MagicMock()

    nodes = DocumentaryNodes(
        research_agent=MagicMock(),
        script_agent=MagicMock(),
        scene_planner_agent=MagicMock(),
        image_prompt_agent=MagicMock(),
        image_generation_service=service,
    )

    result = nodes.image_generation_node(
        {
            "image_prompts": [],
        }
    )

    assert result == {
        "images": [],
    }

    service.generate_images.assert_not_called()