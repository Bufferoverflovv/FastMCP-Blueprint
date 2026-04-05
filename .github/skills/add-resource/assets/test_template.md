# Resource Test Template

Placeholders to substitute before saving:

| Placeholder | Description |
|-------------|-------------|
| `RESOURCE_NAME` | Matches the resource function name |
| `RESOURCE_URI` | Full URI string used when reading the resource |
| `EXPECTED_KEY` | A JSON key to assert in the parsed response (for structured resources) |

## Static resource test

```python
import json


async def test_RESOURCE_NAME_returns_data(client):
    resources = await client.read_resource("RESOURCE_URI")

    assert len(resources) > 0
    content = resources[0].content
    # For JSON resources, parse and assert specific fields:
    data = json.loads(content)
    assert "EXPECTED_KEY" in data
```

## Templated resource error test

Add this when the resource raises `ResourceError` for missing items.

```python
import pytest
from fastmcp.exceptions import McpError


async def test_RESOURCE_NAME_not_found(client):
    with pytest.raises(McpError):
        await client.read_resource("resource://items/nonexistent-id")
```
