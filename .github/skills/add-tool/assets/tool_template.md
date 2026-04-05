# Tool Template

Placeholders to substitute before saving:

| Placeholder | Description |
|-------------|-------------|
| `TOOL_NAME` | snake_case function and file name |
| `TOOL_DOCSTRING` | One-sentence description for the LLM |
| `PACKAGE` | Python package name (e.g. `fastmcp_blueprint`) |
| `PARAM_NAME` | Parameter variable name |
| `PARAM_TYPE` | Python type (`str`, `int`, `float`, `bool`, etc.) |
| `PARAM_DESC` | Short parameter description shown to the LLM |
| `RETURN_TYPE` | Python return type annotation |
| `HINT_LINE` | `@mcp.tool()` or `@mcp.tool(readOnlyHint=True)` or `@mcp.tool(destructiveHint=True)` |

```python
from typing import Annotated

from fastmcp.exceptions import ToolError

from PACKAGE.server import get_tool_logger, mcp

logger = get_tool_logger("TOOL_NAME")


HINT_LINE
async def TOOL_NAME(
    PARAM_NAME: Annotated[PARAM_TYPE, "PARAM_DESC"],
) -> RETURN_TYPE:
    """TOOL_DOCSTRING"""
    logger.info("PARAM_NAME: %s", PARAM_NAME)

    if not PARAM_NAME:
        raise ToolError("PARAM_NAME must not be empty")

    # TODO: implement tool logic here
    result = f"processed {PARAM_NAME}"

    return result
```
