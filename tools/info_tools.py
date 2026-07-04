"""Informational tools for Flux API."""

from core.server import mcp


@mcp.tool()
async def flux_list_models() -> str:
    """List all available Flux models and their capabilities.

    Reference guide for choosing the right Flux model for your use case.

    Returns:
        Detailed list of all Flux models with descriptions and recommendations.
    """
    # Last updated: 2026-04-05
    return """Available Flux Models:

Image Generation Models:
━━━━━━━━━━━━━━━━━━━━━━━
- flux-dev
  Speed: Fast  |  Quality: Good  |  Size: 256-1440px (multiples of 32)
  Best for: Quick prototyping, development, testing
  Default model with good balance of speed and quality.

- flux-pro
  Speed: Medium  |  Quality: High  |  Size: 256-1440px (multiples of 32)
  Best for: Production use, higher quality requirements

- flux-2-flex
  Speed: Medium  |  Quality: High  |  Size: pixel dims (x >= 64, multiples of 32)
  Best for: Flexible Flux 2 generation with fine size control

- flux-2-pro
  Speed: Medium  |  Quality: Higher  |  Size: pixel dims (x >= 64, multiples of 32)
  Best for: Professional Flux 2 production output

- flux-2-max
  Speed: Slower  |  Quality: Highest  |  Size: pixel dims (x >= 64, multiples of 32)
  Best for: Maximum-quality Flux 2 output, final renders

Context-Aware Models (Best for Editing):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- flux-kontext-pro
  Speed: Medium  |  Quality: High  |  Size: Aspect ratios only
  Best for: Image editing, style transfer, context-aware modifications
  Recommended for most editing tasks.

- flux-kontext-max
  Speed: Slower  |  Quality: Highest  |  Size: Aspect ratios only
  Best for: Complex editing, maximum context understanding
  Use for demanding edit operations.

Size Guide:
━━━━━━━━━━━
Pixel dimensions (flux-dev, flux-2-flex/pro/max):
  Square: 1024x1024
  Landscape: 1344x768, 1280x720
  Portrait: 768x1344, 720x1280

Image ratios (kontext models):
  Square: 1:1
  Landscape: 16:9, 21:9, 4:3, 3:2, 5:4
  Portrait: 9:16, 9:21, 3:4, 2:3, 4:5

Recommendations:
━━━━━━━━━━━━━━━
- Quick generation → flux-dev
- High quality → flux-2-max
- Image editing → flux-kontext-pro
- Complex editing → flux-kontext-max
"""


@mcp.tool()
async def flux_list_actions() -> str:
    """List all available Flux tools and their use cases.

    Reference guide for what each tool does and when to use it.

    Returns:
        Categorized list of all tools with descriptions.
    """
    # Last updated: 2026-04-05
    return """Available Flux Tools:

Image Generation:
- flux_generate_image: Generate images from text prompts
  Supports 6 models with different quality/speed tradeoffs.

Image Editing:
- flux_edit_image: Edit existing images with text instructions
  Best with flux-kontext-pro or flux-kontext-max models.

Task Management:
- flux_get_task: Check status of a single generation task
- flux_get_tasks_batch: Check status of multiple tasks at once

Information:
- flux_list_models: Show all available models and capabilities
- flux_list_actions: Show this reference guide (you are here)

Workflows:
━━━━━━━━━━
1. Quick Generation:
   flux_generate_image(prompt="...") → get image_url

2. High Quality Generation:
   flux_generate_image(prompt="...", model="flux-2-max", size="1024x1024")

3. Image Editing:
   flux_edit_image(prompt="Change the sky to sunset", image_url="https://...")

4. Async Generation:
   flux_generate_image(prompt="...", callback_url="https://...") → get task_id
   flux_get_task(task_id) → check status later

5. Batch Monitoring:
   flux_get_tasks_batch(task_ids=["id1", "id2", "id3"])
"""
