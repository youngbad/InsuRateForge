from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rateforge.domain.quotes.entities import Quote
from rateforge.infrastructure.database.models.quotes import QuoteModel


class SQLAlchemyQuoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, entity: Quote) -> Quote:
        model = QuoteModel(
            id=entity.id,
            product_slug=entity.product_slug,
            product_version=entity.product_version,
            user_id=entity.user_id,
            status=entity.status,
            currency=entity.currency,
            premium=entity.premium,
            input_payload=entity.input_payload,
            normalized_payload=entity.normalized_payload,
            output_payload=entity.output_payload,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_domain(model)

    async def get(self, entity_id: str) -> Quote | None:
        model = await self.session.get(QuoteModel, entity_id)
        return self._to_domain(model) if model else None

    async def list_by_user(self, user_id: str) -> list[Quote]:
        result = await self.session.execute(
            select(QuoteModel).where(QuoteModel.user_id == user_id).order_by(QuoteModel.created_at.desc())
        )
        return [self._to_domain(model) for model in result.scalars().all()]

    @staticmethod
    def _to_domain(model: QuoteModel) -> Quote:
        return Quote(
            id=model.id,
            product_slug=model.product_slug,
            product_version=model.product_version,
            user_id=model.user_id,
            status=model.status,
            currency=model.currency,
            premium=model.premium,
            input_payload=dict(model.input_payload),
            normalized_payload=dict(model.normalized_payload),
            output_payload=dict(model.output_payload),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
