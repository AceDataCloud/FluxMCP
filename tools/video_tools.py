"""Video generation, editing and upscaling via the public FLUX API."""

import json

from core.client import client
from core.server import mcp
from core.video_types import FluxVideoRequest, VideoEditRequest, VideoUpscaleRequest


@mcp.tool()
async def flux_generate_video(request: FluxVideoRequest) -> str:
    """Generate text/image/video-to-video or enhance an owned temporary draft. Poll flux_get_task."""
    result = await client.request(
        "/flux/videos", request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def flux_edit_video(request: VideoEditRequest) -> str:
    """Edit an existing video using a prompt. Poll flux_get_task for final delivery."""
    result = await client.request(
        "/flux/videos", request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def flux_upscale_video(request: VideoUpscaleRequest) -> str:
    """Upscale a video. Price depends on actual output MP-seconds and frame rate. Poll flux_get_task."""
    result = await client.request(
        "/flux/videos", request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    return json.dumps(result, ensure_ascii=False, indent=2)
