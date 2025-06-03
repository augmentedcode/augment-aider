---
parent: Connecting to LLMs
nav_order: 600
---

# MCP Servers

Aider can connect to Model Context Protocol (MCP) servers, which provide additional capabilities like file system access, GitHub integration, and more.

## Configuration

Create or edit your `~/.aider/config.json` file to include MCP server configurations:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    }
  }
}
```

## Usage

Start aider with a specific MCP server:

```bash
aider --model claude-3-sonnet --mcp-server filesystem
```

This will start the specified MCP server and configure the LLM to use its capabilities.

## Available MCP Servers

- **memory**: In-memory storage for temporary data
- **filesystem**: Access to specified file system paths
- **github**: GitHub repository access and operations
- **git**: Git repository operations

For more information about MCP servers, visit the [MCP documentation](https://mcp.anthropic.com/docs/reference-implementations).