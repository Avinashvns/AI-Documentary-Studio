from pydantic import BaseModel


class MusicConfig(BaseModel):
    provider: str
    genre: str
    volume: float = 0.3