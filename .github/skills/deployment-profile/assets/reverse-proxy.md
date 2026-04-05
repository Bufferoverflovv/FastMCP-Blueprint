# Reverse Proxy Configuration Templates

The FastMCP server runs on `localhost:8000` (HTTP). The proxy handles TLS and forwards to it.

Placeholders to substitute before saving:

| Placeholder | Description |
|-------------|-------------|
| `YOUR_DOMAIN` | Your server's domain name, e.g. `mcp.example.com` |

---

## nginx (`deploy/nginx.conf`)

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name YOUR_DOMAIN;

    ssl_certificate     /etc/letsencrypt/live/YOUR_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/YOUR_DOMAIN/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;

        # SSE and long-poll support
        proxy_buffering    off;
        proxy_read_timeout 3600s;
    }
}
```

---

## Caddy (`deploy/Caddyfile`)

Caddy handles HTTPS automatically via Let's Encrypt — no manual certificate management needed.

```caddyfile
YOUR_DOMAIN {
    reverse_proxy localhost:8000 {
        header_up X-Forwarded-Proto {scheme}
        header_up X-Real-IP {remote_host}
    }
}
```

---

## Notes

- `proxy_buffering off` (nginx) and Caddy's default streaming mode ensure SSE streams and long-lived connections work correctly
- Set `HOST=127.0.0.1` in `.env` when using a reverse proxy on the same host — the server should only be reachable internally
- Set `HOST=0.0.0.0` only when the server must also accept direct connections (e.g. in Docker Compose where the proxy is in a separate container)
