import pytest

from app.image_generation.models import GeneratedImage
from app.image_generation.providers.base import ImageProvider


def test_image_provider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        ImageProvider()


def test_generated_image_model():
    image = GeneratedImage(
        path="outputs/images/scene_001.png",
        width=1024,
        height=576,
        format="png",
        provider="local",
    )

    assert image.path == "outputs/images/scene_001.png"
    assert image.width == 1024
    assert image.height == 576
    assert image.format == "png"
    assert image.provider == "local"


class FakeImageProvider(ImageProvider):
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 576,
    ) -> GeneratedImage:
        return GeneratedImage(
            path="outputs/images/fake.png",
            width=width,
            height=height,
            format="png",
            provider="fake",
        )


def test_concrete_provider_implements_interface():
    provider = FakeImageProvider()

    result = provider.generate(
        prompt="Historical Mughal palace",
        negative_prompt="text, watermark",
        width=1024,
        height=576,
    )

    assert isinstance(result, GeneratedImage)

    assert result.path == "outputs/images/fake.png"

    assert result.width == 1024
    assert result.height == 576

    assert result.provider == "fake"


def test_provider_without_generate_cannot_be_instantiated():
    class InvalidProvider(ImageProvider):
        pass

    with pytest.raises(TypeError):
        InvalidProvider()


class CloudImageProvider(ImageProvider):
    pass