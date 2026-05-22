import json
from typing import Annotated, Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_database: str = "hhh_bo_gateway"
    host: str = "0.0.0.0"
    port: Annotated[int, Field(ge=1, le=65535)] = 8010
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:3000", "http://localhost:3001"]
    auth_jwks_url: str = ""
    auth_issuer: str = ""
    auth_audiences: Annotated[list[str], NoDecode] = []
    auth_leeway_seconds: int = 30

    @field_validator("auth_audiences", "cors_origins", mode="before")
    @classmethod
    def _parse_csv_or_json_list(cls, v: object) -> object:
        if isinstance(v, str):
            stripped = v.strip()
            if stripped.startswith("["):
                return json.loads(stripped)
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @model_validator(mode="after")
    def _validate_auth_config(self) -> "Settings":
        # WHY: empty triple is the bootstrap escape hatch; partial config fails fast.
        provided = (bool(self.auth_jwks_url), bool(self.auth_issuer), bool(self.auth_audiences))
        if any(provided) and not all(provided):
            raise ValueError("auth_jwks_url, auth_issuer, and auth_audiences must all be provided or all be empty.")
        return self

    model_config = SettingsConfigDict(
        env_prefix="HHH_BO_GATEWAY_",
        env_file=".env",
        extra="ignore",
        frozen=True,
    )
