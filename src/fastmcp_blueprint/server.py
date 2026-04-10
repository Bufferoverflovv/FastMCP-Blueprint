import logging

from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.logging import StructuredLoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware

from fastmcp_blueprint.config import settings
from fastmcp_blueprint.logging_setup import RequestContextMiddleware, install_json_handler

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Auth provider — disabled by default; set AUTH_PROVIDER in .env to enable
# ---------------------------------------------------------------------------


def _build_auth():
    """Return an auth provider based on AUTH_PROVIDER, or None if disabled."""
    provider = settings.auth_provider

    if not provider:
        return None

    if provider == "remote":
        # JWT verification + OAuth protected-resource discovery (DCR providers)
        # https://gofastmcp.com/servers/auth/remote-oauth
        from fastmcp.server.auth import RemoteAuthProvider
        from fastmcp.server.auth.providers.jwt import JWTVerifier
        from pydantic import AnyHttpUrl

        verifier = JWTVerifier(
            jwks_uri=settings.auth_jwks_uri,
            issuer=settings.auth_issuer,
            audience=settings.auth_audience,
        )
        return RemoteAuthProvider(
            token_verifier=verifier,
            authorization_servers=[AnyHttpUrl(settings.auth_issuer)],
            base_url=settings.auth_base_url,
        )

    if provider == "oauth_proxy":
        # OAuth Proxy for providers without DCR (GitHub, Google, Azure, etc.)
        # https://gofastmcp.com/servers/auth/oauth-proxy
        from fastmcp.server.auth import OAuthProxy
        from fastmcp.server.auth.providers.jwt import JWTVerifier

        verifier = JWTVerifier(
            jwks_uri=settings.auth_jwks_uri,
            issuer=settings.auth_issuer,
            audience=settings.auth_audience,
        )
        return OAuthProxy(
            upstream_authorization_endpoint=settings.oauth_upstream_authorize_url,
            upstream_token_endpoint=settings.oauth_upstream_token_url,
            upstream_client_id=settings.oauth_client_id,
            upstream_client_secret=settings.oauth_client_secret,
            token_verifier=verifier,
            base_url=settings.auth_base_url,
        )

    return None


# ---------------------------------------------------------------------------
# Lifespan — server-level startup / teardown
# ---------------------------------------------------------------------------


@lifespan
async def app_lifespan(server):
    """Run once on server start; clean up on stop.

    Yield a dict of shared objects (DB pools, HTTP clients, etc.) that tools
    can access via ``ctx.lifespan_context``.
    """
    if settings.log_format == "json":
        install_json_handler()
    logger.info("Server starting up")
    try:
        yield {}
    finally:
        logger.info("Server shutting down")


# ---------------------------------------------------------------------------
# Logger adapter for tool-scoped structured logs
# ---------------------------------------------------------------------------


class ToolLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter that attaches tool context as structured fields."""

    def process(self, msg, kwargs):
        tool_name = self.extra.get("tool_name", "unknown_tool")
        original_extra = kwargs.get("extra")
        if original_extra is not None:
            extra = dict(original_extra)
        else:
            extra = {}
        extra["tool"] = tool_name
        kwargs["extra"] = extra
        return f"{tool_name} - {msg}", kwargs


def get_tool_logger(tool_name: str) -> ToolLoggerAdapter:
    return ToolLoggerAdapter(logger, {"tool_name": tool_name})


mcp = FastMCP(
    name=settings.name,
    version=settings.version,
    instructions=settings.instructions,
    lifespan=app_lifespan,
    auth=_build_auth(),
    on_duplicate="error",
    mask_error_details=True,
)

# Middleware executes in the order added: first in, last out.
# RequestContext (outermost) assigns request_id before any logging,
# ErrorHandling catches all exceptions, Timing measures duration,
# StructuredLogging (innermost, opt-in) records MCP payloads.
mcp.add_middleware(RequestContextMiddleware())
mcp.add_middleware(ErrorHandlingMiddleware())
mcp.add_middleware(TimingMiddleware())
if settings.log_payload_enabled:
    mcp.add_middleware(StructuredLoggingMiddleware())
