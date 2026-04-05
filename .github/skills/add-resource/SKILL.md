---
name: add-resource
description: "Scaffold a new FastMCP resource following project conventions. Use when: adding a read-only data source, exposing structured or binary content via MCP, creating a resource URI, implementing a static or templated resource endpoint, or adding resource tests. Asks questions then generates the resource file, registers the import, and creates matching tests."
argument-hint: "Optional: pass a resource name or URI to pre-fill the first questions"
---

# Add a New FastMCP Resource

Scaffolds a fully wired FastMCP resource in the correct location following the conventions already used in this project.

## When to use

- Adding any MCP resource that exposes read-only data to the LLM
- Wanting the correct URI pattern, return contract, and error handling in one step
- Unsure about static vs. templated resources or how to serialize return values

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
| 1 | **Resource URI** | e.g. `resource://config`, `resource://user/{user_id}` |
| 2 | **Resource name** | snake_case identifier, used for the function and file name |
| 3 | **What does this resource expose?** | One sentence — becomes the docstring |
| 4 | **Static or templated?** | Static: fixed URI. Templated: URI contains `{param}` segments |
| 5 | **Return type** | plain text (`str`), binary (`bytes`), or structured data (JSON string) |
| 6 | **MIME type** | e.g. `text/plain`, `application/json`, `image/png` (leave blank for default) |
| 7 | **What should raise a ResourceError?** | e.g. item not found, invalid ID, upstream failure |

Derive automatically:
- If the URI contains `{param}` segments, this is a **template resource** — use `@mcp.resource("uri")` with matching function parameters
- File name: `RESOURCE_NAME.py` under `src/PACKAGE/resources/`

## Step 3 — Generate the resource file

Create `src/PACKAGE/resources/RESOURCE_NAME.py` using [./assets/resource_template.md](./assets/resource_template.md) as the base.

Fill in:
- `@mcp.resource("URI")` with the full URI
- Function signature — include path params as typed arguments for templated resources
- Docstring from the resource description answer
- Return type annotation (`str` or `bytes`)
- `mime_type=` argument if non-default
- `ResourceError` raises for stated error cases
- Actual data retrieval or construction logic

See [./references/resource-conventions.md](./references/resource-conventions.md) for exact patterns.

## Step 4 — Register the import in `__main__.py`

Add the import line to `src/PACKAGE/__main__.py` after any existing resource imports:

```python
from PACKAGE.resources import RESOURCE_NAME  # noqa: F401
```

Keep `# noqa: F401` — the import exists only for side-effect registration.

## Step 5 — Generate the test file

Create `tests/test_RESOURCE_NAME.py` using [./assets/test_template.md](./assets/test_template.md) as the base.

Include at minimum:
- A success-path test reading the resource via `await client.read_resource("URI")`
- An error-path test for invalid or missing parameters (templated resources)
- For structured data: parse and assert specific fields, not just status

## Step 6 — Validate

```bash
ruff check .
pytest tests/test_RESOURCE_NAME.py -v
```

Fix any issues before reporting completion.

## Step 7 — Report

Tell the user:
- The path of the new resource file
- The path of the new test file
- What was added to `__main__.py`
- The full URI to use when reading the resource with an MCP client
