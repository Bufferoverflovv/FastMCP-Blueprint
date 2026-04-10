# FastMCP Blueprint

[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1%2B-0A7B83)](https://gofastmcp.com/)
[![Ruff](https://img.shields.io/badge/lint%20%26%20format-ruff-D7FF64?logo=ruff&logoColor=111111)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![License](https://img.shields.io/badge/license-Apache%202.0-orange.svg)](LICENSE)

FastMCP-Blueprint is a minimal but production-aware starting point for building Model Context Protocol servers with [FastMCP](https://gofastmcp.com/).

It gives you a clean `src`-layout Python package, environment-based configuration, a runnable HTTP server, health endpoints, a sample tool, local TLS support, optional authentication wiring, tests, Ruff, and pre-commit hooks without forcing extra application structure on day one.

## What this template includes

- FastMCP server package under `src/fastmcp_blueprint`
- CLI entry point: `fastmcp-blueprint`
- Environment-driven configuration loaded from `.env`
- Sample `hello_world` tool
- `/health` and `/ready` HTTP endpoints
- Optional auth wiring for `remote` and `oauth_proxy`
- Structured JSON logging with request correlation and optional MCP payload logging
- Local TLS certificate generation for development
- In-memory test setup using FastMCP's client
- Ruff formatting and linting with pre-commit integration

## Project layout

```text
src/fastmcp_blueprint/
├── __main__.py          # CLI entry point and server startup
├── config.py            # Environment-backed settings
├── logging_setup.py     # JSON logging formatter, filters, and request context
├── server.py            # FastMCP instance, auth, lifespan, and middleware wiring
├── resources/           # MCP resources
├── routes/              # Custom HTTP routes like health checks
└── tools/               # MCP tools

tests/                   # In-memory tool and HTTP route tests
scripts/generate_cert.py # Local TLS certificate generator
```

## Requirements

- Python 3.13+
- [`uv`](https://github.com/astral-sh/uv) recommended for environment and dependency management

## Quick start

Create a virtual environment, install the project with development dependencies, and create a local `.env` file:

```bash
uv venv .venv --python 3.13
source .venv/bin/activate
uv pip install -e ".[dev]"
cp .env.example .env
```

Run the server:

```bash
fastmcp-blueprint
```

By default the server starts on `localhost:8000` over HTTP.

## Docker

The repository includes a production-oriented `Dockerfile` for packaging the server as a container image.

Build the image:

```bash
docker build -t fastmcp-blueprint .
```

Run the container:

```bash
docker run --rm -p 8000:8000 fastmcp-blueprint
```

Pass configuration through environment variables the same way you would locally:

```bash
docker run --rm -p 8000:8000 \
  --env-file .env \
	fastmcp-blueprint
```

The image exposes port `8000`, runs as a non-root user, and uses the built-in `GET /health` endpoint for the container health check.

If you enable TLS, mount your certificate files into the container and pass the corresponding CLI flags or environment variables.

## Configuration

Configuration is loaded from environment variables and `.env` through `python-dotenv`.

### Core server settings

```env
HOST=localhost
PORT=8000
LOG_LEVEL=INFO
LOG_FORMAT=rich
#LOG_PAYLOAD_ENABLED=false
#SSL_CERTFILE=server.pem
#SSL_KEYFILE=
```

### MCP identity settings

```env
NAME=FastMCP-Blueprint
VERSION=0.2.0
INSTRUCTIONS=This server provides MCP tools and resources.
```

### Supported log formats

- `rich`: FastMCP's default developer-friendly terminal logging
- `plain`: plain text log output
- `json`: JSON-formatted Python logs with FastMCP request logging routed through the same handler

### Payload logging

`LOG_PAYLOAD_ENABLED` controls whether FastMCP's `StructuredLoggingMiddleware` is enabled.

- `false` (default): JSON mode still emits structured startup, tool, auth, and server logs, but MCP request payloads are not logged.
- `true`: enables `StructuredLoggingMiddleware` so MCP request/response metadata and payload-level events are logged too.

Keep payload logging disabled unless the environment is allowed to record tool arguments, resource contents, and similar request data.

## Running with TLS locally

Generate a local certificate for HTTPS development:

```bash
source .venv/bin/activate
python scripts/generate_cert.py
```

This writes:

- `server.pem`: combined private key and certificate chain for the server
- `server-ca.pem`: local certificate authority certificate for trust installation

The generator includes `localhost`, `127.0.0.1`, and `::1` by default. Add extra hostnames if needed:

```bash
python scripts/generate_cert.py --hostname dev.local --hostname 192.168.1.10
```

Then enable TLS in `.env` or on the command line:

```env
SSL_CERTFILE=server.pem
```

Run the server:

```bash
fastmcp-blueprint
```

If your key lives in a separate file, also set `SSL_KEYFILE`.

## CLI options

The CLI exposes common runtime settings directly:

```bash
fastmcp-blueprint --host 0.0.0.0 --port 9000 --log-level DEBUG
```

Available flags:

- `--host`
- `--port`
- `--ssl-certfile`
- `--ssl-keyfile`
- `--log-level`

## Included MCP and HTTP endpoints

### Sample tool

The template includes a simple `hello_world` tool to verify end-to-end wiring:

```text
hello_world(name="World") -> "Hello, World!"
```

This lives in `src/fastmcp_blueprint/tools/hello_world.py` and is registered by importing the module in `__main__.py`.

### Health routes

Two custom HTTP routes are included:

- `GET /health`: liveness probe, returns `{"status": "ok"}`
- `GET /ready`: readiness probe, verifies that tools are registered

These routes are useful for container probes and deployment checks.

## Authentication

Authentication is disabled by default.

To enable it, set `AUTH_PROVIDER` in `.env` to one of:

- `remote`: for providers that support dynamic client registration and protected resource metadata
- `oauth_proxy`: for upstream providers such as GitHub, Google, or Azure that do not support DCR directly

### Shared auth settings

Both auth modes use these settings:

```env
#AUTH_JWKS_URI=https://your-auth-server.com/.well-known/jwks.json
#AUTH_ISSUER=https://your-auth-server.com
#AUTH_AUDIENCE=your-mcp-server
#AUTH_BASE_URL=https://your-mcp-server.com
```

### Remote auth

```env
AUTH_PROVIDER=remote
```

This configures `RemoteAuthProvider` with JWT verification.

### OAuth proxy auth

```env
AUTH_PROVIDER=oauth_proxy
#OAUTH_UPSTREAM_AUTHORIZE_URL=https://provider.com/oauth/authorize
#OAUTH_UPSTREAM_TOKEN_URL=https://provider.com/oauth/token
#OAUTH_CLIENT_ID=
#OAUTH_CLIENT_SECRET=
```

This configures `OAuthProxy` plus JWT verification.

## Development workflow

Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

Run tests:

```bash
pytest -v
```

Run Ruff manually:

```bash
ruff format .
ruff check .
```

Install and use pre-commit hooks:

```bash
pre-commit install
pre-commit run --all-files
```

The repository includes Ruff pre-commit hooks for linting and formatting.

## Testing approach

Tests use FastMCP's in-memory client rather than subprocess or network-heavy integration tests.

- Tool tests call the server through `fastmcp.client.Client`
- Route tests use `httpx.ASGITransport` against `mcp.http_app()`
- Config tests validate default values and environment overrides

This keeps the template fast to iterate on while still exercising real framework behavior.

## Logging and middleware

The server includes:

- `RequestContextMiddleware`
- `ErrorHandlingMiddleware`
- `TimingMiddleware`
- `StructuredLoggingMiddleware` when `LOG_PAYLOAD_ENABLED=true`

The logging implementation lives in `src/fastmcp_blueprint/logging_setup.py`.

When `LOG_FORMAT=json`:

- all Python log records routed through the `fastmcp` logger hierarchy are formatted as single-line JSON
- `uvicorn`, `fastmcp`, and `fastmcp_blueprint` logs share the same JSON handler
- each MCP request receives a `request_id` correlation field
- common secrets such as bearer tokens, JWTs, and `api_key=` style assignments are scrubbed before emission

For tool-level logs, use `get_tool_logger("tool_name")` from `server.py` so logs include structured tool context.

## Copilot skills for extending the blueprint

This repository includes reusable Copilot skills under `.github/skills/` that help you evolve the template without rebuilding the same scaffolding by hand.

- `add-tool`: scaffold a new FastMCP tool module plus matching tests.
- `add-resource`: scaffold a new MCP resource and its tests.
- `add-route`: scaffold a custom HTTP route and route tests.
- `test-scaffold`: generate missing tests for an existing tool, resource, or route.
- `docs-sync`: check whether `README.md`, `AGENTS.md`, and registration imports still match the codebase.
- `auth-setup`: enable and document `remote` or `oauth_proxy` authentication.
- `observability-setup`: add request correlation, slow-request logging, and optional metrics.
- `deployment-profile`: generate deployment-oriented assets such as container and reverse-proxy configuration.
- `bootstrap-personalize`: turn the blueprint into a real project by renaming and customizing the package, CLI, and docs.
- `rename-project`: safely rename an already-customized project without missing entry points or package references.
- `release-readiness`: audit the repository before publishing or sharing it more broadly.

These skills are most useful once you move past the sample `hello_world` tool and start shaping the template around a real MCP server. They encode the conventions documented in `AGENTS.md`, including module registration in `__main__.py`, FastMCP decorator usage, and the test structure used in this repo.

## Extending the template

Typical next steps when starting a real project:

1. Replace the sample `hello_world` tool with your domain tools.
2. Add MCP resources under `src/fastmcp_blueprint/resources`.
3. Expand `app_lifespan` in `server.py` to initialize shared clients or database pools.
4. Tighten authentication settings if your server should not run anonymously.
5. Add project-specific tests around your tools, resources, and routes.

## Release and packaging

This project is packaged with Hatchling and exposes the console script:

```bash
fastmcp-blueprint
```

The Python package name is `fastmcp_blueprint`, and the distribution name is `FastMCP-Blueprint`.

## Related files

- `AGENTS.md` documents FastMCP conventions used in this blueprint
- `.env.example` shows all supported environment variables
- `scripts/generate_cert.py` generates local development TLS certificates

## License

Apache 2.0. See `LICENSE` for details.
