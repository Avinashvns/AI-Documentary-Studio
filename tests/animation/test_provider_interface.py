import pytest

from app.animation.models import GeneratedVideo
from app.animation.providers.base import AnimationProvider


def test_animation_provider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AnimationProvider()


def test_generated_video_model():
    video = GeneratedVideo(
        path="scene_001.mp4",
        width=512,
        height=512,
        fps=16,
        frame_count=33,
        provider="comfyui",
    )

    assert video.path == "scene_001.mp4"
    assert video.width == 512
    assert video.height == 512
    assert video.fps == 16
    assert video.frame_count == 33
    assert video.provider == "comfyui"

    assert video.duration == pytest.approx(
        33 / 16
    )


def test_concrete_provider_implements_interface():
    class FakeAnimationProvider(AnimationProvider):
        def generate(
            self,
            image_path: str,
            prompt: str,
            negative_prompt: str = "",
            width: int = 512,
            height: int = 512,
            frame_count: int = 33,
            fps: int = 16,
        ) -> GeneratedVideo:
            return GeneratedVideo(
                path="generated.mp4",
                width=width,
                height=height,
                fps=fps,
                frame_count=frame_count,
                provider="fake",
            )

    provider = FakeAnimationProvider()

    result = provider.generate(
        image_path="scene_001.png",
        prompt="slow cinematic zoom",
    )

    assert isinstance(
        result,
        GeneratedVideo,
    )

    assert result.path == "generated.mp4"
    assert result.provider == "fake"


def test_provider_without_generate_cannot_be_instantiated():
    class InvalidProvider(AnimationProvider):
        pass

    with pytest.raises(TypeError):
        InvalidProvider()