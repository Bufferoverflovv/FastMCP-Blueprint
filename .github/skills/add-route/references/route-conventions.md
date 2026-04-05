# Route Conventions

Reference for the patterns used in this project when writing FastMCP custom routes.

---

## File location and naming

```
src/<package>/routes/<route_file>.py
```

- Group related routes in one file (e.g. all health probes in `health.py`)
- Create a new file for unrelated endpoint groups
- File name is a noun describing the group: `health.py`, `webhooks.py`, `admin.py`

---

## Handler signature

All handlers must be `async def`, accept a Starlette `Request`, and return a Starlette `Response`:

```python
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response

from PACKAGE.server import mcp


@mcp.custom_route("/path", methods=["GET"])
async def handler_name(request: Request) -> JSONResponse:
    """One-sentence description of what this endpoint does."""
    return JSONResponse({"status": "ok"})
```

---

## Reading request data

```python
# Query parameters
value = request.query_params.get("key", "default")

# JSON body (POST/PUT)
body = await request.json()
field = body.get("field")

# Raw body bytes
raw = await request.body()

# Headers
token = request.headers.get("Authorization", "")
```

---

## Response types

```python
# JSON (most common)
return JSONResponse({"key": "value"})
return JSONResponse({"key": "value"}, status_code=201)

# Plain text
return PlainTextResponse("ok\n")

# Error responses — always use JSON for consistency
return JSONResponse({"error": "Bad input: field is required"}, status_code=400)
return JSONResponse({"error": "Forbidden"}, status_code=403)
return JSONResponse({"error": "Not found"}, status_code=404)

# Redirect
from starlette.responses import RedirectResponse
return RedirectResponse(url="/new-path", status_code=302)
```

---

## Multiple methods on one route

```python
@mcp.custom_route("/webhook", methods=["POST"])
async def receive_webhook(request: Request) -> JSONResponse:
    """Receive and acknowledge an incoming webhook payload."""
    body = await request.json()
    # process body...
    return JSONResponse({"received": True})
```

---

## Error handling pattern

```python
@mcp.custom_route("/admin/reload", methods=["POST"])
async def reload_config(request: Request) -> JSONResponse:
    """Reload server configuration without restarting."""
    token = request.headers.get("X-Admin-Token", "")
    if token != settings.admin_token:
        return JSONResponse({"error": "Forbidden"}, status_code=403)

    try:
        _do_reload()
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)

    return JSONResponse({"status": "reloaded"})
```

---

## Registration

Import the module in `__main__.py`:

```python
from PACKAGE.routes import route_file  # noqa: F401
```
