from pydantic_settings import BaseSettings, SettingsConfigDict


class ImageGenerationSettings(BaseSettings):
    image_provider: str = "local"

    image_width: int = 1024
    image_height: int = 576

    image_format: str = "png"

    image_output_dir: str = "outputs/images"

    image_timeout: int = 300
    image_max_retries: int = 2

    comfyui_base_url: str = "http://127.0.0.1:8188"

    comfyui_workflow_path: str = (
        "app/image_generation/workflows/text_to_image.json"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


image_settings = ImageGenerationSettings()

