from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class RegisterProductDTO(BaseModel):
    slug: str = Field(min_length=2)
    name: str = Field(min_length=2)
    version: str = Field(min_length=1)
    plugin_path: str = Field(min_length=3)
    config: dict[str, object] = Field(default_factory=dict)
    is_active: bool = True
    effective_from: datetime | None = None


class ProductDTO(BaseModel):
    id: str
    slug: str
    name: str
    version: str
    plugin_path: str
    config: dict[str, object]
    is_active: bool
    effective_from: datetime
