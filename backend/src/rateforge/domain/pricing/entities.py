from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PricingResult:
    product_slug: str
    product_version: str
    currency: str
    base_premium: float
    discounts_total: float
    taxes_total: float
    fees_total: float
    total_premium: float
    breakdown: dict[str, object] = field(default_factory=dict)
    normalized_payload: dict[str, object] = field(default_factory=dict)
    summary: dict[str, object] = field(default_factory=dict)
