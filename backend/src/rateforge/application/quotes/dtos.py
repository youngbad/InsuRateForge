from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateQuoteDTO(BaseModel):
    product_slug: str = Field(min_length=2)
    product_version: str | None = None
    payload: dict[str, object]


class QuoteDTO(BaseModel):
    id: str
    product_slug: str
    product_version: str
    user_id: str
    status: str
    currency: str
    premium: float
    input_payload: dict[str, object]
    normalized_payload: dict[str, object]
    output_payload: dict[str, object]
    created_at: datetime
    updated_at: datetime
