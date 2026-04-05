# Route Test Template

Placeholders to substitute before saving:

| Placeholder | Description |
|-------------|-------------|
| `ROUTE_FILE` | Module name in `routes/` (used in import) |
| `ROUTE_PATH` | URL path to call, e.g. `/webhook` |
| `PACKAGE` | Python package name |

## GET route test

```python
import httpx

from PACKAGE.server import mcp

from PACKAGE.routes import ROUTE_FILE  # noqa: F401


async def test_ROUTE_FILE_returns_ok():
    app = mcp.http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        resp = await http.get("ROUTE_PATH")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
```

## POST route test (with body)

```python
import httpx

from PACKAGE.server import mcp

from PACKAGE.routes import ROUTE_FILE  # noqa: F401


async def test_ROUTE_FILE_accepts_valid_payload():
    app = mcp.http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        resp = await http.post("ROUTE_PATH", json={"field": "value"})

    assert resp.status_code == 201


async def test_ROUTE_FILE_rejects_missing_field():
    app = mcp.http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        resp = await http.post("ROUTE_PATH", json={})

    assert resp.status_code == 400
    assert "error" in resp.json()
```
