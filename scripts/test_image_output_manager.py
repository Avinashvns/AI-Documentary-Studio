from app.image_generation.services import (
    ImageGenerationService,
    ImageOutputManager,
)
from app.schemas.image_prompt import ImagePrompt


generation_service = ImageGenerationService()
output_manager = ImageOutputManager()

image_prompt = ImagePrompt(
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
)

generated = generation_service.generate_image(
    image_prompt
)

print("Generated:")
print(generated)

saved = output_manager.save_image(
    image=generated,
    topic="Mughal Empire",
    scene_number=image_prompt.scene_number,
)

print()
print("Organized:")
print(saved)