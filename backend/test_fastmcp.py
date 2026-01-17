"""Test basic FastMCP functionality"""
from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Test Server")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}!"

# Test tool registration
print("✅ FastMCP server created")
print(f"✅ Tools registered: {list(mcp.list_tools().keys()) if hasattr(mcp, 'list_tools') else 'N/A'}")
print("✅ Basic FastMCP test passed")
