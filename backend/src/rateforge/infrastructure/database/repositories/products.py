from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from rateforge.domain.products.entities import ProductDefinition
from rateforge.infrastructure.database.models.products import ProductModel


class SQLAlchemyProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, entity: ProductDefinition) -> ProductDefinition:
        model = ProductModel(
            id=entity.id,
            slug=entity.slug,
            name=entity.name,
            version=entity.version,
            plugin_path=entity.plugin_path,
            config=entity.config,
            is_active=entity.is_active,
            effective_from=entity.effective_from,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_domain(model)

    async def get(self, entity_id: str) -> ProductDefinition | None:
        model = await self.session.get(ProductModel, entity_id)
        return self._to_domain(model) if model else None

    async def get_by_slug(self, slug: str, version: str | None = None) -> ProductDefinition | None:
        statement = select(ProductModel).where(ProductModel.slug == slug)
        if version is not None:
            statement = statement.where(ProductModel.version == version)
        else:
            statement = statement.order_by(desc(ProductModel.effective_from), desc(ProductModel.version))
        result = await self.session.execute(statement.limit(1))
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list(self) -> list[ProductDefinition]:
        result = await self.session.execute(
            select(ProductModel).order_by(ProductModel.slug.asc(), ProductModel.effective_from.desc())
        )
        return [self._to_domain(model) for model in result.scalars().all()]

    @staticmethod
    def _to_domain(model: ProductModel) -> ProductDefinition:
        return ProductDefinition(
            id=model.id,
            slug=model.slug,
            name=model.name,
            version=model.version,
            plugin_path=model.plugin_path,
            config=dict(model.config),
            is_active=model.is_active,
            effective_from=model.effective_from,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
