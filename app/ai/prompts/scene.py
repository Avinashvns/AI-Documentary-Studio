from langchain_core.prompts import ChatPromptTemplate

from app.ai.prompts.system import SYSTEM_PROMPT


class ScenePrompt:
    @staticmethod
    def build() -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    """
Convert the following documentary script into visual scenes.

Documentary Title:
{title}

Hook:
{hook}

Introduction:
{introduction}

Script Sections:
{sections}

Ending:
{ending}

Call To Action:
{cta}

Target Duration:
{duration} minutes

Create a chronological scene plan.

Each scene must contain:

1. Scene number
2. Short descriptive title
3. Narration for that scene
4. Duration in seconds

Requirements:

- Preserve the logical order of the documentary.
- Keep narration suitable for voice-over.
- Break long narration into multiple scenes when necessary.
- Keep scene durations realistic for image-based documentary videos.
- The combined scene durations should approximately match the target duration.
- Scene numbers must start from 1 and remain sequential.
""".strip(),
                ),
            ]
        )