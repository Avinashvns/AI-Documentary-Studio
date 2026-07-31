from langchain_core.prompts import ChatPromptTemplate

from app.ai.prompts.system import SYSTEM_PROMPT


class ResearchPrompt:
    @staticmethod
    def build() -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    """
Research the following documentary topic.

Topic:
{topic}

Return:

1. Summary

2. Timeline

3. Key Characters

4. Interesting Facts

5. Reliable Sources
""".strip(),
                ),
            ]
        )
