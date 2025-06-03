import json
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class McpClient:
    """Handles MCP protocol communication with a single server."""

    def __init__(self, process: subprocess.Popen, io=None):
        self.process = process
        self.io = io
        self.request_id = 0
        self.pending_requests = {}
        self.capabilities = {}
        self.server_info = {}
        self.tools = []
        self.initialized = False
        self.protocol_version = "2025-03-26"
        self._lock = threading.Lock()
        self._reader_thread = None
        self._start_reader()

    def _start_reader(self):
        """Start background thread to read responses from server."""
        self._reader_thread = threading.Thread(target=self._read_responses, daemon=True)
        self._reader_thread.start()

    def _read_responses(self):
        """Background thread to read and process server responses."""
        try:
            while self.process.poll() is None:
                line = self.process.stdout.readline()
                if not line:
                    break

                try:
                    message = json.loads(line.strip())
                    self._handle_message(message)
                except json.JSONDecodeError as e:
                    if self.io:
                        self.io.tool_error(f"Invalid JSON from MCP server: {e}")
                except Exception as e:
                    if self.io:
                        self.io.tool_error(f"Error processing MCP message: {e}")
        except Exception as e:
            if self.io:
                self.io.tool_error(f"Error reading from MCP server: {e}")

    def _handle_message(self, message: Dict[str, Any]):
        """Handle incoming message from server."""
        if "id" in message:
            # This is a response to a request
            request_id = message["id"]
            with self._lock:
                if request_id in self.pending_requests:
                    future = self.pending_requests.pop(request_id)
                    if "error" in message:
                        future["error"] = message["error"]
                    else:
                        future["result"] = message.get("result")
                    future["done"] = True
        else:
            # This is a notification
            method = message.get("method", "")
            if method == "notifications/tools/list_changed":
                # Refresh tools list
                self._refresh_tools()

    def _send_request(
        self, method: str, params: Optional[Dict] = None, timeout: float = 30.0
    ) -> Dict[str, Any]:
        """Send a request and wait for response."""
        with self._lock:
            self.request_id += 1
            request_id = self.request_id

        request = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params:
            request["params"] = params

        # Create future for response
        future = {"done": False, "result": None, "error": None}
        with self._lock:
            self.pending_requests[request_id] = future

        try:
            # Send request
            request_json = json.dumps(request) + "\n"
            self.process.stdin.write(request_json)
            self.process.stdin.flush()

            # Wait for response
            start_time = time.time()
            while not future["done"] and time.time() - start_time < timeout:
                time.sleep(0.01)

            if not future["done"]:
                with self._lock:
                    self.pending_requests.pop(request_id, None)
                raise TimeoutError(f"MCP request {method} timed out after {timeout}s")

            if future["error"]:
                raise Exception(f"MCP error: {future['error']}")

            return future["result"]

        except Exception as e:
            with self._lock:
                self.pending_requests.pop(request_id, None)
            raise e

    def _send_notification(self, method: str, params: Optional[Dict] = None):
        """Send a notification (no response expected)."""
        notification = {"jsonrpc": "2.0", "method": method}
        if params:
            notification["params"] = params

        notification_json = json.dumps(notification) + "\n"
        self.process.stdin.write(notification_json)
        self.process.stdin.flush()

    def initialize(self) -> bool:
        """Initialize MCP connection with capability negotiation."""
        try:
            # Send initialize request
            init_params = {
                "protocolVersion": self.protocol_version,
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "aider", "version": "0.1.0"},
            }

            result = self._send_request("initialize", init_params)

            # Store server capabilities and info
            self.capabilities = result.get("capabilities", {})
            self.server_info = result.get("serverInfo", {})

            # Send initialized notification
            self._send_notification("notifications/initialized")

            # Load available tools
            self._refresh_tools()

            self.initialized = True
            if self.io:
                self.io.tool_output(
                    f"MCP server initialized: {self.server_info.get('name', 'Unknown')}"
                )

            return True

        except Exception as e:
            if self.io:
                self.io.tool_error(f"Failed to initialize MCP server: {e}")
            return False

    def _refresh_tools(self):
        """Refresh the list of available tools."""
        if not self.initialized:
            return

        try:
            if "tools" in self.capabilities:
                result = self._send_request("tools/list")
                self.tools = result.get("tools", [])
                if self.io:
                    tool_names = [tool["name"] for tool in self.tools]
                    self.io.tool_output(f"MCP tools available: {', '.join(tool_names)}")
        except Exception as e:
            if self.io:
                self.io.tool_error(f"Failed to refresh MCP tools: {e}")

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools."""
        return self.tools.copy()

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool and return the result."""
        if not self.initialized:
            raise Exception("MCP client not initialized")

        params = {"name": name, "arguments": arguments}

        result = self._send_request("tools/call", params)
        return result

    def close(self):
        """Close the MCP connection."""
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.close()
                self.process.wait(timeout=5)
            except:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except:
                    self.process.kill()


class McpServerManager:
    """Manages MCP server connections and interactions."""

    def __init__(self, io=None):
        self.io = io
        self.servers = {}
        self.active_processes = {}
        self.mcp_clients = {}

    def start_server(self, server_name: str, config: Dict) -> bool:
        """
        Start an MCP server based on configuration.

        Args:
            server_name: Name of the server to start
            config: Server configuration with command, args, and optional env

        Returns:
            bool: True if server started successfully
        """
        if server_name in self.active_processes:
            self.io.tool_output(f"MCP server '{server_name}' is already running")
            return True

        command = config.get("command")
        args = config.get("args", [])
        env_vars = config.get("env", {})

        if not command:
            self.io.tool_error(
                f"Invalid MCP server configuration for '{server_name}': missing command"
            )
            return False

        # Prepare environment variables
        process_env = os.environ.copy()
        process_env.update(env_vars)

        try:
            # Start the server process
            process = subprocess.Popen(
                [command] + args,
                env=process_env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            self.active_processes[server_name] = process

            # Create MCP client and initialize
            mcp_client = McpClient(process, self.io)
            if mcp_client.initialize():
                self.mcp_clients[server_name] = mcp_client
                self.io.tool_output(f"Started and initialized MCP server '{server_name}'")
                return True
            else:
                # Initialization failed, clean up
                process.terminate()
                del self.active_processes[server_name]
                return False

        except Exception as e:
            self.io.tool_error(f"Failed to start MCP server '{server_name}': {str(e)}")
            return False

    def stop_server(self, server_name: str) -> bool:
        """Stop a running MCP server."""
        if server_name not in self.active_processes:
            return False

        # Close MCP client first
        if server_name in self.mcp_clients:
            try:
                self.mcp_clients[server_name].close()
                del self.mcp_clients[server_name]
            except Exception as e:
                self.io.tool_error(f"Error closing MCP client '{server_name}': {str(e)}")

        process = self.active_processes[server_name]
        try:
            process.terminate()
            process.wait(timeout=5)
            del self.active_processes[server_name]
            self.io.tool_output(f"Stopped MCP server '{server_name}'")
            return True
        except Exception as e:
            self.io.tool_error(f"Error stopping MCP server '{server_name}': {str(e)}")
            try:
                process.kill()
                del self.active_processes[server_name]
            except:
                pass
            return False

    def stop_all_servers(self):
        """Stop all running MCP servers."""
        server_names = list(self.active_processes.keys())
        for server_name in server_names:
            self.stop_server(server_name)

    def get_all_tools(self) -> List[Dict[str, Any]]:
        """Get all tools from all connected MCP servers."""
        all_tools = []
        for server_name, client in self.mcp_clients.items():
            try:
                tools = client.get_tools()
                # Add server name to each tool for identification
                for tool in tools:
                    tool["_mcp_server"] = server_name
                all_tools.extend(tools)
            except Exception as e:
                self.io.tool_error(f"Error getting tools from MCP server '{server_name}': {str(e)}")
        return all_tools

    def call_tool(
        self, tool_name: str, arguments: Dict[str, Any], server_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Call a tool on an MCP server."""
        if server_name:
            # Call tool on specific server
            if server_name not in self.mcp_clients:
                raise Exception(f"MCP server '{server_name}' not found")
            return self.mcp_clients[server_name].call_tool(tool_name, arguments)
        else:
            # Find the server that has this tool
            for name, client in self.mcp_clients.items():
                tools = client.get_tools()
                if any(tool["name"] == tool_name for tool in tools):
                    return client.call_tool(tool_name, arguments)
            raise Exception(f"Tool '{tool_name}' not found on any MCP server")

    def load_config_from_file(self, config_path: Path) -> Dict:
        """Load MCP server configuration from a file."""
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                return config.get("mcpServers", {})
        except Exception as e:
            self.io.tool_error(f"Error loading MCP server config: {str(e)}")
            return {}
