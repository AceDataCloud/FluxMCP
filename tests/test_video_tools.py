import json
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import TypeAdapter, ValidationError

from core.video_types import FluxVideoRequest, VideoEditRequest, VideoUpscaleRequest
from tools.video_tools import flux_edit_video, flux_generate_video, flux_upscale_video


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
        {"mode": "v2v", "prompt": "x", "start_video": "x", "duration": 20},
    ],
)
def test_unusable_requests_are_rejected(body):
    with pytest.raises(ValidationError):
        TypeAdapter(FluxVideoRequest).validate_python(body)


@pytest.mark.parametrize(
    "tool,payload_model,action",
    [
        (flux_edit_video, VideoEditRequest(video="v", prompt="edit"), "edit"),
        (
            flux_upscale_video,
            VideoUpscaleRequest(input_video="v", creativity=0),
            "upscale",
        ),
    ],
)
async def test_video_utilities_use_exact_routes(tool, payload_model, action):
    with patch(
        "tools.video_tools.client.request", new=AsyncMock(return_value={"task_id": "platform"})
    ) as call:
        await tool(payload_model)
    assert call.await_args.args[0] == "/flux/videos"
    assert call.await_args.args[1]["action"] == action


@pytest.mark.parametrize(
    "model,body",
    [
        (VideoEditRequest, {"action": "upscale", "video": "v", "prompt": "edit"}),
        (VideoEditRequest, {"video": "v", "prompt": "edit", "mode": "t2v"}),
        (VideoUpscaleRequest, {"action": "edit", "input_video": "v"}),
    ],
)
def test_video_tools_reject_mixed_actions(model, body):
    with pytest.raises(ValidationError):
        model.model_validate(body)
