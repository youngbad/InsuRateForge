from __future__ import annotations

from dataclasses import dataclass, field

from rateforge.domain.shared.entity import Entity


@dataclass(slots=True)
class AuthContext(Entity):
    user_id: str = ""
    email: str = ""
    roles: list[str] = field(default_factory=list)
