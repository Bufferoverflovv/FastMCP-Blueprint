---
name: docs-sync
description: "Sync README and AGENTS documentation with the current state of the codebase. Use when: tools or resources were added without updating docs, __main__.py imports are missing, README capabilities section is stale, AGENTS.md doesn't mention recent tools, documentation drift is suspected, or checking if docs match code. Scans tools/resources/routes, cross-references imports and docs, reports drift, and offers to fix clear-cut gaps."
argument-hint: "Optional: pass 'fix' to apply all automatically fixable gaps without prompting"
---

# Sync Documentation with Codebase

Detects and fixes drift between the actual tools, resources, and routes in the codebase and what is documented or imported.

## When to use

- After adding tools or resources without updating docs
- After deleting modules that are still referenced in docs
- Periodic housekeeping to catch documentation rot
- Before running `release-readiness` to reduce its findings

## Step 1 — Detect the package name

Read `pyproject.toml` to find the current `PACKAGE` name and locate the source tree.

## Step 2 — Ask the user's intent

Ask whether to:
- **Audit only** — report findings, make no changes
- **Audit and fix** — report findings and fix all automatically resolvable gaps

If the argument `fix` was passed, default to audit-and-fix.

## Step 3 — Scan the codebase

Use [./references/drift-checks.md](./references/drift-checks.md) for the full list of checks.

Build an inventory:
- `TOOLS` — all `.py` files (excluding `__init__.py`) under `src/PACKAGE/tools/`
- `RESOURCES` — all `.py` files (excluding `__init__.py`) under `src/PACKAGE/resources/`
- `ROUTES` — all `.py` files (excluding `__init__.py`) under `src/PACKAGE/routes/`

## Step 4 — Check `__main__.py` imports

For each module in the inventories, check that a corresponding `from PACKAGE.<type> import <module>  # noqa: F401` line exists in `__main__.py`.

Report:
- ❌ **Missing import** — module exists but no import in `__main__.py`
- ❌ **Stale import** — import in `__main__.py` but module file does not exist
- ✅ **OK** — import present and file exists

## Step 5 — Check `AGENTS.md`

- For each tool module, check that the tool name appears somewhere in `AGENTS.md`
- For each resource module, check the resource URI or name appears
- Report missing mentions as ⚠️ warnings (not hard failures — docs may describe them differently)

## Step 6 — Check `README.md`

- Check that the CLI command name in the README matches `pyproject.toml`
- Check that the package name in Python import examples matches the actual package
- Check for any tool or resource names mentioned in README that no longer exist in code

## Step 7 — Fix (if requested)

Automatically fix:
- Missing `__main__.py` imports (add in the correct location)
- Stale `__main__.py` imports (remove)
- CLI command and package name mismatches in README

Do not auto-fix:
- `AGENTS.md` content — tool descriptions require human judgment
- `README.md` capability prose — may need rewording, not just name substitution

For items that cannot be auto-fixed, provide the exact edit needed so the user can apply it manually.

## Step 8 — Report

Show the full findings grouped by category. End with a count:
```
X issues fixed automatically
Y issues require manual attention
Z items are in sync
```
