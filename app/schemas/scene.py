from pydantic import BaseModel


class Scene(BaseModel):
    number: int

    title: str

    narration: str

    duration: int