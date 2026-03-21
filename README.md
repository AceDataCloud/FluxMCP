# MCP Flux

<!-- mcp-name: io.github.AceDataCloud/mcp-flux-pro -->

[![PyPI version](https://badge.fury.io/py/mcp-flux-pro.svg)](https://pypi.org/project/mcp-flux-pro/)
[![CI](https://github.com/AceDataCloud/MCPFlux/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/MCPFlux/actions/workflows/ci.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for AI image generation and editing using [Flux](https://platform.acedata.cloud) through the [AceDataCloud](https://platform.acedata.cloud) platform.

Generate and edit stunning AI images with Flux models (flux-dev, flux-pro, flux-kontext) directly from Claude, Cursor, or any MCP-compatible client.

## Features

- 🎨 **Image Generation** — Generate images from text prompts with 6 Flux models
- ✏️ **Image Editing** — Edit existing images with context-aware Flux Kontext models
- 🔄 **Task Management** — Track async generation tasks and batch status queries
- 📋 **Model Guide** — Built-in model selection and prompt writing guidance
- 🌐 **Dual Transport** — stdio (local) and HTTP (remote/cloud) modes
- 🐳 **Docker Ready** — Containerized with K8s deployment manifests
- 🔒 **Secure** — Bearer token auth with per-request isolation in HTTP mode

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Go to the [API documentation page](https://platform.acedata.cloud)
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Use the Hosted Server (Recommended)

AceDataCloud hosts a managed MCP server — **no local installation required**.

**Endpoint:** `https://flux.mcp.acedata.cloud/mc`

All requests require a Bearer token. Use the API token from Step 1.

#### Claude.ai

Connect directly on [Claude.ai](https://claude.ai) with OAuth — **no API token needed**:

1. Go to Claude.ai **Settings → Integrations → Add More**
2. Enter the server URL: `https://flux.mcp.acedata.cloud/mc`
3. Complete the OAuth login flow
4. Start using the tools in your conversation

#### Claude Desktop

Add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "flux": {
      "type": "streamable-http",
      "url": "https://flux.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Cursor / Windsurf

Add to your MCP config (`.cursor/mcp.json` or `.windsurf/mcp.json`):

```json
{
  "mcpServers": {
    "flux": {
      "type": "streamable-http",
      "url": "https://flux.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### VS Code (Copilot)

Add to your VS Code MCP config (`.vscode/mcp.json`):

```json
{
  "servers": {
    "flux": {
      "type": "streamable-http",
      "url": "https://flux.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

Or install the [Ace Data Cloud MCP extension](https://marketplace.visualstudio.com/items?itemName=acedatacloud.acedatacloud-mcp) for VS Code, which bundles all 11 MCP servers with one-click setup.

#### JetBrains IDEs

1. Go to **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**
2. Click **Add** → **HTTP**
3. Paste:

```json
{
  "mcpServers": {
    "flux": {
      "url": "https://flux.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### cURL Test

```bash
# Health check (no auth required)
curl https://flux.mcp.acedata.cloud/health

# MCP initialize
curl -X POST https://flux.mcp.acedata.cloud/mc \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 3. Or Run Locally (Alternative)

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-flux-pro
# or
uvx mcp-flux-pro

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-flux-pro

# Run (HTTP mode for remote access)
mcp-flux-pro --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "flux": {
      "command": "uvx",
      "args": ["mcp-flux-pro"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-flux-pro:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-flux-pro:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header.

## Cursor Integration

Add to your Cursor MCP configuration (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "flux": {
      "command": "mcp-flux-pro",
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## JetBrains IDEs

Install the [Flux MCP plugin](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.flux) from the JetBrains Marketplace, or configure manually:

1. Go to **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**
2. Click **Add** and select **HTTP**
3. Paste this configuration:

```json
{
  "mcpServers": {
    "flux": {
      "url": "https://flux.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer your_api_token_here"
      }
    }
  }
}
```

## Remote HTTP Mode

For cloud deployment or shared servers:

```bash
mcp-flux-pro --transport http --port 8000
```

Connect from clients using the HTTP endpoint:

```json
{
  "mcpServers": {
    "flux": {
      "url": "https://flux.mcp.acedata.cloud/mc",
      "headers": {
        "Authorization": "Bearer your_api_token_here"
      }
    }
  }
}
```

## Docker

```bash
# Build
docker build -t mcp-flux .

# Run
docker run -p 8000:8000 mcp-flux
```

Or using Docker Compose:

```bash
docker compose up --build
```

## Available Tools

| Tool                   | Description                                            |
| ---------------------- | ------------------------------------------------------ |
| `flux_generate_image`  | Generate images from text prompts with model selection |
| `flux_edit_image`      | Edit existing images with text instructions            |
| `flux_get_task`        | Query status of a single generation task               |
| `flux_get_tasks_batch` | Query multiple task statuses at once                   |
| `flux_list_models`     | List all available Flux models and capabilities        |
| `flux_list_actions`    | Show all tools and workflow examples                   |

## Available Prompts

| Prompt                        | Description                                  |
| ----------------------------- | -------------------------------------------- |
| `flux_image_generation_guide` | Guide for choosing the right tool and model  |
| `flux_prompt_writing_guide`   | Best practices for writing effective prompts |
| `flux_workflow_examples`      | Common workflow patterns and examples        |

## Supported Models

| Model                | Quality | Speed  | Size Format         | Best For                |
| -------------------- | ------- | ------ | ------------------- | ----------------------- |
| `flux-dev`           | Good    | Fast   | Pixels (256-1440px) | Quick prototyping       |
| `flux-pro`           | High    | Medium | Pixels (256-1440px) | Production use          |
| `flux-pro-1.1`       | High    | Medium | Pixels (256-1440px) | Better prompt following |
| `flux-pro-1.1-ultra` | Highest | Slower | Aspect ratios       | Maximum quality         |
| `flux-kontext-pro`   | High    | Medium | Aspect ratios       | Image editing           |
| `flux-kontext-max`   | Highest | Slower | Aspect ratios       | Complex editing         |

## Usage Examples

### Generate an Image

```
"Generate a photorealistic mountain landscape at golden hour"
→ flux_generate_image(prompt="...", model="flux-pro-1.1-ultra", size="16:9")
```

### Edit an Image

```
"Add sunglasses to the person in this photo"
→ flux_edit_image(prompt="Add sunglasses", image_url="https://...", model="flux-kontext-pro")
```

### Check Task Status

```
"What's the status of my generation?"
→ flux_get_task(task_id="...")
```

## Environment Variables

| Variable                    | Required    | Default                     | Description                 |
| --------------------------- | ----------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | Yes (stdio) | —                           | API token from AceDataCloud |
| `ACEDATACLOUD_API_BASE_URL` | No          | `https://api.acedata.cloud` | API base URL                |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `FLUX_REQUEST_TIMEOUT`      | No          | `1800`                      | Request timeout in seconds  |
| `MCP_SERVER_NAME`           | No          | `flux`                      | MCP server name             |
| `LOG_LEVEL`                 | No          | `INFO`                      | Logging level               |

## Development

### Setup

```bash
git clone https://github.com/AceDataCloud/MCPFlux.git
cd MCPFlux
pip install -e ".[all]"
cp .env.example .env
# Edit .env with your API token
```

### Lint & Format

```bash
ruff check .
ruff format .
mypy core tools main.py
```

### Test

```bash
# Unit tests
pytest --cov=core --cov=tools

# Skip integration tests
pytest -m "not integration"

# With coverage report
pytest --cov=core --cov=tools --cov-report=html
```

### Git Hooks

```bash
git config core.hooksPath .githooks
```

## API Reference

This MCP server uses the [AceDataCloud Flux API](https://platform.acedata.cloud):

- **POST /flux/images** — Generate or edit images
- **POST /flux/tasks** — Query task status (single or batch)

Full API documentation: [platform.acedata.cloud](https://platform.acedata.cloud)

## License

MIT License — see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Flux by Black Forest Labs](https://blackforestlabs.ai/)
- [PyPI Package](https://pypi.org/project/mcp-flux-pro/)
