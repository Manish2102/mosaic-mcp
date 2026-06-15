import logging
from tools import mcp  # imports from tools/__init__.py -> add_tools.py

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("MCP server created: %s", mcp.name)
    logger.info("Starting MCP server on stdio transport...")
    mcp.run(transport="sse")
    logger.info("MCP server stopped.")
