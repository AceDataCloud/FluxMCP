"""Type definitions for Flux MCP server."""

from typing import Literal

# Flux image generation actions
FluxAction = Literal["generate", "edit"]

# Flux task actions
TaskAction = Literal["retrieve", "retrieve_batch"]

# Flux supported models
FluxModel = Literal[
    "flux-dev",
    "flux-pro",
    "flux-kontext-pro",
    "flux-kontext-max",
    "flux-2-flex",
    "flux-2-pro",
    "flux-2-max",
]

# Flux supported aspect ratios (for ultra/kontext models)
FluxAspectRatio = Literal[
    "1:1",
    "16:9",
    "21:9",
    "3:2",
    "2:3",
    "4:5",
    "5:4",
    "3:4",
    "4:3",
    "9:16",
    "9:21",
]

# Default model
DEFAULT_MODEL: FluxModel = "flux-dev"
