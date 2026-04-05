import httpx

from fastmcp_blueprint.server import mcp

# Import modules so decorators register routes.
from fastmcp_blueprint.routes import health  # noqa: F401
from fastmcp_blueprint.tools import hello_world  # noqa: F401


async def test_health_returns_ok():
    app = mcp.http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        resp = await http.get("/health")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


async def test_ready_returns_ready_when_tools_registered():
    app = mcp.http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        resp = await http.get("/ready")

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ready"
    assert data["checks"]["tools"] is True
