import pytest
from fastmcp.client import Client

from fastmcp_blueprint.server import mcp

# Import modules so decorators register tools/resources/routes with FastMCP.
from fastmcp_blueprint.routes import health  # noqa: F401
from fastmcp_blueprint.tools import hello_world  # noqa: F401


@pytest.fixture
async def client():
    """In-memory MCP client connected to the server — no network, no subprocess."""
    async with Client(mcp) as c:
        yield c
