from typing import Any

import httpx

from app.image_generation.config.settings import image_settings
from app.image_generation.exceptions import ImageProviderError


class ComfyUIClient:
    """
    Thin adapter around the ComfyUI server API.

    Image generation itself is handled entirely by ComfyUI.
    """

    def __init__(
        self,
        base_url: str | None = None,
        client: httpx.Client | None = None,
    ):
        self.base_url = (
            base_url
            or image_settings.comfyui_base_url
        ).rstrip("/")

        self.client = client or httpx.Client(
            timeout=image_settings.image_timeout
        )

    def health_check(self) -> bool:
        try:
            response = self.client.get(
                f"{self.base_url}/system_stats"
            )

            response.raise_for_status()

            return True

        except httpx.HTTPError:
            return False

    def queue_workflow(
        self,
        workflow: dict[str, Any],
    ) -> str:
        try:
            response = self.client.post(
                f"{self.base_url}/prompt",
                json={
                    "prompt": workflow,
                },
            )

            response.raise_for_status()

            data = response.json()

            prompt_id = data.get("prompt_id")

            if not prompt_id:
                raise ImageProviderError(
                    "ComfyUI did not return prompt_id."
                )

            return prompt_id

        except httpx.HTTPError as exc:
            raise ImageProviderError(
                f"Failed to communicate with ComfyUI: {exc}"
            ) from exc