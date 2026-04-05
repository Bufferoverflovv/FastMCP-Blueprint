---
name: add-route
description: "Scaffold a new FastMCP custom HTTP route following project conventions. Use when: adding a webhook endpoint, adding an admin API, creating an HTTP handler outside MCP protocol, adding a custom route, implementing a POST handler, adding route tests, or extending the server with HTTP endpoints. Asks questions then generates the route file, registers the import, and creates matching tests."
argument-hint: "Optional: pass a route path to pre-fill the first question"
---

# Add a New Custom HTTP Route

Scaffolds a fully wired custom HTTP route using the same pattern as the existing `/health` and `/ready` endpoints.

## When to use

- Adding any HTTP endpoint that lives outside the MCP protocol
- Webhooks, admin APIs, observability probes, or callback receivers
- Wanting the correct Starlette handler signature and test pattern in one step

## Step 1 — Detect the package name

Before asking questions, read `pyproject.toml` to find the current package name from:

```toml
packages = ["src/<package_name>"]
```

Use this as `PACKAGE` for all file paths and imports below.

## Step 2 — Interview the user

Ask the following questions. Use `vscode_askQuestions` if available.

| # | Question | Notes |
|---|----------|-------|
| 1 | **Route path** | e.g. `/webhook`, `/admin/reload`, `/metrics` |
| 2 | **HTTP method(s)** | GET, POST, PUT, DELETE — comma-separated |
| 3 | **What does this handler do?** | One sentence — becomes the docstring |
| 4 | **Response format** | JSON (most common), plain text, or redirect |
| 5 | **Error responses** | Which status codes and when, e.g. 400 bad input, 403 forbidden |
| 6 | **New file or existing?** | Create a new route file, or add to an existing one (list existing files) |

Derive automatically:
- `ROUTE_NAME` — snake_case name derived from the path, used for the function and file (e.g. `/admin/reload` → `admin`)
- `ROUTE_FILE` — the file to create or modify under `src/PACKAGE/routes/`

## Step 3 — Generate the route handler

Create or update `src/PACKAGE/routes/ROUTE_FILE.py` using [./assets/route_template.md](./assets/route_template.md) as the base.

Fill in:
- `@mcp.custom_route("/path", methods=["METHOD"])` decorator
- `async def HANDLER_NAME(request: Request) -> Response:` signature
- Docstring from the handler description answer
- Request body parsing if POST/PUT
- `JSONResponse` or `Response` return with correct status code
- Error response branches

See [./references/route-conventions.md](./references/route-conventions.md) for exact Starlette patterns.

## Step 4 — Register the import in `__main__.py`

Add the import line to `src/PACKAGE/__main__.py` after the existing route imports:

```python
from PACKAGE.routes import ROUTE_FILE  # noqa: F401
```

Skip this step if appending to an already-registered file.

## Step 5 — Generate the test file

Create `tests/test_ROUTE_FILE.py` using [./assets/test_template.md](./assets/test_template.md) as the base.

Include at minimum:
- One success-path test for the expected status code and response body
- One error-path test for each documented error response
- Use `httpx.ASGITransport(app=mcp.http_app())` — never use `app=` directly on `AsyncClient`

## Step 6 — Validate

```bash
ruff check .
pytest tests/test_ROUTE_FILE.py -v
```

Fix any issues before reporting completion.

## Step 7 — Report

Tell the user:
- The route path and method(s) that were registered
- The path of the new or updated route file
- The path of the new test file
- What was added to `__main__.py` (if anything)
