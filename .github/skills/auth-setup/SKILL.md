---
name: auth-setup
description: "Enable and configure authentication on this FastMCP server. Use when: adding authentication to the MCP server, configuring OAuth or JWT auth, enabling remote auth provider, setting up OAuth proxy for GitHub/Google/Azure, documenting required auth environment variables, or troubleshooting auth configuration. Asks which auth mode to enable then updates .env.example, README, and optionally tightens config validation."
argument-hint: "Optional: pass 'remote' or 'oauth_proxy' to skip the first question"
---

# Enable Authentication

Guides you through enabling one of the two built-in auth modes, populating the required environment variables, and updating the documentation so nothing is missing in production.

## When to use

- Enabling authentication for the first time on a new server
- Switching from one auth mode to another
- Auditing whether the auth env vars and documentation are complete and consistent
- Deploying to an environment where unauthenticated access is not acceptable

## Background

Authentication is disabled by default (`AUTH_PROVIDER` is empty). Setting `AUTH_PROVIDER` in `.env` activates one of two modes wired in `server.py`:

| Mode | Use case | FastMCP class |
|------|----------|---------------|
| `remote` | Providers with DCR (WorkOS AuthKit, Descope) | `RemoteAuthProvider` + `JWTVerifier` |
| `oauth_proxy` | Providers without DCR (GitHub, Google, Azure) | `OAuthProxy` + `JWTVerifier` |

Both modes verify JWTs. The `oauth_proxy` mode additionally proxies the upstream authorization flow.

## Step 1 — Interview the user

Ask the following questions. Use `vscode_askQuestions` if available.

**Shared questions (both modes):**

| # | Question | Notes |
|---|----------|-------|
| 1 | **Auth mode** | `remote` or `oauth_proxy` |
| 2 | **JWKS URI** | The JSON Web Key Set endpoint, e.g. `https://your-auth.com/.well-known/jwks.json` |
| 3 | **Issuer** | JWT issuer claim, e.g. `https://your-auth.com` |
| 4 | **Audience** | JWT audience claim, e.g. `my-mcp-server` |
| 5 | **Auth base URL** | Public base URL of this MCP server, used for DCR/OAuth metadata |

**OAuth Proxy additional questions (mode = `oauth_proxy` only):**

| # | Question | Notes |
|---|----------|-------|
| 6 | **Upstream authorize URL** | e.g. `https://github.com/login/oauth/authorize` |
| 7 | **Upstream token URL** | e.g. `https://github.com/login/oauth/access_token` |
| 8 | **OAuth client ID** | From the upstream provider's app registration |
| 9 | **OAuth client secret** | From the upstream provider's app registration |

## Step 2 — Update `.env.example`

Uncomment and fill in the relevant variables. Keep values as placeholders (not real secrets) for `.env.example`.

For `remote`:
```env
AUTH_PROVIDER=remote
AUTH_JWKS_URI=https://your-auth-server.com/.well-known/jwks.json
AUTH_ISSUER=https://your-auth-server.com
AUTH_AUDIENCE=your-mcp-server
AUTH_BASE_URL=https://your-mcp-server.com
```

For `oauth_proxy`, add the above plus:
```env
AUTH_PROVIDER=oauth_proxy
OAUTH_UPSTREAM_AUTHORIZE_URL=https://provider.com/oauth/authorize
OAUTH_UPSTREAM_TOKEN_URL=https://provider.com/oauth/token
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
```

## Step 3 — Update the local `.env` file

If a `.env` file exists, add the same variables with the actual values the user provided. Never commit real secrets to the repo.

Remind the user that `.env` is in `.gitignore` and should not be committed.

## Step 4 — Update `README.md`

Find the Authentication section. If it exists, update the relevant env var table with the actual values or accurate placeholders. If it does not exist, add a short section after the Configuration section. See [./references/readme-auth-section.md](./references/readme-auth-section.md) for a template.

## Step 5 — Optionally tighten config validation

If the user wants the server to refuse to start when required auth vars are missing, add validation to `config.py`:

```python
def validate(self) -> None:
    # existing validation ...

    if self.auth_provider in ("remote", "oauth_proxy"):
        required = [self.auth_jwks_uri, self.auth_issuer, self.auth_audience, self.auth_base_url]
        if not all(required):
            raise ValueError(
                "AUTH_JWKS_URI, AUTH_ISSUER, AUTH_AUDIENCE, and AUTH_BASE_URL "
                "are required when AUTH_PROVIDER is set"
            )
    if self.auth_provider == "oauth_proxy":
        proxy_required = [
            self.oauth_upstream_authorize_url,
            self.oauth_upstream_token_url,
            self.oauth_client_id,
            self.oauth_client_secret,
        ]
        if not all(proxy_required):
            raise ValueError(
                "OAUTH_UPSTREAM_AUTHORIZE_URL, OAUTH_UPSTREAM_TOKEN_URL, "
                "OAUTH_CLIENT_ID, and OAUTH_CLIENT_SECRET are required "
                "when AUTH_PROVIDER=oauth_proxy"
            )
```

Ask the user whether they want this added before applying it.

## Step 6 — Validate

```bash
ruff check .
pytest -v
```

If config validation was added, ensure the existing `test_config.py` tests still pass. The `test_valid_auth_providers_accepted` test uses empty string values, so it may need adjustment if stricter validation is applied.

## Step 7 — Report

Tell the user:
- Which variables were set in `.env.example`
- Whether `.env` was updated
- Whether config validation was tightened
- The next step: start the server and verify the auth flow with an MCP client
