from __future__ import annotations

from datetime import UTC, datetime

from rateforge.application.products.dtos import ProductDTO, RegisterProductDTO
from rateforge.domain.products.entities import ProductDefinition
from rateforge.infrastructure.database.repositories.products import SQLAlchemyProductRepository


class ProductService:
    def __init__(self, product_repo: SQLAlchemyProductRepository) -> None:
        self.product_repo = product_repo

    async def register(self, command: RegisterProductDTO) -> ProductDTO:
        product = ProductDefinition(
            slug=command.slug,
            name=command.name,
            version=command.version,
            plugin_path=command.plugin_path,
            config=command.config,
            is_active=command.is_active,
            effective_from=command.effective_from or datetime.now(UTC),
        )
        created = await self.product_repo.add(product)
        return self._to_dto(created)

    async def list(self) -> list[ProductDTO]:
        return [self._to_dto(product) for product in await self.product_repo.list()]

    async def get_by_slug(self, slug: str, version: str | None = None) -> ProductDTO | None:
        product = await self.product_repo.get_by_slug(slug, version)
        return self._to_dto(product) if product else None

    @staticmethod
    def _to_dto(product: ProductDefinition) -> ProductDTO:
        return ProductDTO(
            id=product.id,
            slug=product.slug,
            name=product.name,
            version=product.version,
            plugin_path=product.plugin_path,
            config=product.config,
            is_active=product.is_active,
            effective_from=product.effective_from,
        )
