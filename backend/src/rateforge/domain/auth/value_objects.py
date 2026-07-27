from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from rateforge.domain.shared.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class JWTToken(ValueObject):
    token: str
    expires_at: datetime
    token_type: str
