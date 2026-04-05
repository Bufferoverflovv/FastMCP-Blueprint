# Release Readiness Checklist

Full list of checks to run during a release-readiness audit. Grouped by category.
Each item includes what to check, how to check it, and what the fix is.

---

## 1. Packaging metadata (`pyproject.toml`)

| Check | How | Fix |
|-------|-----|-----|
| `name` is set and not the default `FastMCP-Blueprint` | Read `[project].name` | Ask user for the correct name |
| `version` is set | Read `[project].version` | Remind user to set a version |
| `description` is set and not the placeholder | Read `[project].description` | Ask user for a real description |
| `requires-python` is `>=3.13` | Read `[project].requires-python` | Update to `>=3.13` |
| Console script entry point is present | Read `[project.scripts]` | Warn if missing |
| `packages` points to the correct source directory | Read `[tool.hatch.build.targets.wheel].packages` | Flag if it still says `src/fastmcp_blueprint` after a rename |
| All runtime deps pinned with `~=` or `>=` | Read `[project].dependencies` | Warn if any are unpinned |

---

## 2. Python package structure

| Check | How | Fix |
|-------|-----|-----|
| `src/<package>/__init__.py` exists | `file_search` | Create empty file |
| `src/<package>/py.typed` exists | `file_search` | Create empty file |
| `src/<package>/tools/__init__.py` exists | `file_search` | Create empty file |
| `src/<package>/resources/__init__.py` exists | `file_search` | Create empty file |
| `src/<package>/routes/__init__.py` exists | `file_search` | Create empty file |
| Package directory name matches `pyproject.toml` `packages` value | Compare dir vs config | Flag mismatch |

---

## 3. Documentation

| Check | How | Fix |
|-------|-----|-----|
| `README.md` exists and has meaningful content (> 20 lines) | Read file, count lines | Remind user to write a README (or run skill if available) |
| README does not contain "FastMCP-Blueprint" if the project has been renamed | Search README for template name | Update references |
| README CLI examples use the correct command name | Search README for CLI command | Update to match `pyproject.toml` entry point |
| README package examples use the correct package name | Search README for Python imports | Update to match package directory |
| `CHANGELOG.md` exists | `file_search` | Create from Keep a Changelog template |
| `CHANGELOG.md` has at least one real entry beyond the template heading | Read file, check for `## [` entries beyond the header | Cannot auto-fix — remind user to add a changelog entry |
| `LICENSE` file exists | `file_search` | Warn — cannot auto-generate a license |
| `AGENTS.md` or `.github/copilot-instructions.md` is present | `file_search` | Warn if missing |

---

## 4. Environment configuration

| Check | How | Fix |
|-------|-----|-----|
| `.env.example` exists | `file_search` | Cannot auto-fix — remind user |
| `.env.example` `NAME=` matches `pyproject.toml` display name | Compare values | Update `NAME=` line |
| `.env.example` `VERSION=` matches `pyproject.toml` `version` | Compare values | Update `VERSION=` line |
| No real secrets in `.env.example` (no non-placeholder values for `*_SECRET`, `*_KEY`, `*_TOKEN`) | Search for patterns | Flag lines, ask user to replace with placeholders |
| `.env` is in `.gitignore` | Read `.gitignore` | Add `.env` entry |
| `server.pem` and `server-ca.pem` are in `.gitignore` | Read `.gitignore` | Add entries |

---

## 5. Sample and placeholder code

| Check | How | Fix |
|-------|-----|-----|
| `hello_world` tool is either intentionally kept or has been replaced | Check if `src/<pkg>/tools/hello_world.py` exists; ask user if so | Offer to delete it and clean up imports |
| No `TODO` comments left in source files (outside of templates) | `grep_search` for `TODO` in `src/` | Report each location — cannot auto-fix |
| No placeholder text like "Your description here" in `pyproject.toml` or README | Search for common placeholder phrases | Flag — ask user to replace |

---

## 6. Code quality

| Check | How | Fix |
|-------|-----|-----|
| `ruff check .` passes with zero errors | Run in terminal | Apply `ruff check --fix .` for auto-fixable issues |
| `ruff format --check .` passes | Run in terminal | Apply `ruff format .` |
| All tests pass | Run `pytest -v` | Report failures — cannot auto-fix |
| Pre-commit config exists (`.pre-commit-config.yaml`) | `file_search` | Warn if missing |

---

## 7. Internal naming consistency

| Check | How | Fix |
|-------|-----|-----|
| Display name is consistent across `pyproject.toml`, `README.md`, `AGENTS.md`, and `.env.example` | Read and compare `name` / `NAME=` fields | Update the outlier files |
| CLI command is consistent across `pyproject.toml`, `README.md`, and `AGENTS.md` | Search for the command name | Update the outlier files |
| Package name is consistent across `pyproject.toml`, all `import` statements, and `__main__.py` | Search for the package name | Flag mismatched imports |

---

## 8. Security baseline

| Check | How | Fix |
|-------|-----|-----|
| No hardcoded secrets in source files (`*.py`) | `grep_search` for `password =`, `secret =`, `api_key =`, `token =` with string values | Flag — cannot auto-fix |
| No hardcoded URLs that should come from config | `grep_search` for `http://` or `https://` in `src/` (excluding comments and docstrings) | Flag — ask user to move to `config.py` |
| `mask_error_details=True` is set on the FastMCP instance | Read `server.py` | Add if missing |

---

## Summary severity guide

- ✅ **Pass** — no action needed
- ⚠️ **Warning** — worth fixing before release, but not blocking
- ❌ **Fail** — should be fixed before making the repo public
