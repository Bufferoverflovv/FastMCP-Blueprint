import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

# Load .env file if present (does not override existing env vars)
load_dotenv()


@dataclass(frozen=True)
class ServerConfig:
    """MCP server configuration loaded from environment variables."""

    host: str = field(default_factory=lambda: os.environ.get("HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.environ.get("PORT", "8000")))
    log_level: str = field(default_factory=lambda: os.environ.get("LOG_LEVEL", "INFO"))
    log_format: str = field(default_factory=lambda: os.environ.get("LOG_FORMAT", "rich"))
    log_payload_enabled: bool = field(
        default_factory=lambda: os.environ.get("LOG_PAYLOAD_ENABLED", "").lower() in ("true", "1")
    )
    ssl_certfile: str | None = field(default_factory=lambda: os.environ.get("SSL_CERTFILE") or None)
    ssl_keyfile: str | None = field(default_factory=lambda: os.environ.get("SSL_KEYFILE") or None)

    name: str = field(default_factory=lambda: os.environ.get("NAME", "FastMCP-Blueprint"))
    version: str = field(default_factory=lambda: os.environ.get("VERSION", "0.2.0"))
    instructions: str = field(
        default_factory=lambda: os.environ.get(
            "INSTRUCTIONS",
            "This server provides MCP tools and resources.",
        )
    )

    # Auth — set AUTH_PROVIDER to "remote" or "oauth_proxy" to enable
    auth_provider: str = field(default_factory=lambda: os.environ.get("AUTH_PROVIDER", ""))

    # Remote auth (AUTH_PROVIDER=remote) — JWT verification + DCR discovery
    auth_jwks_uri: str = field(default_factory=lambda: os.environ.get("AUTH_JWKS_URI", ""))
    auth_issuer: str = field(default_factory=lambda: os.environ.get("AUTH_ISSUER", ""))
    auth_audience: str = field(default_factory=lambda: os.environ.get("AUTH_AUDIENCE", ""))
    auth_base_url: str = field(default_factory=lambda: os.environ.get("AUTH_BASE_URL", ""))

    # OAuth Proxy (AUTH_PROVIDER=oauth_proxy) — for GitHub, Google, Azure, etc.
    oauth_upstream_authorize_url: str = field(
        default_factory=lambda: os.environ.get("OAUTH_UPSTREAM_AUTHORIZE_URL", "")
    )
    oauth_upstream_token_url: str = field(
        default_factory=lambda: os.environ.get("OAUTH_UPSTREAM_TOKEN_URL", "")
    )
    oauth_client_id: str = field(default_factory=lambda: os.environ.get("OAUTH_CLIENT_ID", ""))
    oauth_client_secret: str = field(
        default_factory=lambda: os.environ.get("OAUTH_CLIENT_SECRET", "")
    )

    def validate(self) -> None:
        """Validate configuration."""
        valid_formats = ("rich", "plain", "json")
        if self.log_format not in valid_formats:
            raise ValueError(
                f"LOG_FORMAT must be one of {', '.join(valid_formats)}, got '{self.log_format}'"
            )
        valid_auth = ("", "remote", "oauth_proxy")
        if self.auth_provider not in valid_auth:
            raise ValueError(
                f"AUTH_PROVIDER must be one of {', '.join(repr(v) for v in valid_auth)}, "
                f"got '{self.auth_provider}'"
            )

    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Create config from environment variables and validate."""
        config = cls()
        config.validate()
        return config


settings = ServerConfig.from_env()
