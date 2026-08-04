from app.ai.state.documentary_state import DocumentaryState
from app.image_generation.services import ImageGenerationService


class ImageGenerationNode:
    """
    LangGraph node responsible for converting
    documentary image prompts into generated images.
    """

    def __init__(
        self,
        service: ImageGenerationService | None = None,
    ):
        self.service = (
            service
            or ImageGenerationService()
        )

    def __call__(
        self,
        state: DocumentaryState,
    ) -> dict:
        image_prompts = state.get(
            "image_prompts",
            [],
        )

        if not image_prompts:
            return {
                "images": [],
            }

        generated_images = (
            self.service.generate_images(
                image_prompts=image_prompts,
            )
        )

        image_paths = [
            image.path
            for image in generated_images
        ]

        return {
            "images": image_paths,
        }