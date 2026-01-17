"""
MCP Server setup for Todo AI Chatbot.
"""
from typing import Dict, Any, List
import json


class MCPServer:
    """MCP Server for managing AI tools."""

    def __init__(self):
        self.tools: Dict[str, Any] = {}

    def tool(self, name: str = None):
        """Decorator to register MCP tools."""
        def decorator(func):
            tool_name = name or func.__name__
            self.tools[tool_name] = func
            return func
        return decorator

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get OpenAI-compatible tool definitions."""
        definitions = []
        for tool_name, tool_func in self.tools.items():
            # Extract function signature and docstring
            import inspect
            sig = inspect.signature(tool_func)
            doc = inspect.getdoc(tool_func) or ""

            # Build parameter schema
            parameters = {
                "type": "object",
                "properties": {},
                "required": []
            }

            for param_name, param in sig.parameters.items():
                if param_name in ['self', 'session']:
                    continue

                param_type = "string"
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == bool:
                    param_type = "boolean"

                parameters["properties"][param_name] = {
                    "type": param_type,
                    "description": f"{param_name} parameter"
                }

                if param.default == inspect.Parameter.empty:
                    parameters["required"].append(param_name)

            definitions.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": doc.split('\n')[0] if doc else tool_name,
                    "parameters": parameters
                }
            })

        return definitions

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a registered tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")

        return self.tools[tool_name](**kwargs)


# Global MCP server instance
mcp_server = MCPServer()
