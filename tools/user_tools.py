from fastmcp.server.dependencies import get_access_token
from tools.mcp_instance import mcp


@mcp.tool()
async def get_user_info() -> dict:
    """Returns information about the authenticated Azure user."""
    token = get_access_token()
    return {
        "azure_id": token.claims.get("sub"),
        "email": token.claims.get("email"),
        "name": token.claims.get("name"),
        "tenant": token.claims.get("tid"),
    }
