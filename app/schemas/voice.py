from pydantic import BaseModel


class VoiceConfig(BaseModel):
    provider: str
    voice: str
    speed: float = 1.0