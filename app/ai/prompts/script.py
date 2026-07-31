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
Create a professional documentary narration.

Topic:
{topic}

Summary:
{summary}

Timeline:
{timeline}

Characters:
{characters}

Sources:
{sources}

Language:
{language}

Generate a documentary script with:

1. Title
2. Hook
3. Introduction
4. Multiple Sections
5. Ending
6. Call To Action
""".strip(),
                ),
            ]
        )