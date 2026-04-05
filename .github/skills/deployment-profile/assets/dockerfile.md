# Dockerfile Template

Placeholders to substitute before saving:

| Placeholder | Description |
|-------------|-------------|
| `CLI_COMMAND` | The console script name from `pyproject.toml` (e.g. `fastmcp-blueprint`) |
| `PACKAGE` | The Python package name (e.g. `fastmcp_blueprint`) |

## Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install uv for fast dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for layer caching
COPY pyproject.toml .
COPY src/ src/

# Install the package and runtime dependencies only
RUN uv pip install --system --no-cache -e .

# Non-root user for security
RUN useradd --no-create-home --shell /bin/false app
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["CLI_COMMAND", "--host", "0.0.0.0", "--port", "8000"]
```

## .dockerignore

```
.venv/
__pycache__/
*.pyc
*.pyo
.env
server.pem
server-ca.pem
.git/
tests/
docs/
*.egg-info/
dist/
```
