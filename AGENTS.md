# FastMCP-Blueprint Environment

Blueprint project for developing MCP services with [FastMCP](https://gofastmcp.com/).

Refer to the [FastMCP documentation](https://gofastmcp.com/) for framework details. Key pages:
- [Tools](https://gofastmcp.com/servers/tools) — defining LLM-callable actions
- [Resources](https://gofastmcp.com/servers/resources) — exposing read-only data
- [Prompts](https://gofastmcp.com/servers/prompts) — reusable prompt templates
- [Auth](https://gofastmcp.com/servers/auth) — authentication providers
- [Testing](https://gofastmcp.com/servers/testing) — in-memory client testing
- [Composition](https://gofastmcp.com/pattern/composition) — mounting sub-servers

## Project layout

This project uses the Python `src` layout with packages organized by MCP concept:

```
src/fastmcp_blueprint/
├── __main__.py          # Entry point (python -m fastmcp_blueprint or fastmcp-blueprint CLI)
├── config.py            # Configuration loaded from environment variables / .env
├── server.py            # FastMCP instance, auth provider, tool logger
├── tools/               # @mcp.tool() — LLM-callable actions (one file per tool)
├── resources/           # @mcp.resource() — read-only data for LLMs
├── routes/              # @mcp.custom_route() — HTTP endpoints outside MCP protocol
└── utils/               # Shared helpers (response formatting, etc.)
```

## Development workflow

```bash
uv venv .venv --python 3.13
source .venv/bin/activate
uv pip install -e ".[dev]"
cp .env.example .env        # Configure environment variables
pre-commit install           # Enable ruff hooks

# Optional: generate a local TLS certificate for HTTPS development
python scripts/generate_cert.py
```

Run the server: `fastmcp-blueprint --ssl-certfile server.pem`

## FastMCP conventions

Follow these conventions from the FastMCP framework when adding tools, resources, or prompts.

### Tools (`@mcp.tool`)

- The function name becomes the tool name, the docstring becomes its description for the LLM
- Use descriptive snake_case action-oriented names (e.g., `resolve_dns_record_a`, `verify_url_status`)
- All parameters must have type annotations — no `*args` or `**kwargs`
- Use `Annotated[str, "description"]` or `Annotated[int, Field(ge=1, description="...")]` for parameter documentation and validation
- Both `def` and `async def` are supported; prefer `async def` for I/O-bound work
- Raise `ToolError` from `fastmcp.exceptions` for client-facing error messages — standard exceptions are masked in production
- Add `ctx: Context` parameter to access logging (`ctx.info()`), progress reporting (`ctx.report_progress()`), and resource reading
- Set `readOnlyHint=True` on read-only tools, `destructiveHint=True` on destructive operations

### Resources (`@mcp.resource`)

- The URI is the first argument: `@mcp.resource("resource://networks")`
- Use `{param}` in URIs for templates: `@mcp.resource("resource://user/{user_id}")`
- Return `str` for text, `bytes` for binary (set `mime_type=`), or `json.dumps()` for structured data — never return raw dicts
- Raise `ResourceError` from `fastmcp.exceptions` for client-facing errors

### Custom routes (`@mcp.custom_route`)

- For HTTP endpoints outside the MCP protocol (health checks, webhooks, admin APIs)
- Handler must be `async def` accepting a Starlette `Request` and returning a `Response`

### General

- Never hardcode URLs, secrets, or environment-specific values — use `config.py` and `.env`
- Each new module must be imported in `__main__.py` for its decorators to register with FastMCP
- Use `get_tool_logger("tool_name")` from `server.py` for tool-specific logging
- `on_duplicate="error"` — the server raises on duplicate tool/resource registration instead of silently warning
- `mask_error_details=True` — internal error details are hidden from clients; use `ToolError` for client-facing messages
- The `app_lifespan` in `server.py` handles server startup/teardown; add shared resources (DB pools, HTTP clients) there and access them via `ctx.lifespan_context` in tools
- Start with the minimal server configuration in `.env.example`; add auth settings only if you extend the bootstrap to require them

## Auth

Authentication is disabled by default. Set `AUTH_PROVIDER` in `.env` to enable one of two modes:

| `AUTH_PROVIDER` | Use case | FastMCP class | Docs |
|-----------------|----------|---------------|------|
| `remote` | Identity providers with DCR (WorkOS AuthKit, Descope) | `RemoteAuthProvider` + `JWTVerifier` | [Remote OAuth](https://gofastmcp.com/servers/auth/remote-oauth) |
| `oauth_proxy` | Providers without DCR (GitHub, Google, Azure) | `OAuthProxy` + `JWTVerifier` | [OAuth Proxy](https://gofastmcp.com/servers/auth/oauth-proxy) |

Both modes share `AUTH_JWKS_URI`, `AUTH_ISSUER`, `AUTH_AUDIENCE`, and `AUTH_BASE_URL`. The OAuth Proxy additionally requires `OAUTH_UPSTREAM_AUTHORIZE_URL`, `OAUTH_UPSTREAM_TOKEN_URL`, `OAUTH_CLIENT_ID`, and `OAUTH_CLIENT_SECRET`.

Auth wiring lives in `_build_auth()` in `server.py`. Imports are deferred so no auth dependencies are loaded when auth is disabled.

## Testing

```bash
pytest -v
```

- Tests use FastMCP's in-memory `Client(mcp)` transport — no stubs or mocks of framework internals
- pytest-asyncio with `asyncio_mode = "auto"` — async tests need no decorator
- The `client` fixture in `conftest.py` provides a connected MCP client
- Call tools: `result = await client.call_tool("tool_name", {"param": "value"})`
- Parse results: `data = json.loads(result.content[0].text)`
- Use `raise_on_error=False` when testing error paths
- Each tool has a dedicated test file with success and failure cases

## Structured logging

Set `LOG_FORMAT` to control output: `rich` (default), `plain`, or `json`.

In JSON mode, FastMCP's built-in `StructuredLoggingMiddleware` is added to the server (see `server.py`). It emits structured JSON lines for every MCP request/response — tool calls, resource reads, etc. — suitable for aggregation tools like Datadog, Splunk, or ELK.

Middleware log fields (emitted per MCP request):

| Field | Description |
|-------|-------------|
| `event` | Lifecycle phase (`request_start`, `request_success`, `request_error`) |
| `method` | MCP method (e.g., `tools/call`, `resources/read`) |
| `source` | Origin (`client` or `server`) |
| `duration_ms` | Request duration in milliseconds (on completion/error) |
| `error` | Error message (on error only) |

For in-tool application logs, use `get_tool_logger("tool_name")` from `server.py` — this attaches the `tool` field to log records via `ToolLoggerAdapter`.

**Sample middleware JSON log:**

```json
{"event": "request_start", "method": "tools/call", "source": "client"}
{"event": "request_success", "method": "tools/call", "source": "client", "duration_ms": 1.23}
```

When adding new tools, always use `get_tool_logger("tool_name")` — this ensures the `tool` field is present in application-level structured logs.

## Code style

- Python 3.13+, line length 100, ruff for linting and formatting
- Pre-commit hooks enforce ruff on every commit
- Stage all changes before committing to avoid pre-commit stash conflicts

## Key files

- `pyproject.toml` — build config (hatchling), dependencies, tool settings
- `.env.example` — all available environment variables with descriptions
- `scripts/generate_cert.py` — generates self-signed SSL certs for local dev
