# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./

# Standalone build: see README for BuildKit secret usage.
RUN --mount=type=secret,id=devpi_username,env=UV_INDEX_HEXADIAN_USERNAME \
    --mount=type=secret,id=devpi_password,env=UV_INDEX_HEXADIAN_PASSWORD \
    : "${UV_INDEX_HEXADIAN_USERNAME:?missing UV_INDEX_HEXADIAN_USERNAME (BuildKit secret devpi_username)}"; \
    : "${UV_INDEX_HEXADIAN_PASSWORD:?missing UV_INDEX_HEXADIAN_PASSWORD (BuildKit secret devpi_password)}"; \
    uv sync --frozen --no-dev --no-install-project

COPY . .
RUN --mount=type=secret,id=devpi_username,env=UV_INDEX_HEXADIAN_USERNAME \
    --mount=type=secret,id=devpi_password,env=UV_INDEX_HEXADIAN_PASSWORD \
    : "${UV_INDEX_HEXADIAN_USERNAME:?missing UV_INDEX_HEXADIAN_USERNAME (BuildKit secret devpi_username)}"; \
    : "${UV_INDEX_HEXADIAN_PASSWORD:?missing UV_INDEX_HEXADIAN_PASSWORD (BuildKit secret devpi_password)}"; \
    uv sync --frozen --no-dev

EXPOSE 8010

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8010"]