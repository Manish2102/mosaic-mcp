from tools.mcp_instance import mcp
from fastmcp.utilities.types import Image
from mcp.types import Icon



greet_icon = Image(path="./assets/greet_icon.jpg")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool(
        name = "greet_user", 
        description = "Greet a user by their name.",
        icons = [Icon(src=greet_icon.to_data_uri(), alt="Greet Icon")])
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}! Welcome to Mosaic MCP."
