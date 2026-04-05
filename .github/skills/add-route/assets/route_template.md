# Route Handler Template

Placeholders to substitute before saving:

| Placeholder | Description |
|-------------|-------------|
| `ROUTE_PATH` | URL path, e.g. `/webhook` or `/admin/reload` |
| `METHOD` | HTTP method in uppercase: `GET`, `POST`, `PUT`, `DELETE` |
| `HANDLER_NAME` | snake_case function name |
| `HANDLER_DOCSTRING` | One-sentence description |
| `PACKAGE` | Python package name |

## GET handler

```python
from starlette.requests import Request
from starlette.responses import JSONResponse

from PACKAGE.server import mcp


@mcp.custom_route("ROUTE_PATH", methods=["METHOD"])
async def HANDLER_NAME(request: Request) -> JSONResponse:
    """HANDLER_DOCSTRING"""
    return JSONResponse({"status": "ok"})
```

## POST handler (with JSON body)

```python
from starlette.requests import Request
from starlette.responses import JSONResponse

from PACKAGE.server import mcp


@mcp.custom_route("ROUTE_PATH", methods=["POST"])
async def HANDLER_NAME(request: Request) -> JSONResponse:
    """HANDLER_DOCSTRING"""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    field = body.get("field")
    if not field:
        return JSONResponse({"error": "'field' is required"}, status_code=400)

    # TODO: process the request
    return JSONResponse({"received": True}, status_code=201)
```
