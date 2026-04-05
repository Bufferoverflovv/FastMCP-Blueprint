# Resource Template

Placeholders to substitute before saving:

| Placeholder | Description |
|-------------|-------------|
| `RESOURCE_NAME` | snake_case function and file name |
| `RESOURCE_URI` | Full URI string, e.g. `resource://config` or `resource://user/{user_id}` |
| `RESOURCE_DESC` | One-sentence description for the LLM |
| `PACKAGE` | Python package name (e.g. `fastmcp_blueprint`) |
| `RETURN_TYPE` | `str` for text/JSON, `bytes` for binary |

## Static resource

Use when the URI has no `{param}` segments.

```python
import json

from fastmcp.exceptions import ResourceError

from PACKAGE.server import mcp


@mcp.resource("RESOURCE_URI")
def RESOURCE_NAME() -> RETURN_TYPE:
    """RESOURCE_DESC"""
    # TODO: retrieve or build the resource data
    data = {"example": "value"}

    if not data:
        raise ResourceError("Resource data is unavailable")

    return json.dumps(data)
```

## Templated resource variant

Use when the URI contains `{param}` segments. The function signature must include matching typed parameters.

```python
import json

from fastmcp.exceptions import ResourceError

from PACKAGE.server import mcp


@mcp.resource("resource://items/{item_id}")
def get_item(item_id: str) -> str:
    """Return the item with the given ID."""
    item = lookup(item_id)
    if item is None:
        raise ResourceError(f"Item {item_id!r} not found")
    return json.dumps(item)
```
