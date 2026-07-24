from __future__ import annotations

from decimal import Decimal

from sqlalchemy import JSON, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from rateforge.infrastructure.database.base import Base, TimestampMixin


class QuoteModel(Base, TimestampMixin):
    __tablename__ = "quotes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    product_slug: Mapped[str] = mapped_column(String(100), nullable=False)
    product_version: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    premium: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    input_payload: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    normalized_payload: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    output_payload: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
