from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from rateforge.domain.shared.entity import Entity


@dataclass(slots=True)
class ProductDefinition(Entity):
    slug: str = ""
    name: str = ""
    version: str = ""
    plugin_path: str = ""
    config: dict[str, object] = field(default_factory=dict)
    is_active: bool = True
    effective_from: datetime = field(default_factory=lambda: datetime.now(UTC))
