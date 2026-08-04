from app.image_generation.providers.base import ImageProvider
from app.image_generation.providers.comfyui import (
    ComfyUIImageProvider,
)
from app.image_generation.providers.factory import (
    ImageProviderFactory,
)


ImageProviderFactory.register(
    "local",
    ComfyUIImageProvider,
)


__all__ = [
    "ImageProvider",
    "ImageProviderFactory",
    "ComfyUIImageProvider",
]