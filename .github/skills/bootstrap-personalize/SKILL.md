---
name: bootstrap-personalize
description: "Personalize and rename this FastMCP-Blueprint template into a real project. Use when: bootstrapping a new MCP server from this template, renaming the package or CLI command, customizing the server name/description, choosing an auth mode, removing sample/placeholder code, or setting up a project for real use. Asks questions then updates pyproject.toml, package paths, config.py, server.py, __main__.py, .env.example, README, and AGENTS docs consistently."
argument-hint: "Optional: pass a project name to pre-fill the first question"
---

# Bootstrap and Personalize the Blueprint

Transforms this FastMCP-Blueprint template into a project-specific MCP server by asking a short set of questions and then updating every relevant file consistently.

## When to use

- First time setting up this template for a real project
- Renaming the package, CLI command, or display name
- Changing the MCP server description or default instructions
- Enabling or disabling auth in the base configuration
- Removing the `hello_world` sample tool once real tools exist

## Step 1 — Interview the user

Ask the following questions. Wait for all answers before making any changes. Use the `vscode_askQuestions` tool if available.

| # | Question | Default |
|---|----------|---------|
| 1 | **Project display name** — shown in README, pyproject.toml, and MCP identity | `FastMCP-Blueprint` |
| 2 | **Python package name** — `src/<pkg>/` folder, imports, hatchling config (snake_case) | `fastmcp_blueprint` |
| 3 | **CLI command name** — entry point in pyproject.toml (kebab-case) | `fastmcp-blueprint` |
| 4 | **Short description** — one sentence for pyproject.toml `description` field | current value |
| 5 | **MCP server instructions** — natural-language description the LLM sees at runtime | `This server provides MCP tools and resources.` |
| 6 | **Auth mode** — `disabled`, `remote`, or `oauth_proxy` | `disabled` |
| 7 | **Remove hello_world sample tool?** — yes or no | `no` |

Derive these automatically from the answers:
- `PACKAGE_NAME` — snake_case version of the Python package name
- `CLI_NAME` — kebab-case CLI command
- `CLASS_OR_IMPORT_PREFIX` — matches the package name in all `from fastmcp_blueprint...` imports

## Step 2 — Confirm before changing

Show the user a summary table of every change that will be made. Ask for confirmation before proceeding.

Example summary:

```
Display name:   FastMCP-Blueprint  →  My Weather MCP
Package name:   fastmcp_blueprint  →  my_weather_mcp
CLI command:    fastmcp-blueprint  →  my-weather-mcp
Description:    A FastMCP blueprint…  →  Provides real-time weather data via MCP.
Instructions:   This server provides…  →  You can ask me about weather conditions…
Auth:           disabled  →  disabled
Remove sample:  no  →  yes
```

## Step 3 — Apply changes

Consult [./references/file-substitutions.md](./references/file-substitutions.md) for the exact list of substitutions and which files to update.

Apply changes in this order to avoid import-before-rename problems:

1. Rename the package directory using the terminal:
   ```bash
   mv src/CURRENT_PACKAGE_NAME src/NEW_PACKAGE_NAME
   ```
   Only do this if the package name is actually changing.

2. Update `pyproject.toml`
3. Update `src/<pkg>/__main__.py`
4. Update `src/<pkg>/config.py`
5. Update `src/<pkg>/server.py`
6. Update `src/<pkg>/tools/hello_world.py` and its imports
7. Update `src/<pkg>/routes/health.py` and its imports
8. Update `tests/conftest.py`
9. Update all other test files
10. Update `.env.example`
11. Update `Dockerfile` — replace the CLI command in the `CMD` instruction
12. Update `README.md`
13. Update `AGENTS.md`

## Step 4 — Handle the hello_world tool

If the user asked to remove the sample tool:
- Delete `src/<pkg>/tools/hello_world.py`
- Delete `tests/test_hello_world.py`
- Remove its import from `__main__.py`
- Remove it from `tests/conftest.py`
- Add a placeholder comment in `__main__.py` where it was imported

If the user wants to keep it, leave it untouched.

## Step 5 — Handle auth mode

If auth mode is `disabled` (the default), make no changes to server.py or config.py beyond normal renames.

If auth mode is `remote` or `oauth_proxy`:
- Uncomment the relevant `AUTH_PROVIDER` block in `.env.example`
- Add a note in `README.md` pointing to the auth section
- Leave the wiring in `server.py` as-is; it already handles both modes

## Step 6 — Validate

After applying all changes, run the following and confirm they pass:

```bash
ruff check .
ruff format --check .
pytest -v
```

Fix any import errors or test failures caused by the renames before declaring the workflow complete.

## Step 7 — Report results

Tell the user:
- Which files were changed
- Whether tests passed
- What the next step is (for example: add your first tool, see `add-tool`)
