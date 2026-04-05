# Test Patterns

Reference for the exact test patterns used in this project for each module type.

---

## Setup rules (applies to all tests)

- All test functions are `async def` — `asyncio_mode = "auto"` is set in `pyproject.toml`, no decorator needed
- The `client` fixture in `conftest.py` provides a connected in-memory FastMCP client — never recreate it in a test file
- Route tests must import the route module for side-effect registration (the tool/route import triggers the `@mcp.custom_route` decorator)
- Never use `app=` directly on `httpx.AsyncClient` — use `httpx.ASGITransport(app=...)` and pass it to `transport=`

---

## Tool test pattern

```python
# tests/test_<tool_name>.py

async def test_<tool_name>_success(client):
    result = await client.call_tool("<tool_name>", {"param": "value"})

    assert not result.is_error
    assert len(result.content) == 1
    assert result.content[0].text == "expected output"


async def test_<tool_name>_default_param(client):
    # Only add if the tool has parameters with defaults
    result = await client.call_tool("<tool_name>", {})

    assert not result.is_error
    assert result.content[0].text == "expected default output"


async def test_<tool_name>_error_on_invalid_input(client):
    result = await client.call_tool("<tool_name>", {"param": ""}, raise_on_error=False)

    assert result.is_error
```

Key points:
- `raise_on_error=False` is required on error-path tests — otherwise the call raises instead of returning
- `result.content[0].text` is the string returned by the tool
- For tools returning JSON, parse it: `data = json.loads(result.content[0].text)`

---

## Resource test pattern

```python
# tests/test_<resource_name>.py
import json
import pytest
from fastmcp.exceptions import McpError


async def test_<resource_name>_returns_data(client):
    resources = await client.read_resource("resource://uri-here")

    assert len(resources) > 0
    # For plain text:
    assert resources[0].content == "expected text"
    # For JSON:
    data = json.loads(resources[0].content)
    assert "expected_key" in data


async def test_<resource_name>_not_found(client):
    # Only for templated resources that can raise ResourceError
    with pytest.raises(McpError):
        await client.read_resource("resource://items/nonexistent-id")
```

Key points:
- `client.read_resource(uri)` returns a list of resource content objects
- `.content` is the string or bytes payload
- `McpError` is raised (not `ResourceError`) on the client side when the server raises `ResourceError`

---

## Route test pattern

```python
# tests/test_<route_name>.py
import httpx

from <package>.server import mcp
from <package>.routes import <route_module>  # noqa: F401 — triggers route registration


async def test_<route_name>_success():
    app = mcp.http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        resp = await http.get("/route-path")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


async def test_<route_name>_error():
    app = mcp.http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        resp = await http.post("/route-path", json={})

    assert resp.status_code == 400
    assert "error" in resp.json()
```

Key points:
- Route tests do **not** use the `client` fixture — they use `httpx.AsyncClient` directly
- `mcp.http_app()` returns the ASGI app; pass it to `httpx.ASGITransport`
- The route module import is required for the `@mcp.custom_route` decorator to run
- `base_url="http://test"` is a required placeholder for httpx — the actual host does not matter

---

## Config test pattern

```python
# tests/test_config.py
def test_default_values():
    from <package>.config import ServerConfig
    config = ServerConfig.from_env()
    assert config.host == "localhost"
    assert config.port == 8000


def test_invalid_value_raises(monkeypatch):
    monkeypatch.setenv("SOME_VAR", "bad_value")
    from <package>.config import ServerConfig
    with pytest.raises(ValueError, match="SOME_VAR"):
        ServerConfig.from_env()


def test_env_override(monkeypatch):
    monkeypatch.setenv("PORT", "9000")
    from <package>.config import ServerConfig
    config = ServerConfig.from_env()
    assert config.port == 9000
```
