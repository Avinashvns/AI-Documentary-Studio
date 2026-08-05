import re
from pathlib import Path

from app.schemas.scene import Scene
from app.voice.tts import TextToSpeech


class NarrationService:
    """
    Generates narration audio for documentary scenes.
    """

    def __init__(
        self,
        tts: TextToSpeech,
        output_root: str | Path = "outputs/documentaries",
    ):
        self.tts = tts
        self.output_root = Path(output_root)

    def generate(
        self,
        scenes: list[Scene],
        topic: str,
    ) -> list[str]:
        if not scenes:
            return []

        audio_dir = (
            self.output_root
            / self._slugify(topic)
            / "audio"
        )

        audio_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        audio_paths = []

        for scene in scenes:
            output_path = (
                audio_dir
                / f"scene_{scene.number:03d}.mp3"
            )

            generated_path = self.tts.generate(
                text=scene.narration,
                output_path=str(output_path),
            )

            audio_paths.append(
                generated_path
            )

        return audio_paths

    @staticmethod
    def _slugify(value: str) -> str:
        value = value.strip().lower()

        value = re.sub(
            r"[^a-z0-9]+",
            "-",
            value,
        )

        return value.strip("-")