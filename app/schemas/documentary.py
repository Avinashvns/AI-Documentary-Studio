from pydantic import BaseModel
from pydantic import Field

from app.schemas.request import DocumentaryRequest
from app.schemas.research import ResearchResult
from app.schemas.script import ScriptResult
from app.schemas.scene import Scene
from app.schemas.image_prompt import ImagePrompt
from app.schemas.voice import VoiceConfig
from app.schemas.music import MusicConfig
from app.schemas.render import RenderConfig


class Documentary(BaseModel):

    request: DocumentaryRequest

    research: ResearchResult | None = None

    script: ScriptResult | None = None

    scenes: list[Scene] = Field(default_factory=list)

    image_prompts: list[ImagePrompt] = Field(default_factory=list)

    voice: VoiceConfig | None = None

    music: MusicConfig | None = None

    render: RenderConfig