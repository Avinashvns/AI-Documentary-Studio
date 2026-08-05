from app.animation.models import GeneratedVideo
from app.animation.providers.base import AnimationProvider


class AnimationService:
    """
    Coordinates animation generation for documentary scenes.
    """

    def __init__(
        self,
        provider: AnimationProvider,
    ):
        self.provider = provider

    def generate_animation(
        self,
        image_path: str,
        prompt: str,
        negative_prompt: str = "",
        camera_motion: str = "Zoom In",
        width: int = 512,
        height: int = 512,
        frame_count: int = 33,
        fps: int = 16,
    ) -> GeneratedVideo:
        return self.provider.generate(
            image_path=image_path,
            prompt=prompt,
            negative_prompt=negative_prompt,
            camera_motion=camera_motion,
            width=width,
            height=height,
            frame_count=frame_count,
            fps=fps,
        )

    def generate_animations(
        self,
        images: list[str],
        prompts: list[str],
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        frame_count: int = 33,
        fps: int = 16,
    ) -> list[GeneratedVideo]:
        if len(images) != len(prompts):
            raise ValueError(
                "Images and prompts must have "
                "the same length."
            )

        return [
            self.generate_animation(
                image_path=image_path,
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                frame_count=frame_count,
                fps=fps,
            )
            for image_path, prompt in zip(
                images,
                prompts,
                strict=True,
            )
        ]