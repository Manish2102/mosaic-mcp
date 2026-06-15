import logging
import os
from tools import mcp  # imports from tools/__init__.py -> add_tools.py

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("MCP server created: %s", mcp.name)
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    logger.info("Starting MCP server with transport: %s", transport)
    if transport == "sse":
        port = int(os.getenv("PORT", 8000))
        mcp.run(transport="sse", host="0.0.0.0", port=port)
    else:
        mcp.run(transport="stdio")
    logger.info("MCP server stopped.")
