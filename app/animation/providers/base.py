from abc import ABC, abstractmethod

from app.animation.models import GeneratedVideo


class AnimationProvider(ABC):
    """
    Base interface for all image-to-video providers.

    Implementations may use ComfyUI, cloud APIs,
    or other animation backends.
    """

    @abstractmethod
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
        """
        Generate a video from a source image.
        """
        raise NotImplementedError