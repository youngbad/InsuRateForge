from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from rateforge.domain.shared.entity import Entity


class UserRole(StrEnum):
    ADMIN = "admin"
    UNDERWRITER = "underwriter"
    AGENT = "agent"
    CUSTOMER = "customer"


@dataclass(slots=True)
class User(Entity):
    email: str = ""
    full_name: str = ""
    hashed_password: str = ""
    roles: list[str] = field(default_factory=lambda: [UserRole.CUSTOMER.value])
    is_active: bool = True
