from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum

from rateforge.domain.shared.entity import Entity


class QuoteStatus(StrEnum):
    DRAFT = "draft"
    RATED = "rated"
    BOUND = "bound"
    EXPIRED = "expired"


@dataclass(slots=True)
class Quote(Entity):
    product_slug: str = ""
    product_version: str = ""
    user_id: str = ""
    status: str = QuoteStatus.RATED.value
    currency: str = "USD"
    premium: Decimal = Decimal("0.00")
    input_payload: dict[str, object] = field(default_factory=dict)
    normalized_payload: dict[str, object] = field(default_factory=dict)
    output_payload: dict[str, object] = field(default_factory=dict)
