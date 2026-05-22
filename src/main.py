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

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = Settings()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
    )

    app = FastAPI(
        title="H³ Backoffice Gateway",
        description="Backoffice telemetry aggregation gateway",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
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

    return app


app = create_app()
