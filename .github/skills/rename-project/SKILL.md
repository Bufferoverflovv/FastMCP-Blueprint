---
name: rename-project
description: "Safely rename a FastMCP project after bootstrap without missing package names, entry points, docs, or tests. Use when: renaming the project, changing the Python package name, changing the CLI command name, changing the display name, or fixing an inconsistent project name. Reads current names from pyproject.toml, shows a diff summary, then updates all affected files consistently."
argument-hint: "Optional: pass the new display name to pre-fill the first question"
---

# Rename the Project

Safely updates project names across every affected file in one guided pass, using the same file substitution map as `bootstrap-personalize`.

## When to use

- The project was bootstrapped but the name needs to change
- The package name, CLI command, or display name is inconsistent across files
- A search-and-replace was partially applied and left things inconsistent

## Step 1 — Read current names from `pyproject.toml`

Detect and display the current values:

```
Current display name:  <name from [project].name>
Current package name:  <name from [tool.hatch.build.targets.wheel].packages>
Current CLI command:   <name from [project.scripts]>
```

## Step 2 — Interview the user

Ask only what is changing. Use `vscode_askQuestions` if available.

| # | Question | Default |
|---|----------|---------|
| 1 | **New display name** | Current value |
| 2 | **New Python package name** (snake_case) | Current value |
| 3 | **New CLI command** (kebab-case) | Current value |

If all three answers match the current values exactly, tell the user nothing needs to change and exit.

## Step 3 — Show a confirmation diff

Display a table of every planned substitution before touching any file:

```
Display name:  OldName  →  NewName
Package name:  old_pkg  →  new_pkg
CLI command:   old-cmd  →  new-cmd

Files to update:
  pyproject.toml
  src/old_pkg/__main__.py
  src/old_pkg/config.py
  src/old_pkg/server.py
  src/old_pkg/routes/health.py
  src/old_pkg/tools/hello_world.py  (if present)
  tests/conftest.py
  tests/test_config.py
  tests/test_*.py (import lines)
  .env.example
  Dockerfile
  README.md
  AGENTS.md
  Directory rename: src/old_pkg/ → src/new_pkg/  (if package name changes)
```

Ask for confirmation before proceeding.

## Step 4 — Apply changes

Follow the substitution map in [../bootstrap-personalize/references/file-substitutions.md](../bootstrap-personalize/references/file-substitutions.md).

Apply in this order:

1. Terminal: rename `src/<old_package>/` → `src/<new_package>/` (only if package name changed)
2. `pyproject.toml`
3. `src/<pkg>/__main__.py`
4. `src/<pkg>/config.py`
5. `src/<pkg>/server.py`
6. All files under `src/<pkg>/tools/` and `src/<pkg>/routes/`
7. `tests/conftest.py`
8. All `tests/test_*.py` files
9. `.env.example`
10. `Dockerfile` (update `CMD` with new CLI command)
11. `README.md`
12. `AGENTS.md`

## Step 5 — Validate

```bash
ruff check .
pytest -v
```

Fix any import errors or broken assertions before reporting completion. The most common failure is `tests/test_config.py` asserting a hardcoded display name — check and update those assertion values.

## Step 6 — Report

Tell the user which files were changed and confirm tests pass.
