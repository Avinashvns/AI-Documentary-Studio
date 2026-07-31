from pydantic import BaseModel


class GenerationResponse(BaseModel):
    success: bool
    message: str
    output_video: str | None = None