# Flux MCP — JetBrains Plugin

AI Image Generation with [Flux](https://blackforestlabs.ai) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Flux server with JetBrains AI Assistant.
Once configured, AI Assistant can generate and edit images with flux models
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**6 AI Tools** — Generate and edit images with Flux models.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.flux)
2. Open **Settings → Tools → Flux MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "flux": {
      "command": "uvx",
      "args": ["mcp-flux-pro"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `flux.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "flux": {
      "url": "https://flux.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

## Links

- [Ace Data Cloud Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
- [PyPI Package](https://pypi.org/project/mcp-flux-pro/)
- [Source Code](https://github.com/AceDataCloud/FluxMCP)

## License

MIT
