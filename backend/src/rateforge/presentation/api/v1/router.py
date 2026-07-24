from fastapi import APIRouter

from . import (
    audit,
    auth,
    endorsements,
    metrics,
    portfolio,
    pricing,
    products,
    quotes,
    renewals,
    users,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(quotes.router, prefix="/quotes", tags=["quotes"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(renewals.router, prefix="/renewals", tags=["renewals"])
api_router.include_router(endorsements.router, prefix="/endorsements", tags=["endorsements"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
