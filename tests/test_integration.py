"""
Integration tests for Flux MCP Server.

These tests make REAL API calls to verify all tools work correctly.
Run with: pytest tests/test_integration.py -v -s

Note: These tests require ACEDATACLOUD_API_TOKEN to be set.
They are skipped in CI environments without the token.
"""

import json
import os
import sys

import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Check if API token is configured
HAS_API_TOKEN = bool(os.getenv("ACEDATACLOUD_API_TOKEN"))

# Decorator to skip tests that require API token
requires_api_token = pytest.mark.skipif(
    not HAS_API_TOKEN,
    reason="ACEDATACLOUD_API_TOKEN not configured - skipping integration test",
)


class TestImageTools:
    """Integration tests for image generation tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_generate_image_basic(self) -> None:
        """Test basic image generation with real API."""
        from tools.image_tools import flux_generate_image

        result = await flux_generate_image(
            prompt="A simple red circle on a white background, minimalist",
            model="flux-dev",
        )

        print("\n=== Generate Image Result ===")
        print(result)

        assert "task_id" in result


class TestInfoTools:
    """Integration tests for informational tools."""

    @pytest.mark.asyncio
    async def test_list_models(self) -> None:
        """Test flux_list_models tool."""
        from tools.info_tools import flux_list_models

        result = await flux_list_models()

        print("\n=== List Models Result ===")
        print(result)

        assert "flux-dev" in result
        assert "flux-pro" in result
        assert "flux-2-klein" in result

    @pytest.mark.asyncio
    async def test_list_actions(self) -> None:
        """Test flux_list_actions tool."""
        from tools.info_tools import flux_list_actions

        result = await flux_list_actions()

        print("\n=== List Actions Result ===")
        print(result)

        assert "flux_generate_image" in result
        assert "flux_get_task" in result
        assert "Supports 8 models" in result


class TestTaskTools:
    """Integration tests for task query tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_get_task_with_real_id(self) -> None:
        """Test querying a task - first generate, then query."""
        from tools.image_tools import flux_generate_image
        from tools.task_tools import flux_get_task

        # Generate an image first
        gen_result = await flux_generate_image(
            prompt="A simple blue square, minimal",
            model="flux-dev",
        )

        print("\n=== Generate Result ===")
        print(gen_result)

        gen_data = json.loads(gen_result)
        task_id = gen_data.get("task_id")
        if task_id:
            # Query the task
            task_result = await flux_get_task(task_id=task_id)
            print("\n=== Task Result ===")
            print(task_result)
            assert task_id in task_result
