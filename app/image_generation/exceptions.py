class ImageGenerationError(Exception):
    """Base exception for image generation failures."""


class ImageProviderError(ImageGenerationError):
    """Raised when an image provider fails."""


class ImageValidationError(ImageGenerationError):
    """Raised when a generated image is invalid."""


class UnsupportedImageProviderError(ImageGenerationError):
    """Raised when an unsupported image provider is requested."""