from pydantic import BaseModel, Field


class DocumentaryRequest(BaseModel):
    topic: str = Field(..., min_length=3)
    language: str = Field(default="Hindi")
    duration: int = Field(default=10, ge=1, le=180)
    style: str = Field(default="documentary")