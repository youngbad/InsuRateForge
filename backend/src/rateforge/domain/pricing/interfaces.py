from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from rateforge.domain.products.interfaces import ProductPlugin


@dataclass(slots=True)
class PricingContext:
    product_slug: str
    product_version: str
    plugin: ProductPlugin
    payload: dict[str, Any]
    validated_payload: dict[str, Any] = field(default_factory=dict)
    normalized_payload: dict[str, Any] = field(default_factory=dict)
    base_premium: float = 0.0
    discounts: list[dict[str, Any]] = field(default_factory=list)
    taxes: list[dict[str, Any]] = field(default_factory=list)
    fees: list[dict[str, Any]] = field(default_factory=list)
    calculation: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class PipelineStage(ABC):
    @abstractmethod
    async def execute(self, context: PricingContext) -> PricingContext:
        raise NotImplementedError
