from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from rateforge.application.pricing.use_cases import PricingEngineService
from rateforge.application.quotes.commands import QuoteService
from rateforge.application.quotes.dtos import CreateQuoteDTO, QuoteDTO
from rateforge.presentation.dependencies import (
    get_current_user,
    get_pricing_service,
    get_quote_service,
    get_session,
    write_audit_log,
)

router = APIRouter()


@router.post("/quotes/{quote_id}", response_model=QuoteDTO)
async def renew_quote(
    quote_id: str,
    quote_service: QuoteService = Depends(get_quote_service),
    pricing_service: PricingEngineService = Depends(get_pricing_service),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> QuoteDTO:
    quote = await quote_service.get(quote_id)
    if quote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    product = await pricing_service.product_repo.get_by_slug(quote.product_slug, quote.product_version)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    plugin = pricing_service.plugin_registry.load(
        slug=product.slug,
        version=product.version,
        plugin_path=product.plugin_path,
        config=product.config,
    )
    renewed_payload = plugin.renew(quote.model_dump())
    renewed_quote = await quote_service.create(
        CreateQuoteDTO(product_slug=quote.product_slug, product_version=quote.product_version, payload=renewed_payload),
        current_user,
    )
    await write_audit_log(
        session,
        actor_user_id=current_user.id,
        action="quote.renewed",
        resource_type="quote",
        resource_id=renewed_quote.id,
        payload={"source_quote_id": quote_id},
    )
    return renewed_quote
