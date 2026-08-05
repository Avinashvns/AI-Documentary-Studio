import subprocess
import tempfile
from pathlib import Path


class AudioMixer:
    """
    Combines scene narration audio and background music
    into a single documentary audio track using FFmpeg.
    """

    def __init__(
        self,
        ffmpeg_binary: str = "ffmpeg",
    ):
        self.ffmpeg_binary = ffmpeg_binary

    def mix(
        self,
        narration_paths: list[str],
        music_path: str,
        output_path: str,
        music_volume: float = 0.20,
    ) -> str:
        if not narration_paths:
            raise ValueError(
                "At least one narration file is required."
            )

        if not 0.0 <= music_volume <= 1.0:
            raise ValueError(
                "Music volume must be between 0.0 and 1.0."
            )

        narrations = [
            Path(path)
            for path in narration_paths
        ]

        for narration in narrations:
            if not narration.is_file():
                raise FileNotFoundError(
                    f"Narration file does not exist: "
                    f"{narration}"
                )

        music = Path(music_path)

        if not music.is_file():
            raise FileNotFoundError(
                f"Music file does not exist: {music}"
            )

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            concat_file = (
                Path(temp_dir)
                / "narrations.txt"
            )

            self._write_concat_file(
                concat_file=concat_file,
                narration_paths=narrations,
            )

            command = [
                self.ffmpeg_binary,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-stream_loop",
                "-1",
                "-i",
                str(music),
                "-filter_complex",
                (
                    f"[1:a]volume={music_volume}[music];"
                    "[0:a][music]"
                    "amix=inputs=2:"
                    "duration=first:"
                    "dropout_transition=2"
                    "[mixed]"
                ),
                "-map",
                "[mixed]",
                "-c:a",
                "libmp3lame",
                "-q:a",
                "2",
                str(output),
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    "FFmpeg audio mixing failed:\n"
                    f"{result.stderr}"
                )

        if not output.is_file():
            raise RuntimeError(
                "FFmpeg completed but output "
                "audio was not created."
            )

        return str(output)

    @staticmethod
    def _write_concat_file(
        concat_file: Path,
        narration_paths: list[Path],
    ) -> None:
        lines = []

        for path in narration_paths:
            absolute_path = (
                path.resolve()
                .as_posix()
                .replace("'", r"'\''")
            )

            lines.append(
                f"file '{absolute_path}'"
            )

        concat_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )