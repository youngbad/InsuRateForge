from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from rateforge.application.pricing.use_cases import PricingEngineService
from rateforge.domain.pricing.entities import PricingResult
from rateforge.infrastructure.observability.metrics import PRICING_COUNTER
from rateforge.presentation.dependencies import get_pricing_service, require_roles

router = APIRouter()


class PricingRequest(BaseModel):
    product_slug: str = Field(min_length=2)
    product_version: str | None = None
    payload: dict[str, object]


@router.post("/preview", response_model=PricingResult)
async def preview_pricing(
    request: PricingRequest,
    pricing_service: PricingEngineService = Depends(get_pricing_service),
    _=Depends(require_roles("admin", "underwriter", "agent", "customer")),
) -> PricingResult:
    PRICING_COUNTER.labels(product_slug=request.product_slug).inc()
    return await pricing_service.rate_quote(
        product_slug=request.product_slug,
        product_version=request.product_version,
        payload=request.payload,
    )
