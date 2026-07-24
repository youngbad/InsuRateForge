from __future__ import annotations

from decimal import Decimal

from rateforge.application.pricing.use_cases import PricingEngineService
from rateforge.application.quotes.dtos import CreateQuoteDTO, QuoteDTO
from rateforge.domain.quotes.entities import Quote
from rateforge.domain.users.entities import User
from rateforge.infrastructure.database.repositories.quotes import SQLAlchemyQuoteRepository


class QuoteService:
    def __init__(
        self,
        quote_repo: SQLAlchemyQuoteRepository,
        pricing_service: PricingEngineService,
    ) -> None:
        self.quote_repo = quote_repo
        self.pricing_service = pricing_service

    async def create(self, command: CreateQuoteDTO, actor: User) -> QuoteDTO:
        pricing = await self.pricing_service.rate_quote(
            product_slug=command.product_slug,
            payload=command.payload,
            product_version=command.product_version,
        )
        quote = Quote(
            product_slug=pricing.product_slug,
            product_version=pricing.product_version,
            user_id=actor.id,
            premium=Decimal(str(pricing.total_premium)),
            input_payload=command.payload,
            normalized_payload=pricing.normalized_payload,
            output_payload={
                "summary": pricing.summary,
                "breakdown": pricing.breakdown,
                "total_premium": pricing.total_premium,
            },
        )
        created = await self.quote_repo.add(quote)
        return self._to_dto(created)

    async def get(self, quote_id: str) -> QuoteDTO | None:
        quote = await self.quote_repo.get(quote_id)
        return self._to_dto(quote) if quote else None

    async def list_by_user(self, user_id: str) -> list[QuoteDTO]:
        return [self._to_dto(quote) for quote in await self.quote_repo.list_by_user(user_id)]

    @staticmethod
    def _to_dto(quote: Quote) -> QuoteDTO:
        return QuoteDTO(
            id=quote.id,
            product_slug=quote.product_slug,
            product_version=quote.product_version,
            user_id=quote.user_id,
            status=quote.status,
            currency=quote.currency,
            premium=float(quote.premium),
            input_payload=quote.input_payload,
            normalized_payload=quote.normalized_payload,
            output_payload=quote.output_payload,
            created_at=quote.created_at,
            updated_at=quote.updated_at,
        )
