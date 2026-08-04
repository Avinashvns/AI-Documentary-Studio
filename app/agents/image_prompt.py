from langchain_core.language_models.chat_models import BaseChatModel

from app.agents.exceptions import ImagePromptAgentError
from app.ai.llm.factory import LLMFactory
from app.ai.prompts.image_prompt import ImagePromptTemplate
from app.schemas.image_prompt import (
    ImagePrompt,
    ImagePromptPlan,
)
from app.schemas.scene import Scene


class ImagePromptAgent:
    def __init__(
        self,
        llm: BaseChatModel | None = None,
    ):
        self.llm = llm or LLMFactory.create()

    def run(
        self,
        scenes: list[Scene],
        style: str = "cinematic historical documentary",
    ) -> list[ImagePrompt]:
        try:
            prompt = ImagePromptTemplate.build()

            structured_llm = self.llm.with_structured_output(
                ImagePromptPlan
            )

            chain = prompt | structured_llm

            result: ImagePromptPlan = chain.invoke(
                {
                    "scenes": [
                        scene.model_dump()
                        for scene in scenes
                    ],
                    "style": style,
                }
            )

            return result.image_prompts

        except Exception as exc:
            raise ImagePromptAgentError(
                f"Image prompt generation failed: {exc}"
            ) from exc