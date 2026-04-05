# File Substitutions for bootstrap-personalize

Reference for the exact substitutions to apply in each file. Used in Step 3 of the skill procedure.

Variables used below:

- `OLD_PACKAGE` — current Python package name (default: `fastmcp_blueprint`)
- `NEW_PACKAGE` — new Python package name (snake_case)
- `OLD_CLI` — current CLI command (default: `fastmcp-blueprint`)
- `NEW_CLI` — new CLI command (kebab-case)
- `OLD_DISPLAY` — current display name (default: `FastMCP-Blueprint`)
- `NEW_DISPLAY` — new display name
- `OLD_DESC` — current short description
- `NEW_DESC` — new short description
- `OLD_INSTRUCTIONS` — current MCP instructions string
- `NEW_INSTRUCTIONS` — new MCP instructions string

---

## pyproject.toml

```
name = "OLD_DISPLAY"                   →  name = "NEW_DISPLAY"
description = "OLD_DESC"               →  description = "NEW_DESC"
NEW_CLI = "OLD_PACKAGE.__main__:main"  →  NEW_CLI = "NEW_PACKAGE.__main__:main"
packages = ["src/OLD_PACKAGE"]         →  packages = ["src/NEW_PACKAGE"]
```

---

## src/OLD_PACKAGE/__main__.py

```python
from OLD_PACKAGE.config import settings   →  from NEW_PACKAGE.config import settings
from OLD_PACKAGE.server import mcp        →  from NEW_PACKAGE.server import mcp
from OLD_PACKAGE.routes import health     →  from NEW_PACKAGE.routes import health
from OLD_PACKAGE.tools import hello_world →  from NEW_PACKAGE.tools import hello_world
```

Also update the argparse description if it contains `OLD_DISPLAY`.

---

## src/OLD_PACKAGE/config.py

```python
os.environ.get("NAME", "OLD_DISPLAY")         →  os.environ.get("NAME", "NEW_DISPLAY")
os.environ.get("INSTRUCTIONS", "OLD_INSTRUCTIONS") →  os.environ.get("INSTRUCTIONS", "NEW_INSTRUCTIONS")
```

---

## src/OLD_PACKAGE/server.py

```python
from OLD_PACKAGE.config import settings   →  from NEW_PACKAGE.config import settings
```

If the module docstring references the project name, update it.

---

## src/OLD_PACKAGE/tools/hello_world.py

```python
from OLD_PACKAGE.server import get_tool_logger, mcp  →  from NEW_PACKAGE.server import get_tool_logger, mcp
```

---

## src/OLD_PACKAGE/routes/health.py

```python
from OLD_PACKAGE.server import mcp   →  from NEW_PACKAGE.server import mcp
```

---

## tests/conftest.py

```python
from OLD_PACKAGE.server import mcp           →  from NEW_PACKAGE.server import mcp
from OLD_PACKAGE.routes import health        →  from NEW_PACKAGE.routes import health
from OLD_PACKAGE.tools import hello_world    →  from NEW_PACKAGE.tools import hello_world
```

---

## tests/test_*.py (all test files)

Any `from OLD_PACKAGE` import → `from NEW_PACKAGE`

---

## tests/test_config.py

```python
config.name == "OLD_DISPLAY"   →  config.name == "NEW_DISPLAY"
```

---

## Dockerfile

```dockerfile
CMD ["OLD_CLI", ...   →  CMD ["NEW_CLI", ...
```

Update the `CMD` and any `HEALTHCHECK` lines that reference the CLI command.

---

## .dockerignore

No substitutions needed — `.dockerignore` has no project-specific tokens.

Check all assertion values that reference the display name.

---

## .env.example

```
NAME=OLD_DISPLAY            →  NAME=NEW_DISPLAY
INSTRUCTIONS=OLD_INSTRUCTIONS →  INSTRUCTIONS=NEW_INSTRUCTIONS
```

---

## README.md

```
# OLD_DISPLAY      →  # NEW_DISPLAY
OLD_CLI            →  NEW_CLI      (in all code blocks and prose)
OLD_PACKAGE        →  NEW_PACKAGE  (in all code blocks)
```

Also update the badge `[*-Blueprint` references if badge text includes the display name.

---

## AGENTS.md

```
OLD_DISPLAY            →  NEW_DISPLAY  (in title and headings)
fastmcp-blueprint      →  NEW_CLI      (in all shell examples)
fastmcp_blueprint      →  NEW_PACKAGE  (in all Python import examples)
src/fastmcp_blueprint/ →  src/NEW_PACKAGE/
```

---

## CHANGELOG.md

No automated substitution — leave the template heading structure intact. The user can fill in their own content.

---

## Notes

- All substitutions are case-sensitive.
- Only rename files/directories when the package name actually changes.
- Never use destructive overwrite when adding auth changes to `.env.example`; prefer uncommenting or adding to the existing block.
- After all substitutions, run `ruff format .` then `ruff check --fix .` before running tests.
