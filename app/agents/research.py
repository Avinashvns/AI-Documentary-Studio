from langchain_core.language_models.chat_models import BaseChatModel

from app.ai.llm.factory import LLMFactory
from app.ai.prompts.research import ResearchPrompt
from app.schemas.research import ResearchResult
from app.agents.exceptions import ResearchAgentError

from app.schemas.request import DocumentaryRequest


class ResearchAgent:
    def __init__(self, llm: BaseChatModel | None = None):
        """
        If no LLM is provided, create the default one from the factory.
        """
        self.llm = llm or LLMFactory.create()

    def run(
        self,
        request: DocumentaryRequest,
    ) -> ResearchResult:
        try:
            prompt = ResearchPrompt.build()

            structured_llm = self.llm.with_structured_output(ResearchResult)

            chain = prompt | structured_llm

            return chain.invoke(
                {
                    "topic": request.topic,
                    "language": request.language,
                    "duration": request.duration,
                    "style": request.style,
                }
            )

        except Exception as exc:
            raise ResearchAgentError(str(exc)) from exc
