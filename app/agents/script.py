from langchain_core.language_models.chat_models import BaseChatModel

from app.agents.exceptions import ScriptAgentError
from app.ai.llm.factory import LLMFactory
from app.ai.prompts.script import ScriptPrompt
from app.schemas.research import ResearchResult
from app.schemas.script import ScriptResult


class ScriptAgent:

    def __init__(
        self,
        llm: BaseChatModel | None = None,
    ):
        self.llm = llm or LLMFactory.create()

    def run(
        self,
        research: ResearchResult,
        language: str = "English",
    ) -> ScriptResult:

        try:

            prompt = ScriptPrompt.build()

            structured_llm = self.llm.with_structured_output(
                ScriptResult
            )

            chain = prompt | structured_llm

            return chain.invoke(
                {
                    "topic": research.topic,
                    "summary": research.summary,
                    "timeline": [
                        event.model_dump()
                        for event in research.timeline
                    ],
                    "characters": [
                        character.model_dump()
                        for character in research.characters
                    ],
                    "sources": research.sources,
                    "language": language,
                }
            )

        except Exception as exc:
            raise ScriptAgentError(
                f"Script generation failed: {exc}"
            ) from exc