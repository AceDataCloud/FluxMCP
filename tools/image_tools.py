"""Image generation tools for Flux API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODEL, FluxModel
from core.utils import format_image_result


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
    model: Annotated[
        FluxModel,
        Field(
            description="Flux model to use for generation. Options:\n"
            "- flux-dev: Fast development model, good balance of speed and quality (default)\n"
            "- flux-pro: Higher quality production model\n"
            "- flux-2-flex: Flux 2 flexible model, pixel sizes (x >= 64, multiple of 32)\n"
            "- flux-2-pro: Flux 2 professional model, high quality\n"
            "- flux-2-max: Flux 2 maximum-quality model\n"
            "- flux-kontext-pro: Context-aware model for editing and style transfer\n"
            "- flux-kontext-max: Maximum context model for complex editing tasks"
        ),
    ] = DEFAULT_MODEL,
    size: Annotated[
        str | None,
        Field(
            description="Image size. For flux-dev: pixel dimensions like '1024x1024' "
            "(256-1440px, multiples of 32). For flux-2-flex/pro/max: pixel dimensions "
            "(x >= 64, multiples of 32). For kontext models: image ratios like '1:1', '16:9', "
            "'9:16', '4:3', '3:2', '2:3', '4:5', '5:4', '3:4', '21:9', '9:21'. Default varies by model."
        ),
    ] = None,
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
    payload: dict = {
        "action": "generate",
        "prompt": prompt,
        "model": model,
    }

    if size:
        payload["size"] = size
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
    model: Annotated[
        FluxModel,
        Field(
            description="Flux model to use for editing. Recommended models for editing:\n"
            "- flux-kontext-pro: Best for context-aware editing and style transfer (recommended)\n"
            "- flux-kontext-max: Maximum context for complex edits\n"
            "- flux-dev: Basic editing support\n"
            "Other models also support editing but kontext models give best results."
        ),
    ] = "flux-kontext-pro",
    size: Annotated[
        str | None,
        Field(
            description="Output image size. For kontext models: aspect ratios like '1:1', '16:9'. "
            "For other models: pixel dimensions like '1024x1024'."
        ),
    ] = None,
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
    payload: dict = {
        "action": "edit",
        "prompt": prompt,
        "image_url": image_url,
        "model": model,
    }

    if size:
        payload["size"] = size
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.edit_image(**payload)
    return format_image_result(result)
