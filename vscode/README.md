# Flux MCP

Flux image generation by Black Forest Labs — dev, pro, ultra, and kontext editing.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-flux-pro?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-flux-pro) [![PyPI](https://img.shields.io/pypi/v/mcp-flux-pro.svg?label=PyPI)](https://pypi.org/project/mcp-flux-pro/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://flux.mcp.acedata.cloud/mcp)

Generate high-fidelity images with Flux from VS Code chat, or edit existing images via natural-language instructions using Flux Kontext.

This extension registers the **flux** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `flux` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a image task — VS Code will prompt for the token the first time and store it securely.

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://flux.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "Generate a hyperreal product shot of a matte-black ceramic mug, top-down. Use flux pro ultra."
- "Take https://example.com/cup.jpg and replace the background with a sunlit kitchen."

---

## Tool Reference

**6 tools** available via this server.

| Tool | Description |
| --- | --- |
| `flux_generate_image` | Generate AI images from a text prompt using Flux. |
| `flux_edit_image` | Edit an existing image using Flux with a text prompt. |
| `flux_list_models` | List all available Flux models and their capabilities. |
| `flux_list_actions` | List all available Flux tools and their use cases. |
| `flux_get_task` | Query the status and result of a Flux image generation task. |
| `flux_get_tasks_batch` | Query multiple Flux image generation tasks at once. |

## Supported Models

`flux-dev`, `flux-pro`, `flux-pro-1.1`, `flux-pro-1.1-ultra`, `flux-kontext-pro`, `flux-kontext-max`

## Pricing

From $0.025 per image. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension contributes the following entry to your VS Code MCP config:

```jsonc
{
  "servers": {
    "flux": {
      "type": "http",
      "url": "https://flux.mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer ${input:acedatacloud_api_token}" }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "acedatacloud_api_token",
      "description": "Ace Data Cloud API token",
      "password": true
    }
  ]
}
```

VS Code will prompt for the token on first use and persist it in the OS
secret store (Keychain / Credential Manager / libsecret).

### Alternative: local stdio (no network roundtrip)

If you prefer running the server locally — for offline dev, air-gapped
environments, or to pin to a specific PyPI version — install
[`uv`](https://docs.astral.sh/uv/) and replace your `mcp.json` entry with:

```jsonc
{
  "servers": {
    "flux": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-flux-pro"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-flux-pro`](https://pypi.org/project/mcp-flux-pro/) on demand.

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://flux.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-flux-pro`](https://pypi.org/project/mcp-flux-pro/)
- **Source repository:** https://github.com/AceDataCloud/FluxMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
