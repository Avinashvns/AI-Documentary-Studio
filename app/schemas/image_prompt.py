from pydantic import BaseModel, Field


class ImagePrompt(BaseModel):
    scene_number: int = Field(
        ge=1,
        description="Scene number associated with the image prompt",
    )

    prompt: str = Field(
        min_length=10,
        description="Positive prompt used for image generation",
    )

    negative_prompt: str = Field(
        default="",
        description="Elements that should not appear in the image",
    )


class ImagePromptPlan(BaseModel):
    image_prompts: list[ImagePrompt] = Field(
        default_factory=list
    )