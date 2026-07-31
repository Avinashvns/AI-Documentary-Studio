from pydantic import BaseModel, Field


class TimelineEvent(BaseModel):
    year: str = Field(..., description="Year of the event")
    title: str
    description: str


class Character(BaseModel):
    name: str
    role: str


class ResearchResult(BaseModel):
    topic: str

    summary: str

    timeline: list[TimelineEvent] = Field(default_factory=list)

    characters: list[Character] = Field(default_factory=list)

    sources: list[str] = Field(default_factory=list)