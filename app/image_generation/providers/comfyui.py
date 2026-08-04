import json
import subprocess
from pathlib import Path

from app.image_generation.config.settings import image_settings
from app.image_generation.exceptions import ImageProviderError
from app.image_generation.models import GeneratedImage
from app.image_generation.providers.base import ImageProvider


class ComfyUIImageProvider(ImageProvider):
    """
    Local image provider powered by ComfyUI through Comfy CLI.
    """

    def __init__(
        self,
        checkpoint: str = "dreamshaper_8.safetensors",
    ):
        self.checkpoint = checkpoint

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 768,
        height: int = 432,
    ) -> GeneratedImage:
        command = self._build_command(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
        )

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=image_settings.image_timeout,
            )

        except subprocess.TimeoutExpired as exc:
            raise ImageProviderError(
                "ComfyUI image generation timed out."
            ) from exc

        except subprocess.CalledProcessError as exc:
            error = exc.stderr or exc.stdout

            raise ImageProviderError(
                f"ComfyUI image generation failed: {error}"
            ) from exc

        output_path = self._extract_output_path(
            result.stdout
        )

        return GeneratedImage(
            path=str(output_path),
            width=width,
            height=height,
            format=output_path.suffix.lstrip("."),
            provider="local",
        )

    def _build_command(
        self,
        prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
    ) -> list[str]:
        return [
            "comfy",
            "run",
            "--prompt",
            prompt,
            "--set",
            f"checkpoint={self.checkpoint}",
            "--set",
            f"negative={negative_prompt}",
            "--set",
            f"width={width}",
            "--set",
            f"height={height}",
            "--set",
            "steps=20",
            "--set",
            "cfg=7",
            "--wait",
            "--where",
            "local",
            "--json",
        ]

    @staticmethod
    def _extract_output_path(
        stdout: str,
    ) -> Path:
        """
        Extract generated image path from Comfy CLI NDJSON output.
        """

        for line in stdout.splitlines():
            line = line.strip()

            if not line:
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            path = ComfyUIImageProvider._find_image_path(
                event
            )

            if path is not None:
                return Path(path)

        raise ImageProviderError(
            "ComfyUI completed but no image output was found."
        )

    @staticmethod
    def _find_image_path(
        value,
    ) -> str | None:
        """
        Recursively search a Comfy CLI event for an image path.
        """

        if isinstance(value, str):
            if value.lower().endswith(
                (".png", ".jpg", ".jpeg", ".webp")
            ):
                return value

        elif isinstance(value, dict):
            for item in value.values():
                result = ComfyUIImageProvider._find_image_path(
                    item
                )

                if result is not None:
                    return result

        elif isinstance(value, list):
            for item in value:
                result = ComfyUIImageProvider._find_image_path(
                    item
                )

                if result is not None:
                    return result

        return None