from unittest.mock import MagicMock

import pytest

from app.ai.graph.nodes import DocumentaryNodes
from app.animation.models import GeneratedVideo
from app.schemas.animation import AnimationInstruction
from app.schemas.scene import Scene


def create_nodes(
    animation_agent=None,
    animation_service=None,
):
    return DocumentaryNodes(
        research_agent=MagicMock(),
        script_agent=MagicMock(),
        scene_planner_agent=MagicMock(),
        image_prompt_agent=MagicMock(),
        animation_agent=(
            animation_agent
            or MagicMock()
        ),
        animation_service=(
            animation_service
            or MagicMock()
        ),
    )


def test_animation_planning_node():
    animation_agent = MagicMock()

    scenes = [
        Scene(
            number=1,
            title="The Beginning",
            narration="Babur entered northern India.",
            duration=30,
        )
    ]

    instructions = [
        AnimationInstruction(
            scene_number=1,
            prompt=(
                "cinematic historical documentary, "
                "subtle natural movement"
            ),
            negative_prompt=(
                "flickering, jitter, watermark"
            ),
            camera_motion="Zoom In",
        )
    ]

    animation_agent.run.return_value = instructions

    nodes = create_nodes(
        animation_agent=animation_agent,
    )

    result = nodes.animation_planning_node(
        {
            "scenes": scenes,
        }
    )

    assert result == {
        "animation_instructions": instructions,
    }

    animation_agent.run.assert_called_once_with(
        scenes=scenes,
    )


def test_animation_planning_node_empty_scenes():
    animation_agent = MagicMock()

    nodes = create_nodes(
        animation_agent=animation_agent,
    )

    result = nodes.animation_planning_node(
        {
            "scenes": [],
        }
    )

    assert result == {
        "animation_instructions": [],
    }

    animation_agent.run.assert_not_called()


def test_animation_generation_node():
    animation_service = MagicMock()

    generated_video = GeneratedVideo(
        path="scene_001.mp4",
        width=512,
        height=512,
        fps=16,
        frame_count=33,
        provider="comfyui",
    )

    animation_service.generate_animation.return_value = (
        generated_video
    )

    instruction = AnimationInstruction(
        scene_number=1,
        prompt="slow cinematic zoom",
        negative_prompt="flickering, jitter",
        camera_motion="Zoom In",
    )

    nodes = create_nodes(
        animation_service=animation_service,
    )

    result = nodes.animation_generation_node(
        {
            "images": [
                "scene_001.png",
            ],
            "animation_instructions": [
                instruction,
            ],
        }
    )

    assert result == {
        "animations": [
            "scene_001.mp4",
        ]
    }

    animation_service.generate_animation.assert_called_once_with(
        image_path="scene_001.png",
        prompt="slow cinematic zoom",
        negative_prompt="flickering, jitter",
        camera_motion="Zoom In",
    )


def test_animation_generation_node_empty_input():
    animation_service = MagicMock()

    nodes = create_nodes(
        animation_service=animation_service,
    )

    result = nodes.animation_generation_node(
        {
            "images": [],
            "animation_instructions": [],
        }
    )

    assert result == {
        "animations": [],
    }

    animation_service.generate_animation.assert_not_called()


def test_animation_generation_requires_matching_counts():
    nodes = create_nodes()

    instruction = AnimationInstruction(
        scene_number=1,
        prompt="slow cinematic zoom",
        camera_motion="Zoom In",
    )

    with pytest.raises(
        ValueError,
        match=(
            "Images and animation instructions "
            "must have the same length"
        ),
    ):
        nodes.animation_generation_node(
            {
                "images": [
                    "scene_001.png",
                    "scene_002.png",
                ],
                "animation_instructions": [
                    instruction,
                ],
            }
        )