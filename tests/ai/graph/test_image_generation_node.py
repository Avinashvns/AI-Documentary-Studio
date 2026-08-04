from unittest.mock import MagicMock

from app.ai.graph.nodes import DocumentaryNodes
from app.image_generation.models import GeneratedImage
from app.schemas.image_prompt import ImagePrompt


def test_image_generation_node():
    service = MagicMock()
    output_manager = MagicMock()

    generated_images = [
        GeneratedImage(
            path="ComfyUI_00001_.png",
            width=768,
            height=432,
            format="png",
            provider="local",
        ),
        GeneratedImage(
            path="ComfyUI_00002_.png",
            width=768,
            height=432,
            format="png",
            provider="local",
        ),
    ]

    organized_images = [
        GeneratedImage(
            path=(
                "outputs/documentaries/"
                "mughal-empire/images/scene_001.png"
            ),
            width=768,
            height=432,
            format="png",
            provider="local",
        ),
        GeneratedImage(
            path=(
                "outputs/documentaries/"
                "mughal-empire/images/scene_002.png"
            ),
            width=768,
            height=432,
            format="png",
            provider="local",
        ),
    ]

    service.generate_images.return_value = (
        generated_images
    )

    output_manager.save_images.return_value = (
        organized_images
    )

    nodes = DocumentaryNodes(
        research_agent=MagicMock(),
        script_agent=MagicMock(),
        scene_planner_agent=MagicMock(),
        image_prompt_agent=MagicMock(),
        image_generation_service=service,
        image_output_manager=output_manager,
    )

    state = {
        "topic": "Mughal Empire",
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
        ],
    }

    result = nodes.image_generation_node(
        state
    )

    assert result == {
        "images": [
            (
                "outputs/documentaries/"
                "mughal-empire/images/scene_001.png"
            ),
            (
                "outputs/documentaries/"
                "mughal-empire/images/scene_002.png"
            ),
        ]
    }

    service.generate_images.assert_called_once_with(
        image_prompts=state["image_prompts"],
    )

    output_manager.save_images.assert_called_once_with(
        images=generated_images,
        topic="Mughal Empire",
    )


def test_image_generation_node_empty_prompts():
    service = MagicMock()
    output_manager = MagicMock()

    nodes = DocumentaryNodes(
        research_agent=MagicMock(),
        script_agent=MagicMock(),
        scene_planner_agent=MagicMock(),
        image_prompt_agent=MagicMock(),
        image_generation_service=service,
        image_output_manager=output_manager,
    )

    result = nodes.image_generation_node(
        {
            "topic": "Mughal Empire",
            "image_prompts": [],
        }
    )

    assert result == {
        "images": [],
    }

    service.generate_images.assert_not_called()

    output_manager.save_images.assert_not_called()