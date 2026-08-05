import re
import shutil
from pathlib import Path


class MusicManager:
    """
    Validates and organizes documentary background music.
    """

    SUPPORTED_FORMATS = {
        ".mp3",
        ".wav",
        ".m4a",
        ".aac",
    }

    def __init__(
        self,
        output_root: str | Path = "outputs/documentaries",
    ):
        self.output_root = Path(output_root)

    def prepare(
        self,
        source_path: str | Path,
        topic: str,
    ) -> str:
        source = Path(source_path)

        if not source.is_file():
            raise FileNotFoundError(
                f"Music file does not exist: {source}"
            )

        extension = source.suffix.lower()

        if extension not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported music format: {extension}"
            )

        music_dir = (
            self.output_root
            / self._slugify(topic)
            / "music"
        )

        music_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            music_dir
            / f"background{extension}"
        )

        shutil.copy2(
            source,
            destination,
        )

        return str(destination)

    @staticmethod
    def _slugify(
        value: str,
    ) -> str:
        value = value.strip().lower()

        value = re.sub(
            r"[^a-z0-9]+",
            "-",
            value,
        )

        return value.strip("-")