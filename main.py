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
    port = int(os.getenv("PORT", 8000))
    logger.info("Starting MCP server on SSE transport at 0.0.0.0:%s", port)
    mcp.run(transport="sse", host="0.0.0.0", port=port)
    logger.info("MCP server stopped.")
