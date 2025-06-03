# MCP (Model Context Protocol) Integration in Aider

This document describes the MCP integration implementation in aider, which allows the LLM to access and use tools from MCP servers.

## Overview

The MCP integration consists of several key components:

1. **McpServerManager** - Manages MCP server processes and connections
2. **McpClient** - Handles JSON-RPC communication with individual MCP servers
3. **McpToolsIntegration** - Integrates MCP tools with aider's LLM workflow
4. **Model Integration** - Adds MCP tools to LLM conversations

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│     Aider       │    │  MCP Integration │    │   MCP Server    │
│                 │    │                  │    │                 │
│  ┌───────────┐  │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│  │    LLM    │◄─┼────┼─│ McpToolsInt. │ │    │ │    Tools    │ │
│  └───────────┘  │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│  ┌───────────┐  │    │ │  McpClient   │◄┼────┼─│ JSON-RPC    │ │
│  │   Model   │◄─┼────┼─│              │ │    │ │ Interface   │ │
│  └───────────┘  │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │ ┌──────────────┐ │    └─────────────────┘
│                 │    │ │McpServerMgr  │ │
│                 │    │ └──────────────┘ │
└─────────────────┘    └──────────────────┘
```

## Configuration

### 1. Create MCP Server Configuration

Create or edit `~/.aider/config.json`:

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

### 2. Start Aider with MCP Server

```bash
aider --model claude-3-sonnet --mcp-server filesystem
```

## Usage

Once configured, the LLM will automatically have access to tools from the specified MCP server. The tools will be:

1. **Discovered** - Available tools are loaded from the MCP server
2. **Described** - Tool descriptions are added to the system prompt
3. **Callable** - The LLM can call tools using function calling
4. **Executed** - Tool calls are routed to the appropriate MCP server
5. **Responded** - Tool results are returned to the LLM

## Implementation Details

### MCP Protocol Communication

The implementation follows the MCP specification:

- **Initialization**: Capability negotiation with `initialize` request
- **Tool Discovery**: `tools/list` to get available tools
- **Tool Execution**: `tools/call` to execute tools
- **Notifications**: Handle `notifications/tools/list_changed`

### JSON-RPC Communication

- Asynchronous request/response handling
- Proper error handling and timeouts
- Background thread for reading server responses
- Request ID management for correlation

### LLM Integration

- Tools are converted to OpenAI function calling format
- Tool descriptions are added to system messages
- Function calls are intercepted and routed to MCP servers
- Tool results are formatted for LLM consumption

## Error Handling

The implementation includes comprehensive error handling:

- **Connection Errors**: Server startup failures
- **Protocol Errors**: Invalid JSON-RPC messages
- **Tool Errors**: Tool execution failures
- **Timeout Errors**: Request timeouts

## Security Considerations

- **User Consent**: Tool calls are shown to the user
- **Input Validation**: Tool arguments are validated
- **Process Management**: MCP servers run in isolated processes
- **Environment Isolation**: Environment variables are properly managed

## Testing

Basic tests are included in `tests/basic/test_mcp.py`:

- Configuration loading
- Tool format conversion
- Result formatting
- Error handling

## Available MCP Servers

Popular MCP servers that work with this integration:

- **@modelcontextprotocol/server-memory**: In-memory storage
- **@modelcontextprotocol/server-filesystem**: File system access
- **@modelcontextprotocol/server-github**: GitHub operations
- **@modelcontextprotocol/server-git**: Git operations

## Troubleshooting

### Common Issues

1. **Server Not Starting**: Check command and arguments in config
2. **No Tools Available**: Verify server supports tools capability
3. **Tool Call Failures**: Check tool arguments and permissions
4. **Connection Timeouts**: Increase timeout values if needed

### Debug Mode

Use `--verbose` flag to see detailed MCP communication:

```bash
aider --model claude-3-sonnet --mcp-server filesystem --verbose
```

## Future Enhancements

Potential improvements for the MCP integration:

1. **Multiple Servers**: Support for multiple concurrent MCP servers
2. **Resource Support**: Integration with MCP resources
3. **Prompt Support**: Integration with MCP prompts
4. **HTTP Transport**: Support for HTTP-based MCP servers
5. **Authentication**: Enhanced authentication mechanisms
