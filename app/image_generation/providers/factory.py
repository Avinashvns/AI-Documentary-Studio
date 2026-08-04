from collections.abc import Callable

from app.image_generation.config.settings import image_settings
from app.image_generation.exceptions import (
    UnsupportedImageProviderError,
)
from app.image_generation.providers.base import ImageProvider


ProviderFactory = Callable[[], ImageProvider]


class ImageProviderFactory:
    """
    Factory responsible for creating image providers.
    """

    _providers: dict[str, ProviderFactory] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider_factory: ProviderFactory,
    ) -> None:
        """
        Register an image provider factory.
        """

        cls._providers[name.lower()] = provider_factory

    @classmethod
    def create(
        cls,
        provider: str | None = None,
    ) -> ImageProvider:
        """
        Create an image provider.

        If provider is not explicitly supplied,
        IMAGE_PROVIDER from settings is used.
        """

        provider_name = (
            provider or image_settings.image_provider
        ).lower()

        provider_factory = cls._providers.get(
            provider_name
        )

        if provider_factory is None:
            raise UnsupportedImageProviderError(
                f"Unsupported image provider: {provider_name}"
            )

        return provider_factory()