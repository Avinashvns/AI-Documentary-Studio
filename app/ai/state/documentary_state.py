from typing import TypedDict


class DocumentaryState(TypedDict):
    """
    Shared state for the LangGraph workflow.
    """

    # User Input
    topic: str
    language: str
    duration: int
    style: str

    # Research
    research: str

    # Script
    script: str

    # Scene Planning
    scenes: list

    # Image Generation
    image_prompts: list
    images: list

    # Voice
    narration: str
    audio_path: str

    # Music
    music_path: str

    # Captions
    subtitles_path: str

    # Export
    output_video: str