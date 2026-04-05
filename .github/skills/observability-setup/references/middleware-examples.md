# Middleware Examples

Reference implementations for the observability middleware options in this skill.
All code belongs in `server.py` unless otherwise noted.

---

## Request ID middleware

Generates a unique ID per request, attaches it as a response header, and injects it into log context.

```python
import uuid
from starlette.types import ASGIApp, Receive, Scope, Send


class RequestIDMiddleware:
    """Injects a unique X-Request-ID header into every request and response."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        request_id = scope["headers_dict"].get(b"x-request-id", b"").decode()
        if not request_id:
            request_id = str(uuid.uuid4())

        async def send_with_header(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append((b"x-request-id", request_id.encode()))
                message = {**message, "headers": headers}
            await send(message)

        await self.app(scope, receive, send_with_header)
```

Register **outermost** (first added):
```python
mcp.add_middleware(RequestIDMiddleware())
mcp.add_middleware(ErrorHandlingMiddleware())
# ...
```

---

## Slow-request logger

Logs a warning when a request exceeds a threshold.

Add `SLOW_REQUEST_THRESHOLD_MS` to `config.py`:
```python
slow_request_threshold_ms: int = field(
    default_factory=lambda: int(os.environ.get("SLOW_REQUEST_THRESHOLD_MS", "1000"))
)
```

Add to `.env.example`:
```env
SLOW_REQUEST_THRESHOLD_MS=1000
```

Middleware implementation in `server.py`:
```python
import time
from starlette.types import ASGIApp, Receive, Scope, Send


class SlowRequestMiddleware:
    """Logs a warning for any request that exceeds the slow-request threshold."""

    def __init__(self, app: ASGIApp, threshold_ms: int = 1000) -> None:
        self.app = app
        self.threshold_ms = threshold_ms

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.perf_counter()
        await self.app(scope, receive, send)
        elapsed_ms = (time.perf_counter() - start) * 1000

        if elapsed_ms > self.threshold_ms:
            path = scope.get("path", "unknown")
            logger.warning(
                "Slow request: %s took %.1f ms (threshold %d ms)",
                path,
                elapsed_ms,
                self.threshold_ms,
            )
```

Register after `ErrorHandlingMiddleware`, before `TimingMiddleware`:
```python
mcp.add_middleware(ErrorHandlingMiddleware())
mcp.add_middleware(SlowRequestMiddleware(threshold_ms=settings.slow_request_threshold_ms))
mcp.add_middleware(TimingMiddleware())
```

---

## Prometheus metrics endpoint

Add `prometheus-client` to `pyproject.toml`:
```toml
dependencies = [
    "fastmcp~=3.1",
    "python-dotenv~=1.2",
    "prometheus-client~=0.21",
]
```

Create `src/PACKAGE/routes/metrics.py`:
```python
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.requests import Request
from starlette.responses import Response

from PACKAGE.server import mcp


@mcp.custom_route("/metrics", methods=["GET"])
async def prometheus_metrics(request: Request) -> Response:
    """Expose Prometheus metrics for scraping."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
```

Register in `__main__.py`:
```python
from PACKAGE.routes import metrics  # noqa: F401
```

To track tool call counts, add a counter in each tool:
```python
from prometheus_client import Counter

TOOL_CALLS = Counter("mcp_tool_calls_total", "Total tool calls", ["tool_name"])

@mcp.tool()
async def my_tool(...):
    TOOL_CALLS.labels(tool_name="my_tool").inc()
    ...
```
