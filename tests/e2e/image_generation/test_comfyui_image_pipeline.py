from pathlib import Path

import pytest
from PIL import Image

from app.image_generation.providers.factory import (
    ImageProviderFactory,
)
from app.image_generation.services.image_generation import (
    ImageGenerationService,
)
from app.image_generation.services.output_manager import (
    ImageOutputManager,
)
from app.schemas.image_prompt import ImagePrompt


@pytest.mark.e2e
def test_real_comfyui_image_pipeline(
    tmp_path,
):
    """
    End-to-end test using the real local ComfyUI provider.

    Requirements:
    - ComfyUI server running
    - Local image provider configured
    - DreamShaper checkpoint available
    """

    provider = ImageProviderFactory.create(
        "local"
    )

    service = ImageGenerationService(
        provider=provider
    )

    output_manager = ImageOutputManager(
        output_root=(
            tmp_path / "documentaries"
        )
    )

    image_prompt = ImagePrompt(
        scene_number=1,
        prompt=(
            "cinematic historical documentary photograph "
            "of an ancient Indian palace, "
            "realistic architecture, "
            "dramatic natural lighting, "
            "photorealistic, "
            "wide cinematic composition"
        ),
        negative_prompt=(
            "cartoon, anime, illustration, blurry, "
            "low quality, text, watermark, logo"
        ),
    )

    generated_image = service.generate_image(
        image_prompt=image_prompt,
        width=768,
        height=432,
    )

    generated_path = Path(
        generated_image.path
    )

    assert generated_path.exists()
    assert generated_path.is_file()

    assert generated_image.provider == "local"

    saved_image = output_manager.save_image(
        image=generated_image,
        topic="Mughal Empire",
        scene_number=1,
    )

    final_path = Path(
        saved_image.path
    )

    assert final_path.exists()
    assert final_path.is_file()

    assert final_path.name == (
        "scene_001.png"
    )

    with Image.open(final_path) as image:
        image.verify()

    with Image.open(final_path) as image:
        assert image.size == (
            768,
            432,
        )