from app.image_generation.config.constants import (
    ImageFormat,
    ImageProviderType,
)
from app.image_generation.config.settings import image_settings


def test_image_provider():
    assert image_settings.image_provider == ImageProviderType.LOCAL


def test_image_dimensions():
    assert image_settings.image_width > 0
    assert image_settings.image_height > 0


def test_image_format():
    assert image_settings.image_format in {
        ImageFormat.PNG,
        ImageFormat.JPEG,
        ImageFormat.WEBP,
    }


def test_image_output_directory():
    assert image_settings.image_output_dir


def test_image_generation_limits():
    assert image_settings.image_timeout > 0
    assert image_settings.image_max_retries >= 0