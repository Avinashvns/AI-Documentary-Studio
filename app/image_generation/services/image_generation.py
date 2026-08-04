from app.image_generation.models import GeneratedImage
from app.image_generation.providers.base import ImageProvider
from app.image_generation.providers.factory import ImageProviderFactory
from app.image_generation.validation import ImageValidator
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
        validator: ImageValidator | None = None,
    ):
        self.provider = (
            provider
            or ImageProviderFactory.create("local")
        )

        self.validator = (
            validator
            or ImageValidator()
        )

    def generate_image(
        self,
        image_prompt: ImagePrompt,
        width: int = 768,
        height: int = 432,
    ) -> GeneratedImage:
        """
        Generate and validate a single documentary scene image.
        """

        generated_image = self.provider.generate(
            prompt=image_prompt.prompt,
            negative_prompt=image_prompt.negative_prompt,
            width=width,
            height=height,
        )

        validated_image = self.validator.validate(
            generated_image
        )

        return validated_image

    def generate_images(
        self,
        image_prompts: list[ImagePrompt],
        width: int = 768,
        height: int = 432,
    ) -> list[GeneratedImage]:
        """
        Generate and validate images for multiple
        documentary scenes.
        """

        return [
            self.generate_image(
                image_prompt=image_prompt,
                width=width,
                height=height,
            )
            for image_prompt in image_prompts
        ]