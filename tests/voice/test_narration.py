from unittest.mock import MagicMock

from app.schemas.scene import Scene
from app.voice.narration import NarrationService


def test_generate_scene_narrations(
    tmp_path,
):
    tts = MagicMock()

    tts.generate.side_effect = (
        lambda text, output_path: output_path
    )

    service = NarrationService(
        tts=tts,
        output_root=tmp_path,
    )

    scenes = [
        Scene(
            number=1,
            title="Babur",
            narration="Babur entered northern India.",
            duration=10,
        ),
        Scene(
            number=2,
            title="Panipat",
            narration="The armies met at Panipat.",
            duration=10,
        ),
    ]

    result = service.generate(
        scenes=scenes,
        topic="Mughal Empire",
    )

    assert result == [
        str(
            tmp_path
            / "mughal-empire"
            / "audio"
            / "scene_001.mp3"
        ),
        str(
            tmp_path
            / "mughal-empire"
            / "audio"
            / "scene_002.mp3"
        ),
    ]

    assert tts.generate.call_count == 2


def test_generate_empty_scenes(
    tmp_path,
):
    tts = MagicMock()

    service = NarrationService(
        tts=tts,
        output_root=tmp_path,
    )

    result = service.generate(
        scenes=[],
        topic="Mughal Empire",
    )

    assert result == []

    tts.generate.assert_not_called()