import json

import pytest

from app.animation.providers.comfyui import (
    ComfyUIAnimationProvider,
)


def test_load_workflow(
    tmp_path,
):
    workflow_path = (
        tmp_path / "workflow.json"
    )

    workflow = {
        "1": {
            "class_type": "LoadImage",
            "inputs": {
                "image": "scene.png",
            },
        }
    }

    workflow_path.write_text(
        json.dumps(workflow),
        encoding="utf-8",
    )

    provider = ComfyUIAnimationProvider(
        workflow_path=workflow_path,
    )

    assert provider._workflow == workflow


def test_missing_workflow():
    with pytest.raises(
        FileNotFoundError
    ):
        ComfyUIAnimationProvider(
            workflow_path=(
                "missing_workflow.json"
            ),
        )


def test_workflow_copy_is_independent(
    tmp_path,
):
    workflow_path = (
        tmp_path / "workflow.json"
    )

    workflow = {
        "1": {
            "class_type": "LoadImage",
            "inputs": {
                "image": "scene.png",
            },
        }
    }

    workflow_path.write_text(
        json.dumps(workflow),
        encoding="utf-8",
    )

    provider = ComfyUIAnimationProvider(
        workflow_path=workflow_path,
    )

    copied = provider._workflow_copy()

    copied["1"]["inputs"]["image"] = (
        "changed.png"
    )

    assert (
        provider._workflow["1"]
        ["inputs"]["image"]
        == "scene.png"
    )


def test_create_client_id(
    tmp_path,
):
    workflow_path = (
        tmp_path / "workflow.json"
    )

    workflow_path.write_text(
        "{}",
        encoding="utf-8",
    )

    provider = ComfyUIAnimationProvider(
        workflow_path=workflow_path,
    )

    first = provider._create_client_id()
    second = provider._create_client_id()

    assert first
    assert second
    assert first != second


def test_prepare_workflow(
    tmp_path,
):
    workflow = {
        "6": {
            "inputs": {
                "text": "old positive",
            }
        },
        "7": {
            "inputs": {
                "text": "old negative",
            }
        },
        "52": {
            "inputs": {
                "image": "old.png",
            }
        },
        "57": {
            "inputs": {
                "width": 512,
                "height": 512,
                "length": 33,
            }
        },
        "58": {
            "inputs": {
                "fps": 16,
            }
        },
    }

    workflow_path = (
        tmp_path / "workflow.json"
    )

    workflow_path.write_text(
        json.dumps(workflow),
        encoding="utf-8",
    )

    provider = ComfyUIAnimationProvider(
        workflow_path=workflow_path,
    )

    prepared = provider._prepare_workflow(
        image_name="scene_002.png",
        prompt="slow cinematic zoom",
        negative_prompt="blurry",
        camera_motion="Pan Right",
        width=640,
        height=360,
        frame_count=49,
        fps=24,
    )

    assert (
        prepared["52"]["inputs"]["image"]
        == "scene_002.png"
    )

    assert (
        prepared["6"]["inputs"]["text"]
        == "slow cinematic zoom"
    )

    assert (
        prepared["7"]["inputs"]["text"]
        == "blurry"
    )

    assert (
        prepared["57"]["inputs"]["camera_pose"]
        == "Pan Right"
    )

    assert (
        prepared["57"]["inputs"]["width"]
        == 640
    )

    assert (
        prepared["57"]["inputs"]["height"]
        == 360
    )

    assert (
        prepared["57"]["inputs"]["length"]
        == 49
    )

    assert (
        prepared["58"]["inputs"]["fps"]
        == 24
    )