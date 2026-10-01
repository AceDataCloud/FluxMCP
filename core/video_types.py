"""FLUX video request types from the public PlatformBackend contract."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class VideoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    async_: bool = Field(default=True, alias="async")
    callback_url: str | None = None
    safety_tolerance: int = Field(default=2, ge=0, le=4)


class GenerationRequest(VideoRequest):
    action: Literal["generate"] = "generate"
    model: Literal["flux-3"] = "flux-3"
    prompt: str = Field(min_length=1, max_length=4096)
    duration: Annotated[int, Field(ge=5, le=20)] | Literal["auto"] = "auto"
    resolution: Literal["hd", "fhd", "qhd", "uhd"] = "hd"
    aspect_ratio: Literal["21:9", "2:1", "16:9", "4:3", "1:1", "3:4", "9:16", "9:21", "auto"] = (
        "auto"
    )
    generate_audio: bool = True
    draft: bool = False
    version: Literal["latest"] = "latest"


class TextVideoRequest(GenerationRequest):
    mode: Literal["t2v"] = "t2v"


class ImageVideoRequest(GenerationRequest):
    mode: Literal["i2v"] = "i2v"
    keyframes: str | tuple[float, str] | list[str] | list[tuple[float, str]]


class VideoVideoRequest(GenerationRequest):
    mode: Literal["v2v"] = "v2v"
    start_video: str
    duration: Annotated[int, Field(ge=5, le=15)] | Literal["auto"] = "auto"


class DraftEnhanceRequest(VideoRequest):
    action: Literal["generate"] = "generate"
    model: Literal["flux-3"] = "flux-3"
    mode: Literal["draft_enhance"] = "draft_enhance"
    draft_task_id: str = Field(
        min_length=1,
        description="An owned platform draft task ID; draft availability is temporary.",
    )
    resolution: Literal["hd", "fhd", "qhd", "uhd"] = "fhd"


class VideoEditRequest(VideoRequest):
    action: Literal["edit"] = "edit"
    video: str
    prompt: str = Field(min_length=1, max_length=4096)


class VideoUpscaleRequest(VideoRequest):
    action: Literal["upscale"] = "upscale"
    input_video: str
    prompt: str = ""
    upscale_factor: float = Field(default=2, ge=1.5, le=3)
    creativity: Literal[0, 1] = 1


FluxVideoRequest = Annotated[
    TextVideoRequest | ImageVideoRequest | VideoVideoRequest | DraftEnhanceRequest,
    Field(discriminator="mode"),
]
