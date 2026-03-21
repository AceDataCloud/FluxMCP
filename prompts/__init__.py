"""Prompt templates for Flux MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def flux_image_generation_guide() -> str:
    """Guide for choosing the right Flux tool and model for image tasks."""
    return """# Flux Image Generation Guide

When the user wants to generate or edit images, choose the appropriate tool and model:

## Image Generation
**Tool:** `flux_generate_image`
**Use when:**
- User gives a description of what they want to create
- User wants to generate new images from scratch
- Text-to-image generation

**Model Selection:**
- Quick/draft: `flux-dev` (fastest, good quality)
- Production: `flux-pro-1.1` (better prompt following)
- Maximum quality: `flux-pro-1.1-ultra` (best quality, use aspect ratios)

**Example:** "Create a sunset over mountains"
→ Call `flux_generate_image` with prompt="Breathtaking sunset over mountain range, golden hour, dramatic clouds, landscape photography", model="flux-pro-1.1-ultra", size="16:9"

## Image Editing
**Tool:** `flux_edit_image`
**Use when:**
- User provides an image URL and wants modifications
- User wants to change elements, style, or composition
- Style transfer or artistic transformations

**Model Selection:**
- Standard editing: `flux-kontext-pro` (recommended for most edits)
- Complex editing: `flux-kontext-max` (for demanding transformations)

**Example:** "Add sunglasses to this person"
→ Call `flux_edit_image` with prompt="Add stylish sunglasses to the person", image_url="...", model="flux-kontext-pro"

## Task Checking
**Tool:** `flux_get_task` / `flux_get_tasks_batch`
**Use when:**
- Checking if a generation has completed
- Retrieving results from async generations
- Monitoring batch operations

## Important Notes:
1. For ultra/kontext models, use aspect ratios (e.g., "1:1", "16:9") not pixel dimensions
2. For dev/pro/pro-1.1 models, use pixel dimensions (e.g., "1024x1024")
3. Image URLs must be direct links to images, not web pages
4. Default model is flux-dev — suggest higher quality models for important tasks
5. Flux generation/editing is async in MCP — return the task_id first, then poll with `flux_get_task`
"""


@mcp.prompt()
def flux_prompt_writing_guide() -> str:
    """Best practices for writing effective Flux image generation prompts."""
    return """# Flux Prompt Writing Guide

## Prompt Structure
A good prompt includes these elements in order:
1. **Subject** — The main focus of the image
2. **Style/Medium** — Art style or photography type
3. **Details** — Lighting, mood, composition, colors
4. **Technical** — Quality modifiers

## Example Prompts by Category

**Photography:**
"Professional portrait of a young woman in a garden, natural lighting, shallow depth of field, 85mm lens, golden hour, photorealistic"

**Digital Art:**
"Futuristic cyberpunk cityscape at night, neon lights reflecting on wet streets, flying vehicles, highly detailed digital art, cinematic composition"

**Illustration:**
"Whimsical children's book illustration of a friendly dragon reading a book in a cozy library, watercolor style, warm colors, soft lighting"

**Product Photography:**
"Luxury watch on dark marble surface, dramatic studio lighting, reflection, commercial product photography, ultra sharp focus"

**Landscape:**
"Misty mountain valley at dawn, pine forests, lake reflection, atmospheric perspective, landscape photography, panoramic"

**Abstract:**
"Flowing liquid metal forms in iridescent colors, abstract 3D render, studio lighting, reflective surfaces, minimalist composition"

**Logo/Design:**
"Minimalist geometric logo of a soaring eagle, clean lines, flat design, professional, vector art style, white background"

## Tips for Best Results:
1. Be specific — "golden retriever puppy" not just "dog"
2. Describe lighting — "soft diffused light", "dramatic shadows", "backlit"
3. Mention art style — "oil painting", "3D render", "watercolor", "photorealistic"
4. Include composition — "close-up", "bird's eye view", "centered", "rule of thirds"
5. Add quality words — "highly detailed", "professional", "4K", "sharp focus"
6. For kontext models, describe changes clearly relative to the input image

## Model-Specific Tips:
- **flux-dev**: Good with simple, direct prompts
- **flux-pro-1.1**: Follows complex prompts more accurately
- **flux-pro-1.1-ultra**: Best with detailed, descriptive prompts
- **flux-kontext-pro/max**: Describe edits relative to the source image
"""


@mcp.prompt()
def flux_workflow_examples() -> str:
    """Common workflow examples for Flux image generation."""
    return """# Flux Workflow Examples

## Workflow 1: Quick Image Generation
1. User: "Create a cyberpunk city"
2. Call `flux_generate_image(prompt="Cyberpunk metropolis at night, neon signs, rain-slicked streets, towering skyscrapers, cinematic", model="flux-dev")`
3. Poll with `flux_get_task(task_id)` until the final image URLs are available

## Workflow 2: High Quality Generation
1. User: "I need a professional product photo"
2. Call `flux_generate_image(prompt="Elegant perfume bottle on black velvet, studio lighting, reflections, commercial photography, ultra detailed", model="flux-pro-1.1-ultra", size="4:5")`
3. Poll with `flux_get_task(task_id)` for the final image

## Workflow 3: Image Editing
1. User provides an image URL and says "Change the background to a beach"
2. Call `flux_edit_image(prompt="Change the background to a tropical beach with turquoise water and palm trees, keep the subject unchanged", image_url="...", model="flux-kontext-pro")`
3. Poll with `flux_get_task(task_id)` for the final edited image

## Workflow 4: Style Transfer
1. User provides a photo and says "Make it look like a Van Gogh painting"
2. Call `flux_edit_image(prompt="Transform into Van Gogh oil painting style with swirling brushstrokes and vibrant colors", image_url="...", model="flux-kontext-max")`
3. Return stylized image

## Workflow 5: Multiple Images
1. User wants several variations
2. Call `flux_generate_image(prompt="...", count=4, model="flux-dev")` for quick variations
3. Return all generated images

## Workflow 6: Async Generation with Polling
1. Generate: `flux_generate_image(prompt="...")` → get task_id
2. If generation hasn't completed, poll: `flux_get_task(task_id)`
3. Return result when ready

## Workflow 7: Batch Status Check
1. User has multiple pending generations
2. Call `flux_get_tasks_batch(task_ids=["id1", "id2", "id3"])`
3. Report status of all tasks
"""
