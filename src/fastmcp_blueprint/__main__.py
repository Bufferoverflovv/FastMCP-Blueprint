# https://gofastmcp.com/

import argparse

import fastmcp

from fastmcp_blueprint.config import settings
from fastmcp_blueprint.logging_setup import route_uvicorn_to_fastmcp
from fastmcp_blueprint.server import mcp

# Import modules for side effects so decorators register routes and tools with FastMCP.
from fastmcp_blueprint.routes import health  # noqa: F401
from fastmcp_blueprint.tools import hello_world  # noqa: F401


def _configure_log_format():
    """Configure logging format based on the LOG_FORMAT setting.

    Supported formats:
    - "rich" (default): FastMCP's Rich-formatted console output
    - "plain": Simple %(levelname)s: %(message)s format
    - "json": Structured JSON via FastMCP's StructuredLoggingMiddleware
    """
    if settings.log_format in ("json", "plain"):
        fastmcp.settings.enable_rich_logging = False
        fastmcp.settings.enable_rich_tracebacks = False


def main():
    parser = argparse.ArgumentParser(description="Run MCP server")
    parser.add_argument("--host", default=settings.host, help="Host to bind to")
    parser.add_argument("--port", type=int, default=settings.port, help="Port to listen on")
    parser.add_argument(
        "--ssl-certfile",
        type=str,
        default=settings.ssl_certfile,
        help="Path to the SSL certificate file.",
    )
    parser.add_argument(
        "--ssl-keyfile",
        type=str,
        default=settings.ssl_keyfile,
        help="Path to the SSL private key file. Only needed when the key is separate from the cert.",
    )
    parser.add_argument(
        "--log-level",
        default=settings.log_level,
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Logging level (default: INFO). Use DEBUG for verbose request tracing.",
    )

    args = parser.parse_args()

    _configure_log_format()
    if settings.log_format == "json":
        route_uvicorn_to_fastmcp()

    uvicorn_config = {}
    if args.ssl_certfile:
        uvicorn_config["ssl_certfile"] = args.ssl_certfile
    if args.ssl_keyfile:
        uvicorn_config["ssl_keyfile"] = args.ssl_keyfile

    try:
        mcp.run(
            transport="http",
            host=args.host,
            port=args.port,
            log_level=args.log_level,
            uvicorn_config=uvicorn_config or None,
        )
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
