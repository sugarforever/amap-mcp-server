"""amap_mcp_server package"""

from .server import mcp

def main():
    """Entry point for the MCP server"""
    import sys
    transport = 'stdio'
    if len(sys.argv) > 1:
        transport = sys.argv[1]
    mcp.run(transport=transport)

if __name__ == "__main__":
    main()
