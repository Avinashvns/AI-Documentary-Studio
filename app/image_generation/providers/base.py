from abc import ABC, abstractmethod

from app.image_generation.models import GeneratedImage


class ImageProvider(ABC):
    """
    Base interface for all image generation providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 576,
    ) -> GeneratedImage:
        """
        Generate a single image from a text prompt.

        Args:
            prompt:
                Positive image generation prompt.

            negative_prompt:
                Elements that should not appear in the image.

            width:
                Requested image width.

            height:
                Requested image height.

        Returns:
            GeneratedImage containing information about
            the generated image.
        """

        raise NotImplementedError