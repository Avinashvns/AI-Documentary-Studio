from unittest.mock import MagicMock

from app.image_generation.models import GeneratedImage
from app.image_generation.services.image_generation import (
    ImageGenerationService,
)
from app.schemas.image_prompt import ImagePrompt


def test_generate_single_image():
    provider = MagicMock()

    expected = GeneratedImage(
        path="scene_1.png",
        width=768,
        height=432,
        format="png",
        provider="local",
    )

    provider.generate.return_value = expected

    service = ImageGenerationService(
        provider=provider
    )

    image_prompt = ImagePrompt(
        scene_number=1,
        prompt="cinematic ancient Indian palace",
        negative_prompt="blurry, cartoon",
    )

    result = service.generate_image(
        image_prompt
    )

    assert result == expected

    provider.generate.assert_called_once_with(
        prompt="cinematic ancient Indian palace",
        negative_prompt="blurry, cartoon",
        width=768,
        height=432,
    )

def test_generate_multiple_images():
    provider = MagicMock()

    provider.generate.side_effect = [
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

    service = ImageGenerationService(
        provider=provider
    )

    prompts = [
        ImagePrompt(
            scene_number=1,
            prompt="ancient palace",
            negative_prompt="blurry",
        ),
        ImagePrompt(
            scene_number=2,
            prompt="historical battlefield",
            negative_prompt="cartoon",
        ),
    ]

    results = service.generate_images(
        prompts
    )

    assert len(results) == 2

    assert results[0].path == "scene_1.png"
    assert results[1].path == "scene_2.png"

    assert provider.generate.call_count == 2

def test_generate_empty_prompt_list():
    provider = MagicMock()

    service = ImageGenerationService(
        provider=provider
    )

    results = service.generate_images([])

    assert results == []

    provider.generate.assert_not_called()