from starlette.middleware.trustedhost import TrustedHostMiddleware
from tools import mcp

# Expose the ASGI app for gunicorn/uvicorn (used by Azure App Service)
app = mcp.sse_app()

# Allow Azure App Service host headers
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)
