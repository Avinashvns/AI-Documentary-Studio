from pydantic import BaseModel


class RenderConfig(BaseModel):
    resolution: str = "2K"
    fps: int = 30
    format: str = "mp4"