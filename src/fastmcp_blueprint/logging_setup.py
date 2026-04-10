import json
import logging
import re
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone

from fastmcp.server.middleware.middleware import Middleware

request_id_var: ContextVar[str] = ContextVar("request_id", default="")
auth_client_id_var: ContextVar[str] = ContextVar("auth_client_id", default="")

_BEARER_RE = re.compile(r"(Bearer\s+)\S+", re.IGNORECASE)
_JWT_RE = re.compile(r"\b[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\b")
_SECRET_ASSIGN_RE = re.compile(
    r"((?:api_key|password|secret|token|authorization|credential|private_key)"
    r"\s*[=:]\s*)['\"]?\S+['\"]?",
    re.IGNORECASE,
)
_REDACTED = "[REDACTED]"


class _SecretScrubFilter(logging.Filter):
    """Redacts secrets from log records before any handler sees them."""

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        scrubbed = _BEARER_RE.sub(r"\1" + _REDACTED, msg)
        scrubbed = _JWT_RE.sub(_REDACTED, scrubbed)
        scrubbed = _SECRET_ASSIGN_RE.sub(r"\1" + _REDACTED, scrubbed)
        if scrubbed != msg:
            record.msg = scrubbed
            record.args = None
        return True


class _RequestContextFilter(logging.Filter):
    """Injects request-scoped values from context vars into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get("")  # type: ignore[attr-defined]
        record.auth_client_id = auth_client_id_var.get("")  # type: ignore[attr-defined]
        return True


class _JsonLogFormatter(logging.Formatter):
    """Formats log records as single-line JSON with ISO 8601 UTC timestamps."""

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(
            timespec="milliseconds"
        )
        entry: dict[str, object] = {
            "timestamp": ts,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        request_id = getattr(record, "request_id", "")
        if request_id:
            entry["request_id"] = request_id

        auth_client_id = getattr(record, "auth_client_id", "")
        if auth_client_id:
            entry["auth_client_id"] = auth_client_id

        tool = getattr(record, "tool", None)
        if tool:
            entry["tool"] = tool

        if record.exc_info and record.exc_info[1]:
            entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(entry, default=str)


class RequestContextMiddleware(Middleware):
    """Assigns a request ID before downstream middleware emits logs."""

    async def on_message(self, context, call_next):
        request_id_var.set(uuid.uuid4().hex)
        return await call_next(context)


def install_json_handler(package_logger_name: str = "fastmcp_blueprint") -> None:
    """Route FastMCP and application log records through one JSON handler."""
    fastmcp_logger = logging.getLogger("fastmcp")
    fastmcp_logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(_JsonLogFormatter())
    fastmcp_logger.addHandler(handler)

    fastmcp_logger.addFilter(_SecretScrubFilter())
    fastmcp_logger.addFilter(_RequestContextFilter())

    package_logger = logging.getLogger(package_logger_name)
    package_logger.parent = fastmcp_logger
    package_logger.propagate = True


def route_uvicorn_to_fastmcp() -> None:
    """Reparent uvicorn loggers under ``fastmcp`` for consistent formatting."""
    fastmcp_logger = logging.getLogger("fastmcp")
    for name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.parent = fastmcp_logger
        uvicorn_logger.propagate = True