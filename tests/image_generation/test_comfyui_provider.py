from unittest.mock import patch

import subprocess
import pytest

from app.image_generation.exceptions import ImageProviderError
from app.image_generation.providers.comfyui import (
    ComfyUIImageProvider,
)

from app.image_generation.providers import (
    ImageProviderFactory,
)

from app.image_generation.exceptions import (
    ImageProviderError,
)


def test_build_command():
    provider = ComfyUIImageProvider()

    command = provider._build_command(
        prompt="ancient Indian palace",
        negative_prompt="blurry, watermark",
        width=768,
        height=432,
    )

    assert command[0] == "comfy"
    assert command[1] == "run"

    assert "--prompt" in command

    assert "checkpoint=dreamshaper_8.safetensors" in command
    assert "negative=blurry, watermark" in command
    assert "width=768" in command
    assert "height=432" in command
    assert "--json" in command


def test_extract_output_path():
    stdout = """
{"schema":"event/1","type":"output","url":"D:\\\\AI Generater\\\\ComfyUI\\\\output\\\\ComfyUI_00009_.png"}
{"schema":"envelope/1","type":"envelope","ok":true,"data":{"outputs":["D:\\\\AI Generater\\\\ComfyUI\\\\output\\\\ComfyUI_00009_.png"]}}
"""

    path = ComfyUIImageProvider._extract_output_path(
        stdout
    )

    assert str(path) == (
        "D:\\AI Generater\\ComfyUI\\output\\"
        "ComfyUI_00009_.png"
    )

def test_extract_output_path_prefers_envelope():
    stdout = """
{"schema":"event/1","type":"output","url":"old.png"}
{"schema":"envelope/1","type":"envelope","ok":true,"data":{"outputs":["D:\\\\ComfyUI\\\\output\\\\final.png"]}}
"""

    path = ComfyUIImageProvider._extract_output_path(
        stdout
    )

    assert str(path) == (
        "D:\\ComfyUI\\output\\final.png"
    )


def test_missing_output_raises_error():
    stdout = "Workflow execution completed"

    with pytest.raises(
        ImageProviderError,
        match="no image output",
    ):
        ComfyUIImageProvider._extract_output_path(
            stdout
        )


@patch(
    "app.image_generation.providers.comfyui.subprocess.run"
)
def test_generate(mock_run):
    mock_run.return_value.stdout = """
{"schema":"event/1","type":"output","url":"D:\\\\AI Generater\\\\ComfyUI\\\\output\\\\ComfyUI_00010_.png"}
{"schema":"envelope/1","type":"envelope","ok":true,"data":{"outputs":["D:\\\\AI Generater\\\\ComfyUI\\\\output\\\\ComfyUI_00010_.png"]}}
"""

    provider = ComfyUIImageProvider()

    result = provider.generate(
        prompt="historical palace",
        negative_prompt="blurry",
        width=768,
        height=432,
    )

    assert result.width == 768
    assert result.height == 432
    assert result.format == "png"
    assert result.provider == "local"

    assert result.path == (
        "D:\\AI Generater\\ComfyUI\\output\\"
        "ComfyUI_00010_.png"
    )

    mock_run.assert_called_once()


def test_factory_creates_comfyui_provider():
    provider = ImageProviderFactory.create(
        "local"
    )

    assert isinstance(
        provider,
        ComfyUIImageProvider,
    )


@patch(
    "app.image_generation.providers.comfyui.subprocess.run"
)
def test_generate_timeout(mock_run):
    mock_run.side_effect = (
        subprocess.TimeoutExpired(
            cmd=["comfy", "run"],
            timeout=180,
        )
    )

    provider = ComfyUIImageProvider()

    with pytest.raises(
        ImageProviderError,
        match="timed out",
    ):
        provider.generate(
            prompt="historical palace",
            negative_prompt="blurry",
            width=768,
            height=432,
        )



@patch(
    "app.image_generation.providers.comfyui.subprocess.run"
)
def test_generate_cli_failure(mock_run):
    mock_run.side_effect = (
        subprocess.CalledProcessError(
            returncode=1,
            cmd=["comfy", "run"],
            stderr="ComfyUI server unavailable",
        )
    )

    provider = ComfyUIImageProvider()

    with pytest.raises(
        ImageProviderError,
        match="server unavailable",
    ):
        provider.generate(
            prompt="historical palace",
            negative_prompt="blurry",
            width=768,
            height=432,
        )