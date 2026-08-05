from typing import TypedDict

from app.schemas.animation import AnimationInstruction
from app.schemas.research import ResearchResult
from app.schemas.script import ScriptResult
from app.schemas.scene import Scene
from app.schemas.image_prompt import ImagePrompt


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
    research: ResearchResult | None

    # Script
    script: ScriptResult | None

    # Scene Planning
    scenes: list[Scene]

    # Image Generation
    image_prompts: list[ImagePrompt]
    images: list[str]

     # Animation
    animation_instructions: list[
        AnimationInstruction
    ]
    animations: list[str]

    # Voice / Narration
    audio_paths: list[str]

    # Music
    music_path: str

    # Captions
    subtitles_path: str

    # Export
    output_video: str