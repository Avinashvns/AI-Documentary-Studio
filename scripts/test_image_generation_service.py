from app.image_generation.services import (
    ImageGenerationService,
)
from app.schemas.image_prompt import ImagePrompt


service = ImageGenerationService()

prompts = [
    ImagePrompt(
        scene_number=1,
        prompt=(
            "cinematic historical documentary photograph "
            "of an ancient Indian palace, realistic architecture, "
            "dramatic natural lighting, photorealistic"
        ),
        negative_prompt=(
            "cartoon, anime, blurry, low quality, "
            "text, watermark"
        ),
    ),
    ImagePrompt(
        scene_number=2,
        prompt=(
            "cinematic historical documentary photograph "
            "of an ancient Indian battlefield at sunrise, "
            "realistic soldiers, dramatic atmosphere, "
            "photorealistic"
        ),
        negative_prompt=(
            "cartoon, anime, blurry, low quality, "
            "text, watermark"
        ),
    ),
]

images = service.generate_images(
    prompts
)

for image in images:
    print(image)