from typing import Literal

from pydantic import BaseModel, Field


CameraMotion = Literal[
    "Zoom In",
    "Zoom Out",
    "Pan Left",
    "Pan Right",
]


class AnimationInstruction(BaseModel):
    scene_number: int = Field(
        ge=1,
    )

    prompt: str = Field(
        min_length=1,
    )

    negative_prompt: str = ""

    camera_motion: CameraMotion = "Zoom In"