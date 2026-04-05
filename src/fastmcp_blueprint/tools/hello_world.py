from typing import Annotated

from fastmcp_blueprint.server import get_tool_logger, mcp

logger = get_tool_logger("hello_world")


@mcp.tool()
def hello_world(name: Annotated[str, "Name to greet"] = "World") -> str:
    """Return a friendly greeting."""
    logger.info("name: %s", name)
    return f"Hello, {name}!"
