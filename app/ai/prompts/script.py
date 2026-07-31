from langchain_core.prompts import ChatPromptTemplate

from app.ai.prompts.system import SYSTEM_PROMPT


class ScriptPrompt:

    @staticmethod
    def build():

        return ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    """
Using the following research:

{research}

Write a professional documentary narration.

Requirements:

- Strong hook
- Chronological flow
- Cinematic narration
- Engaging ending
""".strip(),
                ),
            ]
        )