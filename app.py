from tools import mcp

# Expose the ASGI app for gunicorn/uvicorn (used by Azure App Service)
# Uses streamable HTTP transport (/mcp endpoint) compatible with claude.ai
app = mcp.streamable_http_app()
