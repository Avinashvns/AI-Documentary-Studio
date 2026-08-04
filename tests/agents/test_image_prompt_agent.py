from unittest.mock import patch

from app.agents.image_prompt import ImagePromptAgent
from app.schemas.image_prompt import (
    ImagePrompt,
    ImagePromptPlan,
)
from app.schemas.scene import Scene
from tests.fakes.fake_llm import FakeLLM


@patch(
    "app.agents.image_prompt.ImagePromptTemplate.build"
)
def test_image_prompt_agent(mock_prompt):
    expected = ImagePromptPlan(
        image_prompts=[
            ImagePrompt(
                scene_number=1,
                prompt=(
                    "Babur standing on a historical battlefield "
                    "in 1526, Mughal army in the background, "
                    "cinematic wide shot, realistic lighting, "
                    "photorealistic historical documentary style"
                ),
                negative_prompt=(
                    "modern clothing, cars, text, watermark, "
                    "cartoon, blurry image"
                ),
            ),
            ImagePrompt(
                scene_number=2,
                prompt=(
                    "Mughal soldiers advancing across a dusty "
                    "battlefield, historical armor and weapons, "
                    "dramatic cinematic composition, photorealistic"
                ),
                negative_prompt=(
                    "modern weapons, text, watermark, cartoon"
                ),
            ),
        ]
    )

    fake_llm = FakeLLM(expected)

    fake_prompt = mock_prompt.return_value

    fake_prompt.__or__.return_value = (
        fake_llm.with_structured_output(
            ImagePromptPlan
        )
    )

    scenes = [
        Scene(
            number=1,
            title="The Arrival of Babur",
            narration="Babur entered northern India.",
            duration=20,
        ),
        Scene(
            number=2,
            title="The Battle Begins",
            narration="The armies prepared for battle.",
            duration=25,
        ),
    ]

    agent = ImagePromptAgent(
        llm=fake_llm
    )

    result = agent.run(
        scenes=scenes,
        style="historical cinematic documentary",
    )

    assert len(result) == 2

    assert result[0].scene_number == 1

    assert result[1].scene_number == 2

    assert result[0].prompt != ""

    assert result[0].negative_prompt != ""