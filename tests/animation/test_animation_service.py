from unittest.mock import MagicMock

import pytest

from app.animation.models import GeneratedVideo
from app.animation.services.animation_service import (
    AnimationService,
)


def test_generate_animation():
    provider = MagicMock()

    expected = GeneratedVideo(
        path="scene_001.mp4",
        width=512,
        height=512,
        fps=16,
        frame_count=33,
        provider="comfyui",
    )

    provider.generate.return_value = expected

    service = AnimationService(
        provider=provider,
    )

    result = service.generate_animation(
        image_path="scene_001.png",
        prompt="slow cinematic zoom",
        negative_prompt="blurry",
        camera_motion="Pan Right",
    )

    assert result == expected

    provider.generate.assert_called_once_with(
        image_path="scene_001.png",
        prompt="slow cinematic zoom",
        negative_prompt="blurry",
        camera_motion="Pan Right",
        width=512,
        height=512,
        frame_count=33,
        fps=16,
    )


def test_generate_multiple_animations():
    provider = MagicMock()

    provider.generate.side_effect = [
        GeneratedVideo(
            path="scene_001.mp4",
            width=512,
            height=512,
            fps=16,
            frame_count=33,
            provider="comfyui",
        ),
        GeneratedVideo(
            path="scene_002.mp4",
            width=512,
            height=512,
            fps=16,
            frame_count=33,
            provider="comfyui",
        ),
    ]

    service = AnimationService(
        provider=provider,
    )

    results = service.generate_animations(
        images=[
            "scene_001.png",
            "scene_002.png",
        ],
        prompts=[
            "slow cinematic zoom",
            "slow camera pan",
        ],
    )

    assert len(results) == 2

    assert results[0].path == "scene_001.mp4"
    assert results[1].path == "scene_002.mp4"

    assert provider.generate.call_count == 2


def test_generate_animations_length_mismatch():
    service = AnimationService(
        provider=MagicMock(),
    )

    with pytest.raises(
        ValueError,
        match="same length",
    ):
        service.generate_animations(
            images=[
                "scene_001.png",
                "scene_002.png",
            ],
            prompts=[
                "slow cinematic zoom",
            ],
        )