from app.ai.state.documentary_state import DocumentaryState


def test_state_creation():
    state: DocumentaryState = {
        "topic": "Mughal Empire",
        "language": "Hindi",
        "duration": 10,
        "style": "documentary",
        "research": "",
        "script": "",
        "scenes": [],
        "image_prompts": [],
        "images": [],
        "narration": "",
        "audio_path": "",
        "music_path": "",
        "subtitles_path": "",
        "output_video": "",
    }

    assert state["topic"] == "Mughal Empire"
    assert state["duration"] == 10