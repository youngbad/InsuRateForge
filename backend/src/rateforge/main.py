from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import start_http_server

from rateforge.application.products.commands import ProductService
from rateforge.application.products.dtos import RegisterProductDTO
from rateforge.config import Settings, get_settings
from rateforge.infrastructure.cache.redis import RedisCache
from rateforge.infrastructure.database.repositories.products import SQLAlchemyProductRepository
from rateforge.infrastructure.database.session import SessionManager
from rateforge.infrastructure.messaging.broker import configure_broker
from rateforge.infrastructure.observability.logging import configure_logging
from rateforge.infrastructure.observability.metrics import metrics_response
from rateforge.infrastructure.observability.tracing import configure_tracing
from rateforge.presentation.api.v1.router import api_router
from rateforge.presentation.middleware.auth import AuthContextMiddleware
from rateforge.presentation.middleware.logging import RequestLoggingMiddleware
from rateforge.presentation.middleware.metrics import MetricsMiddleware


async def seed_products(session_manager: SessionManager) -> None:
    async with session_manager.session() as session:
        service = ProductService(product_repo=SQLAlchemyProductRepository(session))
        existing = await service.get_by_slug("motor", "2024.1")
        if existing is None:
            await service.register(
                RegisterProductDTO(
                    slug="motor",
                    name="Motor Insurance",
                    version="2024.1",
                    plugin_path="plugins.motor.product:MotorInsuranceProduct",
                    config={"tax_rate": 0.15, "policy_fee": 35.0},
                )
            )


_metrics_server_started = False


def _start_metrics_server() -> None:
    global _metrics_server_started

    if _metrics_server_started:
        return

    try:
        start_http_server(9090)
    except OSError:
        pass

    _metrics_server_started = True


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()
    configure_logging(app_settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        _start_metrics_server()
        session_manager = SessionManager(app_settings)
        if app_settings.db_auto_create:
            await session_manager.create_all()
            await seed_products(session_manager)
        cache = RedisCache(app_settings)
        await cache.connect()
        broker = configure_broker(app_settings.rabbitmq_url, testing=app_settings.testing)
        shutdown_tracing = configure_tracing(app, app_settings, session_manager.engine)
        app.state.settings = app_settings
        app.state.session_manager = session_manager
        app.state.cache = cache
        app.state.broker = broker
        try:
            yield
        finally:
            shutdown_tracing()
            await cache.close()
            await session_manager.close()

    app = FastAPI(title=app_settings.project_name, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(AuthContextMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(MetricsMiddleware)
    app.include_router(api_router, prefix=app_settings.api_v1_prefix)
    app.add_api_route("/metrics", metrics_response, methods=["GET"], include_in_schema=False)
    app.add_api_route("/health", lambda: {"status": "ok"}, methods=["GET"], include_in_schema=False)
    app.add_api_route("/healthz", lambda: {"status": "ok"}, methods=["GET"], include_in_schema=False)
    return app


app = create_app()
