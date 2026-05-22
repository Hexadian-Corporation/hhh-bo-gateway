from src.infrastructure.config.settings import Settings


def test_default_port_is_8010():
    s = Settings()
    assert s.port == 8010


def test_default_mongo_database():
    s = Settings()
    assert s.mongo_database == "hhh_bo_gateway"


def test_env_prefix_loads_log_level(monkeypatch):
    monkeypatch.setenv("HHH_BO_GATEWAY_LOG_LEVEL", "WARNING")
    s = Settings()
    assert s.log_level == "WARNING"


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
