from unittest.mock import MagicMock

from app.image_generation.models import GeneratedImage
from app.image_generation.services.image_generation import (
    ImageGenerationService,
)
from app.schemas.image_prompt import ImagePrompt


def test_generate_single_image():
    provider = MagicMock()
    validator = MagicMock()

    expected = GeneratedImage(
        path="scene_1.png",
        width=768,
        height=432,
        format="png",
        provider="local",
    )

    provider.generate.return_value = expected
    validator.validate.return_value = expected

    service = ImageGenerationService(
        provider=provider,
        validator=validator,
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

    validator.validate.assert_called_once_with(
        expected
    )

def test_generate_multiple_images():
    provider = MagicMock()
    validator = MagicMock()

    generated_1 = GeneratedImage(
        path="scene_1.png",
        width=768,
        height=432,
        format="png",
        provider="local",
    )

    generated_2 = GeneratedImage(
        path="scene_2.png",
        width=768,
        height=432,
        format="png",
        provider="local",
    )

    provider.generate.side_effect = [
        generated_1,
        generated_2,
    ]

    validator.validate.side_effect = [
        generated_1,
        generated_2,
    ]

    service = ImageGenerationService(
        provider=provider,
        validator=validator,
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

    assert results == [
        generated_1,
        generated_2,
    ]

    assert provider.generate.call_count == 2
    assert validator.validate.call_count == 2

    validator.validate.assert_any_call(
        generated_1
    )

    validator.validate.assert_any_call(
        generated_2
    )

def test_generate_empty_prompt_list():
    provider = MagicMock()

    service = ImageGenerationService(
        provider=provider
    )

    results = service.generate_images([])

    assert results == []

    provider.generate.assert_not_called()


def test_service_validates_generated_image():
    provider = MagicMock()
    validator = MagicMock()

    generated = MagicMock()
    validated = MagicMock()

    provider.generate.return_value = generated
    validator.validate.return_value = validated

    service = ImageGenerationService(
        provider=provider,
        validator=validator,
    )

    result = service.generate_image(
        ImagePrompt(
            scene_number=1,
            prompt="historical palace",
            negative_prompt="blurry",
        )
    )

    validator.validate.assert_called_once_with(
        generated
    )

    assert result is validated