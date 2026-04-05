---
name: release-readiness
description: "Audit and fix a FastMCP project before publishing or sharing it publicly. Use when: preparing for a first release, checking if the repo is ready to go public, reviewing packaging metadata, auditing README completeness, checking env example parity, verifying tests and linting pass, confirming sample/placeholder code is removed, or ensuring project naming is internally consistent. Produces a concrete checklist and optionally fixes issues directly."
argument-hint: "Optional: pass 'fix' to apply all fixable issues automatically after audit"
---

# Release Readiness Audit

Systematically reviews a FastMCP project against a checklist of the most common things that are wrong or missing before a first public release. Reports findings as a categorized checklist and offers to fix each item directly.

## When to use

- Before pushing the repository public or sharing it with others
- After running `bootstrap-personalize` to confirm everything is clean
- Periodically to catch documentation drift or configuration rot

## Step 1 — Ask the user's intent

Ask whether to:
- **Audit only** — report all findings, make no changes
- **Audit and fix** — report findings and immediately fix everything that can be fixed automatically

If the argument `fix` was passed, default to audit-and-fix without asking.

## Step 2 — Run the full audit

Work through each category in [./references/checklist.md](./references/checklist.md). For each item:
- Read the relevant file(s)
- Apply the check described
- Record the result as ✅ pass, ⚠️ warning, or ❌ fail

## Step 3 — Report findings

Present the full checklist grouped by category with status icons. Example:

```
## Packaging
✅ name, version, description present in pyproject.toml
✅ requires-python >= 3.13
✅ py.typed marker exists
❌ console script entry point missing

## Documentation
✅ README.md exists and has content
⚠️ CHANGELOG.md has no entries (only template text)
✅ LICENSE file present

## Code quality
✅ ruff check passes
✅ ruff format --check passes
✅ All tests pass

## ...
```

## Step 4 — Fix (if requested)

For every ❌ fail and ⚠️ warning that can be fixed automatically, apply the fix. Skip anything that requires human judgment or real content (e.g. filling in a changelog).

For each fix, briefly note what was changed.

## Step 5 — Re-run affected checks

After applying fixes, re-run only the checks that were ❌ or ⚠️ to confirm they now pass.

## Step 6 — Report final state

Show the updated checklist. If any items remain unfixed, explain why and what the user needs to do manually.
