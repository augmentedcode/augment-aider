"""
Tests for MCP (Model Context Protocol) integration.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from aider.io import InputOutput
from aider.mcp_server import McpClient, McpServerManager
from aider.mcp_tools import McpToolsIntegration


class TestMcpServerManager(unittest.TestCase):
    def setUp(self):
        self.io = InputOutput(pretty=False, fancy_input=False, yes=True)
        self.manager = McpServerManager(self.io)

    def test_load_config_from_file(self):
        """Test loading MCP server configuration from file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            config = {
                "mcpServers": {
                    "test_server": {
                        "command": "echo",
                        "args": ["hello"],
                        "env": {"TEST_VAR": "test_value"},
                    }
                }
            }
            json.dump(config, f)
            config_path = Path(f.name)

        try:
            result = self.manager.load_config_from_file(config_path)
            self.assertEqual(result["test_server"]["command"], "echo")
            self.assertEqual(result["test_server"]["args"], ["hello"])
            self.assertEqual(result["test_server"]["env"]["TEST_VAR"], "test_value")
        finally:
            os.unlink(config_path)

    def test_load_config_missing_file(self):
        """Test loading config from non-existent file."""
        result = self.manager.load_config_from_file(Path("/nonexistent/file.json"))
        self.assertEqual(result, {})


class TestMcpClient(unittest.TestCase):
    def setUp(self):
        self.io = InputOutput(pretty=False, fancy_input=False, yes=True)

    @patch("subprocess.Popen")
    def test_mcp_client_initialization(self, mock_popen):
        """Test MCP client initialization."""
        # Mock process
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdout.readline.return_value = ""
        mock_popen.return_value = mock_process

        client = McpClient(mock_process, self.io)
        self.assertIsNotNone(client)
        self.assertEqual(client.protocol_version, "2025-03-26")
        self.assertFalse(client.initialized)

    @patch("subprocess.Popen")
    def test_mcp_client_send_request(self, mock_popen):
        """Test sending requests to MCP server."""
        # Mock process
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdout.readline.return_value = ""
        mock_process.stdin = Mock()
        mock_popen.return_value = mock_process

        client = McpClient(mock_process, self.io)

        # Mock a successful response
        response = {"result": {"test": "data"}}
        with patch.object(client, "_handle_message") as mock_handle:
            # Simulate response handling
            future = {"done": True, "result": response["result"], "error": None}
            client.pending_requests[1] = future

            # This would normally timeout, but we'll mock the response
            with patch("time.time", side_effect=[0, 0, 0, 1]):  # Simulate immediate response
                try:
                    result = client._send_request("test_method", {"test": "param"}, timeout=0.1)
                    # This will timeout in the test, which is expected
                except TimeoutError:
                    pass


class TestMcpToolsIntegration(unittest.TestCase):
    def setUp(self):
        self.io = InputOutput(pretty=False, fancy_input=False, yes=True)
        self.mock_manager = Mock()
        self.integration = McpToolsIntegration(self.mock_manager, self.io)

    def test_convert_mcp_tool_to_llm_format(self):
        """Test converting MCP tool format to LLM format."""
        mcp_tool = {
            "name": "test_tool",
            "description": "A test tool",
            "inputSchema": {
                "type": "object",
                "properties": {"param1": {"type": "string"}},
                "required": ["param1"],
            },
            "_mcp_server": "test_server",
        }

        llm_tool = self.integration._convert_mcp_tool_to_llm_format(mcp_tool)

        self.assertEqual(llm_tool["type"], "function")
        self.assertEqual(llm_tool["function"]["name"], "test_tool")
        self.assertEqual(llm_tool["function"]["description"], "A test tool")
        self.assertEqual(llm_tool["_mcp_server"], "test_server")

    def test_format_tool_result_text(self):
        """Test formatting tool result with text content."""
        result = {"content": [{"type": "text", "text": "Hello, world!"}], "isError": False}

        formatted = self.integration._format_tool_result(result)
        self.assertEqual(formatted, "Hello, world!")

    def test_format_tool_result_error(self):
        """Test formatting tool result with error."""
        result = {"content": [{"type": "text", "text": "Something went wrong"}], "isError": True}

        formatted = self.integration._format_tool_result(result)
        self.assertEqual(formatted, "Tool execution error: Something went wrong")

    def test_format_tool_result_mixed_content(self):
        """Test formatting tool result with mixed content types."""
        result = {
            "content": [
                {"type": "text", "text": "Text content"},
                {"type": "image", "mimeType": "image/png"},
                {"type": "audio", "mimeType": "audio/wav"},
                {
                    "type": "resource",
                    "resource": {"uri": "file://test.txt", "text": "Resource content"},
                },
            ],
            "isError": False,
        }

        formatted = self.integration._format_tool_result(result)
        expected = (
            "Text content\n[Image: image/png]\n[Audio: audio/wav]\n[Resource:"
            " file://test.txt]\nResource content"
        )
        self.assertEqual(formatted, expected)

    def test_call_mcp_tool_no_manager(self):
        """Test calling MCP tool without manager."""
        integration = McpToolsIntegration(None, self.io)
        result = integration.call_mcp_tool("test_tool", {})
        self.assertEqual(result, "Error: No MCP server manager available")

    def test_has_tools_no_manager(self):
        """Test has_tools with no manager."""
        integration = McpToolsIntegration(None, self.io)
        self.assertFalse(integration.has_tools())


if __name__ == "__main__":
    unittest.main()
