"""
MCP Tools integration for aider.

This module provides integration between MCP (Model Context Protocol) servers
and aider's LLM workflow, allowing the LLM to discover and use tools from
MCP servers.
"""

import json
from typing import Any, Dict, List


class McpToolsIntegration:
    """Integrates MCP tools with aider's LLM workflow."""

    def __init__(self, mcp_server_manager=None, io=None):
        self.mcp_server_manager = mcp_server_manager
        self.io = io
        self._tools_cache = []
        self._tools_cache_valid = False

    def get_tools_for_llm(self) -> List[Dict[str, Any]]:
        """Get MCP tools formatted for LLM consumption."""
        if not self.mcp_server_manager:
            return []

        if not self._tools_cache_valid:
            self._refresh_tools_cache()

        return self._tools_cache

    def _refresh_tools_cache(self):
        """Refresh the cached tools list."""
        try:
            mcp_tools = self.mcp_server_manager.get_all_tools()
            self._tools_cache = []

            for tool in mcp_tools:
                # Convert MCP tool format to LLM tool format
                llm_tool = self._convert_mcp_tool_to_llm_format(tool)
                self._tools_cache.append(llm_tool)

            self._tools_cache_valid = True

            if self.io and self._tools_cache:
                tool_names = [tool["function"]["name"] for tool in self._tools_cache]
                self.io.tool_output(f"MCP tools available for LLM: {', '.join(tool_names)}")

        except Exception as e:
            if self.io:
                self.io.tool_error(f"Error refreshing MCP tools cache: {e}")
            self._tools_cache = []
            self._tools_cache_valid = False

    def _convert_mcp_tool_to_llm_format(self, mcp_tool: Dict[str, Any]) -> Dict[str, Any]:
        """Convert MCP tool format to OpenAI function calling format."""
        return {
            "type": "function",
            "function": {
                "name": mcp_tool["name"],
                "description": mcp_tool.get("description", ""),
                "parameters": mcp_tool.get(
                    "inputSchema", {"type": "object", "properties": {}, "required": []}
                ),
            },
            "_mcp_server": mcp_tool.get("_mcp_server"),
        }

    def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call an MCP tool and return formatted result."""
        if not self.mcp_server_manager:
            return "Error: No MCP server manager available"

        try:
            # Find the server for this tool
            server_name = None
            for tool in self._tools_cache:
                if tool["function"]["name"] == tool_name:
                    server_name = tool.get("_mcp_server")
                    break

            if not server_name:
                return f"Error: Tool '{tool_name}' not found"

            # Call the tool
            result = self.mcp_server_manager.call_tool(tool_name, arguments, server_name)

            # Format the result for the LLM
            return self._format_tool_result(result)

        except Exception as e:
            error_msg = f"Error calling MCP tool '{tool_name}': {str(e)}"
            if self.io:
                self.io.tool_error(error_msg)
            return error_msg

    def _format_tool_result(self, result: Dict[str, Any]) -> str:
        """Format MCP tool result for LLM consumption."""
        if result.get("isError", False):
            return f"Tool execution error: {self._extract_content_text(result)}"

        content = result.get("content", [])
        if not content:
            return "Tool executed successfully (no output)"

        # Extract text content from the result
        text_parts = []
        for item in content:
            if item.get("type") == "text":
                text_parts.append(item.get("text", ""))
            elif item.get("type") == "image":
                text_parts.append(f"[Image: {item.get('mimeType', 'unknown')}]")
            elif item.get("type") == "audio":
                text_parts.append(f"[Audio: {item.get('mimeType', 'unknown')}]")
            elif item.get("type") == "resource":
                resource = item.get("resource", {})
                text_parts.append(f"[Resource: {resource.get('uri', 'unknown')}]")
                if resource.get("text"):
                    text_parts.append(resource["text"])

        return "\n".join(text_parts) if text_parts else "Tool executed successfully"

    def _extract_content_text(self, result: Dict[str, Any]) -> str:
        """Extract text content from MCP result."""
        content = result.get("content", [])
        for item in content:
            if item.get("type") == "text":
                return item.get("text", "Unknown error")
        return "Unknown error"

    def invalidate_cache(self):
        """Invalidate the tools cache to force refresh."""
        self._tools_cache_valid = False

    def has_tools(self) -> bool:
        """Check if any MCP tools are available."""
        if not self.mcp_server_manager:
            return False

        if not self._tools_cache_valid:
            self._refresh_tools_cache()

        return len(self._tools_cache) > 0


def create_mcp_function_call_handler(mcp_tools_integration: McpToolsIntegration):
    """Create a function call handler for MCP tools."""

    def handle_function_call(function_name: str, function_args: Dict[str, Any]) -> str:
        """Handle function calls from the LLM."""
        return mcp_tools_integration.call_mcp_tool(function_name, function_args)

    return handle_function_call


def add_mcp_tools_to_messages(
    messages: List[Dict[str, Any]], mcp_tools_integration: McpToolsIntegration
) -> List[Dict[str, Any]]:
    """Add MCP tools to the messages for LLM consumption."""
    if not mcp_tools_integration or not mcp_tools_integration.has_tools():
        return messages

    tools = mcp_tools_integration.get_tools_for_llm()
    if not tools:
        return messages

    # Add tools information to the system message
    tools_description = "You have access to the following tools from MCP servers:\n\n"
    for tool in tools:
        func = tool["function"]
        tools_description += f"- {func['name']}: {func['description']}\n"

    tools_description += "\nYou can call these tools by using function calls in your response."

    # Find system message and append tools info
    modified_messages = []
    system_message_found = False

    for message in messages:
        if message.get("role") == "system" and not system_message_found:
            # Append tools info to first system message
            content = message.get("content", "")
            content += f"\n\n{tools_description}"
            modified_message = message.copy()
            modified_message["content"] = content
            modified_messages.append(modified_message)
            system_message_found = True
        else:
            modified_messages.append(message)

    # If no system message found, add one
    if not system_message_found:
        system_message = {"role": "system", "content": tools_description}
        modified_messages.insert(0, system_message)

    return modified_messages
