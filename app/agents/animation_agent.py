from typing import Any

from app.schemas.animation import AnimationInstruction
from app.schemas.scene import Scene


class AnimationAgent:
    """
    Plans cinematic animation instructions
    for documentary scenes.
    """

    def __init__(
        self,
        llm: Any,
    ):
        self.llm = llm

        self.structured_llm = (
            llm.with_structured_output(
                AnimationInstruction
            )
        )

    def run(
        self,
        scenes: list[Scene],
    ) -> list[AnimationInstruction]:
        return [
            self._plan_scene(scene)
            for scene in scenes
        ]

    def _plan_scene(
        self,
        scene: Scene,
    ) -> AnimationInstruction:
        prompt = self._build_prompt(
            scene
        )

        return self.structured_llm.invoke(
            prompt
        )

    @staticmethod
    def _build_prompt(
        scene: Scene,
    ) -> str:
        return f"""
You are a cinematic animation director
for historical documentary videos.

Create subtle and realistic animation
instructions for the following scene.

Scene Number:
{scene.number}

Scene Title:
{scene.title}

Narration:
{scene.narration}

Choose one suitable camera motion from:

- Zoom In
- Zoom Out
- Pan Left
- Pan Right

Create an animation prompt describing:

- subtle subject movement
- natural environmental movement
- cinematic camera movement
- realistic lighting continuity
- preservation of the original composition

Avoid:

- excessive movement
- unrealistic motion
- flickering
- jitter
- distorted objects
- warped architecture
- modern objects
- text
- watermark

The final animation should look like a
cinematic historical documentary shot.
""".strip()