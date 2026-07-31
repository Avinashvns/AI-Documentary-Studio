from pydantic import BaseModel


class ImagePrompt(BaseModel):
    scene_number: int

    prompt: str

    negative_prompt: str = ""