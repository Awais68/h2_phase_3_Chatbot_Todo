"""
MCP Server startup for Todo AI Chatbot.
"""
import os
import sys
from mcp.server.fastmcp import FastMCP
from mcp.server.http import serve
from src.mcp.mcp_server import mcp


def run_server():
    """Run the MCP server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))

    print(f"Starting MCP server on {host}:{port}")

    # Run the MCP server
    serve(mcp, host, port)


if __name__ == "__main__":
    run_server()