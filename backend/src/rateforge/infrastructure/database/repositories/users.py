from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rateforge.domain.users.entities import User
from rateforge.infrastructure.database.models.users import UserModel


class SQLAlchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, entity: User) -> User:
        model = UserModel(
            id=entity.id,
            email=entity.email,
            full_name=entity.full_name,
            hashed_password=entity.hashed_password,
            roles=entity.roles,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_domain(model)

    async def get(self, entity_id: str) -> User | None:
        model = await self.session.get(UserModel, entity_id)
        return self._to_domain(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list(self) -> list[User]:
        result = await self.session.execute(select(UserModel).order_by(UserModel.created_at.desc()))
        return [self._to_domain(model) for model in result.scalars().all()]

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            hashed_password=model.hashed_password,
            roles=list(model.roles),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
