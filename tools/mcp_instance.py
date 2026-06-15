from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# Disable DNS rebinding protection so Azure's proxy host headers are accepted
mcp = FastMCP(
    "MosaicMCP",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)
