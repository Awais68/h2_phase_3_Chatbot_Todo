"""
MCP Server entry point for Todo AI Chatbot.
This file serves as the main entry point for the MCP server when run as a module.
"""
import asyncio
import os
from mcp.server.fastmcp import FastMCP
from mcp.server.http import serve
from src.mcp.mcp_server import mcp

async def main():
    """Main function to start the MCP server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))

    print(f"Starting MCP server on {host}:{port}")
    await serve(mcp, host, port)

if __name__ == "__main__":
    asyncio.run(main())