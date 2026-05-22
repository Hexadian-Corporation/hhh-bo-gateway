import json
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    log_level: str = "DEBUG"

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_database: str = "hhh_bo_gateway"
    host: str = "0.0.0.0"
    port: int = 8010
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:3000", "http://localhost:3001"]
    events_mongo_uri: str = "mongodb://localhost:27017"
    events_db: str = "hhh_events"
    auth_base_url: str = "http://auth-service:8000"

    auth_jwks_url: str
    auth_issuer: str
    auth_audiences: Annotated[list[str], NoDecode]
    auth_leeway_seconds: int = 30
    auth_allow_insecure_jwks: bool = False

    @field_validator("auth_audiences", "cors_origins", mode="before")
    @classmethod
    def _parse_csv_or_json_list(cls, v: object) -> object:
        if isinstance(v, str):
            stripped = v.strip()
            if stripped.startswith("["):
                return json.loads(stripped)
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    model_config = {"env_prefix": "HHH_BO_GATEWAY_"}
