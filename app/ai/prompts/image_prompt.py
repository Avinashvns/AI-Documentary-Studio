from langchain_core.prompts import ChatPromptTemplate

from app.ai.prompts.system import SYSTEM_PROMPT


class ImagePromptTemplate:
    @staticmethod
    def build() -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    """
Create high-quality image generation prompts for the following
documentary scenes.

Scenes:
{scenes}

Documentary Style:
{style}

For every scene, create exactly one image prompt.

Each result must contain:

1. Scene number
2. Positive image prompt
3. Negative prompt

Positive prompt requirements:

- Clearly describe the main subject.
- Describe the historical period when relevant.
- Describe clothing, architecture, environment, and atmosphere.
- Use cinematic composition.
- Include appropriate camera framing.
- Include realistic lighting.
- Prefer photorealistic documentary visuals.
- Maintain historical accuracy.
- Avoid unnecessary text inside the image.
- Keep visual style consistent across scenes.

Negative prompt should exclude unwanted elements such as:

- modern objects in historical scenes
- modern clothing
- incorrect architecture
- text
- watermark
- logo
- blurry image
- distorted faces
- bad anatomy
- duplicate people
- cartoon appearance

Preserve the original scene numbers.
""".strip(),
                ),
            ]
        )