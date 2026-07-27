from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RATEFORGE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = "InsuRateForge"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "dev-secret-key"
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 30
    refresh_token_ttl_minutes: int = 60 * 24 * 7
    database_url: str = "postgresql+asyncpg://rateforge:rateforge@localhost:5432/rateforge"
    redis_url: str = "redis://localhost:6379/0"
    rabbitmq_url: str = "amqp://rateforge:rateforge@localhost:5672//"
    otlp_endpoint: str | None = None
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    log_json: bool = False
    db_echo: bool = False
    db_auto_create: bool = True
    testing: bool = False
    metrics_namespace: str = "rateforge"
    service_version: str = "0.1.0"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if value is None:
            return ["*"]
        if isinstance(value, list):
            return [str(item) for item in value]
        if isinstance(value, str):
            if value.startswith("["):
                return json.loads(value)
            return [item.strip() for item in value.split(",") if item.strip()]
        raise TypeError("Unsupported CORS origins value")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
