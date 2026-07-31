from pydantic import BaseModel


class ScriptSection(BaseModel):
    title: str
    narration: str


class ScriptResult(BaseModel):
    title: str

    hook: str

    introduction: str

    sections: list[ScriptSection]

    ending: str

    cta: str