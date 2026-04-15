# Run the notebook inside Docker

Quick steps to build and run the ProjectTwo notebook in Docker (from repository root `c:\SNHU\CS340`):

1. Build and start the container:

```powershell
docker compose up --build
```

2. Open the notebook in your browser:

- URL: http://localhost:8888
- Token: `secret` (set in `docker-compose.yml` / `Dockerfile` as `JUPYTER_TOKEN`)

Notes:
- The repository is mounted into the container at `/workspace`, so edits persist on your host.
- To change the token, set `JUPYTER_TOKEN` in `docker-compose.yml` or pass it as an environment variable.
- If you prefer `docker-compose` (v1), use `docker-compose up --build`.
