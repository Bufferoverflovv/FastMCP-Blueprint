# Docker Compose Template

Placeholders to substitute before saving:

| Placeholder | Description |
|-------------|-------------|
| `PACKAGE` | Python package name (used as the service name) |
| `CLI_COMMAND` | Console script name |

## docker-compose.yml

```yaml
services:
  mcp:
    build: .
    image: PACKAGE:latest
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      HOST: "0.0.0.0"
      PORT: "8000"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

## Usage

```bash
# Build and start
docker compose up --build -d

# Check health
curl http://localhost:8000/health

# View logs
docker compose logs -f mcp

# Stop
docker compose down
```

## With TLS (app terminates TLS)

Mount the certificate into the container and set env vars:

```yaml
services:
  mcp:
    build: .
    ports:
      - "443:443"
    env_file:
      - .env
    environment:
      HOST: "0.0.0.0"
      PORT: "443"
      SSL_CERTFILE: "/certs/server.pem"
    volumes:
      - ./server.pem:/certs/server.pem:ro
```
