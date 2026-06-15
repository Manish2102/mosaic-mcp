from mcp.server.fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("MosaicMCP")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}! Welcome to Mosaic MCP."
