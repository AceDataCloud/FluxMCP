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
