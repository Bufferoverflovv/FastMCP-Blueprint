# Transport and TLS Decision Guide

Reference for choosing the right transport and TLS strategy when deploying a FastMCP server.

---

## Transport options

| Transport | When to use |
|-----------|-------------|
| `http` (default) | Any network-accessible deployment — web, container, cloud |
| `sse` | Clients that require Server-Sent Events; less common with modern MCP clients |
| `stdio` | Local process invocation only (e.g. Claude Desktop direct integration) |

The transport is set via `mcp.run(transport="http", ...)` in `__main__.py`. For `stdio`, remove the `host`/`port` arguments.

---

## TLS strategies

### App handles TLS directly

Set `SSL_CERTFILE` (and optionally `SSL_KEYFILE`) in `.env`. The combined PEM file from `generate_cert.py` works here.

```env
SSL_CERTFILE=server.pem
```

Suitable for: direct-to-internet deployments, development with HTTPS.

### TLS terminates at the proxy

Run the FastMCP server on HTTP (`localhost:8000`) and let nginx, Caddy, or a cloud load balancer handle TLS.

Leave `SSL_CERTFILE` unset. Set `HOST=0.0.0.0` or `HOST=127.0.0.1` depending on whether the proxy is on the same host.

Suitable for: most production deployments — simpler cert management, automatic renewal via Let's Encrypt.

### No TLS

Only appropriate for local development or private internal networks. Never expose an MCP server without TLS on a public network.

---

## Port recommendations

| Scenario | Port |
|----------|------|
| Local HTTP development | 8000 |
| Local HTTPS development | 8443 |
| Production (behind proxy) | 8000 (internal only) |
| Production (direct TLS) | 443 |

---

## Health check path

Always configure the deployment platform's health check to hit:

```
GET /health
```

Use `/ready` for readiness probes (e.g. Kubernetes, Render zero-downtime deploys) — it verifies that tools are registered, not just that the process is alive.
