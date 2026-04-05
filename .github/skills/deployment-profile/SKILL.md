---
name: deployment-profile
description: "Generate deployment configuration and documentation for a FastMCP server. Use when: deploying to production, containerizing the server with Docker, setting up a reverse proxy with nginx or Caddy, deploying to a cloud platform, or generating docker-compose configuration. Asks about target environment, TLS strategy, and transport, then generates config files and a README deployment section."
argument-hint: "Optional: pass 'docker', 'compose', 'nginx', 'caddy', or a cloud name to skip to a specific profile"
---

# Deployment Profile

Generates deployment configuration and documentation for a specific target environment.

## When to use

- Moving from local development to a real deployment
- Containerizing the server for the first time
- Setting up a reverse proxy in front of the MCP server
- Deploying to a cloud platform (Render, Fly.io, Railway, etc.)

## Step 1 — Detect the package name and CLI command

Read `pyproject.toml` for `PACKAGE` and the console script name (`CLI_COMMAND`).

## Step 2 — Interview the user

Ask the following questions. Use `vscode_askQuestions` if available.

| # | Question | Options |
|---|----------|---------|
| 1 | **Deployment target** | Docker container, Docker Compose, reverse-proxy (nginx/Caddy), cloud platform, or bare server |
| 2 | **TLS strategy** | App handles TLS directly, TLS terminates at the proxy/load balancer, or no TLS |
| 3 | **MCP transport** | HTTP (default), SSE, or stdio |
| 4 | **Auth required?** | Yes or no — affects whether `AUTH_PROVIDER` must be set in the deployment env |
| 5 | **Cloud platform** (if cloud selected) | Render, Fly.io, Railway, or other |

## Step 3 — Generate config files

Based on answers, create the relevant files. See assets for templates:

| Target | Files to create |
|--------|----------------|
| Docker | The project already includes `Dockerfile` and `.dockerignore` — review and update them rather than generating new ones. See [./assets/dockerfile.md](./assets/dockerfile.md) for the template reference. |
| Docker Compose | [./assets/docker-compose.md](./assets/docker-compose.md) → `docker-compose.yml` |
| nginx | [./assets/reverse-proxy.md](./assets/reverse-proxy.md) → `deploy/nginx.conf` |
| Caddy | [./assets/reverse-proxy.md](./assets/reverse-proxy.md) → `deploy/Caddyfile` |
| Render | `render.yaml` |
| Fly.io | `fly.toml` |
| Railway | `railway.toml` |

See [./references/transport-tls.md](./references/transport-tls.md) for transport and TLS decision guidance.

## Step 4 — Update `README.md`

Add or update a Deployment section after the Quick Start section. Include:
- The deployment target and how to use the generated config
- Which env vars must be set in the deployment environment
- TLS setup notes
- How to verify the server is running (health check URL)

## Step 5 — Validate

For Docker targets, offer to run a build check:
```bash
docker build -t PACKAGE:latest .
```

For other targets, show the user the key command to verify the config is syntactically correct.

## Step 6 — Report

Tell the user:
- Which files were created
- Which env vars must be set in the deployment environment
- The health check URL to verify the deployment
- Any manual steps required (e.g. setting secrets in the platform UI)
