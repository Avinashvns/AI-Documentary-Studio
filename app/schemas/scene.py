from pydantic import BaseModel, Field


class Scene(BaseModel):
    number: int = Field(ge=1)

    title: str

    narration: str

    duration: int = Field(
        ge=1,
        description="Scene duration in seconds",
    )


class ScenePlan(BaseModel):
    scenes: list[Scene] = Field(default_factory=list)