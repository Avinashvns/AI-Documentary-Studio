from pathlib import Path

from PIL import Image

from app.image_generation.models import GeneratedImage
from app.image_generation.services.image_generation import (
    ImageGenerationService,
)
from app.image_generation.services.output_manager import (
    ImageOutputManager,
)
from app.schemas.image_prompt import ImagePrompt


class FakeImageProvider:
    """
    Fake provider used for integration testing.

    It creates a real image file without running
    ComfyUI or using the GPU.
    """

    def __init__(
        self,
        output_path: Path,
    ):
        self.output_path = output_path

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 768,
        height: int = 432,
    ) -> GeneratedImage:
        Image.new(
            "RGB",
            (width, height),
        ).save(self.output_path)

        return GeneratedImage(
            path=str(self.output_path),
            width=width,
            height=height,
            format="png",
            provider="fake",
        )


def test_image_generation_pipeline(
    tmp_path,
):
    raw_image_path = (
        tmp_path / "generated.png"
    )

    provider = FakeImageProvider(
        output_path=raw_image_path
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
            "cinematic historical photograph "
            "of an ancient Indian palace"
        ),
        negative_prompt=(
            "cartoon, blurry, watermark"
        ),
    )

    generated_image = service.generate_image(
        image_prompt=image_prompt,
        width=768,
        height=432,
    )

    saved_image = output_manager.save_image(
        image=generated_image,
        topic="Mughal Empire",
        scene_number=1,
    )

    final_path = Path(
        saved_image.path
    )

    assert final_path.exists()

    assert final_path.name == (
        "scene_001.png"
    )

    assert saved_image.width == 768
    assert saved_image.height == 432
    assert saved_image.format == "png"

    with Image.open(final_path) as image:
        assert image.size == (
            768,
            432,
        )


def test_multiple_scene_image_pipeline(
    tmp_path,
):
    class MultiImageProvider:
        def __init__(self):
            self.counter = 0

        def generate(
            self,
            prompt: str,
            negative_prompt: str = "",
            width: int = 768,
            height: int = 432,
        ) -> GeneratedImage:
            self.counter += 1

            path = (
                tmp_path
                / f"generated_{self.counter}.png"
            )

            Image.new(
                "RGB",
                (width, height),
            ).save(path)

            return GeneratedImage(
                path=str(path),
                width=width,
                height=height,
                format="png",
                provider="fake",
            )

    provider = MultiImageProvider()

    service = ImageGenerationService(
        provider=provider
    )

    output_manager = ImageOutputManager(
        output_root=(
            tmp_path / "documentaries"
        )
    )

    prompts = [
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

    generated_images = (
        service.generate_images(
            image_prompts=prompts,
        )
    )

    saved_images = (
        output_manager.save_images(
            images=generated_images,
            topic="Mughal Empire",
        )
    )

    assert len(saved_images) == 2

    assert Path(
        saved_images[0].path
    ).name == "scene_001.png"

    assert Path(
        saved_images[1].path
    ).name == "scene_002.png"

    assert Path(
        saved_images[0].path
    ).exists()

    assert Path(
        saved_images[1].path
    ).exists()