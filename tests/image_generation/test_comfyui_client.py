from unittest.mock import MagicMock

from app.image_generation.providers.comfyui import (
    ComfyUIClient,
)


def test_comfyui_health_check():
    client = MagicMock()

    response = MagicMock()
    client.get.return_value = response

    comfy = ComfyUIClient(
        client=client
    )

    result = comfy.health_check()

    assert result is True

    client.get.assert_called_once()


def test_queue_workflow():
    client = MagicMock()

    response = MagicMock()

    response.json.return_value = {
        "prompt_id": "test-prompt-id"
    }

    client.post.return_value = response

    comfy = ComfyUIClient(
        client=client
    )

    workflow = {
        "1": {
            "class_type": "TestNode"
        }
    }

    prompt_id = comfy.queue_workflow(
        workflow
    )

    assert prompt_id == "test-prompt-id"

    client.post.assert_called_once()