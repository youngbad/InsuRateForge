from __future__ import annotations

from pathlib import Path

import httpx
import pytest_asyncio

from rateforge.config import Settings
from rateforge.main import create_app


@pytest_asyncio.fixture
async def app():
    db_path = Path("test_rateforge.db")
    if db_path.exists():
        db_path.unlink()
    settings = Settings(
        testing=True,
        database_url=f"sqlite+aiosqlite:///{db_path}",
        redis_url="",
        rabbitmq_url="",
        otlp_endpoint=None,
        secret_key="test-secret-key",
        log_json=False,
        db_auto_create=True,
        cors_origins=["*"],
    )
    application = create_app(settings)
    async with application.router.lifespan_context(application):
        yield application
    if db_path.exists():
        db_path.unlink()


@pytest_asyncio.fixture
async def client(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client
