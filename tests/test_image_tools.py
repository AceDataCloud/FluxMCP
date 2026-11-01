"""Unit tests for Flux image tool payloads."""

import inspect
import json
from unittest.mock import AsyncMock, patch

import pytest

from tools.image_tools import flux_edit_image, flux_generate_image


def test_flux_generate_image_requires_size() -> None:
    signature = inspect.signature(flux_generate_image)

    assert signature.parameters["size"].default is inspect.Parameter.empty


def test_flux_edit_image_requires_size() -> None:
    signature = inspect.signature(flux_edit_image)

    assert signature.parameters["size"].default is inspect.Parameter.empty


@pytest.mark.asyncio
async def test_flux_generate_image_sends_required_size() -> None:
    response = {"success": True, "task_id": "task-123", "data": []}
    with patch(
        "tools.image_tools.client.generate_image", new=AsyncMock(return_value=response)
    ) as generate_image:
        result = await flux_generate_image(prompt="a cat", size="1024x1024")

    generate_image.assert_awaited_once_with(
        action="generate",
        prompt="a cat",
        model="flux-dev",
        size="1024x1024",
    )
    assert json.loads(result)["task_id"] == "task-123"


@pytest.mark.asyncio
async def test_flux_edit_image_sends_required_size() -> None:
    response = {"success": True, "task_id": "task-456", "data": []}
    with patch(
        "tools.image_tools.client.edit_image", new=AsyncMock(return_value=response)
    ) as edit_image:
        result = await flux_edit_image(
            prompt="add sunglasses",
            image_url="https://example.com/image.png",
            size="1:1",
        )

    edit_image.assert_awaited_once_with(
        action="edit",
        prompt="add sunglasses",
        image_url="https://example.com/image.png",
        model="flux-kontext-pro",
        size="1:1",
    )
    assert json.loads(result)["task_id"] == "task-456"


@pytest.mark.asyncio
async def test_generation_only_klein_cannot_be_selected_for_editing() -> None:
    from core.server import mcp

    tools = {tool.name: tool for tool in await mcp.list_tools()}
    assert "flux-2-klein" in tools["flux_generate_image"].inputSchema["properties"]["model"]["enum"]
    assert "flux-2-klein" not in tools["flux_edit_image"].inputSchema["properties"]["model"]["enum"]
    with (
        patch("tools.image_tools.client.edit_image", new=AsyncMock()) as edit,
        pytest.raises(Exception, match="model"),
    ):
        await mcp.call_tool(
            "flux_edit_image",
            {
                "prompt": "test",
                "image_url": "https://example.com/a.png",
                "model": "flux-2-klein",
                "size": "1:1",
            },
        )
    edit.assert_not_awaited()


@pytest.mark.asyncio
async def test_flux_2_guidance_and_examples_use_aspect_ratios() -> None:
    from core.server import mcp
    from tools.info_tools import flux_list_actions, flux_list_models

    tools = {tool.name: tool for tool in await mcp.list_tools()}
    description = tools["flux_generate_image"].inputSchema["properties"]["size"]["description"]
    assert "flux-2-flex/pro/max" in description
    assert "aspect ratios only" in description
    assert 'model="flux-2-max", size="1:1"' in await flux_list_actions()
    assert "pixel dims (x >= 64" not in await flux_list_models()


@pytest.mark.parametrize("model", ["flux-2-flex", "flux-2-pro", "flux-2-max", "flux-kontext-pro"])
async def test_ratio_only_models_reject_pixel_sizes_before_submission(model):
    with (
        patch("tools.image_tools.client.generate_image", new=AsyncMock()) as generate,
        pytest.raises(ValueError, match="requires a supported aspect ratio"),
    ):
        await flux_generate_image(prompt="test", model=model, size="1024x1024")
    generate.assert_not_awaited()
