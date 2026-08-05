from pydantic import BaseModel, Field


class AnimationInstruction(BaseModel):
    scene_number: int = Field(
        ge=1,
    )

    prompt: str = Field(
        min_length=1,
    )

    negative_prompt: str = ""

    camera_motion: str = "Zoom In"