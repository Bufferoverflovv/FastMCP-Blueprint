---
name: observability-setup
description: "Add production observability to a FastMCP server: request IDs, slow-request logging, structured log fields, and optional Prometheus metrics. Use when: hardening logging for production, adding request tracing or correlation IDs, setting up slow-request alerts, adding a /metrics endpoint, or improving structured log output beyond the base middleware."
argument-hint: "Optional: pass 'request-id', 'slow-requests', or 'metrics' to skip to a specific feature"
---

# Observability Setup

Adds production-grade observability features to the FastMCP server on top of the base middleware already configured in `server.py`.

## When to use

- The server is heading toward a production or staging deployment
- Logs need correlation IDs for request tracing
- Slow requests need to be flagged automatically
- A Prometheus-compatible `/metrics` endpoint is required
- The current JSON log output needs additional structured fields

## Baseline

The project already includes:
- `ErrorHandlingMiddleware` — catches unhandled exceptions
- `TimingMiddleware` — measures request duration
- `StructuredLoggingMiddleware` — JSON request logs when `LOG_FORMAT=json`

This skill adds on top of that baseline.

## Step 1 — Interview the user

Ask which features to add. Use `vscode_askQuestions` if available.

| # | Feature | What it adds |
|---|---------|-------------|
| A | **Request ID middleware** | Injects a `X-Request-ID` header and attaches it to every log record |
| B | **Slow-request logger** | Logs a warning when a request exceeds a configurable threshold (ms) |
| C | **Prometheus `/metrics` endpoint** | Exposes request count and latency histograms via `prometheus-client` |

Ask for confirmation of which to apply before making changes.

## Step 2 — Detect the package name

Read `pyproject.toml` to find `PACKAGE`.

## Step 3 — Apply: Request ID middleware (if selected)

See [./references/middleware-examples.md](./references/middleware-examples.md) for the implementation.

Changes:
- Add `RequestIDMiddleware` class to `server.py`
- Register it via `mcp.add_middleware(RequestIDMiddleware())` — place it outermost (before `ErrorHandlingMiddleware`)
- No new env vars needed

## Step 4 — Apply: Slow-request logger (if selected)

See [./references/middleware-examples.md](./references/middleware-examples.md) for the implementation.

Changes:
- Add `SlowRequestMiddleware` class to `server.py`, threshold read from config
- Add `SLOW_REQUEST_THRESHOLD_MS` field to `config.py` with default `1000`
- Add `SLOW_REQUEST_THRESHOLD_MS=1000` to `.env.example`
- Register via `mcp.add_middleware(SlowRequestMiddleware())` — place after `ErrorHandlingMiddleware`, before `TimingMiddleware`

## Step 5 — Apply: Prometheus metrics endpoint (if selected)

See [./references/middleware-examples.md](./references/middleware-examples.md) for the implementation.

Changes:
- Add `prometheus-client` to `[project.dependencies]` in `pyproject.toml`
- Create `src/PACKAGE/routes/metrics.py` with a `GET /metrics` route
- Add `from PACKAGE.routes import metrics  # noqa: F401` to `__main__.py`
- Add a `CounterMiddleware` or use `prometheus-client` multiprocess support as appropriate

## Step 6 — Validate

```bash
uv pip install -e ".[dev]"
ruff check .
pytest -v
```

Test the metrics endpoint manually if added:
```bash
fastmcp-blueprint &
curl http://localhost:8000/metrics
```

## Step 7 — Update `AGENTS.md`

Update the middleware table in the Structured logging section to document any new middleware added.

## Step 8 — Report

Tell the user what was added, which env vars are new, and how to verify each feature is working.
