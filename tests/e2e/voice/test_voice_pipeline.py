from pathlib import Path

import pytest

from app.schemas.scene import Scene
from app.schemas.voice import VoiceConfig
from app.voice.narration import NarrationService
from app.voice.tts import TextToSpeech


@pytest.mark.e2e
def test_voice_pipeline_e2e(
    tmp_path,
):
    config = VoiceConfig(
        provider="edge",
        voice="hi-IN-MadhurNeural",
        speed=1.0,
    )

    tts = TextToSpeech(
        config=config,
    )

    service = NarrationService(
        tts=tts,
        output_root=tmp_path,
    )

    scenes = [
        Scene(
            number=1,
            title="The Beginning",
            narration=(
                "बाबर ने भारत में मुगल साम्राज्य "
                "की नींव रखी।"
            ),
            duration=10,
        )
    ]

    result = service.generate(
        scenes=scenes,
        topic="Mughal Empire",
    )

    assert len(result) == 1

    audio_path = Path(
        result[0]
    )

    assert audio_path.is_file()

    assert audio_path.suffix == ".mp3"

    assert audio_path.stat().st_size > 0

    assert audio_path.name == (
        "scene_001.mp3"
    )

    assert audio_path.parent.name == "audio"

    assert (
        audio_path.parent.parent.name
        == "mughal-empire"
    )