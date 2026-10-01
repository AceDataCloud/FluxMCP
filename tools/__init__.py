"""Tools module for MCP Flux server."""

# Import all tools to register them with the MCP server
from tools import (
    image_tools,
    info_tools,
    task_tools,
    video_tools,
)

__all__ = [
    "image_tools",
    "video_tools",
    "task_tools",
    "info_tools",
]
