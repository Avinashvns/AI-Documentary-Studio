import asyncio
from pathlib import Path

import edge_tts

from app.schemas.voice import VoiceConfig


class TextToSpeech:
    """
    Generates documentary narration audio using Edge TTS.
    """

    def __init__(
        self,
        config: VoiceConfig,
    ):
        self.config = config

    def generate(
        self,
        text: str,
        output_path: str,
    ) -> str:
        if not text.strip():
            raise ValueError(
                "Narration text cannot be empty."
            )

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        asyncio.run(
            self._generate(
                text=text,
                output_path=str(path),
            )
        )

        return str(path)

    async def _generate(
        self,
        text: str,
        output_path: str,
    ) -> None:
        rate = self._speed_to_rate(
            self.config.speed
        )

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.config.voice,
            rate=rate,
        )

        await communicate.save(
            output_path
        )

    @staticmethod
    def _speed_to_rate(
        speed: float,
    ) -> str:
        percentage = round(
            (speed - 1.0) * 100
        )

        return f"{percentage:+d}%"