import pytest

from app.voice.tts import TextToSpeech


def test_speed_to_rate():
    assert TextToSpeech._speed_to_rate(1.0) == "+0%"
    assert TextToSpeech._speed_to_rate(1.1) == "+10%"
    assert TextToSpeech._speed_to_rate(0.9) == "-10%"


def test_empty_narration():
    from app.schemas.voice import VoiceConfig

    tts = TextToSpeech(
        VoiceConfig(
            provider="edge",
            voice="hi-IN-MadhurNeural",
        )
    )

    with pytest.raises(
        ValueError,
        match="Narration text cannot be empty",
    ):
        tts.generate(
            text="",
            output_path="outputs/test.mp3",
        )