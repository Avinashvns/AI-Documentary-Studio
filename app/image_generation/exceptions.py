class ImageGenerationError(Exception):
    """Base exception for image generation failures."""


class ImageProviderError(ImageGenerationError):
    """Raised when an image provider fails."""


class ImageValidationError(ImageGenerationError):
    """Raised when a generated image is invalid."""


class UnsupportedImageProviderError(ImageGenerationError):
    """Raised when an unsupported image provider is requested."""

class ImageValidationError(Exception):
    """
    Raised when a generated image fails validation.
    """


class ImageFileNotFoundError(ImageValidationError):
    """
    Raised when the generated image file does not exist.
    """


class CorruptImageError(ImageValidationError):
    """
    Raised when the generated image cannot be decoded.
    """


class InvalidImageFormatError(ImageValidationError):
    """
    Raised when the image format is unsupported.
    """


class InvalidImageDimensionsError(ImageValidationError):
    """
    Raised when image dimensions are invalid.
    """