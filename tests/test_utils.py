"""Unit tests for utility functions."""

import json

from core.utils import format_image_result, format_task_result


class TestFormatImageResult:
    """Tests for format_image_result function."""

    def test_format_success(self, mock_image_response):
        """Test formatting successful image response."""
        result = format_image_result(mock_image_response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"
        assert data["trace_id"] == "test-trace-456"
        assert len(data["data"]) == 1
        assert "image_url" in data["data"][0]
        assert data["mcp_async_submission"]["poll_tool"] == "flux_get_task"

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_image_result(mock_error_response)
        data = json.loads(result)
        assert data["success"] is False
        assert data["error"]["code"] == "invalid_request"

    def test_format_empty_data(self):
        """Test formatting response with no image data."""
        response = {"success": True, "task_id": "123", "data": []}
        result = format_image_result(response)
        data = json.loads(result)
        assert data["task_id"] == "123"
        assert data["data"] == []


class TestFormatTaskResult:
    """Tests for format_task_result function."""

    def test_format_success(self, mock_task_response):
        """Test formatting successful task response."""
        result = format_task_result(mock_task_response)
        data = json.loads(result)
        assert data["id"] == "task-123"
        assert data["request"]["action"] == "generate"
        assert data["response"]["success"] is True
        assert data["mcp_task_polling"]["poll_tool"] == "flux_get_task"

    def test_format_error(self):
        """Test formatting error response."""
        error_response = {"error": {"code": "not_found", "message": "Task not found"}}
        result = format_task_result(error_response)
        data = json.loads(result)
        assert data["error"]["code"] == "not_found"
