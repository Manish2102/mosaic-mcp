import uuid
from tools.mcp_instance import mcp


@mcp.tool()
def generate_uuid() -> str:
    """Generate a new random UUID."""
    return str(uuid.uuid4())
