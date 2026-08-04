from pathlib import Path

from PIL import Image, UnidentifiedImageError

from app.image_generation.exceptions import (
    CorruptImageError,
    ImageFileNotFoundError,
    InvalidImageDimensionsError,
    InvalidImageFormatError,
)
from app.image_generation.models import GeneratedImage


class ImageValidator:
    """
    Validates generated image files before they enter
    the rest of the documentary pipeline.
    """

    SUPPORTED_FORMATS = {
        "PNG",
        "JPEG",
        "WEBP",
    }

    def validate(
        self,
        image: GeneratedImage,
    ) -> GeneratedImage:
        path = Path(image.path)

        self._validate_exists(path)

        try:
            with Image.open(path) as opened_image:
                actual_format = opened_image.format
                actual_width, actual_height = opened_image.size

                opened_image.verify()

        except (
            UnidentifiedImageError,
            OSError,
            SyntaxError,
        ) as exc:
            raise CorruptImageError(
                f"Invalid or corrupt image: {path}"
            ) from exc

        self._validate_format(
            actual_format,
            path,
        )

        self._validate_dimensions(
            width=actual_width,
            height=actual_height,
            path=path,
        )

        return GeneratedImage(
            path=str(path),
            width=actual_width,
            height=actual_height,
            format=actual_format.lower(),
            provider=image.provider,
        )

    @staticmethod
    def _validate_exists(
        path: Path,
    ) -> None:
        if not path.is_file():
            raise ImageFileNotFoundError(
                f"Generated image file does not exist: {path}"
            )

    def _validate_format(
        self,
        image_format: str | None,
        path: Path,
    ) -> None:
        if (
            image_format is None
            or image_format.upper()
            not in self.SUPPORTED_FORMATS
        ):
            raise InvalidImageFormatError(
                f"Unsupported image format for {path}: "
                f"{image_format}"
            )

    @staticmethod
    def _validate_dimensions(
        width: int,
        height: int,
        path: Path,
    ) -> None:
        if width <= 0 or height <= 0:
            raise InvalidImageDimensionsError(
                f"Invalid image dimensions for {path}: "
                f"{width}x{height}"
            )