from unittest.mock import MagicMock, patch

import pytest

from app.music.audio_mixer import AudioMixer


def test_mix_audio(
    tmp_path,
):
    narration_1 = tmp_path / "scene_001.mp3"
    narration_2 = tmp_path / "scene_002.mp3"
    music = tmp_path / "background.mp3"
    output = tmp_path / "final_audio.mp3"

    narration_1.write_bytes(b"audio")
    narration_2.write_bytes(b"audio")
    music.write_bytes(b"music")

    mixer = AudioMixer()

    completed = MagicMock()
    completed.returncode = 0
    completed.stderr = ""

    with patch(
        "app.music.audio_mixer.subprocess.run",
        return_value=completed,
    ) as run_mock:
        def create_output(*args, **kwargs):
            output.write_bytes(b"mixed audio")
            return completed

        run_mock.side_effect = create_output

        result = mixer.mix(
            narration_paths=[
                str(narration_1),
                str(narration_2),
            ],
            music_path=str(music),
            output_path=str(output),
        )

    assert result == str(output)
    assert output.is_file()

    run_mock.assert_called_once()


def test_mix_requires_narration(
    tmp_path,
):
    music = tmp_path / "background.mp3"
    music.write_bytes(b"music")

    mixer = AudioMixer()

    with pytest.raises(
        ValueError,
        match="At least one narration",
    ):
        mixer.mix(
            narration_paths=[],
            music_path=str(music),
            output_path=str(
                tmp_path / "output.mp3"
            ),
        )


def test_mix_missing_narration(
    tmp_path,
):
    music = tmp_path / "background.mp3"
    music.write_bytes(b"music")

    mixer = AudioMixer()

    with pytest.raises(
        FileNotFoundError,
        match="Narration file does not exist",
    ):
        mixer.mix(
            narration_paths=[
                str(tmp_path / "missing.mp3")
            ],
            music_path=str(music),
            output_path=str(
                tmp_path / "output.mp3"
            ),
        )


def test_mix_missing_music(
    tmp_path,
):
    narration = tmp_path / "scene_001.mp3"
    narration.write_bytes(b"audio")

    mixer = AudioMixer()

    with pytest.raises(
        FileNotFoundError,
        match="Music file does not exist",
    ):
        mixer.mix(
            narration_paths=[
                str(narration)
            ],
            music_path=str(
                tmp_path / "missing.mp3"
            ),
            output_path=str(
                tmp_path / "output.mp3"
            ),
        )


def test_invalid_music_volume(
    tmp_path,
):
    mixer = AudioMixer()

    with pytest.raises(
        ValueError,
        match="Music volume",
    ):
        mixer.mix(
            narration_paths=["anything.mp3"],
            music_path="music.mp3",
            output_path="output.mp3",
            music_volume=1.5,
        )