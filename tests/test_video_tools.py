import json
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import TypeAdapter, ValidationError

from core.video_types import FluxVideoRequest
from tools.video_tools import flux_generate_video


@pytest.mark.parametrize(
    "body",
    [
        {
            "mode": "t2v",
            "model": "flux-3",
            "prompt": "ocean",
            "generate_audio": False,
            "draft": False,
            "async": False,
        },
        {
            "mode": "i2v",
            "prompt": "ocean",
            "keyframes": [[0, "https://example.com/a.png"], [2, "https://example.com/b.png"]],
        },
        {
            "mode": "v2v",
            "prompt": "ocean",
            "start_video": "https://example.com/v.mp4",
            "duration": 15,
        },
        {"mode": "draft_enhance", "draft_task_id": "owned-platform-id"},
    ],
)
async def test_video_modes_preserve_contract(body):
    request = TypeAdapter(FluxVideoRequest).validate_python(body)
    with patch(
        "tools.video_tools.client.request", new=AsyncMock(return_value={"task_id": "platform"})
    ) as call:
        assert json.loads(await flux_generate_video(request))["task_id"] == "platform"
    path, payload = call.await_args.args
    assert path == "/flux/videos"
    assert payload["action"] == "generate"
    for key, value in body.items():
        assert payload[key] == value
    assert "cache_reference" not in payload


@pytest.mark.parametrize(
    "body",
    [
        {"mode": "draft_enhance", "cache_reference": "secret"},
        {"action": "edit", "mode": "t2v", "prompt": "x", "video": "v"},
        {"action": "upscale", "mode": "t2v", "prompt": "x", "input_video": "v"},
        {"mode": "v2v", "prompt": "x", "start_video": "x", "duration": 20},
    ],
)
def test_unusable_requests_are_rejected(body):
    with pytest.raises(ValidationError):
        TypeAdapter(FluxVideoRequest).validate_python(body)


async def test_public_video_tools_only_offer_generation():
    import tools  # noqa: F401 - register the public tools
    from core.server import mcp

    names = {tool.name for tool in await mcp.list_tools()}
    assert "flux_generate_video" in names
    assert "flux_edit_video" not in names
    assert "flux_upscale_video" not in names
