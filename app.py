from tools import mcp

# Expose the ASGI app for gunicorn/uvicorn (used by Azure App Service)
app = mcp.sse_app()
