import re
import shutil
from pathlib import Path

from app.image_generation.exceptions import ImageProviderError
from app.image_generation.models import GeneratedImage


class ImageOutputManager:
    """
    Organizes generated images into documentary-specific
    output directories with predictable scene filenames.
    """

    def __init__(
        self,
        output_root: str | Path = "outputs/documentaries",
    ):
        self.output_root = Path(output_root)

    def save_image(
        self,
        image: GeneratedImage,
        topic: str,
        scene_number: int,
    ) -> GeneratedImage:
        source = Path(image.path)

        if not source.exists():
            raise ImageProviderError(
                f"Generated image does not exist: {source}"
            )

        documentary_dir = (
            self.output_root
            / self._slugify(topic)
            / "images"
        )

        documentary_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        extension = source.suffix or f".{image.format}"

        destination = documentary_dir / (
            f"scene_{scene_number:03d}{extension}"
        )

        shutil.copy2(
            source,
            destination,
        )

        return GeneratedImage(
            path=str(destination),
            width=image.width,
            height=image.height,
            format=image.format,
            provider=image.provider,
        )

    def save_images(
        self,
        images: list[GeneratedImage],
        topic: str,
    ) -> list[GeneratedImage]:
        return [
            self.save_image(
                image=image,
                topic=topic,
                scene_number=index,
            )
            for index, image in enumerate(
                images,
                start=1,
            )
        ]

    @staticmethod
    def _slugify(value: str) -> str:
        value = value.strip().lower()

        value = re.sub(
            r"[^a-z0-9]+",
            "-",
            value,
        )

        return value.strip("-")