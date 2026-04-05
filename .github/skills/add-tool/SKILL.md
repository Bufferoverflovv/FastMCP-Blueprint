---
name: add-tool
description: "Scaffold a new FastMCP tool following project conventions. Use when: adding a new tool, creating an LLM-callable action, implementing a new MCP tool endpoint, adding tool tests, or extending the server with a new capability. Asks questions then generates the tool file, registers the import, and creates matching tests."
argument-hint: "Optional: pass a tool name to pre-fill the first question"
---

# Add a New FastMCP Tool

Scaffolds a fully wired FastMCP tool in the correct location following the conventions already used in this project.

## When to use

- Adding any new MCP tool to the server
- Wanting a correctly structured tool file and matching tests in one step
- Unsure about parameter annotations, error handling, or async patterns

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
| 1 | **Tool name** | snake_case, action-oriented (e.g. `fetch_weather`, `resolve_dns_record`) |
| 2 | **What does this tool do?** | One sentence — becomes the docstring |
| 3 | **Parameters** | Name, type, description for each. Ask one at a time if unclear |
| 4 | **Sync or async?** | Default: async for any I/O, sync for pure computation |
| 5 | **Read-only or destructive?** | Read-only → add `readOnlyHint=True`; destructive → add `destructiveHint=True` |
| 6 | **What should raise a ToolError?** | e.g. invalid input, network failure, resource not found |
| 7 | **Does it need external I/O?** | If yes, suggest adding an HTTP client or DB pool via `app_lifespan` |

## Step 3 — Generate the tool file

Create `src/PACKAGE/tools/TOOL_NAME.py` using [./assets/tool_template.md](./assets/tool_template.md) as the base.

Fill in:
- The import block (`sync` or `async` variant)
- `@mcp.tool()` decorator with hints if applicable
- Function signature with all `Annotated` parameters
- Docstring from the tool description answer
- Logger call using `get_tool_logger("TOOL_NAME")`
- Return type annotation
- `ToolError` raises for the stated error cases

See [./references/tool-conventions.md](./references/tool-conventions.md) for exact patterns.

## Step 4 — Register the import in `__main__.py`

Add the import line to `src/PACKAGE/__main__.py` after the existing tool imports:

```python
from PACKAGE.tools import TOOL_NAME  # noqa: F401
```

Keep the `# noqa: F401` comment — the import is intentional for side-effect registration.

## Step 5 — Generate the test file

Create `tests/test_TOOL_NAME.py` using [./assets/test_template.md](./assets/test_template.md) as the base.

Include at minimum:
- A success-path test using `await client.call_tool("TOOL_NAME", {...})`
- An error-path test using `raise_on_error=False` and asserting `result.is_error`
- A test for any default parameter values if applicable

## Step 6 — Validate

Run and confirm both pass:

```bash
ruff check .
pytest tests/test_TOOL_NAME.py -v
```

Fix any issues before reporting completion.

## Step 7 — Report

Tell the user:
- The path of the new tool file
- The path of the new test file
- What was added to `__main__.py`
- Any suggestions for next steps (e.g. if the tool needs `lifespan` context for an HTTP client)
