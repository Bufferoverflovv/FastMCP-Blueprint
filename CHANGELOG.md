# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-10

### Changed

- Extracted structured logging internals into `src/fastmcp_blueprint/logging_setup.py` while keeping server assembly and middleware registration in `server.py`.
- Updated logging documentation to describe request correlation, secret scrubbing, uvicorn log routing, and the `LOG_PAYLOAD_ENABLED` toggle for FastMCP payload logging.

### Added

- Request-scoped correlation IDs for MCP logs via `RequestContextMiddleware`.
- JSON log formatting for Python log records emitted through the `fastmcp` logger hierarchy.
- Secret scrubbing for common bearer tokens, JWTs, and `api_key=`/`password=`-style assignments.

## [0.1.0] - 2026-04-05

Initial public blueprint release.

### Added

- FastMCP server scaffold with a Python `src` layout and CLI entry point.
- Environment-based configuration loading through `.env`.
- Sample `hello_world` MCP tool for end-to-end validation.
- Built-in `/health` and `/ready` HTTP routes for liveness and readiness checks.
- Optional authentication wiring for `remote` and `oauth_proxy` providers.
- Structured logging support, local TLS certificate generation, and container packaging.
- In-memory test setup with pytest, Ruff formatting/linting, and pre-commit hooks.
- Copilot skill files to help extend the blueprint with tools, resources, routes, tests, docs, auth, observability, deployment, and release work.

### Notes

- This release is experimental. The blueprint is intended to accelerate new FastMCP projects, but some workflows may still need manual adjustment depending on the server you are building.
- Not every extension path has been exercised in a production deployment yet. Expect some rough edges, especially when combining auth, deployment, and project renaming flows.

### Known limitations

- The included sample tool and routes are scaffolding, not production features.
- Container, auth, and deployment settings provide a strong starting point, but they should be validated in your target environment before relying on them.
- Additional hardening, domain-specific tests, and operational checks will usually be required before a real release.