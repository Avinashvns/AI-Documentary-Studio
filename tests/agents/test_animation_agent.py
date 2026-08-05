from unittest.mock import MagicMock

from app.agents.animation_agent import AnimationAgent
from app.schemas.animation import AnimationInstruction
from app.schemas.scene import Scene


def test_animation_agent():
    llm = MagicMock()
    structured_llm = MagicMock()

    llm.with_structured_output.return_value = (
        structured_llm
    )

    expected = AnimationInstruction(
        scene_number=1,
        prompt=(
            "slow cinematic zoom toward "
            "the historical palace"
        ),
        negative_prompt=(
            "flickering, jitter, distortion"
        ),
        camera_motion="Zoom In",
    )

    structured_llm.invoke.return_value = (
        expected
    )

    agent = AnimationAgent(
        llm=llm,
    )

    scenes = [
        Scene(
            number=1,
            title="The Beginning",
            narration=(
                "Babur entered northern India."
            ),
            duration=30,
        )
    ]

    result = agent.run(
        scenes=scenes,
    )

    assert result == [
        expected
    ]

    llm.with_structured_output.assert_called_once_with(
        AnimationInstruction
    )

    structured_llm.invoke.assert_called_once()


def test_animation_agent_multiple_scenes():
    llm = MagicMock()
    structured_llm = MagicMock()

    llm.with_structured_output.return_value = (
        structured_llm
    )

    structured_llm.invoke.side_effect = [
        AnimationInstruction(
            scene_number=1,
            prompt=(
                "slow cinematic zoom"
            ),
            negative_prompt=(
                "flickering, jitter"
            ),
            camera_motion="Zoom In",
        ),
        AnimationInstruction(
            scene_number=2,
            prompt=(
                "slow cinematic pan"
            ),
            negative_prompt=(
                "flickering, distortion"
            ),
            camera_motion="Pan Right",
        ),
    ]

    agent = AnimationAgent(
        llm=llm,
    )

    scenes = [
        Scene(
            number=1,
            title="The Beginning",
            narration=(
                "The empire begins."
            ),
            duration=20,
        ),
        Scene(
            number=2,
            title="Expansion",
            narration=(
                "The empire expands."
            ),
            duration=20,
        ),
    ]

    result = agent.run(
        scenes=scenes,
    )

    assert len(result) == 2

    assert (
        result[0].scene_number
        == 1
    )

    assert (
        result[0].camera_motion
        == "Zoom In"
    )

    assert (
        result[1].scene_number
        == 2
    )

    assert (
        result[1].camera_motion
        == "Pan Right"
    )

    assert (
        structured_llm.invoke.call_count
        == 2
    )

    llm.with_structured_output.assert_called_once_with(
        AnimationInstruction
    )


def test_animation_agent_empty_scenes():
    llm = MagicMock()
    structured_llm = MagicMock()

    llm.with_structured_output.return_value = (
        structured_llm
    )

    agent = AnimationAgent(
        llm=llm,
    )

    result = agent.run(
        scenes=[],
    )

    assert result == []

    structured_llm.invoke.assert_not_called()