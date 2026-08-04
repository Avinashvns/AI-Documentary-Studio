from langchain_core.language_models.chat_models import BaseChatModel

from app.agents.exceptions import ScenePlannerAgentError
from app.ai.llm.factory import LLMFactory
from app.ai.prompts.scene import ScenePrompt
from app.schemas.scene import Scene, ScenePlan
from app.schemas.script import ScriptResult


class ScenePlannerAgent:
    def __init__(
        self,
        llm: BaseChatModel | None = None,
    ):
        self.llm = llm or LLMFactory.create()

    def run(
        self,
        script: ScriptResult,
        duration: int = 10,
    ) -> list[Scene]:
        try:
            prompt = ScenePrompt.build()

            structured_llm = self.llm.with_structured_output(
                ScenePlan
            )

            chain = prompt | structured_llm

            result: ScenePlan = chain.invoke(
                {
                    "title": script.title,
                    "hook": script.hook,
                    "introduction": script.introduction,
                    "sections": [
                        section.model_dump()
                        for section in script.sections
                    ],
                    "ending": script.ending,
                    "cta": script.cta,
                    "duration": duration,
                }
            )

            return result.scenes

        except Exception as exc:
            raise ScenePlannerAgentError(
                f"Scene planning failed: {exc}"
            ) from exc