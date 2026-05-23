import pytest
from pydantic import ValidationError

from src.infrastructure.config.settings import Settings


def test_auth_audiences_csv_parsing(monkeypatch):
    monkeypatch.setenv("HHH_BO_GATEWAY_AUTH_AUDIENCES", "a,b,c")
    s = Settings()
    assert s.auth_audiences == ["a", "b", "c"]


def test_cors_origins_csv_parsing(monkeypatch):
    monkeypatch.setenv("HHH_BO_GATEWAY_CORS_ORIGINS", "http://x.com,http://y.com")
    s = Settings()
    assert s.cors_origins == ["http://x.com", "http://y.com"]


def test_auth_audiences_json_array_parsing(monkeypatch):
    monkeypatch.setenv("HHH_BO_GATEWAY_AUTH_AUDIENCES", '["foo","bar"]')
    s = Settings()
    assert s.auth_audiences == ["foo", "bar"]


def test_cors_origins_single_value(monkeypatch):
    monkeypatch.setenv("HHH_BO_GATEWAY_CORS_ORIGINS", "http://only-one.com")
    s = Settings()
    assert s.cors_origins == ["http://only-one.com"]


def test_log_level_rejects_unknown_value(monkeypatch):
    monkeypatch.setenv("HHH_BO_GATEWAY_LOG_LEVEL", "VERBOSE")
    with pytest.raises(ValidationError):
        Settings()


def test_port_rejects_out_of_range(monkeypatch):
    monkeypatch.setenv("HHH_BO_GATEWAY_PORT", "70000")
    with pytest.raises(ValidationError):
        Settings()
    monkeypatch.setenv("HHH_BO_GATEWAY_PORT", "0")
    with pytest.raises(ValidationError):
        Settings()


def test_auth_partial_config_rejected(monkeypatch):
    monkeypatch.setenv("HHH_BO_GATEWAY_AUTH_JWKS_URL", "http://jwks.local/.well-known/jwks.json")
    monkeypatch.setenv("HHH_BO_GATEWAY_AUTH_ISSUER", "")
    monkeypatch.setenv("HHH_BO_GATEWAY_AUTH_AUDIENCES", "")
    with pytest.raises(ValidationError):
        Settings()


def test_mongo_db_default(monkeypatch):
    # WHY: clear the env var if leaked from the surrounding environment to assert the default.
    monkeypatch.delenv("HHH_BO_GATEWAY_MONGO_DB", raising=False)
    assert Settings().mongo_db == "hhh_bo_gateway"


def test_mongo_db_env_var(monkeypatch):
    monkeypatch.setenv("HHH_BO_GATEWAY_MONGO_DB", "custom_db")
    assert Settings().mongo_db == "custom_db"
