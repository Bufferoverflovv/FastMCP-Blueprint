# Tool Conventions

Reference for the patterns used in this project when writing FastMCP tools.

---

## File location and naming

```
src/<package>/tools/<tool_name>.py
```

- One tool per file
- File name matches the decorated function name exactly
- snake_case, action-oriented: `fetch_weather.py`, `resolve_dns_record.py`

---

## Minimal sync tool

```python
from typing import Annotated

from fastmcp_blueprint.server import get_tool_logger, mcp

logger = get_tool_logger("tool_name")


@mcp.tool()
def tool_name(param: Annotated[str, "Description of param"]) -> str:
    """One-sentence description of what the tool does."""
    logger.info("param: %s", param)
    return f"result for {param}"
```

---

## Minimal async tool (preferred for I/O)

```python
from typing import Annotated

from fastmcp_blueprint.server import get_tool_logger, mcp

logger = get_tool_logger("tool_name")


@mcp.tool()
async def tool_name(param: Annotated[str, "Description of param"]) -> str:
    """One-sentence description of what the tool does."""
    logger.info("param: %s", param)
    # await external_call(param)
    return f"result for {param}"
```

---

## Parameter annotations

Always use `Annotated` — the second element becomes the parameter description visible to the LLM:

```python
from typing import Annotated
from pydantic import Field

# Simple string description
name: Annotated[str, "The hostname to look up"]

# With validation constraints
port: Annotated[int, Field(ge=1, le=65535, description="TCP port number")]

# Optional with default
timeout: Annotated[int, "Request timeout in seconds"] = 30
```

Never use bare untyped parameters or `*args`/`**kwargs`.

---

## Hints

Set tool-level hints on the decorator for read-only or destructive operations:

```python
@mcp.tool(readOnlyHint=True)
async def fetch_data(...): ...

@mcp.tool(destructiveHint=True)
async def delete_record(...): ...
```

---

## Error handling

Use `ToolError` for expected, client-facing failures. Standard exceptions are masked by `mask_error_details=True` in production.

```python
from fastmcp.exceptions import ToolError

@mcp.tool()
async def resolve_hostname(hostname: Annotated[str, "Hostname to resolve"]) -> str:
    """Resolve a hostname to an IP address."""
    if not hostname:
        raise ToolError("Hostname must not be empty")
    try:
        result = await do_lookup(hostname)
    except LookupError as e:
        raise ToolError(f"Could not resolve {hostname!r}") from e
    return result
```

---

## Lifespan context

When the tool needs a shared resource (HTTP client, DB pool), access it through `ctx.lifespan_context`:

```python
from fastmcp import Context

@mcp.tool()
async def fetch_url(url: Annotated[str, "URL to fetch"], ctx: Context) -> str:
    """Fetch the content of a URL."""
    http_client = ctx.lifespan_context["http_client"]
    response = await http_client.get(url)
    return response.text
```

The shared resource must be yielded from `app_lifespan` in `server.py`.

---

## Logging

Always use `get_tool_logger("tool_name")` — this attaches `{"tool": "tool_name"}` to every log record:

```python
logger = get_tool_logger("tool_name")

# Inside the tool:
logger.info("processing: %s", value)
logger.warning("unexpected state: %s", detail)
```

Never use `print()` or `logging.getLogger(__name__)` directly inside a tool.

---

## Registration

Import the module in `__main__.py` for its decorator to register with FastMCP:

```python
from PACKAGE.tools import tool_name  # noqa: F401
```

The `# noqa: F401` suppresses the "imported but unused" warning — the import is intentional.
