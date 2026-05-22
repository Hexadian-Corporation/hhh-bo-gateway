> **(C) 2026 Hexadian Corporation** -- Licensed under [PolyForm Noncommercial 1.0.0 (Modified)](./LICENSE). No commercial use, no public deployment, no plagiarism. See [LICENSE](./LICENSE) for full terms.

# hhh-bo-gateway -- Backoffice Gateway Service

Backoffice telemetry aggregation gateway for **H3 -- Hexadian Hauling Helper**. Bootstrap scaffold exposing /health and /metrics; the REST snapshot endpoint and the WebSocket live feed will be added in follow-up issues.

## Stack

- Python 3.11+ / FastAPI
- MongoDB (database: `hhh_bo_gateway`)
- opyoid (dependency injection)
- Hexagonal architecture (Ports and Adapters)
- prometheus-client metrics

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- MongoDB running on localhost:27017 (planned, not required for bootstrap /health)

## Setup

```bash
uv sync --extra dev
```

## Run

```bash
uv run uvicorn src.main:app --reload --port 8010
```

## Test

```bash
uv run pytest --cov --cov-fail-under=90
```

## Lint

```bash
uv run ruff check .
```

## Format

```bash
uv run ruff format .
```

## Environment Variables

| Variable | Default |
|---|---|
| `HHH_BO_GATEWAY_LOG_LEVEL` | `DEBUG` |
| `HHH_BO_GATEWAY_HOST` | `0.0.0.0` |
| `HHH_BO_GATEWAY_PORT` | `8010` |
| `HHH_BO_GATEWAY_MONGO_URI` | `mongodb://localhost:27017` |
| `HHH_BO_GATEWAY_MONGO_DATABASE` | `hhh_bo_gateway` |
| `HHH_BO_GATEWAY_EVENTS_MONGO_URI` | `mongodb://localhost:27017` |
| `HHH_BO_GATEWAY_EVENTS_DB` | `hhh_events` |
| `HHH_BO_GATEWAY_CORS_ORIGINS` | `http://localhost:3000,http://localhost:3001` |
| `HHH_BO_GATEWAY_AUTH_JWKS_URL` | (required) |
| `HHH_BO_GATEWAY_AUTH_ISSUER` | (required) |
| `HHH_BO_GATEWAY_AUTH_AUDIENCES` | (required, CSV) |
| `HHH_BO_GATEWAY_AUTH_LEEWAY_SECONDS` | `30` |
| `HHH_BO_GATEWAY_AUTH_ALLOW_INSECURE_JWKS` | `false` |

## Architecture

Strict hexagonal -- `src/domain`, `src/application/{ports, services}`, `src/infrastructure/{config, adapters/inbound/api, adapters/outbound}`. Domain layer empty for bootstrap; will be populated by follow-up issues that introduce the snapshot aggregator and WS live feed.