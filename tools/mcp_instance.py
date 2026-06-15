import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider

load_dotenv()
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
tenant_id = os.getenv("AZURE_TENANT_ID")
base_url = os.getenv("AZURE_BASE_URL", "http://localhost:8000")
jwt_signing_key = os.getenv("JWT_SIGNING_KEY")

auth_provider = AzureProvider(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id,
    base_url=base_url,
    required_scopes="api://8601532b-6517-43c9-a321-ed5f6f0b8a97/Read",
    jwt_signing_key=jwt_signing_key,
)

mcp = FastMCP("MosaicMCP", auth=auth_provider)


@mcp.custom_route("/health", methods=["GET"])
async def health_check():
    """Health check endpoint to verify the server is running."""
    return {"status": "ok"}
