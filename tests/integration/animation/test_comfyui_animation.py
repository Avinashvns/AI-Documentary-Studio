from pathlib import Path

import pytest

from app.animation.providers.comfyui import (
    ComfyUIAnimationProvider,
)


@pytest.mark.integration
@pytest.mark.slow
def test_real_comfyui_animation():
    provider = ComfyUIAnimationProvider(
        workflow_path=(
            "app/animation/workflows/"
            "wan21_fun_camera_1.3b_api.json"
        ),
        timeout=600,
    )

    image_path = Path(
        "outputs/documentaries/"
        "mughal-empire/images/scene_001.png"
    )

    result = provider.generate(
        image_path=str(image_path),
        prompt=(
            "cinematic historical documentary, "
            "subtle natural movement, "
            "slow cinematic zoom, "
            "photorealistic"
        ),
        negative_prompt=(
            "cartoon, blurry, distorted, "
            "flickering, jitter, watermark, text"
        ),
        width=512,
        height=512,
        frame_count=33,
        fps=16,
    )

    assert Path(result.path).is_file()
    assert result.provider == "comfyui"
    assert result.width == 512
    assert result.height == 512
    assert result.frame_count == 33
    assert result.fps == 16
    assert result.duration > 0