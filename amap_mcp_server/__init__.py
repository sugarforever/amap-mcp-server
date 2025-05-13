"""amap_mcp_server package"""

import argparse
from .server import mcp

def main():
    """Entry point for the MCP server"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Amap MCP Server")
    parser.add_argument('transport', nargs='?', default='stdio', choices=['stdio', 'sse', 'streamable-http'],
                        help='Transport type (stdio, sse, or streamable-http)')
    args = parser.parse_args()
    
    # Run the MCP server with the specified transport
    mcp.run(transport=args.transport)

if __name__ == "__main__":
    main()
