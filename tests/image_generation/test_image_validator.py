import pytest
from PIL import Image

from app.image_generation.exceptions import (
    CorruptImageError,
    ImageFileNotFoundError,
)
from app.image_generation.models import GeneratedImage
from app.image_generation.validation import ImageValidator


def test_valid_image(tmp_path):
    path = tmp_path / "scene.png"

    Image.new(
        "RGB",
        (768, 432),
    ).save(path)

    image = GeneratedImage(
        path=str(path),
        width=768,
        height=432,
        format="png",
        provider="local",
    )

    validator = ImageValidator()

    result = validator.validate(image)

    assert result.path == str(path)
    assert result.width == 768
    assert result.height == 432
    assert result.format == "png"
    assert result.provider == "local"


def test_missing_image():
    image = GeneratedImage(
        path="missing_image.png",
        width=768,
        height=432,
        format="png",
        provider="local",
    )

    validator = ImageValidator()

    with pytest.raises(
        ImageFileNotFoundError,
        match="does not exist",
    ):
        validator.validate(image)


def test_corrupt_image(tmp_path):
    path = tmp_path / "corrupt.png"

    path.write_bytes(
        b"this-is-not-a-real-image"
    )

    image = GeneratedImage(
        path=str(path),
        width=768,
        height=432,
        format="png",
        provider="local",
    )

    validator = ImageValidator()

    with pytest.raises(
        CorruptImageError,
        match="corrupt image",
    ):
        validator.validate(image)


def test_actual_dimensions_are_used(tmp_path):
    path = tmp_path / "scene.png"

    Image.new(
        "RGB",
        (640, 360),
    ).save(path)

    image = GeneratedImage(
        path=str(path),
        width=999,
        height=999,
        format="png",
        provider="local",
    )

    validator = ImageValidator()

    result = validator.validate(image)

    assert result.width == 640
    assert result.height == 360