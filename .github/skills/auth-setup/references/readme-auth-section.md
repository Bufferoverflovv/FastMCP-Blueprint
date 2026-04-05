# README Authentication Section Template

Use this template when updating or adding an Authentication section to `README.md` after running `auth-setup`.

---

## Authentication

Authentication is disabled by default. Set `AUTH_PROVIDER` in `.env` to enable one of two modes:

| `AUTH_PROVIDER` | Use case | Upstream docs |
|-----------------|----------|---------------|
| `remote` | Identity providers with DCR (WorkOS AuthKit, Descope) | [Remote OAuth](https://gofastmcp.com/servers/auth/remote-oauth) |
| `oauth_proxy` | Providers without DCR (GitHub, Google, Azure) | [OAuth Proxy](https://gofastmcp.com/servers/auth/oauth-proxy) |

### Shared env vars (both modes)

```env
AUTH_PROVIDER=remote          # or oauth_proxy
AUTH_JWKS_URI=https://your-auth-server.com/.well-known/jwks.json
AUTH_ISSUER=https://your-auth-server.com
AUTH_AUDIENCE=your-mcp-server
AUTH_BASE_URL=https://your-mcp-server.com
```

### OAuth Proxy additional env vars

```env
OAUTH_UPSTREAM_AUTHORIZE_URL=https://provider.com/oauth/authorize
OAUTH_UPSTREAM_TOKEN_URL=https://provider.com/oauth/token
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
```

Auth wiring lives in `_build_auth()` in `server.py`. Auth dependencies are loaded lazily so no auth packages are imported when auth is disabled.

---

**Placement guidance:** Add this section after the Configuration section and before any operational sections like Health endpoints or Logging.
