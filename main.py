""" this are the imports """
import logging
import os
from tools import mcp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("MCP server created: %s", mcp.name)
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    logger.info("Starting MCP server with transport: %s", transport)
    if transport == "http":
        port = int(os.getenv("PORT", 8000))
        mcp.run(transport="http", host="0.0.0.0", port=port)
    else:
        mcp.run(transport="stdio")
    logger.info("MCP server stopped.")
