import copy
import json
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx

from app.animation.models import GeneratedVideo
from app.animation.providers.base import AnimationProvider


class ComfyUIAnimationProvider(AnimationProvider):
    """
    Local image-to-video provider backed by ComfyUI
    and the Wan 2.1 Fun Camera workflow.
    """

    INPUT_NODE = "52"
    POSITIVE_PROMPT_NODE = "6"
    NEGATIVE_PROMPT_NODE = "7"
    CAMERA_NODE = "57"
    VIDEO_NODE = "58"
    OUTPUT_NODE = "59"

    def __init__(
        self,
        workflow_path: str | Path,
        base_url: str = "http://127.0.0.1:8188",
        timeout: float = 600.0,
        poll_interval: float = 1.0,
    ):
        self.workflow_path = Path(workflow_path)
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.poll_interval = poll_interval

        self._workflow = self._load_workflow()

    def generate(
        self,
        image_path: str,
        prompt: str,
        negative_prompt: str = "",
        camera_motion: str = "Zoom In",
        width: int = 512,
        height: int = 512,
        frame_count: int = 33,
        fps: int = 16,
    ) -> GeneratedVideo:
        """
        Generate a video from an image using ComfyUI.
        """

        image_path_obj = Path(image_path)

        if not image_path_obj.is_file():
            raise FileNotFoundError(
                f"Input image not found: {image_path}"
            )

        uploaded_name = self._upload_image(
            image_path_obj
        )

        workflow = self._prepare_workflow(
            image_name=uploaded_name,
            prompt=prompt,
            negative_prompt=negative_prompt,
            camera_motion=camera_motion,
            width=width,
            height=height,
            frame_count=frame_count,
            fps=fps,
        )

        prompt_id = self._queue_prompt(
            workflow
        )

        output = self._wait_for_output(
            prompt_id
        )

        video_path = self._download_video(
            output=output,
            prompt_id=prompt_id,
        )

        return GeneratedVideo(
            path=str(video_path),
            width=width,
            height=height,
            fps=fps,
            frame_count=frame_count,
            provider="comfyui",
        )

    def _load_workflow(
        self,
    ) -> dict[str, Any]:
        if not self.workflow_path.is_file():
            raise FileNotFoundError(
                f"Workflow not found: "
                f"{self.workflow_path}"
            )

        with self.workflow_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def _workflow_copy(
        self,
    ) -> dict[str, Any]:
        return copy.deepcopy(
            self._workflow
        )

    @staticmethod
    def _create_client_id() -> str:
        return str(uuid4())

    def _prepare_workflow(
        self,
        image_name: str,
        prompt: str,
        negative_prompt: str,
        camera_motion: str,
        width: int,
        height: int,
        frame_count: int,
        fps: int,
    ) -> dict[str, Any]:
        workflow = self._workflow_copy()

        workflow[
            self.INPUT_NODE
        ]["inputs"]["image"] = image_name

        workflow[
            self.POSITIVE_PROMPT_NODE
        ]["inputs"]["text"] = prompt

        workflow[
            self.NEGATIVE_PROMPT_NODE
        ]["inputs"]["text"] = negative_prompt

        camera_inputs = workflow[
            self.CAMERA_NODE
        ]["inputs"]

        camera_inputs["camera_pose"] = camera_motion
        camera_inputs["width"] = width
        camera_inputs["height"] = height
        camera_inputs["length"] = frame_count

        camera_inputs["width"] = width
        camera_inputs["height"] = height
        camera_inputs["length"] = frame_count

        workflow[
            self.VIDEO_NODE
        ]["inputs"]["fps"] = fps

        return workflow

    def _upload_image(
        self,
        image_path: Path,
    ) -> str:
        with image_path.open("rb") as image_file:
            response = httpx.post(
                f"{self.base_url}/upload/image",
                files={
                    "image": (
                        image_path.name,
                        image_file,
                    )
                },
                data={
                    "type": "input",
                    "overwrite": "true",
                },
                timeout=60.0,
            )

        response.raise_for_status()

        data = response.json()

        name = data["name"]
        subfolder = data.get(
            "subfolder",
            "",
        )

        if subfolder:
            return (
                f"{subfolder}/{name}"
            )

        return name

    def _queue_prompt(
        self,
        workflow: dict[str, Any],
    ) -> str:
        response = httpx.post(
            f"{self.base_url}/prompt",
            json={
                "prompt": workflow,
                "client_id": (
                    self._create_client_id()
                ),
            },
            timeout=60.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["prompt_id"]

    def _wait_for_output(
        self,
        prompt_id: str,
    ) -> dict[str, Any]:
        deadline = (
            time.monotonic()
            + self.timeout
        )

        while time.monotonic() < deadline:
            response = httpx.get(
                (
                    f"{self.base_url}"
                    f"/history/{prompt_id}"
                ),
                timeout=30.0,
            )

            response.raise_for_status()

            history = response.json()

            if prompt_id in history:
                result = history[prompt_id]

                status = result.get(
                    "status",
                    {},
                )

                if status.get(
                    "status_str"
                ) == "error":
                    raise RuntimeError(
                        "ComfyUI animation "
                        "generation failed."
                    )

                outputs = result.get(
                    "outputs",
                    {},
                )

                if self.OUTPUT_NODE in outputs:
                    return outputs[
                        self.OUTPUT_NODE
                    ]

            time.sleep(
                self.poll_interval
            )

        raise TimeoutError(
            "Timed out waiting for "
            "ComfyUI animation."
        )

    def _download_video(
        self,
        output: dict[str, Any],
        prompt_id: str,
    ) -> Path:
        """
        Download the generated video returned by ComfyUI.

        ComfyUI SaveVideo may expose video files under
        the "images" output key.
        """

        files = (
            output.get("videos")
            or output.get("images")
            or []
        )

        if not files:
            raise RuntimeError(
                "ComfyUI returned no video output."
            )

        video = next(
            (
                item
                for item in files
                if Path(
                    item.get("filename", "")
                ).suffix.lower()
                in {
                    ".mp4",
                    ".webm",
                    ".mov",
                    ".mkv",
                }
            ),
            None,
        )

        if video is None:
            raise RuntimeError(
                "ComfyUI output did not contain "
                "a supported video file."
            )

        filename = video["filename"]

        subfolder = video.get(
            "subfolder",
            "",
        )

        output_type = video.get(
            "type",
            "output",
        )

        response = httpx.get(
            f"{self.base_url}/view",
            params={
                "filename": filename,
                "subfolder": subfolder,
                "type": output_type,
            },
            timeout=120.0,
        )

        response.raise_for_status()

        output_directory = Path(
            "outputs/animation"
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        suffix = (
            Path(filename).suffix
            or ".mp4"
        )

        destination = (
            output_directory
            / f"{prompt_id}{suffix}"
        )

        destination.write_bytes(
            response.content
        )

        return destination