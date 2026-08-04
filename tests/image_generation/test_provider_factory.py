import pytest

from app.image_generation.exceptions import (
    UnsupportedImageProviderError,
)
from app.image_generation.models import GeneratedImage
from app.image_generation.providers.base import ImageProvider
from app.image_generation.providers.factory import (
    ImageProviderFactory,
)


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


@pytest.fixture(autouse=True)
def clean_provider_registry():
    original = ImageProviderFactory._providers.copy()

    ImageProviderFactory._providers.clear()

    yield

    ImageProviderFactory._providers.clear()
    ImageProviderFactory._providers.update(original)


def test_register_provider():
    ImageProviderFactory.register(
        "fake",
        FakeImageProvider,
    )

    assert "fake" in ImageProviderFactory._providers


def test_create_registered_provider():
    ImageProviderFactory.register(
        "fake",
        FakeImageProvider,
    )

    provider = ImageProviderFactory.create(
        "fake"
    )

    assert isinstance(
        provider,
        FakeImageProvider,
    )


def test_provider_name_is_case_insensitive():
    ImageProviderFactory.register(
        "fake",
        FakeImageProvider,
    )

    provider = ImageProviderFactory.create(
        "FAKE"
    )

    assert isinstance(
        provider,
        FakeImageProvider,
    )


def test_unsupported_provider_raises_error():
    with pytest.raises(
        UnsupportedImageProviderError,
        match="Unsupported image provider",
    ):
        ImageProviderFactory.create(
            "unknown"
        )


def test_create_uses_configured_provider(monkeypatch):
    ImageProviderFactory.register(
        "fake",
        FakeImageProvider,
    )

    monkeypatch.setattr(
        "app.image_generation.providers.factory."
        "image_settings.image_provider",
        "fake",
    )

    provider = ImageProviderFactory.create()

    assert isinstance(
        provider,
        FakeImageProvider,
    )