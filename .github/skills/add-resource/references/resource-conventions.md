# Resource Conventions

Reference for the patterns used in this project when writing FastMCP resources.

---

## File location and naming

```
src/<package>/resources/<resource_name>.py
```

- One resource per file
- File name matches the decorated function name exactly
- snake_case, noun-oriented: `server_config.py`, `user_profile.py`

---

## Static resource (fixed URI)

Returns a single value, always at the same URI.

```python
import json

from fastmcp_blueprint.server import mcp


@mcp.resource("resource://config")
def server_config() -> str:
    """Return server configuration as a JSON string."""
    return json.dumps({"version": "1.0", "environment": "production"})
```

---

## Templated resource (URI with parameters)

URI contains `{param}` segments. The function signature must include matching typed parameters.

```python
import json

from fastmcp.exceptions import ResourceError

from fastmcp_blueprint.server import mcp


@mcp.resource("resource://user/{user_id}")
def user_profile(user_id: str) -> str:
    """Return the profile for a given user."""
    user = lookup_user(user_id)
    if user is None:
        raise ResourceError(f"User {user_id!r} not found")
    return json.dumps(user)
```

---

## Binary resource

Return `bytes` and set `mime_type` explicitly.

```python
from fastmcp_blueprint.server import mcp


@mcp.resource("resource://logo", mime_type="image/png")
def logo() -> bytes:
    """Return the server logo as PNG bytes."""
    return Path("assets/logo.png").read_bytes()
```

---

## Return contract rules

| Return value | When to use |
|---|---|
| `str` | Plain text or pre-serialised JSON (`json.dumps(...)`) |
| `bytes` | Binary data; always set `mime_type=` |

**Never return a raw `dict` or `list`.** Always call `json.dumps()` for structured data.

---

## Error handling

Use `ResourceError` for expected, client-visible failures:

```python
from fastmcp.exceptions import ResourceError

raise ResourceError(f"Record {record_id!r} does not exist")
```

Standard exceptions are masked in production by `mask_error_details=True`.

---

## URI design guidelines

- Use `resource://` scheme for most data resources
- Use descriptive noun-based paths: `resource://metrics`, `resource://config`
- For collections with lookup by ID: `resource://posts/{post_id}`
- Avoid verbs in URIs — resources are nouns, tools are verbs

---

## Registration

Import the module in `__main__.py` for its decorator to register with FastMCP:

```python
from PACKAGE.resources import resource_name  # noqa: F401
```
