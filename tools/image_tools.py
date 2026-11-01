"""Image generation tools for Flux API."""

from typing import Annotated, get_args

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODEL, FluxAspectRatio, FluxEditModel, FluxModel
from core.utils import format_image_result

_RATIO_ONLY_MODELS = {
    "flux-kontext-pro",
    "flux-kontext-max",
    "flux-2-flex",
    "flux-2-pro",
    "flux-2-max",
}


def _validate_size(model: str, size: str) -> None:
    if model in _RATIO_ONLY_MODELS and size not in get_args(FluxAspectRatio):
        raise ValueError(f"{model} requires a supported aspect ratio, such as 1:1 or 16:9")


@mcp.tool()
async def flux_generate_image(
    prompt: Annotated[
        str,
        Field(
            description="Description of the image to generate. Be descriptive about style, subject, "
            "lighting, and composition. Examples: 'A majestic mountain landscape at golden hour, "
            "photorealistic', 'Cyberpunk street scene with neon lights and rain, cinematic', "
            "'Minimalist logo design of a phoenix, vector art style'"
        ),
    ],
    size: Annotated[
        str,
        Field(
            description="Required image size. For flux-dev/pro/2-klein, use documented pixel presets "
            "such as '1024x1024' or aspect ratios. For flux-2-flex/pro/max and kontext models, "
            "use aspect ratios only: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, or 9:21."
        ),
    ],
    model: Annotated[
        FluxModel,
        Field(
            description="Flux model to use for generation. Options:\n"
            "- flux-dev: Fast development model, good balance of speed and quality (default)\n"
            "- flux-pro: Higher quality production model\n"
            "- flux-2-flex: Flux 2 flexible model, aspect-ratio sizes only\n"
            "- flux-2-pro: Flux 2 professional model, high quality\n"
            "- flux-2-max: Flux 2 maximum-quality model\n"
            "- flux-2-klein: Flux 2 klein model, efficient generation\n"
            "- flux-kontext-pro: Context-aware model for editing and style transfer\n"
            "- flux-kontext-max: Maximum context model for complex editing tasks"
        ),
    ] = DEFAULT_MODEL,
    count: Annotated[
        int | None,
        Field(
            description="Number of images to generate. Only supported for generate action. "
            "Default is 1."
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, "
            "the API will POST to this URL when the image is generated."
        ),
    ] = None,
) -> str:
    """Generate AI images from a text prompt using Flux.

    Flux is a family of fast, high-quality image generation models by Black Forest Labs.
    Different models offer different tradeoffs between speed, quality, and capabilities.

    Use this when:
    - You want to create new images from a text description
    - You need high-quality AI-generated artwork or photos
    - You want fast image generation with good prompt following

    For editing existing images, use flux_edit_image instead.

    Returns:
        Task ID and generated image information including URLs.
    """
    _validate_size(model, size)
    payload: dict = {
        "action": "generate",
        "prompt": prompt,
        "model": model,
        "size": size,
    }

    if count is not None:
        payload["count"] = count
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_image(**payload)
    return format_image_result(result)


@mcp.tool()
async def flux_edit_image(
    prompt: Annotated[
        str,
        Field(
            description="Description of how to edit the image. Be specific about what changes "
            "to make. Examples: 'Change the background to a sunset beach', 'Add sunglasses "
            "to the person', 'Make it look like a watercolor painting', 'Replace the car "
            "with a bicycle'"
        ),
    ],
    image_url: Annotated[
        str,
        Field(
            description="URL of the image to edit. Must be a direct image URL (JPEG, PNG, etc.), "
            "not a web page containing an image."
        ),
    ],
    size: Annotated[
        str,
        Field(
            description="Required output size. Kontext and flux-2-flex/pro/max require aspect "
            "ratios such as '1:1' or '16:9'; flux-dev/pro also accept documented pixel presets."
        ),
    ],
    model: Annotated[
        FluxEditModel,
        Field(
            description="Flux model to use for editing. Recommended models for editing:\n"
            "- flux-kontext-pro: Best for context-aware editing and style transfer (recommended)\n"
            "- flux-kontext-max: Maximum context for complex edits\n"
            "- flux-dev: Basic editing support\n"
            "flux-2-flex/pro/max also support editing. flux-2-klein supports generation only."
        ),
    ] = "flux-kontext-pro",
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Edit an existing image using Flux with a text prompt.

    This allows you to modify an existing image based on a text description.
    The kontext models (flux-kontext-pro, flux-kontext-max) are specifically
    designed for high-quality image editing and style transfer.

    Use this when:
    - You want to modify or transform an existing image
    - You want to change specific elements in an image
    - You want to apply style changes or artistic effects
    - You want to add, remove, or replace objects in an image

    For generating new images from scratch, use flux_generate_image instead.

    Returns:
        Task ID and edited image information including URLs.
    """
    _validate_size(model, size)
    payload: dict = {
        "action": "edit",
        "prompt": prompt,
        "image_url": image_url,
        "model": model,
        "size": size,
    }

    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.edit_image(**payload)
    return format_image_result(result)
