from pathlib import Path

import pytest

from app.agents.animation_agent import AnimationAgent
from app.ai.llm.factory import LLMFactory
from app.animation.providers.comfyui import (
    ComfyUIAnimationProvider,
)
from app.animation.services.animation_service import (
    AnimationService,
)
from app.schemas.scene import Scene


@pytest.mark.e2e
@pytest.mark.slow
def test_animation_pipeline_e2e():
    """
    Test the real animation pipeline:

    Scene
        -> LLM
        -> AnimationAgent
        -> AnimationInstruction
        -> AnimationService
        -> ComfyUI
        -> Wan 2.1
        -> MP4
    """

    # ---------------------------------
    # 1. Existing documentary image
    # ---------------------------------

    image_path = Path(
        "outputs/documentaries/"
        "mughal-empire/images/"
        "scene_001.png"
    )

    assert image_path.is_file(), (
        f"Test image does not exist: {image_path}"
    )

    # ---------------------------------
    # 2. Documentary scene
    # ---------------------------------

    scene = Scene(
        number=1,
        title="The Beginning of the Mughal Empire",
        narration=(
            "Babur entered northern India, "
            "beginning a new chapter in history."
        ),
        duration=30,
    )

    # ---------------------------------
    # 3. Production LLM
    # ---------------------------------

    llm = LLMFactory.create()

    # ---------------------------------
    # 4. Animation Agent
    # ---------------------------------

    animation_agent = AnimationAgent(
        llm=llm,
    )

    instructions = animation_agent.run(
        scenes=[scene],
    )

    assert len(instructions) == 1

    instruction = instructions[0]

    assert instruction.scene_number == 1
    assert instruction.prompt
    assert instruction.camera_motion in {
        "Zoom In",
        "Zoom Out",
        "Pan Left",
        "Pan Right",
    }

    # ---------------------------------
    # 5. Real ComfyUI Provider
    # ---------------------------------

    provider = ComfyUIAnimationProvider(
        workflow_path=(
            "app/animation/workflows/"
            "wan21_fun_camera_1.3b_api.json"
        ),
        timeout=600,
    )

    # ---------------------------------
    # 6. Animation Service
    # ---------------------------------

    service = AnimationService(
        provider=provider,
    )

    # ---------------------------------
    # 7. Generate real animation
    # ---------------------------------

    video = service.generate_animation(
        image_path=str(image_path),
        prompt=instruction.prompt,
        negative_prompt=(
            instruction.negative_prompt
        ),
        camera_motion=(
            instruction.camera_motion
        ),
        width=512,
        height=512,
        frame_count=33,
        fps=16,
    )

    # ---------------------------------
    # 8. Validate generated video
    # ---------------------------------

    video_path = Path(video.path)

    assert video_path.is_file()

    assert video.provider == "comfyui"

    assert video.width == 512
    assert video.height == 512

    assert video.frame_count == 33
    assert video.fps == 16

    assert video.duration > 0

    assert video_path.suffix.lower() == ".mp4"