from starlette.requests import Request
from starlette.responses import JSONResponse

from fastmcp_blueprint.server import mcp


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Liveness probe — always returns ok if the process is running."""
    return JSONResponse({"status": "ok"})


@mcp.custom_route("/ready", methods=["GET"])
async def readiness_check(request: Request) -> JSONResponse:
    """Readiness probe — verifies the server can serve MCP requests."""
    checks = {}

    tools = await mcp.list_tools()
    checks["tools"] = len(tools) > 0

    ready = all(checks.values())

    return JSONResponse(
        {"status": "ready" if ready else "not_ready", "checks": checks},
        status_code=200 if ready else 503,
    )
