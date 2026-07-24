from __future__ import annotations

from collections.abc import AsyncIterator, Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rateforge.application.auth.commands import AuthError, AuthService
from rateforge.application.pricing.use_cases import PricingEngineService, ProductPluginRegistry
from rateforge.application.products.commands import ProductService
from rateforge.application.quotes.commands import QuoteService
from rateforge.application.users.commands import UserService
from rateforge.config import Settings
from rateforge.domain.users.entities import User
from rateforge.infrastructure.database.models.audit import AuditLogModel
from rateforge.infrastructure.database.repositories.auth import SQLAlchemyAuthRepository
from rateforge.infrastructure.database.repositories.products import SQLAlchemyProductRepository
from rateforge.infrastructure.database.repositories.quotes import SQLAlchemyQuoteRepository
from rateforge.infrastructure.database.repositories.users import SQLAlchemyUserRepository
from rateforge.infrastructure.database.session import SessionManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_manager: SessionManager = request.app.state.session_manager
    async with session_manager.session() as session:
        yield session


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_auth_service(
    session: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    user_repo = SQLAlchemyUserRepository(session)
    auth_repo = SQLAlchemyAuthRepository(session)
    return AuthService(settings=settings, user_repo=user_repo, auth_repo=auth_repo)


def get_user_service(
    session: AsyncSession = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(SQLAlchemyUserRepository(session), auth_service)


def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(SQLAlchemyProductRepository(session))


def get_pricing_service(session: AsyncSession = Depends(get_session)) -> PricingEngineService:
    registry = ProductPluginRegistry()
    return PricingEngineService(SQLAlchemyProductRepository(session), registry)


def get_quote_service(
    session: AsyncSession = Depends(get_session),
    pricing_service: PricingEngineService = Depends(get_pricing_service),
) -> QuoteService:
    return QuoteService(SQLAlchemyQuoteRepository(session), pricing_service)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    try:
        return await auth_service.get_current_user(token)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


def require_roles(*roles: str) -> Callable[[User], User]:
    async def checker(current_user: User = Depends(get_current_user)) -> User:
        if roles and not any(role in current_user.roles for role in roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current_user

    return checker


async def write_audit_log(
    session: AsyncSession,
    *,
    actor_user_id: str | None,
    action: str,
    resource_type: str,
    resource_id: str,
    payload: dict[str, object],
) -> None:
    from datetime import UTC, datetime
    from uuid import uuid4

    session.add(
        AuditLogModel(
            id=str(uuid4()),
            actor_user_id=actor_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            payload=payload,
            created_at=datetime.now(UTC),
        )
    )
    await session.flush()


async def list_audit_logs(session: AsyncSession) -> list[AuditLogModel]:
    result = await session.execute(select(AuditLogModel).order_by(AuditLogModel.created_at.desc()))
    return list(result.scalars().all())
