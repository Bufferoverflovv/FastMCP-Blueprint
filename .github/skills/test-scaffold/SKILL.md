---
name: test-scaffold
description: "Generate tests for an existing FastMCP tool, resource, or custom route. Use when: adding missing tests, improving test coverage, writing tests for a tool that has none, scaffolding route tests, adding error-path tests, or creating tests for a resource URI. Detects the module type and generates correctly structured tests without the user needing to remember fixture or assertion patterns."
argument-hint: "Optional: pass a tool name, resource URI, or route path to skip the first question"
---

# Scaffold Tests for an Existing Module

Generates correctly structured pytest tests for a tool, resource, or custom route already present in the codebase, using the exact patterns established in this project.

## When to use

- A tool, resource, or route exists but has no test file
- An existing test file is missing error-path or edge-case coverage
- Unsure about fixture usage, assertion patterns, or how to test error responses

## Step 1 — Detect the package name

Read `pyproject.toml` to find the current `PACKAGE` name.

## Step 2 — Interview the user

Ask the following questions. Use `vscode_askQuestions` if available.

| # | Question | Notes |
|---|----------|-------|
| 1 | **What to test?** | Tool name, resource URI (e.g. `resource://config`), or route path (e.g. `/health`) |
| 2 | **Module type** | Auto-detect from the answer: tool → `tools/`, URI → `resources/`, path → `routes/`. Ask if ambiguous |
| 3 | **Does a test file already exist?** | Check `tests/test_<name>.py`; if yes, ask whether to append or create a companion file |
| 4 | **What scenarios to cover?** | Ask the user to list them, or offer a default set based on module type |
| 5 | **Include edge cases?** | Empty/null input, type errors, not-found, auth failure (optional) |

## Step 3 — Read the source module

Read the source file to understand:
- Function/handler signature and parameter names
- Return type and error cases (`ToolError`, `ResourceError`, status codes)
- Default parameter values for optional arguments

## Step 4 — Generate the test file

Use [./references/test-patterns.md](./references/test-patterns.md) for the exact assertion and fixture patterns for each module type.

**Tool test file** → `tests/test_TOOL_NAME.py`
- Success path with a representative input
- Default parameter path (if any parameters have defaults)
- Error path using `raise_on_error=False` and asserting `result.is_error`
- Uses the shared `client` fixture from `conftest.py`

**Resource test file** → `tests/test_RESOURCE_NAME.py`
- Success path reading the resource URI
- JSON field assertion for structured resources
- Not-found error path for templated resources using `pytest.raises(McpError)`

**Route test file** → `tests/test_ROUTE_NAME.py`
- Success path asserting status code and response body
- Error path for each documented error response
- Uses `httpx.ASGITransport(app=mcp.http_app())` — import the route module for side effects

## Step 5 — Validate

```bash
ruff check .
pytest tests/test_<name>.py -v
```

Fix any issues before reporting completion.

## Step 6 — Report

Tell the user:
- The test file path
- How many test cases were generated
- Any scenarios that could not be auto-generated and require manual implementation
