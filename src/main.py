import logging
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import psutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.infrastructure.config.settings import Settings

_PROC = psutil.Process()
_PROC.cpu_percent()

_settings = Settings()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, _settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


app = FastAPI(
    title="H³ Backoffice Gateway",
    description="Backoffice telemetry aggregation gateway",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "hhh-bo-gateway",
        "cpu_percent": _PROC.cpu_percent(),
        "ram_mb": round(_PROC.memory_info().rss / 1024 / 1024, 1),
        "threads": _PROC.num_threads(),
        "uptime_seconds": round(time.time() - _PROC.create_time()),
    }


@app.get("/metrics", tags=["metrics"])
def metrics_endpoint() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
