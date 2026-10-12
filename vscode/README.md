# Flux MCP

Flux image generation by Black Forest Labs — dev, pro, ultra, and kontext editing.

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-Marketplace-blue?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-flux) [![PyPI](https://img.shields.io/pypi/v/mcp-flux-pro.svg?label=PyPI)](https://pypi.org/project/mcp-flux-pro/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://flux.mcp.acedata.cloud/mcp)

Generate high-fidelity images with Flux from VS Code chat, or edit existing images via natural-language instructions using Flux Kontext.

This extension registers the **flux** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `flux` MCP server automatically.
2. **Get an application API key** using the detailed steps below. Check service access and your current balance before the first request.
3. **Open Copilot Chat** in agent mode and ask for a image task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Flux MCP: Set Ace Data Cloud API Key**
- **Flux MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://flux.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_mcp_vscode_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_mcp_vscode_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->

## VS Code Setup Guide

For screenshots, token setup, project-level and user-level `mcp.json`, and Copilot Agent Mode examples, see:

- [Flux MCP VS Code guide](https://platform.acedata.cloud/documents/promotion_article_mcp_flux_vscode?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_mcp_vscode_documents_promotion_article_mcp_flux_vscode)
- [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_mcp_vscode_documents_promotion_article_mcp_all_vscode)

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

`flux-dev`, `flux-pro`, `flux-2-flex`, `flux-2-pro`, `flux-2-max`, `flux-2-klein`, `flux-kontext-pro`, `flux-kontext-max`

## Pricing

From $0.025 per image. Free trial credit on sign-up. See full pricing at [https://platform.acedata.cloud/documents/flux-mcp](https://platform.acedata.cloud/documents/flux-mcp?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_mcp_vscode_quick_start).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.flux
Server label: Flux MCP
Server URL  : https://flux.mcp.acedata.cloud/mcp
Transport   : Streamable HTTP
Auth        : Bearer API key from VS Code SecretStorage (or $ACEDATACLOUD_API_TOKEN)
```

You don't need to edit `mcp.json` — the extension handles registration and
token handling automatically. If you'd rather configure things by hand, the
sections below show equivalent `mcp.json` snippets you can use **instead of**
this extension.

### Alternative: manual `mcp.json` (hosted)

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
      "description": "Ace Data Cloud API key",
      "password": true
    }
  ]
}
```

### Alternative: local stdio (no network roundtrip)

For offline dev, air-gapped environments, or pinning to a specific PyPI
version, install [`uv`](https://docs.astral.sh/uv/) and use:

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

---

## Links

- **Hosted endpoint:** https://flux.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-flux-pro`](https://pypi.org/project/mcp-flux-pro/)
- **Source repository:** https://github.com/AceDataCloud/FluxMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_mcp_vscode_platform
- **MCP documentation:** https://platform.acedata.cloud/documents/flux-mcp?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_mcp_vscode_quick_start

## License

MIT — see [LICENSE](LICENSE).
