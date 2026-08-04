from app.image_generation.providers.comfyui import (
    ComfyUIImageProvider,
)


provider = ComfyUIImageProvider()

result = provider.generate(
    prompt=(
        "cinematic historical documentary photograph "
        "of an ancient Indian palace, realistic "
        "architecture, dramatic natural lighting, "
        "photorealistic"
    ),
    negative_prompt=(
        "cartoon, anime, blurry, low quality, "
        "text, watermark, logo"
    ),
    width=768,
    height=432,
)

print(result)