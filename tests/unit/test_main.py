import pytest
from fastapi.testclient import TestClient

from src.infrastructure.config.settings import Settings
from src.main import app, lifespan


def test_health_endpoint_returns_ok():
    with TestClient(app) as client:
        resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "hhh-bo-gateway"
    assert "cpu_percent" in data
    assert "ram_mb" in data
    assert "threads" in data
    assert "uptime_seconds" in data
    assert isinstance(data["ram_mb"], (int, float))
    assert isinstance(data["threads"], int)
    assert isinstance(data["uptime_seconds"], int)
    assert isinstance(data["cpu_percent"], (int, float))


def test_metrics_endpoint_returns_prometheus_format():
    with TestClient(app) as client:
        resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "text/plain" in resp.headers["content-type"]


def test_cors_origins_in_settings():
    s = Settings()
    assert "http://localhost:3000" in s.cors_origins
    assert "http://localhost:3001" in s.cors_origins


@pytest.mark.asyncio
async def test_lifespan_yields_cleanly():
    async with lifespan(app):
        pass
