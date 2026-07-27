from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from rateforge.application.pricing.use_cases import PricingEngineService
from rateforge.infrastructure.messaging.tasks import run_portfolio_batch
from rateforge.presentation.dependencies import get_pricing_service, require_roles

router = APIRouter()


class PortfolioRunRequest(BaseModel):
    product_slug: str = Field(min_length=2)
    payloads: list[dict[str, object]]


@router.post("/runs")
async def run_portfolio(
    request: PortfolioRunRequest,
    pricing_service: PricingEngineService = Depends(get_pricing_service),
    _=Depends(require_roles("admin", "underwriter", "agent")),
) -> dict[str, object]:
    run_id = str(uuid4())
    aggregate = await pricing_service.run_portfolio(request.product_slug, request.payloads)
    run_portfolio_batch.send(run_id, [result["summary"]["headline"] for result in aggregate["results"]])
    return {"run_id": run_id, **aggregate}
