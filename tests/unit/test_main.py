import pytest
from fastapi.testclient import TestClient

from src.main import create_app, lifespan


def test_health_endpoint_returns_ok():
    app = create_app()
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
    assert isinstance(data["ram_mb"], int | float)
    assert isinstance(data["threads"], int)
    assert isinstance(data["uptime_seconds"], int)
    assert isinstance(data["cpu_percent"], int | float)


def test_metrics_endpoint_returns_prometheus_format():
    app = create_app()
    with TestClient(app) as client:
        resp = client.get("/metrics")
    assert resp.status_code == 200
    content_type = resp.headers["content-type"]
    assert "text/plain" in content_type
    # WHY: Prometheus exposition format announces a version in Content-Type (0.0.4 in
    # older prometheus_client, 1.0.0 in newer); we assert the marker is present, not its value.
    assert "version=" in content_type


def test_cors_preflight_echoes_origin():
    app = create_app()
    with TestClient(app) as client:
        resp = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
    assert resp.status_code == 200
    assert resp.headers["access-control-allow-origin"] == "http://localhost:3000"


@pytest.mark.asyncio
async def test_lifespan_yields_cleanly():
    app = create_app()
    async with lifespan(app):
        pass
