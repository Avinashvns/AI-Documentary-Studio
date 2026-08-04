from app.image_generation.models import GeneratedImage
from app.image_generation.providers.base import ImageProvider
from app.image_generation.providers.factory import ImageProviderFactory
from app.schemas.image_prompt import ImagePrompt


class ImageGenerationService:
    """
    Application service responsible for generating documentary images.

    It does not perform image inference itself.
    Actual generation is delegated to an ImageProvider.
    """

    def __init__(
        self,
        provider: ImageProvider | None = None,
    ):
        self.provider = (
            provider
            or ImageProviderFactory.create("local")
        )

    def generate_image(
        self,
        image_prompt: ImagePrompt,
        width: int = 768,
        height: int = 432,
    ) -> GeneratedImage:
        """
        Generate a single documentary scene image.
        """

        return self.provider.generate(
            prompt=image_prompt.prompt,
            negative_prompt=image_prompt.negative_prompt,
            width=width,
            height=height,
        )

    def generate_images(
        self,
        image_prompts: list[ImagePrompt],
        width: int = 768,
        height: int = 432,
    ) -> list[GeneratedImage]:
        """
        Generate images for multiple documentary scenes.
        """

        return [
            self.generate_image(
                image_prompt=image_prompt,
                width=width,
                height=height,
            )
            for image_prompt in image_prompts
        ]