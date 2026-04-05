# Drift Checks

Reference for the exact checks to run during a `docs-sync` audit.

---

## 1. Build the codebase inventory

Scan these directories for Python modules (all `.py` files excluding `__init__.py`):

| Source | Directory |
|--------|-----------|
| Tools | `src/PACKAGE/tools/` |
| Resources | `src/PACKAGE/resources/` |
| Routes | `src/PACKAGE/routes/` |

Produce three lists: `TOOLS`, `RESOURCES`, `ROUTES` — each is a list of module names (filename without `.py`).

---

## 2. Check `__main__.py` imports

For each module in the inventory, look for a line matching:

```python
from PACKAGE.<type> import <module>  # noqa: F401
```

| Finding | Severity | Auto-fix? |
|---------|----------|-----------|
| Module exists, import missing | ❌ Fail | Yes — add import in the correct block |
| Import present, module file missing | ❌ Fail | Yes — remove the stale import |
| Import present and file exists | ✅ OK | — |

When adding a missing import, place it after the last import in the same block (tools with tools, routes with routes).

---

## 3. Check `AGENTS.md` mentions

For each tool name in `TOOLS`, check whether the name appears anywhere in `AGENTS.md`.

For each resource name in `RESOURCES`, check whether the name or its URI appears.

| Finding | Severity | Auto-fix? |
|---------|----------|-----------|
| Module not mentioned anywhere | ⚠️ Warning | No — requires human-written description |
| `AGENTS.md` mentions a name that no longer exists | ⚠️ Warning | No — context needed |

---

## 4. Check `README.md` consistency

| Check | How to detect | Severity | Auto-fix? |
|-------|---------------|----------|-----------|
| CLI command in README doesn't match `pyproject.toml` `[project.scripts]` | Compare strings | ❌ Fail | Yes |
| Package name in Python import examples wrong | Search for `from <wrong_pkg>` | ❌ Fail | Yes |
| Tool/resource names in README that no longer exist | Scan README for known tool names | ⚠️ Warning | No |

---

## 5. Check `conftest.py` imports

`conftest.py` imports tool and route modules for side-effect registration. Verify these match `__main__.py`:

- Any module imported in `conftest.py` but not in `__main__.py` → ⚠️ Warning
- Any module imported in `__main__.py` but not in `conftest.py` → ⚠️ Warning (tests may miss coverage)

---

## Fix order

When applying automatic fixes, always:
1. Fix `__main__.py` imports first (add missing, remove stale)
2. Fix README string substitutions
3. Run `ruff format .` after any Python file edits
4. Report `AGENTS.md` and prose issues separately for manual review
