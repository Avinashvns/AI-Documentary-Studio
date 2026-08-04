from app.image_generation.models import GeneratedImage
from app.image_generation.services.output_manager import (
    ImageOutputManager,
)

import pytest

from app.image_generation.exceptions import (
    ImageProviderError,
)

def test_save_image(tmp_path):
    source = tmp_path / "ComfyUI_00001_.png"
    source.write_bytes(b"fake-image")

    output_root = tmp_path / "documentaries"

    manager = ImageOutputManager(
        output_root=output_root
    )

    image = GeneratedImage(
        path=str(source),
        width=768,
        height=432,
        format="png",
        provider="local",
    )

    result = manager.save_image(
        image=image,
        topic="Mughal Empire",
        scene_number=1,
    )

    expected = (
        output_root
        / "mughal-empire"
        / "images"
        / "scene_001.png"
    )

    assert expected.exists()
    assert result.path == str(expected)

    # Original ComfyUI image should remain.
    assert source.exists()


def test_save_multiple_images(tmp_path):
    source_1 = tmp_path / "image1.png"
    source_2 = tmp_path / "image2.png"

    source_1.write_bytes(b"image-one")
    source_2.write_bytes(b"image-two")

    images = [
        GeneratedImage(
            path=str(source_1),
            width=768,
            height=432,
            format="png",
            provider="local",
        ),
        GeneratedImage(
            path=str(source_2),
            width=768,
            height=432,
            format="png",
            provider="local",
        ),
    ]

    manager = ImageOutputManager(
        output_root=tmp_path / "documentaries"
    )

    results = manager.save_images(
        images=images,
        topic="Ancient India",
    )

    assert len(results) == 2

    assert results[0].path.endswith(
        "scene_001.png"
    )

    assert results[1].path.endswith(
        "scene_002.png"
    )

def test_slugify():
    result = ImageOutputManager._slugify(
        "The Mughal Empire!"
    )

    assert result == "the-mughal-empire"


def test_missing_source_image(tmp_path):
    manager = ImageOutputManager(
        output_root=tmp_path / "documentaries"
    )

    image = GeneratedImage(
        path=str(tmp_path / "missing.png"),
        width=768,
        height=432,
        format="png",
        provider="local",
    )

    with pytest.raises(
        ImageProviderError,
        match="does not exist",
    ):
        manager.save_image(
            image=image,
            topic="Mughal Empire",
            scene_number=1,
        )